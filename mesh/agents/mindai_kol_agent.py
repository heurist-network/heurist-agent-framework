import logging
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class MindAiKolAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("MINDAI_API_KEY")
        if not self.api_key:
            raise ValueError("MINDAI_API_KEY environment variable is required")

        self.base_url = "https://app.mind-ai.io"
        self.headers = {"accept": "application/json", "x-api-key": self.api_key}

        self.metadata.update(
            {
                "name": "Mind AI KOL Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes Key Opinion Leaders (KOLs) and token performance in the crypto space using Mind AI API.",
                "external_apis": ["Mind AI"],
                "tags": ["KOL"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/MindAI.png",
                "examples": [
                    "Find the best initial calls for HEU token",
                    "What are the statistics for KOL @agentcookiefun?",
                    "Show me the top gainers in the past week",
                    "Get token statistics for ETH in the last month",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a crypto KOL analyst that provides insights on crypto Key Opinion Leaders (KOLs) and token performance based on Mind AI data.

        Focus on delivering factual information and insights that help users understand:
        - Which KOLs are performing well
        - Which tokens are trending or gaining value
        - Historical performance of specific KOLs or tokens
        - Best initial calls for particular tokens or by specific KOLs

        Keep your responses concise and data-driven while making the information accessible. NEVER make up data that is not returned from the tool.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_best_initial_calls",
                    "description": "Get the best initial calls for a specific token or from a specific KOL. ROA means Return on Assets, which measures the performance of a token call by a KOL. This tool returns data about which KOLs made the best early calls on tokens and their return metrics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "period": {
                                "type": "integer",
                                "description": "Time period in hours to look back (default: 168 hours/7 days)",
                                "default": 168,
                            },
                            "token_category": {
                                "type": "string",
                                "description": "Optional category of tokens to consider: 'top100', 'top500', or 'lowRank'",
                                "enum": ["top100", "top500", "lowRank"],
                            },
                            "kol_name": {
                                "type": "string",
                                "description": "Name of the KOL to filter by (e.g., '@agentcookiefun')",
                            },
                            "token_symbol": {
                                "type": "string",
                                "description": "Symbol of the token to filter by (e.g., 'BTC', 'ETH')",
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_kol_statistics",
                    "description": "Get performance statistics for KOLs. This tool provides metrics on KOL performance across multiple tokens and time periods. ROA means Return on Assets, which measures the performance of token calls by KOLs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "period": {
                                "type": "integer",
                                "description": "Time period in hours to look back (default: 168 hours/7 days)",
                                "default": 168,
                            },
                            "kol_name": {
                                "type": "string",
                                "description": "Name of the KOL to get statistics for (e.g., '@agentcookiefun')",
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_statistics",
                    "description": "Get performance statistics for tokens. This tool provides metrics on token performance and which KOLs have called them. ROA means Return on Assets, which measures the performance of tokens after being called by KOLs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "period": {
                                "type": "integer",
                                "description": "Time period in hours to look back (default: 168 hours/7 days)",
                                "default": 168,
                            },
                            "token_symbol": {
                                "type": "string",
                                "description": "Symbol of the token to get statistics for (e.g., 'BTC', 'ETH')",
                            },
                        },
                        "required": ["token_symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_gainers",
                    "description": "Get top gaining tokens and the KOLs who called them. This tool identifies which tokens have gained the most value and which KOLs made the best calls. ROA means Return on Assets, which measures the performance of tokens after being called by KOLs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "period": {
                                "type": "integer",
                                "description": "Time period in hours to look back (default: 168 hours/7 days)",
                                "default": 168,
                            },
                            "token_category": {
                                "type": "string",
                                "description": "Category of tokens to consider: 'top100', 'top500', or 'lowRank'",
                                "enum": ["top100", "top500", "lowRank"],
                                "default": "top100",
                            },
                            "tokens_amount": {
                                "type": "integer",
                                "description": "Number of top tokens to return (1-10)",
                                "default": 5,
                            },
                            "kols_amount": {
                                "type": "integer",
                                "description": "Number of KOLs to return per token (3-10)",
                                "default": 3,
                            },
                        },
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      MIND AI API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def make_api_request(self, endpoint: str, params: Dict) -> Dict:
        """Make a direct API request to the Mind AI API"""
        url = f"{self.base_url}{endpoint}"

        try:
            # Use direct synchronous request
            response = requests.get(url, headers=self.headers, params=params)
            logger.info(f"Request URL: {response.url}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def best_initial_call(
        self, period: int = 720, token_category: str = None, kol_name: str = None, token_symbol: str = None
    ) -> Dict:
        """Fetch best initial calls with optional filters."""
        endpoint = "/api/v1/best-initial-call"
        params = {"period": period, "sortBy": "RoaAtCurrPrice"}

        if token_symbol:
            params["tokenSymbol"] = token_symbol.upper()
        if token_category:
            params["tokenCategory"] = token_category
        if kol_name:
            params["kolName"] = kol_name

        return await self.make_api_request(endpoint, params)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def kol_statistics(self, period: int = 168, kol_name: str = None) -> Dict:
        """Fetch KOL statistics with optional KOL name."""
        endpoint = "/api/v1/kol-stats"
        params = {"period": period}

        if kol_name:
            params["kolName"] = kol_name

        return await self.make_api_request(endpoint, params)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def token_statistics(self, period: int = 168, token_symbol: str = None) -> Dict:
        """Fetch token statistics with optional token symbol."""
        endpoint = "/api/v1/token-stats"
        params = {"period": period}

        if token_symbol:
            params["tokenSymbol"] = token_symbol.upper()

        return await self.make_api_request(endpoint, params)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def top_gainers(
        self, period: int = 168, token_category: str = "top100", tokens_amount: int = 5, kols_amount: int = 3
    ) -> Dict:
        """Fetch top gaining tokens and the KOLs who called them."""
        kols_amount = max(3, min(kols_amount, 10))
        endpoint = "/api/v1/top-gainers-token"
        params = {
            "period": period,
            "tokenCategory": token_category,
            "tokensAmount": tokens_amount,
            "kolsAmount": kols_amount,
        }

        return await self.make_api_request(endpoint, params)

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        if tool_name == "get_best_initial_calls":
            period = function_args.get("period", 720)  # Default to 720 hours (30 days) for best initial calls
            token_category = function_args.get("token_category")
            kol_name = function_args.get("kol_name")
            token_symbol = function_args.get("token_symbol")

            logger.info(f"Fetching best initial calls for token: {token_symbol}, period: {period}")
            result = await self.best_initial_call(
                period=period, token_category=token_category, kol_name=kol_name, token_symbol=token_symbol
            )

        elif tool_name == "get_kol_statistics":
            period = function_args.get("period", 168)
            kol_name = function_args.get("kol_name")

            logger.info(f"Fetching KOL statistics for: {kol_name}, period: {period}")
            result = await self.kol_statistics(period=period, kol_name=kol_name)

        elif tool_name == "get_token_statistics":
            period = function_args.get("period", 168)
            token_symbol = function_args.get("token_symbol")

            if not token_symbol:
                return {"error": "Missing 'token_symbol' in tool arguments"}

            logger.info(f"Fetching token statistics for: {token_symbol}, period: {period}")
            result = await self.token_statistics(period=period, token_symbol=token_symbol)

        elif tool_name == "get_top_gainers":
            period = function_args.get("period", 168)
            token_category = function_args.get("token_category", "top100")
            tokens_amount = function_args.get("tokens_amount", 5)
            kols_amount = function_args.get("kols_amount", 3)

            logger.info(f"Fetching top gainers for category: {token_category}, period: {period}")
            result = await self.top_gainers(
                period=period, token_category=token_category, tokens_amount=tokens_amount, kols_amount=kols_amount
            )

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

        if errors := self._handle_error(result):
            return errors

        return result
