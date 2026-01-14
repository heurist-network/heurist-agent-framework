"""
ERC-8004 Registration File Builder

Converts Heurist Mesh agent metadata to ERC-8004 compliant registration format.
"""

import time
from typing import Any

from mesh.erc8004.config import CHAIN_CONFIGS


def get_mcp_endpoint(agent_name: str) -> str:
    return f"https://mesh.heurist.xyz/mcp/agents/{agent_name}"


def is_x402_enabled(metadata: dict[str, Any]) -> bool:
    return metadata.get("x402_config", {}).get("enabled", False)


def get_x402_endpoints(agent_name: str, tool_names: list[str]) -> dict[str, Any]:
    return {
        "version": "v1",
        "tools": {
            tool_name: {
                "base": f"https://mesh.heurist.xyz/x402/agents/{agent_name}/{tool_name}",
                "solana": f"https://mesh.heurist.xyz/x402/solana/agents/{agent_name}/{tool_name}",
            }
            for tool_name in tool_names
        },
    }


def build_endpoints(metadata: dict[str, Any], agent_class_name: str) -> list[dict[str, str]]:
    agent_name = agent_class_name
    endpoints = [
        {
            "name": "MCP",
            "endpoint": get_mcp_endpoint(agent_name),
            "version": "2025-06-18",
        }
    ]

    return endpoints


def get_supported_trust(metadata: dict[str, Any]) -> list[str]:
    erc8004_config = metadata.get("erc8004_config", {})
    return erc8004_config.get("supported_trust", ["reputation"])


def build_registration_file(
    metadata: dict[str, Any],
    chain_id: int,
    agent_class_name: str,
    tool_names: list[str],
) -> dict:
    """Convert MeshAgent metadata to ERC-8004 registration file format.

    Args:
        metadata: Agent metadata dict from MeshAgent
        chain_id: Target chain ID for registration

    Returns:
        ERC-8004 compliant registration file dict
    """
    agent_name = metadata["name"]
    endpoints = build_endpoints(metadata, agent_class_name)

    metadata_block: dict[str, Any] = {}
    if is_x402_enabled(metadata):
        metadata_block["x402Endpoints"] = get_x402_endpoints(agent_class_name, tool_names)

    # Build registration file
    registration = {
        "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
        "name": agent_name,
        "description": f"{metadata.get('description', '')} Created by Heurist Mesh.",
        "image": metadata.get("image_url"),
        "endpoints": endpoints,
        "registrations": [],  # Filled after minting
        "supportedTrust": get_supported_trust(metadata),
        "active": True,
        "x402support": is_x402_enabled(metadata),
        "updatedAt": int(time.time()),
    }
    if metadata_block:
        registration["metadata"] = metadata_block

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
