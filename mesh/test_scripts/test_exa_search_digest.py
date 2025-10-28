import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.exa_search_digest_agent import ExaSearchDigestAgent  # noqa: E402


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def print_subsection(title: str):
    print("\n" + "-" * 60)
    print(f" {title}")
    print("-" * 60)


async def test_web_search_basic(agent):
    print_section("TEST 1: Basic Web Search")

    query = "Latest developments in artificial intelligence safety"

    start_time = time.time()
    result = await agent.exa_web_search(search_term=query, limit=7)
    elapsed = time.time() - start_time

    print(f"Query: {query}")
    print(f"Status: {result.get('status')}")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

    if result.get("status") == "success":
        summary = result["data"].get("processed_summary", "")
        print(f"\n📝 Processed Summary (length: {len(summary)} chars):")
        print("-" * 40)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    else:
        print(f"❌ Error: {result.get('error')}")

    return elapsed


async def test_web_search_with_time_filter(agent):
    print_section("TEST 2: Web Search with Time Filter (Past Week)")

    query = "cryptocurrency market trends"

    start_time = time.time()
    result = await agent.exa_web_search(search_term=query, time_filter="past_week", limit=5)
    elapsed = time.time() - start_time

    print(f"Query: {query}")
    print("Time Filter: past_week")
    print(f"Status: {result.get('status')}")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

    if result.get("status") == "success":
        summary = result["data"].get("processed_summary", "")
        print(f"\n📝 Processed Summary (length: {len(summary)} chars):")
        print("-" * 40)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    else:
        print(f"❌ Error: {result.get('error')}")

    return elapsed


async def test_scrape_url(agent):
    print_section("TEST 3: Scrape URL")

    url = "https://techcrunch.com"

    start_time = time.time()
    result = await agent.exa_scrape_url(url=url)
    elapsed = time.time() - start_time

    print(f"URL: {url}")
    print(f"Status: {result.get('status')}")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

    if result.get("status") == "success":
        summary = result["data"].get("processed_summary", "")
        print(f"\n📝 Processed Summary (length: {len(summary)} chars):")
        print("-" * 40)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    else:
        print(f"❌ Error: {result.get('error')}")

    return elapsed


async def test_natural_language_query(agent):
    print_section("TEST 4: Natural Language Query")

    query = "What are the recent breakthroughs in quantum computing in the past month?"

    start_time = time.time()
    result = await agent.handle_message({"query": query, "raw_data_only": False})
    elapsed = time.time() - start_time

    print(f"Query: {query}")
    print(f"Status: {result.get('status')}")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

    if result.get("status") == "success":
        data = result.get("data", {})
        if isinstance(data, str):
            print(f"\n📝 Response (length: {len(data)} chars):")
            print("-" * 40)
            print(data[:500] + "..." if len(data) > 500 else data)
        else:
            print("\n📝 Response:")
            print("-" * 40)
            print(str(data)[:500])
    else:
        print(f"❌ Error: {result.get('error')}")

    return elapsed


async def test_direct_tool_call(agent):
    print_section("TEST 5: Direct Tool Call - Search with Parameters")

    start_time = time.time()
    result = await agent.handle_message(
        {
            "tool": "exa_web_search",
            "tool_arguments": {
                "search_term": "Ethereum layer 2 scaling solutions",
                "time_filter": "past_month",
                "limit": 8,
            },
            "raw_data_only": True,
        }
    )
    elapsed = time.time() - start_time

    print("Tool: exa_web_search")
    print("Search Term: Ethereum layer 2 scaling solutions")
    print("Time Filter: past_month")
    print("Limit: 8")
    print(f"Status: {result.get('status')}")
    print(f"⏱️  Time taken: {elapsed:.2f} seconds")

    if result.get("status") == "success":
        data = result.get("data", {})
        summary = data.get("processed_summary", "") if isinstance(data, dict) else str(data)
        print(f"\n📝 Raw Data Response (length: {len(summary)} chars):")
        print("-" * 40)
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    else:
        print(f"❌ Error: {result.get('error')}")

    return elapsed


async def compare_with_firecrawl():
    print_section("COMPARISON: Exa vs Firecrawl (if available)")

    try:
        from mesh.agents.firecrawl_search_digest_agent import FirecrawlSearchDigestAgent

        exa_agent = ExaSearchDigestAgent()
        firecrawl_agent = FirecrawlSearchDigestAgent()

        query = "Bitcoin price prediction analysis"

        print_subsection("Testing Exa Search Digest")
        start_time = time.time()
        exa_result = await exa_agent.exa_web_search(search_term=query, limit=7)
        exa_time = time.time() - start_time

        print(f"Exa Status: {exa_result.get('status')}")
        print(f"Exa Time: {exa_time:.2f}s")

        print_subsection("Testing Firecrawl Search Digest")
        start_time = time.time()
        firecrawl_result = await firecrawl_agent.firecrawl_web_search(search_term=query, limit=7)
        firecrawl_time = time.time() - start_time

        print(f"Firecrawl Status: {firecrawl_result.get('status')}")
        print(f"Firecrawl Time: {firecrawl_time:.2f}s")

        print(f"\n🏆 Speed Difference: Exa is {firecrawl_time - exa_time:.2f}s faster")
        print(f"   Percentage: {((firecrawl_time - exa_time) / firecrawl_time * 100):.1f}% faster")

    except ImportError:
        print("FirecrawlSearchDigestAgent not available for comparison")
    except Exception as e:
        print(f"Comparison failed: {e}")


async def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " EXA SEARCH DIGEST AGENT - Comprehensive Test Suite".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    print(f"\n📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize agent
    print("\n🔧 Initializing Exa Search Digest Agent...")
    try:
        agent = ExaSearchDigestAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return

    # Track all test times
    test_times = {}

    # Run tests
    try:
        # Test 1: Basic search
        test_times["basic_search"] = await test_web_search_basic(agent)
        await asyncio.sleep(1)
        test_times["time_filtered_search"] = await test_web_search_with_time_filter(agent)
        await asyncio.sleep(1)
        test_times["scrape_url"] = await test_scrape_url(agent)
        await asyncio.sleep(1)
        test_times["natural_language"] = await test_natural_language_query(agent)
        await asyncio.sleep(1)
        test_times["direct_tool_call"] = await test_direct_tool_call(agent)
        await compare_with_firecrawl()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()

    # Summary
    print_section("TEST SUMMARY - Performance Metrics")

    print("\n📊 LATENCY MEASUREMENTS:\n")
    print("Test Case                    | Time (seconds)")
    print("-" * 50)

    total_time = 0
    for test_name, test_time in test_times.items():
        print(f"{test_name.ljust(28)} | {test_time:.2f}s")
        total_time += test_time

    if test_times:
        avg_time = total_time / len(test_times)
        print("-" * 50)
        print(f"{'Average Time'.ljust(28)} | {avg_time:.2f}s")
        print(f"{'Total Time'.ljust(28)} | {total_time:.2f}s")

    print("\n\n✨ KEY FEATURES TESTED:")
    print(" ✅ Neural/semantic search (Exa's strength)")
    print(" ✅ Time-based filtering")
    print(" ✅ URL scraping with /contents endpoint")
    print(" ✅ LLM summarization (concise mode)")
    print(" ✅ Natural language queries")
    print(" ✅ Direct tool calls with raw data")

    print("\n\n🎯 EXPECTED PERFORMANCE:")
    print(" • Target: 5-7s faster than Firecrawl (~15-20s)")
    print(" • Actual: See comparison results above")
    print(" • Quality: Concise summaries under 1000 words")
    print(" • Citations: Inline numerical references [1], [2], etc.")

    print("\n" + "=" * 80)
    print(" All tests completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
