import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.arkham_intelligence_agent import ArkhamIntelligenceAgent
from mesh.tests._test_agents import test_agent

load_dotenv()

TEST_CASES = {
    "address_analysis": {
        "input": {
            "query": "Analyze address 0xec463d00aa4da76fb112cd2e4ac1c6bef02da6ea on ethereum",
            "raw_data_only": False,
        },
        "description": "Natural language address intelligence query",
    },
    "base_address_direct": {
        "input": {
            "tool": "get_address_intelligence",
            "tool_arguments": {"address": "0x7d9d1821d15b9e0b8ab98a058361233e255e405d", "chain": "base"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Base chain address",
    },
    "contract_metadata": {
        "input": {
            "tool": "get_contract_metadata",
            "tool_arguments": {"chain": "ethereum", "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"},
        },
        "description": "Get WETH contract metadata on Ethereum",
    },
    "portfolio_snapshot": {
        "input": {
            "query": "Get portfolio snapshot for 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
            "raw_data_only": False,
        },
        "description": "Natural language portfolio query",
    },
    "token_holders_eth": {
        "input": {
            "tool": "get_token_holders",
            "tool_arguments": {
                "chain": "ethereum",
                "address": "0xdd3b11ef34cd511a2da159034a05fcb94d806686",
                "groupByEntity": True,
            },
        },
        "description": "Get token holders on Ethereum grouped by entity",
    },
    "token_holders_base": {
        "input": {
            "tool": "get_token_holders",
            "tool_arguments": {
                "chain": "base",
                "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "groupByEntity": True,
            },
        },
        "description": "Get USDC holders on Base chain",
    },
    "portfolio_with_timestamp": {
        "input": {
            "tool": "get_portfolio_snapshot",
            "tool_arguments": {"address": "0x742d35Cc6634C0532925a3b8D84c5d146D4B6bb2", "time": 1748361600000},
        },
        "description": "Portfolio snapshot at specific timestamp",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ArkhamIntelligenceAgent, TEST_CASES))
