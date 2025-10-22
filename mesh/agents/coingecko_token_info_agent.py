import logging
import os
from typing import Any, Dict, List, Optional

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

COINGECKO_ID_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "XRP": "ripple",
    "BNB": "binancecoin",
    "SOL": "solana",
    "USDC": "usd-coin",
    "DOGE": "dogecoin",
    "STETH": "staked-ether",  # Lido Staked Ether
    "TRX": "tron",
    "ADA": "cardano",
    "WSTETH": "wrapped-steth",
    "AVAX": "avalanche-2",
    "WBETH": "wrapped-beacon-eth",
    "LINK": "chainlink",
    "WBTC": "wrapped-bitcoin",
    "USDE": "usde",  # Ethena USDe
    "HYPE": "hyperliquid",
    "SUI": "sui",
    "XLM": "stellar",
    "BCH": "bitcoin-cash",
    "WEETH": "wrapped-eeth",
    "WETH": "weth",
    "HBAR": "hedera-hashgraph",
    "LEO": "leo-token",
    "USDS": "usds",
    "LTC": "litecoin",
    "CRO": "crypto-com-chain",  # Cronos
    "TON": "the-open-network",
}


class CoinGeckoTokenInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.public_api_url = "https://api.coingecko.com/api/v3"
        self.pro_api_url = "https://pro-api.coingecko.com/api/v3"
        self.api_key = os.getenv("COINGECKO_API_KEY")
        if not self.api_key:
            raise ValueError("COINGECKO_API_KEY environment variable is required")

        self.public_headers = {"Authorization": f"Bearer {self.api_key}"}
        self.pro_headers = {"x-cg-pro-api-key": self.api_key}

        self.metadata.update(
            {
                "name": "CoinGecko Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch token information, market data, trending coins, and category data from CoinGecko.",
                "external_apis": ["Coingecko"],
                "tags": ["Trading"],
                "recommended": True,
                "large_model_id": "google/gemini-2.0-flash-001",
                "small_model_id": "google/gemini-2.0-flash-001",
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Coingecko.png",
                "examples": [
                    "Top 5 crypto by market cap",
                    "24-hr price change of ETH",
                    "Get information about HEU",
                    "Analyze AI16Z token",
                    "List crypto categories",
                    "Compare DeFi tokens",
                    "Get trending on-chain pools",
                    "Get top token holders for a token",
                ],
            }
        )

    def _resolve_coingecko_id(self, coingecko_id: str) -> str:
        """Resolve a CoinGecko ID or symbol to the actual CoinGecko ID using the mapping."""
        actual_coingecko_id = COINGECKO_ID_MAP.get(coingecko_id.upper(), coingecko_id)
        if actual_coingecko_id != coingecko_id:
            logger.info(f"Mapped {coingecko_id} to {actual_coingecko_id} using COINGECKO_ID_MAP")
        return actual_coingecko_id

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that can access CoinGecko API to provide cryptocurrency token information, market data, trending coins, and category data.

Format your response in clean text. Be objective and informative."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_token_info",
                    "description": "Get detailed token information and market data using CoinGecko ID. This tool provides comprehensive cryptocurrency data including current price, market cap, trading volume, price changes, and more.",
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
                    "description": "Get today's trending cryptocurrencies based on trading activities. This tool retrieves a list of crypto assets including basic market data.",
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
                    "name": "get_token_price_multi",
                    "description": "Fetch price data for multiple tokens. Returns current price, market cap, 24hr volume, 24hr change %",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ids": {
                                "type": "string",
                                "description": "Comma-separated CoinGecko IDs of the tokens to query",
                            },
                        },
                        "required": ["ids"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_categories_list",
                    "description": "Get a list of all available cryptocurrency categories from CoinGecko, like layer-1, layer-2, defi, etc. This tool retrieves all the category IDs and names that can be used for further category-specific queries.",
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
                    "description": "Get market data for all cryptocurrency categories from CoinGecko. This tool retrieves comprehensive information about all categories including market cap, volume, market cap change, top coins in each category, and more.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order": {
                                "type": "string",
                                "description": "Sort order for categories",
                                "enum": [
                                    "market_cap_desc",
                                    "market_cap_change_24h_desc",
                                ],
                                "default": "market_cap_change_24h_desc",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of categories to return",
                                "default": 5,
                                "minimum": 3,
                                "maximum": 20,
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_tokens_by_category",
                    "description": "Get USD price data for tokens within a specific category. Returns price, market cap, volume, and price changes.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category_id": {
                                "type": "string",
                                "description": "The CoinGecko category ID (e.g., 'layer-1')",
                            },
                            "order": {
                                "type": "string",
                                "description": "Sort order for tokens",
                                "enum": [
                                    "market_cap_desc",
                                    "volume_desc",
                                ],
                                "default": "market_cap_desc",
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "Number of results per page",
                                "default": 100,
                                "minimum": 10,
                                "maximum": 250,
                            },
                            "page": {
                                "type": "integer",
                                "description": "Page number",
                                "default": 1,
                                "minimum": 1,
                            },
                        },
                        "required": ["category_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_trending_pools",
                    "description": "Get top 10 trending onchain pools with token data from CoinGecko.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "include": {
                                "type": "string",
                                "description": "Single attribute to include: base_token, quote_token, dex, or network",
                                "enum": ["base_token", "quote_token", "dex", "network"],
                                "default": "base_token",
                            },
                            "pools": {
                                "type": "integer",
                                "description": "Number of pools to return (1-10)",
                                "default": 4,
                                "minimum": 1,
                                "maximum": 10,
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_token_holders",
                    "description": "Get top 50 token holder addresses for a token on a specific network.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string", "description": "Network ID (e.g., base, bsc, solana, eth)"},
                            "address": {"type": "string", "description": "Token contract address"},
                        },
                        "required": ["network", "address"],
                    },
                },
            },
        ]

    def get_api_config(self, endpoint: str) -> tuple[str, Dict[str, str]]:
        """Determine the appropriate API URL and headers based on the endpoint."""
        if endpoint.startswith("/onchain"):
            return self.pro_api_url, self.pro_headers
        return self.public_api_url, self.public_headers

    async def _api_request(
        self, url: str, method: str = "GET", headers: Dict = None, params: Dict = None, json_data: Dict = None
    ) -> Dict:
        result = await super()._api_request(url, method, headers, params, json_data)
        if "error" not in result:
            return self.preprocess_api_response(result)
        return result

    @staticmethod
    def preprocess_api_response(data: Any) -> Any:
        """
        Preprocess API response to remove unnecessary data like images, URLs, and advertisements.
        Note: 'tickers' is intentionally preserved for CEX data extraction.
        """
        # fmt: off
        FIELDS_TO_REMOVE = {"image", "thumb", "small", "large", "icon", "logo", "img", "thumbnail", "image_url", "thumb_url", "small_image", "large_image", "icon_url", "logo_url", "img_url", "thumbnail_url", "images", "homepage", "official_forum_url", "chat_url", "announcement_url", "twitter_screen_name", "facebook_username", "bitcointalk_thread_identifier", "telegram_channel_identifier", "subreddit_url", "repos_url", "github", "bitbucket", "urls", "blockchain_site", "official_forum", "chat", "announcement", "twitter", "facebook", "reddit", "telegram", "discord", "website", "whitepaper", "explorer", "source_code", "technical_doc", "repos", "social_links", "community_data", "developer_data", "public_interest_stats", "coingecko_rank", "coingecko_score", "developer_score", "community_score", "liquidity_score", "public_interest_score", "status_updates", "sparkline_in_7d", "roi", "description", "genesis_date", "hashing_algorithm", "country_origin", "last_updated", "localization", "detail_platforms", "asset_platform_id", "block_time_in_minutes", "mining_stats", "additional_notices", "ico_data", "market_data.sparkline_7d", "top_3_coins", "top_3_coins_id"}
        # fmt: on

        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                if key.lower() in FIELDS_TO_REMOVE:
                    continue

                if any(
                    term in key.lower()
                    for term in [
                        "image",
                        "thumb",
                        "icon",
                        "logo",
                        "url",
                        "link",
                        "homepage",
                        "website",
                        "twitter",
                        "facebook",
                        "telegram",
                        "discord",
                        "reddit",
                        "github",
                        "repos",
                    ]
                ):
                    continue

                cleaned[key] = CoinGeckoTokenInfoAgent.preprocess_api_response(value)

            if "market_data" in cleaned and isinstance(cleaned["market_data"], dict):
                market_data = cleaned["market_data"]
                for key in list(market_data.keys()):
                    if "sparkline" in key.lower():
                        del market_data[key]

            return cleaned

        elif isinstance(data, list):
            return [CoinGeckoTokenInfoAgent.preprocess_api_response(item) for item in data]

        else:
            return data

    @staticmethod
    def extract_cex_data(tickers: List[Dict]) -> Optional[List[Dict]]:
        """
        Extract CEX data from tickers for specific exchanges.

        Filters for:
        - Binance (binance) with USDT target
        - Bybit Spot (bybit_spot) with USDT target
        - Upbit (upbit) - any target
        - Coinbase (coinbase) - any target

        Args:
            tickers: List of ticker data from CoinGecko API

        Returns:
            List of CEX data dictionaries or None if no relevant tickers found
        """
        if not tickers:
            return None

        # Define filter rules: (market_identifier, target_required)
        # None for target_required means accept any target
        # target means USDT, USD, KRW, etc.
        cex_filters = [
            ("binance", "USDT"),
            ("bybit_spot", "USDT"),
            ("gate", "USDT"),
            ("bitget", "USDT"),
            ("upbit", None),
            ("coinbase", None),
        ]

        cex_data = []
        seen_exchanges = set()  # Track unique exchange/target combinations

        for ticker in tickers:
            market = ticker.get("market", {})
            market_identifier = market.get("identifier")
            target = ticker.get("target", "")

            for exchange_id, required_target in cex_filters:
                if market_identifier != exchange_id:
                    continue

                if required_target and target != required_target:
                    continue

                exchange_key = f"{market_identifier}_{target}"
                if exchange_key in seen_exchanges:
                    continue

                seen_exchanges.add(exchange_key)

                cex_entry = {
                    "cex_name": market.get("name", market_identifier),
                    "base_token": target,
                    "volume_24h": ticker.get("volume"),
                }

                cex_data.append(cex_entry)
                break

        return cex_data if cex_data else None

    def format_token_info(self, data: Dict) -> Dict:
        market_data = data.get("market_data", {})
        links = data.get("links", {})
        tickers = data.get("tickers", [])

        result = {
            "token_info": {
                "id": data.get("id", "N/A"),
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A").upper(),
                "market_cap_rank": data.get("market_cap_rank", "N/A"),
                "categories": data.get("categories", []),
                "links": {
                    "website": next((u for u in (links.get("homepage") or []) if u), None),
                    "twitter": f"https://twitter.com/{links.get('twitter_screen_name')}"
                    if links.get("twitter_screen_name")
                    else None,
                    "telegram": f"https://t.me/{links.get('telegram_channel_identifier')}"
                    if links.get("telegram_channel_identifier")
                    else None,
                    "github": (links.get("repos_url") or {}).get("github", []),
                    "explorers": [u for u in (links.get("blockchain_site") or []) if u],
                },
            },
            "platforms": {k: v.lower() if v else v for k, v in data.get("platforms", {}).items()},
            "market_metrics": {
                "current_price_usd": market_data.get("current_price", {}).get("usd", "N/A"),
                "market_cap_usd": market_data.get("market_cap", {}).get("usd", "N/A"),
                "fully_diluted_valuation_usd": market_data.get("fully_diluted_valuation", {}).get("usd", "N/A"),
                "total_volume_usd": market_data.get("total_volume", {}).get("usd", "N/A"),
            },
            "price_metrics": {
                "ath_usd": market_data.get("ath", {}).get("usd", "N/A"),
                "ath_change_percentage": market_data.get("ath_change_percentage", {}).get("usd", "N/A"),
                "ath_date": market_data.get("ath_date", {}).get("usd", "N/A"),
                "high_24h_usd": market_data.get("high_24h", {}).get("usd", "N/A"),
                "low_24h_usd": market_data.get("low_24h", {}).get("usd", "N/A"),
                "price_change_24h": market_data.get("price_change_24h", "N/A"),
                "price_change_percentage_24h": market_data.get("price_change_percentage_24h", "N/A"),
            },
            "supply_info": {
                "total_supply": market_data.get("total_supply", "N/A"),
                "max_supply": market_data.get("max_supply", "N/A"),
                "circulating_supply": market_data.get("circulating_supply", "N/A"),
            },
        }

        cex_data = self.extract_cex_data(tickers)
        if cex_data:
            result["cex_data"] = cex_data

        return result

    @with_retry(max_retries=3)
    async def _search_token(self, query: str) -> str | None:
        """Internal helper to search for a token and return its id"""
        try:
            api_url, headers = self.get_api_config("/search")
            url = f"{api_url}/search"
            params = {"query": query}
            response = await self._api_request(url=url, headers=headers, params=params)

            if "error" in response or not response.get("coins"):
                return None

            if len(response["coins"]) == 1:
                return response["coins"][0]["id"]

            # try exact matches first
            for coin in response["coins"]:
                if coin["name"].lower() == query.lower() or coin["symbol"].lower() == query.lower():
                    return coin["id"]

            # if no exact match, return first result
            return response["coins"][0]["id"]
        except Exception as e:
            logger.error(f"Error searching for token: {e}")
            return None

    # ------------------------------------------------------------------------
    #                      COINGECKO API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    async def _get_trending_coins(self) -> dict:
        try:
            api_url, headers = self.get_api_config("/search/trending")
            url = f"{api_url}/search/trending"
            response = await self._api_request(url=url, headers=headers)

            if "error" in response:
                return {"error": response["error"]}

            formatted_trending = []
            for coin in response.get("coins", [])[:10]:
                coin_info = coin["item"]
                formatted_trending.append(
                    {
                        "coingecko_id": coin_info.get("id", "N/A"),
                        "name": coin_info["name"],
                        "symbol": coin_info["symbol"],
                        "market_cap_rank": coin_info.get("market_cap_rank", "N/A"),
                        "price_usd": coin_info["data"].get("price", "N/A"),
                        "market_cap": coin_info["data"].get("market_cap", "N/A"),
                        "total_volume_24h": coin_info["data"].get("total_volume", "N/A"),
                        "price_change_percentage_24h": coin_info["data"].get("price_change_percentage_24h", {}).get("usd", "N/A"),
                    }
                )
            return {"trending_coins": formatted_trending}

        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch trending coins: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def _get_token_info(self, coingecko_id: str) -> dict:
        try:
            actual_coingecko_id = self._resolve_coingecko_id(coingecko_id)
            api_url, headers = self.get_api_config(f"/coins/{actual_coingecko_id}")
            url = f"{api_url}/coins/{actual_coingecko_id}"
            response = await self._api_request(url=url, headers=headers)
            if "error" not in response:
                return response

            # if response contains error, try search fallback (only if we didn't already use the map)
            if actual_coingecko_id == coingecko_id:
                fallback_id = await self._search_token(coingecko_id)
                if fallback_id:
                    api_url, headers = self.get_api_config(f"/coins/{fallback_id}")
                    fallback_url = f"{api_url}/coins/{fallback_id}"
                    fallback_response = await self._api_request(url=fallback_url, headers=headers)
                    if "error" not in fallback_response:
                        return fallback_response
            return {"error": "Failed to fetch token info"}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch token info: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def _get_categories_list(self) -> dict:
        """Get a list of all CoinGecko categories"""
        try:
            api_url, headers = self.get_api_config("/coins/categories/list")
            url = f"{api_url}/coins/categories/list"
            response = await self._api_request(url=url, headers=headers)
            return {"categories": response} if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch categories list: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _get_category_data(self, order: Optional[str] = "market_cap_change_24h_desc", limit: int = 5) -> dict:
        """Get market data for cryptocurrency categories with limit"""
        limit = max(3, min(limit, 20))

        try:
            api_url, headers = self.get_api_config("/coins/categories")
            url = f"{api_url}/coins/categories"
            params = {"order": order} if order else {}
            response = await self._api_request(url=url, headers=headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            if isinstance(response, list):
                limited_data = response[:limit]
                return {
                    "category_data": limited_data,
                    "total_available": len(response),
                    "returned_count": len(limited_data),
                    "limit": limit,
                }
            else:
                return {"category_data": response}

        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch category data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _get_token_price_multi(
        self,
        ids: str,
    ) -> dict:
        try:
            api_url, headers = self.get_api_config("/simple/price")
            url = f"{api_url}/simple/price"
            params = {
                "ids": ids,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            }

            response = await self._api_request(url=url, headers=headers, params=params)
            return response if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch multi-token price data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _get_tokens_by_category(
        self,
        category_id: str,
        vs_currency: str = "usd",
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
    ) -> dict:
        """Get tokens within a specific category"""
        try:
            api_url, headers = self.get_api_config("/coins/markets")
            url = f"{api_url}/coins/markets"
            params = {
                "vs_currency": vs_currency,
                "category": category_id,
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
            }
            response = await self._api_request(url=url, headers=headers, params=params)
            return (
                {"category_tokens": {"category_id": category_id, "tokens": response}}
                if "error" not in response
                else {"error": response["error"]}
            )
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch tokens for category '{category_id}': {str(e)}"}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming messages with direct tool calls."""
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})

        try:
            if tool_name:
                logger.info(f"Direct tool call: {tool_name} with args {tool_args}")
                result = await self._handle_tool_logic(tool_name, tool_args)
                return {"data": result}

            return {"error": "Tool name must be provided in the parameters."}

        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            return {"error": str(e)}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        tool_map = {
            "get_token_info": lambda: self._get_token_info(function_args["coingecko_id"]),
            "get_trending_coins": lambda: self._get_trending_coins(),
            "get_token_price_multi": lambda: self._get_token_price_multi(
                ids=function_args["ids"],
            ),
            "get_categories_list": lambda: self._get_categories_list(),
            "get_category_data": lambda: self._get_category_data(
                function_args.get("order", "market_cap_change_24h_desc"), function_args.get("limit", 5)
            ),
            "get_tokens_by_category": lambda: self._get_tokens_by_category(
                category_id=function_args["category_id"],
                vs_currency="usd",
                order=function_args.get("order", "market_cap_desc"),
                per_page=function_args.get("per_page", 100),
                page=function_args.get("page", 1),
            ),
            "get_trending_pools": lambda: self._handle_trending_pools(
                include=function_args.get("include", "base_token"),
                pools=function_args.get("pools", 4),
            ),
            "get_top_token_holders": lambda: self._handle_top_token_holders(
                network=function_args["network"],
                address=function_args["address"],
            ),
        }

        if tool_name not in tool_map:
            return {"error": f"Unsupported tool: {tool_name}"}

        result = await tool_map[tool_name]()
        if tool_name == "get_token_info" and "error" not in result:
            return self.format_token_info(result)
        if tool_name == "get_token_price_multi" and "error" not in result:
            return {"price_data": result}

        return result

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _handle_trending_pools(self, include: str, pools: int) -> Dict[str, Any]:
        valid_includes = ["base_token", "quote_token", "dex", "network"]
        if include not in valid_includes:
            return {"error": f"Invalid include parameter: {include}. Must be one of {valid_includes}"}

        try:
            api_url, headers = self.get_api_config("/onchain/pools/trending_search")
            url = f"{api_url}/onchain/pools/trending_search"
            params = {"include": include, "pools": pools}
            response = await self._api_request(url=url, headers=headers, params=params)
            return {"trending_pools": response} if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error getting trending pools: {e}")
            return {"error": f"Failed to fetch trending pools: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _handle_top_token_holders(self, network: str, address: str) -> Dict[str, Any]:
        try:
            api_url, headers = self.get_api_config(f"/onchain/networks/{network}/tokens/{address}/top_holders")
            url = f"{api_url}/onchain/networks/{network}/tokens/{address}/top_holders"
            response = await self._api_request(url=url, headers=headers)
            return {"top_holders": response} if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error getting top token holders: {e}")
            return {"error": f"Failed to fetch top token holders: {str(e)}"}
