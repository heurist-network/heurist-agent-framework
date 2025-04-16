import asyncio

from duckduckgo_search import DDGS

from .base_search_client import BaseSearchClient, SearchResponse


class DuckDuckGoClient(BaseSearchClient):
    """
    DuckDuckGo implementation of the search client.
    DuckDuckGo is unique among search providers as it doesn't require an API key or custom URL.
    """

    def __init__(self, rate_limit: int = 1):
        """
        Initialize a DuckDuckGo search client.

        Args:
            rate_limit: Rate limit in seconds between requests
        """
        # We call the parent constructor with empty strings for api_key and api_url
        # since DuckDuckGo doesn't use these parameters
        super().__init__(api_key="", api_url=None, rate_limit=rate_limit)

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using DuckDuckGo in a thread pool to keep it async."""
        try:
            # Apply rate limiting
            await self._apply_rate_limiting()

            # Run the synchronous DDGS call in a thread pool
            # Note: DDGS doesn't accept a timeout parameter for its text() method
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self._perform_search(query, max_results=10)
            )

            return {"data": response}

        except Exception as e:
            print(f"Error searching with DuckDuckGo: {e}")
            return {"data": []}

    def _perform_search(self, query: str, max_results: int = 10) -> list:
        """
        Perform the actual search using DDGS.
        Note: Unlike other search clients, DDGS doesn't accept a timeout parameter.
        """
        results = []
        try:
            with DDGS() as ddgs:
                # DDGS text() doesn't accept a timeout parameter
                for r in ddgs.text(query, max_results=max_results):
                    results.append(
                        {
                            "url": r["href"],
                            "markdown": r["body"],
                            "title": r["title"],
                        }
                    )
        except Exception as e:
            print(f"DDGS search error: {e}")

        return results
