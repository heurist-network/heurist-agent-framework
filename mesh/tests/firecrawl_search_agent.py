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
        # Example for natural language query with analysis
        agent_input_query = {
            "query": "What are the latest developments in zero knowledge proofs?",
            "raw_data_only": False,
        }
        agent_output_query = await agent.handle_message(agent_input_query)

        # Example for natural language query with raw data only
        agent_input_query_raw = {
            "query": "What are the latest developments in zero knowledge proofs?",
            "raw_data_only": True,
        }
        agent_output_query_raw = await agent.handle_message(agent_input_query_raw)

        # Example for direct tool (no LLM analysis, always returns raw data)
        agent_input_search = {
            "tool": "firecrawl_web_search",
            "tool_arguments": {"search_term": "zero knowledge proofs recent advancements"},
        }
        agent_output_search = await agent.handle_message(agent_input_search)

        # Example for direct tool (no LLM analysis, always returns raw data)
        agent_input_extract = {
            "tool": "firecrawl_extract_web_data",
            "tool_arguments": {
                "urls": ["https://ethereum.org/en/zero-knowledge-proofs/"],
                "extraction_prompt": "Extract information about how zero knowledge proofs are being used in blockchain technology",
                "enable_web_search": False,
            },
        }
        agent_output_extract = await agent.handle_message(agent_input_extract)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_query_with_analysis": {"input": agent_input_query, "output": agent_output_query},
            "natural_language_query_raw_data": {"input": agent_input_query_raw, "output": agent_output_query_raw},
            "direct_search": {"input": agent_input_search, "output": agent_output_search},
            "direct_extract": {"input": agent_input_extract, "output": agent_output_extract},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
