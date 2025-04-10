import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.space_and_time_agent import SpaceTimeAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = SpaceTimeAgent()
    try:
        # Example 1: Natural language query to generate and execute SQL
        agent_input_nl = {
            "query": "Get the number of blocks created on Ethereum per day over the last month",
            "raw_data_only": False,
        }
        agent_output_nl = await agent.handle_message(agent_input_nl)

        # Example 2: Direct call to generate and execute SQL from NL
        agent_input_n2 = {
            "tool": "generate_and_execute_sql",
            "tool_arguments": {"nl_query": "What's the average transactions in past week for Ethereum"},
            "raw_data_only": True,
        }
        agent_output_n2 = await agent.handle_message(agent_input_n2)

        # Example 3: Natural language query to generate and execute SQL
        agent_input_n3 = {
            "query": "Tell me top 10 GPUs from HEURIST",
            "raw_data_only": False,
        }
        agent_output_n3 = await agent.handle_message(agent_input_n3)

        # Example 4: Natural language query to generate and execute SQL
        agent_input_n4 = {
            "query": "How many transactions occurred on Ethereum yesterday?",
            "raw_data_only": False,
        }
        agent_output_n4 = await agent.handle_message(agent_input_n4)

        # Example 5: Natural language query to generate and execute SQL
        agent_input_n5 = {
            "query": "What's the largest transaction value on Ethereum in the past 24 hours?",
            "raw_data_only": False,
        }
        agent_output_n5 = await agent.handle_message(agent_input_n5)

        # Save results to YAML file for inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "query 1": {"input": agent_input_nl, "output": agent_output_nl},
            "query 2": {"input": agent_input_n2, "output": agent_output_n2},
            "query 3": {"input": agent_input_n3, "output": agent_output_n3},
            "query 4": {"input": agent_input_n4, "output": agent_output_n4},
            "query 5": {"input": agent_input_n5, "output": agent_output_n5},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
