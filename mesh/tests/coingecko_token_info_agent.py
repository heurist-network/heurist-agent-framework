import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.coingecko_token_info_agent import CoinGeckoTokenInfoAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = CoinGeckoTokenInfoAgent()
    try:
        # Below commented tests are from previous version examples:
        """
        # Test with a query mentioning CoinGecko ID
        agent_input = {"query": "Get information about MONA"}

        agent_output = await agent.handle_message(agent_input)

        # Test with query mentioned the token name
        agent_input_name = {"query": "analyze HEU"}

        agent_output_name = await agent.handle_message(agent_input_name)

        # test with trending coins
        agent_input_trending = {"query": "Get information about trending coins"}
        agent_output_trending = await agent.handle_message(agent_input_trending)

        """
        # NEW: Test with categories list
        agent_input_categories = {"query": "List all cryptocurrency categories"}
        agent_output_categories = await agent.handle_message(agent_input_categories)

        # NEW: Test with category data
        agent_input_category_data = {"query": "Show me market data for all cryptocurrency categories"}
        agent_output_category_data = await agent.handle_message(agent_input_category_data)

        # NEW: Test with tokens by category
        agent_input_category_tokens = {"query": "Show me all tokens in the layer-1 category"}
        agent_output_category_tokens = await agent.handle_message(agent_input_category_tokens)

        # NEW: Test direct tool calls for each new category function
        agent_input_direct_categories = {"tool": "get_categories_list", "tool_arguments": {}, "raw_data_only": True}
        agent_output_direct_categories = await agent.handle_message(agent_input_direct_categories)

        agent_input_direct_category_data = {
            "tool": "get_category_data",
            "tool_arguments": {"order": "market_cap_desc"},
            "raw_data_only": True,
        }
        agent_output_direct_category_data = await agent.handle_message(agent_input_direct_category_data)

        agent_input_direct_category_tokens = {
            "tool": "get_tokens_by_category",
            "tool_arguments": {
                "category_id": "layer-1",
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
            },
            "raw_data_only": True,
        }
        agent_output_direct_category_tokens = await agent.handle_message(agent_input_direct_category_tokens)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        # Below commented tests are from previous version
        yaml_content = {
            # "input_by_id": agent_input,
            # "output_by_id": agent_output,
            # "input_by_name": agent_input_name,
            # "output_by_name": agent_output_name,
            # "input_by_trending": agent_input_trending,
            # "output_by_trending": agent_output_trending,
            "input_categories_list": agent_input_categories,
            "output_categories_list": agent_output_categories,
            "input_category_data": agent_input_category_data,
            "output_category_data": agent_output_category_data,
            "input_category_tokens": agent_input_category_tokens,
            "output_category_tokens": agent_output_category_tokens,
            "input_direct_categories": agent_input_direct_categories,
            "output_direct_categories": agent_output_direct_categories,
            "input_direct_category_data": agent_input_direct_category_data,
            "output_direct_category_data": agent_output_direct_category_data,
            "input_direct_category_tokens": agent_input_direct_category_tokens,
            "output_direct_category_tokens": agent_output_direct_category_tokens,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
