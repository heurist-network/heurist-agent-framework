#!/usr/bin/env python3
"""
Test script for CaesarResearchAgent with two-tool workflow.
Submit a research query, then poll for results with retry logic.
"""

import asyncio
import json
import random
import sys
import time
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.caesar_research_agent import CaesarResearchAgent

# ========== MODIFY THESE VARIABLES TO TEST DIFFERENT SCENARIOS ==========
RESEARCH_QUERY = "What is Heurist Mesh and how does it work?"
BASE_WAIT_SECONDS = 150  # Base wait time before first check
RANDOM_WAIT_RANGE = (0, 30)  # Random seconds to add to base wait (min, max)
RETRY_WAIT_SECONDS = 30  # Wait time between retries if not completed
MAX_RETRIES = 3  # Maximum number of retries
# =====================================================================


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_status(status: str, message: str):
    """Print a status message with emoji."""
    emoji_map = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "waiting": "⏳",
    }
    emoji = emoji_map.get(status, "•")
    print(f"{emoji} {message}")


async def submit_research(agent: CaesarResearchAgent, query: str) -> dict:
    """Submit a research query and return the result."""
    print_section("Submitting Research Query")
    print(f"Query: {query}")

    try:
        result = await agent._handle_tool_logic("caesar_research", {"query": query})

        if result.get("status") == "error":
            print_status("error", f"Submission failed: {result.get('error')}")
            return None

        data = result.get("data", {})
        research_id = data.get("research_id")
        initial_status = data.get("initial_status")
        message = data.get("message")

        print_status("success", "Research submitted successfully!")
        print(f"\nResearch ID: {research_id}")
        print(f"Initial Status: {initial_status}")
        print(f"Message: {message}")

        return {"research_id": research_id, "query": query}

    except Exception as e:
        print_status("error", f"Exception during submission: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


async def fetch_research_result(agent: CaesarResearchAgent, research_id: str) -> dict:
    """Fetch research results by ID."""
    try:
        result = await agent._handle_tool_logic("get_research_result", {"research_id": research_id})

        if result.get("status") == "error":
            print_status("error", f"Fetch failed: {result.get('error')}")
            return None

        return result.get("data", {})

    except Exception as e:
        print_status("error", f"Exception during fetch: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


async def poll_for_results(agent: CaesarResearchAgent, research_id: str):
    """Poll for research results with retry logic."""
    print_section("Polling for Results")

    # Calculate initial wait time
    random_wait = random.randint(RANDOM_WAIT_RANGE[0], RANDOM_WAIT_RANGE[1])
    total_wait = BASE_WAIT_SECONDS + random_wait

    print_status("waiting", f"Waiting {total_wait} seconds before first check...")
    print(f"  (Base: {BASE_WAIT_SECONDS}s + Random: {random_wait}s)")
    await asyncio.sleep(total_wait)

    # Attempt to fetch results with retries
    for attempt in range(1, MAX_RETRIES + 1):
        print_section(f"Attempt {attempt}/{MAX_RETRIES}")

        data = await fetch_research_result(agent, research_id)

        if data is None:
            print_status("error", "Failed to fetch results")
            if attempt < MAX_RETRIES:
                print_status("waiting", f"Retrying in {RETRY_WAIT_SECONDS} seconds...")
                await asyncio.sleep(RETRY_WAIT_SECONDS)
            continue

        research_status = data.get("research_status")
        print(f"Status: {research_status}")

        if research_status == "completed":
            print_status("success", "Research completed!")
            print_completed_results(data)
            return True

        elif research_status in ["queued", "researching"]:
            message = data.get("message", "Research still in progress")
            print_status("info", message)

            if attempt < MAX_RETRIES:
                print_status("waiting", f"Waiting {RETRY_WAIT_SECONDS} seconds before retry...")
                await asyncio.sleep(RETRY_WAIT_SECONDS)
            else:
                print_status("warning", "Max retries reached. Research may still be processing.")
                print(f"\n💡 You can check the result later using research_id: {research_id}")
                return False

        elif research_status == "failed":
            print_status("error", "Research failed")
            return False

        else:
            print_status("warning", f"Unknown status: {research_status}")
            return False

    return False


def print_completed_results(data: dict):
    """Print the completed research results."""
    print("\n--- Research Details ---")
    print(f"Query: {data.get('query')}")
    print(f"Created At: {data.get('created_at')}")
    print(f"Completed At: {data.get('completed_at')}")

    content = data.get("content", "")
    print(f"\n--- Research Content ---")
    print(f"Content Length: {len(content)} characters")

    if content:
        # Print first 1000 characters of content
        preview_length = min(1000, len(content))
        print(f"\nContent Preview (first {preview_length} chars):")
        print("-" * 60)
        print(content[:preview_length])
        if len(content) > preview_length:
            print(f"\n... ({len(content) - preview_length} more characters)")
        print("-" * 60)
    else:
        print("No content available")


async def main():
    """Main test runner."""
    start_time = time.time()

    print("\n🚀 CaesarResearchAgent Test Script")
    print(f"Query: {RESEARCH_QUERY}")
    print(f"Base Wait: {BASE_WAIT_SECONDS}s + Random: {RANDOM_WAIT_RANGE[0]}-{RANDOM_WAIT_RANGE[1]}s")
    print(f"Retry Logic: {MAX_RETRIES} attempts with {RETRY_WAIT_SECONDS}s intervals")

    agent = CaesarResearchAgent()

    # Step 1: Submit research
    submission = await submit_research(agent, RESEARCH_QUERY)
    if not submission:
        print("\n❌ Test failed: Could not submit research")
        return

    research_id = submission["research_id"]

    # Step 2: Poll for results
    success = await poll_for_results(agent, research_id)

    # Summary
    elapsed_time = time.time() - start_time
    print_section("Test Summary")
    print(f"Total elapsed time: {elapsed_time:.1f} seconds")
    print(f"Research ID: {research_id}")

    if success:
        print_status("success", "Test completed successfully!")
    else:
        print_status("warning", "Test completed but research may still be processing")
        print(f"\n💡 You can manually check the result using:")
        print(f"   Research ID: {research_id}")

    print("\n🏁 Test finished\n")


if __name__ == "__main__":
    asyncio.run(main())
