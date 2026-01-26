"""
ERC-8004 Agent Manager

Main orchestrator for registering and updating Heurist Mesh agents on-chain.
"""

import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger

# Add agent0-py to path
agent0_path = Path(__file__).parent.parent.parent.parent / "agent0-py"
if agent0_path.exists():
    sys.path.insert(0, str(agent0_path))

from agent0_sdk import SDK

from mesh.erc8004.config import CHAIN_CONFIGS
from mesh.erc8004.r2_client import ERC8004R2Client
from mesh.erc8004.registration import (
    add_registration_info,
    build_registration_file,
    get_mcp_endpoint,
    get_supported_trust,
    is_x402_enabled,
)


class ERC8004Manager:
    def __init__(self, chain_id: int = 11155111):
        """Initialize ERC-8004 manager.

        Args:
            chain_id: Target chain ID (default: Sepolia 11155111)
        """
        self.chain_id = chain_id
        self.config = CHAIN_CONFIGS.get(chain_id)

        if not self.config:
            raise ValueError(f"Unsupported chain ID: {chain_id}")

        if not self.config["identity_registry"]:
            raise ValueError(f"Identity registry not configured for chain {chain_id}")

        self.r2_client = ERC8004R2Client()

        # Initialize agent0 SDK
        rpc_url = os.getenv(self.config["rpc_env"])
        private_key = os.getenv("ERC8004_PRIVATE_KEY")

        if not rpc_url:
            raise ValueError(f"RPC URL not set: {self.config['rpc_env']}")
        if not private_key:
            raise ValueError("ERC8004_PRIVATE_KEY not set")

        # Pass registry addresses from our config to SDK
        registry_overrides = {}
        if self.config["identity_registry"] or self.config["reputation_registry"]:
            registry_overrides[chain_id] = {}
            if self.config["identity_registry"]:
                registry_overrides[chain_id]["IDENTITY"] = self.config["identity_registry"]
            if self.config["reputation_registry"]:
                registry_overrides[chain_id]["REPUTATION"] = self.config["reputation_registry"]

        self.sdk = SDK(
            chainId=chain_id,
            rpcUrl=rpc_url,
            signer=private_key,
            registryOverrides=registry_overrides,
        )

    def _iter_eligible_agents(self) -> list[tuple[str, dict[str, Any], list[str]]]:
        """Load all agents with erc8004.enabled=True.

        Returns list of (agent_class_name, metadata, tool_names) tuples.
        """
        from mesh.mesh_manager import AgentLoader, Config

        config = Config()
        loader = AgentLoader(config)
        all_agents = loader.load_agents()

        eligible = []
        for agent_class in all_agents.values():
            agent = agent_class()
            metadata = agent.metadata
            tool_schemas = agent.get_tool_schemas() or []
            tool_names = [
                tool.get("function", {}).get("name")
                for tool in tool_schemas
                if tool.get("function", {}).get("name")
            ]
            erc8004 = metadata.get("erc8004", {})

            if erc8004.get("enabled"):
                eligible.append((agent.agent_name, metadata, tool_names))

        return eligible

    def get_eligible_agents(self) -> list[dict[str, Any]]:
        """Load all agents with erc8004.enabled=True.

        Returns list of agent metadata dicts.
        """
        return [metadata for _, metadata, _ in self._iter_eligible_agents()]

    def register_agent(self, metadata: dict[str, Any], agent_class_name: str, tool_names: list[str]) -> str:
        """Register new agent on-chain.

        Args:
            metadata: Agent metadata dict

        Returns:
            Agent ID in format "chainId:tokenId"
        """
        agent_name = metadata["name"]
        logger.info(f"Registering agent: {agent_name}")

        # Build registration file
        reg_data = build_registration_file(metadata, self.chain_id, agent_class_name, tool_names)

        # Upload to R2 first (without registrations array)
        reg_url = self.r2_client.upload_registration(agent_class_name, reg_data)

        # Create agent via SDK
        agent = self.sdk.createAgent(
            name=agent_name,
            description=reg_data["description"],
            image=metadata.get("image_url"),
        )

        # Set MCP endpoint
        mcp_url = get_mcp_endpoint(agent_class_name)
        agent.setMCP(mcp_url, auto_fetch=False)

        # Set trust models
        supported_trust = get_supported_trust(metadata)
        agent.setTrust(
            reputation="reputation" in supported_trust,
            cryptoEconomic="crypto-economic" in supported_trust,
            teeAttestation="tee-attestation" in supported_trust,
        )

        # Set x402 support
        x402_enabled = is_x402_enabled(metadata)
        agent.setX402Support(x402_enabled)
        agent.setActive(True)

        # Set custom metadata
        agent.setMetadata(
            {
                "meshAgentId": agent_name,
                "source": "Heurist Mesh",
                "version": metadata.get("version", "1.0.0"),
            }
        )

        # Register on-chain with HTTP URL
        tx_handle = agent.register(reg_url)
        tx_handle.wait_confirmed(timeout=180)
        agent_id = agent.agentId

        logger.info(f"Registered agent {agent_name} with ID: {agent_id}")

        # Update R2 file with registration info
        reg_data = add_registration_info(reg_data, agent_id, self.chain_id)
        self.r2_client.upload_registration(agent_class_name, reg_data)

        # Save to registry file (auto-tracks agent_id)
        from mesh.erc8004.registry import set_agent_id

        chain_name = self.config["name"]
        set_agent_id(agent_class_name, chain_name, agent_id)
        logger.info(f"Saved {agent_class_name} to registry: {chain_name} -> {agent_id}")

        return agent_id

    def update_agent(self, metadata: dict[str, Any], agent_class_name: str, tool_names: list[str]) -> tuple[str, bool]:
        """Update existing agent registration if changed.

        Args:
            metadata: Agent metadata dict

        Returns:
            Tuple of (agent_id, was_updated) - was_updated is False if no changes detected
        """
        from mesh.erc8004.registry import get_agent_id

        chain_name = self.config["name"]
        agent_id = get_agent_id(agent_class_name, chain_name)

        if not agent_id:
            raise ValueError(f"Agent {agent_class_name} not in registry for {chain_name}")

        agent_name = metadata["name"]

        # Build new registration data
        reg_data = build_registration_file(metadata, self.chain_id, agent_class_name, tool_names)
        reg_data = add_registration_info(reg_data, agent_id, self.chain_id)

        # Read existing registration from R2 to compare
        existing = self.r2_client.get_registration(agent_class_name)
        if existing and self._is_registration_equal(existing, reg_data):
            logger.info(f"Agent {agent_name} unchanged, skipping update")
            return agent_id, False

        logger.info(f"Updating agent: {agent_name}")

        # Upload updated registration to R2
        reg_url = self.r2_client.upload_registration(agent_class_name, reg_data)

        # Load and update on-chain
        agent = self.sdk.loadAgent(agent_id)
        agent.updateInfo(
            name=agent_name,
            description=reg_data["description"],
            image=metadata.get("image_url"),
        )
        supported_trust = get_supported_trust(metadata)
        agent.setTrust(
            reputation="reputation" in supported_trust,
            cryptoEconomic="crypto-economic" in supported_trust,
            teeAttestation="tee-attestation" in supported_trust,
        )
        agent.setX402Support(is_x402_enabled(metadata))
        tx_handle = agent.register(reg_url)
        tx_handle.wait_confirmed(timeout=180)

        logger.info(f"Updated agent {agent_name}")
        return agent_id, True

    def _is_registration_equal(self, existing: dict, new: dict) -> bool:
        """Compare registration files, ignoring updatedAt timestamp."""
        compare_fields = [
            "name",
            "description",
            "image",
            "services",
            "supportedTrust",
            "active",
            "x402Support",
            "metadata",
        ]
        for field in compare_fields:
            if existing.get(field) != new.get(field):
                return False
        return True

    def sync_all(self, dry_run: bool = False) -> dict:
        """Sync all eligible agents: register new, update existing, skip unchanged.

        Args:
            dry_run: If True, don't make any changes

        Returns:
            Dict with keys: registered, updated, skipped, errors
        """
        from mesh.erc8004.registry import get_agent_id

        results: dict[str, list] = {"registered": [], "updated": [], "skipped": [], "errors": []}
        chain_name = self.config["name"]

        for agent_class_name, metadata, tool_names in self._iter_eligible_agents():
            agent_name = metadata["name"]
            agent_id = get_agent_id(agent_class_name, chain_name)

            try:
                if agent_id:
                    # Check for updates
                    if dry_run:
                        # In dry-run, check if would update
                        reg_data = build_registration_file(metadata, self.chain_id, agent_class_name, tool_names)
                        existing = self.r2_client.get_registration(agent_class_name)
                        if existing and self._is_registration_equal(existing, reg_data):
                            results["skipped"].append(agent_name)
                        else:
                            results["updated"].append(agent_name)
                    else:
                        _, was_updated = self.update_agent(metadata, agent_class_name, tool_names)
                        if was_updated:
                            results["updated"].append(agent_name)
                        else:
                            results["skipped"].append(agent_name)
                else:
                    # Register new (auto-saves to registry)
                    if dry_run:
                        results["registered"].append(agent_name)
                    else:
                        self.register_agent(metadata, agent_class_name, tool_names)
                        results["registered"].append(agent_name)
            except Exception as ex:
                logger.error(f"Error processing {agent_name}: {ex}")
                results["errors"].append({"agent": agent_name, "error": str(ex)})

        return results

    def get_agent_by_name(self, agent_name: str) -> tuple[str, dict[str, Any], list[str]] | None:
        """Get (agent_class_name, metadata, tool_names) by class or display name."""
        for agent_class_name, metadata, tool_names in self._iter_eligible_agents():
            if agent_class_name == agent_name or metadata["name"] == agent_name:
                return agent_class_name, metadata, tool_names
        return None
