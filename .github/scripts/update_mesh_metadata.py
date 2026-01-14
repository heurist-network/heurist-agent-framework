#!/usr/bin/env python3
import argparse
import ast
import copy
import json
import logging
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import boto3  # type: ignore since it's only for github actions
import requests
from dotenv import load_dotenv

from mesh.erc8004.registry import load_registry

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# this is to get the base agent metadata structure, from mesh/mesh_agent.py
# we don't directly import it because we don't want to load all the dependencies
# of the mesh_agent.py file just to extract its metadata
def _convert_ast_node_to_python(node, default_model_id=None):
    """Helper to convert various AST nodes to Python equivalents."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.List):
        # pass default_model_id down recursively
        return [_convert_ast_node_to_python(item, default_model_id) for item in node.elts]
    elif isinstance(node, ast.Dict):
        # pass default_model_id down recursively
        return _convert_ast_dict_to_python_dict(node, default_model_id)
    elif isinstance(node, ast.Name):
        if node.id == "DEFAULT_MODEL_ID" and default_model_id is not None:
            return default_model_id
        else:
            log.warning(f"Skipping unsupported ast.Name: {node.id}")
            return f"UNSUPPORTED_AST_NAME_{node.id}"
    elif isinstance(node, ast.Attribute):
        # handle self.agent_name specifically as a placeholder
        if isinstance(node.value, ast.Name) and node.value.id == "self" and node.attr == "agent_name":
            return ""  # placeholder, will be overwritten by actual agent name later
        else:
            log.warning(f"Skipping unsupported ast.Attribute: {ast.dump(node)}")
            return "UNSUPPORTED_AST_ATTRIBUTE"
    else:
        log.warning(f"Skipping unsupported node type during conversion: {type(node)}")
        return f"UNSUPPORTED_AST_NODE_{type(node).__name__}"


def _convert_ast_dict_to_python_dict(node: ast.Dict, default_model_id=None) -> dict:
    """Converts an ast.Dict node to a Python dictionary."""
    result = {}
    for k, v in zip(node.keys, node.values):
        key = None
        if isinstance(k, ast.Constant):
            key = k.value
        else:
            log.warning(f"Skipping non-constant key in base metadata dict: {type(k)}")
            continue

        # pass default_model_id down
        result[key] = _convert_ast_node_to_python(v, default_model_id)
    return result


def extract_base_metadata(mesh_agent_path: Path) -> dict:
    """Extracts the base self.metadata dict from MeshAgent.__init__ using AST."""
    default_model_id = None
    base_metadata_dict = {}

    try:
        with open(mesh_agent_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        # first pass: find default_model_id at module level
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == "DEFAULT_MODEL_ID":
                    if isinstance(node.value, ast.Constant):
                        default_model_id = node.value.value
                        break
                    else:
                        log.warning("DEFAULT_MODEL_ID assignment is not a simple constant.")
                        break

        # second pass: find meshagent class and extract metadata
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "MeshAgent":
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                        for stmt in item.body:
                            # look for self.metadata = { ... } or self.metadata: type = { ... }
                            is_assign = isinstance(stmt, ast.Assign)
                            is_annassign = isinstance(stmt, ast.AnnAssign)

                            target = None
                            value = None
                            if is_assign and len(stmt.targets) == 1:
                                target = stmt.targets[0]
                                value = stmt.value
                            elif is_annassign:
                                target = stmt.target
                                value = stmt.value

                            # check if we found an assignment and if it's self.metadata = {dict}
                            if (
                                target is not None
                                and value is not None
                                and isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id == "self"
                                and target.attr == "metadata"
                                and isinstance(value, ast.Dict)
                            ):
                                # pass the found default_model_id to the converter
                                base_metadata_dict = _convert_ast_dict_to_python_dict(value, default_model_id)
                                break  # found metadata, exit inner loops
                        if base_metadata_dict:
                            break  # found metadata, exit outer loop
                if base_metadata_dict:
                    break  # found metadata, exit class search

        if not base_metadata_dict:
            log.error(
                f"Could not find 'self.metadata = {{...}}' or 'self.metadata: type = {{...}}' assignment in {mesh_agent_path}"
            )

        return base_metadata_dict

    except FileNotFoundError:
        log.error(f"Mesh agent file not found at: {mesh_agent_path}")
        return {}
    except Exception as e:
        log.error(f"Error parsing {mesh_agent_path} for base metadata: {e}")
        return {}


class AgentMetadataExtractor(ast.NodeVisitor):
    """
    Extract metadata from agent class definitions using AST

    This is because the old approach of importing the agent class and calling its metadata
    attribute is not feasible since we would have to install all the dependencies of the agent
    just to extract its metadata.
    """

    def __init__(self):
        self.metadata = {}
        self.current_class = None
        self.found_tools = []

    def visit_ClassDef(self, node):
        # Only look at classes that end with 'Agent'
        if node.name.endswith("Agent") and node.name != "MeshAgent":
            self.current_class = node.name
            self.metadata[node.name] = {"metadata": {}, "tools": []}
            self.generic_visit(node)
            self.current_class = None

    def visit_Call(self, node):
        if not self.current_class:
            return

        # Look for self.metadata.update() calls
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Attribute)
            and isinstance(node.func.value.value, ast.Name)
            and node.func.value.value.id == "self"
            and node.func.value.attr == "metadata"
            and node.func.attr == "update"
        ):
            # Extract the dictionary from the update call
            if node.args and isinstance(node.args[0], ast.Dict):
                metadata = self._extract_dict(node.args[0])
                self.metadata[self.current_class]["metadata"].update(metadata)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not self.current_class:
            return

        if node.name == "get_tool_schemas":
            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    if isinstance(child.value, ast.List):
                        tools = []
                        for elt in child.value.elts:
                            if isinstance(elt, ast.Dict):
                                tool = self._extract_dict(elt)
                                tools.append(tool)
                        self.metadata[self.current_class]["tools"] = tools

        self.generic_visit(node)

    def _extract_dict(self, node: ast.Dict) -> dict:
        result = {}
        for k, v in zip(node.keys, node.values):
            if not isinstance(k, ast.Constant):
                continue
            key = k.value
            if isinstance(v, ast.Constant):
                result[key] = v.value
            elif isinstance(v, ast.List):
                result[key] = [
                    self._extract_dict(item)
                    if isinstance(item, ast.Dict)
                    else item.value
                    if isinstance(item, ast.Constant)
                    else None
                    for item in v.elts
                ]
            elif isinstance(v, ast.Dict):
                result[key] = self._extract_dict(v)
        return result


def merge_erc8004_agent_ids(agents_dict: Dict[str, dict]) -> Dict[str, dict]:
    """Merge agent_id from registry into erc8004_config.

    Reads mesh/erc8004/registered_agents.json and adds agent_ids to each
    agent's erc8004_config in the format:
    {
        "erc8004_config": {
            "enabled": true,
            "agent_ids": {"sepolia": "11155111:42", "mainnet": "1:123"}
        }
    }
    """
    try:
        registry = load_registry()
    except Exception as e:
        log.warning(f"Failed to load ERC-8004 registry: {e}")
        return agents_dict

    # Build name -> agent_ids mapping from registry
    agent_ids_by_name: Dict[str, Dict[str, str]] = {}
    for chain_name, chain_agents in registry.items():
        for agent_name, agent_id in chain_agents.items():
            if agent_name not in agent_ids_by_name:
                agent_ids_by_name[agent_name] = {}
            agent_ids_by_name[agent_name][chain_name] = agent_id

    # Merge into agents_dict (registry uses class names as keys)
    for agent_class, agent_data in agents_dict.items():
        erc8004 = agent_data["metadata"].get("erc8004_config")
        if erc8004 and agent_class in agent_ids_by_name:
            erc8004["agent_ids"] = agent_ids_by_name[agent_class]

    return agents_dict


def merge_erc8004_registration_data(agents_dict: Dict[str, dict]) -> Dict[str, dict]:
    """Fetch ERC-8004 registration data from R2 and add to metadata."""
    try:
        from mesh.erc8004.r2_client import ERC8004R2Client

        r2_client = ERC8004R2Client()
    except Exception as e:
        log.warning(f"Failed to initialize ERC8004 R2 client: {e}")
        return agents_dict

    for agent_class, agent_data in agents_dict.items():
        metadata = agent_data["metadata"]
        erc8004_config = metadata.get("erc8004_config", {})
        if not erc8004_config.get("agent_ids"):
            continue

        try:
            registration = r2_client.get_registration(agent_class)
            if registration:
                metadata["erc8004"] = {
                    "registrations": registration.get("registrations", []),
                    "supportedTrust": registration.get("supportedTrust", []),
                    "active": registration.get("active", False),
                    "registrationUrl": f"https://mesh-data.heurist.xyz/erc8004/{agent_class}.json",
                }
        except Exception as e:
            log.warning(f"Failed to fetch ERC-8004 registration for {agent_class}: {e}")

    return agents_dict


class MetadataManager:
    def __init__(self):
        # Only initialize S3 client if all required env vars are present
        if all(k in os.environ for k in ["S3_ENDPOINT", "S3_ACCESS_KEY", "S3_SECRET_KEY"]):
            self.s3_client = boto3.client(
                "s3",
                endpoint_url=os.environ["S3_ENDPOINT"],
                aws_access_key_id=os.environ["S3_ACCESS_KEY"],
                aws_secret_access_key=os.environ["S3_SECRET_KEY"],
                region_name="enam",
            )
        else:
            self.s3_client = None
            log.info("S3 credentials not found, skipping metadata upload")

        mesh_agent_file = Path("mesh/mesh_agent.py").resolve()
        self.base_metadata = extract_base_metadata(mesh_agent_file)
        if not self.base_metadata:
            raise ValueError("Failed to extract base metadata")

    def fetch_existing_metadata(self) -> Dict:
        try:
            response = requests.get("https://mesh.heurist.ai/metadata.json")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.warning(f"Failed to fetch existing metadata: {e}")
            return {"agents": {}}

    def load_agents(self) -> Dict[str, dict]:
        mesh_dir = Path("mesh/agents")
        if not mesh_dir.exists():
            log.error("Mesh directory not found")
            return {}

        agents_dict = {}
        for file_path in mesh_dir.glob("*_agent.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                extractor = AgentMetadataExtractor()
                extractor.visit(tree)

                for agent_id, data in extractor.metadata.items():
                    if "EchoAgent" in agent_id:
                        continue

                    agent_base_meta = copy.deepcopy(self.base_metadata)
                    agent_data = {
                        "metadata": {**agent_base_meta, **(data.get("metadata", {}))},
                        "module": file_path.stem,
                        "tools": data.get("tools", []),
                    }

                    if agent_data["tools"]:
                        tool_names = ", ".join(t["function"]["name"] for t in agent_data["tools"])
                        if isinstance(agent_data["metadata"].get("inputs"), list):
                            agent_data["metadata"]["inputs"].extend(
                                [
                                    {
                                        "name": "tool",
                                        "description": f"Directly specify which tool to call: {tool_names}. Bypasses LLM.",
                                        "type": "str",
                                        "required": False,
                                    },
                                    {
                                        "name": "tool_arguments",
                                        "description": "Arguments for the tool call as a dictionary",
                                        "type": "dict",
                                        "required": False,
                                        "default": {},
                                    },
                                ]
                            )

                    agents_dict[agent_id] = agent_data

            except Exception as e:
                log.warning(f"Error parsing {file_path}: {e}")

        log.info(f"Found {len(agents_dict)} agents" if agents_dict else "No agents found")
        return agents_dict

    def create_metadata(self, agents_dict: Dict[str, dict]) -> Dict:
        existing_metadata = self.fetch_existing_metadata()
        existing_agents = existing_metadata.get("agents", {})

        # preserve total_calls and greeting_message for each agent
        # these are added by a separate AWS cronjob, so preserve them
        for agent_id, agent_data in agents_dict.items():
            if agent_id in existing_agents:
                existing_agent = existing_agents[agent_id]
                if "total_calls" in existing_agent.get("metadata", {}):
                    agent_data["metadata"]["total_calls"] = existing_agent["metadata"]["total_calls"]
                if "greeting_message" in existing_agent.get("metadata", {}):
                    agent_data["metadata"]["greeting_message"] = existing_agent["metadata"]["greeting_message"]

        # Merge ERC-8004 agent_ids from registry into metadata
        agents_dict = merge_erc8004_agent_ids(agents_dict)

        # Merge ERC-8004 registration data from R2
        agents_dict = merge_erc8004_registration_data(agents_dict)

        sorted_agents_dict = {k: agents_dict[k] for k in sorted(agents_dict.keys())}

        metadata = {
            "last_updated": datetime.now(UTC).isoformat(),
            "commit_sha": os.environ.get("GITHUB_SHA", ""),
            "agents": sorted_agents_dict,
        }
        return metadata

    def generate_agent_table(self, metadata: Dict) -> str:
        """Generate markdown table from agent metadata"""
        table_header = """| Agent ID | Description | Available Tools | Source Code | External APIs |
|----------|-------------|-----------------|-------------|---------------|"""

        rows = []
        for agent_id, agent_data in sorted(metadata["agents"].items()):
            tools = agent_data.get("tools", [])
            tool_names = [f"• {tool['function']['name']}" for tool in tools] if tools else []
            tools_text = "<br>".join(tool_names) if tool_names else "-"

            apis = agent_data["metadata"].get("external_apis", [])
            apis_text = ", ".join(apis) if apis else "-"

            module_name = agent_data.get("module", "")
            source_link = f"[Source](./agents/{module_name}.py)" if module_name else "-"

            description = agent_data["metadata"].get("description", "").replace("\n", " ")
            rows.append(f"| {agent_id} | {description} | {tools_text} | {source_link} | {apis_text} |")

        return f"{table_header}\n" + "\n".join(rows)

    def update_readme(self, table_content: str) -> None:
        readme_path = Path("mesh/README.md")

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            section_pattern = r"(## Appendix: All Available Mesh Agents\n)(.*?)(\n---)"
            if not re.search(section_pattern, content, re.DOTALL):
                log.warning("Could not find '## Appendix: All Available Mesh Agents' section in README")
                return

            updated_content = re.sub(
                section_pattern,
                f"## Appendix: All Available Mesh Agents\n\n{table_content}\n---",
                content,
                flags=re.DOTALL,
            )

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

            log.info("Updated README with new agent table")

        except Exception as e:
            log.error(f"Failed to update README: {e}")
            raise

    def upload_metadata(self, metadata: Dict) -> None:
        """Upload metadata to S3 if credentials are available"""
        if not self.s3_client:
            return

        try:
            metadata_json = json.dumps(metadata, indent=2)
            self.s3_client.put_object(
                Bucket="mesh",
                Key="metadata.json",
                Body=metadata_json,
                ContentType="application/json",
            )
            log.info("Uploaded metadata to S3")
        except Exception as e:
            log.warning(f"Failed to upload metadata to S3: {e}")
            # Don't raise the error, just log it and continue

    def write_metadata_local(self, metadata: Dict) -> None:
        """Write metadata to a local file"""
        try:
            metadata_json = json.dumps(metadata, indent=2)
            with open("metadata.json", "w", encoding="utf-8") as f:
                f.write(metadata_json)
            log.info("Wrote metadata to local file metadata.json")
        except Exception as e:
            log.error(f"Failed to write metadata locally: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="Update mesh agent metadata.")
    parser.add_argument("--dev", action="store_true", help="Write metadata to local file instead of uploading to S3")
    args = parser.parse_args()

    try:
        manager = MetadataManager()

        agents = manager.load_agents()
        if not agents:
            log.error("No agents found")
            sys.exit(1)

        metadata = manager.create_metadata(agents)

        if args.dev:
            manager.write_metadata_local(metadata)
        elif manager.s3_client:
            manager.upload_metadata(metadata)
        else:
            log.info("S3 credentials not found, writing metadata.json locally")
            manager.write_metadata_local(metadata)

        table = manager.generate_agent_table(metadata)
        manager.update_readme(table)

    except Exception:
        log.exception("Failed to update metadata")
        sys.exit(1)


if __name__ == "__main__":
    main()
