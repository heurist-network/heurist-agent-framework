import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.exa_search_agent import ExaSearchAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = ExaSearchAgent()
    try:
        # Natural language query
        agent_input = {
            "query": "What are the latest developments in quantum computing?",
            "raw_data_only": False,
        }
        agent_output = await agent.handle_message(agent_input)

        # Direct search tool call
        agent_input_search = {
            "tool": "exa_web_search",
            "tool_arguments": {"search_term": "quantum computing breakthroughs 2024", "limit": 5},
            "raw_data_only": False,
        }
        agent_output_search = await agent.handle_message(agent_input_search)

        # Direct answer tool call
        agent_input_answer = {
            "tool": "exa_answer_question",
            "tool_arguments": {"question": "What is quantum supremacy?"},
            "raw_data_only": False,
        }
        agent_output_answer = await agent.handle_message(agent_input_answer)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_query": {"input": agent_input, "output": agent_output},
            "direct_search": {"input": agent_input_search, "output": agent_output_search},
            "direct_answer": {"input": agent_input_answer, "output": agent_output_answer},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
