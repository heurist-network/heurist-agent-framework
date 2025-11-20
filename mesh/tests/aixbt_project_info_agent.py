# test_aixbt_agent.py
"""Test suite for AIXBT Project Info Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.aixbt_project_info_agent import AIXBTProjectInfoAgent
from mesh.tests._test_agents import test_agent

# Define test cases
TEST_CASES = {
    "heu_token_query": {
        "input": {"query": "Tell me about HEU token"},
        "description": "Natural language query about HEU token",
    },
    "trending_solana": {
        "input": {"query": "Tell me about trending projects on solana with minscore of 0.1", "raw_data_only": False},
        "description": "Query trending Solana projects with minimum score filter",
    },
    "search_projects_direct": {
        "input": {"tool": "search_projects", "tool_arguments": {"name": "heurist", "limit": 1}},
        "description": "Direct tool call to search for Heurist project",
    },
    "search_with_limit": {
        "input": {"tool": "search_projects", "tool_arguments": {"name": "bitcoin", "limit": 25}, "raw_data_only": True},
        "description": "Search Bitcoin projects with increased limit and raw data",
    },
    "market_summary_1day": {
        "input": {"tool": "get_market_summary", "tool_arguments": {"lookback_days": 1}},
        "description": "Get market summary for last 1 day - should return empty if data is stale (>3 days old)",
    },
    "market_summary_3days": {
        "input": {"tool": "get_market_summary", "tool_arguments": {"lookback_days": 3}},
        "description": "Get market summary for last 3 days - filters out data older than 3 days",
    },
    "market_summary_default": {
        "input": {"tool": "get_market_summary", "tool_arguments": {}},
        "description": "Get market summary with default lookback (1 day) - verify stale data filtering",
    },
    "market_summary_week": {
        "input": {"tool": "get_market_summary", "tool_arguments": {"lookback_days": 7}},
        "description": "Attempt to get 7-day summary (capped at 3 days max, filters stale data)",
    },
    "market_query_natural": {
        "input": {"query": "What's happening in the crypto market today?"},
        "description": "Natural language query for today's market - should handle stale data gracefully",
    },
    "empty_search_args": {
        "input": {"tool": "search_projects", "tool_arguments": {}},
        "description": "Test empty tool arguments handling",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(AIXBTProjectInfoAgent, TEST_CASES))
