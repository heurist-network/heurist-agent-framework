import asyncio
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.aixbt_project_info_agent import AixbtProjectInfoAgent  # noqa: E402


async def run_agent():
    agent = AixbtProjectInfoAgent()
    try:
        # Test 1: Natural language query mode
        query_input = {"query": "Tell me about trending projects on Ethereum"}
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

        # Test 6: Empty tool_arguments (should fallback or error gracefully)
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
            "empty_args_test": {"input": empty_input, "output": empty_output},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"\nResults saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
