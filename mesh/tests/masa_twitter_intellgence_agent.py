import asyncio
import subprocess
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.masa_twitter_search_agent import MasaTwitterSearchAgent  # noqa: E402

load_dotenv()

# DEBUG Mode:
# Set DEBUG=True to run the script normally (blocking execution until completion).
# Set DEBUG=False to execute processing in the background and exit early to avoid long wait times.
DEBUG = True


def save_results(output_file, yaml_content):
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)
    if DEBUG:
        print(f"Results saved to {output_file}")
    else:
        print(f"Result will be stored to {output_file}")


async def run_agent():
    agent = MasaTwitterSearchAgent()
    try:
        # Natural language query
        agent_input = {"query": "@heurist_ai", "max_results": 100}
        agent_output = await agent.handle_message(agent_input)

        # Another natural language query
        agent_input_specific = {"query": "$BTC", "max_results": 30}
        agent_output_specific = await agent.handle_message(agent_input_specific)

        # Direct tool call
        agent_input_direct = {
            "tool": "search_twitter",
            "tool_arguments": {"search_term": "Elon musk", "max_results": 30},  # Changed from "query" to "search_term"
            "raw_data_only": True,
        }
        agent_output_direct = await agent.handle_message(agent_input_direct)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_basic": agent_input,
            "output_basic": agent_output,
            "input_specific": agent_input_specific,
            "output_specific": agent_output_specific,
            "input_direct": agent_input_direct,
            "output_direct": agent_output_direct,
        }

        save_results(output_file, yaml_content)
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    if "--background" in sys.argv:
        asyncio.run(run_agent())
    else:
        if DEBUG:
            asyncio.run(run_agent())
        else:
            subprocess.Popen(
                [sys.executable, __file__, "--background"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )
            print("Result will be stored")
            sys.exit(0)
