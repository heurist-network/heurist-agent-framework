#!/usr/bin/env python3
"""
Test script for TrendingTokenAgent.
Tests the aggregation of trending tokens from multiple sources.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.trending_token_agent import TrendingTokenAgent


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_trending_source(source_name: str, data: dict):
    """Print trending data from a specific source."""
    print_section(source_name)

    if data.get("status") == "error":
        print(f"❌ Error: {data.get('error')}")
        return

    if not data or data.get("status") == "no_data":
        print("⚠️  No data available")
        return

    # Try to extract token list from different possible structures
    tokens = None
    if isinstance(data, dict):
        # Check common data keys
        for key in ["data", "tokens", "coins", "trending_coins", "graduated_tokens"]:
            if key in data:
                tokens = data[key]
                break

    if not tokens:
        print("📊 Raw response:")
        print(json.dumps(data, indent=2)[:1000])
        return

    if isinstance(tokens, list):
        print(f"✅ Found {len(tokens)} trending token(s)\n")
        for i, token in enumerate(tokens[:10], 1):  # Show top 10
            if isinstance(token, dict):
                # Extract common fields - handle nested token_info structure (PumpFun)
                token_info = token.get("token_info", {})
                name = token.get("name") or token_info.get("name") or token.get("token_name") or "Unknown"
                symbol = token.get("symbol") or token_info.get("symbol") or token.get("token_symbol") or "Unknown"
                chain = token.get("chain") or token.get("network") or "N/A"
                price = token.get("price") or token.get("price_usd") or token.get("current_price")
                volume = token.get("volume") or token.get("volume_24h") or token.get("total_volume") or token.get("total_volume_24h")
                market_cap = token.get("market_cap") or token.get("marketcap") or token.get("market_cap_usd")
                price_change = token.get("price_change_percentage_24h") or token.get("price_change_24h")
                rank = token.get("market_cap_rank") or token.get("rank")
                coingecko_id = token.get("coingecko_id")
                mint_address = token_info.get("mint_address")  # For Solana tokens

                print(f"[{i}] {name} ({symbol})")
                if coingecko_id:
                    print(f"    CoinGecko ID: {coingecko_id}")
                if mint_address:
                    print(f"    Mint Address: {mint_address[:20]}...{mint_address[-10:]}")
                if rank:
                    print(f"    Rank: #{rank}")
                if chain != "N/A":
                    print(f"    Chain: {chain}")
                if price:
                    print(f"    Price: ${price}")
                if market_cap:
                    print(f"    Market Cap: {market_cap}")
                if volume:
                    print(f"    24h Volume: {volume}")
                if price_change is not None:
                    sign = "+" if price_change > 0 else ""
                    print(f"    24h Change: {sign}{price_change:.2f}%")

                # Show any other notable fields
                for key, value in token.items():
                    if key not in [
                        "name",
                        "symbol",
                        "chain",
                        "price",
                        "volume",
                        "market_cap",
                        "token_name",
                        "token_symbol",
                        "network",
                        "price_usd",
                        "volume_24h",
                        "total_volume",
                        "total_volume_24h",
                        "marketcap",
                        "market_cap_usd",
                        "current_price",
                        "price_change_percentage_24h",
                        "price_change_24h",
                        "market_cap_rank",
                        "rank",
                        "coingecko_id",
                    ]:
                        # Show interesting metadata
                        if key in ["score", "trending_score", "graduation_time", "created_at"]:
                            print(f"    {key.replace('_', ' ').title()}: {value}")
                print()
    else:
        print("📊 Data structure:")
        print(json.dumps(tokens, indent=2)[:500])


async def test_trending_tokens():
    """Test the get_trending_tokens functionality."""
    print("\n🚀 TrendingTokenAgent Test Script")
    print_section("Initializing Agent")

    try:
        agent = TrendingTokenAgent()
        print("✅ Agent initialized successfully")

        print("\n⏳ Fetching trending tokens from all sources...")
        print("   (This may take a few seconds as we query multiple APIs)")

        result = await agent.get_trending_tokens()

        if result.get("status") == "error":
            print(f"\n❌ Error: {result.get('error')}")
            return

        print("\n✅ Successfully retrieved trending tokens!")

        data = result.get("data", {})

        # Print notes if available
        notes = data.get("notes")
        if notes:
            print_section("Notes")
            print(notes)

        # Print each source's trending tokens
        sources = [
            ("GMGN Trending (24h, Top 10)", "gmgn_trending"),
            ("CoinGecko Trending", "coingecko_trending"),
            ("Pump.fun Recent Graduations (24h)", "pumpfun_recent_graduated"),
            ("Twitter/ELFA Trending (24h)", "twitter_trending"),
        ]

        for source_name, source_key in sources:
            source_data = data.get(source_key, {})
            print_trending_source(source_name, source_data)

        # Print summary
        print_section("Summary")
        available_sources = sum(
            1
            for _, key in sources
            if data.get(key) and data[key].get("status") not in ["error", "no_data"]
        )
        print(f"Available data sources: {available_sources}/{len(sources)}")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n🏁 Test completed\n")


if __name__ == "__main__":
    asyncio.run(test_trending_tokens())
