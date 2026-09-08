# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/builder.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""SAR-402 receipt builder.

Constructs schema-shaped SAR-402 receipt objects from normalized
`SettlementEvidence`. The builder:

    * sets schema_id / profile / sar_type from the committed schema consts,
    * keeps sar_verdict in PASS | FAIL | INDETERMINATE (derived from the five
      Continuity predicates unless explicitly overridden),
    * populates payment_state, delivery_state, settlement_state separately,
    * evaluates and includes the canonical five continuity predicates,
    * always includes authority_binding with verifier_has_execution_authority=false,
    * requires gate_controller + release_policy for gate mode and refuses any
      forbidden gate controller (authority boundary),
    * requires delivery evidence for post-delivery / post-settlement-audit,
    * refuses executor_continuity=PASS pre-delivery without delivery evidence,
    * self-validates output before returning.

It builds receipts; it never releases resources, moves funds, or executes.
"""

from __future__ import annotations

import hashlib
import json
from typing import Dict, List, Optional

from . import constants
from .models import SettlementEvidence
from .predicates import derive_verdict, evaluate_continuity
from .validate import is_forbidden_gate_controller, validate_receipt, AuthorityBoundaryError


# ---------------------------------------------------------------------------
# Identity derivation
# ---------------------------------------------------------------------------

def derive_agent_id(chain: str, payer: str) -> str:
    """Deterministic settlement-derived agent id: agent:x402:<chain>:<payer>."""
    return f"agent:x402:{chain}:{payer}"


# ---------------------------------------------------------------------------
# Canonicalization / integrity
# ---------------------------------------------------------------------------

def canonical_json(obj) -> str:
    """Deterministic JSON: sorted keys, compact separators. Not RFC 8785 JCS."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_integrity(receipt_without_integrity: dict) -> dict:
    digest = hashlib.sha256(
        canonical_json(receipt_without_integrity).encode("utf-8")
    ).hexdigest()
    return {
        "digest_alg": "sha256",
        "canonicalization": constants.CANONICALIZATION,
        "digest": f"sha256:{digest}",
    }


# ---------------------------------------------------------------------------
# Sub-object construction
# ---------------------------------------------------------------------------

def _build_payment(ev: SettlementEvidence) -> dict:
    payment = {
        "resource": ev.resource,
        "quote_id": ev.quote_id,
        "price": ev.price.as_dict(),
    }
    payment["amount_paid"] = ev.effective_amount_paid.as_dict()
    payment["asset"] = ev.asset
    payment["chain"] = ev.chain
    payment["recipient"] = ev.recipient
    payment["payer"] = ev.payer
    payment["payment_ref"] = ev.payment_ref
    if ev.facilitator:
        payment["facilitator"] = ev.facilitator
    return payment


def _build_identity(ev: SettlementEvidence, identity_status: str) -> dict:
    identity = {"payer": ev.payer}
    if ev.agent:
        identity["agent"] = ev.agent
    if ev.wallet:
        identity["wallet"] = ev.wallet
    identity["derived_identity"] = {
        "registration_mode": constants.REGISTRATION_MODE_DERIVED,
        "derived_agent_id": derive_agent_id(ev.chain, ev.payer),
        "identity_status": identity_status,
    }
    return identity


def _build_timestamps(ev: SettlementEvidence) -> dict:
    missing = [
        name
        for name in ("quoted_at", "verified_at", "issued_at")
        if not getattr(ev, name)
    ]
    if missing:
        raise ValueError(
            f"SettlementEvidence missing required timestamp(s): {', '.join(missing)}"
        )
    ts = {"quoted_at": ev.quoted_at}
    if ev.paid_at:
        ts["paid_at"] = ev.paid_at
    ts["verified_at"] = ev.verified_at
    if ev.delivered_at:
        ts["delivered_at"] = ev.delivered_at
    ts["issued_at"] = ev.issued_at
    if ev.quote_expires_at:
        ts["quote_expires_at"] = ev.quote_expires_at
    return ts


def _assemble(
    *,
    ev: SettlementEvidence,
    verification_point: str,
    verification_mode: str,
    authority_binding: dict,
    payment_state: str,
    delivery_state: str,
    settlement_state: str,
    continuity: Dict[str, str],
    sar_verdict: str,
    issuer: dict,
    environment: Optional[str],
    identity_status: str,
    notes: Optional[str],
    links: Optional[List[str]],
    prior_sar_digest: Optional[str],
    include_delivery: bool,
    validate: bool,
) -> dict:
    issuer_block = dict(issuer)
    if environment and "environment" not in issuer_block:
        issuer_block["environment"] = environment

    receipt: dict = {
        "schema_id": constants.SCHEMA_ID,
        "profile": constants.PROFILE,
        "sar_type": constants.SAR_TYPE,
        "sar_verdict": sar_verdict,
        "verification_point": verification_point,
        "verification_mode": verification_mode,
        "authority_binding": authority_binding,
        "payment_state": payment_state,
        "delivery_state": delivery_state,
        "settlement_state": settlement_state,
        "continuity": {name: continuity[name] for name in constants.CONTINUITY_PREDICATES},
        "payment": _build_payment(ev),
    }

    if include_delivery:
        if ev.delivery is None:
            raise ValueError("delivery evidence required but SettlementEvidence.delivery is None")
        receipt["delivery"] = ev.delivery.as_dict()

    receipt["identity"] = _build_identity(ev, identity_status)
    receipt["timestamps"] = _build_timestamps(ev)
    receipt["issuer"] = issuer_block

    if notes:
        receipt["notes"] = notes
    if links:
        receipt["links"] = list(links)
    if prior_sar_digest:
        receipt["prior_sar_digest"] = prior_sar_digest

    receipt["integrity"] = compute_integrity(receipt)

    if validate:
        validate_receipt(receipt)
    return receipt


# ---------------------------------------------------------------------------
# Public builders
# ---------------------------------------------------------------------------

def build_record_mode_receipt(
    ev: SettlementEvidence,
    *,
    acting_party: str = "resource_server",
    issuer: Optional[dict] = None,
    environment: Optional[str] = "test",
    identity_status: str = "derived",
    notes: Optional[str] = None,
    links: Optional[List[str]] = None,
    prior_sar_digest: Optional[str] = None,
    sar_verdict: Optional[str] = None,
    validate: bool = True,
) -> dict:
    """Build a record-mode, post-delivery SAR-402 receipt (the low-friction path).

    Requires delivery evidence. Continuity is evaluated from the evidence and the
    verdict derived from it unless `sar_verdict` is explicitly supplied."""
    if ev.delivery is None:
        raise ValueError("record-mode post-delivery receipt requires ev.delivery")

    continuity = evaluate_continuity(ev)
    verification_point = "post_delivery"
    verdict = sar_verdict or derive_verdict(continuity, verification_point)

    executor = continuity["executor_continuity"]
    if ev.delivery.failed or executor == constants.FAIL:
        delivery_state = "failed"
        settlement_state = "not_delivered"
    elif executor == constants.PASS:
        delivery_state = "confirmed"
        settlement_state = "delivered"
    else:
        delivery_state = "indeterminate"
        settlement_state = "indeterminate"

    payment_state = "verified"

    authority_binding = {
        "acting_party": acting_party,
        "verifier_has_execution_authority": False,
    }

    return _assemble(
        ev=ev,
        verification_point=verification_point,
        verification_mode="record",
        authority_binding=authority_binding,
        payment_state=payment_state,
        delivery_state=delivery_state,
        settlement_state=settlement_state,
        continuity=continuity,
        sar_verdict=verdict,
        issuer=issuer or constants.DEFAULT_ISSUER,
        environment=environment,
        identity_status=identity_status,
        notes=notes,
        links=links,
        prior_sar_digest=prior_sar_digest,
        include_delivery=True,
        validate=validate,
    )


def build_gate_authority_binding(gate_controller: str, release_policy: str) -> dict:
    """Construct (and guard) a gate-mode authority_binding.

    Refuses any gate controller that implies the verifier / Default Settlement /
    Morpheus / SettlementWitness / this SAR-402 implementation."""
    if not gate_controller:
        raise AuthorityBoundaryError("gate_controller is required in gate mode")
    if not release_policy:
        raise AuthorityBoundaryError("release_policy is required in gate mode")
    if is_forbidden_gate_controller(gate_controller):
        raise AuthorityBoundaryError(
            f"gate_controller {gate_controller!r} implies a forbidden identity and "
            "cannot hold release authority"
        )
    return {
        "gate_controller": gate_controller,
        "release_policy": release_policy,
        "verifier_has_execution_authority": False,
    }


def build_gate_mode_receipt(
    ev: SettlementEvidence,
    *,
    gate_controller: str,
    release_policy: str = "release_on_PASS_escalate_on_INDETERMINATE_withhold_on_FAIL",
    issuer: Optional[dict] = None,
    environment: Optional[str] = "test",
    identity_status: str = "derived",
    notes: Optional[str] = None,
    links: Optional[List[str]] = None,
    prior_sar_digest: Optional[str] = None,
    sar_verdict: Optional[str] = None,
    validate: bool = True,
) -> dict:
    """Build a gate-mode, payment-verified-pre-delivery SAR-402 receipt.

    The verifier returns a result; the named gate_controller decides whether to
    release under its own policy. executor_continuity is normally INDETERMINATE
    here (nothing delivered yet). Delivery evidence is not included at this seam."""
    authority_binding = build_gate_authority_binding(gate_controller, release_policy)

    continuity = evaluate_continuity(ev)
    verification_point = "payment_verified_pre_delivery"
    verdict = sar_verdict or derive_verdict(continuity, verification_point)

    return _assemble(
        ev=ev,
        verification_point=verification_point,
        verification_mode="gate",
        authority_binding=authority_binding,
        payment_state="verified",
        delivery_state="not_applicable",
        settlement_state="pending",
        continuity=continuity,
        sar_verdict=verdict,
        issuer=issuer or constants.DEFAULT_ISSUER,
        environment=environment,
        identity_status=identity_status,
        notes=notes,
        links=links,
        prior_sar_digest=prior_sar_digest,
        include_delivery=False,
        validate=validate,
    )
