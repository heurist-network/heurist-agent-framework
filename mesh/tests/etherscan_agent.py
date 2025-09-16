# test_etherscan_agent.py
"""Test suite for Etherscan Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.etherscan_agent import EtherscanAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "natural_language_transaction": {
        "input": {
            "query": "analyze transaction pattern of https://etherscan.io/address/0x2B25B37c683F042E9Ae1877bc59A1Bb642Eb1073",
            "raw_data_only": False,
        },
        "description": "Natural language query for transaction analysis from Etherscan URL",
    },
    "direct_transaction_call": {
        "input": {
            "tool": "get_transaction_details",
            "tool_arguments": {
                "chain": "ethereum",
                "txid": "0xd8a484a402a4373221288fed84e9025ed48eba2a45a7294c19289f740ca00fcd",
            },
        },
        "description": "Direct tool call for transaction details on Ethereum",
    },
    "natural_language_address": {
        "input": {
            "query": "Get address history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 on ethereum",
            "raw_data_only": False,
        },
        "description": "Natural language query for Ethereum address history",
    },
    "direct_address_call": {
        "input": {
            "tool": "get_address_history",
            "tool_arguments": {"chain": "base", "address": "0x742d35Cc6639C0532fEa3BcdE3524A0be79C3b7B"},
        },
        "description": "Direct tool call for address history on Base chain",
    },
    "natural_language_token_transfers": {
        "input": {
            "query": "Show recent token transfers for 0x55d398326f99059ff775485246999027b3197955 on BSC",
            "raw_data_only": False,
        },
        "description": "Natural language query for token transfers on BSC",
    },
    "direct_token_transfers_call": {
        "input": {
            "tool": "get_erc20_token_transfers",
            "tool_arguments": {"chain": "bsc", "address": "0x55d398326f99059ff775485246999027b3197955"},
        },
        "description": "Direct tool call for ERC20 token transfers on BSC",
    },
    "natural_language_token_holders": {
        "input": {
            "query": "Get top holders for token 0xEF22cb48B8483dF6152e1423b19dF5553BbD818b on Base",
            "raw_data_only": False,
        },
        "description": "Natural language query for top token holders on Base",
    },
    "direct_token_holders_call": {
        "input": {
            "tool": "get_erc20_top_holders",
            "tool_arguments": {"chain": "base", "address": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b"},
        },
        "description": "Direct tool call for ERC20 top holders on Base",
    },
    "raw_data_only": {
        "input": {
            "query": "Analyze transaction 0xabc123 on Arbitrum",
            "raw_data_only": True,
        },
        "description": "Raw data mode test with transaction query on Arbitrum",
    },
    "error_handling": {
        "input": {
            "tool": "get_transaction_details",
            "tool_arguments": {"chain": "unsupported_chain", "txid": "0x123"},
        },
        "description": "Error handling test with unsupported chain",
    },
    "combined_query": {
        "input": {
            "query": "Show me both the transfers and top holders for USDT 0x55d398326f99059ff775485246999027b3197955 on BSC",
            "raw_data_only": False,
        },
        "description": "Combined natural language query for transfers and holders",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(EtherscanAgent, TEST_CASES))
