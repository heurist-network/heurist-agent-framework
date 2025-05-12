import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class TokenMetricsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("TOKENMETRICS_API_KEY")
        if not self.api_key:
            raise ValueError("TOKENMETRICS_API_KEY is not set in the environment.")

        self.base_url = "https://api.tokenmetrics.com/v2"
        self.headers = {"accept": "application/json", "api_key": self.api_key}

        self.metadata.update(
            {
                "name": "TokenMetrics Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides market insights, sentiment analysis, and resistance/support data for cryptocurrencies using TokenMetrics API.",
                "external_apis": ["TokenMetrics"],
                "tags": ["Market Analysis"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/TokenMetrics.png",
                "examples": [
                    "What is the current crypto market sentiment?",
                    "Show me resistance and support levels for ETH",
                    "resistance and support levels for Solana",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a cryptocurrency market analyst specializing in technical analysis and sentiment data.
        You provide insights based on data from TokenMetrics, a leading crypto analytics platform.

        AVAILABLE TOOLS:

        1. get_sentiments:
           - This tool ONLY provides GENERAL MARKET SENTIMENT, not token-specific sentiment.
           - Use when user asks about overall market mood or sentiment trends.
           - The data includes Twitter sentiment grades, labels, and summaries about the crypto market as a whole.
           - IMPORTANT: This tool cannot provide sentiment specifically about individual tokens.

        2. get_resistance_support_levels:
           - This tool provides technical analysis data (support/resistance levels) for SPECIFIC tokens.
           - Use when user asks about price targets, entry/exit points, or trading ranges.
           - You can specify token_ids or symbols to get data for specific cryptocurrencies.

        3. get_token_info:
           - Use this tool to look up token information including their IDs.
           - Helpful when user mentions tokens by name and you need to find their token_id for other tools.

        RESPONSE GUIDELINES:

        - Be transparent about limitations: If a user asks for token-specific sentiment but only general market sentiment is available, clearly explain this limitation.
        - Properly interpret results: Distinguish between general market sentiment and token-specific data.
        - Be clear and concise, focusing on data rather than speculation.
        - Format your responses to be suitable for both beginner and advanced crypto traders.

        When handling queries about specific tokens:
        - If the query is about sentiment for a specific token, clearly explain that get_sentiments provides general market sentiment, not token-specific sentiment.
        - When appropriate, suggest using get_resistance_support_levels instead for token-specific technical analysis.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_sentiments",
                    "description": "Retrieves GENERAL market sentiment data for the ENTIRE cryptocurrency market from TokenMetrics. IMPORTANT: This tool only returns general market sentiment, NOT the sentiment of any specific token. Use for questions about overall market mood.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 10)",
                                "default": 10,
                            },
                            "page": {
                                "type": "number",
                                "description": "Page number for pagination (default: 0)",
                                "default": 0,
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_resistance_support_levels",
                    "description": "Retrieves resistance and support level data for specified cryptocurrencies. This tool provides token-specific technical analysis data showing key price levels where tokens might encounter buying or selling pressure. Use this for technical analysis of specific tokens.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_ids": {
                                "type": "string",
                                "description": "Comma-separated list of token IDs, limited to two tokens (e.g., '3375,3306' for BTC,ETH)",
                                "default": "3375,3306",
                            },
                            "symbols": {
                                "type": "string",
                                "description": "Comma-separated list of token symbols, limited to two tokens (e.g., 'BTC,ETH')",
                                "default": "BTC,ETH",
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 10)",
                                "default": 10,
                            },
                            "page": {
                                "type": "number",
                                "description": "Page number for pagination (default: 0)",
                                "default": 0,
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_info",
                    "description": "Retrieves token information from TokenMetrics API using token name or symbol. Returns the token ID for use in other API calls.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_name": {
                                "type": "string",
                                "description": "Name of the token to search for (e.g., 'bitcoin')",
                            },
                            "token_symbol": {
                                "type": "string",
                                "description": "Symbol of the token to search for (e.g., 'BTC')",
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 20)",
                                "default": 20,
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_token_info(
        self, token_name: Optional[str] = None, token_symbol: Optional[str] = None, limit: int = 20
    ) -> Dict:
        """
        Retrieves token information from TokenMetrics API using token name or symbol.
        Returns the token ID for use in other API calls.
        """
        try:
            params = {"limit": limit}

            if token_name:
                params["token_name"] = token_name.lower()
            if token_symbol:
                params["token_symbol"] = token_symbol.upper()

            url = f"{self.base_url}/tokens"

            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return response

            return {"status": "success", "data": response}

        except Exception as e:
            logger.error(f"Error getting token information: {e}")
            return {"error": f"Failed to get token information: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_sentiments(self, limit: int = 10, page: int = 0) -> Dict:
        try:
            params = {"limit": limit, "page": page}
            url = f"{self.base_url}/sentiments"

            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return response

            # Extract only Twitter-related fields from each record
            if "data" in response and isinstance(response["data"], list):
                twitter_sentiments = []
                for record in response["data"]:
                    twitter_fields = {
                        "DATETIME": record.get("DATETIME"),
                        "TWITTER_SENTIMENT_GRADE": record.get("TWITTER_SENTIMENT_GRADE"),
                        "TWITTER_SENTIMENT_LABEL": record.get("TWITTER_SENTIMENT_LABEL"),
                        "TWITTER_SUMMARY": record.get("TWITTER_SUMMARY"),
                    }
                    # Only include records that have Twitter sentiment data
                    if twitter_fields["TWITTER_SENTIMENT_GRADE"] is not None:
                        twitter_sentiments.append(twitter_fields)

                response["data"] = twitter_sentiments

                if "metadata" in response and "record_count" in response["metadata"]:
                    response["metadata"]["record_count"] = len(twitter_sentiments)

            return {"status": "success", "data": response}

        except Exception as e:
            logger.error(f"Error getting sentiments: {e}")
            return {"error": f"Failed to get market sentiments: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_resistance_support_levels(
        self, token_ids: str = "3375,3306", symbols: str = "BTC,ETH", limit: int = 10, page: int = 0
    ) -> Dict:
        try:
            params = {"limit": limit, "page": page}

            # If custom symbols are provided (different from default), use only those
            if symbols != "BTC,ETH":
                params["symbol"] = symbols
            # If custom token_ids are provided (different from default), use only those
            elif token_ids != "3375,3306":
                params["token_id"] = token_ids
            # If no custom values are provided, use defaults
            else:
                params["symbol"] = symbols
                params["token_id"] = token_ids

            url = f"{self.base_url}/resistance-support"

            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return response

            return {"status": "success", "data": response}

        except Exception as e:
            logger.error(f"Error getting resistance & support data: {e}")
            return {"error": f"Failed to get resistance & support data: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      MESH AGENT REQUIRED METHOD
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        This method is required by the MeshAgent abstract base class.
        """
        if tool_name == "get_sentiments":
            limit = function_args.get("limit", 10)
            page = function_args.get("page", 0)

            logger.info(f"Getting market sentiments with limit={limit}, page={page}")
            result = await self.get_sentiments(limit=limit, page=page)

            if errors := self._handle_error(result):
                return errors

            return result

        elif tool_name == "get_resistance_support_levels":
            token_ids = function_args.get("token_ids", "3375,3306")
            symbols = function_args.get("symbols", "BTC,ETH")
            limit = function_args.get("limit", 10)
            page = function_args.get("page", 0)

            logger.info(f"Getting resistance & support data for {symbols} with limit={limit}, page={page}")
            result = await self.get_resistance_support_levels(
                token_ids=token_ids, symbols=symbols, limit=limit, page=page
            )

            if errors := self._handle_error(result):
                return errors

            return result

        elif tool_name == "get_token_info":
            token_name = function_args.get("token_name")
            token_symbol = function_args.get("token_symbol")
            limit = function_args.get("limit", 20)

            if not token_name and not token_symbol:
                return {"error": "Either token_name or token_symbol must be provided"}

            logger.info(f"Getting token info for name={token_name}, symbol={token_symbol}")
            result = await self.get_token_info(token_name=token_name, token_symbol=token_symbol, limit=limit)

            if errors := self._handle_error(result):
                return errors

            return result

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}
