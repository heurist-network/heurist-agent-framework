import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from tavily import AsyncTavilyClient

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class TavilySearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.metadata.update(
            {
                "name": "Tavily Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": (
                    "This agent can perform web searches and extract content from URLs using the Tavily API, "
                    "designed for AI-powered search with high relevance results."
                ),
                "external_apis": ["Tavily"],
                "tags": ["Search"],
                "verified": True,
                "examples": [
                    "What are the latest breakthroughs in quantum computing?",
                    "Search for recent news about renewable energy",
                    "Extract the main content from this article URL",
                    "What is the current state of AI regulation?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a web search and content extraction agent using Tavily. For a user question or search query, provide a clean, concise, and accurate answer based on the search results. Respond in a conversational manner, ensuring the content is extremely clear and effective. Avoid mentioning sources.
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
                    "name": "tavily_web_search",
                    "description": "Search the web using Tavily Search API with configurable depth and topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query to look up"},
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 5)",
                                "minimum": 1,
                                "maximum": 10,
                            },
                            "search_depth": {
                                "type": "string",
                                "description": "Search depth: 'basic' for fast results or 'advanced' for higher relevance (default: basic)",
                                "enum": ["basic", "advanced"],
                            },
                            "topic": {
                                "type": "string",
                                "description": "Search topic category (default: general)",
                                "enum": ["general", "news", "finance"],
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tavily_extract_content",
                    "description": "Extract content from one or more URLs using Tavily Extract API",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "urls": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of URLs to extract content from (max 20)",
                            },
                        },
                        "required": ["urls"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      TAVILY API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def tavily_web_search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "basic",
        topic: str = "general",
    ) -> Dict:
        logger.info(f"Tavily searching for: {query}, depth: {search_depth}, topic: {topic}")
        try:
            client = AsyncTavilyClient(api_key=self.api_key)
            response = await client.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                topic=topic,
            )

            results = []
            for r in response.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("content", ""),
                    "score": r.get("score", 0),
                })

            logger.info(f"Found {len(results)} results for search: {query}")
            return {"status": "success", "data": {"query": query, "results": results}}

        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch search results: {str(e)}", "data": None}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def tavily_extract_content(self, urls: list) -> Dict:
        logger.info(f"Tavily extracting content from {len(urls)} URLs")
        try:
            client = AsyncTavilyClient(api_key=self.api_key)
            response = await client.extract(urls=urls[:20])

            results = []
            for r in response.get("results", []):
                results.append({
                    "url": r.get("url", ""),
                    "raw_content": r.get("raw_content", ""),
                })

            logger.info(f"Extracted content from {len(results)} URLs")
            return {"status": "success", "data": {"urls": urls, "results": results}}

        except Exception as e:
            logger.error(f"Tavily extract error: {str(e)}")
            return {"status": "error", "error": f"Failed to extract content: {str(e)}", "data": None}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "tavily_web_search":
            query = function_args.get("query")
            if not query:
                return {"error": "Missing 'query' parameter"}

            max_results = min(max(function_args.get("max_results", 5), 1), 10)
            search_depth = function_args.get("search_depth", "basic")
            topic = function_args.get("topic", "general")

            result = await self.tavily_web_search(
                query=query, max_results=max_results, search_depth=search_depth, topic=topic
            )

            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "tavily_extract_content":
            urls = function_args.get("urls")
            if not urls:
                return {"error": "Missing 'urls' parameter"}

            result = await self.tavily_extract_content(urls=urls)

            if errors := self._handle_error(result):
                return errors
            return result

        return {"error": f"Unsupported tool: {tool_name}"}
