import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.unifai_web3_news_agent import UnifaiWeb3NewsAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "natural_language_query": {
        "input": {
            "query": "What are the latest developments in Web3?",
            "raw_data_only": False,
        },
        "description": "Natural language query for latest Web3 developments",
    },
    "default_parameters": {
        "input": {
            "tool": "get_web3_news",
            "tool_arguments": {},
            "raw_data_only": False,
        },
        "description": "Direct tool call with default parameters",
    },
    "limit_parameter": {
        "input": {
            "tool": "get_web3_news",
            "tool_arguments": {"limit": 1},
            "raw_data_only": True,
        },
        "description": "Direct tool call with limit=1 and raw_data_only=True",
    },
    "keyword_parameter": {
        "input": {
            "tool": "get_web3_news",
            "tool_arguments": {"keyword": "bitcoin", "limit": 2},
            "raw_data_only": False,
        },
        "description": "Direct tool call with keyword='bitcoin' and limit=2",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(UnifaiWeb3NewsAgent, TEST_CASES))
