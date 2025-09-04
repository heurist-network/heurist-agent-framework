import asyncio
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.zora_agent import ZoraAgent  # noqa: E402


async def run_agent():
    agent = ZoraAgent()
    try:
        # Test 1: Natural language query - explore top gainers
        query_top_gainers = {"query": "Show me the top gainers on Zora"}
        output_top_gainers = await agent.handle_message(query_top_gainers)

        # Test 2: Natural language query - most valuable creators
        query_creators = {"query": "Who are the most valuable creators on Zora?"}
        output_creators = await agent.handle_message(query_creators)

        # Test 3: Direct tool call - explore with specific list type
        tool_explore = {"tool": "explore_collections", "tool_arguments": {"list_type": "TOP_VOLUME_24H", "count": 5}}
        output_explore = await agent.handle_message(tool_explore)

        # Test 4: Natural language query - get coin holders
        query_holders = {"query": "Get coin holders for address 0xd769d56f479e9e72a77bb1523e866a33098feec5 on Base"}
        output_holders = await agent.handle_message(query_holders)

        # Test 5: Direct tool call - get coin holders with custom count
        tool_holders = {
            "tool": "get_coin_holders",
            "tool_arguments": {"address": "0xd769d56f479e9e72a77bb1523e866a33098feec5", "chain_id": 8453, "count": 25},
        }
        output_tool_holders = await agent.handle_message(tool_holders)

        # Test 6: Natural language query - get coin info
        query_coin_info = {"query": "What's the coin info for collection 0xd769d56f479e9e72a77bb1523e866a33098feec5?"}
        output_coin_info = await agent.handle_message(query_coin_info)

        # Test 7: Direct tool call - get coin info
        tool_coin_info = {
            "tool": "get_coin_info",
            "tool_arguments": {"collection_address": "0xd769d56f479e9e72a77bb1523e866a33098feec5", "chain_id": 8453},
        }
        output_tool_coin_info = await agent.handle_message(tool_coin_info)

        # Test 8: Natural language query - get coin comments
        query_comments = {"query": "Show me comments for Zora coin 0xd769d56f479e9e72a77bb1523e866a33098feec5"}
        output_comments = await agent.handle_message(query_comments)

        # Test 9: Direct tool call - get coin comments
        tool_comments = {
            "tool": "get_coin_comments",
            "tool_arguments": {"address": "0xd769d56f479e9e72a77bb1523e866a33098feec5", "chain": 8453, "count": 15},
        }
        output_tool_comments = await agent.handle_message(tool_comments)

        # Test 10: Raw data mode - explore featured collections
        raw_featured = {"query": "Show me featured collections on Zora", "raw_data_only": True}
        output_raw_featured = await agent.handle_message(raw_featured)

        # Test 11: Explore last traded collections
        tool_last_traded = {"tool": "explore_collections", "tool_arguments": {"list_type": "LAST_TRADED", "count": 20}}
        output_last_traded = await agent.handle_message(tool_last_traded)

        # Test 12: Natural language - top volume in 24h
        query_volume = {"query": "What are the top volume collections in the last 24 hours?"}
        output_volume = await agent.handle_message(query_volume)

        # Save results to YAML
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "test_top_gainers": {"input": query_top_gainers, "output": output_top_gainers},
            "test_creators": {"input": query_creators, "output": output_creators},
            "test_explore_tool": {"input": tool_explore, "output": output_explore},
            "test_holders_query": {"input": query_holders, "output": output_holders},
            "test_holders_tool": {"input": tool_holders, "output": output_tool_holders},
            "test_coin_info_query": {"input": query_coin_info, "output": output_coin_info},
            "test_coin_info_tool": {"input": tool_coin_info, "output": output_tool_coin_info},
            "test_comments_query": {"input": query_comments, "output": output_comments},
            "test_comments_tool": {"input": tool_comments, "output": output_tool_comments},
            "test_raw_featured": {"input": raw_featured, "output": output_raw_featured},
            "test_last_traded": {"input": tool_last_traded, "output": output_last_traded},
            "test_volume_query": {"input": query_volume, "output": output_volume},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
