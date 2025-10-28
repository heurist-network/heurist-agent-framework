# test_trending_token_agent.py
"""Test suite for Trending Token Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.trending_token_agent import TrendingTokenAgent
from mesh.tests._test_agents import test_agent

# Define test cases
TEST_CASES = {
    "basic_trending_query": {
        "input": {"query": "Show me trending tokens"},
        "description": "",
    },
    "trending_with_memes": {
        "input": {"query": "Get trending tokens including memecoins"},
        "description": "Natural language query for trending tokens including memes",
    },
    "direct_tool_basic": {
        "input": {"tool": "get_trending_tokens", "tool_arguments": {}},
        "description": "",
    },
    "direct_tool_with_memes": {
        "input": {"tool": "get_trending_tokens", "tool_arguments": {"include_memes": True}},
        "description": "Direct tool call including memecoins and pump.fun data",
    },
    "trending_without_memes_raw": {
        "input": {"tool": "get_trending_tokens", "tool_arguments": {"include_memes": False}, "raw_data_only": True},
        "description": "",
    },
    "trending_with_memes_formatted": {
        "input": {"tool": "get_trending_tokens", "tool_arguments": {"include_memes": True}, "raw_data_only": False},
        "description": "",
    },
    "market_overview_query": {
        "input": {"query": "What are the hottest tokens right now across all platforms?"},
        "description": "Natural language query for comprehensive token trends",
    },
    "coingecko_twitter_only": {
        "input": {"query": "Show me trending tokens from CoinGecko and Twitter only"},
        "description": "Query for standard trending sources (excluding meme platforms)",
    },
    "pump_fun_graduations": {
        "input": {"query": "What tokens have recently graduated from pump.fun?"},
        "description": "Natural language query specifically for pump.fun graduations",
    },
    "gmgn_meme_trends": {
        "input": {"query": "Show me what's trending on GMGN"},
        "description": "",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(TrendingTokenAgent, TEST_CASES))
