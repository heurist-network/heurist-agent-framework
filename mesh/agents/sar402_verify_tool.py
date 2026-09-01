"""The single tool this agent exposes: `verify_settlement_evidence`.

This module contains no verification logic of its own. It:

    1. accepts a Heurist Mesh-shaped `tool_arguments` dict (structured
       execution/service-delivery evidence, with an optional `x402_context`
       passthrough block),
    2. maps it onto the `sar402_verify_tmp.sar402_agent` manual evidence shape
       (reusing the vendored normalizer, builder, and validator verbatim),
    3. fails closed (returns a Mesh-style `{"error": ...}` payload, never a
       guessed verdict) on malformed, incomplete, or authority-violating input,
    4. returns a Mesh-style `{"status": "success", "data": {...}}` payload
       wrapping the full SAR-402 receipt (PASS | FAIL | INDETERMINATE) plus a
       `reproduction` block that lets an independent party recompute the
       receipt's integrity digest without trusting this adapter's own verdict.

x402 context (`x402_context` in the input) is carried through into the
receipt's `notes`/`links` only as supporting/contextual information. This
adapter never claims that a receipt independently proves x402 payment
settlement or finality -- it only evaluates the five committed Continuity
predicates over the evidence it was given.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from sar402_verify_tmp.sar402 import compute_integrity, validate_receipt
from sar402_verify_tmp.sar402_agent import EvidenceError, normalize_manual
from sar402_verify_tmp.sar402_agent.runner import build_receipt

VERIFY_TOOL_NAME = "verify_settlement_evidence"

TOOL_SCHEMA: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": VERIFY_TOOL_NAME,
        "description": (
            "Verify structured execution/service-delivery evidence (optionally "
            "with x402 settlement context) and return a deterministic "
            "PASS | FAIL | INDETERMINATE SAR-402 receipt, reproducible by an "
            "independent verifier. Never releases funds, resources, or holds "
            "execution authority."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["record", "gate"],
                    "description": (
                        "record = post-delivery (requires delivery evidence); "
                        "gate = payment-verified pre-delivery (no delivery yet)."
                    ),
                },
                "payment": {
                    "type": "object",
                    "description": "Quote/settlement constraints (resource, quote_id, price, asset, chain, recipient, payer, payment_ref, ...).",
                },
                "identity": {
                    "type": "object",
                    "description": "Optional agent/wallet/authorized_payers context.",
                },
                "timestamps": {
                    "type": "object",
                    "description": "quoted_at, verified_at, issued_at (required); paid_at, delivered_at, quote_expires_at (optional).",
                },
                "delivery": {
                    "type": "object",
                    "description": "Delivery evidence (record mode only): delivered_resource, evidence_type, evidence_digest, status_code, delivered_at, failed.",
                },
                "authority": {
                    "type": "object",
                    "description": "acting_party (record mode) or gate_controller/release_policy (gate mode). The verifier itself can never be named as gate_controller.",
                },
                "x402_context": {
                    "type": "object",
                    "description": (
                        "Optional supporting x402 facilitator/settlement reference "
                        "(e.g. facilitator id, tx hash). Carried through as context "
                        "only -- this tool does not independently re-verify x402 "
                        "payment finality."
                    ),
                },
            },
            "required": ["mode", "payment", "timestamps"],
        },
    },
}


def _evidence_doc(function_args: Dict[str, Any]) -> Dict[str, Any]:
    """Strip the Mesh-only `x402_context` passthrough key before handing the
    rest to the committed `normalize_manual` shape (which does not know about
    it). x402_context, when present, is folded into `notes` for traceability."""
    doc = {k: v for k, v in function_args.items() if k != "x402_context"}
    return doc


def _x402_note(function_args: Dict[str, Any]) -> Optional[str]:
    ctx = function_args.get("x402_context")
    if not ctx:
        return None
    parts = [f"{k}={v}" for k, v in sorted(ctx.items())]
    return "x402_context(supporting, not independently reverified): " + ", ".join(parts)


def independent_reproduction(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Recompute the receipt's integrity digest independently of the adapter
    that produced it, and re-run the committed schema/authority validator.

    This is the "independent verifier" step: it does not trust the adapter's
    own `sar_verdict` claim -- it recomputes the digest from the receipt body
    (minus the `integrity` block) using the same committed canonicalization the
    builder used, and compares it against the receipt's stated digest. A
    tampered or fabricated receipt will fail this check.
    """
    stated_integrity = receipt.get("integrity")
    body = {k: v for k, v in receipt.items() if k != "integrity"}
    recomputed = compute_integrity(body)
    digest_match = stated_integrity == recomputed

    schema_errors = []
    try:
        validate_receipt(receipt)
        schema_valid = True
    except Exception as exc:  # committed validator raises on any failure
        schema_valid = False
        schema_errors.append(str(exc))

    return {
        "digest_match": digest_match,
        "stated_integrity": stated_integrity,
        "recomputed_integrity": recomputed,
        "schema_valid": schema_valid,
        "schema_errors": schema_errors,
        "reproducible": digest_match and schema_valid,
    }


async def verify_settlement_evidence(
    function_args: Dict[str, Any],
    session_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Mesh-shaped tool handler: normalize -> build (committed) -> validate ->
    attach independent-reproduction evidence. Fails closed on any evidence or
    authority error (never guesses a verdict)."""
    try:
        doc = _evidence_doc(function_args)
        normalized = normalize_manual(doc)
        receipt = build_receipt(normalized)
        validate_receipt(receipt)  # defense in depth, mirrors sar402_agent.runner
    except EvidenceError as exc:
        return {
            "status": "rejected",
            "error": f"evidence rejected ({type(exc).__name__}): {exc}",
        }
    except Exception as exc:  # schema/build errors: fail closed, do not guess
        return {
            "status": "rejected",
            "error": f"verification failed closed ({type(exc).__name__}): {exc}",
        }

    note = _x402_note(function_args)
    if note:
        receipt = dict(receipt)
        receipt["notes"] = (receipt.get("notes") + " | " + note) if receipt.get("notes") else note
        # Notes were appended after the committed builder computed integrity;
        # recompute so the returned receipt's own digest stays self-consistent.
        body = {k: v for k, v in receipt.items() if k != "integrity"}
        receipt["integrity"] = compute_integrity(body)
        validate_receipt(receipt)

    return {
        "status": "success",
        "data": {
            "receipt": receipt,
            "reproduction": independent_reproduction(receipt),
        },
    }
