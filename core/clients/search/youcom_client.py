import asyncio
from typing import Optional

import requests

from .base_search_client import BaseSearchClient, SearchResponse


class YouComClient(BaseSearchClient):
    """You.com implementation of the search client."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        super().__init__(api_key, api_url, rate_limit)
        self.base_url = api_url or "https://api.you.com"
        
        # Set up headers - if API key is provided, use bearer auth; otherwise go keyless
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Search using You.com API."""
        try:
            # Apply rate limiting
            await self._apply_rate_limiting()

            # Run the API call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self._make_request(query, timeout)
            )

            # Format the search results data
            formatted_results = []
            
            # Handle both web and news results from You.com API
            web_results = response.get("results", {}).get("web", [])
            news_results = response.get("results", {}).get("news", [])
            
            # Process web results
            for result in web_results:
                formatted_results.append(
                    {
                        "url": result.get("url", ""),
                        "markdown": result.get("snippet", ""),
                        "title": result.get("title", ""),
                        "type": "web"
                    }
                )
            
            # Process news results
            for result in news_results:
                formatted_results.append(
                    {
                        "url": result.get("url", ""),
                        "markdown": result.get("snippet", ""),
                        "title": result.get("title", ""),
                        "type": "news"
                    }
                )

            return {"data": formatted_results}

        except Exception as e:
            print(f"Error searching with You.com: {e}")
            return {"data": []}

    def _make_request(self, query: str, timeout: int):
        """Make synchronous request to You.com API."""
        url = f"{self.base_url}/v1/agents/search"
        payload = {"query": query, "count": 10}

        response = requests.get(
            url, 
            params=payload, 
            headers=self.headers, 
            timeout=timeout / 1000
        )
        response.raise_for_status()
        return response.json()