import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.pond_wallet_analysis_agent import PondWalletAnalysisAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Natural language queries
    "ethereum_wallet_natural": {
        "input": {
            "query": "Analyze Ethereum wallet 0x2B25B37c683F042E9Ae1877bc59A1Bb642Eb1073",
            "raw_data_only": False,
        },
        "description": "Natural language query for Ethereum wallet analysis",
    },
    "solana_wallet_natural": {
        "input": {
            "query": "What's the trading volume for Solana wallet 8gc59zf1ZQCxzkSuepV8WmuuobHCPpydJ2RLqwXyCASS?",
            "raw_data_only": False,
        },
        "description": "Natural language query for Solana wallet trading volume",
    },
    "base_wallet_natural": {
        "input": {
            "query": "Check the transaction activity for Base wallet 0x97224Dd2aFB28F6f442E773853F229B3d8A0999a",
            "raw_data_only": False,
        },
        "description": "Natural language query for Base wallet transaction activity",
    },
    # Direct tool calls
    "ethereum_wallet_direct": {
        "input": {
            "tool": "analyze_ethereum_wallet",
            "tool_arguments": {"address": "0x73AF3bcf944a6559933396c1577B257e2054D935"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Ethereum wallet analysis with raw data",
    },
    "solana_wallet_direct": {
        "input": {
            "tool": "analyze_solana_wallet",
            "tool_arguments": {"address": "7g275uQ9JuvTa7EC3TERyAsQUGwid9eDYK2JgpSLrmjK"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Solana wallet analysis with raw data",
    },
    "base_wallet_direct": {
        "input": {
            "tool": "analyze_base_wallet",
            "tool_arguments": {"address": "0x1C0002972259E13dBC5eAF01D108624430c744f9"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Base wallet analysis with raw data",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(PondWalletAnalysisAgent, TEST_CASES))
