import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class CoinGeckoTokenInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.coingecko.com/api/v3"
        self.headers = {"Authorization": f"Bearer {os.getenv('COINGECKO_API_KEY')}"}

        self.metadata.update(
            {
                "name": "CoinGecko Token Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch token information, market data, trending coins, and category data from CoinGecko.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about a token (you can use the token name or symbol or ideally the CoinGecko ID if you have it, but NOT the token address), or a request for trending coins. ",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw or base structured data without additional LLM explanation.",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of the token information (empty if a direct tool call).",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured token information, trending coins data, or category data.",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Coingecko"],
                "tags": ["Trading", "Data"],
            }
        )

    def get_system_prompt(self) -> str:
        return """
    IDENTITY:
    You are a crypto data specialist that can fetch token information and category data from CoinGecko.

    CAPABILITIES:
    - Search and retrieve token details
    - Get current trending coins
    - Analyze token market data
    - List crypto categories
    - Get tokens within specific categories
    - Compare tokens across categories

    RESPONSE GUIDELINES:
    - Keep responses focused on what was specifically asked
    - Format numbers in a human-readable way (e.g., "$150.4M")
    - Provide only relevant metrics for the query context

    DOMAIN-SPECIFIC RULES:
    For specific token queries, identify whether the user provided a CoinGecko ID directly or needs to search by token name or symbol. Coingecko ID is lowercase string and may contain dashes. If the user doesn't explicitly say the input is the CoinGecko ID, you should use get_coingecko_id to search for the token. Do not make up CoinGecko IDs.
    
    For trending coins requests, use the get_trending_coins tool to fetch the current top trending cryptocurrencies.
    
    For category-related requests:
    - Use get_categories_list to fetch all available categories
    - Use get_category_data to get market data for all categories
    - Use get_tokens_by_category to fetch tokens within a specific category

    When selecting tokens from search results, apply these criteria in order:
    1. First priority: Select the token where name or symbol perfectly matches the query
    2. If multiple matches exist, select the token with the highest market cap rank (lower number = higher rank)
    3. If market cap ranks are not available, prefer the token with the most complete information

    For comparison queries across tokens or categories, extract the relevant metrics and provide a comparative analysis.

    IMPORTANT:
    - Never invent or assume CoinGecko IDs or category IDs
    - Keep responses concise and relevant"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_coingecko_id",
                    "description": "Search for a token by name to get its CoinGecko ID. This tool helps you find the correct CoinGecko ID for any cryptocurrency when you only know its name or symbol. The CoinGecko ID is required for fetching detailed token information using other CoinGecko tools. Use this when you need to look up a token's identifier before requesting more detailed information. You can skip this tool if you have the CoinGecko ID already.",
                    "parameters": {
                        "type": "object",
                        "properties": {"token_name": {"type": "string", "description": "The token name to search for"}},
                        "required": ["token_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_info",
                    "description": "Get detailed token information and market data using CoinGecko ID. This tool provides comprehensive cryptocurrency data including current price, market cap, trading volume, price changes, supply information, and more. Use this when you need up-to-date information of a specific cryptocurrency. Note that you must use the token's CoinGecko ID (not its symbol or address) - you can find this ID using the get_coingecko_id tool if needed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "coingecko_id": {"type": "string", "description": "The CoinGecko ID of the token"}
                        },
                        "required": ["coingecko_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_trending_coins",
                    "description": "Get the current top trending cryptocurrencies on CoinGecko. This tool retrieves a list of the most popular cryptocurrencies based on trading volume and social media mentions. It provides key information about each trending coin such as name, symbol, market cap rank, and price data. Use this when you want to discover which cryptocurrencies are currently gaining the most attention in the market. Data is sourced directly from CoinGecko and represents real-time trends.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_categories_list",
                    "description": "Get a list of all available cryptocurrency categories from CoinGecko. This tool retrieves all the category IDs and names that can be used for further category-specific queries. Use this when you need to discover what categories exist or to find the correct category ID for another tool.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_category_data",
                    "description": "Get market data for all cryptocurrency categories from CoinGecko. This tool retrieves comprehensive information about all categories including market cap, volume, market cap change, top coins in each category, and more. Use this when you want to compare performance across different cryptocurrency sectors or understand market trends by category.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order": {
                                "type": "string",
                                "description": "Sort order for categories (default: market_cap_desc)",
                                "enum": [
                                    "market_cap_desc",
                                    "market_cap_asc",
                                    "name_desc",
                                    "name_asc",
                                    "market_cap_change_24h_desc",
                                    "market_cap_change_24h_asc",
                                ],
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_tokens_by_category",
                    "description": "Get a list of tokens within a specific category. This tool retrieves token data for all cryptocurrencies that belong to a particular category, including price, market cap, volume, and price changes. Use this when you want to explore or compare tokens within a specific sector of the cryptocurrency market.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category_id": {
                                "type": "string",
                                "description": "The CoinGecko category ID (e.g., 'layer-1')",
                            },
                            "vs_currency": {
                                "type": "string",
                                "description": "The currency to show results in (default: usd)",
                                "default": "usd",
                            },
                            "order": {
                                "type": "string",
                                "description": "Sort order for tokens (default: market_cap_desc)",
                                "enum": [
                                    "market_cap_desc",
                                    "market_cap_asc",
                                    "volume_desc",
                                    "volume_asc",
                                    "id_asc",
                                    "id_desc",
                                ],
                                "default": "market_cap_desc",
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "Number of results per page (1-250, default: 100)",
                                "default": 100,
                                "minimum": 1,
                                "maximum": 250,
                            },
                            "page": {
                                "type": "integer",
                                "description": "Page number (default: 1)",
                                "default": 1,
                                "minimum": 1,
                            },
                        },
                        "required": ["category_id"],
                    },
                },
            },
        ]

    async def select_best_token_match(self, search_results: Dict, query: str) -> str:
        """
        Select best matching token using the following criteria:
        1. Ignore tokens with None market_cap_rank
        2. Find closest name/symbol match
        3. Use market cap rank as tiebreaker
        """
        if not search_results.get("coins"):
            return None

        # Filter out tokens with None market_cap_rank
        valid_tokens = [token for token in search_results["coins"] if token.get("market_cap_rank") is not None]

        if not valid_tokens:
            return None

        logger.info(f"valid_tokens: {valid_tokens}")

        # Create prompt for token selection
        token_selection_prompt = f"""Given the search query "{query}" and these token results:
        {json.dumps(valid_tokens, indent=2)}

        Select the most appropriate token based on these criteria in order:
        1. Find the token where name or symbol most closely matches the query
        - Exact matches are preferred
        - For partial matches, consider string similarity and common variations
        2. If multiple tokens have similar name matches, select the one with the highest market cap rank (lower number = higher rank)

        Return only the CoinGecko ID of the selected token, nothing else."""

        selected_token = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["small_model_id"],
            messages=[
                {
                    "role": "system",
                    "content": "You are a token selection assistant. You only return the CoinGecko ID of the best matching token based on the given criteria.",
                },
                {"role": "user", "content": token_selection_prompt},
            ],
            temperature=0.1,
        )

        # Clean up response to get just the ID
        selected_token = selected_token.strip().strip('"').strip("'")

        # Verify the selected ID exists in filtered results
        if any(token["id"] == selected_token for token in valid_tokens):
            return selected_token
        return None

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

    # ------------------------------------------------------------------------
    #                      COINGECKO API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    async def get_trending_coins(self) -> dict:
        try:
            response = requests.get(f"{self.api_url}/search/trending", headers=self.headers)
            response.raise_for_status()
            trending_data = response.json()

            # Format the trending coins data
            formatted_trending = []
            for coin in trending_data.get("coins", [])[:10]:
                coin_info = coin["item"]
                formatted_trending.append(
                    {
                        "name": coin_info["name"],
                        "symbol": coin_info["symbol"],
                        "market_cap_rank": coin_info.get("market_cap_rank", "N/A"),
                        "price_usd": coin_info["data"].get("price", "N/A"),
                    }
                )
            return {"trending_coins": formatted_trending}

        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to fetch trending coins: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    async def get_coingecko_id(self, token_name: str) -> dict | str:
        try:
            response = requests.get(f"{self.api_url}/search?query={token_name}", headers=self.headers)
            response.raise_for_status()
            search_results = response.json()
            # Return the first coin id if found
            if search_results.get("coins") and len(search_results["coins"]) == 1:
                first_coin = search_results["coins"][0]
                return first_coin["id"]
            elif (search_results.get("coins") and len(search_results["coins"]) == 0) or (
                search_results.get("coins") is None
            ):
                return None
            else:
                selected_token_id = await self.select_best_token_match(search_results, token_name)
                return selected_token_id or None

        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to search for token: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    async def get_token_info(self, coingecko_id: str) -> dict:
        try:
            response = requests.get(f"{self.api_url}/coins/{coingecko_id}", headers=self.headers)

            # if response fails, try to search for the token and use first result
            if response.status_code != 200:
                fallback_id = await self.get_coingecko_id(coingecko_id)
                if isinstance(fallback_id, str):  # ensure we got a valid id back
                    response = requests.get(f"{self.api_url}/coins/{fallback_id}", headers=self.headers)
                    response.raise_for_status()
                    return response.json()
                return {"error": "Failed to fetch token info and fallback search failed"}

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to fetch token info: {str(e)}"}

    def format_token_info(self, data: Dict) -> Dict:
        """Format token information in a structured way"""
        market_data = data.get("market_data", {})
        return {
            "token_info": {
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A").upper(),
                "market_cap_rank": data.get("market_cap_rank", "N/A"),
                "current_price": market_data.get("current_price", {}).get("usd", "N/A"),
                "market_cap": market_data.get("market_cap", {}).get("usd", "N/A"),
                "total_volume": market_data.get("total_volume", {}).get("usd", "N/A"),
                "high_24h": market_data.get("high_24h", {}).get("usd", "N/A"),
                "low_24h": market_data.get("low_24h", {}).get("usd", "N/A"),
                "price_change_24h": market_data.get("price_change_24h", "N/A"),
                "price_change_percentage_24h": market_data.get("price_change_percentage_24h", "N/A"),
                "circulating_supply": market_data.get("circulating_supply", "N/A"),
                "total_supply": market_data.get("total_supply", "N/A"),
                "max_supply": market_data.get("max_supply", "N/A"),
            }
        }

    # ------------------------------------------------------------------------
    #                      NEW CATEGORY API METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    async def get_categories_list(self) -> dict:
        """Get a list of all CoinGecko categories"""
        try:
            response = requests.get(f"{self.api_url}/coins/categories/list", headers=self.headers)
            response.raise_for_status()
            return {"categories": response.json()}
        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to fetch categories list: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    async def get_category_data(self, order: Optional[str] = "market_cap_desc") -> dict:
        """Get market data for all cryptocurrency categories"""
        try:
            params = {}
            if order:
                params["order"] = order

            response = requests.get(f"{self.api_url}/coins/categories", headers=self.headers, params=params)
            response.raise_for_status()
            return {"category_data": response.json()}
        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to fetch category data: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    async def get_tokens_by_category(
        self,
        category_id: str,
        vs_currency: str = "usd",
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
    ) -> dict:
        """Get tokens within a specific category"""
        try:
            params = {
                "vs_currency": vs_currency,
                "category": category_id,
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
            }

            response = requests.get(f"{self.api_url}/coins/markets", headers=self.headers, params=params)
            response.raise_for_status()
            return {"category_tokens": {"category_id": category_id, "tokens": response.json()}}
        except requests.RequestException as e:
            print(f"error: {e}")
            return {"error": f"Failed to fetch tokens for category '{category_id}': {str(e)}"}

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
    ) -> Dict[str, Any]:
        """
        A single method that calls the appropriate function, handles
        errors/formatting, and optionally calls the LLM to explain the result.
        """
        result = {}

        # Token-related methods
        if tool_name == "get_trending_coins":
            result = await self.get_trending_coins()
        elif tool_name == "get_token_info":
            result = await self.get_token_info(function_args["coingecko_id"])
        elif tool_name == "get_coingecko_id":
            result = await self.get_coingecko_id(function_args["token_name"])
            if isinstance(result, str):
                result = {"coingecko_id": result}
            elif result is None:
                result = {"error": f"No token found for {function_args['token_name']}"}

        # Category-related methods
        elif tool_name == "get_categories_list":
            result = await self.get_categories_list()
        elif tool_name == "get_category_data":
            order = function_args.get("order", "market_cap_desc")
            result = await self.get_category_data(order)
        elif tool_name == "get_tokens_by_category":
            category_id = function_args["category_id"]
            vs_currency = function_args.get("vs_currency", "usd")
            order = function_args.get("order", "market_cap_desc")
            per_page = function_args.get("per_page", 100)
            page = function_args.get("page", 1)
            result = await self.get_tokens_by_category(category_id, vs_currency, order, per_page, page)
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        error = self._handle_error(result)
        if error:
            return error

        # Format the token information if we're returning token info
        if tool_name == "get_token_info":
            result = self.format_token_info(result)

        # If raw data only is requested, return just the data
        if raw_data_only:
            return {"response": "", "data": result}

        # Default temperature: higher for more creative responses
        temp = 0.7

        # Generate an explanation using the LLM
        explanation = await self._respond_with_llm(
            query=query, tool_call_id=tool_call_id, data=result, temperature=temp
        )

        return {"response": explanation, "data": result}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Either 'query' or 'tool' is required in params.
          - If 'tool' is provided, call that tool directly with 'tool_arguments' (bypassing the LLM).
          - If 'query' is provided, route via LLM for dynamic tool selection.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            return await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
                query=query or "Direct tool call without LLM",
                tool_call_id="direct_tool",
                raw_data_only=raw_data_only,
            )

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY (LLM decides the tool)
        # ---------------------
        if query:
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
                return {"error": "Failed to process query"}

            if not response.get("tool_calls"):
                # No tool calls => the LLM just answered
                return {"response": response["content"], "data": {}}

            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            return await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
                query=query,
                tool_call_id=tool_call.id,
                raw_data_only=raw_data_only,
            )

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------

        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
