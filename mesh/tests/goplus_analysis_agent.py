import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.goplus_analysis_agent import GoplusAnalysisAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = GoplusAnalysisAgent()
    try:
        # Test with a query for Ethereum token
        agent_input = {
            "query": "Check the safety of this token: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 on Ethereum"
        }
        agent_output = await agent.handle_message(agent_input)

        # Test with a query for Solana token
        agent_input_solana = {
            "query": "Check the safety of this Solana token: AcmFHCquGwbrPxh9b3sUPMtAtXKMjkEzKnqkiHEnpump"
        }
        agent_output_solana = await agent.handle_message(agent_input_solana)

        # Test direct tool call for Ethereum token
        agent_input_direct_tool = {
            "tool": "fetch_security_details",
            "tool_arguments": {"contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "chain_id": "1"},
        }
        agent_output_direct_tool = await agent.handle_message(agent_input_direct_tool)

        # Test direct tool call for Base token
        agent_input_direct_base = {
            "tool": "fetch_security_details",
            "tool_arguments": {"contract_address": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb", "chain_id": "8453"},
        }
        agent_output_direct_base = await agent.handle_message(agent_input_direct_base)

        # Test with raw_data_only flag
        agent_input_raw_data = {
            "query": "Is 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 safe on chain 1?",
            "raw_data_only": True,
        }
        agent_output_raw_data = await agent.handle_message(agent_input_raw_data)

        # Save the test inputs and outputs to a YAML file for further inspection
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_ethereum": agent_input,
            "output_ethereum": agent_output,
            "input_solana": agent_input_solana,
            "output_solana": agent_output_solana,
            "input_direct_ethereum": agent_input_direct_tool,
            "output_direct_ethereum": agent_output_direct_tool,
            "input_direct_base": agent_input_direct_base,
            "output_direct_base": agent_output_direct_base,
            "input_raw_data": agent_input_raw_data,
            "output_raw_data": agent_output_raw_data,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
