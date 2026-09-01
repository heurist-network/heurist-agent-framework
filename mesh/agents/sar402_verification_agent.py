"""SAR-402 execution/service-delivery verification agent.

This agent and its sibling module `sar402_verify_tool.py` import only from
`sar402_verify_tmp` (a small, self-contained, vendored package included in
this repository -- see `sar402_verify_tmp/README.md`) and the framework's
own `mesh.mesh_agent.MeshAgent`. Neither module has any dependency on an
external project or repository at runtime.

`sar402_verify_tmp` is a verbatim-logic copy of the SAR-402 reference
implementation's evidence-normalization, receipt-construction, and
schema/authority-validation code, with only its schema file path and
internal import prefix adjusted for standalone operation -- no predicate,
constant, or verdict-vocabulary change.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from mesh.mesh_agent import MeshAgent  # real framework import; only resolves
# when this file is placed inside a pinned-framework checkout.

from .sar402_verify_tool import TOOL_SCHEMA, VERIFY_TOOL_NAME, verify_settlement_evidence


class Sar402VerificationAgent(MeshAgent):
    """Deterministic SAR-402 execution/service-delivery verification agent.

    Evaluates supplied structured evidence (optionally alongside x402
    settlement context, treated as unverified supporting context) and
    returns a deterministic PASS / FAIL / INDETERMINATE receipt with a
    recomputable, digest-based integrity value. Never holds funds, custody,
    or execution/release authority, and never claims payment settlement
    finality, a cryptographic signature, or legal finality.
    """

    def __init__(self) -> None:
        super().__init__()
        self.metadata.update(
            {
                "name": "SAR-402 Execution Verification",
                "version": "0.1.0",
                "author": "SAR-402 contributors",
                "author_address": "0x0000000000000000000000000000000000000000",
                "description": (
                    "Evaluates supplied execution/service-delivery evidence "
                    "(optionally with x402 settlement context as unverified "
                    "supporting input) and returns a deterministic "
                    "PASS/FAIL/INDETERMINATE receipt with reason codes and a "
                    "recomputable digest-based integrity value. Does not "
                    "verify payment settlement finality and does not produce "
                    "a cryptographic signature."
                ),
                "external_apis": [],
                "tags": ["verification", "x402", "sar-402"],
                "hidden": True,
                "verified": False,
                "recommended": False,
                "examples": [
                    "Verify a record-mode settlement + delivery evidence bundle",
                    "Verify a gate-mode payment-verified-pre-delivery bundle",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You evaluate structured execution/service-delivery evidence, "
            "optionally alongside x402 settlement context supplied as "
            "unverified context, and return a deterministic PASS, FAIL, or "
            "INDETERMINATE receipt with reason codes. You never hold funds, "
            "custody, or execution/release authority. You never claim to "
            "verify payment settlement finality, and you never claim the "
            "receipt's integrity value is a cryptographic signature -- it is "
            "a recomputable digest only."
        )

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return [TOOL_SCHEMA]

    async def _handle_tool_logic(
        self,
        tool_name: str,
        function_args: Dict[str, Any],
        session_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if tool_name != VERIFY_TOOL_NAME:
            return {"error": f"Unsupported tool: {tool_name}"}
        return await verify_settlement_evidence(function_args, session_context)
