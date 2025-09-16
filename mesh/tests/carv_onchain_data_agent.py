import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.carv_onchain_data_agent import CarvOnchainDataAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "ethereum_query": {
        "input": {"query": "Identify the biggest transaction of ETH in the past 30 days"},
        "description": "Natural language query for biggest ETH transaction in past 30 days",
    },
    "direct_tool_call": {
        "input": {
            "tool": "query_onchain_data",
            "tool_arguments": {
                "blockchain": "bitcoin",
                "query": "How many Bitcoins have been mined since the beginning of 2025?",
            },
        },
        "description": "Direct tool call for Bitcoin mining data since 2025",
    },
    "raw_data_query": {
        "input": {
            "query": "What are the top 5 most popular smart contracts on Ethereum in the past 30 days?",
            "raw_data_only": True,
        },
        "description": "Smart contracts query with raw data only flag",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(CarvOnchainDataAgent, TEST_CASES))
