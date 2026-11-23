import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from duckduckgo_search import DDGS

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class DuckDuckGoSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.tavily_client = None
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            from tavily import TavilyClient

            self.tavily_client = TavilyClient(api_key=tavily_api_key)
            logger.info("Tavily client initialized as fallback for DuckDuckGo")
        self.metadata.update(
            {
                "name": "DuckDuckGo Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": (
                    "This agent can fetch and analyze web search results using DuckDuckGo API and provide intelligent summaries."
                ),
                "external_apis": ["DuckDuckGo"],
                "tags": ["Search"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/DuckDuckGo.png",
                "examples": [
                    "What happens if you put a mirror in front of a black hole?",
                    "Could octopuses be considered alien life forms?",
                    "Why don't birds get electrocuted when sitting on power lines?",
                    "How do fireflies produce light?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a web search and analysis agent using DuckDuckGo. For a user question or search query, provide a clean, concise, and accurate answer based on the search results. Respond in a conversational manner, ensuring the content is extremely clear and effective. Avoid mentioning sources.
        Strict formatting rules:
        1. no bullet points or markdown
        2. You don't need to mention the sources
        3. Just provide the answer in a straightforward way.
        Avoid introductory phrases, unnecessary filler, and mentioning sources.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web using DuckDuckGo Search API",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "The search term to look up"},
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 5)",
                                "minimum": 1,
                                "maximum": 10,
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                      DUCKDUCKGO API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_web(self, search_term: str, max_results: int = 5) -> Dict:
        """Search the web using DuckDuckGo, with Tavily fallback on failure"""
        logger.info(f"Searching web for: {search_term}, max_results: {max_results}")
        try:

            def _do_search():
                with DDGS() as ddgs:
                    results = []
                    for r in ddgs.text(search_term, max_results=max_results):
                        results.append({"title": r["title"], "link": r["href"], "snippet": r["body"]})
                    return results

            results = await asyncio.get_event_loop().run_in_executor(None, _do_search)

            logger.info(f"Found {len(results)} results for search: {search_term}")
            return {"status": "success", "data": {"search_term": search_term, "results": results}}

        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {str(e)}, attempting Tavily fallback")
            if self.tavily_client:
                return await self._tavily_fallback_search(search_term, max_results)
            logger.error(f"Search error (no Tavily fallback available): {str(e)}")
            return {"status": "error", "error": f"Failed to fetch search results: {str(e)}", "data": None}

    async def _tavily_fallback_search(self, search_term: str, max_results: int = 5) -> Dict:
        """Fallback search using Tavily when DuckDuckGo fails"""

        def _do_tavily_search():
            response = self.tavily_client.search(query=search_term, max_results=max_results)
            results = []
            for r in response.get("results", []):
                results.append({"title": r.get("title", ""), "link": r.get("url", ""), "snippet": r.get("content", "")})
            return results

        results = await asyncio.get_event_loop().run_in_executor(None, _do_tavily_search)
        logger.info(f"Tavily fallback returned {len(results)} results for: {search_term}")
        return {"status": "success", "data": {"search_term": search_term, "results": results}}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name != "search_web":
            return {"error": f"Unsupported tool: {tool_name}"}

        search_term = function_args.get("search_term")
        max_results = min(max(function_args.get("max_results", 5), 1), 10)  # Ensure between 1-10

        if not search_term:
            return {"error": "Missing 'search_term' parameter"}

        result = await self.search_web(search_term=search_term, max_results=max_results)

        if errors := self._handle_error(result):
            return errors

        return result
