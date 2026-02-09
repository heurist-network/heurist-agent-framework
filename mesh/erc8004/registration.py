"""
ERC-8004 Registration File Builder

Converts Heurist Mesh agent metadata to ERC-8004 compliant registration format.
"""

import time
from typing import Any

from mesh.erc8004.config import CHAIN_CONFIGS

BASE_URL = "https://mesh.heurist.xyz"


def get_mcp_endpoint(agent_name: str) -> str:
    return f"{BASE_URL}/mcp/agents/{agent_name}/sse"


def is_x402_enabled(metadata: dict[str, Any]) -> bool:
    return metadata.get("x402_config", {}).get("enabled", False)


def get_supported_trust(metadata: dict[str, Any]) -> list[str]:
    return metadata.get("erc8004", {}).get("supported_trust", ["reputation"])


def build_registration_file(
    metadata: dict[str, Any],
    chain_id: int,
    agent_class_name: str,
    tool_names: list[str],
) -> dict:
    """Convert MeshAgent metadata to ERC-8004 registration file format."""
    x402_enabled = is_x402_enabled(metadata)

    registration: dict[str, Any] = {
        "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
        "name": metadata["name"],
        "description": f"{metadata.get('description', '')} Created by Heurist Mesh.",
        "image": metadata.get("image_url"),
        "services": [{"name": "MCP", "endpoint": get_mcp_endpoint(agent_class_name), "version": "2025-06-18"}],
        "registrations": [],
        "supportedTrust": get_supported_trust(metadata),
        "active": True,
        "x402Support": x402_enabled,
        "updatedAt": int(time.time()),
    }

    if x402_enabled and tool_names:
        registration["metadata"] = {
            "x402Endpoints": {
                "version": "v1",
                "tools": {
                    name: {
                        "base": f"{BASE_URL}/x402/agents/{agent_class_name}/{name}",
                        "solana": f"{BASE_URL}/x402/solana/agents/{agent_class_name}/{name}",
                    }
                    for name in tool_names
                },
            }
        }

    return registration


def add_registration_info(registration: dict, agent_id: str, chain_id: int) -> dict:
    """Add on-chain registration info to registration file.

    Args:
        registration: Registration file dict
        agent_id: Agent ID in format "chainId:tokenId"
        chain_id: Chain ID

    Returns:
        Updated registration file with registrations array populated
    """
    config = CHAIN_CONFIGS.get(chain_id)
    if not config or not config["identity_registry"]:
        raise ValueError(f"No identity registry configured for chain {chain_id}")

    token_id = int(agent_id.split(":")[-1])
    registry_address = config["identity_registry"]

    registration["registrations"] = [
        {
            "agentId": token_id,
            "agentRegistry": f"eip155:{chain_id}:{registry_address}",
        }
    ]

    return registration
