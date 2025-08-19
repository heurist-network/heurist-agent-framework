import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.arkham_intelligence_agent import ArkhamIntelligenceAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = ArkhamIntelligenceAgent()
    try:
        # Test 1: Natural language query for address intelligence
        agent_input_1 = {
            "query": "Analyze address 0xec463d00aa4da76fb112cd2e4ac1c6bef02da6ea on ethereum",
            "raw_data_only": False,
        }
        agent_output_1 = await agent.handle_message(agent_input_1)

        # Test 2: Direct tool call for address intelligence on Base
        agent_input_2 = {
            "tool": "get_address_intelligence",
            "tool_arguments": {"address": "0x7d9d1821d15b9e0b8ab98a058361233e255e405d", "chain": "base"},
            "raw_data_only": True,
        }
        agent_output_2 = await agent.handle_message(agent_input_2)

        # Test 3: Contract metadata for EVM chain (Ethereum)
        agent_input_3 = {
            "tool": "get_contract_metadata",
            "tool_arguments": {"chain": "ethereum", "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"},
        }
        agent_output_3 = await agent.handle_message(agent_input_3)

        # Test 4: Portfolio snapshot
        agent_input_4 = {
            "query": "Get portfolio snapshot for 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
            "raw_data_only": False,
        }
        agent_output_4 = await agent.handle_message(agent_input_4)

        # Test 5: Token holders analysis
        agent_input_5 = {
            "tool": "get_token_holders",
            "tool_arguments": {
                "chain": "ethereum",
                "address": "0xdd3b11ef34cd511a2da159034a05fcb94d806686",
                "groupByEntity": True,
            },
        }
        agent_output_5 = await agent.handle_message(agent_input_5)

        # Test 6: Token holders analysis - USDC on Base (different chain)
        agent_input_6 = {
            "tool": "get_token_holders",
            "tool_arguments": {
                "chain": "base",
                "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
                "groupByEntity": True,
            },
        }
        agent_output_6 = await agent.handle_message(agent_input_6)

        # Test 7: Natural language query for token holders on unsupported chain
        agent_input_7 = {
            "query": "Show me the top holders of token 0xdAC17F958D2ee523a2206206994597C13D831ec7 on Solana",
            "raw_data_only": False,
        }
        agent_output_7 = await agent.handle_message(agent_input_7)

        # Test 8: Portfolio with specific timestamp
        agent_input_8 = {
            "tool": "get_portfolio_snapshot",
            "tool_arguments": {
                "address": "0x742d35Cc6634C0532925a3b8D84c5d146D4B6bb2",
                "time": 1748361600000,  # Specific timestamp
            },
        }
        agent_output_8 = await agent.handle_message(agent_input_8)

        # Save results to YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_results"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "address_intelligence_nlp": {"input": agent_input_1, "output": agent_output_1},
            "address_intelligence_base": {"input": agent_input_2, "output": agent_output_2},
            "contract_metadata_ethereum": {"input": agent_input_3, "output": agent_output_3},
            "portfolio_snapshot_nlp": {"input": agent_input_4, "output": agent_output_4},
            "token_holders_usdc_ethereum": {"input": agent_input_5, "output": agent_output_5},
            "token_holders_usdc_base": {"input": agent_input_6, "output": agent_output_6},
            "token_holders_solana_nlp": {"input": agent_input_7, "output": agent_output_7},
            "portfolio_with_timestamp": {"input": agent_input_8, "output": agent_output_8},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
