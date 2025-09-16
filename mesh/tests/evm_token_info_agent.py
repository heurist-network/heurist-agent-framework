# test_evm_token_info_agent.py
"""Test suite for EVM Token Info Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.evm_token_info_agent import EvmTokenInfoAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    # Test 1: BSC - BNB trades (all)
    "bsc_bnb_all": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "bsc",
                "tokenAddress": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",  # WBNB
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        },
        "description": "BSC - BNB all trades with $5k+ minimum",
    },
    # Test 2: Ethereum - USDC buyers only
    "eth_usdc_buyers": {
        "input": {
            "query": "Show me only the large buyers of USDC 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 on ethereum"
        },
        "description": "Ethereum - USDC buyers only via natural language",
    },
    # Test 3: Base - WETH sellers only
    "base_weth_sellers": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0x4200000000000000000000000000000000000006",  # WETH on Base
                "minUsdAmount": 10000,
                "filter": "sell",
                "limit": 5,
            },
        },
        "description": "Base - WETH sellers only with $10k+ minimum",
    },
    # Test 4: Arbitrum - USDC all trades
    "arb_usdc_all": {
        "input": {
            "query": "What are the large trades for USDC 0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8 on arbitrum?"
        },
        "description": "Arbitrum - USDC all trades via natural language",
    },
    # Test 5: BSC - BTCB large trades
    "bsc_btcb": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "bsc",
                "tokenAddress": "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",  # BTCB
                "minUsdAmount": 50000,
                "filter": "all",
                "limit": 5,
            },
        },
        "description": "BSC - BTCB large trades ($50k+)",
    },
    # Test 6: Ethereum - WETH buyers
    "eth_weth_buyers": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "eth",
                "tokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
                "minUsdAmount": 100000,
                "filter": "buy",
                "limit": 5,
            },
        },
        "description": "Ethereum - WETH buyers with $100k+ minimum",
    },
    # Test 7: Natural language - BSC USDT
    "bsc_usdt_nl": {
        "input": {
            "query": "Show me the recent large trades for USDT 0x55d398326f99059fF775485246999027B3197955 on BSC"
        },
        "description": "Natural language - BSC USDT traders",
    },
    # Test 8: Invalid token address
    "invalid_address": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "ethereum",
                "tokenAddress": "not_a_valid_address",
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        },
        "description": "Invalid token address test",
    },
    # Test 9: Unsupported chain test
    "unsupported_chain": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "polygon",  # Not supported
                "tokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        },
        "description": "Unsupported chain test",
    },
    # Test 10: Raw data mode
    "raw_data_mode": {
        "input": {
            "query": "Large trades for DAI 0x6B175474E89094C44Da98b954EedeAC495271d0F on ethereum above $25k",
            "raw_data_only": True,
        },
        "description": "Raw data mode - Ethereum DAI",
    },
    # Test 11a: HEU all trades
    "heu_all_trades": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 5,
            },
        },
        "description": "HEU token - all trades for trade type verification",
    },
    # Test 11b: HEU sells from trader perspective
    "heu_sells_from_trader": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "sell",  # Trader sells (should query DEX buys)
                "limit": 3,
            },
        },
        "description": "HEU token - trader sells (queries DEX buys)",
    },
    # Test 11c: HEU buys from trader perspective
    "heu_buys_from_trader": {
        "input": {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "buy",  # Trader buys (should query DEX sells)
                "limit": 3,
            },
        },
        "description": "HEU token - trader buys (queries DEX sells)",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(EvmTokenInfoAgent, TEST_CASES))
