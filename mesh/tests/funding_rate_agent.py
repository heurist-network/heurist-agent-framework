import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.funding_rate_agent import FundingRateAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "funding_rates_by_symbol": {
        "input": {"query": "What are the current funding rates for Bitcoin?"},
        "description": "Natural language query for Bitcoin funding rates",
    },
    "cross_exchange_arbitrage": {
        "input": {"query": "Find arbitrage opportunities across exchanges with at least 0.05% funding rate difference"},
        "description": "Natural language query for cross-exchange arbitrage opportunities with 0.05% minimum difference",
    },
    "spot_futures_opportunities": {
        "input": {"query": "What are the best spot-futures funding rate opportunities right now?"},
        "description": "Natural language query for spot-futures funding rate opportunities",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(FundingRateAgent, TEST_CASES))
