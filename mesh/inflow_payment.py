import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import aiohttp
from fastapi import HTTPException, Request
from pydantic import BaseModel

logger = logging.getLogger("InflowPayment")

INFLOW_STATUS_APPROVED = "APPROVED"
INFLOW_STATUS_PENDING = "PENDING"
INFLOW_STATUS_DECLINED = "DECLINED"
INFLOW_STATUS_EXPIRED = "EXPIRED"
INFLOW_STATUS_CANCELLED = "CANCELLED"
INFLOW_TERMINAL_STATUSES = {
    INFLOW_STATUS_APPROVED,
    INFLOW_STATUS_DECLINED,
    INFLOW_STATUS_EXPIRED,
    INFLOW_STATUS_CANCELLED,
}

DEFAULT_INFLOW_BASE_URL = "https://sandbox.inflowpay.ai"
DEFAULT_CONTEXT_TTL_SECONDS = 1800
DEFAULT_SIGNUP_RATE_LIMIT_SECONDS = 300

# Single-process in-memory request context keyed by inflow requestId.
INFLOW_REQUEST_CONTEXT: dict[str, dict[str, Any]] = {}
INFLOW_SIGNUP_RATE_LIMIT: dict[str, float] = {}

STATUS_REUSE_ALLOWLIST = {
    ("AskHeuristAgent", "check_job_status"),
    ("CaesarResearchAgent", "get_research_result"),
}

INFLOW_TRANSACTION_STATUS_TO_REQUEST_STATUS = {
    "APPROVED": INFLOW_STATUS_APPROVED,
    "PAID": INFLOW_STATUS_APPROVED,
    "POLICY_APPROVED": INFLOW_STATUS_APPROVED,
    "DECLINED": INFLOW_STATUS_DECLINED,
    "POLICY_DECLINED": INFLOW_STATUS_DECLINED,
    "EXPIRED": INFLOW_STATUS_EXPIRED,
    "CANCELLED": INFLOW_STATUS_CANCELLED,
}


class InflowPayment(BaseModel):
    provider: str
    user_id: str
    currency: str = "USDC"
    request_id: Optional[str] = None


class InflowSignupRequest(BaseModel):
    locale: Optional[str] = "EN_US"
    timezone: Optional[str] = "US/Pacific"


class InflowSignupAttachRequest(BaseModel):
    privateKey: str
    email: str
    firstName: str
    lastName: str
    password: str


@dataclass
class InflowVerificationResult:
    approved: bool
    inflow_status: str
    inflow_request: dict[str, Any]
    context: dict[str, Any]
    reused: bool = False


def is_inflow_payment_request(payment: Optional[InflowPayment]) -> bool:
    if not payment:
        return False
    return payment.provider.upper() == "INFLOW"


def _get_context_ttl_seconds() -> int:
    raw = os.getenv("INFLOW_REQUEST_CONTEXT_TTL_SECONDS", str(DEFAULT_CONTEXT_TTL_SECONDS))
    try:
        ttl = int(raw)
        return ttl if ttl > 0 else DEFAULT_CONTEXT_TTL_SECONDS
    except ValueError:
        return DEFAULT_CONTEXT_TTL_SECONDS


def _get_signup_rate_limit_seconds() -> int:
    raw = os.getenv("INFLOW_SIGNUP_IP_RATE_LIMIT_SECONDS", str(DEFAULT_SIGNUP_RATE_LIMIT_SECONDS))
    try:
        value = int(raw)
        return value if value > 0 else DEFAULT_SIGNUP_RATE_LIMIT_SECONDS
    except ValueError:
        return DEFAULT_SIGNUP_RATE_LIMIT_SECONDS


def _cleanup_expired_context() -> None:
    now = time.time()
    for request_id in list(INFLOW_REQUEST_CONTEXT.keys()):
        expires_at = INFLOW_REQUEST_CONTEXT[request_id].get("expires_at", 0)
        if expires_at <= now:
            INFLOW_REQUEST_CONTEXT.pop(request_id, None)


def _cleanup_signup_rate_limit(now: float, window_seconds: int) -> None:
    for ip in list(INFLOW_SIGNUP_RATE_LIMIT.keys()):
        if now - INFLOW_SIGNUP_RATE_LIMIT[ip] >= window_seconds:
            INFLOW_SIGNUP_RATE_LIMIT.pop(ip, None)


def get_client_ip_from_request(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for", "").strip()
    if x_forwarded_for:
        # First IP in X-Forwarded-For is the originating client IP.
        return x_forwarded_for.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def enforce_signup_rate_limit(client_ip: str) -> None:
    now = time.time()
    window_seconds = _get_signup_rate_limit_seconds()
    _cleanup_signup_rate_limit(now, window_seconds)

    last_request_at = INFLOW_SIGNUP_RATE_LIMIT.get(client_ip)
    if last_request_at is not None:
        elapsed = now - last_request_at
        if elapsed < window_seconds:
            retry_after = int(window_seconds - elapsed)
            raise HTTPException(
                status_code=429,
                detail=f"Too many signup requests from this IP. Try again in {retry_after} seconds.",
            )

    INFLOW_SIGNUP_RATE_LIMIT[client_ip] = now


def _hash_request_payload(agent_id: str, input_payload: Dict[str, Any], user_id: str) -> str:
    payload = {
        "agent_id": agent_id,
        "tool": input_payload.get("tool"),
        "tool_arguments": input_payload.get("tool_arguments", {}),
        "user_id": user_id,
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _inflow_base_url() -> str:
    return os.getenv("INFLOW_BASE_URL", DEFAULT_INFLOW_BASE_URL).rstrip("/")


def _inflow_api_key() -> str:
    api_key = os.getenv("INFLOW_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="INFLOW_API_KEY is not configured")
    return api_key


async def _inflow_request(method: str, path: str, json_data: Optional[dict[str, Any]] = None) -> tuple[int, dict[str, Any]]:
    url = f"{_inflow_base_url()}{path}"
    headers = {"X-API-Key": _inflow_api_key(), "Content-Type": "application/json"}
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request(method, url, headers=headers, json=json_data) as response:
            try:
                body = await response.json(content_type=None)
                if not isinstance(body, dict):
                    body = {"raw": body}
            except Exception:
                body = {"raw": await response.text()}
            return response.status, body


async def _inflow_request_with_api_key(
    method: str,
    path: str,
    api_key: str,
    json_data: Optional[dict[str, Any]] = None,
) -> tuple[int, dict[str, Any]]:
    url = f"{_inflow_base_url()}{path}"
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request(method, url, headers=headers, json=json_data) as response:
            try:
                body = await response.json(content_type=None)
                if not isinstance(body, dict):
                    body = {"raw": body}
            except Exception:
                body = {"raw": await response.text()}
            return response.status, body


def _http_error_from_inflow(status_code: int, message: str, inflow_body: dict[str, Any]) -> HTTPException:
    mapped_status = 502 if status_code >= 500 else 400
    return HTTPException(status_code=mapped_status, detail={"message": message, "inflow": inflow_body})


def _build_payment_response(
    response_status: str,
    request_id: str,
    inflow_status: str,
    message: str,
    inflow_request: Optional[dict[str, Any]] = None,
) -> dict:
    payload = {
        "status": response_status,
        "payment": {
            "provider": "INFLOW",
            "request_id": request_id,
            "inflow_status": inflow_status,
            "message": message,
        },
    }
    if inflow_request is not None:
        payload["payment"]["inflow_request"] = inflow_request
    return payload


def build_payment_pending_response(request_id: str, inflow_request: Optional[dict[str, Any]] = None) -> dict:
    return _build_payment_response(
        "payment_pending",
        request_id,
        INFLOW_STATUS_PENDING,
        "Approve this payment in Inflow, then retry /mesh_request with the same payment.request_id.",
        inflow_request,
    )


def build_payment_not_ready_response(request_id: str, inflow_status: str, inflow_request: dict[str, Any]) -> dict:
    message = (
        "Payment is still pending. Approve in Inflow and retry."
        if inflow_status == INFLOW_STATUS_PENDING
        else f"Payment status is {inflow_status}. Tool execution is blocked."
    )
    response_status = "payment_pending" if inflow_status == INFLOW_STATUS_PENDING else "payment_not_approved"
    return _build_payment_response(response_status, request_id, inflow_status, message, inflow_request)


async def create_inflow_payment_request(
    payment: InflowPayment, agent_id: str, input_payload: Dict[str, Any], amount_usd: float
) -> dict:
    if payment.currency != "USDC":
        raise HTTPException(status_code=400, detail="Only USDC is supported for Inflow payments")

    payload = {
        "userId": payment.user_id,
        "amount": round(max(amount_usd, 0.01), 2),
        "currency": payment.currency,
        "display": "HEADLESS",
        "userDetails": [],
    }

    status_code, inflow_body = await _inflow_request("POST", "/v1/requests/payment", json_data=payload)
    if status_code != 200:
        raise _http_error_from_inflow(status_code, "Failed to create Inflow payment request", inflow_body)

    request_id = inflow_body.get("requestId")
    if not request_id:
        raise HTTPException(
            status_code=502,
            detail={"message": "Inflow response missing requestId", "inflow": inflow_body},
        )

    _cleanup_expired_context()
    now = time.time()
    INFLOW_REQUEST_CONTEXT[request_id] = {
        "request_id": request_id,
        "transaction_id": inflow_body.get("transactionId"),
        "inflow_user_id": payment.user_id,
        "agent_id": agent_id,
        "tool_name": input_payload.get("tool"),
        "tool_args_hash": _hash_request_payload(agent_id, input_payload, payment.user_id),
        "status": inflow_body.get("status", INFLOW_STATUS_PENDING),
        "approved": False,
        "consumed": False,
        "created_at": now,
        "expires_at": now + _get_context_ttl_seconds(),
    }

    return {"request_id": request_id, "inflow_request": inflow_body}


async def _get_inflow_request(request_id: str) -> dict[str, Any]:
    status_code, inflow_body = await _inflow_request("GET", f"/v1/requests/{request_id}")
    if status_code != 200:
        raise _http_error_from_inflow(status_code, "Failed to fetch Inflow request status", inflow_body)
    return inflow_body


async def _get_inflow_transaction(transaction_id: str) -> dict[str, Any] | None:
    status_code, inflow_body = await _inflow_request("GET", f"/v1/transactions/{transaction_id}")
    if status_code == 200:
        return inflow_body
    return None


async def _find_transaction_by_approval_id(approval_id: str, limit: int = 20) -> dict[str, Any] | None:
    status_code, inflow_body = await _inflow_request("GET", f"/v1/transactions?limit={limit}")
    if status_code != 200:
        return None

    data = inflow_body.get("data")
    if not isinstance(data, list):
        return None

    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("approvalId") == approval_id:
            return item
    return None


def _extract_inflow_error_codes(inflow_body: dict[str, Any]) -> set[str]:
    errors = inflow_body.get("errors")
    if not isinstance(errors, list):
        return set()
    codes: set[str] = set()
    for item in errors:
        if not isinstance(item, dict):
            continue
        code = item.get("code")
        if isinstance(code, str) and code:
            codes.add(code)
    return codes


def _derive_request_status_from_transaction(transaction_status: Any) -> str:
    status_upper = str(transaction_status or "").upper()
    if status_upper in INFLOW_TRANSACTION_STATUS_TO_REQUEST_STATUS:
        return INFLOW_TRANSACTION_STATUS_TO_REQUEST_STATUS[status_upper]
    return INFLOW_STATUS_PENDING


def _build_request_from_transaction(request_id: str, transaction: dict[str, Any]) -> dict[str, Any]:
    return {
        "object": "Request",
        "requestId": request_id,
        "status": _derive_request_status_from_transaction(transaction.get("status")),
        "type": "PAYMENT",
        "transactionId": transaction.get("transactionId"),
        "source": "transaction_fallback",
        "transaction": transaction,
    }


async def _get_inflow_request_with_transaction_fallback(request_id: str, context: dict[str, Any]) -> dict[str, Any]:
    status_code, inflow_body = await _inflow_request("GET", f"/v1/requests/{request_id}")
    if status_code == 200:
        return inflow_body

    # Some accounts can access payment status via transactions but not /requests.
    # Fallback to seller-visible transaction records when approval lookup is unavailable.
    if status_code == 404 and "APPROVAL_NOT_FOUND" in _extract_inflow_error_codes(inflow_body):
        transaction_id = context.get("transaction_id")
        tx: dict[str, Any] | None = None
        if isinstance(transaction_id, str) and transaction_id:
            tx = await _get_inflow_transaction(transaction_id)

        if tx is None:
            tx = await _find_transaction_by_approval_id(request_id)

        if tx is not None:
            return _build_request_from_transaction(request_id, tx)

    raise _http_error_from_inflow(status_code, "Failed to fetch Inflow request status", inflow_body)


async def signup_inflow_agentic_user(payload: InflowSignupRequest) -> dict[str, Any]:
    request_payload: dict[str, Any] = {}
    if payload.locale:
        request_payload["locale"] = payload.locale
    if payload.timezone:
        request_payload["timezone"] = payload.timezone

    status_code, inflow_body = await _inflow_request("POST", "/v1/users/agentic", json_data=request_payload)
    if status_code != 200:
        raise _http_error_from_inflow(status_code, "Failed to create Inflow agentic user", inflow_body)

    return {"status": "success", "data": inflow_body}


def _validate_attach_password(password: str) -> None:
    if len(password) < 10:
        raise HTTPException(status_code=400, detail="Password must be at least 10 characters")
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(not ch.isalnum() for ch in password)
    if not (has_upper and has_lower and has_digit and has_symbol):
        raise HTTPException(
            status_code=400,
            detail="Password must include uppercase, lowercase, number, and symbol",
        )


async def attach_inflow_agentic_user(payload: InflowSignupAttachRequest) -> dict[str, Any]:
    _validate_attach_password(payload.password)
    attach_payload = {
        "email": payload.email,
        "firstName": payload.firstName,
        "lastName": payload.lastName,
        "password": payload.password,
    }
    status_code, inflow_body = await _inflow_request_with_api_key(
        "POST",
        "/v1/users/agentic/attach",
        api_key=payload.privateKey,
        json_data=attach_payload,
    )
    if status_code != 200:
        raise _http_error_from_inflow(status_code, "Failed to attach details to Inflow agentic user", inflow_body)

    return {"status": "success", "data": inflow_body}


def _is_allowlisted_status_tool(agent_id: str, input_payload: Dict[str, Any]) -> bool:
    return (agent_id, input_payload.get("tool")) in STATUS_REUSE_ALLOWLIST


def _is_valid_status_reuse(payment: InflowPayment, agent_id: str, input_payload: Dict[str, Any], context: dict[str, Any]) -> bool:
    if not _is_allowlisted_status_tool(agent_id, input_payload):
        return False
    if not context.get("approved"):
        return False
    if context.get("inflow_user_id") != payment.user_id:
        return False
    if context.get("agent_id") != agent_id:
        return False

    tool_name = input_payload.get("tool")
    tool_args = input_payload.get("tool_arguments", {}) or {}
    if tool_name == "check_job_status":
        return context.get("linked_job_id") == tool_args.get("job_id")
    if tool_name == "get_research_result":
        return context.get("linked_research_id") == tool_args.get("research_id")
    return False


async def verify_inflow_request(
    payment: InflowPayment, agent_id: str, input_payload: Dict[str, Any]
) -> InflowVerificationResult:
    _cleanup_expired_context()

    request_id = payment.request_id
    if not request_id:
        raise HTTPException(status_code=400, detail="payment.request_id is required for verification")

    context = INFLOW_REQUEST_CONTEXT.get(request_id)
    if not context:
        raise HTTPException(status_code=400, detail="Invalid or expired payment.request_id")

    if _is_valid_status_reuse(payment, agent_id, input_payload, context):
        return InflowVerificationResult(
            approved=True,
            inflow_status=INFLOW_STATUS_APPROVED,
            inflow_request={"requestId": request_id, "status": INFLOW_STATUS_APPROVED, "type": "PAYMENT"},
            context=context,
            reused=True,
        )

    if context.get("consumed"):
        raise HTTPException(status_code=400, detail="payment.request_id was already consumed")

    if context.get("expires_at", 0) <= time.time():
        INFLOW_REQUEST_CONTEXT.pop(request_id, None)
        raise HTTPException(status_code=400, detail="payment.request_id expired")

    if context.get("inflow_user_id") != payment.user_id or context.get("agent_id") != agent_id:
        raise HTTPException(status_code=400, detail="payment.request_id does not match user or agent")

    expected_hash = _hash_request_payload(agent_id, input_payload, payment.user_id)
    if expected_hash != context.get("tool_args_hash"):
        raise HTTPException(status_code=400, detail="payment.request_id payload mismatch")

    inflow_request = await _get_inflow_request_with_transaction_fallback(request_id, context)
    inflow_status = inflow_request.get("status", INFLOW_STATUS_PENDING)
    context["status"] = inflow_status
    transaction_id = inflow_request.get("transactionId")
    if isinstance(transaction_id, str) and transaction_id:
        context["transaction_id"] = transaction_id
    context["last_checked_at"] = time.time()
    if inflow_status == INFLOW_STATUS_APPROVED:
        context["approved"] = True
        return InflowVerificationResult(
            approved=True,
            inflow_status=inflow_status,
            inflow_request=inflow_request,
            context=context,
            reused=False,
        )

    return InflowVerificationResult(
        approved=False,
        inflow_status=inflow_status,
        inflow_request=inflow_request,
        context=context,
        reused=False,
    )


async def process_inflow_mesh_request(
    *,
    payment: InflowPayment,
    agent_id: str,
    input_payload: Dict[str, Any],
    heurist_api_key: Optional[str],
    agent: Any,
    agent_credits: float,
) -> Dict[str, Any]:
    tool_name = input_payload.get("tool")
    if not tool_name:
        raise HTTPException(status_code=400, detail="Inflow payment path requires input.tool")
    if input_payload.get("query"):
        raise HTTPException(status_code=400, detail="Inflow payment path does not support input.query")

    # First call: create payment request and return request_id.
    if not payment.request_id:
        created = await create_inflow_payment_request(
            payment=payment,
            agent_id=agent_id,
            input_payload=input_payload,
            amount_usd=max(float(agent_credits) / 100, 0.01),
        )
        return build_payment_pending_response(
            request_id=created["request_id"],
            inflow_request=created.get("inflow_request"),
        )

    verification = await verify_inflow_request(
        payment=payment,
        agent_id=agent_id,
        input_payload=input_payload,
    )
    if not verification.approved:
        return build_payment_not_ready_response(
            request_id=payment.request_id,
            inflow_status=verification.inflow_status,
            inflow_request=verification.inflow_request,
        )

    try:
        if heurist_api_key:
            agent.set_heurist_api_key(heurist_api_key)

        result = await agent.call_agent(dict(input_payload))
        finalize_inflow_execution(payment.request_id, tool_name, result)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing inflow request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


def finalize_inflow_execution(request_id: str, tool_name: str, result: Dict[str, Any]) -> None:
    context = INFLOW_REQUEST_CONTEXT.get(request_id)
    if not context:
        return

    context["approved"] = True
    context["approved_at"] = time.time()
    context["consumed"] = True
    context["status"] = "CONSUMED"

    data = result.get("data", {}) if isinstance(result, dict) else {}
    if not isinstance(data, dict):
        return

    if tool_name == "ask_heurist":
        job_id = data.get("job_id")
        if job_id:
            context["linked_job_id"] = job_id
    elif tool_name == "caesar_research":
        nested = data.get("data", {})
        if isinstance(nested, dict):
            research_id = nested.get("research_id")
            if research_id:
                context["linked_research_id"] = research_id
