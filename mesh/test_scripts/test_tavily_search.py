#!/usr/bin/env python3
"""
Test script for TavilySearchAgent.
Runs both tavily_web_search and tavily_extract_content tools and prints results.
"""

import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.tavily_search_agent import TavilySearchAgent


async def main():
    agent = TavilySearchAgent()

    print("=== Test 1: tavily_web_search ===")
    search_result = await agent._handle_tool_logic(
        "tavily_web_search",
        {"query": "What are the latest breakthroughs in quantum computing?", "max_results": 3, "search_depth": "basic", "topic": "general"},
    )
    print(json.dumps(search_result, indent=2, default=str))

    urls = []
    if search_result.get("status") == "success":
        urls = [r["url"] for r in search_result["data"]["results"][:1]]

    if urls:
        print("\n=== Test 2: tavily_extract_content ===")
        extract_result = await agent._handle_tool_logic(
            "tavily_extract_content",
            {"urls": urls},
        )
        print(json.dumps(extract_result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
