import logging
import os
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class TavilySearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is required")

        from tavily import AsyncTavilyClient

        self.client = AsyncTavilyClient(api_key=api_key)

        self.metadata.update(
            {
                "name": "Tavily Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search the web using Tavily's API and extract content from URLs.",
                "external_apis": ["Tavily"],
                "tags": ["Search"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Tavily.png",
                "examples": [
                    "What is the latest news on Bitcoin?",
                    "Recent developments in quantum computing",
                    "Search for articles about the latest trends in AI",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
    IDENTITY:
    You are a web search specialist that can find information using Tavily's search and extract APIs.

    CAPABILITIES:
    - Search for webpages related to a query
    - Extract content from specific URLs

    RESPONSE GUIDELINES:
    - Keep responses focused on what was specifically asked
    - Format information in a clear, readable way
    - Prioritize relevant, credible sources
    - Provide direct answers where possible, with supporting search results

    DOMAIN-SPECIFIC RULES:
    For search queries, use the search tool to find relevant webpages.
    For extracting content from known URLs, use the extract tool.
    For complex queries, consider using both tools to provide comprehensive information.

    When presenting search results, apply these criteria:
    1. Prioritize recency and relevance
    2. Include source URLs where available
    3. Organize information logically and highlight key insights

    IMPORTANT:
    - Never invent or assume information not found in search results
    - Clearly indicate when information might be outdated
    - Keep responses concise and relevant"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "tavily_web_search",
                    "description": "Search for webpages using Tavily's search API. Returns relevant results with titles, snippets, and URLs. Supports domain filtering, date filtering, and topic selection.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "The search term or natural language query (max 400 characters)",
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 10)",
                            },
                            "include_domains": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of domains to restrict search to (e.g., ['arxiv.org', 'nature.com'])",
                            },
                            "topic": {
                                "type": "string",
                                "description": "Search topic category: 'general', 'news', or 'finance' (default: 'general')",
                                "enum": ["general", "news", "finance"],
                            },
                            "time_range": {
                                "type": "string",
                                "description": "Time range filter: 'day', 'week', 'month', 'year', or 'd', 'w', 'm', 'y'",
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tavily_extract_url",
                    "description": "Extract content from one or more URLs using Tavily's extract API. Returns raw content from the specified URLs. Useful for getting full page content from known URLs.",
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

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def tavily_web_search(
        self,
        search_term: str,
        limit: int = 10,
        include_domains: Optional[List[str]] = None,
        topic: str = "general",
        time_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info(f"Executing Tavily web search for '{search_term}' with limit {limit}")

        kwargs = {
            "query": search_term,
            "max_results": limit,
            "search_depth": "advanced",
            "topic": topic,
        }
        if include_domains:
            kwargs["include_domains"] = include_domains
        if time_range:
            kwargs["time_range"] = time_range

        response = await self.client.search(**kwargs)

        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(
                {
                    "title": result.get("title", "N/A"),
                    "url": result.get("url", "N/A"),
                    "score": result.get("score", 0),
                    "text": result.get("content", ""),
                }
            )

        logger.info(f"Successfully retrieved {len(formatted_results)} search results")
        return {"status": "success", "data": {"search_results": formatted_results}}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def tavily_extract_url(self, urls: List[str]) -> Dict[str, Any]:
        logger.info(f"Extracting content from {len(urls)} URL(s)")

        urls = urls[:20]
        response = await self.client.extract(urls=urls)

        extracted_results = []
        for result in response.get("results", []):
            extracted_results.append(
                {
                    "url": result.get("url", "N/A"),
                    "raw_content": result.get("raw_content", ""),
                }
            )

        logger.info(f"Successfully extracted content from {len(extracted_results)} URL(s)")
        return {"status": "success", "data": {"extracted_results": extracted_results}}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "tavily_web_search":
            search_term = function_args.get("search_term")
            if not search_term:
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            limit = function_args.get("limit", 10)
            if limit < 5:
                limit = 5

            include_domains = function_args.get("include_domains")
            topic = function_args.get("topic", "general")
            time_range = function_args.get("time_range")

            result = await self.tavily_web_search(search_term, limit, include_domains, topic, time_range)

        elif tool_name == "tavily_extract_url":
            urls = function_args.get("urls")
            if not urls:
                return {"status": "error", "error": "Missing 'urls' parameter"}

            result = await self.tavily_extract_url(urls)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
