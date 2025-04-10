import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.funding_rate_agent import FundingRateAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = FundingRateAgent()
    try:
        # Test with a query for all funding rates
        agent_input = {"query": "What are the current funding rates for Bitcoin?"}

        agent_output = await agent.handle_message(agent_input)

        # Test with query for cross-exchange arbitrage opportunities
        agent_input_arb = {
            "query": "Find arbitrage opportunities across exchanges with at least 0.05% funding rate difference"
        }

        agent_output_arb = await agent.handle_message(agent_input_arb)

        # Test with query for spot-futures opportunities
        agent_input_spot = {"query": "What are the best spot-futures funding rate opportunities right now?"}
        agent_output_spot = await agent.handle_message(agent_input_spot)
        print(f"Result of handle_message for spot-futures opportunities: {agent_output_spot}")

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_by_symbol": agent_input,
            "output_by_symbol": agent_output,
            "input_by_arbitrage": agent_input_arb,
            "output_by_arbitrage": agent_output_arb,
            "input_by_spot_futures": agent_input_spot,
            "output_by_spot_futures": agent_output_spot,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
