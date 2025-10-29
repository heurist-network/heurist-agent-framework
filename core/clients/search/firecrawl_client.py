import asyncio
from typing import Optional

from firecrawl import FirecrawlApp

from .base_search_client import BaseSearchClient, SearchResponse


class FirecrawlClient(BaseSearchClient):
    """Firecrawl implementation of the search client."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        super().__init__(api_key, api_url, rate_limit)
        self.app = FirecrawlApp(api_key=api_key, api_url=api_url)

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using Firecrawl SDK in a thread pool to keep it async."""
        try:
            # Apply rate limiting
            await self._apply_rate_limiting()

            # Create ScrapeOptions object instead of passing raw dict
            scrape_options = {"formats": ["markdown"]}

            # Run the synchronous SDK call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.app.search(query=query, scrape_options=scrape_options),
            )

            # Handle the response format from the SDK
            if hasattr(response, "web"):
                return {"data": response.web}
            else:
                print(f"Unexpected response format from Firecrawl: {type(response)}")
                return {"data": []}

        except Exception as e:
            print(f"Error searching with Firecrawl: {e}")
            print(f"Response type: {type(response) if 'response' in locals() else 'N/A'}")
            return {"data": []}
