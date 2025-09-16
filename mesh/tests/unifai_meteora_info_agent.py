import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.unifai_meteora_info_agent import UnifaiMeteoraInfoAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "trending_dlmm_natural": {
        "input": {
            "query": "Show me trending DLMM pools on Meteora",
            "raw_data_only": False,
        },
        "description": "Natural language query for trending DLMM pools on Meteora",
    },
    "trending_dlmm_direct": {
        "input": {
            "tool": "get_trending_dlmm_pools",
            "tool_arguments": {"limit": 5},
            "raw_data_only": True,
        },
        "description": "Direct tool call for trending DLMM pools with limit 5",
    },
    "trending_dlmm_filtered": {
        "input": {
            "tool": "get_trending_dlmm_pools",
            "tool_arguments": {"limit": 3, "include_pool_token_pairs": ["SOL/USDC"]},
            "raw_data_only": False,
        },
        "description": "Trending DLMM pools filtered by SOL/USDC pair with limit 3",
    },
    "dynamic_amm_natural": {
        "input": {
            "query": "Find dynamic AMM pools with SOL token",
            "raw_data_only": False,
        },
        "description": "Natural language query for dynamic AMM pools with SOL token",
    },
    "dynamic_amm_direct": {
        "input": {
            "tool": "search_dynamic_amm_pools",
            "tool_arguments": {
                "limit": 5,
                "include_token_mints": ["So11111111111111111111111111111111111111112"],  # SOL mint
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for dynamic AMM pools with SOL mint address",
    },
    "dlmm_pools_natural": {
        "input": {
            "query": "Search for DLMM pools on Meteora",
            "raw_data_only": False,
        },
        "description": "Natural language query to search for DLMM pools",
    },
    "dlmm_pools_direct": {
        "input": {
            "tool": "search_dlmm_pools",
            "tool_arguments": {
                "limit": 5,
                "include_pool_token_pairs": [
                    "So11111111111111111111111111111111111111112-EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
                ],
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for DLMM pools with SOL-USDC token pair",
    },
    "dlmm_pools_combined": {
        "input": {
            "tool": "search_dlmm_pools",
            "tool_arguments": {
                "limit": 3,
                "include_token_mints": ["So11111111111111111111111111111111111111112"],
                "include_pool_token_pairs": [],
            },
            "raw_data_only": False,
        },
        "description": "DLMM pools search with SOL mint filter and empty token pairs",
    },
    # Additional test cases from the original file
    "top_5_trending_pools": {
        "input": {"query": "What are the top 5 trending pools on Meteora?"},
        "description": "Natural language query for top 5 trending pools",
    },
    "high_tvl_pools": {
        "input": {"query": "Show me pools with high TVL"},
        "description": "Natural language query for pools with high TVL",
    },
    "sol_liquidity_pools": {
        "input": {"query": "Find liquidity pools for SOL"},
        "description": "Natural language query for SOL liquidity pools",
    },
    "best_dlmm_pools": {
        "input": {"query": "Get me the best DLMM pools"},
        "description": "Natural language query for best DLMM pools",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(UnifaiMeteoraInfoAgent, TEST_CASES))
