#!/usr/bin/env python3
"""
Test script for WanVideoGenAgent
Tests all 5 video generation tools (480p 5s) with automatic retry logic
"""

import asyncio
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from mesh.agents.wan_video_gen_agent import WanVideoGenAgent


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(label: str, result: dict):
    """Pretty print result with task_id extraction."""
    print(f"\n{label}")
    print("-" * 80)

    data = result.get("data", {})
    if isinstance(data, dict):
        nested_data = data.get("data", {})
        if isinstance(nested_data, dict):
            task_id = nested_data.get("task_id")
            task_status = nested_data.get("task_status")
            message = nested_data.get("message")
            video_url = nested_data.get("video_url")
            r2_preview_url = nested_data.get("r2_preview_url")

            if task_id:
                print(f"✅ Task ID: {task_id}")
            if task_status:
                print(f"📊 Status: {task_status}")
            if message:
                print(f"💬 Message: {message}")
            if video_url:
                print(f"🎬 Original URL: {video_url}")
            if r2_preview_url:
                print(f"🌐 R2 URL: {r2_preview_url}")

        if data.get("status") == "error":
            print(f"❌ Error: {data.get('error')}")


async def check_status_with_retry(agent, task_id: str, max_retries: int = 3) -> dict:
    """
    Check video status with automatic retry logic.

    Args:
        agent: WanVideoGenAgent instance
        task_id: Task ID to check
        max_retries: Maximum number of retries (default: 3)

    Returns:
        Final status result
    """
    retry_intervals = [30, 45, 60]

    for retry in range(max_retries):
        result = await agent.call_agent({"tool": "get_video_status", "tool_arguments": {"task_id": task_id}})

        data = result.get("data", {}).get("data", {})
        status = data.get("task_status")

        if status == "SUCCEEDED":
            print("✅ Video ready!")
            return result
        elif status == "FAILED":
            print("❌ Video generation failed")
            return result
        elif status in ["PENDING", "RUNNING"]:
            if retry < max_retries - 1:
                wait_time = retry_intervals[retry]
                print(f"⏳ Status: {status}. Waiting {wait_time}s before retry {retry + 2}/{max_retries}...")
                await asyncio.sleep(wait_time)
            else:
                print(f"⏱️  Max retries reached. Status: {status}")
                return result
        else:
            print(f"⚠️  Unknown status: {status}")
            return result

    return result


async def test_wan_video_agent():
    """Test all 5 WanVideoGenAgent tools (480p 5s)"""

    overall_start = time.time()
    print_section("WanVideoGenAgent - Comprehensive Test (480p 5s)")
    test_image_url = "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
    tests = [
        {
            "name": "text_to_video_480p_5s",
            "tool": "text_to_video_480p_5s",
            "args": {
                "prompt": "A golden retriever puppy playing with a red ball in a sunlit park, wagging its tail happily"
            },
        },
        {
            "name": "text_to_video_with_audio_480p_5s",
            "tool": "text_to_video_with_audio_480p_5s",
            "args": {
                "prompt": "A bustling Tokyo street at night with neon signs, people walking, and cars passing by with rain reflections"
            },
        },
        {
            "name": "image_to_video_plus_480p_5s",
            "tool": "image_to_video_plus_480p_5s",
            "args": {
                "prompt": "Gentle camera zoom and subtle lighting changes, flowers swaying softly in a breeze",
                "image_url": test_image_url,
            },
        },
        {
            "name": "image_to_video_flash_480p_5s",
            "tool": "image_to_video_flash_480p_5s",
            "args": {
                "prompt": "Dynamic parallax effect with leaves falling and light rays moving across the scene",
                "image_url": test_image_url,
            },
        },
        {
            "name": "image_to_video_with_audio_480p_5s",
            "tool": "image_to_video_with_audio_480p_5s",
            "args": {
                "prompt": "The scene comes alive with birds chirping, wind rustling through leaves, and subtle movements",
                "image_url": test_image_url,
            },
        },
    ]

    task_ids = {}
    task_start_times = {}

    async with WanVideoGenAgent() as agent:
        # ========== PHASE 1: CREATE ALL VIDEO TASKS ==========
        print_section("PHASE 1: Creating Video Generation Tasks")

        for i, test in enumerate(tests, 1):
            print(f"\n🎯 Test {i}/{len(tests)}: {test['name']}")
            start_time = time.time()
            result = await agent.call_agent({"tool": test["tool"], "tool_arguments": test["args"]})

            print_result(f"  Tool: {test['tool']}", result)

            task_id = result.get("data", {}).get("data", {}).get("task_id")
            if task_id:
                task_ids[test["name"]] = task_id
                task_start_times[test["name"]] = start_time

        # Summary of created tasks
        print_section("Task Creation Summary")
        print(f"\n✅ Successfully created {len(task_ids)}/{len(tests)} video generation tasks:")
        for name, task_id in task_ids.items():
            print(f"  • {name}: {task_id}")

        if len(task_ids) == 0:
            print("\n❌ No tasks were created. Exiting test.")
            return

        # ========== PHASE 2: WAIT 120 SECONDS ==========
        wait_time = 120
        print_section(f"PHASE 2: Waiting {wait_time} seconds before checking status...")
        print("(Video generation typically takes 3-15 minutes)")

        for i in range(wait_time, 0, -10):
            print(f"⏳ {i} seconds remaining...", end="\r", flush=True)
            await asyncio.sleep(10)
        print("\n")

        print_section("PHASE 3: Checking Video Generation Status (with 3 retries)")

        results = {}
        task_end_times = {}
        for name, task_id in task_ids.items():
            print(f"\n{'=' * 80}")
            print(f"📊 Checking: {name}")
            print(f"   Task ID: {task_id}")
            print(f"{'=' * 80}")

            result = await check_status_with_retry(agent, task_id, max_retries=3)
            end_time = time.time()
            results[name] = result
            task_end_times[name] = end_time

            if name in task_start_times:
                elapsed = end_time - task_start_times[name]
                print(f"⏱️  Time taken: {elapsed:.1f} seconds ({elapsed / 60:.1f} minutes)")

            print_result(f"Final Status: {name}", result)

        print_section("Test Completed!")

        succeeded = sum(
            1 for r in results.values() if r.get("data", {}).get("data", {}).get("task_status") == "SUCCEEDED"
        )
        failed = sum(1 for r in results.values() if r.get("data", {}).get("data", {}).get("task_status") == "FAILED")
        pending = sum(
            1
            for r in results.values()
            if r.get("data", {}).get("data", {}).get("task_status") in ["PENDING", "RUNNING"]
        )

        print("\n📊 Results Summary:")
        print(f"  ✅ Succeeded: {succeeded}/{len(task_ids)}")
        print(f"  ❌ Failed: {failed}/{len(task_ids)}")
        print(f"  ⏳ Still Processing: {pending}/{len(task_ids)}")

        if succeeded > 0:
            print("\n🎬 Successful Videos:")
            for name, result in results.items():
                data = result.get("data", {}).get("data", {})
                if data.get("task_status") == "SUCCEEDED":
                    r2_url = data.get("r2_preview_url") or data.get("video_url")
                    elapsed = task_end_times[name] - task_start_times[name]
                    print(f"  • {name}: {r2_url}")
                    print(f"    ⏱️  {elapsed:.1f}s ({elapsed / 60:.1f} min)")

        if pending > 0:
            print(f"\n💡 Tip: {pending} video(s) still processing. You can check them later using:")
            for name, result in results.items():
                data = result.get("data", {}).get("data", {})
                if data.get("task_status") in ["PENDING", "RUNNING"]:
                    print(f"  • {name}: Task ID = {task_ids[name]}")

        overall_end = time.time()
        total_elapsed = overall_end - overall_start

        print("\n" + "=" * 80)
        print("⏱️  TIMING SUMMARY")
        print("=" * 80)
        print(f"\n📊 Overall Test Duration: {total_elapsed:.1f} seconds ({total_elapsed / 60:.1f} minutes)")

        if succeeded > 0:
            print("\n⏱️  Individual Job Times:")
            for name, result in results.items():
                data = result.get("data", {}).get("data", {})
                if data.get("task_status") == "SUCCEEDED" and name in task_start_times and name in task_end_times:
                    elapsed = task_end_times[name] - task_start_times[name]
                    print(f"  • {name}: {elapsed:.1f}s ({elapsed / 60:.1f} min)")

            successful_times = [
                task_end_times[name] - task_start_times[name]
                for name in results.keys()
                if results[name].get("data", {}).get("data", {}).get("task_status") == "SUCCEEDED"
                and name in task_start_times
                and name in task_end_times
            ]
            if successful_times:
                avg_time = sum(successful_times) / len(successful_times)
                print(f"\n📈 Average Time per Successful Job: {avg_time:.1f}s ({avg_time / 60:.1f} min)")

        print()


if __name__ == "__main__":
    asyncio.run(test_wan_video_agent())
