"""Test suite for Chainbase Address Label Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.chainbase_address_label_agent import ChainbaseAddressLabelAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "vitalik_address": {
        "input": {"query": "Get labels for address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"},
        "description": "Get labels for Vitalik's address (should resolve to vitalik.eth)",
    },
    "jesse_base_address": {
        "input": {"query": "What is the owner of 0x2211d1D0020DAEA8039E46Cf1367962070d77DA9?"},
        "description": "Get labels for Jesse's address (should resolve to jesse.base.eth)",
    },
    "uniswap_token_contract": {
        "input": {"query": "Get information about 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"},
        "description": "Get labels for Uniswap (UNI) token contract",
    },
    "uniswap_v2_router": {
        "input": {"query": "Get labels for 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"},
        "description": "Get labels for Uniswap V2 Router contract",
    },
    "opensea_seaport": {
        "input": {"query": "Get labels for 0x00000000000000ADc04C56Bf30aC9d3c0aAF14dC"},
        "description": "Get labels for OpenSea Seaport contract",
    },
    "binance_hot_wallet": {
        "input": {"query": "Get labels for 0x28C6c06298d514Db089934071355E5743bf21d60"},
        "description": "Get labels for Binance hot wallet",
    },
    "usdt_contract": {
        "input": {"query": "Get labels for 0xdAC17F958D2ee523a2206206994597C13D831ec7"},
        "description": "Get labels for USDT token contract",
    },
    "random_eoa": {
        "input": {"query": "Get labels for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"},
        "description": "Get labels for a random EOA address",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ChainbaseAddressLabelAgent, TEST_CASES))
