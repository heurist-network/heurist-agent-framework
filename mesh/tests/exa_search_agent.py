# test_exa_search_agent.py
"""Test suite for Exa Search Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.exa_search_agent import ExaSearchAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "natural_language_query": {
        "input": {
            "query": "What are the latest developments in quantum computing?",
            "raw_data_only": False,
        },
        "description": "Natural language query for quantum computing developments",
    },
    "direct_search": {
        "input": {
            "tool": "exa_web_search",
            "tool_arguments": {"search_term": "quantum computing breakthroughs 2024", "limit": 5},
            "raw_data_only": False,
        },
        "description": "Direct search tool call for quantum computing breakthroughs",
    },
    "direct_answer": {
        "input": {
            "tool": "exa_answer_question",
            "tool_arguments": {"question": "What is quantum supremacy?"},
            "raw_data_only": False,
        },
        "description": "Direct answer tool call for quantum supremacy definition",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ExaSearchAgent, TEST_CASES))
