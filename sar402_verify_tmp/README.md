# sar402_verify_tmp

A small, self-contained, vendored copy of the SAR-402 reference
implementation's evidence-normalization, receipt-construction, and
schema/authority-validation logic. It exists so `mesh/agents/sar402_verify_tool.py`
and `sar402_verification_agent.py` can run with zero dependency on any
external repository being present.

## Provenance

- Source: SAR-402 reference implementation, `sar402/` and `sar402_agent/`
  modules (evidence normalization, receipt construction, schema/authority
  validation, digest-based integrity).
- Only the schema file path and internal import prefix were adjusted for
  standalone operation -- no predicate, constant, or verdict-vocabulary
  change.

## What was excluded and why

See `EXCLUDED.md` for the full list. In short: file-persistence code
(`storage.py`, never invoked by the Mesh tool) and test/demo-only sample
fixtures (`samples.py`) were dropped, along with the CLI/local-persistence
entry points in `runner.py` (`run_evidence_doc`, `run_evidence_file`, `main`)
that depended on `storage.py`. Only `build_receipt` was kept from `runner.py`.

## Not a separately published package

This is vendored source under this repository, not published or installed
from a package registry.
