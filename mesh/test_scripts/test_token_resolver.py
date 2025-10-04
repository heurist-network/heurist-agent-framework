#!/usr/bin/env python3
"""
Test script for TokenResolverAgent.
Modify the variables below to test different search/profile scenarios.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.token_resolver_agent import TokenResolverAgent

# ========== MODIFY THESE VARIABLES TO TEST DIFFERENT SCENARIOS ==========
# Test mode: "search" or "profile"
TEST_MODE = "search"

# For search mode
SEARCH_QUERY = "ETH"  # Can be address, symbol, or name
SEARCH_CHAIN = None  # Optional: "ethereum", "base", "solana", etc.
SEARCH_TYPE_HINT = None  # Optional: "address", "symbol", or "name"

# For profile mode
PROFILE_CHAIN = "base"  # "ethereum", "base", "solana", etc.
PROFILE_ADDRESS = "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b"  # Token address
PROFILE_SYMBOL = None  # Alternative: use symbol like "BTC" or "ETH"
PROFILE_COINGECKO_ID = None  # Alternative: use CoinGecko ID
PROFILE_INCLUDE = ["pairs"]  # Options: "pairs", "holders", "traders", "funding_rates", "technical_indicators"
PROFILE_TOP_N_PAIRS = 3  # Number of top pairs to return
PROFILE_INDICATOR_INTERVAL = "1d"  # "1h" or "1d"
# =====================================================================


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_results(results: dict, indent: int = 0):
    """Pretty print results with proper indentation."""
    indent_str = "  " * indent

    if isinstance(results, dict):
        for key, value in results.items():
            if isinstance(value, (dict, list)):
                print(f"{indent_str}{key}:")
                print_results(value, indent + 1)
            else:
                print(f"{indent_str}{key}: {value}")
    elif isinstance(results, list):
        for i, item in enumerate(results, 1):
            if isinstance(item, dict):
                print(f"{indent_str}[{i}]")
                print_results(item, indent + 1)
            else:
                print(f"{indent_str}[{i}] {item}")
    else:
        print(f"{indent_str}{results}")


async def test_search():
    """Test the search functionality."""
    print_section("Testing Token Search")

    print(f"Query: {SEARCH_QUERY}")
    if SEARCH_CHAIN:
        print(f"Chain: {SEARCH_CHAIN}")
    if SEARCH_TYPE_HINT:
        print(f"Type Hint: {SEARCH_TYPE_HINT}")

    agent = TokenResolverAgent()

    args = {"query": SEARCH_QUERY}
    if SEARCH_CHAIN:
        args["chain"] = SEARCH_CHAIN
    if SEARCH_TYPE_HINT:
        args["type_hint"] = SEARCH_TYPE_HINT

    try:
        result = await agent._handle_tool_logic("search", args)

        if result.get("status") == "error":
            print(f"\n❌ Error: {result.get('error')}")
            return

        print("\n✅ Search successful!")

        data = result.get("data", {})
        results = data.get("results", [])

        print(f"\nFound {len(results)} result(s)")
        print(f"Timestamp: {data.get('timestamp')}")

        for i, token in enumerate(results, 1):
            print(f"\n--- Token {i} ---")
            print(f"Name: {token.get('name')}")
            print(f"Symbol: {token.get('symbol')}")
            print(f"Chain: {token.get('chain')}")
            print(f"Address: {token.get('address')}")
            print(f"CoinGecko ID: {token.get('coingecko_id')}")
            print(f"Price USD: ${token.get('price_usd')}")
            print(f"Market Cap USD: ${token.get('market_cap_usd')}")

            links = token.get('links', {})
            if any(links.values()):
                print("\nLinks:")
                if links.get('website'):
                    print(f"  Website: {links['website']}")
                if links.get('twitter'):
                    print(f"  Twitter: {links['twitter']}")
                if links.get('telegram'):
                    print(f"  Telegram: {links['telegram']}")

            top_pairs = token.get('top_pairs', [])
            if top_pairs:
                print(f"\nTop {len(top_pairs)} Pair(s):")
                for j, pair in enumerate(top_pairs, 1):
                    print(f"  [{j}] {pair.get('chain')} - {pair.get('dex')}")
                    print(f"      Liquidity: ${pair.get('liquidity_usd')}")
                    print(f"      Volume 24h: ${pair.get('volume24h_usd')}")
                    print(f"      Price: ${pair.get('price_usd')}")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_profile():
    """Test the profile functionality."""
    print_section("Testing Token Profile")

    if PROFILE_SYMBOL:
        print(f"Symbol: {PROFILE_SYMBOL}")
    elif PROFILE_COINGECKO_ID:
        print(f"CoinGecko ID: {PROFILE_COINGECKO_ID}")
    else:
        print(f"Chain: {PROFILE_CHAIN}")
        print(f"Address: {PROFILE_ADDRESS}")

    print(f"Include sections: {', '.join(PROFILE_INCLUDE)}")
    print(f"Top N pairs: {PROFILE_TOP_N_PAIRS}")

    agent = TokenResolverAgent()

    args = {
        "include": PROFILE_INCLUDE,
        "top_n_pairs": PROFILE_TOP_N_PAIRS,
        "indicator_interval": PROFILE_INDICATOR_INTERVAL,
    }

    if PROFILE_SYMBOL:
        args["symbol"] = PROFILE_SYMBOL
    elif PROFILE_COINGECKO_ID:
        args["coingecko_id"] = PROFILE_COINGECKO_ID
    else:
        args["chain"] = PROFILE_CHAIN
        args["address"] = PROFILE_ADDRESS

    try:
        result = await agent._handle_tool_logic("profile", args)

        if result.get("status") == "error":
            print(f"\n❌ Error: {result.get('error')}")
            return

        print("\n✅ Profile retrieved successfully!")

        data = result.get("data", {})

        print("\n--- Basic Info ---")
        print(f"Name: {data.get('name')}")
        print(f"Symbol: {data.get('symbol')}")
        print(f"CoinGecko ID: {data.get('coingecko_id')}")
        print(f"Timestamp: {data.get('timestamp')}")

        contracts = data.get('contracts', {})
        if contracts:
            print("\n--- Contracts ---")
            for chain, address in contracts.items():
                print(f"{chain}: {address}")

        categories = data.get('categories', [])
        if categories:
            print(f"\n--- Categories ---")
            print(f"{', '.join(categories)}")

        links = data.get('links', {})
        if any(links.values()):
            print("\n--- Links ---")
            if links.get('website'):
                print(f"Website: {links['website']}")
            if links.get('twitter'):
                print(f"Twitter: {links['twitter']}")
            if links.get('telegram'):
                print(f"Telegram: {links['telegram']}")
            if links.get('github'):
                print(f"GitHub: {links['github']}")

        fundamentals = data.get('fundamentals')
        if fundamentals:
            print("\n--- Fundamentals ---")
            print(f"Price USD: ${fundamentals.get('price_usd')}")
            print(f"Market Cap USD: ${fundamentals.get('market_cap_usd')}")
            print(f"FDV USD: ${fundamentals.get('fdv_usd')}")
            print(f"Volume 24h USD: ${fundamentals.get('volume24h_usd')}")

        supply = data.get('supply')
        if supply:
            print("\n--- Supply ---")
            print(f"Circulating: {supply.get('circulating')}")
            print(f"Total: {supply.get('total')}")
            print(f"Max: {supply.get('max')}")

        price_extremes = data.get('price_extremes')
        if price_extremes:
            print("\n--- Price Extremes ---")
            print(f"ATH: ${price_extremes.get('ath_usd')} ({price_extremes.get('ath_date')})")
            print(f"ATL: ${price_extremes.get('atl_usd')} ({price_extremes.get('atl_date')})")

        best_pool = data.get('best_pool')
        if best_pool:
            print("\n--- Best Pool ---")
            print(f"Chain: {best_pool.get('chain')}")
            print(f"DEX: {best_pool.get('dex')}")
            print(f"Pair Address: {best_pool.get('pair_address')}")
            print(f"Price USD: ${best_pool.get('price_usd')}")
            print(f"Liquidity USD: ${best_pool.get('liquidity_usd')}")
            print(f"Volume 24h USD: ${best_pool.get('volume24h_usd')}")

        top_pools = data.get('top_pools', [])
        if top_pools and len(top_pools) > 1:
            print(f"\n--- Top {len(top_pools)} Pools ---")
            for i, pool in enumerate(top_pools, 1):
                print(f"\n[{i}] {pool.get('chain')} - {pool.get('dex')}")
                print(f"    Liquidity: ${pool.get('liquidity_usd')}")
                print(f"    Volume 24h: ${pool.get('volume24h_usd')}")

        extras = data.get('extras', {})
        if extras:
            print("\n--- Extras ---")
            for key, value in extras.items():
                print(f"\n{key}:")
                if isinstance(value, str):
                    print(f"  {value[:200]}..." if len(value) > 200 else f"  {value}")
                else:
                    print(f"  {json.dumps(value, indent=2)[:500]}...")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()


async def main():
    """Main test runner."""
    print("\n🚀 TokenResolverAgent Test Script")

    if TEST_MODE == "search":
        await test_search()
    elif TEST_MODE == "profile":
        await test_profile()
    else:
        print(f"❌ Invalid TEST_MODE: {TEST_MODE}. Must be 'search' or 'profile'")
        return

    print("\n🏁 Test completed\n")


if __name__ == "__main__":
    asyncio.run(main())
