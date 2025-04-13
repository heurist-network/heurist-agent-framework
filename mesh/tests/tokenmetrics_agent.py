import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.tokenmetrics_agent import TokenMetricsAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = TokenMetricsAgent()
    try:
        # Test with a query for market sentiments
        agent_input_sentiments = {
            "query": "What is the current market sentiment for top cryptocurrencies?",
            "raw_data_only": False,
        }
        agent_output_sentiments = await agent.handle_message(agent_input_sentiments)

        # Test with a query that should auto-detect sentiment with limit
        agent_input_sentiment_with_limit = {
            "query": "Can you show me the top 5 cryptocurrencies by market feeling?",
            "raw_data_only": False,
        }
        agent_output_sentiment_with_limit = await agent.handle_message(agent_input_sentiment_with_limit)

        # Test with a query for resistance and support levels
        agent_input_resistance_support = {
            "query": "What are the key resistance and support levels for Bitcoin and Ethereum?",
            "raw_data_only": False,
        }
        agent_output_resistance_support = await agent.handle_message(agent_input_resistance_support)

        # Test with a query for a specific non-BTC/ETH token (by symbol)
        agent_input_custom_token_symbol = {
            "query": "What are the resistance and support levels for Solana (SOL)?",
            "raw_data_only": False,
        }
        agent_output_custom_token_symbol = await agent.handle_message(agent_input_custom_token_symbol)

        # Test with a query for a specific non-BTC/ETH token (by name)
        agent_input_custom_token_name = {
            "query": "What's the current sentiment for Heurist token?",
            "raw_data_only": False,
        }
        agent_output_custom_token_name = await agent.handle_message(agent_input_custom_token_name)

        # Test direct tool calls
        # Direct tool call for token info
        agent_input_direct_token_info = {
            "tool": "get_token_info",
            "tool_arguments": {"token_symbol": "HEU", "limit": 5},
            "raw_data_only": True,
        }
        agent_output_direct_token_info = await agent.handle_message(agent_input_direct_token_info)

        # Direct tool call for market sentiments
        agent_input_direct_sentiments = {
            "tool": "get_sentiments",
            "tool_arguments": {"limit": 5, "page": 0},
            "raw_data_only": True,
        }
        agent_output_direct_sentiments = await agent.handle_message(agent_input_direct_sentiments)

        # Direct tool call for market sentiments with default limit
        agent_input_direct_sentiments_default = {
            "tool": "get_sentiments",
            "tool_arguments": {},
            "raw_data_only": True,
        }
        agent_output_direct_sentiments_default = await agent.handle_message(agent_input_direct_sentiments_default)

        # Direct tool call for resistance and support levels
        agent_input_direct_resistance_support = {
            "tool": "get_resistance_support_levels",
            "tool_arguments": {"token_ids": "3393", "symbols": "DOGE", "limit": 10, "page": 0},
            "raw_data_only": True,
        }
        agent_output_direct_resistance_support = await agent.handle_message(agent_input_direct_resistance_support)

        # Direct tool call for resistance and support levels with default limit
        agent_input_direct_resistance_support_default = {
            "tool": "get_resistance_support_levels",
            "tool_arguments": {"token_ids": "3988,73672,42740", "symbols": "SOL,SOL,SOL"},
            "raw_data_only": True,
        }
        agent_output_direct_resistance_support_default = await agent.handle_message(
            agent_input_direct_resistance_support_default
        )

        # Direct tool call for resistance and support levels with custom token
        # This test first gets the token ID for SOL, then uses it in the resistance/support call
        agent_input_token_info_sol = {
            "tool": "get_token_info",
            "tool_arguments": {"token_symbol": "ETC"},
            "raw_data_only": True,
        }
        token_info_sol_result = await agent.handle_message(agent_input_token_info_sol)

        # Extract token ID if successful
        sol_token_id = None
        if (
            token_info_sol_result.get("status") == "success"
            and "data" in token_info_sol_result
            and "data" in token_info_sol_result["data"]
            and token_info_sol_result["data"]["data"]
        ):
            sol_token_id = str(token_info_sol_result["data"]["data"][0].get("TOKEN_ID"))

        if sol_token_id:
            agent_input_direct_custom_token = {
                "tool": "get_resistance_support_levels",
                "tool_arguments": {"token_ids": f"{sol_token_id},3375", "symbols": "SOL,BTC", "limit": 2},
                "raw_data_only": True,
            }
            agent_output_direct_custom_token = await agent.handle_message(agent_input_direct_custom_token)
        else:
            agent_output_direct_custom_token = {"error": "Could not retrieve SOL token ID"}

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_market_sentiment": agent_input_sentiments,
            "output_market_sentiment": agent_output_sentiments,
            "input_sentiment_with_limit": agent_input_sentiment_with_limit,
            "output_sentiment_with_limit": agent_output_sentiment_with_limit,
            "input_resistance_support": agent_input_resistance_support,
            "output_resistance_support": agent_output_resistance_support,
            "input_custom_token_symbol": agent_input_custom_token_symbol,
            "output_custom_token_symbol": agent_output_custom_token_symbol,
            "input_custom_token_name": agent_input_custom_token_name,
            "output_custom_token_name": agent_output_custom_token_name,
            "input_direct_token_info": agent_input_direct_token_info,
            "output_direct_token_info": agent_output_direct_token_info,
            "input_direct_sentiments": agent_input_direct_sentiments,
            "output_direct_sentiments": agent_output_direct_sentiments,
            "input_direct_sentiments_default": agent_input_direct_sentiments_default,
            "output_direct_sentiments_default": agent_output_direct_sentiments_default,
            "input_direct_resistance_support": agent_input_direct_resistance_support,
            "output_direct_resistance_support": agent_output_direct_resistance_support,
            "input_direct_resistance_support_default": agent_input_direct_resistance_support_default,
            "output_direct_resistance_support_default": agent_output_direct_resistance_support_default,
            "input_token_info_sol": agent_input_token_info_sol,
            "output_token_info_sol": token_info_sol_result,
            "input_direct_custom_token": agent_input_direct_custom_token
            if sol_token_id
            else {"error": "Could not construct request"},
            "output_direct_custom_token": agent_output_direct_custom_token,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
