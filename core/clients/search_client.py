from typing import Optional

from .search.base_search_client import BaseSearchClient, SearchResponse
from .search.duckduckgo_client import DuckDuckGoClient
from .search.exa_client import ExaClient
from .search.firecrawl_client import FirecrawlClient


class SearchClient(BaseSearchClient):
    """
    Unified search client that wraps different search implementations.
    Initializes with a client type and delegates to the appropriate implementation.
    """

    def __init__(self, client_type: str, api_key: str = "", api_url: Optional[str] = None, rate_limit: int = 1):
        """
        Initialize a search client of the specified type.

        Args:
            client_type: Type of search client to use ('firecrawl', 'exa', 'duckduckgo', etc.)
            api_key: API key for the search service
            api_url: Optional custom API URL
            rate_limit: Rate limit in seconds between requests
        """
        super().__init__(api_key, api_url, rate_limit)

        # Create the appropriate client implementation
        if client_type.lower() == "firecrawl":
            self._implementation = FirecrawlClient(api_key=api_key, api_url=api_url, rate_limit=rate_limit)
        elif client_type.lower() == "exa":
            self._implementation = ExaClient(api_key=api_key, api_url=api_url, rate_limit=rate_limit)
        elif client_type.lower() == "duckduckgo":
            # DuckDuckGo doesn't require API key or custom URL
            self._implementation = DuckDuckGoClient(rate_limit=rate_limit)
        else:
            raise ValueError(f"Unsupported search client type: {client_type}")

        self.client_type = client_type.lower()

    async def search(self, query: str, timeout: int = 15000) -> SearchResponse:
        """
        Execute a search query using the configured search implementation.

        Args:
            query: The search query to execute
            timeout: Timeout in milliseconds

        Returns:
            Standardized search response with results
        """
        # Delegate to the implementation
        return await self._implementation.search(query, timeout)

    def update_rate_limit(self, rate_limit: int) -> None:
        """
        Update the rate limit for the search client.

        Args:
            rate_limit: New rate limit in seconds
        """
        self.rate_limit = rate_limit
        self._implementation.rate_limit = rate_limit
