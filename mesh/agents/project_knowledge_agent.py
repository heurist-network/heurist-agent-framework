"""
Project Knowledge Agent - provides access to project information database.
Supports searching projects by name, symbol, x handle, and contract address.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from clients.project_knowledge_client import ProjectKnowledgeClient
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

EXCLUDED_FIELDS = {"active", "logo_url"}


class ProjectKnowledgeAgent(MeshAgent):
    """Agent for querying project knowledge database."""

    def __init__(self):
        super().__init__()
        self.client = ProjectKnowledgeClient()

        self.metadata.update(
            {
                "name": "Project Knowledge Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides access to a comprehensive database of crypto projects. It can search for projects by name, token symbol, or X handle, and retrieve detailed project information including funding, team, events, and more.",
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/ProjectKnowledge.png",
                "external_apis": ["PostgreSQL", "AIXBT"],
                "tags": ["Projects", "Research"],
                "verified": True,
                "examples": [
                    "Get information about Ethereum",
                    "Search for projects by symbol BTC",
                    "Get project details for @ethereum",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that provides information about crypto projects from a comprehensive database.

You can search for projects by:
- Project name (e.g., "Ethereum", "Uniswap") - exact match with cascading fallback
- Token symbol (e.g., "ETH", "UNI") - exact match
- X (Twitter) handle (e.g., "@ethereum", "ethereum") - exact match
- Contract address (e.g., "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984") - exact match

When providing project information, be clear and concise. Include key details like:
- Project name and token symbol
- One-liner description
- Key investors and funding rounds
- Recent events
- Links to official websites and social media

Format your response in clean text. Be objective and informative."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_project",
                    "description": "Get crypto project details including description, twitter handle, defillama slug, token info (CA on multiple chains, coingecko id, symbol, WITHOUT market data), team, investors, chronological events, similar projects. Lookup parameter MUST be ONE OF name, symbol, x_handle, or contract_address. Not all result fields are available. New or small projects might be missing. Data aggregated from multiple sources may have inconsistencies. Name lookups can be ambiguous - must verify the returned entity matches the user intent. In case of mismatch, ignore the tool response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Project name (e.g., 'Ethereum', 'Uniswap'). Use for exact match and prefix match.",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "Token symbol. Use for exact match for projects with a live token.",
                            },
                            "x_handle": {
                                "type": "string",
                                "description": "X (Twitter) handle with or without @. Use for exact match.",
                            },
                            "contract_address": {
                                "type": "string",
                                "description": "Token contract address. Case-insensitive for 0x addresses.",
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    async def _handle_tool_logic(
        self,
        tool_name: str,
        function_args: dict,
        session_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Handle tool execution."""
        if tool_name == "get_project":
            return await self._get_project(
                name=function_args.get("name"),
                symbol=function_args.get("symbol"),
                x_handle=function_args.get("x_handle"),
                contract_address=function_args.get("contract_address"),
            )
        return {"error": f"Unknown tool: {tool_name}"}

    async def _aixbt_search(
        self,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        x_handle: Optional[str] = None,
    ) -> Any:
        """Search AIXBT for project information. Returns project dict, 'not found', or 'error'."""
        args = {"limit": 1, "minScore": 0}

        if name:
            args["name"] = name
        if symbol:
            args["ticker"] = symbol
        if x_handle:
            args["xHandle"] = x_handle.lstrip("@") if x_handle.startswith("@") else x_handle

        result = await self._call_agent_tool_safe(
            "mesh.agents.aixbt_project_info_agent",
            "AIXBTProjectInfoAgent",
            "search_projects",
            args,
            log_instance=logger,
            context="AIXBTProjectInfoAgent.search_projects",
        )

        if result.get("status") == "error" or "error" in result:
            return "error"

        projects = []
        if "data" in result and isinstance(result["data"], dict):
            projects = result["data"].get("projects", [])
        elif "projects" in result:
            projects = result.get("projects", [])

        if not projects:
            return "not found"

        return projects[0]

    async def _get_project(
        self,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        x_handle: Optional[str] = None,
        contract_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get project details from database and AIXBT in parallel."""
        if not any([name, symbol, x_handle, contract_address]):
            return {"error": "At least one of name, symbol, x_handle, or contract_address must be provided"}

        contract_only = contract_address and not any([name, symbol, x_handle])

        async def fetch_database():
            project = await self.client.get_project(
                name=name,
                symbol=symbol,
                x_handle=x_handle,
                contract_address=contract_address,
            )
            if not project:
                return "not found"
            return {k: v for k, v in project.items() if k not in EXCLUDED_FIELDS}

        if contract_only:
            db_result = await fetch_database()
            if isinstance(db_result, Exception):
                logger.warning(f"Database lookup failed: {db_result}")
                db_result = "error"
            return {"database_project": db_result}

        db_result, aixbt_result = await asyncio.gather(
            fetch_database(),
            self._aixbt_search(name=name, symbol=symbol, x_handle=x_handle),
            return_exceptions=True,
        )

        if isinstance(db_result, Exception):
            logger.warning(f"Database lookup failed: {db_result}")
            db_result = "error"

        if isinstance(aixbt_result, Exception):
            logger.warning(f"AIXBT lookup failed: {aixbt_result}")
            aixbt_result = "error"

        return {
            "database_project": db_result,
            "aixbt_data": aixbt_result,
        }

    async def cleanup(self):
        """Cleanup resources including database connection pool."""
        await self.client.close()
        await super().cleanup()
