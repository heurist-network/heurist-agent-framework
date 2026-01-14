"""
ERC-8004 Agent Registry

Stores agent_id mappings in a JSON file, separate from agent source code.
This file is auto-updated when agents are registered and read by
update_mesh_metadata.py to merge into metadata.json.
"""

import json
from pathlib import Path

REGISTRY_FILE = Path(__file__).parent / "registered_agents.json"


def load_registry() -> dict:
    """Load the registered agents registry."""
    if not REGISTRY_FILE.exists():
        return {"sepolia": {}, "mainnet": {}}
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(registry: dict) -> None:
    """Save the registered agents registry."""
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")  # Trailing newline


def get_agent_id(agent_name: str, chain: str) -> str | None:
    """Get agent_id for a given agent name and chain.

    Args:
        agent_name: The agent's display name (e.g., "Token Resolver Agent")
        chain: Chain name ("sepolia" or "mainnet")

    Returns:
        Agent ID in format "chainId:tokenId" or None if not registered
    """
    registry = load_registry()
    return registry.get(chain, {}).get(agent_name)


def set_agent_id(agent_name: str, chain: str, agent_id: str) -> None:
    """Set agent_id for a given agent name and chain.

    Args:
        agent_name: The agent's display name
        chain: Chain name ("sepolia" or "mainnet")
        agent_id: Agent ID in format "chainId:tokenId"
    """
    registry = load_registry()
    if chain not in registry:
        registry[chain] = {}
    registry[chain][agent_name] = agent_id
    save_registry(registry)


def list_registered_agents(chain: str | None = None) -> dict:
    """List all registered agents, optionally filtered by chain.

    Args:
        chain: Optional chain name to filter by

    Returns:
        Dict of {chain: {agent_name: agent_id}}
    """
    registry = load_registry()
    if chain:
        return {chain: registry.get(chain, {})}
    return registry
