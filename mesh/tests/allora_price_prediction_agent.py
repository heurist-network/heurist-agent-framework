# test_allora_agent.py
"""Test suite for Allora Price Prediction Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.allora_price_prediction_agent import AlloraPricePredictionAgent
from mesh.tests._test_agents import test_agent

# Define test cases
TEST_CASES = {
    "eth_price_5min": {
        "input": {"query": "Predict ETH price in 5 minutes"},
        "description": "Predict ETH price 5 minutes ahead",
    },
    "btc_price_1hour": {
        "input": {"query": "What will BTC price be in 1 hour?"},
        "description": "Predict BTC price 1 hour ahead",
    },
    "sol_price_30min": {
        "input": {"query": "Predict Solana price in 30 minutes"},
        "description": "Predict SOL price 30 minutes ahead",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(AlloraPricePredictionAgent, TEST_CASES))
