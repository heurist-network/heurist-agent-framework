import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.masa_twitter_search_agent import MasaTwitterSearchAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "masa_twitter_search": {
        "input": {"query": "@getmasafi", "max_results": 100},
        "description": "Natural language query for @getmasafi with 100 max results",
    },
    "btc_twitter_search": {
        "input": {"query": "$BTC", "max_results": 30},
        "description": "Natural language query for $BTC with 30 max results",
    },
    "direct_twitter_search": {
        "input": {
            "tool": "search_twitter",
            "tool_arguments": {"search_term": "Elon musk", "max_results": 30},
            "raw_data_only": True,
        },
        "description": "Direct tool call to search Twitter for Elon Musk with raw data",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(MasaTwitterSearchAgent, TEST_CASES))
