import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.tokenmetrics_agent import TokenMetricsAgent  # noqa: E402

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

        # Test direct tool calls
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
            "tool_arguments": {"token_ids": "3375,3306", "symbols": "BTC,ETH", "limit": 2, "page": 0},
            "raw_data_only": True,
        }
        agent_output_direct_resistance_support = await agent.handle_message(agent_input_direct_resistance_support)

        # Direct tool call for resistance and support levels with default limit
        agent_input_direct_resistance_support_default = {
            "tool": "get_resistance_support_levels",
            "tool_arguments": {"token_ids": "3375,3306", "symbols": "BTC,ETH"},
            "raw_data_only": True,
        }
        agent_output_direct_resistance_support_default = await agent.handle_message(
            agent_input_direct_resistance_support_default
        )

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
            "input_direct_sentiments": agent_input_direct_sentiments,
            "output_direct_sentiments": agent_output_direct_sentiments,
            "input_direct_sentiments_default": agent_input_direct_sentiments_default,
            "output_direct_sentiments_default": agent_output_direct_sentiments_default,
            "input_direct_resistance_support": agent_input_direct_resistance_support,
            "output_direct_resistance_support": agent_output_direct_resistance_support,
            "input_direct_resistance_support_default": agent_input_direct_resistance_support_default,
            "output_direct_resistance_support_default": agent_output_direct_resistance_support_default,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
