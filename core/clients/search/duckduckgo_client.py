import asyncio
import logging
import os

from duckduckgo_search import DDGS

from .base_search_client import BaseSearchClient, SearchResponse

logger = logging.getLogger(__name__)


class DuckDuckGoClient(BaseSearchClient):
    """
    DuckDuckGo implementation of the search client.
    DuckDuckGo is unique among search providers as it doesn't require an API key or custom URL.
    Falls back to Tavily when TAVILY_API_KEY is set and DDGS fails.
    """

    def __init__(self, rate_limit: int = 1):
        """
        Initialize a DuckDuckGo search client.

        Args:
            rate_limit: Rate limit in seconds between requests
        """
        super().__init__(api_key="", api_url=None, rate_limit=rate_limit)
        self.tavily_client = None
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            from tavily import TavilyClient

            self.tavily_client = TavilyClient(api_key=tavily_api_key)
            logger.info("Tavily client initialized as fallback for DuckDuckGoClient")

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using DuckDuckGo in a thread pool to keep it async, with Tavily fallback."""
        try:
            await self._apply_rate_limiting()

            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self._perform_search(query, max_results=10)
            )

            return {"data": response}

        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}, attempting Tavily fallback")
            if self.tavily_client:
                return await self._tavily_fallback_search(query)
            logger.error(f"Error searching with DuckDuckGo (no Tavily fallback available): {e}")
            return {"data": []}

    def _perform_search(self, query: str, max_results: int = 10) -> list:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "url": r["href"],
                        "markdown": r["body"],
                        "title": r["title"],
                    }
                )
        return results

    async def _tavily_fallback_search(self, query: str, max_results: int = 10) -> SearchResponse:
        def _do_tavily_search():
            response = self.tavily_client.search(query=query, max_results=max_results)
            results = []
            for r in response.get("results", []):
                results.append(
                    {
                        "url": r.get("url", ""),
                        "markdown": r.get("content", ""),
                        "title": r.get("title", ""),
                    }
                )
            return results

        results = await asyncio.get_event_loop().run_in_executor(None, _do_tavily_search)
        logger.info(f"Tavily fallback returned {len(results)} results for: {query}")
        return {"data": results}
