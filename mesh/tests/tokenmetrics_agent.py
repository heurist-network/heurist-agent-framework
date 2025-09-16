import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.tokenmetrics_agent import TokenMetricsAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "market_sentiments_query": {
        "input": {
            "query": "What is the current market sentiment for top cryptocurrencies?",
            "raw_data_only": False,
        },
        "description": "Natural language query for current market sentiment",
    },
    "top_5_crypto_sentiment": {
        "input": {
            "query": "Can you show me the top 5 cryptocurrencies by market feeling?",
            "raw_data_only": False,
        },
        "description": "Natural language query for top 5 cryptocurrencies by sentiment with auto-detected limit",
    },
    "btc_eth_resistance_support": {
        "input": {
            "query": "What are the key resistance and support levels for Bitcoin and Ethereum?",
            "raw_data_only": False,
        },
        "description": "Natural language query for BTC and ETH resistance/support levels",
    },
    "solana_resistance_support": {
        "input": {
            "query": "What are the resistance and support levels for Solana (SOL)?",
            "raw_data_only": False,
        },
        "description": "Natural language query for Solana resistance/support levels by symbol",
    },
    "heurist_sentiment_query": {
        "input": {
            "query": "What's the current sentiment for Heurist token?",
            "raw_data_only": False,
        },
        "description": "Natural language query for Heurist token sentiment by name",
    },
    "direct_token_info": {
        "input": {
            "tool": "get_token_info",
            "tool_arguments": {"token_symbol": "HEU", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Direct tool call for HEU token info with limit 5",
    },
    "direct_sentiments": {
        "input": {
            "tool": "get_sentiments",
            "tool_arguments": {"limit": 5, "page": 0},
            "raw_data_only": True,
        },
        "description": "Direct tool call for market sentiments with limit 5",
    },
    "direct_sentiments_default": {
        "input": {
            "tool": "get_sentiments",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "description": "Direct tool call for market sentiments with default parameters",
    },
    "direct_resistance_support": {
        "input": {
            "tool": "get_resistance_support_levels",
            "tool_arguments": {"token_ids": "3393", "symbols": "DOGE", "limit": 10, "page": 0},
            "raw_data_only": True,
        },
        "description": "Direct tool call for DOGE resistance/support levels",
    },
    "direct_resistance_support_default": {
        "input": {
            "tool": "get_resistance_support_levels",
            "tool_arguments": {"token_ids": "3988,73672,42740", "symbols": "SOL,SOL,SOL"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for SOL resistance/support levels with default limit",
    },
    "token_info_etc": {
        "input": {
            "tool": "get_token_info",
            "tool_arguments": {"token_symbol": "ETC"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for ETC token info (used for subsequent resistance/support call)",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(TokenMetricsAgent, TEST_CASES))
