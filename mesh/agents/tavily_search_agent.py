import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from tavily import AsyncTavilyClient

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class TavilySearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable is required")

        self.client = AsyncTavilyClient(api_key=self.api_key)
        self.metadata.update(
            {
                "name": "Tavily Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Search agent that uses Tavily to perform web searches optimized for LLM consumption.",
                "external_apis": ["Tavily"],
                "tags": ["Search"],
                "verified": True,
                "examples": [
                    "What are the latest developments in AI?",
                    "Find recent news about cryptocurrency regulations",
                ],
                "credits": {"default": 2},
            }
        )

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "tavily_web_search",
                    "description": "Execute a web search query using Tavily, optimized for LLM consumption.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "The search query.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to return (default: 10).",
                                "minimum": 1,
                                "maximum": 20,
                                "default": 10,
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            },
        ]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def tavily_web_search(self, search_term: str, limit: int = 10) -> Dict[str, Any]:
        logger.info(f"Executing Tavily web search for '{search_term}' with limit={limit}")

        try:
            response = await self.client.search(
                query=search_term,
                max_results=limit,
                search_depth="basic",
                topic="general",
            )

            results = response.get("results", [])
            if results:
                logger.info(f"Tavily search completed with {len(results)} results")
                return {"status": "success", "data": {"results": results}}

            logger.warning("Tavily search completed but no results were found")
            return {"status": "no_data", "data": {"results": []}}

        except Exception as e:
            logger.error(f"Exception in tavily_web_search: {str(e)}")
            return {"status": "error", "error": f"Failed to execute search: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "tavily_web_search":
            search_term = function_args.get("search_term")
            limit = function_args.get("limit", 10)

            if not search_term:
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            result = await self.tavily_web_search(search_term, limit)
        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result


def build_tavily_search_fallback(search_term: str, limit: int = 10) -> Dict[str, Any]:
    """Build a fallback spec targeting Tavily web search."""
    return {
        "module": "mesh.agents.tavily_search_agent",
        "class": "TavilySearchAgent",
        "input": {"tool": "tavily_web_search", "tool_arguments": {"search_term": search_term, "limit": limit}},
    }


def build_firecrawl_to_tavily_fallback(
    tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Standard mapping from Firecrawl tools or NL queries to Tavily search fallback.
    Returns a fallback spec or None when not applicable.
    """
    if tool_name == "firecrawl_web_search":
        search_term = function_args.get("search_term") or original_params.get("query") or ""
        limit = function_args.get("limit", 10)
        return build_tavily_search_fallback(search_term, limit)
    if tool_name == "firecrawl_scrape_url":
        url = function_args.get("url") or ""
        return build_tavily_search_fallback(url, 10)
    if tool_name == "firecrawl_extract_web_data":
        urls = function_args.get("urls") or []
        search_term = urls[0] if urls else (original_params.get("query") or "")
        return build_tavily_search_fallback(search_term, 10)

    if not tool_name:
        query = original_params.get("query") or ""
        return build_tavily_search_fallback(query, 10)

    return None
