import aiohttp
import asyncio
from typing import Dict, Optional, Any
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

class BaseAPIClient:
    """Base class for all API clients with shared functionality"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Any:
        """Make an API request"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        try:
            async with getattr(self.session, method)(
                f"{self.base_url}{endpoint}", **kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            logger.error(f"API request failed: {e}")
            raise

    async def close(self):
        """Close the API client session"""
        if self.session:
            await self.session.close()
            self.session = None