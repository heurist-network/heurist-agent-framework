# test_pqs_agent.py
"""Test suite for PQS Prompt Quality Score Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.pqs_agent import PqsAgent
from mesh.tests._test_agents import test_agent

# Define test cases
TEST_CASES = {
    "query_mode_basic": {
        "input": {
            "query": "How good is this prompt: Write a Python function that sorts a list",
        },
        "description": "Natural language query — agent should extract the prompt and call score_prompt",
    },
    "direct_tool_call_general": {
        "input": {
            "tool": "score_prompt",
            "tool_arguments": {
                "prompt": "Write a haiku about postgres",
            },
        },
        "description": "Direct tool call with default vertical",
    },
    "direct_tool_call_software": {
        "input": {
            "tool": "score_prompt",
            "tool_arguments": {
                "prompt": (
                    "As a senior backend engineer, review this Python REST API for security "
                    "vulnerabilities. Focus on SQL injection, authentication bypass, and rate "
                    "limiting. Provide findings as a markdown table with severity, location, "
                    "and recommended fix."
                ),
                "vertical": "software",
            },
        },
        "description": "Direct tool call with software vertical — should score higher due to specificity",
    },
    "direct_tool_raw_data": {
        "input": {
            "tool": "score_prompt",
            "tool_arguments": {
                "prompt": "Explain quantum computing to a 5 year old using analogies",
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call with raw_data_only — returns unformatted API response",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(PqsAgent, TEST_CASES, delay_seconds=2))
