import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.lets_bonk_token_info_agent import LetsBonkTokenInfoAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = LetsBonkTokenInfoAgent()
    try:
        # Test about to graduate tokens
        print("Testing about to graduate tokens (query)")
        graduate_query_input = {"query": "Show me top 10 tokens about to graduate on LetsBonk.fun"}
        graduate_query_output = await agent.handle_message(graduate_query_input)

        print("Testing about to graduate tokens (tool)")
        graduate_tool_input = {
            "tool": "query_about_to_graduate_tokens",
            "tool_arguments": {"limit": 15},
        }
        graduate_tool_output = await agent.handle_message(graduate_tool_input)

        # Test latest trades - with and without launchpad filter
        print("Testing latest trades - ALL LAUNCHPADS (query)")
        trades_all_query_input = {
            "query": "Show me the latest 10 trades for token So11111111111111111111111111111111111111112"
        }
        trades_all_query_output = await agent.handle_message(trades_all_query_input)

        print("Testing latest trades - SPECIFIC LAUNCHPAD (query)")
        trades_raydium_query_input = {
            "query": "Show me the latest 10 trades for token So11111111111111111111111111111111111111112 on raydium_launchpad"
        }
        trades_raydium_query_output = await agent.handle_message(trades_raydium_query_input)

        print("Testing latest trades - ALL LAUNCHPADS (tool)")
        trades_all_tool_input = {
            "tool": "query_latest_trades",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "limit": 25,
            },  # porkfolio token - no launchpad filter
        }
        trades_all_tool_output = await agent.handle_message(trades_all_tool_input)

        print("Testing latest trades - SPECIFIC LAUNCHPAD (tool)")
        trades_raydium_tool_input = {
            "tool": "query_latest_trades",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "limit": 25,
                "launchpad": "raydium_launchpad",
            },  # porkfolio token with launchpad filter
        }
        trades_raydium_tool_output = await agent.handle_message(trades_raydium_tool_input)

        # Test latest price - with and without launchpad filter
        print("Testing latest price - ALL LAUNCHPADS (query)")
        price_all_query_input = {
            "query": "What's the current price of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk?"
        }  # porkfolio
        price_all_query_output = await agent.handle_message(price_all_query_input)

        print("Testing latest price - SPECIFIC LAUNCHPAD (tool)")
        price_raydium_tool_input = {
            "tool": "query_latest_price",
            "tool_arguments": {
                "token_address": "GN7BPjVW6UfexZ1Tu6UTa9X7Qd9pJBDNEstR5Lv3bonk",
                "launchpad": "raydium_launchpad",
            },  # Groktor token with filter
        }
        price_raydium_tool_output = await agent.handle_message(price_raydium_tool_input)

        # Test top buyers - with and without launchpad filter
        print("Testing top buyers - ALL LAUNCHPADS (query)")
        buyers_all_query_input = {
            "query": "Show me the top 10 buyers of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"
        }  # porkfolio
        buyers_all_query_output = await agent.handle_message(buyers_all_query_input)

        print("Testing top buyers - SPECIFIC LAUNCHPAD (query)")
        buyers_raydium_query_input = {
            "query": "Show me the top 10 buyers of token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk on raydium_launchpad"
        }
        buyers_raydium_query_output = await agent.handle_message(buyers_raydium_query_input)

        print("Testing top buyers - ALL LAUNCHPADS (tool)")
        buyers_all_tool_input = {
            "tool": "query_top_buyers",
            "tool_arguments": {
                "token_address": "F9WhPkcmLCVfgKucysxUWbqjrZfUYFsyQkxYnam9bonk",
                "limit": 40,
            },  # "How is this not tokenized yet" - no filter
        }
        buyers_all_tool_output = await agent.handle_message(buyers_all_tool_input)

        # Test top sellers - with and without launchpad filter
        print("Testing top sellers - ALL LAUNCHPADS (query)")
        sellers_all_query_input = {
            "query": "Show me the top 10 sellers of token 6SuHwUtzC1yZQhrfY3GZqcphPfhG2k9rPeBbB9Q3bonk"  # GROKPHONE
        }
        sellers_all_query_output = await agent.handle_message(sellers_all_query_input)

        print("Testing top sellers - SPECIFIC LAUNCHPAD (tool)")
        sellers_raydium_tool_input = {
            "tool": "query_top_sellers",
            "tool_arguments": {
                "token_address": "AKmQ3Uv7yZzU6YgTGf7hXfETcJu8kj6CaqvWmiv7bonk",
                "limit": 35,
                "launchpad": "raydium_launchpad",
            },  # gecko.jpg with filter
        }
        sellers_raydium_tool_output = await agent.handle_message(sellers_raydium_tool_input)

        # Test OHLCV data - with and without launchpad filter
        print("Testing OHLCV data - ALL LAUNCHPADS (query)")
        ohlcv_all_query_input = {
            "query": "Get OHLCV data for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"
        }  # porkfolio
        ohlcv_all_query_output = await agent.handle_message(ohlcv_all_query_input)

        print("Testing OHLCV data - SPECIFIC LAUNCHPAD (query)")
        ohlcv_raydium_query_input = {
            "query": "Get OHLCV data for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk on raydium_launchpad"
        }
        ohlcv_raydium_query_output = await agent.handle_message(ohlcv_raydium_query_input)

        print("Testing OHLCV data - ALL LAUNCHPADS (tool)")
        ohlcv_all_tool_input = {
            "tool": "query_ohlcv_data",
            "tool_arguments": {
                "token_address": "E8XPu39wNY4HfRgCRMmp2vee75N9gCAd9PnPsoesbonk",
                "limit": 50,
            },  # UMS token - no filter
        }
        ohlcv_all_tool_output = await agent.handle_message(ohlcv_all_tool_input)

        # Test pair address - with and without launchpad filter
        print("Testing pair address - ALL LAUNCHPADS (query)")
        pair_all_query_input = {"query": "Get pair address for token So11111111111111111111111111111111111111112"}
        pair_all_query_output = await agent.handle_message(pair_all_query_input)

        print("Testing pair address - SPECIFIC LAUNCHPAD (query)")
        pair_raydium_query_input = {
            "query": "Get pair address for token So11111111111111111111111111111111111111112 on raydium_launchpad"
        }
        pair_raydium_query_output = await agent.handle_message(pair_raydium_query_input)

        print("Testing pair address - SPECIFIC LAUNCHPAD (tool)")
        pair_raydium_tool_input = {
            "tool": "query_pair_address",
            "tool_arguments": {
                "token_address": "AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk",
                "launchpad": "raydium_launchpad",
            },  # porkfolio with filter
        }
        pair_raydium_tool_output = await agent.handle_message(pair_raydium_tool_input)

        # Test liquidity - using the market address from porkfolio
        print("Testing liquidity (query)")
        liquidity_query_input = {
            "query": "Get liquidity for pool address EUb3rQrPBdEZdTo8i6HtxHTMxtfKxBnGmqmAQxcXgSk4"
        }  # porkfolio market
        liquidity_query_output = await agent.handle_message(liquidity_query_input)

        print("Testing liquidity (tool)")
        liquidity_tool_input = {
            "tool": "query_liquidity",
            "tool_arguments": {
                "pool_address": "EJdLYGBMt6uvyijmGgGjz6aCMD4hkGtt6Tk5iV9YnH9b"
            },  # "How is this not tokenized yet" market
        }
        liquidity_tool_output = await agent.handle_message(liquidity_tool_input)

        # Test recently created tokens
        print("Testing recently created tokens (query)")
        created_query_input = {"query": "Show me recently created LetsBonk.fun tokens"}
        created_query_output = await agent.handle_message(created_query_input)

        print("Testing recently created tokens (tool)")
        created_tool_input = {
            "tool": "query_recently_created_tokens",
            "tool_arguments": {"limit": 20},
        }
        created_tool_output = await agent.handle_message(created_tool_input)

        # Test bonding curve progress - using active LetsBonk tokens
        print("Testing bonding curve progress (query)")
        bonding_query_input = {
            "query": "Calculate bonding curve progress for token AF5ZJKsC12VsvmLASF6JWDZQjeKMBdD7mCQYSHHnbonk"  # porkfolio
        }
        bonding_query_output = await agent.handle_message(bonding_query_input)

        print("Testing bonding curve progress (tool)")
        bonding_tool_input = {
            "tool": "query_bonding_curve_progress",
            "tool_arguments": {
                "token_address": "F9WhPkcmLCVfgKucysxUWbqjrZfUYFsyQkxYnam9bonk"
            },  # "How is this not tokenized yet"
        }
        bonding_tool_output = await agent.handle_message(bonding_tool_input)

        # Test tokens above 95%
        print("Testing tokens above 95% bonding curve progress (query)")
        percent_95_query_input = {"query": "Show me tokens above 95% bonding curve progress"}
        percent_95_query_output = await agent.handle_message(percent_95_query_input)

        print("Testing tokens above 95% bonding curve progress (tool)")
        percent_95_tool_input = {
            "tool": "query_tokens_above_95_percent",
            "tool_arguments": {"limit": 15},
        }
        percent_95_tool_output = await agent.handle_message(percent_95_tool_input)

        # Save results to YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "about_to_graduate": {
                "natural_language_query": {"input": graduate_query_input, "output": graduate_query_output},
                "direct_tool_call": {"input": graduate_tool_input, "output": graduate_tool_output},
            },
            "latest_trades": {
                "all_launchpads": {
                    "natural_language_query": {"input": trades_all_query_input, "output": trades_all_query_output},
                    "direct_tool_call": {"input": trades_all_tool_input, "output": trades_all_tool_output},
                },
                "specific_launchpad": {
                    "natural_language_query": {
                        "input": trades_raydium_query_input,
                        "output": trades_raydium_query_output,
                    },
                    "direct_tool_call": {"input": trades_raydium_tool_input, "output": trades_raydium_tool_output},
                },
            },
            "latest_price": {
                "all_launchpads": {
                    "natural_language_query": {"input": price_all_query_input, "output": price_all_query_output},
                },
                "specific_launchpad": {
                    "direct_tool_call": {"input": price_raydium_tool_input, "output": price_raydium_tool_output},
                },
            },
            "top_buyers": {
                "all_launchpads": {
                    "natural_language_query": {"input": buyers_all_query_input, "output": buyers_all_query_output},
                    "direct_tool_call": {"input": buyers_all_tool_input, "output": buyers_all_tool_output},
                },
                "specific_launchpad": {
                    "natural_language_query": {
                        "input": buyers_raydium_query_input,
                        "output": buyers_raydium_query_output,
                    },
                },
            },
            "top_sellers": {
                "all_launchpads": {
                    "natural_language_query": {"input": sellers_all_query_input, "output": sellers_all_query_output},
                },
                "specific_launchpad": {
                    "direct_tool_call": {"input": sellers_raydium_tool_input, "output": sellers_raydium_tool_output},
                },
            },
            "ohlcv_data": {
                "all_launchpads": {
                    "natural_language_query": {"input": ohlcv_all_query_input, "output": ohlcv_all_query_output},
                    "direct_tool_call": {"input": ohlcv_all_tool_input, "output": ohlcv_all_tool_output},
                },
                "specific_launchpad": {
                    "natural_language_query": {
                        "input": ohlcv_raydium_query_input,
                        "output": ohlcv_raydium_query_output,
                    },
                },
            },
            "pair_address": {
                "all_launchpads": {
                    "natural_language_query": {"input": pair_all_query_input, "output": pair_all_query_output},
                },
                "specific_launchpad": {
                    "natural_language_query": {"input": pair_raydium_query_input, "output": pair_raydium_query_output},
                    "direct_tool_call": {"input": pair_raydium_tool_input, "output": pair_raydium_tool_output},
                },
            },
            "liquidity": {
                "natural_language_query": {"input": liquidity_query_input, "output": liquidity_query_output},
                "direct_tool_call": {"input": liquidity_tool_input, "output": liquidity_tool_output},
            },
            "recently_created_tokens": {
                "natural_language_query": {"input": created_query_input, "output": created_query_output},
                "direct_tool_call": {"input": created_tool_input, "output": created_tool_output},
            },
            "bonding_curve_progress": {
                "natural_language_query": {"input": bonding_query_input, "output": bonding_query_output},
                "direct_tool_call": {"input": bonding_tool_input, "output": bonding_tool_output},
            },
            "tokens_above_95_percent": {
                "natural_language_query": {"input": percent_95_query_input, "output": percent_95_query_output},
                "direct_tool_call": {"input": percent_95_tool_input, "output": percent_95_tool_output},
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
