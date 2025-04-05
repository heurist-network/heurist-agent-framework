import asyncio
from typing import Optional

import requests

from .base_search_client import BaseSearchClient, SearchResponse


class ExaClient(BaseSearchClient):
    """Exa implementation of the search client."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        super().__init__(api_key, api_url, rate_limit)
        self.base_url = api_url or "https://api.exa.ai"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using Exa API."""
        try:
            # Apply rate limiting
            await self._apply_rate_limiting()

            # Run the API call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: self._make_request(query, timeout))

            # Format the search results data
            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append(
                    {
                        "url": result.get("url", ""),
                        "markdown": result.get("text", ""),
                        "title": result.get("title", ""),
                    }
                )

            return {"data": formatted_results}

        except Exception as e:
            print(f"Error searching with Exa: {e}")
            return {"data": []}

    def _make_request(self, query: str, timeout: int):
        """Make synchronous request to Exa API."""
        url = f"{self.base_url}/search"
        payload = {"query": query, "numResults": 10, "contents": {"text": True}}

        response = requests.post(url, json=payload, headers=self.headers, timeout=timeout / 1000)
        response.raise_for_status()
        return response.json()
