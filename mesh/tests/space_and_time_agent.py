import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.space_and_time_agent import SpaceTimeAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "ethereum_blocks_query": {
        "input": {
            "query": "Get the number of blocks created on Ethereum per day over the last month",
            "raw_data_only": False,
        },
        "description": "Natural language query for Ethereum daily block creation in last month",
    },
    "ethereum_transactions_direct": {
        "input": {
            "tool": "generate_and_execute_sql",
            "tool_arguments": {"nl_query": "What's the average transactions in past week for Ethereum"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Ethereum average transactions in past week",
    },
    "heurist_gpus_query": {
        "input": {
            "query": "Tell me top 10 GPUs from HEURIST",
            "raw_data_only": False,
        },
        "description": "Natural language query for top 10 GPUs from HEURIST",
    },
    "ethereum_yesterday_transactions": {
        "input": {
            "query": "How many transactions occurred on Ethereum yesterday?",
            "raw_data_only": False,
        },
        "description": "Natural language query for Ethereum transactions count yesterday",
    },
    "ethereum_largest_transaction": {
        "input": {
            "query": "What's the largest transaction value on Ethereum in the past 24 hours?",
            "raw_data_only": False,
        },
        "description": "Natural language query for largest Ethereum transaction value in last 24 hours",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(SpaceTimeAgent, TEST_CASES))
