import asyncio
import sys
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.pumpfun_token_agent import PumpFunTokenAgent  # noqa: E402

load_dotenv()


QUERIES = {
    "creation": {"query": "Show me the latest Solana token creations in the last hour"},
    "graduated_tokens": {"query": "Show me all tokens that have graduated on Pump.fun in the last 48 hours"},
}


async def format_query_result(query_name: str, agent_output: Dict[str, Any]) -> Dict[str, Any]:
    """Format the query results based on query type."""
    base_result = {"input": QUERIES[query_name], "output": {"response": agent_output.get("response", ""), "data": {}}}

    if "error" in agent_output:
        return {"input": QUERIES[query_name], "error": str(agent_output["error"])}

    if query_name == "creation":
        base_result["output"]["data"] = {
            "tokens": [
                {
                    "name": token["token_info"]["name"],
                    "symbol": token["token_info"]["symbol"],
                    "mint_address": token["token_info"]["mint_address"],
                    "amount": token["amount"],
                    "signer": token["signer"],
                }
                for token in agent_output.get("data", {}).get("tokens", [])[:10]
            ]
        }
    elif query_name == "graduated_tokens":
        base_result["output"]["data"] = {
            "graduated_tokens": [
                {
                    "price_usd": token.get("price_usd", 0),
                    "market_cap_usd": token.get("market_cap_usd", 0),
                    "token_info": {
                        "name": token.get("token_info", {}).get("name", "Unknown"),
                        "symbol": token.get("token_info", {}).get("symbol", "Unknown"),
                        "mint_address": token.get("token_info", {}).get("mint_address", ""),
                        "decimals": token.get("token_info", {}).get("decimals", 0),
                    },
                }
                for token in agent_output.get("data", {}).get("graduated_tokens", [])
            ],
            "timeframe_hours": agent_output.get("data", {}).get("timeframe_hours", 24),
            "tokens_without_price_data": agent_output.get("data", {}).get("tokens_without_price_data", []),
        }

    return base_result


async def run_single_query(agent: PumpFunTokenAgent, query_name: str) -> Dict[str, Any]:
    """Run a single query using the PumpFunTokenAgent."""
    try:
        agent_input = QUERIES[query_name]
        agent_output = await agent.handle_message(agent_input)
        return await format_query_result(query_name, agent_output)
    except Exception as e:
        return {"input": QUERIES[query_name], "error": str(e)}


async def save_results(results: Dict[str, Any], output_file: Path):
    """Save results to a YAML file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(results, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"Error saving results: {str(e)}")


async def run_queries(query_type: str = "all", query_params: Dict = None):
    """Run queries based on the specified type with optional custom parameters."""
    results = {}
    script_dir = Path(__file__).parent
    current_file = Path(__file__).stem
    base_filename = f"{current_file}_example"
    output_file = script_dir / f"{base_filename}.yaml"

    query_params = query_params or {}

    async with PumpFunTokenAgent() as agent:
        try:
            if query_type.lower() == "all":
                for query_name in QUERIES.keys():
                    print(f"Running query: {query_name}")
                    if query_name in query_params:
                        # Update query if needed
                        if "query" in query_params[query_name]:
                            QUERIES[query_name]["query"] = query_params[query_name]["query"]
                    results[query_name] = await run_single_query(agent, query_name)
            elif query_type in QUERIES:
                if query_type in query_params:
                    # Update query if needed
                    if "query" in query_params[query_type]:
                        QUERIES[query_type]["query"] = query_params[query_type]["query"]
                results[query_type] = await run_single_query(agent, query_type)
            else:
                raise ValueError(f"Invalid query type. Must be one of: {', '.join(QUERIES.keys())} or 'all'")

            await save_results(results, output_file)
            print(f"Results saved to {output_file}")

        except Exception as e:
            print(f"Error executing queries: {str(e)}")


def main():
    """Main entry point for the script."""
    agent_query = "all"
    # Available agent_query options:
    # - creation (recent token creations)
    # - graduated_tokens (recently graduated tokens with prices)
    # - all (runs all queries)
    #
    print(f"Running query type: {agent_query}")
    asyncio.run(run_queries(agent_query))


async def test_graduated_tokens(timeframe=24):
    """Run only the graduated tokens test with a specific timeframe."""
    # Update the query to reflect the timeframe
    QUERIES["graduated_tokens"]["query"] = (
        f"Show me all tokens that have graduated on Pump.fun in the last {timeframe} hours"
    )

    # Run the query
    print(f"Running graduated_tokens test with {timeframe} hour timeframe")

    async with PumpFunTokenAgent() as agent:
        # First, try with natural language query
        nl_result = await run_single_query(agent, "graduated_tokens")
        print("Natural language query results:")
        print(yaml.dump(nl_result, allow_unicode=True, sort_keys=False))

        # Then try with direct tool call for comparison
        print("\nDirect tool call results:")
        direct_result = await agent.handle_message(
            {"tool": "query_latest_graduated_tokens", "tool_arguments": {"timeframe": timeframe}, "raw_data_only": True}
        )

        # Count and display tokens found
        token_count = len(direct_result.get("data", {}).get("graduated_tokens", []))
        print(f"Found {token_count} graduated tokens with price data")

        # Save results
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        output_file = script_dir / f"{current_file}_graduated_tokens_{timeframe}h.yaml"

        results = {
            "natural_language_query": nl_result,
            "direct_tool_call": {
                "input": {"tool": "query_latest_graduated_tokens", "tool_arguments": {"timeframe": timeframe}},
                "output": direct_result,
            },
        }

        await save_results(results, output_file)
        print(f"Results saved to {output_file}")


if __name__ == "__main__":
    # Uncomment to run only the graduated tokens test with a custom timeframe
    # asyncio.run(test_graduated_tokens(48))  # Use 48 hours timeframe

    main()
