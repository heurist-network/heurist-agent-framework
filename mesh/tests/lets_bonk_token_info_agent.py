import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.lets_bonk_token_info_agent import LetsBonkTokenInfoAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # About to graduate tokens
    "graduate_tokens_query": {
        "input": {"query": "Show me top 10 tokens about to graduate on LetsBonk.fun"},
        "description": "Natural language query for tokens about to graduate",
    },
    "graduate_tokens_tool": {
        "input": {
            "tool": "query_about_to_graduate_tokens",
            "tool_arguments": {"limit": 15},
        },
        "description": "Direct tool call for tokens about to graduate with limit 15",
    },
    # Latest trades - all launchpads
    "trades_all_query": {
        "input": {"query": "Show me the latest 10 trades for token So11111111111111111111111111111111111111112"},
        "description": "Natural language query for latest trades (all launchpads)",
    },
    "trades_all_tool": {
        "input": {
            "tool": "query_latest_trades",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "limit": 25,
            },
        },
        "description": "Direct tool call for latest trades (porkfolio token, all launchpads)",
    },
    # Latest trades - specific launchpad
    "trades_raydium_query": {
        "input": {
            "query": "Show me the latest 10 trades for token So11111111111111111111111111111111111111112 on raydium_launchpad"
        },
        "description": "Natural language query for latest trades on specific launchpad",
    },
    "trades_raydium_tool": {
        "input": {
            "tool": "query_latest_trades",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "limit": 25,
                "launchpad": "raydium_launchpad",
            },
        },
        "description": "Direct tool call for latest trades on specific launchpad",
    },
    # Latest price
    "price_all_query": {
        "input": {"query": "What's the current price of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk?"},
        "description": "Natural language query for current price (all launchpads)",
    },
    "price_raydium_tool": {
        "input": {
            "tool": "query_latest_price",
            "tool_arguments": {
                "token_address": "GN7BPjVW6UfexZ1Tu6UTa9X7Qd9pJBDNEstR5Lv3bonk",
                "launchpad": "raydium_launchpad",
            },
        },
        "description": "Direct tool call for latest price on specific launchpad (Groktor token)",
    },
    # Top buyers
    "buyers_all_query": {
        "input": {"query": "Show me the top 10 buyers of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"},
        "description": "Natural language query for top buyers (all launchpads)",
    },
    "buyers_raydium_query": {
        "input": {
            "query": "Show me the top 10 buyers of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk on raydium_launchpad"
        },
        "description": "Natural language query for top buyers on specific launchpad",
    },
    "buyers_all_tool": {
        "input": {
            "tool": "query_top_buyers",
            "tool_arguments": {
                "token_address": "F9WhPkcmLCVfgKucysxUWbqjrZfUYFsyQkxYnam9bonk",
                "limit": 40,
            },
        },
        "description": "Direct tool call for top buyers (all launchpads, limit 40)",
    },
    # Top sellers
    "sellers_all_query": {
        "input": {"query": "Show me the top 10 sellers of token 6SuHwUtzC1yZQhrfY3GZqcphPfhG2k9rPeBbB9Q3bonk"},
        "description": "Natural language query for top sellers (GROKPHONE token)",
    },
    "sellers_raydium_tool": {
        "input": {
            "tool": "query_top_sellers",
            "tool_arguments": {
                "token_address": "AKmQ3Uv7yZzU6YgTGf7hXfETcJu8kj6CaqvWmiv7bonk",
                "limit": 35,
                "launchpad": "raydium_launchpad",
            },
        },
        "description": "Direct tool call for top sellers on specific launchpad (gecko.jpg token)",
    },
    # OHLCV data
    "ohlcv_all_query": {
        "input": {"query": "Get OHLCV data for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"},
        "description": "Natural language query for OHLCV data (all launchpads)",
    },
    "ohlcv_raydium_query": {
        "input": {
            "query": "Get OHLCV data for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk on raydium_launchpad"
        },
        "description": "Natural language query for OHLCV data on specific launchpad",
    },
    "ohlcv_all_tool": {
        "input": {
            "tool": "query_ohlcv_data",
            "tool_arguments": {
                "token_address": "E8XPu39wNY4HfRgCRMmp2vee75N9gCAd9PnPsoesbonk",
                "limit": 50,
            },
        },
        "description": "Direct tool call for OHLCV data (UMS token, all launchpads)",
    },
    # Pair address
    "pair_all_query": {
        "input": {"query": "Get pair address for token So11111111111111111111111111111111111111112"},
        "description": "Natural language query for pair address (all launchpads)",
    },
    "pair_raydium_query": {
        "input": {
            "query": "Get pair address for token So11111111111111111111111111111111111111112 on raydium_launchpad"
        },
        "description": "Natural language query for pair address on specific launchpad",
    },
    "pair_raydium_tool": {
        "input": {
            "tool": "query_pair_address",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "launchpad": "raydium_launchpad",
            },
        },
        "description": "Direct tool call for pair address on specific launchpad (porkfolio token)",
    },
    # Liquidity
    "liquidity_query": {
        "input": {"query": "Get liquidity for pool address EUb3rQrPBdEZdTo8i6HtxHTMxtfKxBnGmqmAQxcXgSk4"},
        "description": "Natural language query for liquidity (porkfolio market)",
    },
    "liquidity_tool": {
        "input": {
            "tool": "query_liquidity",
            "tool_arguments": {"pool_address": "EJdLYGBMt6uvyijmGgGjz6aCMD4hkGtt6Tk5iV9YnH9b"},
        },
        "description": "Direct tool call for liquidity analysis",
    },
    # Recently created tokens
    "created_tokens_query": {
        "input": {"query": "Show me recently created LetsBonk.fun tokens"},
        "description": "Natural language query for recently created tokens",
    },
    "created_tokens_tool": {
        "input": {
            "tool": "query_recently_created_tokens",
            "tool_arguments": {"limit": 20},
        },
        "description": "Direct tool call for recently created tokens with limit 20",
    },
    # Bonding curve progress
    "bonding_curve_query": {
        "input": {"query": "Calculate bonding curve progress for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"},
        "description": "Natural language query for bonding curve progress (porkfolio token)",
    },
    "bonding_curve_tool": {
        "input": {
            "tool": "query_bonding_curve_progress",
            "tool_arguments": {"token_address": "F9WhPkcmLCVfgKucysxUWbqjrZfUYFsyQkxYnam9bonk"},
        },
        "description": "Direct tool call for bonding curve progress calculation",
    },
    # Tokens above 95%
    "tokens_95_percent_query": {
        "input": {"query": "Show me tokens above 95% bonding curve progress"},
        "description": "Natural language query for tokens above 95% bonding curve progress",
    },
    "tokens_95_percent_tool": {
        "input": {
            "tool": "query_tokens_above_95_percent",
            "tool_arguments": {"limit": 15},
        },
        "description": "Direct tool call for tokens above 95% with limit 15",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(LetsBonkTokenInfoAgent, TEST_CASES))
