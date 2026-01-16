"""
ERC-8004 Configuration

Chain-specific registry addresses and R2 storage configuration.
"""

from typing import TypedDict


class ChainConfig(TypedDict):
    name: str
    rpc_env: str
    identity_registry: str | None
    reputation_registry: str | None


CHAIN_CONFIGS: dict[int, ChainConfig] = {
    11155111: {  # Ethereum Sepolia
        "name": "sepolia",
        "rpc_env": "SEPOLIA_RPC_URL",
        "identity_registry": "0x8004A818BFB912233c491871b3d84c89A494BD9e",
        "reputation_registry": "0x8004B663056A597Dffe9eCcC1965A193B7388713",
    },
    1: {  # Ethereum Mainnet
        "name": "mainnet",
        "rpc_env": "ETH_RPC_URL",
        "identity_registry": "0x106e3d8500B92A86D669702e75097E945C2e2B0e",
        "reputation_registry": "0x106e3d8500B92A86D669702e75097E945C2e2B0e",
    },
}

R2_CONFIG = {
    "bucket": "mesh",
    "base_url": "https://mesh-data.heurist.xyz",
    "folder": "erc8004",
}

CHAIN_NAME_TO_ID = {
    "sepolia": 11155111,
    "mainnet": 1,
}
