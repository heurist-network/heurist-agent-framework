# test_cookie_project_info_agent.py
"""Test suite for Cookie Project Info Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.cookie_project_info_agent import CookieProjectInfoAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "twitter_username_query": {
        "input": {
            "query": "Tell me about the project with Twitter handle @cookiedotfun",
            "raw_data_only": False,
        },
        "description": "Natural language query for project with @cookiedotfun Twitter handle",
    },
    "twitter_username_query_2": {
        "input": {
            "query": "Tell me about the project with Twitter handle @heurist_ai for past 30 days",
            "raw_data_only": False,
        },
        "description": "Natural language query for @heurist_ai project with 30-day timeframe",
    },
    "contract_address_query": {
        "input": {
            "query": "Get details for the contract 0xc0041ef357b183448b235a8ea73ce4e4ec8c265f",
            "raw_data_only": False,
        },
        "description": "Natural language query for project by contract address",
    },
    "tool_twitter_username": {
        "input": {
            "tool": "get_project_by_twitter_username",
            "tool_arguments": {"twitter_username": "heurist_ai"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for project by Twitter username with raw data",
    },
    "tool_contract_address": {
        "input": {
            "tool": "get_project_by_contract_address",
            "tool_arguments": {"contract_address": "0xc0041ef357b183448b235a8ea73ce4e4ec8c265f"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for project by contract address with raw data",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(CookieProjectInfoAgent, TEST_CASES))
