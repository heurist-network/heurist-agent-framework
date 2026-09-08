"""Receipt-construction dispatch: normalized evidence -> committed builder call.

TRIMMED COPY NOTICE (read before modifying):
    canonical source repository : SAR-402 reference implementation
    exact source commit SHA     : 84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0
    original source file path   : sar402_reference/sar402_agent/runner.py
    date copied                 : 2026-07-31
    scope                       : verification-only Heurist adapter support
    status                      : NON-CANONICAL TEMPORARY COPY
    canonical logic remains in the SAR-402 reference implementation at the path/commit above.
    shared-core packaging (a real installable package) was deferred pending
    actual Heurist interest or review -- this is a disposable local copy, not
    a package release.
    Future maintenance MUST diff this file against
    morpheus/sar402_agent/runner.py @ 84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0
    before modification or any submission.

    This file is a DELIBERATELY TRIMMED subset of the canonical runner.py: it
    keeps only `build_receipt` (the mode-dispatch call into the committed
    builder), which is the single symbol the Heurist Mesh tool needs. The
    canonical file's `run_evidence_doc`, `run_evidence_file`, and CLI `main`
    are CLI/local-persistence entry points that depend on
    `sar402_agent.storage.preserve_run` (file-persistence logic never invoked
    by the Mesh tool) and are intentionally NOT copied here. See
    `PROVENANCE_EXCLUDED_SYMBOLS` below.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sar402_verify_tmp.sar402 import build_gate_mode_receipt, build_record_mode_receipt

from .evidence import EvidenceError, GATE_MODE, RECORD_MODE

if TYPE_CHECKING:
    from .evidence import NormalizedEvidence

PROVENANCE_SOURCE_COMMIT = "84d9060b57bf81bae8ebaf0b3ec438ab6f7732a0"
PROVENANCE_SOURCE_PATH = "morpheus/sar402_agent/runner.py"
PROVENANCE_EXCLUDED_SYMBOLS = (
    "run_evidence_doc",  # depends on storage.preserve_run; not needed by the Mesh tool
    "run_evidence_file",  # CLI-only entry point; not needed by the Mesh tool
    "main",  # CLI-only entry point; not needed by the Mesh tool
    "RunResult",  # dataclass only used by the excluded CLI/run_* entry points
)


def build_receipt(normalized: "NormalizedEvidence") -> dict:
    """Call the committed builder for the normalized evidence's mode.

    The builder self-validates; we do not bypass or duplicate it."""
    if normalized.mode == RECORD_MODE:
        return build_record_mode_receipt(
            normalized.settlement,
            acting_party=normalized.acting_party,
        )
    if normalized.mode == GATE_MODE:
        return build_gate_mode_receipt(
            normalized.settlement,
            gate_controller=normalized.gate_controller,
            release_policy=normalized.release_policy,
        )
    # NormalizedEvidence already guards mode, but be explicit.
    raise EvidenceError(f"unsupported mode {normalized.mode!r}")
