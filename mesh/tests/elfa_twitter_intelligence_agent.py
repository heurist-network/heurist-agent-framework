import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.elfa_twitter_intelligence_agent import ElfaTwitterIntelligenceAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = ElfaTwitterIntelligenceAgent()
    try:
        # Test with a query for searching mentions (token/topic)
        agent_input_mentions = {"query": "Search for mentions of Heurist, HEU, and heurist_ai in the last 30 days"}
        agent_output_mentions = await agent.handle_message(agent_input_mentions)
        print(f"Result of handle_message (search mentions): {agent_output_mentions}")

        # Test with a query for account analysis (using the new search_account tool)
        agent_input_account = {"query": "Analyze the Twitter account @heurist_ai"}
        agent_output_account = await agent.handle_message(agent_input_account)
        print(f"Result of handle_message (account analysis): {agent_output_account}")

        # Test direct trending tokens tool (no LLM routing)
        agent_input_trending = {
            "tool": "get_trending_tokens",
            "tool_arguments": {"time_window": "24h"},
            "query": "Get trending tokens for reference",
        }
        agent_output_trending = await agent.handle_message(agent_input_trending)
        print(f"Result of handle_message (trending tokens direct call): {agent_output_trending}")

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_mentions": agent_input_mentions,
            "output_mentions": agent_output_mentions,
            "input_account": agent_input_account,
            "output_account": agent_output_account,
            "input_trending": agent_input_trending,
            "output_trending": agent_output_trending,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
