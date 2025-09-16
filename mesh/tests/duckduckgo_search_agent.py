# test_duckduckgo_search_agent.py
"""Test suite for DuckDuckGo Search Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.duckduckgo_search_agent import DuckDuckGoSearchAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "ai_developments_search": {
        "input": {
            "query": "What are the latest developments in artificial intelligence?",
            "tool": "search_web",
            "tool_arguments": {
                "search_term": "What are the latest developments in artificial intelligence?",
                "max_results": 3,
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call to search web for AI developments with 3 max results",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(DuckDuckGoSearchAgent, TEST_CASES))
