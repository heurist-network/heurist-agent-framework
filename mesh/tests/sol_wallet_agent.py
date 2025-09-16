import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.sol_wallet_agent import SolWalletAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "token_holders_query": {
        "input": {
            "query": "Give me the holders of this 4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump",
            "raw_data_only": False,
        },
        "description": "Natural language query for token holders",
    },
    "wallet_transactions_raw": {
        "input": {
            "query": "Show me the txs of this wallet DbDi7soBXALYRMZSyJMEAfpaK3rD1hr5HuCYzuDrcEEN",
            "raw_data_only": True,
        },
        "description": "Natural language query for wallet transactions with raw data flag",
    },
    "get_wallet_assets": {
        "input": {
            "tool": "get_wallet_assets",
            "tool_arguments": {"owner_address": "DbDi7soBXALYRMZSyJMEAfpaK3rD1hr5HuCYzuDrcEEN"},
        },
        "description": "Direct tool call to get wallet assets",
    },
    "get_tx_history": {
        "input": {
            "tool": "get_tx_history",
            "tool_arguments": {"owner_address": "DbDi7soBXALYRMZSyJMEAfpaK3rD1hr5HuCYzuDrcEEN"},
        },
        "description": "Direct tool call to get transaction history",
    },
    "analyze_common_holdings": {
        "input": {
            "tool": "analyze_common_holdings_of_top_holders",
            "tool_arguments": {"token_address": "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump"},
        },
        "description": "Direct tool call to analyze common holdings of top holders",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(SolWalletAgent, TEST_CASES))
