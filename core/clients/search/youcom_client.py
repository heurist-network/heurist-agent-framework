import asyncio
import json
import os
from typing import Optional

import requests

from .base_search_client import BaseSearchClient, SearchResponse


class YouComClient(BaseSearchClient):
    """You.com implementation of the search client."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        super().__init__(api_key, api_url, rate_limit)
        self.base_url = api_url or "https://api.you.com"
        
        # Support both YDC_API_KEY and YOUCOM_API_KEY for compatibility
        if not api_key:
            api_key = os.getenv("YDC_API_KEY") or os.getenv("YOUCOM_API_KEY", "")
        
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "heurist-agent-framework/youcom-integration",
        }
        
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key

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
            
            # Handle both web and news results
            web_results = response.get("results", {}).get("web", [])
            news_results = response.get("results", {}).get("news", [])
            
            # Process web results
            for result in web_results:
                formatted_results.append({
                    "url": result.get("url", ""),
                    "markdown": result.get("description", ""),
                    "title": result.get("title", ""),
                    "type": "web"
                })
            
            # Process news results  
            for result in news_results:
                formatted_results.append({
                    "url": result.get("url", ""),
                    "markdown": result.get("description", ""),
                    "title": result.get("title", ""),
                    "type": "news"
                })

            return {"data": formatted_results}

        except Exception as e:
            print(f"Error searching with You.com: {e}")
            return {"data": []}

    def _make_request(self, query: str, timeout: int):
        """Make synchronous request to You.com API."""
        
        # Use the search endpoint (works with or without API key)
        url = f"{self.base_url}/v1/agents/search"
        
        params = {
            "query": query,
            "count": 10
        }

        try:
            response = requests.get(
                url, 
                params=params, 
                headers=self.headers, 
                timeout=timeout / 1000
            )
            response.raise_for_status()
            
            # Handle different response formats
            response_data = response.json()
            
            # If the response is in the expected format, return it
            if "results" in response_data:
                return response_data
                
            # If it's a flat list of results, wrap it
            if isinstance(response_data, list):
                return {"results": {"web": response_data}}
                
            # If it has a different structure, try to normalize it
            return {"results": {"web": [response_data] if isinstance(response_data, dict) else []}}
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception(
                    "You.com API authentication failed. Please set YDC_API_KEY environment variable "
                    "or pass api_key parameter. For free usage, ensure you're within the daily quota."
                )
            elif e.response.status_code == 429:
                raise Exception(
                    "You.com API rate limit exceeded. Please wait before making more requests "
                    "or upgrade your API plan."
                )
            else:
                raise Exception(f"You.com API error {e.response.status_code}: {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error connecting to You.com API: {str(e)}")