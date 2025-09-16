# test_elfa_twitter_intelligence_agent.py
"""Test suite for ELFA Twitter Intelligence Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.elfa_twitter_intelligence_agent import ElfaTwitterIntelligenceAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "search_mentions_tool": {
        "input": {
            "tool": "search_mentions",
            "tool_arguments": {"keywords": ["bitcoin", "solana", "ethereum"], "days_ago": 30, "limit": 25},
            "query": "Search for crypto mentions using tool arguments",
        },
        "description": "Direct tool call to search mentions for crypto keywords",
    },
    "search_mentions_query": {
        "input": {"query": "Search for mentions of bitcoin, solana, and ethereum in the last 30 days"},
        "description": "Natural language query to search for crypto mentions",
    },
    "search_account_tool": {
        "input": {
            "tool": "search_account",
            "tool_arguments": {"username": "heurist_ai", "days_ago": 30, "limit": 20},
            "query": "Analyze account using tool arguments",
        },
        "description": "Direct tool call to analyze @heurist_ai account",
    },
    "search_account_query": {
        "input": {"query": "Analyze the Twitter account @heurist_ai and show me their recent activity"},
        "description": "Natural language query to analyze @heurist_ai account activity",
    },
    "get_trending_tokens_tool": {
        "input": {
            "tool": "get_trending_tokens",
            "tool_arguments": {"time_window": "24h"},
            "query": "Get trending tokens using tool arguments",
        },
        "description": "Direct tool call to get trending tokens for 24h window",
    },
    "get_trending_tokens_query": {
        "input": {"query": "What are the trending tokens on Twitter in the last 24 hours?"},
        "description": "Natural language query for trending tokens in last 24 hours",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ElfaTwitterIntelligenceAgent, TEST_CASES))
