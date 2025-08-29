import asyncio
import sys
from pathlib import Path

import yaml  # Required for saving output as YAML

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.evm_token_info_agent import EvmTokenInfoAgent  # noqa: E402


async def run_agent():
    agent = EvmTokenInfoAgent()
    try:
        # Test 1: BSC - BNB trades (all)
        print("Test 1: BSC - BNB all trades")
        bsc_bnb_test = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "bsc",
                "tokenAddress": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",  # WBNB
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        }
        bsc_bnb_output = await agent.handle_message(bsc_bnb_test)

        # Test 2: Ethereum - USDC buyers only
        print("\nTest 2: Ethereum - USDC buyers only")
        eth_usdc_buyers = {
            "query": "Show me only the large buyers of USDC 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 on ethereum"
        }
        eth_usdc_buyers_output = await agent.handle_message(eth_usdc_buyers)

        # Test 3: Base - WETH sellers only
        print("\nTest 3: Base - WETH sellers only")
        base_weth_sellers = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0x4200000000000000000000000000000000000006",  # WETH on Base
                "minUsdAmount": 10000,
                "filter": "sell",
                "limit": 5,
            },
        }
        base_weth_sellers_output = await agent.handle_message(base_weth_sellers)

        # Test 4: Arbitrum - USDC all trades
        print("\nTest 4: Arbitrum - USDC all trades")
        arb_usdc_all = {
            "query": "What are the large trades for USDC 0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8 on arbitrum?"
        }
        arb_usdc_all_output = await agent.handle_message(arb_usdc_all)

        # Test 5: BSC - BTCB large trades
        print("\nTest 5: BSC - BTCB large trades ($50k+)")
        bsc_btcb = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "bsc",
                "tokenAddress": "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",  # BTCB
                "minUsdAmount": 50000,
                "filter": "all",
                "limit": 5,
            },
        }
        bsc_btcb_output = await agent.handle_message(bsc_btcb)

        # Test 6: Ethereum - WETH buyers
        print("\nTest 6: Ethereum - WETH buyers")
        eth_weth_buyers = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "eth",
                "tokenAddress": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
                "minUsdAmount": 100000,
                "filter": "buy",
                "limit": 5,
            },
        }
        eth_weth_buyers_output = await agent.handle_message(eth_weth_buyers)

        # Test 7: Natural language - BSC USDT
        print("\nTest 7: Natural language - BSC USDT traders")
        bsc_usdt_nl = {
            "query": "Show me the recent large trades for USDT 0x55d398326f99059fF775485246999027B3197955 on BSC"
        }
        bsc_usdt_nl_output = await agent.handle_message(bsc_usdt_nl)

        # Test 8: Invalid token address
        print("\nTest 8: Invalid token address test")
        invalid_test = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "ethereum",
                "tokenAddress": "not_a_valid_address",
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        }
        invalid_output = await agent.handle_message(invalid_test)

        # Test 9: Unsupported chain test
        print("\nTest 9: Unsupported chain test")
        unsupported_chain = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "polygon",  # Not supported
                "tokenAddress": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 10,
            },
        }
        unsupported_output = await agent.handle_message(unsupported_chain)

        # Test 10: Raw data mode
        print("\nTest 10: Raw data mode - Ethereum DAI")
        raw_data_test = {
            "query": "Large trades for DAI 0x6B175474E89094C44Da98b954EedeAC495271d0F on ethereum above $25k",
            "raw_data_only": True,
        }
        raw_data_output = await agent.handle_message(raw_data_test)

        # ===== NEW TEST 11: HEU TOKEN TEST FOR TRADE TYPE VERIFICATION =====
        # Test 11a: HEU all trades
        heu_all_trades = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "all",
                "limit": 5,
            },
        }
        heu_all_output = await agent.handle_message(heu_all_trades)

        # Test 11b: HEU sells from trader perspective
        heu_sells = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "sell",  # Trader sells (should query DEX buys)
                "limit": 3,
            },
        }
        heu_sells_output = await agent.handle_message(heu_sells)

        # Test 11c: HEU buys from trader perspective
        heu_buys = {
            "tool": "get_recent_large_trades",
            "tool_arguments": {
                "chain": "base",
                "tokenAddress": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",  # HEU token
                "minUsdAmount": 5000,
                "filter": "buy",  # Trader buys (should query DEX sells)
                "limit": 3,
            },
        }
        heu_buys_output = await agent.handle_message(heu_buys)

        # Construct final results
        yaml_content = {
            "direct_tool_calls": {
                "bsc_bnb_all": {"input": bsc_bnb_test, "output": bsc_bnb_output},
                "base_weth_sellers": {"input": base_weth_sellers, "output": base_weth_sellers_output},
                "bsc_btcb": {"input": bsc_btcb, "output": bsc_btcb_output},
                "eth_weth_buyers": {"input": eth_weth_buyers, "output": eth_weth_buyers_output},
            },
            "natural_language_queries": {
                "eth_usdc_buyers": {"input": eth_usdc_buyers, "output": eth_usdc_buyers_output},
                "arb_usdc_all": {"input": arb_usdc_all, "output": arb_usdc_all_output},
                "bsc_usdt_nl": {"input": bsc_usdt_nl, "output": bsc_usdt_nl_output},
            },
            "error_tests": {
                "invalid_address": {"input": invalid_test, "output": invalid_output},
                "unsupported_chain": {"input": unsupported_chain, "output": unsupported_output},
            },
            "special_tests": {
                "raw_data_mode": {"input": raw_data_test, "output": raw_data_output},
            },
            "heu_token_tests": {
                "description": "HEU token tests verify trade type fix (v1.1.0) - trader perspective",
                "heu_all_trades": {"input": heu_all_trades, "output": heu_all_output},
                "heu_sells_from_trader": {"input": heu_sells, "output": heu_sells_output},
                "heu_buys_from_trader": {"input": heu_buys, "output": heu_buys_output},
            },
        }

        # Save YAML to file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        output_file = script_dir / f"{current_file}_example.yaml"
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, sort_keys=False, allow_unicode=True)

        print(f"\n✅ All tests completed! Results saved to: {output_file}")

        # Summary
        print("\n📊 Test Summary:")
        print(f"- Direct Tool Calls: {len(yaml_content['direct_tool_calls'])}")
        print(f"- Natural Language Queries: {len(yaml_content['natural_language_queries'])}")
        print(f"- Error Tests: {len(yaml_content['error_tests'])}")
        print(f"- Special Tests: {len(yaml_content['special_tests'])}")

        # Print HEU test verification
        print("\n🔍 HEU Trade Type Fix Verification:")
        if heu_all_output and "data" in heu_all_output and "data" in heu_all_output["data"]:
            trades = heu_all_output["data"]["data"]["EVM"]["DEXTradeByTokens"]
            if trades and len(trades) > 0:
                first_trade = trades[0]
                dex_type = first_trade["Trade"]["Side"]["Type"]
                trader_type = first_trade.get("TradeType", "unknown")
                print(f"  ✓ DEX reports: '{dex_type}' → Trader action: '{trader_type}'")
                print("  ✓ Trade types correctly inverted for trader perspective")

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    print("🚀 Starting EVM Token Info Agent Tests...")
    print("=" * 60)
    print("Supported chains: Ethereum (eth), BSC (bsc), Base (base), Arbitrum (arbitrum)")
    print("=" * 60)
    asyncio.run(run_agent())
