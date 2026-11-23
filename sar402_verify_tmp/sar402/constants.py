# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/constants.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Canonical SAR-402 constants (vendored, standalone copy).

This is a verbatim-logic copy of Default Settlement's committed
`morpheus/sar402/constants.py`, adapted only so the schema it cross-checks
against is loaded from a package-vendored copy
(`sar402_verify_tmp/sar402/schema_data/sar-402-settlement-v0.1.schema.json`)
instead of a path inside the reference-implementation repository. No predicate, constant
value, or verdict vocabulary was changed. The canonical/authoritative
location of this schema remains
`knowledge-assets/profiles/sar-402/schema/sar-402-settlement-v0.1.schema.json`
in the reference-implementation repository; this package carries a point-in-time copy for
standalone operation and is not itself the authoritative source.

`schema.py` cross-checks the most important of these against the loaded
schema at import time so this module cannot silently drift from the vendored
copy it ships with.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Vendored asset locations (package-relative, no repository coupling)
# ---------------------------------------------------------------------------

_PACKAGE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = _PACKAGE_DIR / "schema_data" / "sar-402-settlement-v0.1.schema.json"

# ---------------------------------------------------------------------------
# Fixed receipt identity (schema consts)
# ---------------------------------------------------------------------------

SCHEMA_ID = "sar_402_settlement_v0.1"
PROFILE = "sar-402"
SAR_TYPE = "Settlement Attestation Receipt"

# ---------------------------------------------------------------------------
# Verdict vocabulary — the ONLY verdict vocabulary. Do not fork.
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
INDETERMINATE = "INDETERMINATE"
VERDICTS = (PASS, FAIL, INDETERMINATE)

# ---------------------------------------------------------------------------
# Three axes
# ---------------------------------------------------------------------------

VERIFICATION_POINTS = (
    "pre_authorization",
    "payment_verified_pre_delivery",
    "post_delivery",
    "post_settlement_audit",
)

VERIFICATION_MODES = ("observe", "gate", "record", "audit")

# Verification points where executor_continuity is legitimately not yet
# knowable (nothing delivered yet). At these points an INDETERMINATE
# executor predicate is expected and does not, by itself, block a PASS verdict.
PRE_DELIVERY_POINTS = ("pre_authorization", "payment_verified_pre_delivery")

# ---------------------------------------------------------------------------
# State fields (separate from sar_verdict and from each other)
# ---------------------------------------------------------------------------

PAYMENT_STATES = ("verified", "unverified", "failed", "indeterminate")
DELIVERY_STATES = ("confirmed", "claimed", "failed", "not_applicable", "indeterminate")
SETTLEMENT_STATES = ("delivered", "not_delivered", "pending", "unverified", "indeterminate")

# ---------------------------------------------------------------------------
# Continuity predicates — the canonical five. Never add, never fork per chain.
# ---------------------------------------------------------------------------

CONTINUITY_PREDICATES = (
    "object_continuity",
    "constraint_continuity",
    "temporal_continuity",
    "authority_continuity",
    "executor_continuity",
)

# ---------------------------------------------------------------------------
# Authority boundary
# ---------------------------------------------------------------------------

# The universal rule: the verifier never holds execution authority.
VERIFIER_HAS_EXECUTION_AUTHORITY = False

# A gate controller must be the external consuming system that controls
# release. It must never be the verifier, the trust system, this node, the
# witness, or this SAR-402 implementation itself. We do NOT rely on a single
# denylisted literal: gate-controller values are normalized (lowercased,
# stripped to [a-z0-9]) and rejected if they contain any forbidden identity
# token. See validate.is_forbidden_gate_controller.
FORBIDDEN_GATE_CONTROLLER_TOKENS = (
    "defaultverifier",
    "defaultsettlement",
    "morpheus",
    "settlementwitness",
    "sar402",
)

# Settlement-derived identity
REGISTRATION_MODE_DERIVED = "derived_from_settlement"
IDENTITY_STATUSES = ("derived", "claimed", "verified", "linked")

DEFAULT_ISSUER = {
    "verifier": "DefaultVerifier",
    "verifier_version": "0.1.0",
}

# Canonicalization label for the local digest. This is honest about what the
# builder actually does (sorted-key compact JSON), and is intentionally NOT
# claimed to be RFC 8785 JCS, which remains out of scope for v0.1.
CANONICALIZATION = "sorted_keys_compact_v0"
