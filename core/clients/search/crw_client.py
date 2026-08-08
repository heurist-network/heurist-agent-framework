import asyncio
import os
from typing import Optional

from firecrawl import FirecrawlApp
from firecrawl.firecrawl import ScrapeOptions

from .base_search_client import BaseSearchClient, SearchResponse

# fastCRW is a Firecrawl-compatible web scraper (single binary; self-host or cloud).
# It exposes a Firecrawl-compatible REST API, so the cleanest integration is to
# reuse the Firecrawl SDK pointed at the fastCRW base URL.
DEFAULT_CRW_API_URL = "https://fastcrw.com/api"


class CrwClient(BaseSearchClient):
    """fastCRW implementation of the search client (Firecrawl-compatible)."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        api_key = api_key or os.getenv("CRW_API_KEY", "")
        api_url = api_url or DEFAULT_CRW_API_URL
        super().__init__(api_key, api_url, rate_limit)
        self.app = FirecrawlApp(api_key=api_key, api_url=api_url)

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using the fastCRW (Firecrawl-compatible) SDK in a thread pool to keep it async."""
        try:
            # Apply rate limiting
            await self._apply_rate_limiting()

            # Create ScrapeOptions object instead of passing raw dict
            scrape_options = ScrapeOptions(formats=["markdown"])

            # Run the synchronous SDK call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.app.search(query=query, scrape_options=scrape_options),
            )

            # Handle the response format from the SDK
            if isinstance(response, dict) and "data" in response:
                # Response is already in the right format
                return response
            elif isinstance(response, dict) and "success" in response:
                # Response is in the documented format
                return {"data": response.get("data", [])}
            elif isinstance(response, list):
                # Response is a list of results
                formatted_data = []
                for item in response:
                    if isinstance(item, dict):
                        formatted_data.append(item)
                    else:
                        # Handle non-dict items (like objects)
                        formatted_data.append(
                            {
                                "url": getattr(item, "url", ""),
                                "markdown": getattr(item, "markdown", "") or getattr(item, "content", ""),
                                "title": getattr(item, "title", "") or getattr(item, "metadata", {}).get("title", ""),
                            }
                        )
                return {"data": formatted_data}
            else:
                print(f"Unexpected response format from fastCRW: {type(response)}")
                return {"data": []}

        except Exception as e:
            print(f"Error searching with fastCRW: {e}")
            print(f"Response type: {type(response) if 'response' in locals() else 'N/A'}")
            return {"data": []}
