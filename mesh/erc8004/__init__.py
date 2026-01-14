"""
ERC-8004 Agent Identity Registration Module

This module provides tools to register Heurist Mesh agents on-chain using the ERC-8004 protocol.
"""

from mesh.erc8004.config import CHAIN_CONFIGS, R2_CONFIG
from mesh.erc8004.manager import ERC8004Manager
from mesh.erc8004.r2_client import ERC8004R2Client
from mesh.erc8004.registration import build_registration_file
from mesh.erc8004.registry import get_agent_id, list_registered_agents, load_registry, set_agent_id

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
