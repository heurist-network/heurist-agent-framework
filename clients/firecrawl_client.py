import asyncio
from typing import Dict, List, Optional, TypedDict

from firecrawl import FirecrawlApp


class SearchResponse(TypedDict):
    data: List[Dict[str, str]]


class Firecrawl:
    """Simple wrapper for Firecrawl SDK."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None):
        self.app = FirecrawlApp(api_key=api_key, api_url=api_url)
        self._last_request_time = 0  # Track the last request time

    async def search(self, query: str, timeout: int = 15000, rate_limit: int = 1) -> SearchResponse:
        """Search using Firecrawl SDK in a thread pool to keep it async."""
        try:
            # Add rate limiting delay
            current_time = asyncio.get_event_loop().time()
            time_since_last_request = current_time - self._last_request_time
            if time_since_last_request < rate_limit:
                await asyncio.sleep(rate_limit - time_since_last_request)

            # Update last request time
            self._last_request_time = asyncio.get_event_loop().time()

            # Run the synchronous SDK call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.app.search(query=query, params={"scrapeOptions": {"formats": ["markdown"]}}),
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
                print(f"Unexpected response format from Firecrawl: {type(response)}")
                return {"data": []}

        except Exception as e:
            print(f"Error searching with Firecrawl: {e}")
            print(f"Response type: {type(response) if 'response' in locals() else 'N/A'}")
            return {"data": []}
