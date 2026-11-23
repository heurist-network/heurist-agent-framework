# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0
# original source file path   : sar402_reference/sar402_agent/normalizer.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Normalizers: ingestion JSON -> internal `NormalizedEvidence`.

Two ingestion shapes are supported in this pass:

    * Option A — the manual / fixture-driven shape (`normalize_manual`): a
      hand-constructed JSON evidence object describing an x402 payment + delivery
      event in agent-friendly field names.
    * Option B — the controlled demo-endpoint shape (`normalize_demo`): a fixed
      local shape for a future `/pay/url-summary`-style demo endpoint, using the
      endpoint's own field names. It normalizes into the *same* internal model.

Both produce a `NormalizedEvidence` wrapping a committed
`sar402_verify_tmp.sar402.SettlementEvidence`. Neither calls a network or a chain; both
operate purely on a local dict. Invalid evidence and authority-boundary
violations are rejected here (cleanly) before the committed builder is invoked.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional

from sar402_verify_tmp.sar402 import Amount, DeliveryEvidence, SettlementEvidence

from .evidence import (
    GATE_MODE,
    RECORD_MODE,
    SUPPORTED_MODES,
    AuthorityViolationError,
    EvidenceValidationError,
    NormalizedEvidence,
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _require_mapping(obj: Any, where: str) -> Mapping:
    if not isinstance(obj, Mapping):
        raise EvidenceValidationError(f"{where}: expected an object, got {type(obj).__name__}")
    return obj


def _require(obj: Mapping, key: str, where: str) -> Any:
    if key not in obj or obj[key] in (None, ""):
        raise EvidenceValidationError(f"{where}: missing required field {key!r}")
    return obj[key]


def _amount(obj: Any, where: str) -> Amount:
    obj = _require_mapping(obj, where)
    return Amount(
        amount=str(_require(obj, "amount", where)),
        asset=str(_require(obj, "asset", where)),
        decimals=int(_require(obj, "decimals", where)),
    )


def _check_authority_block(authority: Mapping, *, where: str) -> None:
    """Reject an authority block that asserts verifier execution authority."""
    vhea = authority.get("verifier_has_execution_authority")
    if vhea is not None and vhea is not False:
        raise AuthorityViolationError(
            f"{where}.verifier_has_execution_authority must be false (or omitted); "
            "the verifier never holds execution authority"
        )


# ---------------------------------------------------------------------------
# Option A — manual / fixture-driven shape
# ---------------------------------------------------------------------------

def normalize_manual(doc: Any) -> NormalizedEvidence:
    """Normalize a manual evidence JSON object into `NormalizedEvidence`.

    Expected shape (record mode adds `delivery`; gate mode adds `authority`):

        {
          "mode": "record" | "gate",
          "payment": { resource, quote_id, price{amount,asset,decimals},
                       amount_paid{...}?, asset, chain, recipient, payer,
                       payment_ref, facilitator? },
          "identity": { agent?, wallet?, authorized_payers?[] },
          "timestamps": { quoted_at, paid_at?, verified_at, delivered_at?,
                          issued_at, quote_expires_at? },
          "delivery": { delivered_resource, evidence_type, evidence_digest?,
                        status_code?, delivered_at?, failed? },     # record mode
          "authority": { gate_controller, release_policy?,
                         acting_party?, verifier_has_execution_authority? }
        }
    """
    doc = _require_mapping(doc, "evidence")
    mode = str(_require(doc, "mode", "evidence")).strip().lower()
    if mode not in SUPPORTED_MODES:
        raise EvidenceValidationError(
            f"evidence.mode {mode!r} unsupported; expected one of {SUPPORTED_MODES}"
        )

    payment = _require_mapping(_require(doc, "payment", "evidence"), "payment")
    identity = doc.get("identity") or {}
    identity = _require_mapping(identity, "identity")
    timestamps = _require_mapping(_require(doc, "timestamps", "evidence"), "timestamps")
    authority = doc.get("authority") or {}
    authority = _require_mapping(authority, "authority")
    _check_authority_block(authority, where="authority")

    price = _amount(_require(payment, "price", "payment"), "payment.price")
    amount_paid = (
        _amount(payment["amount_paid"], "payment.amount_paid")
        if payment.get("amount_paid") is not None
        else None
    )

    delivery = _build_delivery(doc.get("delivery"), where="delivery")

    settlement = SettlementEvidence(
        resource=str(_require(payment, "resource", "payment")),
        quote_id=str(_require(payment, "quote_id", "payment")),
        price=price,
        asset=str(_require(payment, "asset", "payment")),
        chain=str(_require(payment, "chain", "payment")),
        recipient=str(_require(payment, "recipient", "payment")),
        payer=str(_require(payment, "payer", "payment")),
        payment_ref=str(_require(payment, "payment_ref", "payment")),
        amount_paid=amount_paid,
        settled_asset=payment.get("settled_asset"),
        settled_chain=payment.get("settled_chain"),
        settled_recipient=payment.get("settled_recipient"),
        facilitator=payment.get("facilitator"),
        agent=identity.get("agent"),
        wallet=identity.get("wallet"),
        authorized_payers=identity.get("authorized_payers"),
        quoted_at=_require(timestamps, "quoted_at", "timestamps"),
        paid_at=timestamps.get("paid_at"),
        verified_at=_require(timestamps, "verified_at", "timestamps"),
        delivered_at=timestamps.get("delivered_at"),
        issued_at=_require(timestamps, "issued_at", "timestamps"),
        quote_expires_at=timestamps.get("quote_expires_at"),
        delivery=delivery,
    )

    return _assemble_normalized(
        mode=mode,
        settlement=settlement,
        authority=authority,
        source_kind="manual",
    )


# ---------------------------------------------------------------------------
# Option B — controlled demo-endpoint shape (/pay/url-summary style)
# ---------------------------------------------------------------------------

def normalize_demo(doc: Any) -> NormalizedEvidence:
    """Normalize a controlled demo-endpoint evidence object into the same model.

    This is the fixed local shape a future `/pay/url-summary`-style demo endpoint
    would emit. It uses the endpoint's own field names (quote / payment / delivery
    sub-objects) and is mapped here onto the identical internal model. No live
    endpoint is called in this pass.

        {
          "endpoint": "/pay/url-summary",
          "mode": "record" | "gate",
          "request": { "target_url": "..." },
          "x402": {
            "quote":   { id, resource_url, price{value,currency,decimals},
                         pay_to, network, quoted_at, expires_at },
            "payment": { from, tx, paid{value,currency,decimals}?, paid_at,
                         verified_at, facilitator?, authorized_from?[] },
            "delivery":{ url, content_digest?, http_status?, served_at? }?  # record
          },
          "issuer_agent": "...",
          "issued_at": "...",
          "authority": { gate_controller, release_policy?, acting_party?,
                         verifier_has_execution_authority? }
        }
    """
    doc = _require_mapping(doc, "demo_evidence")
    mode = str(_require(doc, "mode", "demo_evidence")).strip().lower()
    if mode not in SUPPORTED_MODES:
        raise EvidenceValidationError(
            f"demo_evidence.mode {mode!r} unsupported; expected one of {SUPPORTED_MODES}"
        )

    x402 = _require_mapping(_require(doc, "x402", "demo_evidence"), "x402")
    quote = _require_mapping(_require(x402, "quote", "x402"), "x402.quote")
    payment = _require_mapping(_require(x402, "payment", "x402"), "x402.payment")
    authority = doc.get("authority") or {}
    authority = _require_mapping(authority, "authority")
    _check_authority_block(authority, where="authority")

    price_obj = _require_mapping(_require(quote, "price", "x402.quote"), "x402.quote.price")
    price = Amount(
        amount=str(_require(price_obj, "value", "x402.quote.price")),
        asset=str(_require(price_obj, "currency", "x402.quote.price")),
        decimals=int(_require(price_obj, "decimals", "x402.quote.price")),
    )
    paid_obj = payment.get("paid")
    amount_paid: Optional[Amount] = None
    if paid_obj is not None:
        paid_obj = _require_mapping(paid_obj, "x402.payment.paid")
        amount_paid = Amount(
            amount=str(_require(paid_obj, "value", "x402.payment.paid")),
            asset=str(_require(paid_obj, "currency", "x402.payment.paid")),
            decimals=int(_require(paid_obj, "decimals", "x402.payment.paid")),
        )

    resource = str(_require(quote, "resource_url", "x402.quote"))

    delivery = None
    delivery_doc = x402.get("delivery")
    if delivery_doc is not None:
        delivery_doc = _require_mapping(delivery_doc, "x402.delivery")
        delivery = DeliveryEvidence(
            delivered_resource=str(_require(delivery_doc, "url", "x402.delivery")),
            evidence_type=str(delivery_doc.get("evidence_type", "http_response")),
            evidence_digest=delivery_doc.get("content_digest"),
            status_code=delivery_doc.get("http_status"),
            delivered_at=delivery_doc.get("served_at"),
            failed=bool(delivery_doc.get("failed", False)),
        )

    settlement = SettlementEvidence(
        resource=resource,
        quote_id=str(_require(quote, "id", "x402.quote")),
        price=price,
        asset=str(_require(price_obj, "currency", "x402.quote.price")),
        chain=str(_require(quote, "network", "x402.quote")),
        recipient=str(_require(quote, "pay_to", "x402.quote")),
        payer=str(_require(payment, "from", "x402.payment")),
        payment_ref=str(_require(payment, "tx", "x402.payment")),
        amount_paid=amount_paid,
        facilitator=payment.get("facilitator"),
        agent=doc.get("issuer_agent"),
        wallet=payment.get("from"),
        authorized_payers=payment.get("authorized_from"),
        quoted_at=_require(quote, "quoted_at", "x402.quote"),
        paid_at=payment.get("paid_at"),
        verified_at=_require(payment, "verified_at", "x402.payment"),
        delivered_at=(delivery.delivered_at if delivery else None),
        issued_at=_require(doc, "issued_at", "demo_evidence"),
        quote_expires_at=quote.get("expires_at"),
        delivery=delivery,
    )

    return _assemble_normalized(
        mode=mode,
        settlement=settlement,
        authority=authority,
        source_kind="demo_url_summary",
    )


# ---------------------------------------------------------------------------
# Shared assembly
# ---------------------------------------------------------------------------

def _build_delivery(doc: Any, *, where: str) -> Optional[DeliveryEvidence]:
    if doc is None:
        return None
    doc = _require_mapping(doc, where)
    return DeliveryEvidence(
        delivered_resource=str(_require(doc, "delivered_resource", where)),
        evidence_type=str(_require(doc, "evidence_type", where)),
        evidence_digest=doc.get("evidence_digest"),
        status_code=doc.get("status_code"),
        delivered_at=doc.get("delivered_at"),
        failed=bool(doc.get("failed", False)),
    )


def _assemble_normalized(
    *,
    mode: str,
    settlement: SettlementEvidence,
    authority: Mapping,
    source_kind: str,
) -> NormalizedEvidence:
    acting_party = authority.get("acting_party") or "resource_server"
    gate_controller = authority.get("gate_controller") if mode == GATE_MODE else None
    release_policy = authority.get("release_policy") if mode == GATE_MODE else None
    if mode == GATE_MODE and not release_policy:
        # Provide the canonical default policy so gate evidence that names a
        # controller but omits the policy string is still explicit, not blank.
        release_policy = "release_on_PASS_escalate_on_INDETERMINATE_withhold_on_FAIL"

    # NormalizedEvidence.__post_init__ performs the authority / seam invariants.
    return NormalizedEvidence(
        mode=mode,
        settlement=settlement,
        source_kind=source_kind,
        acting_party=acting_party,
        gate_controller=gate_controller,
        release_policy=release_policy,
    )


def normalize(doc: Any, *, source: str = "manual") -> NormalizedEvidence:
    """Dispatch to the right normalizer by source ("manual" | "demo")."""
    if source == "manual":
        return normalize_manual(doc)
    if source == "demo":
        return normalize_demo(doc)
    raise EvidenceValidationError(f"unknown evidence source {source!r}")
