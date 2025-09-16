import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.moni_twitter_insight_agent import MoniTwitterInsightAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "followers_history_query": {
        "input": {"query": "Show me the follower growth trends for heurist_ai over the last week"},
        "description": "Natural language query for smart followers history",
    },
    "follower_categories_query": {
        "input": {"query": "What categories of followers does heurist_ai have?"},
        "description": "Natural language query for smart followers categories",
    },
    "smart_mentions_query": {
        "input": {"query": "Show me the recent smart mentions for ethereum"},
        "description": "Natural language query for smart mentions",
    },
    "direct_followers_history": {
        "input": {
            "tool": "get_smart_followers_history",
            "tool_arguments": {"username": "heurist_ai", "timeframe": "D7"},
        },
        "description": "Direct tool call for smart followers history with 7-day timeframe",
    },
    "direct_follower_categories": {
        "input": {
            "tool": "get_smart_followers_categories",
            "tool_arguments": {"username": "heurist_ai"},
        },
        "description": "Direct tool call for smart followers categories",
    },
    "direct_mentions_feed": {
        "input": {
            "tool": "get_smart_mentions_feed",
            "tool_arguments": {"username": "heurist_ai", "limit": 100},
        },
        "description": "Direct tool call for smart mentions feed with limit 100",
    },
    "raw_data_mentions": {
        "input": {
            "query": "Get smart mentions feed for bitcoin",
            "raw_data_only": True,
        },
        "description": "Natural language query for smart mentions with raw data flag",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(MoniTwitterInsightAgent, TEST_CASES))
