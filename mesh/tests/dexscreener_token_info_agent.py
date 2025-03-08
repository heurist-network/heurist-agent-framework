import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.dexscreener_token_info_agent import DexScreenerTokenInfoAgent

load_dotenv()


async def run_agent():
    agent = DexScreenerTokenInfoAgent()
    try:
        # Test search_pairs tool
        agent_input = {
            "tool": "search_pairs",
            "tool_arguments": {"search_term": "ETH"},  # Changed from "query" to "search_term"
            "raw_data_only": False,  # Set to True if you only want raw data without LLM analysis
        }
        agent_output = await agent.handle_message(agent_input)
        print(f"Result of search_pairs: {agent_output}")

        # Test get_specific_pair_info tool
        agent_input_pair_info = {
            "tool": "get_specific_pair_info",
            "tool_arguments": {"chain": "solana", "pair_address": "7qsdv1yr4yra9fjazccrwhbjpykvpcbi3158u1qcjuxp"},
        }
        agent_output_pair_info = await agent.handle_message(agent_input_pair_info)
        print(f"Result of get_specific_pair_info: {agent_output_pair_info}")

        # Test get_token_pairs tool
        agent_input_pairs = {
            "tool": "get_token_pairs",
            "tool_arguments": {"chain": "solana", "token_address": "8TE8oxirpnriy9CKCd6dyjtff2vvP3n6hrSMqX58pump"},
        }
        agent_output_pairs = await agent.handle_message(agent_input_pairs)
        print(f"Result of get_token_pairs: {agent_output_pairs}")

        # Test get_token_profiles tool
        agent_input_profiles = {
            "tool": "get_token_profiles",
            "tool_arguments": {},  # No arguments needed for this tool
        }
        agent_output_profiles = await agent.handle_message(agent_input_profiles)
        print(f"Result of get_token_profiles: {agent_output_profiles}")

        # Save the test inputs and outputs to a YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "search_pairs_test": {"input": agent_input, "output": agent_output},
            "specific_pair_info_test": {"input": agent_input_pair_info, "output": agent_output_pair_info},
            "token_pairs_test": {"input": agent_input_pairs, "output": agent_output_pairs},
            "token_profiles_test": {"input": agent_input_profiles, "output": agent_output_profiles},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())