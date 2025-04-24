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

        print("\nQuery mode test:")
        print(f"Input: {query_input}")
        print(f"Output keys: {query_output.keys()}")

        # Test 2: Direct tool call mode
        tool_input = {"tool": "search_projects", "tool_arguments": {"name": "heurist", "limit": 1}}

        tool_output = await agent.handle_message(tool_input)

        print("\nTool mode test:")
        print(f"Input: {tool_input}")
        print(f"Output keys: {tool_output.keys()}")

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_results"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "query_test": {"input": query_input, "output": query_output},
            "tool_test": {"input": tool_input, "output": tool_output},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"\nResults saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
