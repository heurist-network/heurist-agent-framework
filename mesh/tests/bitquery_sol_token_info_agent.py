import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.bitquery_solana_token_info_agent import BitquerySolanaTokenInfoAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = BitquerySolanaTokenInfoAgent()
    try:
        # Test with a query that mentions a token mint address for trading info
        agent_input = {"query": "Get token info for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"}
        agent_output = await agent.handle_message(agent_input)
        print(f"Result of handle_message (by token address): {agent_output}")

        # Test token metrics with different quote tokens
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"
        quote_tokens = ["usdc", "sol", "virtual"]
        metrics_results = {}

        for quote_token in quote_tokens:
            print(f"\nTesting metrics with {quote_token.upper()} quote token:")

            # Test via natural language query
            metrics_input = {
                "query": f"Get market cap, liquidity and trade volume for {test_token} using {quote_token} pair"
            }
            metrics_output = await agent.handle_message(metrics_input)
            print(f"Natural language query result for {quote_token}:")
            print(yaml.dump(metrics_output, allow_unicode=True, sort_keys=False))

            # Test via direct tool call
            metrics_direct_input = {
                "tool": "query_token_metrics",
                "tool_arguments": {"token_address": test_token, "quote_token": quote_token},
                "raw_data_only": True,
            }
            metrics_direct_output = await agent.handle_message(metrics_direct_input)

            metrics_results[f"{quote_token}_pair"] = {
                "natural_language_query": {"input": metrics_input, "output": metrics_output},
                "direct_tool_call": {"input": metrics_direct_input, "output": metrics_direct_output},
            }

        # Test token holders functionality
        test_token = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"  # USDC token address
        print("\nTesting token holders functionality:")

        # Test via natural language query
        holders_input = {"query": f"Show me the top token holders of {test_token}"}
        holders_output = await agent.handle_message(holders_input)
        print("Natural language query result for token holders:")
        print(yaml.dump(holders_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call
        holders_direct_input = {
            "tool": "query_token_holders",
            "tool_arguments": {"token_address": test_token},
            "raw_data_only": True,
        }
        holders_direct_output = await agent.handle_message(holders_direct_input)
        print("Direct tool call result for token holders:")
        print(yaml.dump(holders_direct_output, allow_unicode=True, sort_keys=False))

        # Test token buyers functionality
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"  # Example token address
        print("\nTesting token buyers functionality:")

        # Test via natural language query
        buyers_input = {"query": f"Show me the first 100 buyers of {test_token}"}
        buyers_output = await agent.handle_message(buyers_input)
        print("Natural language query result for token buyers:")
        print(yaml.dump(buyers_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call
        buyers_direct_input = {
            "tool": "query_token_buyers",
            "tool_arguments": {"token_address": test_token, "limit": 100},
            "raw_data_only": True,
        }
        buyers_direct_output = await agent.handle_message(buyers_direct_input)
        print("Direct tool call result for token buyers:")
        print(yaml.dump(buyers_direct_output, allow_unicode=True, sort_keys=False))

        # Test holder status functionality
        test_token = "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump"  # Example token address
        test_addresses = [
            "5ZZnqunFJZr7QgL6ciFGJtbdy35GoVkvv672JTWhVgET",
            "DNZwmHYrS7bekmsJeFPxFvkWRfXRPu44phUqZgdK7Pxy",
        ]
        print("\nTesting holder status functionality:")

        # Test via natural language query
        holder_status_input = {"query": f"Check if these addresses {test_addresses} are still holding {test_token}"}
        holder_status_output = await agent.handle_message(holder_status_input)
        print("Natural language query result for holder status:")
        print(yaml.dump(holder_status_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call
        holder_status_direct_input = {
            "tool": "query_holder_status",
            "tool_arguments": {"token_address": test_token, "buyer_addresses": test_addresses},
            "raw_data_only": True,
        }
        holder_status_direct_output = await agent.handle_message(holder_status_direct_input)
        print("Direct tool call result for holder status:")
        print(yaml.dump(holder_status_direct_output, allow_unicode=True, sort_keys=False))

        # Test top traders functionality
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"  # Example token address
        print("\nTesting top traders functionality:")

        # Test via natural language query
        traders_input = {"query": f"List the top traders of {test_token}"}
        traders_output = await agent.handle_message(traders_input)
        print("Natural language query result for top traders:")
        print(yaml.dump(traders_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call
        traders_direct_input = {
            "tool": "query_top_traders",
            "tool_arguments": {"token_address": test_token, "limit": 100},
            "raw_data_only": True,
        }
        traders_direct_output = await agent.handle_message(traders_direct_input)
        print("Direct tool call result for top traders:")
        print(yaml.dump(traders_direct_output, allow_unicode=True, sort_keys=False))

        # Test with a query for trending tokens
        agent_input_trending = {"query": "Get trending tokens"}
        agent_output_trending = await agent.handle_message(agent_input_trending)
        print(f"Result of handle_message (trending tokens): {agent_output_trending}")

        # Test direct tool call for token metrics
        agent_input_direct_tool = {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC", "quote_token": "sol"},
        }
        agent_output_direct_tool = await agent.handle_message(agent_input_direct_tool)
        print(f"Result of direct tool call (token metrics): {agent_output_direct_tool}")

        # Test direct tool call for top trending tokens
        agent_input_direct_trending = {"tool": "get_top_trending_tokens", "tool_arguments": {}}
        agent_output_direct_trending = await agent.handle_message(agent_input_direct_trending)
        print(f"Result of direct tool call (trending tokens): {agent_output_direct_trending}")

        # Test with raw_data_only flag
        agent_input_raw_data = {
            "query": "Get token info for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
            "raw_data_only": True,
        }
        agent_output_raw_data = await agent.handle_message(agent_input_raw_data)
        print(f"Result with raw_data_only=True: {agent_output_raw_data}")

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_by_token_address": agent_input,
            "output_by_token_address": agent_output,
            "token_metrics": metrics_results,
            "token_holders": {
                "natural_language_query": {"input": holders_input, "output": holders_output},
                "direct_tool_call": {"input": holders_direct_input, "output": holders_direct_output},
            },
            "token_buyers": {
                "natural_language_query": {"input": buyers_input, "output": buyers_output},
                "direct_tool_call": {"input": buyers_direct_input, "output": buyers_direct_output},
            },
            "holder_status": {
                "natural_language_query": {"input": holder_status_input, "output": holder_status_output},
                "direct_tool_call": {"input": holder_status_direct_input, "output": holder_status_direct_output},
            },
            "top_traders": {
                "natural_language_query": {"input": traders_input, "output": traders_output},
                "direct_tool_call": {"input": traders_direct_input, "output": traders_direct_output},
            },
            "input_trending": agent_input_trending,
            "output_trending": agent_output_trending,
            "input_direct_tool": agent_input_direct_tool,
            "output_direct_tool": agent_output_direct_tool,
            "input_direct_trending": agent_input_direct_trending,
            "output_direct_trending": agent_output_direct_trending,
            "input_raw_data": agent_input_raw_data,
            "output_raw_data": agent_output_raw_data,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
