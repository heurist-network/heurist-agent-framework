import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Point the module-level SQLite context store at a temp file before importing.
_tmp = tempfile.NamedTemporaryFile(prefix="inflow_test_", suffix=".db", delete=False)
_tmp.close()
os.environ["INFLOW_CONTEXT_DB_PATH"] = _tmp.name

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi import HTTPException

from mesh import inflow_payment
from mesh.inflow_payment import InflowPayment


def _context(**overrides):
    context = {
        "request_id": "req-1",
        "transaction_id": None,
        "inflow_user_id": "user-1",
        "agent_id": "AgentA",
        "tool_name": "some_tool",
        "tool_args_hash": "hash",
        "status": "PENDING",
        "approved": False,
        "consumed": False,
        "expected_amount": 0.01,
        "expected_currency": "USDC",
        "created_at": 0,
        "expires_at": 9_999_999_999,
    }
    context.update(overrides)
    return context


def test_verify_approved_payment_passes_on_match():
    async def run():
        await inflow_payment._verify_approved_payment({"transaction": {"amount": 0.01, "currency": "USDC"}}, _context())

    asyncio.run(run())


def test_verify_approved_payment_rejects_amount_mismatch():
    async def run():
        with pytest.raises(HTTPException):
            await inflow_payment._verify_approved_payment(
                {"transaction": {"amount": 5.0, "currency": "USDC"}}, _context()
            )

    asyncio.run(run())


def test_verify_approved_payment_rejects_currency_mismatch():
    async def run():
        with pytest.raises(HTTPException):
            await inflow_payment._verify_approved_payment(
                {"transaction": {"amount": 0.01, "currency": "EURC"}}, _context()
            )

    asyncio.run(run())


def test_verify_inflow_request_rejects_amount_mismatch(monkeypatch):
    agent_id = "AgentA"
    user_id = "user-1"
    input_payload = {"tool": "some_tool", "tool_arguments": {"a": 1}}

    context = _context(
        request_id="req-1",
        inflow_user_id=user_id,
        agent_id=agent_id,
        tool_name="some_tool",
        tool_args_hash=inflow_payment._hash_request_payload(agent_id, input_payload, user_id),
    )
    inflow_payment._context_store.set("req-1", context)

    async def fake_fallback(request_id, ctx):
        return {
            "requestId": "req-1",
            "status": inflow_payment.INFLOW_STATUS_APPROVED,
            "transaction": {"amount": 5.0, "currency": "USDC"},
        }

    monkeypatch.setattr(inflow_payment, "_get_inflow_request_with_transaction_fallback", fake_fallback)

    payment = InflowPayment(provider="INFLOW", user_id=user_id, currency="USDC", request_id="req-1")

    async def run():
        with pytest.raises(HTTPException):
            await inflow_payment.verify_inflow_request(payment, agent_id, input_payload)

    asyncio.run(run())
