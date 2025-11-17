#!/usr/bin/env python3
"""
Test script for WanVideoGenAgent - Two-Step Workflow
Tests the async video generation with task_id creation and status checking
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.wan_video_gen_agent import WanVideoGenAgent


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_result(label: str, result: dict):
    """Pretty print result with task_id extraction."""
    print(f"\n{label}")
    print("-" * 70)

    # Print the full response
    print(f"Response: {result.get('response', 'N/A')}")

    # Extract and highlight important data
    data = result.get("data", {})
    if isinstance(data, dict):
        nested_data = data.get("data", {})
        if isinstance(nested_data, dict):
            task_id = nested_data.get("task_id")
            task_status = nested_data.get("task_status")
            message = nested_data.get("message")
            video_url = nested_data.get("video_url")

            if task_id:
                print(f"\n✅ Task ID: {task_id}")
            if task_status:
                print(f"📊 Status: {task_status}")
            if message:
                print(f"💬 Message: {message}")
            if video_url:
                print(f"🎬 Video URL: {video_url}")

        # Show error if present
        if data.get("status") == "error":
            print(f"\n❌ Error: {data.get('error')}")

    print("\nFull Response Data:")
    print(json.dumps(result, indent=2))


async def test_wan_video_agent():
    """Test WanVideoGenAgent with two-step workflow"""

    print_section("WanVideoGenAgent - Two-Step Workflow Test")

    task_ids = {}

    async with WanVideoGenAgent() as agent:
        # ========== PHASE 1: CREATE VIDEO TASKS ==========
        print_section("PHASE 1: Creating Video Generation Tasks")

        # Test 1: Text-to-Video
        print_result(
            "🎯 Test 1: Text-to-Video - Cat running on grass",
            result1 := await agent.call_agent(
                {
                    "tool": "text_to_video",
                    "tool_arguments": {"prompt": "A playful cat running on grass in a sunny garden"},
                }
            ),
        )
        if result1.get("data", {}).get("data", {}).get("task_id"):
            task_ids["cat_video"] = result1["data"]["data"]["task_id"]

        # Test 2: Image-to-Video (wan2.2-i2v-plus)
        print_result(
            "🎯 Test 2: Image-to-Video - Ocean waves (plus model)",
            result2 := await agent.call_agent(
                {
                    "tool": "image_to_video",
                    "tool_arguments": {
                        "prompt": "Ocean waves gently crashing on the shore",
                        "image_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
                        "model": "wan2.2-i2v-plus",
                    },
                }
            ),
        )
        if result2.get("data", {}).get("data", {}).get("task_id"):
            task_ids["ocean_video"] = result2["data"]["data"]["task_id"]

        # Test 3: Image-to-Video (wan2.2-i2v-flash)
        print_result(
            "🎯 Test 3: Image-to-Video - Chinese prompt (flash model)",
            result3 := await agent.call_agent(
                {
                    "tool": "image_to_video",
                    "tool_arguments": {
                        "prompt": "一只猫在草地上奔跑",
                        "image_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
                        "model": "wan2.2-i2v-flash",
                        "prompt_extend": False,
                    },
                }
            ),
        )
        if result3.get("data", {}).get("data", {}).get("task_id"):
            task_ids["cat_chinese"] = result3["data"]["data"]["task_id"]

        # Test 4: Natural Language Query
        print_result(
            "🎯 Test 4: Natural Language - Sunset over mountains",
            result4 := await agent.call_agent({"query": "Generate a video of a sunset over mountains"}),
        )
        if result4.get("data", {}).get("data", {}).get("task_id"):
            task_ids["sunset_video"] = result4["data"]["data"]["task_id"]

        # Summary of created tasks
        print_section("Task Creation Summary")
        print(f"\n✅ Created {len(task_ids)} video generation task(s):")
        for name, task_id in task_ids.items():
            print(f"  • {name}: {task_id}")

        # ========== PHASE 2: WAIT AND CHECK STATUS ==========
        wait_time = 120  # 2 minutes
        print_section(f"PHASE 2: Waiting {wait_time} seconds before checking status...")

        for i in range(wait_time, 0, -10):
            print(f"⏳ {i} seconds remaining...", end="\r")
            await asyncio.sleep(10)
        print("\n")

        # Check status of all tasks
        print_section("PHASE 3: Checking Video Generation Status")

        for name, task_id in task_ids.items():
            print_result(
                f"📊 Status Check: {name} ({task_id})",
                await agent.call_agent({"tool": "get_video_status", "tool_arguments": {"task_id": task_id}}),
            )

        # Final summary
        print_section("Test Completed Successfully!")
        print(f"\n✅ All {len(task_ids)} video generation tasks were created and checked")
        print("\n💡 Tip: If videos are still processing, wait a bit longer and check again")
        print("         by calling get_video_status with the task_id\n")


if __name__ == "__main__":
    asyncio.run(test_wan_video_agent())
