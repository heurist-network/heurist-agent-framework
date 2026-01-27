import logging
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from clients.project_knowledge_client import ProjectKnowledgeClient
from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class ProjectKnowledgeAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self._client = ProjectKnowledgeClient()
        self.metadata.update(
            {
                "name": "Project Knowledge Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Search crypto projects by name, ticker, or contract address using fuzzy matching. Get detailed project information including team, investors, funding, and events. Supports semantic search for natural language queries.",
                "external_apis": ["RootData", "AIXBT"],
                "tags": ["Project Search", "Crypto Knowledge"],
                "recommended": True,
                "image_url": "",
                "examples": [
                    "semantic_search name=SocialDAO",
                    "semantic_search symbol=WLFI",
                    "semantic_search contract_address=0xd3c6880d797c4c26b5d8bf76d8cdf6042c2cd48b",
                    "semantic_search twitter_handle=@heurist_ai",
                    "semantic_search query=projects backed by a16z",
                    "semantic_search query=AI-powered DeFi yield aggregators",
                    "get_project canonical_name=SocialDAO",
                ],
            }
        )
    async def cleanup(self):
        """Close pooled resources for reuse via agent pool."""
        await self._client.close()
        await super().cleanup()

    def get_system_prompt(self) -> str:
        return (
            "You are a crypto project knowledge assistant. You help users find and understand crypto projects. "
            "Use semantic_search to find projects by name, symbol, contract_address, twitter_handle, or natural language queries. "
            "When searching by specific identifiers (name/symbol/twitter_handle), results include AIXBT project intelligence. "
            "Semantic search returns name, symbol, one_liner, and description. For full project details (team, investors, events, fundraising, exchanges), call get_project with the canonical project name. "
            "Use get_project to retrieve comprehensive project information when you know the exact project name. "
            "Be precise and return accurate project information."
        )

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "semantic_search",
                    "description": "Search for crypto projects with comprehensive details including overview, funding status, recent developments in chronological order, team info, and token info. Useful for researching specific projects or tokens. Can search by specific identifiers (name, symbol, contract_address, twitter_handle) or use natural language queries.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Filter by project name (case-insensitive fuzzy match)",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "Filter by token symbol/ticker (case-insensitive match)",
                            },
                            "contract_address": {
                                "type": "string",
                                "description": "Filter by smart contract address (0x...)",
                            },
                            "twitter_handle": {
                                "type": "string",
                                "description": "Filter by Twitter/X handle (with or without @)",
                            },
                            "query": {
                                "type": "string",
                                "description": "Natural language query for semantic search (e.g., 'projects backed by a16z'). Use when no specific identifiers provided.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 10,
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_project",
                    "description": "Get all details about a project when you already know its canonical name. Returns comprehensive information including team, investors, events, fundraising, exchanges, and token details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "canonical_name": {
                                "type": "string",
                                "description": "The canonical project name (exact match required)",
                            },
                        },
                        "required": ["canonical_name"],
                    },
                },
            },
        ]

    def _detect_query_specificity(self, query: str) -> float:
        query_lower = query.lower().strip()
        
        if len(query.split()) <= 2 and not any(word in query_lower for word in ["project", "token", "protocol", "platform", "backed", "funded"]):
            return 0.9
        
        if any(word in query_lower for word in ["backed by", "funded by", "investor", "category", "type"]):
            return 0.75
        
        if len(query.split()) <= 5:
            return 0.7
        
        return 0.65

    @with_retry(max_retries=3, delay=1.0)
    @with_cache(ttl_seconds=300)
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        await self._client.connect()

        if tool_name == "semantic_search":
            name = function_args.get("name")
            symbol = function_args.get("symbol")
            contract_address = function_args.get("contract_address")
            twitter_handle = function_args.get("twitter_handle")
            query = function_args.get("query")
            limit = function_args.get("limit", 10)

            has_specific_params = any([name, symbol, contract_address, twitter_handle])

            if has_specific_params:
                search_query = name or symbol or contract_address or twitter_handle
                results = await self._client.lexical_search(search_query, return_details=True)

                aixbt_results = None
                if name or symbol or twitter_handle:
                    aixbt_params = {"limit": 5}
                    if twitter_handle:
                        aixbt_params["xHandle"] = twitter_handle.lstrip("@")
                    elif symbol:
                        aixbt_params["ticker"] = symbol
                    elif name:
                        aixbt_params["name"] = name

                    try:
                        aixbt_results = await self._call_agent_tool(
                            "mesh.agents.aixbt_project_info_agent",
                            "AIXBTProjectInfoAgent",
                            "search_projects",
                            aixbt_params,
                            raw_data_only=True,
                            session_context=session_context,
                        )
                    except Exception as e:
                        logger.debug(f"AIXBT search failed: {e}")

                response = {"results": results, "count": len(results)}
                if aixbt_results:
                    response["aixbt_results"] = aixbt_results
                return response

            elif query:
                query_specificity = self._detect_query_specificity(query)
                results = await self._client.semantic_search(query, limit=limit, query_specificity=query_specificity)
                return {
                    "results": results,
                    "count": len(results),
                    "note": "For full project details (team, investors, events, fundraising), call get_project with the canonical project name.",
                }
            else:
                return {"error": "Either provide specific search parameters (name/symbol/contract_address/twitter_handle) or a natural language query"}

        elif tool_name == "get_project":
            canonical_name = function_args.get("canonical_name", "")

            if not canonical_name:
                return {"error": "canonical_name parameter is required"}

            project = await self._client.get_project_details(canonical_name)

            if not project:
                return {"error": f"Project '{canonical_name}' not found"}

            return {"project": project}

        else:
            return {"error": f"Unknown tool: {tool_name}"}
