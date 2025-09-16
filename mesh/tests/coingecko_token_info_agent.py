# test_coingecko_token_info_agent.py
"""Test suite for CoinGecko Token Info Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.coingecko_token_info_agent import CoinGeckoTokenInfoAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    # Test with a natural language query
    "natural_language_query": {
        "input": {"query": "Get information about $HEURIST"},
        "description": "Natural language query for HEURIST token information",
    },
    # Test direct tool calls for each tool
    # 1. get_token_info
    "get_token_info_tool": {
        "input": {
            "tool": "get_token_info",
            "tool_arguments": {"coingecko_id": "bitcoin"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Bitcoin token info with raw data",
    },
    # 2. get_trending_coins
    "get_trending_coins_tool": {
        "input": {
            "tool": "get_trending_coins",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "description": "Direct tool call for trending coins with raw data",
    },
    # 3. get_token_price_multi
    "get_token_price_multi_tool": {
        "input": {
            "tool": "get_token_price_multi",
            "tool_arguments": {
                "ids": "bitcoin,ethereum",
                "vs_currencies": "usd",
                "include_market_cap": True,
                "include_24hr_vol": True,
                "include_24hr_change": True,
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for multi-token price data with market metrics",
    },
    # 4. get_categories_list
    "get_categories_list_tool": {
        "input": {
            "tool": "get_categories_list",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "description": "Direct tool call for categories list with raw data",
    },
    # 5. get_category_data
    "get_category_data_tool": {
        "input": {
            "tool": "get_category_data",
            "tool_arguments": {"order": "market_cap_desc"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for category data ordered by market cap",
    },
    # 6. get_tokens_by_category
    "get_tokens_by_category_tool": {
        "input": {
            "tool": "get_tokens_by_category",
            "tool_arguments": {
                "category_id": "layer-1",
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call for layer-1 tokens with formatted response",
    },
    # 7. get_trending_pools
    "get_trending_pools_tool": {
        "input": {
            "tool": "get_trending_pools",
            "tool_arguments": {
                "include": "base_token",
                "pools": 4,
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call for trending pools with base token info",
    },
    # 8. get_top_token_holders
    "get_top_token_holders_tool": {
        "input": {
            "tool": "get_top_token_holders",
            "tool_arguments": {
                "network": "base",
                "address": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call for top token holders on Base network",
    },
    # Test with raw data only for natural language query
    "raw_data_query": {
        "input": {
            "query": "Compare Bitcoin and Ethereum prices",
            "raw_data_only": True,
        },
        "description": "Natural language query comparing BTC and ETH with raw data flag",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(CoinGeckoTokenInfoAgent, TEST_CASES))
