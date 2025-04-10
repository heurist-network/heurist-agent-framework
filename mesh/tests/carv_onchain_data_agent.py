import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Adjust the path to access the parent directory
sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.carv_onchain_data_agent import CarvOnchainDataAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = CarvOnchainDataAgent()
    try:
        # Test with a natural language query
        ethereum_query = {"query": "Identify the biggest transaction of ETH in the past 30 days"}
        ethereum_result = await agent.handle_message(ethereum_query)
        print(f"Ethereum Query Result: {ethereum_result}")

        # Test with a direct tool call
        direct_input = {
            "tool": "query_onchain_data",
            "tool_arguments": {
                "blockchain": "bitcoin",
                "query": "How many Bitcoins have been mined since the beginning of 2025?",
            },
        }
        direct_result = await agent.handle_message(direct_input)
        print(f"Direct Tool Call Result: {direct_result}")

        # Test with raw data only
        raw_input = {
            "query": "What are the top 5 most popular smart contracts on Ethereum in the past 30 days?",
            "raw_data_only": True,
        }
        raw_result = await agent.handle_message(raw_input)
        print(f"Raw Data Result: {raw_result}")

        # Save the test results to a YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "ethereum_example": {"input": ethereum_query, "output": ethereum_result},
            "direct_example": {"input": direct_input, "output": direct_result},
            "raw_example": {"input": raw_input, "output": raw_result},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
