import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.firecrawl_search_agent import FirecrawlSearchAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = FirecrawlSearchAgent()
    try:
        # Example for natural language query
        agent_input = {
            "query": "What are the latest developments in zero knowledge proofs?",
            "raw_data_only": False,
        }
        agent_output = await agent.handle_message(agent_input)
        
        # Example for direct execute_search tool
        agent_input_search = {
            "tool": "execute_search",
            "tool_arguments": {
                "search_term": "zero knowledge proofs recent advancements"
            },
            "raw_data_only": False,
        }
        agent_output_search = await agent.handle_message(agent_input_search)
        
        # Example for generate_queries tool
        agent_input_queries = {
            "tool": "generate_queries",
            "tool_arguments": {
                "topic": "zero knowledge proofs",
                "num_queries": 3
            },
            "raw_data_only": False,
        }
        agent_output_queries = await agent.handle_message(agent_input_queries)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_query": {"input": agent_input, "output": agent_output},
            "direct_search": {"input": agent_input_search, "output": agent_output_search},
            "generate_queries": {"input": agent_input_queries, "output": agent_output_queries}
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())