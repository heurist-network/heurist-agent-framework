import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.arbus_agent import ArbusAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = ArbusAgent()
    try:
        # Test 1: AI Assistant - Direct tool call
        agent_input_ai_direct = {
            "tool": "ask_ai_assistant",
            "tool_arguments": {"query": "What's happening with DeFi markets?", "days": 7},
        }
        agent_output_ai_direct = await agent.handle_message(agent_input_ai_direct)

        # Test 2: AI Assistant - Natural language query
        agent_input_ai_query = {"query": "Is Bitcoin bullish right now?"}
        agent_output_ai_query = await agent.handle_message(agent_input_ai_query)

        # Test 3: AI Assistant - Market sentiment query
        agent_input_sentiment_query = {"query": "Analyze the current crypto market sentiment over the last 14 days"}
        agent_output_sentiment_query = await agent.handle_message(agent_input_sentiment_query)

        # Test 4: Report Generation - Direct tool call
        agent_input_report_direct = {
            "tool": "generate_report",
            "tool_arguments": {"twitter_handle": "ethereum", "category": "projects"},
        }
        agent_output_report_direct = await agent.handle_message(agent_input_report_direct)

        # Test 5: Report Generation - Natural language query
        agent_input_report_query = {"query": "Generate a report on Ethereum's partnerships"}
        agent_output_report_query = await agent.handle_message(agent_input_report_query)

        # Test 6: Report Generation - Solana with date range
        agent_input_report_solana = {
            "tool": "generate_report",
            "tool_arguments": {
                "twitter_handle": "solana",
                "category": "projects",
                "date_from": "2024-01-01",
                "date_to": "2024-12-31",
            },
        }
        agent_output_report_solana = await agent.handle_message(agent_input_report_solana)

        # Save results to YAML
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "ai_assistant_direct": {"input": agent_input_ai_direct, "output": agent_output_ai_direct},
            "ai_assistant_query": {"input": agent_input_ai_query, "output": agent_output_ai_query},
            "ai_assistant_sentiment": {"input": agent_input_sentiment_query, "output": agent_output_sentiment_query},
            "report_generation_direct": {"input": agent_input_report_direct, "output": agent_output_report_direct},
            "report_generation_query": {"input": agent_input_report_query, "output": agent_output_report_query},
            "report_generation_solana": {"input": agent_input_report_solana, "output": agent_output_report_solana},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
