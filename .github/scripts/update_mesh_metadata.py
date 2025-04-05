#!/usr/bin/env python3
import ast
import json
import logging
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict

import boto3
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# base agent metadata structure from mesh/mesh_agent.py
BASE_AGENT_METADATA = {
    "name": "",
    "version": "1.0.0",
    "author": "unknown",
    "author_address": "0x0000000000000000000000000000000000000000",
    "description": "",
    "inputs": [],
    "outputs": [],
    "external_apis": [],
    "tags": [],
    "large_model_id": "anthropic/claude-3.5-haiku",
    "small_model_id": "anthropic/claude-3.5-haiku",
    "hidden": False,
    "recommended": False,
    "image_url": "",
    "examples": [],
}


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

    def fetch_existing_metadata(self) -> Dict:
        try:
            response = requests.get("https://mesh.heurist.ai/mesh_agents_metadata.json")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.warning(f"Failed to fetch existing metadata: {e}")
            return {"agents": {}}

    def load_agents(self) -> Dict[str, dict]:
        mesh_dir = Path("mesh")
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

                    agent_data = {
                        "metadata": {**BASE_AGENT_METADATA, **(data.get("metadata", {}))},
                        "module": file_path.stem,
                        "tools": data.get("tools", []),
                    }

                    if agent_data["tools"]:
                        tool_names = ", ".join(t["function"]["name"] for t in agent_data["tools"])
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
            source_link = f"[Source](./{module_name}.py)" if module_name else "-"

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
            log.info("Skipping metadata upload to S3 (no credentials)")
            return

        try:
            metadata_json = json.dumps(metadata, indent=2)
            self.s3_client.put_object(
                Bucket="mesh",
                Key="mesh_agents_metadata.json",
                Body=metadata_json,
                ContentType="application/json",
            )
            log.info("Uploaded metadata to S3")
        except Exception as e:
            log.warning(f"Failed to upload metadata to S3: {e}")
            # Don't raise the error, just log it and continue


def main():
    try:
        manager = MetadataManager()

        agents = manager.load_agents()
        if not agents:
            log.error("No agents found")
            sys.exit(1)

        metadata = manager.create_metadata(agents)
        manager.upload_metadata(metadata)

        table = manager.generate_agent_table(metadata)
        manager.update_readme(table)

    except Exception:
        log.exception("Failed to update metadata")
        sys.exit(1)


if __name__ == "__main__":
    main()
