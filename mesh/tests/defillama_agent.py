"""Test suite for DefiLlama Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.defillama_agent import DefiLlamaAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "protocol_metrics_query": {
        "input": {"query": "What is the TVL of Aave?"},
        "description": "Natural language query for Aave protocol TVL",
    },
    "get_protocol_metrics_tool": {
        "input": {
            "tool": "get_protocol_metrics",
            "tool_arguments": {"protocol": "uniswap-v3"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Uniswap V3 protocol metrics with raw data",
    },
    "chain_metrics_query": {
        "input": {"query": "Get chain metrics for Base"},
        "description": "Natural language query for Base chain metrics",
    },
    "get_chain_metrics_tool": {
        "input": {
            "tool": "get_chain_metrics",
            "tool_arguments": {"chain": "Solana"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Solana chain metrics with raw data",
    },
    "top_protocols_by_fees_query": {
        "input": {"query": "What are the top protocols on Solana by fees?"},
        "description": "Natural language query for top fee-generating protocols on Solana",
    },
    "search_yield_pools_stablecoin_tool": {
        "input": {
            "tool": "search_yield_pools",
            "tool_arguments": {
                "chains": ["Ethereum"],
                "stablecoin": True,
                "sort_by": "apy",
                "limit": 5,
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for top stablecoin yield pools on Ethereum sorted by APY",
    },
    "search_yield_pools_by_project_tool": {
        "input": {
            "tool": "search_yield_pools",
            "tool_arguments": {
                "projects": ["aave-v3", "curve-dex"],
                "sort_by": "tvl",
                "limit": 10,
            },
            "raw_data_only": False,
        },
        "description": "Direct tool call for Aave V3 and Curve yield pools sorted by TVL with formatted response",
    },
    "search_yield_pools_by_symbol_tool": {
        "input": {
            "tool": "search_yield_pools",
            "tool_arguments": {
                "symbols": ["USDC", "USDT"],
                "chains": ["Arbitrum"],
                "limit": 5,
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for USDC/USDT yield pools on Arbitrum",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(DefiLlamaAgent, TEST_CASES))
