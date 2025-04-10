import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.dexscreener_token_info_agent import DexScreenerTokenInfoAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = DexScreenerTokenInfoAgent()
    try:
        # Example for natural language query with analysis
        agent_input_query = {
            "query": "Show me information about ETH on Uniswap",
            "raw_data_only": False,
        }
        agent_output_query = await agent.handle_message(agent_input_query)

        # Example for natural language query with raw data only
        agent_input_query_raw = {
            "query": "Tell me about ETH on Uniswap",
            "raw_data_only": True,
        }
        agent_output_query_raw = await agent.handle_message(agent_input_query_raw)

        # Test search_pairs tool - Direct tool call (no LLM analysis)
        agent_input_search = {
            "tool": "search_pairs",
            "tool_arguments": {"search_term": "ETH"},
        }
        agent_output_search = await agent.handle_message(agent_input_search)
        print(f"Result of search_pairs: {agent_output_search}")

        # Test get_specific_pair_info tool - Direct tool call (no LLM analysis)
        agent_input_pair_info = {
            "tool": "get_specific_pair_info",
            "tool_arguments": {"chain": "solana", "pair_address": "7qsdv1yr4yra9fjazccrwhbjpykvpcbi3158u1qcjuxp"},
        }
        agent_output_pair_info = await agent.handle_message(agent_input_pair_info)
        print(f"Result of get_specific_pair_info: {agent_output_pair_info}")

        # Test get_token_pairs tool - Direct tool call (no LLM analysis)
        agent_input_pairs = {
            "tool": "get_token_pairs",
            "tool_arguments": {"chain": "solana", "token_address": "8TE8oxirpnriy9CKCd6dyjtff2vvP3n6hrSMqX58pump"},
        }
        agent_output_pairs = await agent.handle_message(agent_input_pairs)
        print(f"Result of get_token_pairs: {agent_output_pairs}")

        # Save the test inputs and outputs to a YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_query_with_analysis": {"input": agent_input_query, "output": agent_output_query},
            "natural_language_query_raw_data": {"input": agent_input_query_raw, "output": agent_output_query_raw},
            "search_pairs_test": {"input": agent_input_search, "output": agent_output_search},
            "specific_pair_info_test": {"input": agent_input_pair_info, "output": agent_output_pair_info},
            "token_pairs_test": {"input": agent_input_pairs, "output": agent_output_pairs},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
