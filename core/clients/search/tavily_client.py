import asyncio
from typing import Optional

from tavily import TavilyClient as TavilySDKClient

from .base_search_client import BaseSearchClient, SearchResponse


class TavilyClient(BaseSearchClient):
    """Tavily implementation of the search client."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        super().__init__(api_key, api_url, rate_limit)
        self.client = TavilySDKClient(api_key=api_key)

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using Tavily API."""
        try:
            await self._apply_rate_limiting()

            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.client.search(query=query, max_results=10, search_depth="basic")
            )

            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append(
                    {
                        "url": result.get("url", ""),
                        "markdown": result.get("content", ""),
                        "title": result.get("title", ""),
                    }
                )

            return {"data": formatted_results}

        except Exception as e:
            print(f"Error searching with Tavily: {e}")
            return {"data": []}
