import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))

import yaml

from mesh.sol_wallet_agent import SolWalletAgent

load_dotenv()

async def run_agent():
    ca = "J7tYmq2JnQPvxyhcXpCDrvJnc9R5ts8rv7tgVHDPsw7U"
    wallet = "DbDi7soBXALYRMZSyJMEAfpaK3rD1hr5HuCYzuDrcEEN"

    async with SolWalletAgent() as agent:
        try:
            agent_input_query = {
                "query": f"Give me the holders of this {ca}",
                "raw_data_only": False,
            }
            agent_output_query = await agent.handle_message(agent_input_query)
            print(agent_output_query)

            agent_input_query_raw = {
                "query": f"Show me the txs of this wallet {wallet}",
                "raw_data_only": True,
            }
            agent_output_query_raw = await agent.handle_message(agent_input_query_raw)
            print(agent_output_query_raw)


            agent_input_assets = {
                "tool": "get_wallet_assets",
                "tool_arguments": {"owner_address": wallet},
            }
            agent_output_assets = await agent.handle_message(agent_input_assets)
            print(f"Result of get_wallet_assets: {agent_output_assets}")


            agent_input_tx = {
                "tool": "get_tx_history",
                "tool_arguments": {"owner_address": wallet},
            }
            agent_output_tx = await agent.handle_message(agent_input_tx)
            print(f"Result of get_tx_history: {agent_output_tx}")


            agent_input_holders = {
                "tool": "analyze_holders",
                "tool_arguments": {"token_address": ca},
            }
            agent_output_holders = await agent.handle_message(agent_input_holders)
            print(f"Result of analyze_holders: {agent_output_holders}")

            script_dir = Path(__file__).parent
            current_file = Path(__file__).stem
            base_filename = f"{current_file}_example"
            output_file = script_dir / f"{base_filename}.yaml"

            yaml_content = {
                "natural_language_query_with_analysis": {"input": agent_input_query, "output": agent_output_query},
                "natural_language_query_raw_data": {"input": agent_input_query_raw, "output": agent_output_query_raw},
                "get_wallet_assets_test": {"input": agent_input_assets, "output": agent_output_assets},
                "get_tx_history_test": {"input": agent_input_tx, "output": agent_output_tx},
                "analyze_holders_test": {"input": agent_input_holders, "output": agent_output_holders},
            }

            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

            print(f"Results saved to {output_file}")


        finally:
            await agent.cleanup()





if __name__ == "__main__":
    asyncio.run(run_agent())
