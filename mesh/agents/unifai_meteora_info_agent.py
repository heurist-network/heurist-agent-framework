import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class UnifaiMeteoraInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("UNIFAI_API_KEY")
        if not self.api_key:
            raise ValueError("UNIFAI_API_KEY environment variable is required")

        self.api_endpoint = "https://backend.unifai.network/api/v1/actions/call"
        self.meteora_trending_id = 103
        self.meteora_search_id = 29
        self.headers = {"Authorization": self.api_key, "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "UnifAI Meteora Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides Meteora pool information using UnifAI's API, including trending DLMM pools, dynamic AMM pools, and DLMM pool search functionality",
                "external_apis": ["UnifAI"],
                "tags": ["Liquidity Pool"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Unifai.png",
                "examples": [
                    "Show me trending DLMM pools on Meteora",
                    "Search for SOL/USDC pools",
                    "Find dynamic AMM pools with high TVL",
                    "Get DLMM pools for SOL token",
                ],
                "credits": {"default": 0},
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a Meteora DeFi specialist that helps users understand liquidity pools and DeFi opportunities on the Meteora platform. You provide clear pool information, TVL data, and APR metrics. Be factual and objective in your analysis. NEVER make up any data not returned by the tools.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_trending_dlmm_pools",
                    "description": "Get trending DLMM pools from Meteora",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of pools to return",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50,
                            },
                            "include_pool_token_pairs": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of token pairs to include (e.g., ['SOL/USDC'])",
                                "default": [],
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_dynamic_amm_pools",
                    "description": "Search for dynamic AMM pools on Meteora",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of pools to return",
                                "default": 10,
                            },
                            "include_token_mints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of token mint addresses to include (e.g., ['So11111111111111111111111111111111111111112'] for SOL)",
                                "default": [],
                            },
                            "include_pool_token_pairs": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of token pairs to include (e.g., ['USDC-SOL'])",
                                "default": [],
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_dlmm_pools",
                    "description": "Search for DLMM pools on Meteora",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of pools to return",
                                "default": 10,
                            },
                            "include_pool_token_pairs": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of token pairs to include",
                                "default": [],
                            },
                            "include_token_mints": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional array of token mint addresses to include",
                                "default": [],
                            },
                        },
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_trending_dlmm_pools(self, limit: int = 10, include_pool_token_pairs: List[str] = None) -> Dict:
        """
        Fetches trending DLMM pools from Meteora

        Args:
            limit: Maximum number of pools to return
            include_pool_token_pairs: Optional array of token pairs to include

        Returns:
            Dict containing trending pools or error information
        """
        try:
            action = f"Meteora/{self.meteora_trending_id}/getTrendingDLMMPools"
            payload = {
                "limit": limit,
                "include_pool_token_pairs": include_pool_token_pairs or [],
            }

            data = {"action": action, "payload": payload}

            logger.info(f"Fetching trending DLMM pools with limit {limit}")

            result = await self._api_request(url=self.api_endpoint, method="POST", headers=self.headers, json_data=data)

            if "error" in result:
                logger.error(f"API error: {result['error']}")
                return {"status": "error", "error": result["error"]}

            logger.info("Successfully fetched trending DLMM pools")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Error fetching trending DLMM pools: {str(e)}")
            return {"status": "error", "error": f"Failed to get trending DLMM pools: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_dynamic_amm_pools(
        self,
        limit: int = 10,
        include_token_mints: List[str] = None,
        include_pool_token_pairs: List[str] = None,
    ) -> Dict:
        """
        Searches for dynamic AMM pools on Meteora

        Args:
            limit: Number of pools to return
            include_token_mints: Optional array of token mint addresses to include
            include_pool_token_pairs: Optional array of token pairs to include

        Returns:
            Dict containing pool search results or error information
        """
        try:
            action = f"Meteora/{self.meteora_search_id}/searchDynamicAmmPools"
            payload = {
                "size": limit,
                "page": 0,
                "order_by": "desc",
                "sort_key": "fee_tvl_ratio",
                "hide_low_tvl": 100000,
                "hide_low_apr": True,
                "include_pool_token_pairs": include_pool_token_pairs or [],
                "include_token_mints": include_token_mints or [],
            }

            data = {"action": action, "payload": payload}

            logger.info(f"Searching dynamic AMM pools with size {limit}")

            result = await self._api_request(url=self.api_endpoint, method="POST", headers=self.headers, json_data=data)

            if "error" in result:
                logger.error(f"API error: {result['error']}")
                return {"status": "error", "error": result["error"]}

            logger.info("Successfully searched dynamic AMM pools")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Error searching dynamic AMM pools: {str(e)}")
            return {"status": "error", "error": f"Failed to search dynamic AMM pools: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_dlmm_pools(
        self,
        limit: int = 10,
        include_pool_token_pairs: List[str] = None,
        include_token_mints: List[str] = None,
    ) -> Dict:
        """
        Searches for DLMM pools on Meteora

        Args:
            limit: Number of pools to return
            include_pool_token_pairs: Optional array of token pairs to include
            include_token_mints: Optional array of token mint addresses to include

        Returns:
            Dict containing pool search results or error information
        """
        try:
            action = f"Meteora/{self.meteora_search_id}/searchDlmmPools"
            payload = {
                "limit": limit,
                "page": 0,
                "order_by": "desc",
                "sort_key": "tvl",
                "hide_low_tvl": 1000,
                "hide_low_apr": False,
                "include_pool_token_pairs": include_pool_token_pairs or [],
                "include_token_mints": include_token_mints or [],
            }

            data = {"action": action, "payload": payload}

            logger.info(f"Searching DLMM pools with limit {limit}")

            result = await self._api_request(url=self.api_endpoint, method="POST", headers=self.headers, json_data=data)

            if "error" in result:
                logger.error(f"API error: {result['error']}")
                return {"status": "error", "error": result["error"]}

            logger.info("Successfully searched DLMM pools")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Error searching DLMM pools: {str(e)}")
            return {"status": "error", "error": f"Failed to search DLMM pools: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution logic"""
        if tool_name == "get_trending_dlmm_pools":
            limit = function_args.get("limit", 10)
            include_pool_token_pairs = function_args.get("include_pool_token_pairs", [])

            result = await self.get_trending_dlmm_pools(limit=limit, include_pool_token_pairs=include_pool_token_pairs)

            if result.get("status") == "error":
                return {"error": result.get("error", "Failed to get trending DLMM pools")}

            return result.get("data", {})

        elif tool_name == "search_dynamic_amm_pools":
            limit = function_args.get("limit", 10)
            include_token_mints = function_args.get("include_token_mints", [])
            include_pool_token_pairs = function_args.get("include_pool_token_pairs", [])

            result = await self.search_dynamic_amm_pools(
                limit=limit,
                include_token_mints=include_token_mints,
                include_pool_token_pairs=include_pool_token_pairs,
            )

            if result.get("status") == "error":
                return {"error": result.get("error", "Failed to search dynamic AMM pools")}

            return result.get("data", {})

        elif tool_name == "search_dlmm_pools":
            limit = function_args.get("limit", 10)
            include_pool_token_pairs = function_args.get("include_pool_token_pairs", [])
            include_token_mints = function_args.get("include_token_mints", [])

            result = await self.search_dlmm_pools(
                limit=limit,
                include_pool_token_pairs=include_pool_token_pairs,
                include_token_mints=include_token_mints,
            )

            if result.get("status") == "error":
                return {"error": result.get("error", "Failed to search DLMM pools")}

            return result.get("data", {})

        else:
            return {"error": f"Unsupported tool: {tool_name}"}
