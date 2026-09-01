# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0
# original source file path   : sar402_reference/sar402_agent/__init__.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
#
# TRIMMED relative to the canonical __init__.py: `storage.preserve_run`
# (file-persistence logic, never invoked by the Mesh tool) and
# `normalize_demo` (demo-endpoint ingestion, not used by the manual-evidence
# Mesh tool contract) are intentionally NOT imported or re-exported here.
# `runner` here is the trimmed local copy (see runner.py's own provenance
# header for its own exclusion list). See
# sar402_verify_tmp/EXCLUDED.md for the full exclusion list and rationale.
# -----------------------------------------------------------------------------
"""SAR-402 evidence-ingestion agent layer -- local, network-free, NON-CANONICAL
temporary copy.

This is a disposable, unpublished, local copy of the minimum evidence
normalization + receipt-construction-dispatch surface needed by a Heurist
Mesh candidate tool. It does NOT reinvent receipt construction, define a new
schema, or change the governing SAR-402 architecture. The canonical
implementation is the SAR-402 reference implementation's `sar402_agent/` package.

Authority boundary (non-negotiable, inherited from the canonical package):
the verifier never holds execution authority. In gate mode the named
external gate_controller -- never DefaultVerifier, Default Settlement,
Morpheus, SettlementWitness, or this copy -- decides release under its own
policy. Verification is never execution.
"""

from __future__ import annotations

from .evidence import (
    AuthorityViolationError,
    EvidenceError,
    EvidenceValidationError,
    GATE_MODE,
    NormalizedEvidence,
    RECORD_MODE,
    SUPPORTED_MODES,
)
from .normalizer import normalize_manual
from .runner import build_receipt

__all__ = [
    # errors
    "EvidenceError",
    "EvidenceValidationError",
    "AuthorityViolationError",
    # model / modes
    "NormalizedEvidence",
    "RECORD_MODE",
    "GATE_MODE",
    "SUPPORTED_MODES",
    # normalizers
    "normalize_manual",
    # runner
    "build_receipt",
]
