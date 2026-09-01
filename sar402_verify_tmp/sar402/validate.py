# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/validate.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""SAR-402 validation: schema + authority boundary + continuity semantics.

`validate_receipt` is the entry point a future SAR-402 agent calls. It layers
three checks that together preserve the governing architecture in code:

    1. Structural schema validation (schema.py; jsonschema or local fallback).
    2. Authority-boundary guard (this module). Broader than the schema's single
       `default_verifier` denylist: a normalized forbidden-identity check that
       rejects any gate controller implying DefaultVerifier, Default Settlement,
       Morpheus, SettlementWitness, or this SAR-402 implementation itself, and
       enforces verifier_has_execution_authority == false everywhere.
    3. Continuity-semantics guard: executor_continuity cannot be PASS at a
       pre-delivery seam without delivery evidence.

The verifier never holds execution authority. A PASS does not release anything.
"""

from __future__ import annotations

import json
import re
from typing import List

from . import constants
from .schema import active_backend, schema_errors


class SAR402ValidationError(ValueError):
    """A receipt failed SAR-402 validation."""

    def __init__(self, errors):
        if isinstance(errors, str):
            errors = [errors]
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class AuthorityBoundaryError(SAR402ValidationError):
    """A receipt violated the SAR-402 authority boundary."""


# ---------------------------------------------------------------------------
# Authority-boundary guard
# ---------------------------------------------------------------------------

def _normalize_identity(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def is_forbidden_gate_controller(value) -> bool:
    """True if `value` names or implies an identity that must never be the gate
    controller (the verifier / trust system / this node / witness / this
    implementation). Normalized substring match, not a single literal denylist."""
    if not isinstance(value, str) or not value.strip():
        # An empty / non-string gate controller is not a *forbidden identity*
        # here; the missing-field case is handled by required-field checks.
        return False
    normalized = _normalize_identity(value)
    return any(token in normalized for token in constants.FORBIDDEN_GATE_CONTROLLER_TOKENS)


def authority_boundary_errors(receipt: dict) -> List[str]:
    errors: List[str] = []
    binding = receipt.get("authority_binding")
    if not isinstance(binding, dict):
        errors.append("authority_binding: missing or not an object")
        return errors

    if binding.get("verifier_has_execution_authority") is not False:
        errors.append(
            "authority_binding.verifier_has_execution_authority must be exactly false "
            "(the verifier never holds execution authority)"
        )

    if receipt.get("verification_mode") == "gate":
        controller = binding.get("gate_controller")
        if not controller:
            errors.append("authority_binding.gate_controller is required in gate mode")
        elif is_forbidden_gate_controller(controller):
            errors.append(
                f"authority_binding.gate_controller {controller!r} implies a forbidden "
                "identity (verifier / Default Settlement / Morpheus / SettlementWitness / "
                "SAR-402 implementation) and cannot hold release authority"
            )
        if not binding.get("release_policy"):
            errors.append("authority_binding.release_policy is required in gate mode")

    return errors


# ---------------------------------------------------------------------------
# Continuity-semantics guard
# ---------------------------------------------------------------------------

def continuity_semantics_errors(receipt: dict) -> List[str]:
    errors: List[str] = []
    continuity = receipt.get("continuity")
    if not isinstance(continuity, dict):
        return errors  # structural validation reports the shape problem
    point = receipt.get("verification_point")
    has_delivery = isinstance(receipt.get("delivery"), dict)
    if (
        point in constants.PRE_DELIVERY_POINTS
        and not has_delivery
        and continuity.get("executor_continuity") == constants.PASS
    ):
        errors.append(
            "continuity.executor_continuity cannot be PASS at a pre-delivery seam "
            f"({point}) without delivery evidence"
        )
    return errors


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def iter_errors(receipt: dict) -> List[str]:
    """Return all SAR-402 validation errors (schema + authority + semantics)."""
    errors = list(schema_errors(receipt))
    errors.extend(authority_boundary_errors(receipt))
    errors.extend(continuity_semantics_errors(receipt))
    return errors


def is_valid(receipt: dict) -> bool:
    return not iter_errors(receipt)


def validate_receipt(receipt: dict) -> dict:
    """Validate a receipt; raise SAR402ValidationError on any violation.

    Authority-boundary violations are raised as AuthorityBoundaryError (a
    subclass) when they are the cause, so callers can distinguish them."""
    schema_errs = schema_errors(receipt)
    authority_errs = authority_boundary_errors(receipt)
    semantic_errs = continuity_semantics_errors(receipt)
    all_errs = schema_errs + authority_errs + semantic_errs
    if not all_errs:
        return receipt

    # Authority-boundary classification takes precedence: if the receipt
    # violates the authority boundary, raise the specific error type even when
    # the schema backend independently flags the same field (e.g. the local
    # validator also catches gate_controller=default_verifier).
    if authority_errs:
        raise AuthorityBoundaryError(all_errs)
    raise SAR402ValidationError(all_errs)


def validate_fixture(path) -> dict:
    """Load a fixture file and validate it. Returns the parsed receipt."""
    with open(path, "r", encoding="utf-8") as handle:
        receipt = json.load(handle)
    validate_receipt(receipt)
    return receipt
