import asyncio
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.zkignite_analyst_agent import ZkIgniteAnalystAgent  # noqa: E402


async def run_agent():
    agent = ZkIgniteAnalystAgent()
    try:
        agent_input = {
            "query": "I have some ETH and ZK token and I want to farm on zksync. What are the best opportunities?",
            "task_id": "123",
        }
        agent_output = await agent.handle_message(agent_input)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {"input": agent_input, "output": agent_output}
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
