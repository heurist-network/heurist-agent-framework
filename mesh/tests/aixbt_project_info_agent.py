import asyncio
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.aixbt_project_info_agent import AIXBTProjectInfoAgent  # noqa: E402


async def run_agent():
    agent = AIXBTProjectInfoAgent()
    try:
        # Test 1: Natural language query mode
        query_input = {"query": "Tell me about HEU token"}
        query_output = await agent.handle_message(query_input)

        # Test 2: Natural language query mode
        raw_query_input = {
            "query": "Tell me about trending projects on solana with minscore of 0.1",
            "raw_data_only": False,
        }
        raw_query_output = await agent.handle_message(raw_query_input)

        # Test 3: Direct tool call mode
        tool_input = {"tool": "search_projects", "tool_arguments": {"name": "heurist", "limit": 1}}
        tool_output = await agent.handle_message(tool_input)

        # Test 4: Tool call with keyword only
        keyword_input = {"tool": "search_projects", "tool_arguments": {"name": "ethereum"}}
        keyword_output = await agent.handle_message(keyword_input)

        # Test 5: Tool call with increased limit
        limit_input = {
            "tool": "search_projects",
            "tool_arguments": {"name": "bitcoin", "limit": 25},
            "raw_data_only": True,
        }
        limit_output = await agent.handle_message(limit_input)

        # Test 6: Direct tool call for market summary
        test_market_input = {"tool": "get_market_summary", "tool_arguments": {"lookback_days": 3}}
        test_market_output = await agent.handle_message(test_market_input)

        # Test 7: Direct tool call exceeding limit
        test_market_input2 = {"tool": "get_market_summary", "tool_arguments": {"lookback_days": 7}}
        test_market_output2 = await agent.handle_message(test_market_input2)

        # Test 8: Natural language query for market summary (today)
        market_nl_today = {"query": "What's happening in the crypto market today?"}
        market_nl_today_output = await agent.handle_message(market_nl_today)

        # Test 9: Natural language query for market summary (3 days)
        market_nl_3days = {"query": "Give me crypto market updates for the last 3 days"}
        market_nl_3days_output = await agent.handle_message(market_nl_3days)

        # Test 10: Natural language query requesting more than available
        market_nl_week = {"query": "What happened in crypto markets over the past week?"}
        market_nl_week_output = await agent.handle_message(market_nl_week)

        # Test 11: Natural language query requesting 30 days
        market_nl_month = {"query": "Can you show me the crypto market summary for the last 30 days?"}
        market_nl_month_output = await agent.handle_message(market_nl_month)

        # Test 12: Empty tool_arguments (should fallback or error gracefully)
        empty_input = {"tool": "search_projects", "tool_arguments": {}}
        empty_output = await agent.handle_message(empty_input)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_results"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "query_test": {"input": query_input, "output": query_output},
            "raw_query_test": {"input": raw_query_input, "output": raw_query_output},
            "tool_test": {"input": tool_input, "output": tool_output},
            "keyword_test": {"input": keyword_input, "output": keyword_output},
            "limit_test": {"input": limit_input, "output": limit_output},
            "test_market_direct": {"input": test_market_input, "output": test_market_output},
            "test_market_exceed": {"input": test_market_input2, "output": test_market_output2},
            "market_nl_today": {"input": market_nl_today, "output": market_nl_today_output},
            "market_nl_3days": {"input": market_nl_3days, "output": market_nl_3days_output},
            "market_nl_week": {"input": market_nl_week, "output": market_nl_week_output},
            "market_nl_month": {"input": market_nl_month, "output": market_nl_month_output},
            "empty_args_test": {"input": empty_input, "output": empty_output},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"\nResults saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
