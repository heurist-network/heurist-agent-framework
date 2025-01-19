from typing import Dict, List
from .base_client import BaseAPIClient
import logging

logger = logging.getLogger(__name__)

class DefiLlamaClient(BaseAPIClient):
    """DefiLlama API implementation"""
    
    def __init__(self):
        super().__init__("https://api.llama.fi")
    
    async def get_protocol_tvl(self, protocol: str) -> Dict:
        """
        Get TVL data for a specific protocol
        
        Args:
            protocol: Protocol identifier (e.g. 'aave', 'uniswap') in lowercase
                
        Returns:
            Dictionary containing detailed TVL data for the protocol, including:
            - tvl: Current total locked value
            - chainTvls: TVL distribution across chains
            - tokens: Details of locked tokens
            - name: Protocol name
            - symbol: Protocol token symbol (if any)
            - gecko_id: CoinGecko API ID (if any)
        """
        return await self._make_request(
            "get",
            f"/protocol/{protocol}"
        )
    
    async def get_protocols(self) -> List[Dict]:
        """
        Get list of all protocols and their TVL data
        
        Returns:
            List of protocols, each containing:
            - name: Protocol name
            - symbol: Protocol token symbol
            - chain: Main chain
            - tvl: Current TVL
            - change_1h: 1 hour TVL change percentage
            - change_1d: 24 hour TVL change percentage
            - change_7d: 7 day TVL change percentage
        """
        return await self._make_request(
            "get",
            "/protocols"
        )
    
    async def get_chain_tvl(self, chain: str) -> Dict:
        """
        Get historical TVL data for a specific blockchain
        
        Args:
            chain: Blockchain identifier (e.g. 'ethereum', 'bsc') in lowercase
                
        Returns:
            Historical TVL data for the chain, containing timestamps and corresponding TVL values:
            [
                {
                    "date": unix timestamp,
                    "tvl": float
                },
                ...
            ]
        """
        return await self._make_request(
            "get",
            f"/v2/historicalChainTvl/{chain}"
        )

    def get_current_tvl_all_chains(self) -> float:
        """
        Get current TVL data for all chains
        
        Returns:
            List containing current TVL data for all chains:
            [
                {
                    "gecko_id": str,
                    "tvl": float,
                    "tokenSymbol": str,
                    "cmcId": str,
                    "name": str,
                    "chainId": str
                },
                ...
            ]
        """
        return self._make_request("/v2/chains")
