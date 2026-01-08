# test_aave_agent.py
"""Test suite for Aave Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.aave_agent import AaveAgent
from mesh.tests._test_agents import test_agent

# Define test cases
TEST_CASES = {
    "borrow_rates_query": {
        "input": {"query": "What are the current borrow rates for USDC on Polygon?"},
        "description": "Natural language query for USDC borrow rates on Polygon",
    },
    "direct_tool_call": {
        "input": {"tool": "get_aave_reserves", "tool_arguments": {"chain_id": 42161, "asset_filter": "USDC"}},
        "description": "Direct tool call for USDC reserves on Arbitrum",
    },
    "polygon_assets_raw": {
        "input": {"query": "Show me all Aave assets on Polygon with their liquidity rates", "raw_data_only": True},
        "description": "Get all Polygon assets with raw data only",
    },
    "polygon_assets_formatted": {
        "input": {"query": "Show me all Aave assets on Polygon with their liquidity rates", "raw_data_only": False},
        "description": "Get all Polygon assets with formatted response",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(AaveAgent, TEST_CASES))
