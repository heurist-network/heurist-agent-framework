import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.pumpfun_token_agent import PumpFunTokenAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "token_creation": {
        "input": {"query": "Show me the latest Solana token creations in the last hour"},
        "description": "Natural language query for latest token creations in last hour",
    },
    "graduated_tokens": {
        "input": {"query": "Show me all tokens that have graduated on Pump.fun in the last 48 hours"},
        "description": "Natural language query for tokens that graduated in last 48 hours",
    },
    "graduated_tokens_direct": {
        "input": {
            "tool": "query_latest_graduated_tokens",
            "tool_arguments": {"timeframe": 24},
            "raw_data_only": True,
        },
        "description": "Direct tool call for graduated tokens with 24 hour timeframe",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(PumpFunTokenAgent, TEST_CASES))
