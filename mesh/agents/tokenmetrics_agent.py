import json
import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
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
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/tokenmetrics.png",
                "examples": [
                    "What is the current market sentiment?",
                    "Show me resistance and support levels for BTC and ETH",
                    "Get the latest sentiment analysis for top cryptocurrencies",
                    "What are the key support and resistance levels for Bitcoin?",
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
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    async def _respond_with_llm(self, query: str, tool_call_id: str, data: dict, temperature: float) -> str:
        """
        Reusable helper to ask the LLM to generate a user-friendly explanation
        given a piece of data from a tool call.
        """
        return await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query},
                {"role": "tool", "content": str(data), "tool_call_id": tool_call_id},
            ],
            temperature=temperature,
        )

    def _handle_error(self, maybe_error: dict) -> dict:
        """
        Small helper to return the error if present in
        a dictionary with the 'error' key.
        """
        if "error" in maybe_error:
            return {"error": maybe_error["error"]}
        return {}

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

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_sentiments(self, limit: int = 10, page: int = 0) -> Dict:
        """
        Retrieves market sentiment data from TokenMetrics API.
        Filters results to only include records with the 'TWITTER' prefix.
        """
        try:
            params = {"limit": limit, "page": page}
            url = f"{self.base_url}/sentiments"

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            sentiments_data = response.json()

            # filter the results to only include records with the 'TWITTER' prefix
            if "data" in sentiments_data and isinstance(sentiments_data["data"], list):
                twitter_sentiments = [record for record in sentiments_data["data"] if record.get("prefix") == "TWITTER"]
                sentiments_data["data"] = twitter_sentiments

                if "metadata" in sentiments_data and "record_count" in sentiments_data["metadata"]:
                    sentiments_data["metadata"]["record_count"] = len(twitter_sentiments)

            return {"status": "success", "data": sentiments_data}
        except requests.RequestException as e:
            logger.error(f"Error getting sentiments: {e}")
            return {"status": "error", "error": f"Failed to get market sentiments: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

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
            return {"status": "error", "error": f"Failed to get resistance & support data: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle direct tool calls with proper error handling and response formatting
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
            return {"status": "error", "error": f"Unsupported tool '{tool_name}'"}

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

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle both direct tool calls and natural language queries.
        Either 'query' or 'tool' must be provided in params.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
            return {"response": "", "data": data}

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY (LLM decides the tool)
        # ---------------------
        if query:
            if self._should_use_sentiment_tool(query):
                limit = self._extract_limit_from_query(query)

                logger.info(f"Auto-detected sentiment query, using get_sentiments with limit={limit}")
                data = await self._handle_tool_logic(
                    tool_name="get_sentiments", function_args={"limit": limit, "page": 0}
                )

                if raw_data_only:
                    return {"response": "", "data": data}

                tool_call_id = "auto_detected_sentiment_tool_call"
                explanation = await self._respond_with_llm(
                    query=query, tool_call_id=tool_call_id, data=data, temperature=0.3
                )
                return {"response": explanation, "data": data}

            response = await call_llm_with_tools_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                user_prompt=query,
                temperature=0.1,
                tools=self.get_tool_schemas(),
            )

            if not response:
                return {"status": "error", "error": "Failed to process query"}
            tool_calls = response.get("tool_calls")
            if not tool_calls:
                return {"response": response.get("content", "No response content"), "data": {}}

            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                tool_call = tool_calls[0]
            else:
                tool_call = tool_calls

            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            if "limit" not in tool_call_args:
                limit = self._extract_limit_from_query(query)
                tool_call_args["limit"] = limit

            data = await self._handle_tool_logic(tool_name=tool_call_name, function_args=tool_call_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call.id, data=data, temperature=0.3
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"status": "error", "error": "Either 'query' or 'tool' must be provided in the parameters."}
