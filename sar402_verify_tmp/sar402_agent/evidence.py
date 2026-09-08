# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0
# original source file path   : sar402_reference/sar402_agent/evidence.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Agent-facing normalized evidence model for SAR-402 ingestion.

This is the *single internal model* that every ingestion source (manual JSON,
the controlled demo-endpoint shape, and any future source) normalizes into
before the receipt is built. It is deliberately a thin, explicit container:

    * a `mode` ("record" | "gate") naming the seam/builder to use,
    * a fully-built `sar402_verify_tmp.sar402.SettlementEvidence` (the authoritative
      normalized input the committed builder/validator already understand),
    * gate-mode authority parameters (gate_controller / release_policy) when and
      only when mode == "gate",
    * optional record-mode acting_party for clarity.

The ingestion layer never reinvents receipt construction and never defines a new
schema. It collects/normalizes evidence and hands a `SettlementEvidence` to the
committed `sar402_verify_tmp.sar402` builder, which self-validates against the committed
schema. This module only owns the *agent-facing* normalized shape and the
authority pre-checks that let invalid evidence be rejected cleanly before the
builder is ever called.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sar402_verify_tmp.sar402 import SettlementEvidence
from sar402_verify_tmp.sar402.validate import is_forbidden_gate_controller


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class EvidenceError(ValueError):
    """Base class for ingestion-layer evidence errors."""


class EvidenceValidationError(EvidenceError):
    """Evidence was missing, malformed, or insufficient to build a receipt."""


class AuthorityViolationError(EvidenceError):
    """Evidence attempted to violate a SAR-402 authority boundary.

    Raised, for example, when the input asserts the verifier holds execution
    authority, or names a forbidden gate controller (the verifier / Default
    Settlement / Morpheus / SettlementWitness / this SAR-402 implementation)."""


# Recognized ingestion modes -> the seam each one targets.
RECORD_MODE = "record"
GATE_MODE = "gate"
SUPPORTED_MODES = (RECORD_MODE, GATE_MODE)


@dataclass
class NormalizedEvidence:
    """The internal normalized evidence model produced by every normalizer.

    `settlement` is the authoritative `SettlementEvidence` the committed builder
    consumes. `mode` selects which committed builder to call. Gate parameters are
    present only for gate mode."""

    mode: str
    settlement: SettlementEvidence
    source_kind: str = "manual"
    # record-mode clarity (who actually controlled the action). Never authority.
    acting_party: str = "resource_server"
    # gate-mode authority binding inputs.
    gate_controller: Optional[str] = None
    release_policy: Optional[str] = None

    def __post_init__(self) -> None:
        if self.mode not in SUPPORTED_MODES:
            raise EvidenceValidationError(
                f"unsupported mode {self.mode!r}; expected one of {SUPPORTED_MODES}"
            )
        if self.mode == RECORD_MODE and self.settlement.delivery is None:
            # Post-delivery record mode is meaningless without delivery evidence.
            raise EvidenceValidationError(
                "record mode is post-delivery and requires delivery evidence"
            )
        if self.mode == GATE_MODE:
            if not self.gate_controller:
                raise EvidenceValidationError(
                    "gate mode requires a gate_controller (the external system "
                    "that controls release); the verifier never controls release"
                )
            if is_forbidden_gate_controller(self.gate_controller):
                raise AuthorityViolationError(
                    f"gate_controller {self.gate_controller!r} implies a forbidden "
                    "identity (verifier / Default Settlement / Morpheus / "
                    "SettlementWitness / SAR-402 implementation) and cannot hold "
                    "release authority"
                )
            if not self.release_policy:
                raise EvidenceValidationError(
                    "gate mode requires an explicit release_policy"
                )
            # Gate seam (payment_verified_pre_delivery) does not permit delivery
            # evidence: it must not be used to force executor_continuity to PASS
            # before anything has been delivered.
            if self.settlement.delivery is not None:
                raise AuthorityViolationError(
                    "gate-mode (pre-delivery) evidence must not carry delivery "
                    "evidence; executor_continuity stays INDETERMINATE until a "
                    "later post-delivery receipt resolves it"
                )
