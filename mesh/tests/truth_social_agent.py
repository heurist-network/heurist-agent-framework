import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.truth_social_agent import TruthSocialAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = TruthSocialAgent()
    try:
        # Test with a natural language query
        agent_input_query = {
            "query": "What has Donald Trump posted recently on Truth Social?",
        }
        agent_output_query = await agent.handle_message(agent_input_query)

        # Test direct tool call
        agent_input_direct = {
            "tool": "get_trump_posts",
            "tool_arguments": {"max_posts": 20},
            "raw_data_only": True,
        }
        agent_output_direct = await agent.handle_message(agent_input_direct)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_query": agent_input_query,
            "output_query": agent_output_query,
            "input_direct": agent_input_direct,
            "output_direct": agent_output_direct,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
