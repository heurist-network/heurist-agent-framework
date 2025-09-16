import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.zerion_wallet_analysis_agent import ZerionWalletAnalysisAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "fetch_wallet_tokens": {
        "input": {
            "tool": "fetch_wallet_tokens",
            "tool_arguments": {"wallet_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D"},
            "raw_data_only": False,
        },
        "description": "Direct tool call to fetch wallet token holdings",
    },
    "fetch_wallet_nfts": {
        "input": {
            "tool": "fetch_wallet_nfts",
            "tool_arguments": {"wallet_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D"},
            "raw_data_only": False,
        },
        "description": "Direct tool call to fetch wallet NFT holdings",
    },
    "wallet_tokens_query": {
        "input": {
            "query": "What tokens does 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D hold?",
            "raw_data_only": True,
        },
        "description": "Natural language query for wallet token holdings with raw data",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ZerionWalletAnalysisAgent, TEST_CASES))
