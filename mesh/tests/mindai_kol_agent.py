import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.mindai_kol_agent import MindAiKolAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = MindAiKolAgent()
    try:
        # Test with a query for best initial calls
        agent_input_best_calls = {
            "query": "Find the best initial calls for HEU token",
        }
        agent_output_best_calls = await agent.handle_message(agent_input_best_calls)

        # Test with a query for KOL statistics
        agent_input_kol_stats = {
            "query": "What are the statistics for KOL @agentcookiefun?",
        }
        agent_output_kol_stats = await agent.handle_message(agent_input_kol_stats)

        # Test with a query for token statistics
        agent_input_token_stats = {
            "query": "Get token statistics for ETH in the last month",
        }
        agent_output_token_stats = await agent.handle_message(agent_input_token_stats)

        # Test with a query for top gainers
        agent_input_top_gainers = {
            "query": "Show me the top gainers in the past week",
        }
        agent_output_top_gainers = await agent.handle_message(agent_input_top_gainers)

        # Test direct tool calls

        # Direct tool call for best initial calls - using working parameters from cURL example
        agent_input_direct_best_calls = {
            "tool": "get_best_initial_calls",
            "tool_arguments": {
                "period": 168,
                "token_symbol": "HEU",
                # Note: tokenCategory is not included as it's optional
            },
            "raw_data_only": True,
        }
        agent_output_direct_best_calls = await agent.handle_message(agent_input_direct_best_calls)

        # Direct tool call for KOL statistics
        agent_input_direct_kol_stats = {
            "tool": "get_kol_statistics",
            "tool_arguments": {"period": 720, "kol_name": "@agentcookiefun"},
            "raw_data_only": True,
        }
        agent_output_direct_kol_stats = await agent.handle_message(agent_input_direct_kol_stats)

        # Direct tool call for token statistics
        agent_input_direct_token_stats = {
            "tool": "get_token_statistics",
            "tool_arguments": {"period": 720, "token_symbol": "HEU"},
            "raw_data_only": True,
        }
        agent_output_direct_token_stats = await agent.handle_message(agent_input_direct_token_stats)

        # Direct tool call for top gainers
        agent_input_direct_top_gainers = {
            "tool": "get_top_gainers",
            "tool_arguments": {"period": 720, "token_category": "top100", "tokens_amount": 5, "kols_amount": 3},
            "raw_data_only": True,
        }
        agent_output_direct_top_gainers = await agent.handle_message(agent_input_direct_top_gainers)

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_best_calls": agent_input_best_calls,
            "output_best_calls": agent_output_best_calls,
            "input_kol_stats": agent_input_kol_stats,
            "output_kol_stats": agent_output_kol_stats,
            "input_token_stats": agent_input_token_stats,
            "output_token_stats": agent_output_token_stats,
            "input_top_gainers": agent_input_top_gainers,
            "output_top_gainers": agent_output_top_gainers,
            "input_direct_best_calls": agent_input_direct_best_calls,
            "output_direct_best_calls": agent_output_direct_best_calls,
            "input_direct_kol_stats": agent_input_direct_kol_stats,
            "output_direct_kol_stats": agent_output_direct_kol_stats,
            "input_direct_token_stats": agent_input_direct_token_stats,
            "output_direct_token_stats": agent_output_direct_token_stats,
            "input_direct_top_gainers": agent_input_direct_top_gainers,
            "output_direct_top_gainers": agent_output_direct_top_gainers,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
