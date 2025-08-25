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

        # Test token metrics with different quote tokens including native_sol
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"
        quote_tokens = ["usdc", "sol", "virtual", "native_sol"]  # Added native_sol
        metrics_results = {}

        for quote_token in quote_tokens:
            print(f"\nTesting metrics with {quote_token.upper()} quote token:")

            # Test via natural language query
            metrics_input = {"query": f"Get market cap and trade volume for {test_token} using {quote_token} pair"}
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

        # Test token holders functionality with different limits
        test_token = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
        print("\nTesting token holders functionality:")

        # Test via natural language query
        holders_input = {"query": f"Show me the top 15 token holders of {test_token}"}
        holders_output = await agent.handle_message(holders_input)
        print("Natural language query result for token holders:")
        print(yaml.dump(holders_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call with limit
        holders_direct_input = {
            "tool": "query_token_holders",
            "tool_arguments": {"token_address": test_token, "limit": 15},
            "raw_data_only": True,
        }
        holders_direct_output = await agent.handle_message(holders_direct_input)
        print("Direct tool call result for token holders:")
        print(yaml.dump(holders_direct_output, allow_unicode=True, sort_keys=False))

        # Test token buyers functionality with higher limits
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"
        print("\nTesting token buyers functionality:")

        # Test via natural language query
        buyers_input = {"query": f"Show me the first 50 buyers of {test_token}"}
        buyers_output = await agent.handle_message(buyers_input)
        print("Natural language query result for token buyers:")
        print(yaml.dump(buyers_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call with higher limit
        buyers_direct_input = {
            "tool": "query_token_buyers",
            "tool_arguments": {"token_address": test_token, "limit": 50},
            "raw_data_only": True,
        }
        buyers_direct_output = await agent.handle_message(buyers_direct_input)
        print("Direct tool call result for token buyers:")
        print(yaml.dump(buyers_direct_output, allow_unicode=True, sort_keys=False))

        # Test holder status functionality with multiple test addresses
        test_token = "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump"
        test_addresses = [
            "5ZZnqunFJZr7QgL6ciFGJtbdy35GoVkvv672JTWhVgET",
            "DNZwmHYrS7bekmsJeFPxFvkWRfXRPu44phUqZgdK7Pxy",
            "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
            "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
            "FNNvb1AFDnDVPkocEri8mWbJ1952HQZtFLuwPiUjSJQ",
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

        # Test top traders functionality with different limits
        test_token = "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"
        print("\nTesting top traders functionality:")

        # Test via natural language query
        traders_input = {"query": f"List the top 20 traders of {test_token} by volume"}
        traders_output = await agent.handle_message(traders_input)
        print("Natural language query result for top traders:")
        print(yaml.dump(traders_output, allow_unicode=True, sort_keys=False))

        # Test via direct tool call with higher limit
        traders_direct_input = {
            "tool": "query_top_traders",
            "tool_arguments": {"token_address": test_token, "limit": 20},
            "raw_data_only": True,
        }
        traders_direct_output = await agent.handle_message(traders_direct_input)
        print("Direct tool call result for top traders:")
        print(yaml.dump(traders_direct_output, allow_unicode=True, sort_keys=False))

        # Test with a query for trending tokens with different limits
        agent_input_trending = {"query": "Get top 15 trending tokens on Solana"}
        agent_output_trending = await agent.handle_message(agent_input_trending)
        print(f"Result of handle_message (trending tokens): {agent_output_trending}")

        # Test direct tool call for token metrics with native_sol
        agent_input_direct_tool = {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
                "quote_token": "native_sol",
            },
        }
        agent_output_direct_tool = await agent.handle_message(agent_input_direct_tool)
        print(f"Result of direct tool call (token metrics with native_sol): {agent_output_direct_tool}")

        # Test direct tool call for top trending tokens with limit
        agent_input_direct_trending = {"tool": "get_top_trending_tokens", "tool_arguments": {"limit": 15}}
        agent_output_direct_trending = await agent.handle_message(agent_input_direct_trending)
        print(f"Result of direct tool call (trending tokens with limit): {agent_output_direct_trending}")

        # Test with raw_data_only flag
        agent_input_raw_data = {
            "query": "Get detailed token analysis for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
            "raw_data_only": True,
        }
        agent_output_raw_data = await agent.handle_message(agent_input_raw_data)
        print(f"Result with raw_data_only=True: {agent_output_raw_data}")

        # Test native_sol specific functionality
        print("\nTesting native_sol specific functionality:")

        # Test native SOL token metrics
        native_sol_metrics_input = {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "quote_token": "sol"},
            "raw_data_only": True,
        }
        native_sol_metrics_output = await agent.handle_message(native_sol_metrics_input)
        print(f"Native SOL metrics test: {native_sol_metrics_output}")

        # Test using native_sol as quote token for different tokens
        native_sol_quote_input = {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": test_token, "quote_token": "native_sol"},
            "raw_data_only": True,
        }
        native_sol_quote_output = await agent.handle_message(native_sol_quote_input)
        print(f"Native SOL as quote token test: {native_sol_quote_output}")

        # Test native SOL holders
        native_sol_holders_input = {
            "tool": "query_token_holders",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 10},
            "raw_data_only": True,
        }
        native_sol_holders_output = await agent.handle_message(native_sol_holders_input)
        print(f"Native SOL holders test: {native_sol_holders_output}")

        # Test native SOL buyers
        native_sol_buyers_input = {
            "tool": "query_token_buyers",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 20},
            "raw_data_only": True,
        }
        native_sol_buyers_output = await agent.handle_message(native_sol_buyers_input)
        print(f"Native SOL buyers test: {native_sol_buyers_output}")

        # Test native SOL top traders
        native_sol_traders_input = {
            "tool": "query_top_traders",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 15},
            "raw_data_only": True,
        }
        native_sol_traders_output = await agent.handle_message(native_sol_traders_input)
        print(f"Native SOL traders test: {native_sol_traders_output}")

        # Test price movement analysis
        price_analysis_input = {
            "query": f"Analyze price movements and trading volume for token {test_token} in the last hour"
        }
        price_analysis_output = await agent.handle_message(price_analysis_input)
        print(f"Price analysis result: {price_analysis_output}")

        # Test with different quote token addresses directly
        direct_quote_address_input = {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": test_token,
                "quote_token": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC direct address
            },
            "raw_data_only": True,
        }
        direct_quote_address_output = await agent.handle_message(direct_quote_address_input)
        print(f"Direct quote address test: {direct_quote_address_output}")

        # Test large batch holder status (chunking functionality)
        large_address_list = test_addresses * 12  # 60 addresses to test chunking
        large_batch_input = {
            "tool": "query_holder_status",
            "tool_arguments": {"token_address": test_token, "buyer_addresses": large_address_list},
            "raw_data_only": True,
        }
        large_batch_output = await agent.handle_message(large_batch_input)
        print(f"Large batch chunking test: {large_batch_output}")

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
            "native_sol_tests": {
                "native_sol_metrics": {"input": native_sol_metrics_input, "output": native_sol_metrics_output},
                "native_sol_as_quote": {"input": native_sol_quote_input, "output": native_sol_quote_output},
                "native_sol_holders": {"input": native_sol_holders_input, "output": native_sol_holders_output},
                "native_sol_buyers": {"input": native_sol_buyers_input, "output": native_sol_buyers_output},
                "native_sol_traders": {"input": native_sol_traders_input, "output": native_sol_traders_output},
            },
            "additional_tests": {
                "price_analysis": {"input": price_analysis_input, "output": price_analysis_output},
                "direct_quote_address": {"input": direct_quote_address_input, "output": direct_quote_address_output},
                "large_batch_chunking": {"input": large_batch_input, "output": large_batch_output},
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
