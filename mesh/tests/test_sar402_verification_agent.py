"""Smoke test for the SAR-402 verification agent.

A plain `unittest` module under `mesh/tests/` that imports
`mesh.agents.sar402_verification_agent` and `mesh.mesh_manager` directly, with
no runtime dependency outside this repository.

Covers: module discovery, class loading, no-argument instantiation,
deterministic PASS / FAIL / INDETERMINATE, malformed-input fail-closed,
missing-required-input fail-closed, unsupported-tool bounding, mocked
normal-query dispatch, and absence of any dependency outside this repository.
"""

from __future__ import annotations

import asyncio
import json
import sys
import types
import unittest
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "sar402_fixtures"


def _load(name: str):
    with open(FIXTURES_DIR / name) as f:
        return json.load(f)


class Sar402VerificationAgentSmokeTest(unittest.TestCase):
    def test_module_discovery_and_class_loading(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        self.assertTrue(hasattr(Sar402VerificationAgent, "_handle_tool_logic"))

    def test_agent_loader_discovers_and_registers(self):
        from mesh.mesh_manager import AgentLoader, Config

        agents = AgentLoader(Config()).load_agents()
        self.assertIn("Sar402VerificationAgent", agents)

    def test_no_argument_instantiation(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        self.assertEqual(agent.metadata["name"], "SAR-402 Execution Verification")
        tool_names = [t["function"]["name"] for t in agent.get_tool_schemas()]
        self.assertEqual(tool_names, ["verify_settlement_evidence"])

    def test_deterministic_pass(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(
            agent.call_agent(
                {"tool": "verify_settlement_evidence", "tool_arguments": _load("pass_record_mode.json")}
            )
        )
        self.assertEqual(result["data"]["data"]["receipt"]["sar_verdict"], "PASS")

    def test_deterministic_fail(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(
            agent.call_agent(
                {"tool": "verify_settlement_evidence", "tool_arguments": _load("fail_constraint_drift.json")}
            )
        )
        self.assertEqual(result["data"]["data"]["receipt"]["sar_verdict"], "FAIL")

    def test_deterministic_indeterminate(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(
            agent.call_agent(
                {
                    "tool": "verify_settlement_evidence",
                    "tool_arguments": _load("indeterminate_unknown_authority.json"),
                }
            )
        )
        self.assertEqual(result["data"]["data"]["receipt"]["sar_verdict"], "INDETERMINATE")

    def test_malformed_input_fails_closed(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(
            agent.call_agent(
                {
                    "tool": "verify_settlement_evidence",
                    "tool_arguments": _load("malformed_missing_timestamp.json"),
                }
            )
        )
        self.assertEqual(result["data"]["status"], "rejected")

    def test_missing_required_input_fails_closed(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(
            agent.call_agent({"tool": "verify_settlement_evidence", "tool_arguments": {"mode": "record"}})
        )
        self.assertEqual(result["data"]["status"], "rejected")

    def test_unsupported_tool_is_bounded(self):
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        agent = Sar402VerificationAgent()
        result = asyncio.run(agent.call_agent({"tool": "nonexistent_tool", "tool_arguments": {}}))
        self.assertIn("Unsupported tool", result["data"]["error"])

    def test_mocked_normal_query_dispatch(self):
        import mesh.mesh_agent as mesh_agent_mod
        from mesh.agents.sar402_verification_agent import Sar402VerificationAgent

        class FakeToolCall:
            def __init__(self, name, arguments):
                self.id = "fake_tool_call_1"
                self.function = types.SimpleNamespace(name=name, arguments=json.dumps(arguments))

        async def fake_llm(*args, **kwargs):
            return {"tool_calls": FakeToolCall("verify_settlement_evidence", _load("pass_record_mode.json"))}

        original = mesh_agent_mod.call_gemini_with_tools_async
        mesh_agent_mod.call_gemini_with_tools_async = fake_llm
        try:
            agent = Sar402VerificationAgent()
            result = asyncio.run(agent.call_agent({"query": "verify this", "raw_data_only": True}))
        finally:
            mesh_agent_mod.call_gemini_with_tools_async = original

        self.assertEqual(result["data"]["data"]["receipt"]["sar_verdict"], "PASS")

    def test_no_morpheus_dependency_available(self):
        """This candidate's dispatch path must never import `morpheus`. Run
        this file with cwd = a disposable checkout that has no Morpheus path
        anywhere on sys.path/PYTHONPATH for the strongest form of this claim
        (verified separately, see the evidence report); the in-process
        assertion here checks that nothing above this line pulled it in."""
        self.assertNotIn("morpheus", sys.modules)


if __name__ == "__main__":
    unittest.main()
