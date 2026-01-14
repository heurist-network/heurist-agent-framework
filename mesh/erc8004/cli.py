#!/usr/bin/env python
"""
ERC-8004 Agent Management CLI

Usage:
    uv run python -m mesh.erc8004.cli list                    # List eligible agents
    uv run python -m mesh.erc8004.cli sync --dry-run          # Preview sync
    uv run python -m mesh.erc8004.cli sync --chain sepolia    # Sync to Sepolia
    uv run python -m mesh.erc8004.cli sync --chain mainnet    # Sync to Mainnet
    uv run python -m mesh.erc8004.cli register <agent_name>   # Register single agent
    uv run python -m mesh.erc8004.cli update <agent_name>     # Update single agent
    uv run python -m mesh.erc8004.cli status <agent_name>     # Check agent status
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

from mesh.erc8004.config import CHAIN_NAME_TO_ID
from mesh.erc8004.manager import ERC8004Manager
from mesh.erc8004.r2_client import ERC8004R2Client
from mesh.erc8004.registry import get_agent_id


def cmd_list(args):
    """List all eligible agents."""
    chain_id = CHAIN_NAME_TO_ID[args.chain]
    manager = ERC8004Manager(chain_id=chain_id)
    agents = list(manager._iter_eligible_agents())

    if not agents:
        print("No eligible agents found (none have erc8004_config.enabled=True)")
        return

    print(f"\nEligible agents for ERC-8004 registration on {args.chain} ({len(agents)} total):\n")
    for agent_class_name, metadata, _ in agents:
        name = metadata["name"]
        agent_id = get_agent_id(agent_class_name, args.chain)
        status = "Registered" if agent_id else "Not registered"
        print(f"  - {name} ({agent_class_name})")
        print(f"      Status: {status}")
        if agent_id:
            print(f"      Agent ID: {agent_id}")
        print()


def cmd_sync(args):
    """Sync all eligible agents."""
    chain_id = CHAIN_NAME_TO_ID[args.chain]
    manager = ERC8004Manager(chain_id=chain_id)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Syncing agents to {args.chain} (chain {chain_id})...\n")

    results = manager.sync_all(dry_run=args.dry_run)

    if results["registered"]:
        print(f"Registered ({len(results['registered'])}):")
        for name in results["registered"]:
            print(f"  - {name}")
        print()

    if results["updated"]:
        print(f"Updated ({len(results['updated'])}):")
        for name in results["updated"]:
            print(f"  - {name}")
        print()

    if results["skipped"]:
        print(f"Skipped (no changes) ({len(results['skipped'])}):")
        for name in results["skipped"]:
            print(f"  - {name}")
        print()

    if results["errors"]:
        print(f"Errors ({len(results['errors'])}):")
        for err in results["errors"]:
            print(f"  - {err['agent']}: {err['error']}")
        print()

    # Summary
    print("Summary:")
    print(f"  Registered: {len(results['registered'])}")
    print(f"  Updated: {len(results['updated'])}")
    print(f"  Skipped: {len(results['skipped'])}")
    print(f"  Errors: {len(results['errors'])}")


def cmd_register(args):
    """Register a single agent."""
    chain_id = CHAIN_NAME_TO_ID[args.chain]
    manager = ERC8004Manager(chain_id=chain_id)

    result = manager.get_agent_by_name(args.agent_name)
    if not result:
        print(f"Agent '{args.agent_name}' not found or not eligible (erc8004_config.enabled != True)")
        sys.exit(1)
    agent_class_name, metadata, tool_names = result

    agent_id = get_agent_id(agent_class_name, args.chain)
    if agent_id:
        print(f"Agent '{agent_class_name}' is already registered with ID: {agent_id}")
        print("Use 'update' command to update an existing agent.")
        sys.exit(1)

    print(f"Registering {args.agent_name} on {args.chain}...")
    agent_id = manager.register_agent(metadata, agent_class_name, tool_names)
    print(f"\nSuccess! Agent registered with ID: {agent_id}")


def cmd_update(args):
    """Update a single agent."""
    chain_id = CHAIN_NAME_TO_ID[args.chain]
    manager = ERC8004Manager(chain_id=chain_id)

    result = manager.get_agent_by_name(args.agent_name)
    if not result:
        print(f"Agent '{args.agent_name}' not found or not eligible")
        sys.exit(1)
    agent_class_name, metadata, tool_names = result

    agent_id = get_agent_id(agent_class_name, args.chain)
    if not agent_id:
        print(f"Agent '{agent_class_name}' is not registered yet.")
        print("Use 'register' command first.")
        sys.exit(1)

    print(f"Updating {args.agent_name} on {args.chain}...")
    agent_id, was_updated = manager.update_agent(metadata, agent_class_name, tool_names)

    if was_updated:
        print(f"Success! Agent {agent_id} updated.")
    else:
        print(f"No changes detected for agent {agent_id}.")


def cmd_status(args):
    """Check agent status."""
    r2_client = ERC8004R2Client()

    agent_key = args.agent_name
    try:
        from mesh.mesh_manager import AgentLoader, Config

        loader = AgentLoader(Config())
        for agent_class in loader.load_agents().values():
            agent = agent_class()
            if agent.agent_name == args.agent_name:
                agent_key = agent.agent_name
                break
            if agent.metadata.get("name") == args.agent_name:
                agent_key = agent.agent_name
                break
    except Exception:
        pass

    # Check R2
    registration = r2_client.get_registration(agent_key)
    if registration:
        print(f"\nR2 Registration for {args.agent_name}:")
        print(json.dumps(registration, indent=2))
    else:
        print(f"\nNo R2 registration found for {args.agent_name}")


def main():
    parser = argparse.ArgumentParser(
        description="ERC-8004 Agent Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    list_parser = subparsers.add_parser("list", help="List eligible agents")
    list_parser.add_argument("--chain", choices=["sepolia", "mainnet"], default="sepolia")

    # sync command
    sync_parser = subparsers.add_parser("sync", help="Sync all agents")
    sync_parser.add_argument("--chain", choices=["sepolia", "mainnet"], default="sepolia")
    sync_parser.add_argument("--dry-run", action="store_true", help="Preview changes without making them")

    # register command
    reg_parser = subparsers.add_parser("register", help="Register single agent")
    reg_parser.add_argument("agent_name", help="Class or display name of the agent to register")
    reg_parser.add_argument("--chain", choices=["sepolia", "mainnet"], default="sepolia")

    # update command
    upd_parser = subparsers.add_parser("update", help="Update single agent")
    upd_parser.add_argument("agent_name", help="Class or display name of the agent to update")
    upd_parser.add_argument("--chain", choices=["sepolia", "mainnet"], default="sepolia")

    # status command
    status_parser = subparsers.add_parser("status", help="Check agent status")
    status_parser.add_argument("agent_name", help="Class or display name of the agent to check")

    args = parser.parse_args()

    # Route to command handler
    if args.command == "list":
        cmd_list(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "register":
        cmd_register(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
