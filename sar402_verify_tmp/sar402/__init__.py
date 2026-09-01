# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/__init__.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
#
# TRIMMED relative to the canonical __init__.py: `samples` (test/demo-only
# fixtures, never invoked by the Mesh tool) is intentionally NOT imported or
# re-exported here. See sar402_verify_tmp/EXCLUDED.md for the full exclusion
# list and rationale.
# -----------------------------------------------------------------------------
"""SAR-402 -- local, network-free, NON-CANONICAL temporary copy.

SAR means Settlement Attestation Receipt. SAR-402 is an x402-specific *profile*
of SAR, not the whole Default Settlement system and not a new primitive.

This is a disposable, unpublished, local copy of the minimum SAR-402
verification surface needed by a Heurist Mesh candidate tool. It is NOT a new
standard, NOT an authoritative SAR-402 implementation, and NOT a package
release. The canonical implementation is the SAR-402 reference implementation's `sar402/` package.

Authority boundary (non-negotiable): the verifier never holds custody, moves
funds, releases resources, executes actions, or enforces decisions.
verifier_has_execution_authority is always false. In gate mode the verifier
returns a result; the named external gate_controller decides whether to act.
"""

from __future__ import annotations

from . import constants, predicates
from .builder import (
    build_gate_authority_binding,
    build_gate_mode_receipt,
    build_record_mode_receipt,
    canonical_json,
    compute_integrity,
    derive_agent_id,
)
from .constants import FAIL, INDETERMINATE, PASS
from .models import Amount, DeliveryEvidence, SettlementEvidence, parse_timestamp
from .predicates import derive_verdict, evaluate_continuity
from .schema import active_backend, load_schema, schema_errors
from .validate import (
    AuthorityBoundaryError,
    SAR402ValidationError,
    is_forbidden_gate_controller,
    is_valid,
    iter_errors,
    validate_fixture,
    validate_receipt,
)

__all__ = [
    "constants",
    "predicates",
    # verdicts
    "PASS",
    "FAIL",
    "INDETERMINATE",
    # models
    "Amount",
    "DeliveryEvidence",
    "SettlementEvidence",
    "parse_timestamp",
    # predicates
    "evaluate_continuity",
    "derive_verdict",
    # builder
    "build_record_mode_receipt",
    "build_gate_mode_receipt",
    "build_gate_authority_binding",
    "derive_agent_id",
    "canonical_json",
    "compute_integrity",
    # schema
    "load_schema",
    "schema_errors",
    "active_backend",
    # validate
    "validate_receipt",
    "validate_fixture",
    "iter_errors",
    "is_valid",
    "is_forbidden_gate_controller",
    "SAR402ValidationError",
    "AuthorityBoundaryError",
]
