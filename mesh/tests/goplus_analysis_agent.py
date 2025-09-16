import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.goplus_analysis_agent import GoplusAnalysisAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "ethereum_token_safety": {
        "input": {"query": "Check the safety of this token: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 on Ethereum"},
        "description": "Natural language query for Ethereum token safety analysis",
    },
    "solana_token_safety": {
        "input": {"query": "Check the safety of this Solana token: AcmFHCquGwbrPxh9b3sUPMtAtXKMjkEzKnqkiHEnpump"},
        "description": "Natural language query for Solana token safety analysis",
    },
    "ethereum_direct_tool": {
        "input": {
            "tool": "fetch_security_details",
            "tool_arguments": {"contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "chain_id": "1"},
        },
        "description": "Direct tool call for Ethereum token security details (USDC)",
    },
    "base_direct_tool": {
        "input": {
            "tool": "fetch_security_details",
            "tool_arguments": {"contract_address": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb", "chain_id": "8453"},
        },
        "description": "Direct tool call for Base network token security details",
    },
    "raw_data_query": {
        "input": {
            "query": "Is 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 safe on chain 1?",
            "raw_data_only": True,
        },
        "description": "Token safety query with raw data flag (WBTC on Ethereum)",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(GoplusAnalysisAgent, TEST_CASES))
