import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.deep_research_agent import DeepResearchAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = DeepResearchAgent()
    try:
        agent_input = {
            "query": "What are the latest developments in zero knowledge proofs?",
            "depth": 2,
            "breadth": 3,
            "concurrency": 9,
        }

        try:
            agent_output = await agent.handle_message(agent_input)
        except Exception as e:
            print(f"Error during agent execution: {str(e)}")
            return

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input": agent_input,
            "output": {
                "response": agent_output["response"],
                "data": agent_output["data"],
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        try:
            await agent.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
