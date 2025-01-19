from typing import Dict, List, Optional, Union
from .base_client import BaseAPIClient
import logging

logger = logging.getLogger(__name__)

class MerklClient(BaseAPIClient):
    """Merkl API implementation for accessing DeFi opportunities and rewards data"""
    
    def __init__(self):
        super().__init__("https://api.merkl.xyz/v4")
    
    async def get_opportunities(self, 
                              name: Optional[str] = None,
                              chain_id: Optional[str] = None,
                              action: Optional[str] = None,
                              tags: Optional[List[str]] = None,
                              test: Optional[bool] = None,
                              minimum_tvl: Optional[float] = None,
                              status: Optional[str] = None,
                              tokens: Optional[List[str]] = None,
                              sort: Optional[str] = None,
                              order: Optional[str] = None,
                              main_protocol_id: Optional[str] = None,
                              page: Optional[int] = None,
                              items: Optional[int] = None) -> Dict:
        """
        Get list of DeFi opportunities with optional filters
        
        Args:
            name: Filter by opportunity name
            chain_id: Filter by blockchain ID
            action: Filter by action type (POOL, HOLD, DROP, LEND, BORROW)
            tags: Filter by tags
            test: Include test opportunities
            minimum_tvl: Minimum TVL threshold
            status: Filter by status (LIVE, PAST, SOON)
            tokens: Filter by token addresses
            sort: Sort field (apr, tvl, rewards)
            order: Sort order (asc, desc)
            main_protocol_id: Filter by main protocol ID
            page: Page number for pagination
            items: Items per page
        """
        params = {k: v for k, v in locals().items() 
                 if v is not None and k != 'self'}
        
        return await self._make_request(
            "get",
            "/opportunities/",
            params=params
        )

    async def get_opportunity_detail(self, opportunity_id: str) -> Dict:
        """Get detailed information about a specific opportunity"""
        return await self._make_request(
            "get",
            f"/opportunities/{opportunity_id}"
        )

    async def get_campaigns(self,
                          chain_id: Optional[str] = None,
                          token_address: Optional[str] = None,
                          test: bool = False,
                          opportunity_id: Optional[str] = None,
                          start_timestamp: Optional[int] = None,
                          end_timestamp: Optional[int] = None,
                          page: int = 0,
                          items: int = 20) -> Dict:
        """Get list of reward campaigns with optional filters"""
        params = {k: v for k, v in locals().items() 
                 if v is not None and k != 'self'}
        
        return await self._make_request(
            "get",
            "/campaigns/",
            params=params
        )

    async def get_protocols(self,
                          protocol_id: Optional[str] = None,
                          tags: Optional[List[str]] = None,
                          opportunity_tag: Optional[str] = None,
                          page: int = 0,
                          items: int = 20) -> Dict:
        """Get list of protocols with optional filters"""
        params = {k: v for k, v in locals().items() 
                 if v is not None and k != 'self'}
        
        return await self._make_request(
            "get",
            "/protocols/",
            params=params
        )

    async def get_user_rewards(self,
                             address: str,
                             chain_id: str,
                             reload_chain_id: Optional[str] = None,
                             test: bool = False) -> Dict:
        """Get rewards for a specific user address"""
        params = {k: v for k, v in locals().items() 
                 if v is not None and k != 'self' and k != 'address'}
        
        return await self._make_request(
            "get",
            f"/users/{address}/rewards",
            params=params
        )

    async def get_chains(self, name: Optional[str] = None) -> List[Dict]:
        """Get list of supported blockchains"""
        params = {'name': name} if name else None
        return await self._make_request(
            "get",
            "/chains/",
            params=params
        )