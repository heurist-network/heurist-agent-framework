import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.zerion_wallet_analysis_agent import ZerionWalletAnalysisAgent  # noqa: E402

load_dotenv()

# 8453 chain is base


async def run_agent():
    agent = ZerionWalletAnalysisAgent()
    try:
        # Example for direct fetch_wallet_tokens tool
        agent_input_tokens = {
            "tool": "fetch_wallet_tokens",
            "tool_arguments": {"wallet_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D"},
            "raw_data_only": False,
        }
        agent_output_tokens = await agent.handle_message(agent_input_tokens)

        # Example for fetch_wallet_nfts tool
        agent_input_nfts = {
            "tool": "fetch_wallet_nfts",
            "tool_arguments": {"wallet_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D"},
            "raw_data_only": False,
        }
        agent_output_nfts = await agent.handle_message(agent_input_nfts)

        # Example with raw data only
        agent_input_raw = {
            "query": "What tokens does 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D hold?",
            "raw_data_only": True,
        }
        agent_output_raw = await agent.handle_message(agent_input_raw)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "token_holdings": {"input": agent_input_tokens, "output": agent_output_tokens},
            "nft_holdings": {"input": agent_input_nfts, "output": agent_output_nfts},
            "raw_data_query": {"input": agent_input_raw, "output": agent_output_raw},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
