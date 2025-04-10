import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.moni_twitter_insight_agent import MoniTwitterInsightAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = MoniTwitterInsightAgent()
    try:
        # Test with a query for smart followers history
        agent_input_followers_history = {
            "query": "Show me the follower growth trends for heurist_ai over the last week",
        }
        agent_output_followers_history = await agent.handle_message(agent_input_followers_history)
        print(f"Result of handle_message (followers history): {agent_output_followers_history}")

        # Test with a query for smart followers categories
        agent_input_categories = {
            "query": "What categories of followers does heurist_ai have?",
        }
        agent_output_categories = await agent.handle_message(agent_input_categories)
        print(f"Result of handle_message (follower categories): {agent_output_categories}")

        # Test with a query for smart mentions
        agent_input_mentions = {
            "query": "Show me the recent smart mentions for ethereum",
        }
        agent_output_mentions = await agent.handle_message(agent_input_mentions)
        print(f"Result of handle_message (smart mentions): {agent_output_mentions}")

        # Test direct tool calls

        # Direct tool call for smart followers history
        agent_input_direct_history = {
            "tool": "get_smart_followers_history",
            "tool_arguments": {"username": "heurist_ai", "timeframe": "D7"},
        }
        agent_output_direct_history = await agent.handle_message(agent_input_direct_history)
        print(f"Result of direct tool call (followers history): {agent_output_direct_history}")

        # Direct tool call for smart followers categories
        agent_input_direct_categories = {
            "tool": "get_smart_followers_categories",
            "tool_arguments": {"username": "heurist_ai"},
        }
        agent_output_direct_categories = await agent.handle_message(agent_input_direct_categories)
        print(f"Result of direct tool call (follower categories): {agent_output_direct_categories}")

        # Direct tool call for smart mentions feed
        agent_input_direct_mentions = {
            "tool": "get_smart_mentions_feed",
            "tool_arguments": {"username": "heurist_ai", "limit": 100},
        }
        agent_output_direct_mentions = await agent.handle_message(agent_input_direct_mentions)
        print(f"Result of direct tool call (mentions feed): {agent_output_direct_mentions}")

        # Test with raw_data_only flag
        agent_input_raw_data = {
            "query": "Get smart mentions feed for bitcoin",
            "raw_data_only": True,
        }
        agent_output_raw_data = await agent.handle_message(agent_input_raw_data)
        print(f"Result with raw_data_only=True: {agent_output_raw_data}")

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_followers_history": agent_input_followers_history,
            "output_followers_history": agent_output_followers_history,
            "input_categories": agent_input_categories,
            "output_categories": agent_output_categories,
            "input_mentions": agent_input_mentions,
            "output_mentions": agent_output_mentions,
            "input_direct_history": agent_input_direct_history,
            "output_direct_history": agent_output_direct_history,
            "input_direct_categories": agent_input_direct_categories,
            "output_direct_categories": agent_output_direct_categories,
            "input_direct_mentions": agent_input_direct_mentions,
            "output_direct_mentions": agent_output_direct_mentions,
            "input_raw_data": agent_input_raw_data,
            "output_raw_data": agent_output_raw_data,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
