import sys
from pathlib import Path
import yaml
import os
from dotenv import load_dotenv
import asyncio

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.dexscreener_token_info_agent import DexScreenerTokenInfoAgent

load_dotenv()

async def run_agent():
    agent = DexScreenerTokenInfoAgent()
    try:
        # Test with a query that mentions a token name, symbol, or address
        agent_input = {
            'query': 'Search for trading pairs for token name ETH'
        }
        agent_output = await agent.handle_message(agent_input)
        print(f"Result of handle_message (search trading pairs by query): {agent_output}")

        # Test with a query for specific pair info
        agent_input_pair_info = {
            'query': 'Get specific pair info for chain: solana, pair address: 7qsdv1yr4yra9fjazccrwhbjpykvpcbi3158u1qcjuxp'
        }
        agent_output_pair_info = await agent.handle_message(agent_input_pair_info)
        print(f"Result of handle_message (specific pair info by chain and pair address): {agent_output_pair_info}")

        # Test with a query for token pairs
        agent_input_pairs = {
            'query': 'Get the token pairs for chain: solana, token address: 8TE8oxirpnriy9CKCd6dyjtff2vvP3n6hrSMqX58pump'
        }
        agent_output_pairs = await agent.handle_message(agent_input_pairs)
        print(f"Result of handle_message (token pairs by chain and token address): {agent_output_pairs}")

        # Test with a query for token profiles
        agent_input_profiles = {
            'query': 'Get the latest token profiles'
        }
        agent_output_profiles = await agent.handle_message(agent_input_profiles)
        print(f"Result of handle_message (the latest token profiles): {agent_output_profiles}")

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            'input_by_token_info': agent_input,
            'output_by_token_info': agent_output,
            'input_specific_pair_info': agent_input_pair_info,
            'output_specific_pair_info': agent_output_pair_info,
            'input_token_pairs': agent_input_pairs,
            'output_token_pairs': agent_output_pairs,
            'input_latest_token_profiles': agent_input_profiles,
            'output_latest_token_profiles': agent_output_profiles,
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(run_agent())