import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypedDict


class SearchResponse(TypedDict):
    data: List[Dict[str, Any]]


class BaseSearchClient(ABC):
    """Abstract base class for search clients."""

    def __init__(self, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        self.api_key = api_key
        self.api_url = api_url
        self.rate_limit = rate_limit
        self._last_request_time = 0  # Track the last request time

    @abstractmethod
    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """Execute a search query and return formatted results."""
        pass

    async def _apply_rate_limiting(self):
        """Apply rate limiting before making a request."""
        current_time = asyncio.get_event_loop().time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self.rate_limit:
            await asyncio.sleep(self.rate_limit - time_since_last_request)

        # Update last request time
        self._last_request_time = asyncio.get_event_loop().time()
