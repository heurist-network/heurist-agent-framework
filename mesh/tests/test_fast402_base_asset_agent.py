"""
Test script untuk Fast402BaseAssetAgent
Jalankan dengan: python mesh/tests/test_fast402_base_asset_agent.py
"""

import asyncio
import yaml
from mesh.agents.fast402_base_asset_agent import Fast402BaseAssetAgent


async def test():
    agent = Fast402BaseAssetAgent()

    print("=" * 60)
    print("TEST 1: Check ETH balance (wallet only)")
    print("=" * 60)
    result = await agent.handle_message({
        "tool": "check_base_assets",
        "tool_arguments": {
            "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",  # vitalik.eth
        },
    })
    print(yaml.dump(result, default_flow_style=False))

    print("=" * 60)
    print("TEST 2: Check ETH balance + LP reserves")
    print("=" * 60)
    result2 = await agent.handle_message({
        "tool": "check_base_assets",
        "tool_arguments": {
            "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            "pool_address": "0x7f670f78B17dEC44d5Ef68a48740b6f8849cc2e6",  # Aerodrome pool
        },
    })
    print(yaml.dump(result2, default_flow_style=False))

    print("=" * 60)
    print("TEST 3: Invalid wallet address (error handling)")
    print("=" * 60)
    result3 = await agent.handle_message({
        "tool": "check_base_assets",
        "tool_arguments": {
            "wallet_address": "invalid_address",
        },
    })
    print(yaml.dump(result3, default_flow_style=False))


if __name__ == "__main__":
    asyncio.run(test())
