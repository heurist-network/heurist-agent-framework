# test_dexscreener_token_info_agent.py
"""Test suite for DexScreener Token Info Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.dexscreener_token_info_agent import DexScreenerTokenInfoAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "natural_language_query_with_analysis": {
        "input": {
            "query": "Show me information about ETH on Uniswap",
            "raw_data_only": False,
        },
        "description": "Natural language query for ETH on Uniswap with analysis",
    },
    "natural_language_query_raw_data": {
        "input": {
            "query": "Tell me about ETH on Uniswap",
            "raw_data_only": True,
        },
        "description": "Natural language query for ETH on Uniswap with raw data only",
    },
    "search_pairs_test": {
        "input": {
            "tool": "search_pairs",
            "tool_arguments": {"search_term": "ETH"},
        },
        "description": "Direct tool call to search pairs for ETH",
    },
    "specific_pair_info_test": {
        "input": {
            "tool": "get_specific_pair_info",
            "tool_arguments": {"chain": "solana", "pair_address": "7qsdv1yr4yra9fjazccrwhbjpykvpcbi3158u1qcjuxp"},
        },
        "description": "Direct tool call to get specific pair info on Solana",
    },
    "token_pairs_test": {
        "input": {
            "tool": "get_token_pairs",
            "tool_arguments": {"chain": "solana", "token_address": "8TE8oxirpnriy9CKCd6dyjtff2vvP3n6hrSMqX58pump"},
        },
        "description": "Direct tool call to get all pairs for a Solana token",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(DexScreenerTokenInfoAgent, TEST_CASES))
