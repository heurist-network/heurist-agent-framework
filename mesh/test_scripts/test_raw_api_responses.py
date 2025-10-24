#!/usr/bin/env python3
"""
Test script to check raw API responses from CoinGecko and PumpFun agents.
This helps identify additional data fields that might be useful.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.coingecko_token_info_agent import CoinGeckoTokenInfoAgent
from mesh.agents.pumpfun_token_agent import PumpFunTokenAgent


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}")


async def test_coingecko_raw_response():
    """Test CoinGecko trending coins raw API response."""
    print_section("CoinGecko Trending Coins - Raw API Response")

    agent = CoinGeckoTokenInfoAgent()

    try:
        # Call the internal method directly to get raw response
        result = await agent._get_trending_coins()

        print("\n📊 Full Response Structure:")
        print(json.dumps(result, indent=2))

        # Check what fields are available in the raw API response
        if "trending_coins" in result:
            print("\n🔍 Available fields in first coin:")
            if result["trending_coins"]:
                first_coin = result["trending_coins"][0]
                print(json.dumps(first_coin, indent=2))

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def test_coingecko_raw_api():
    """Test direct CoinGecko API call to see full response."""
    print_section("CoinGecko Trending - Direct API Response (Before Preprocessing)")

    import os

    import aiohttp

    api_key = os.getenv("COINGECKO_API_KEY")
    if not api_key:
        print("❌ COINGECKO_API_KEY not found")
        return

    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        url = "https://api.coingecko.com/api/v3/search/trending"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                print("\n📊 Raw API Response (first coin only):")
                if "coins" in data and data["coins"]:
                    first_coin = data["coins"][0]
                    print(json.dumps(first_coin, indent=2))

                    print("\n🔍 Available data fields in first coin:")
                    if "item" in first_coin:
                        item = first_coin["item"]
                        print(f"Available keys in 'item': {list(item.keys())}")

                        if "data" in item:
                            print(f"Available keys in 'data': {list(item['data'].keys())}")
                            print(f"\nFull 'data' object:")
                            print(json.dumps(item["data"], indent=2))

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def test_pumpfun_raw_response():
    """Test PumpFun graduated tokens raw API response."""
    print_section("PumpFun Graduated Tokens - Raw API Response")

    agent = PumpFunTokenAgent()

    try:
        # Call the internal method directly to get raw response
        result = await agent.query_latest_graduated_tokens(timeframe=24)

        print("\n📊 Full Response Structure:")
        print(json.dumps(result, indent=2, default=str))

        # Check what fields are available
        if "graduated_tokens" in result and result["graduated_tokens"]:
            print("\n🔍 Available fields in first graduated token:")
            first_token = result["graduated_tokens"][0]
            print(json.dumps(first_token, indent=2, default=str))

            print("\n📋 Summary of available fields:")
            print(f"  - Top-level keys: {list(result.keys())}")
            print(f"  - Token data keys: {list(first_token.keys())}")
            if "token_info" in first_token:
                print(f"  - Token info keys: {list(first_token['token_info'].keys())}")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback

        traceback.print_exc()


async def main():
    """Main test runner."""
    print("\n🚀 Testing Raw API Responses\n")

    await test_coingecko_raw_api()
    await test_coingecko_raw_response()
    await test_pumpfun_raw_response()

    print("\n🏁 Test completed\n")


if __name__ == "__main__":
    asyncio.run(main())
