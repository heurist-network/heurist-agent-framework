"""
Project Knowledge Agent - provides access to project information database.
Supports searching projects by name, symbol, and x handle.
Also supports semantic search for discovering projects using natural language.
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from clients.project_knowledge_client import ProjectKnowledgeClient
from decorators import with_cache
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

EXCLUDED_FIELDS = {"active", "logo_url"}


class ProjectKnowledgeAgent(MeshAgent):
    """Agent for querying project knowledge database."""

    def __init__(self):
        super().__init__()
        self.client = ProjectKnowledgeClient()
        self.pageindex_base_url = (os.getenv("PAGEINDEX_URL") or "").rstrip("/")
        self.internal_api_key = os.getenv("INTERNAL_API_KEY")
        self.pageindex_model = "gpt-5.1"

        self.metadata.update(
            {
                "name": "Project Knowledge Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides access to a comprehensive database of crypto projects. It can search for projects by name, token symbol, or X handle, and retrieve detailed project information including funding, team, events, and more.",
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/ProjectKnowledge.png",
                "external_apis": ["PostgreSQL", "AIXBT", "PageIndex"],
                "tags": ["Projects", "Research"],
                "verified": True,
                "recommended": True,
                "examples": [
                    "Get information about Ethereum",
                    "Search for projects by symbol BTC",
                    "Get project details for @ethereum",
                    "Find DeFi projects funded by Paradigm in 2024",
                    "AI projects listed on Binance with recent airdrops",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that provides information about crypto projects from a comprehensive database.

You can search for projects by:
- Project name (e.g., "Ethereum", "Uniswap") - exact match with cascading fallback
- Token symbol (e.g., "ETH", "UNI") - exact match
- X (Twitter) handle (e.g., "@ethereum", "ethereum") - exact match

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
                    "description": "Get crypto project details including description, twitter handle, defillama slug, token info (CA on multiple chains, coingecko id, symbol, WITHOUT market data), team, investors, chronological events, similar projects. Lookup parameter MUST be ONE OF name, symbol, or x_handle. Not all result fields are available. New or small projects without VC backing might be missing. Data aggregated from multiple sources may have inconsistencies. Name lookups can be ambiguous - must verify the returned entity matches the user intent. In case of mismatch, ignore the tool response.",
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
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "semantic_search_projects",
                    "description": "Search crypto projects using natural language criteria. Supports investor filters, tag/category filters, funding years, event years, exchange listings, and event keywords. You can combine multiple constraints in one query. Example queries: 'DeFi projects funded by Paradigm in 2024', 'AI projects listed on Binance with airdrop events in 2025'. Returns matching projects with relevant fields (name, one_liner, tags, investors, fundraising, events, exchanges). Best for discovery and filtering across 10k+ indexed projects. New or small projects without VC backing might be missing. For single project lookup by exact name/symbol/address/twitter, use get_project instead.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Natural language query describing what to find. Include any combination of: investor names like a16z, Paradigm; tags/categories like DeFi, AI, Infra, Layer1, Layer2, zk, NFT, Privacy, Gaming, DePIN, Stablecoin Protocol, DEX, Lending, Derivatives; funded years; event years; exchanges like Binance, Binance Alpha, Coinbase, OKX, Bybit; events like airdrop, mainnet, listing, partnership, exploit/hack, TGE; description of the project business",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of projects to return",
                                "default": 20,
                                "minimum": 1,
                                "maximum": 100,
                            },
                        },
                        "required": ["query"],
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
            )
        elif tool_name == "semantic_search_projects":
            return await self._search_projects_semantic(
                query=function_args.get("query", ""),
                limit=function_args.get("limit", 20),
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

    @with_cache(ttl_seconds=300)
    async def _get_project(
        self,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        x_handle: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get project details from database and AIXBT in parallel."""
        if not any([name, symbol, x_handle]):
            return {"error": "At least one of name, symbol, or x_handle must be provided"}

        async def fetch_database():
            project = await self.client.get_project(
                name=name,
                symbol=symbol,
                x_handle=x_handle,
            )
            if not project:
                return "not found"
            return {k: v for k, v in project.items() if k not in EXCLUDED_FIELDS}

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

    @with_cache(ttl_seconds=300)
    async def _search_projects_semantic(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """Call PageIndex RAG service to search projects with natural language."""
        if not self.pageindex_base_url:
            return {"error": "PAGEINDEX_URL environment variable is required for semantic search"}
        if not self.internal_api_key:
            return {"error": "INTERNAL_API_KEY environment variable is required for semantic search"}
        if not query or not query.strip():
            return {"error": "Query must be a non-empty string"}

        try:
            validated_limit = int(limit)
        except (TypeError, ValueError):
            validated_limit = 20
        validated_limit = max(1, min(validated_limit, 50))

        result = await self._api_request(
            url=f"{self.pageindex_base_url}/api/v1/query",
            method="POST",
            headers={"Content-Type": "application/json", "X-API-Key": self.internal_api_key},
            json_data={"query": query.strip(), "limit": validated_limit, "model": self.pageindex_model},
            timeout=30,
        )
        if not isinstance(result, dict):
            return {"error": "PageIndex API returned an unexpected response format"}
        if result.get("error"):
            return {"error": f"PageIndex API error: {result['error']}"}
        return result

    async def cleanup(self):
        """Cleanup resources including database connection pool."""
        await self.client.close()
        await super().cleanup()
