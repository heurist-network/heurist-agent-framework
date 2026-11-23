# Excluded from sar402_verify_tmp (considered, not copied)

Traced from the actual imports of `mesh_candidate/mesh/agents/sar402_verify_tool.py`
and `sar402_verification_agent.py` (`compute_integrity`, `validate_receipt`,
`EvidenceError`, `normalize_manual`, `build_receipt`), transitively resolved.

| File / symbol | Why excluded |
|---|---|
| `morpheus/sar402_agent/storage.py` (whole file) | File-persistence / `preserve_run` logic. Never invoked by the Mesh tool (the tool returns a receipt in-memory; it never writes to disk). Flagged as unnecessary scope creep by the 2026-07-31 architecture-decision-gate review. |
| `morpheus/sar402/samples.py` (whole file) | Test/demo-only fixture data. Not needed for normalization, evaluation, receipt construction, or validation. Flagged by the same architecture-decision-gate review. |
| `sar402_agent/runner.py: run_evidence_doc` | Depends on `storage.preserve_run`; local-persistence CLI helper, not needed by the Mesh tool. |
| `sar402_agent/runner.py: run_evidence_file` | CLI-only entry point; not needed by the Mesh tool. |
| `sar402_agent/runner.py: main` / CLI arg parser | CLI-only entry point; not needed by the Mesh tool. |
| `sar402_agent/runner.py: RunResult` dataclass | Only used by the excluded CLI/run_* entry points above. |
| `sar402_agent/normalizer.py: normalize_demo` | Demo-endpoint ingestion shape (Option B). The Mesh tool's input contract is the manual/fixture shape (Option A) only; not exported from `sar402_agent/__init__.py` in this copy (function body kept in the already-required `normalizer.py` file but unused/unreferenced). |
| Signing code, signer selection, key discovery, production registries | None exist in the canonical `morpheus/sar402*` modules being copied; not applicable. |
| Endpoint/server code, wallets, payment execution | None exist in the canonical `morpheus/sar402*` modules being copied; not applicable. `defaultverifier.com` is never referenced. |
| Reference-implementation orchestration, state files, production configuration, deployment logic | None exist in the canonical sar402 modules being copied; not applicable. |
| Unrelated builders/utilities outside `sar402`/`sar402_agent` | Not traced as a dependency of the Mesh tool; not copied. |

## Kept (and why each is essential)

| File | Why kept |
|---|---|
| `sar402/models.py` | `Amount`, `DeliveryEvidence`, `SettlementEvidence`, `parse_timestamp` — input normalization data model, used by `normalizer.py` and `builder.py`. |
| `sar402/constants.py` | Verdict/mode/schema-path constants used by `predicates.py`, `schema.py`, `validate.py`. |
| `sar402/predicates.py` | `derive_verdict`, `evaluate_continuity` — the five committed Continuity predicates (deterministic evaluation), used by `builder.py`. |
| `sar402/schema.py` | Schema loading/backend used by `validate.py`. |
| `sar402/schema_data/*.json` | The committed SAR-402 JSON Schema itself, loaded by `schema.py`. |
| `sar402/builder.py` | `build_record_mode_receipt`, `build_gate_mode_receipt`, `compute_integrity` — receipt construction and integrity recomputation, used by `runner.py` and `sar402_verify_tool.py`. |
| `sar402/validate.py` | `validate_receipt`, `is_forbidden_gate_controller`, `AuthorityBoundaryError` — receipt/authority validation, used by `builder.py`, `evidence.py`, and `sar402_verify_tool.py`. |
| `sar402_agent/evidence.py` | `NormalizedEvidence`, `EvidenceError`, mode constants, authority-boundary check — normalization model and errors, used by `normalizer.py` and `runner.py`. |
| `sar402_agent/normalizer.py` | `normalize_manual` — the input-normalization entry point the Mesh tool calls directly. |
| `sar402_agent/runner.py` (trimmed) | `build_receipt` — the mode-dispatch call into the committed builder, the only symbol the Mesh tool needs from the canonical runner. |
