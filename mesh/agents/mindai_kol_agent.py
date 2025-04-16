import logging
import os
from typing import Any, Dict, List

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
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about crypto KOLs, tokens, or performance metrics.",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, return only raw data without natural language response.",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of the KOL and token analysis.",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured data from Mind AI API.", "type": "dict"},
                ],
                "external_apis": ["Mind AI"],
                "tags": ["KOL"],
                "recommended": True,
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

        When analyzing KOLs and tokens:
        1. Summarize the overall performance metrics
        2. Highlight key insights from the data
        3. Present the information in a clear, structured format
        4. Explain ROA (Return on Assets) and other metrics in simple terms

        Focus on delivering factual information and insights that help users understand:
        - Which KOLs are performing well
        - Which tokens are trending or gaining value
        - Historical performance of specific KOLs or tokens
        - Best initial calls for particular tokens or by specific KOLs

        Keep your responses concise and data-driven while making the information accessible.
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
    async def best_initial_call(
        self, period: int = 168, token_category: str = None, kol_name: str = None, token_symbol: str = None
    ) -> Dict:
        """Fetch best initial calls with optional filters."""
        endpoint = "/api/v1/best-initial-call"
        params = {
            "period": period,
            "sortBy": "RoaAtCurrPrice",
            **({"tokenCategory": token_category} if token_category else {}),
            **({"kolName": kol_name} if kol_name else {}),
            **({"tokenSymbol": token_symbol.lower()} if token_symbol else {}),
        }

        url = f"{self.base_url}{endpoint}"

        try:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching best initial calls: %s", e)
            return {"error": f"Failed to fetch best initial calls: {e}"}
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return {"error": f"Unexpected error: {e}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def kol_statistics(self, period: int = 168, kol_name: str = None) -> Dict:
        """Fetch KOL statistics with optional KOL name."""
        endpoint = "/api/v1/kol-stats"
        params = {
            "period": period,
            **({"kolName": kol_name} if kol_name else {}),
        }

        url = f"{self.base_url}{endpoint}"

        try:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching KOL statistics: %s", e)
            return {"error": f"Failed to fetch KOL statistics: {e}"}
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return {"error": f"Unexpected error: {e}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def token_statistics(self, period: int = 168, token_symbol: str = None) -> Dict:
        """Fetch token statistics with optional token symbol."""
        endpoint = "/api/v1/token-stats"
        params = {
            "period": period,
            **({"tokenSymbol": token_symbol.lower()} if token_symbol else {}),
        }
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching token statistics: %s", e)
            return {"error": f"Failed to fetch token statistics: {e}"}
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return {"error": f"Unexpected error: {e}"}

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
        url = f"{self.base_url}{endpoint}"
        try:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching top gainers: %s", e)
            return {"error": f"Failed to fetch top gainers: {e}"}
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return {"error": f"Unexpected error: {e}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle tool execution and return results."""
        tool_functions = {
            "get_best_initial_calls": self.best_initial_call,
            "get_kol_statistics": self.kol_statistics,
            "get_token_statistics": self.token_statistics,
            "get_top_gainers": self.top_gainers,
        }

        if tool_name not in tool_functions:
            return {"error": f"Unsupported tool: {tool_name}"}

        period = function_args.get("period", 168)

        if tool_name == "get_best_initial_calls":
            result = await tool_functions[tool_name](
                period,
                function_args.get("token_category"),
                function_args.get("kol_name"),
                function_args.get("token_symbol"),
            )

        elif tool_name == "get_kol_statistics":
            result = await tool_functions[tool_name](period, function_args.get("kol_name"))

        elif tool_name == "get_token_statistics":
            token_symbol = function_args.get("token_symbol")
            if not token_symbol:
                return {"error": "Missing 'token_symbol' in tool_arguments"}
            result = await tool_functions[tool_name](period, token_symbol)

        elif tool_name == "get_top_gainers":
            result = await tool_functions[tool_name](
                period,
                function_args.get("token_category", "top100"),
                function_args.get("tokens_amount", 5),
                function_args.get("kols_amount", 3),
            )

        errors = self._handle_error(result)
        return errors if errors else result
