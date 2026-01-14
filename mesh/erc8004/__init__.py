"""
ERC-8004 Agent Identity Registration Module

This module provides tools to register Heurist Mesh agents on-chain using the ERC-8004 protocol.
"""

# Light imports only - no heavy dependencies
from mesh.erc8004.config import CHAIN_CONFIGS, R2_CONFIG
from mesh.erc8004.registry import get_agent_id, list_registered_agents, load_registry, set_agent_id


def __getattr__(name: str):
    """Lazy import heavy modules only when accessed."""
    if name == "ERC8004Manager":
        from mesh.erc8004.manager import ERC8004Manager

        return ERC8004Manager
    if name == "ERC8004R2Client":
        from mesh.erc8004.r2_client import ERC8004R2Client

        return ERC8004R2Client
    if name == "build_registration_file":
        from mesh.erc8004.registration import build_registration_file

        return build_registration_file
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "CHAIN_CONFIGS",
    "R2_CONFIG",
    "ERC8004Manager",
    "ERC8004R2Client",
    "build_registration_file",
    "load_registry",
    "get_agent_id",
    "set_agent_id",
    "list_registered_agents",
]
