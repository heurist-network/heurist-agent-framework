"""Live public-data example, using the shared Mesh test harness without an LLM call."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mesh.agents.xrpl_token_safety_agent import XrplTokenSafetyAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {"rlusd_snapshot": {"input": {
    "tool": "check_token_safety",
    "tool_arguments": {"issuer": "rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De", "currency": "RLUSD"},
    "raw_data_only": True,
}, "description": "Public snapshot only; no wallet, LLM, signature or paid API."}}

if __name__ == "__main__":
    asyncio.run(test_agent(XrplTokenSafetyAgent, TEST_CASES))
