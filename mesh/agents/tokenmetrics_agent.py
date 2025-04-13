import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import requests
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
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides market insights, sentiment analysis, and resistance/support data for cryptocurrencies using TokenMetrics API.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about market sentiment or token analysis",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, returns only raw data without analysis",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language analysis of token metrics data",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured data from TokenMetrics API",
                        "type": "dict",
                    },
                ],
                "external_apis": ["TokenMetrics"],
                "tags": ["Market Analysis"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/TokenMetrics.png",
                "examples": [
                    "What is the current market sentiment?",
                    "Show me resistance and support levels for BTC and ETH",
                    "Get the latest sentiment analysis for top cryptocurrencies",
                    "What are the key support and resistance levels for Bitcoin?",
                    "What's the sentiment for Solana (SOL)?",
                    "Show me resistance levels for HEU token",
                    "What is the current market sentiment for top cryptocurrencies?",
                    "Can you show me the top 5 cryptocurrencies by market feeling?",
                    "What are the key resistance and support levels for Bitcoin and Ethereum?",
                    "What are the resistance and support levels for Solana (SOL)?",
                    "What's the current sentiment for Heurist token?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a cryptocurrency market analyst specializing in technical analysis and sentiment data.
        You provide insights based on data from TokenMetrics, a leading crypto analytics platform.

        When analyzing sentiment data:
        1. Summarize the overall market sentiment (bullish, bearish, or neutral)
        2. Highlight tokens with notably positive or negative sentiment
        3. Identify any significant sentiment shifts compared to previous periods
        4. Provide context on what the sentiment data might mean for investors

        When analyzing resistance and support levels:
        1. Explain the current price in relation to resistance/support zones
        2. Identify key price levels that traders should watch
        3. Note when a token is testing significant support or resistance
        4. Suggest what the technical setup might indicate for short-term price action

        Your analysis should be:
        - Clear and concise
        - Focused on data rather than speculation
        - Suitable for both beginner and advanced crypto traders
        - Careful to note that this is analysis, not financial advice

        IMPORTANT: When a user asks about sentiment, feeling, or mood of the market, always use the get_sentiments tool.
        The default number of results should be 10 unless explicitly specified by the user.

        When a user asks about a specific token other than BTC or ETH:
        1. First use get_token_info internally to find the token's ID (don't explain this step)
        2. Then use that ID for any further analysis with other tools
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_sentiments",
                    "description": "Retrieves market sentiment data for cryptocurrencies from TokenMetrics. This tool provides sentiment analysis that indicates whether the market or specific tokens are trending bullish or bearish. Use this for understanding the current market sentiment and help with investment decisions.",
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
                    "description": "Retrieves resistance and support level data for specified cryptocurrencies. This tool provides technical analysis data showing key price levels where tokens might encounter buying or selling pressure. Use this for technical analysis and identifying potential trade entry/exit points.",
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
        ]

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_token_info(
        self, token_name: Optional[str] = None, token_symbol: Optional[str] = None, limit: int = 20
    ) -> Dict:
        """
        Retrieves token information from TokenMetrics API using token name or symbol.
        Returns the token ID for use in other API calls.
        This is an internal method and should not be exposed as a tool.
        """
        try:
            params = {"limit": limit}

            if token_name:
                params["token_name"] = token_name.lower()
            if token_symbol:
                params["token_symbol"] = token_symbol.upper()

            url = f"{self.base_url}/tokens"

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            token_data = response.json()

            return {"status": "success", "data": token_data}
        except requests.RequestException as e:
            logger.error(f"Error getting token information: {e}")
            return {"error": f"Failed to get token information: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_sentiments(self, limit: int = 10, page: int = 0) -> Dict:
        """
        Retrieves market sentiment data from TokenMetrics API.
        Filters results to only include Twitter-related fields.
        """
        try:
            params = {"limit": limit, "page": page}
            url = f"{self.base_url}/sentiments"

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            sentiments_data = response.json()

            # Extract only Twitter-related fields from each record
            if "data" in sentiments_data and isinstance(sentiments_data["data"], list):
                twitter_sentiments = []
                for record in sentiments_data["data"]:
                    twitter_fields = {
                        "DATETIME": record.get("DATETIME"),
                        "TWITTER_SENTIMENT_GRADE": record.get("TWITTER_SENTIMENT_GRADE"),
                        "TWITTER_SENTIMENT_LABEL": record.get("TWITTER_SENTIMENT_LABEL"),
                        "TWITTER_SUMMARY": record.get("TWITTER_SUMMARY"),
                    }
                    # Only include records that have Twitter sentiment data
                    if twitter_fields["TWITTER_SENTIMENT_GRADE"] is not None:
                        twitter_sentiments.append(twitter_fields)

                sentiments_data["data"] = twitter_sentiments

                if "metadata" in sentiments_data and "record_count" in sentiments_data["metadata"]:
                    sentiments_data["metadata"]["record_count"] = len(twitter_sentiments)

            return {"status": "success", "data": sentiments_data}
        except requests.RequestException as e:
            logger.error(f"Error getting sentiments: {e}")
            return {"error": f"Failed to get market sentiments: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_resistance_support_levels(
        self, token_ids: str = "3375,3306", symbols: str = "BTC,ETH", limit: int = 10, page: int = 0
    ) -> Dict:
        """
        Retrieves resistance and support level data for specified cryptocurrencies.
        """
        try:
            params = {"token_id": token_ids, "symbol": symbols, "limit": limit, "page": page}
            url = f"{self.base_url}/resistance-support"

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            res_sup_data = response.json()

            return {"status": "success", "data": res_sup_data}
        except requests.RequestException as e:
            logger.error(f"Error getting resistance & support data: {e}")
            return {"error": f"Failed to get resistance & support data: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      HELPER METHODS FOR TOKEN HANDLING
    # ------------------------------------------------------------------------
    async def extract_token_id_from_response(
        self, response_data: Dict, search_name: Optional[str] = None, search_symbol: Optional[str] = None
    ) -> Optional[int]:
        """
        Extracts token ID from response data.
        If multiple tokens match, returns the first one that matches the search criteria.
        """
        if "status" not in response_data or response_data["status"] != "success":
            logger.error(f"Invalid response data: {response_data}")
            return None
        if "data" not in response_data or "data" not in response_data["data"]:
            logger.error(f"No data in response: {response_data}")
            return None
        tokens = response_data["data"]["data"]
        if not tokens:
            logger.warning("No tokens found in response")
            return None
        for token in tokens:
            if search_name and token.get("TOKEN_NAME") == search_name:
                return token.get("TOKEN_ID")
            if search_symbol and token.get("TOKEN_SYMBOL") == search_symbol:
                return token.get("TOKEN_ID")
        if tokens:
            return tokens[0].get("TOKEN_ID")

        return None

    async def extract_tokens_from_query(self, query: str) -> List[str]:
        """
        Extracts token names or symbols from a user query.
        Returns a list of possible token identifiers.
        """
        import re

        default_tokens = {"btc", "bitcoin", "eth", "ethereum"}
        pattern1 = r"(\w+)\s*\((\w+)\)"
        pattern2 = r"\b(solana|cardano|ripple|xrp|bnb|ada|dot|avax|sol|heu|doge|shib|link|matic)\b"

        tokens = []

        for match in re.finditer(pattern1, query.lower()):
            name, symbol = match.groups()
            if name not in default_tokens and symbol not in default_tokens:
                tokens.append({"name": name, "symbol": symbol})
        for match in re.finditer(pattern2, query.lower()):
            token = match.group(1)
            if token not in default_tokens and not any(
                t.get("name") == token or t.get("symbol") == token for t in tokens
            ):
                tokens.append({"name": token})

        return tokens

    async def process_custom_tokens(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Processes a query to identify custom tokens.
        Returns token_ids and symbols for use in API calls.
        """
        tokens = await self.extract_tokens_from_query(query)

        if not tokens:
            return None, None

        token_ids = []
        symbols = []

        for token_info in tokens:
            if "symbol" in token_info:
                token_resp = await self.get_token_info(token_symbol=token_info["symbol"])
                token_id = await self.extract_token_id_from_response(token_resp, search_symbol=token_info["symbol"])

                if token_id:
                    token_ids.append(str(token_id))
                    symbols.append(token_info["symbol"].upper())
                    continue

            if "name" in token_info:
                token_resp = await self.get_token_info(token_name=token_info["name"])
                token_id = await self.extract_token_id_from_response(token_resp, search_name=token_info["name"])

                if token_id:
                    token_ids.append(str(token_id))
                    # Get the symbol from response
                    if "data" in token_resp and "data" in token_resp["data"] and token_resp["data"]["data"]:
                        for t in token_resp["data"]["data"]:
                            if t.get("TOKEN_ID") == token_id:
                                symbols.append(t.get("TOKEN_SYMBOL", "").upper())
                                break

        if not token_ids:
            return "3375,3306", "BTC,ETH"

        if len(token_ids) == 1:
            token_ids.append("3375")
            symbols.append("BTC")

        token_ids = token_ids[:2]
        symbols = symbols[:2]

        return ",".join(token_ids), ",".join(symbols)

    # ------------------------------------------------------------------------
    #                      MESH AGENT REQUIRED METHOD
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        This method is required by the MeshAgent abstract base class.
        """
        if tool_name == "get_sentiments":
            limit = function_args.get("limit", 10)
            page = function_args.get("page", 0)

            logger.info(f"Getting market sentiments with limit={limit}, page={page}")
            result = await self.get_sentiments(limit=limit, page=page)

            errors = self._handle_error(result)
            if errors:
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

            errors = self._handle_error(result)
            if errors:
                return errors

            return result

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

    async def _before_handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called before message handling.
        Allows for modification of parameters before they're processed.
        Processes custom tokens in the query if present.
        """
        query = params.get("query")

        if query:
            if self._should_use_sentiment_tool(query):
                limit = self._extract_limit_from_query(query)
                logger.info(f"Auto-detected sentiment query, sentiment keywords found with limit={limit}")
            custom_token_ids, custom_symbols = await self.process_custom_tokens(query)
            if custom_token_ids and custom_symbols:
                logger.info(f"Detected custom tokens: IDs={custom_token_ids}, Symbols={custom_symbols}")
                params["custom_token_ids"] = custom_token_ids
                params["custom_symbols"] = custom_symbols

        return super()._before_handle_message(params)

    async def _after_handle_message(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Hook called after message handling.
        Allows for modification of the response before it's returned to the caller.
        """
        return super()._after_handle_message(response)

    def _should_use_sentiment_tool(self, query: str) -> bool:
        """
        Determines if the query is asking about sentiment, feeling, or mood.
        """
        query_lower = query.lower()
        sentiment_keywords = [
            "sentiment",
            "feeling",
            "mood",
            "emotion",
            "attitude",
            "bullish",
            "bearish",
            "positive",
            "negative",
            "outlook",
            "optimistic",
            "pessimistic",
            "market sentiment",
        ]
        return any(keyword in query_lower for keyword in sentiment_keywords)

    def _extract_limit_from_query(self, query: str) -> int:
        """
        Extract limit number from a query if present, otherwise return default 10.
        """
        import re

        # Look for patterns like "top 5", "show me 20", "get 15", etc.
        patterns = [
            r"top\s+(\d+)",
            r"show\s+(?:me\s+)?(\d+)",
            r"get\s+(\d+)",
            r"limit\s+(?:to\s+)?(\d+)",
            r"(\d+)\s+results",
            r"(\d+)\s+tokens",
            r"(\d+)\s+coins",
            r"(\d+)\s+cryptocurrencies",
        ]

        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                try:
                    limit = int(match.group(1))
                    return limit
                except ValueError:
                    pass

        # Return default if no pattern matched
        return 10
