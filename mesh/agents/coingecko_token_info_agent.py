import asyncio
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent
from mesh.utils.r2_image_uploader import R2ImageUploader

logger = logging.getLogger(__name__)


def load_coingecko_id_map() -> Dict[str, str]:
    """Load CoinGecko ID mapping from JSON file."""
    map_file = Path(__file__).parent.parent / "data" / "coingecko_id_map.json"

    if not map_file.exists():
        logger.warning(f"CoinGecko ID map not found at {map_file}, using empty map")
        return {}

    with open(map_file, "r") as f:
        return json.load(f)


COINGECKO_ID_MAP = load_coingecko_id_map()


class CoinGeckoTokenInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.pro_api_url = "https://pro-api.coingecko.com/api/v3"
        self.api_key = os.getenv("COINGECKO_API_KEY")
        if not self.api_key:
            raise ValueError("COINGECKO_API_KEY environment variable is required")

        self.pro_headers = {"x-cg-pro-api-key": self.api_key}

        self.r2_uploader = R2ImageUploader()

        self.metadata.update(
            {
                "name": "CoinGecko Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch token information, market data, trending coins, and category data from CoinGecko.",
                "external_apis": ["Coingecko"],
                "tags": ["Trading"],
                "verified": True,
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
                    "Get historical token holders chart",
                    "Get recent trades for a token",
                ],
            }
        )

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
                            "coingecko_id": {
                                "type": "string",
                                "description": "The CoinGecko ID of the token (preferred), or symbol/name as fallback",
                            }
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
                    "description": "Get top token holder addresses for a token on a specific network. Max 40 holders.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string", "description": "Network ID (e.g., base, bsc, solana, eth)"},
                            "address": {"type": "string", "description": "Token contract address"},
                            "holders": {
                                "type": "integer",
                                "description": "Number of top holders to return.",
                                "default": 10,
                                "minimum": 5,
                                "maximum": 40
                            },
                        },
                        "required": ["network", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_historical_holders",
                    "description": "Get historical token holders with daily aggregated data and trend analysis.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string", "description": "Network ID (e.g., eth, base, solana, polygon)"},
                            "address": {"type": "string", "description": "Token contract address"},
                            "days": {
                                "type": "string",
                                "description": "Time period: 7 days or 30 days.",
                                "enum": ["7", "30"],
                                "default": "7",
                            },
                        },
                        "required": ["network", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recent_large_trades",
                    "description": "Get recent large trades on DEX for a specific token. Filters by minimum USD volume.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string", "description": "Network ID (e.g., eth, base, solana, bsc)"},
                            "address": {"type": "string", "description": "Token contract address"},
                            "min_amount": {
                                "type": "number",
                                "description": "Minimum trade volume in USD to include",
                                "default": 3000,
                            },
                        },
                        "required": ["network", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_holders_traders",
                    "description": "Get token holder and trader data combining: 1) Top holders - ranked wallet addresses with ownership percentages 2) Daily holder trend 3) Large trades in past 24 hours showing buy/sell whale activity.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "network": {"type": "string", "description": "Network ID (e.g., eth, base, solana, bsc, polygon)"},
                            "address": {"type": "string", "description": "Token contract address"},
                            "days": {
                                "type": "string",
                                "description": "Historical holder data period: 7 or 30 days",
                                "enum": ["7", "30"],
                                "default": "7",
                            },
                            "min_trade_amount": {
                                "type": "number",
                                "description": "Minimum trade volume in USD for recent trades",
                                "default": 3000,
                            },
                        },
                        "required": ["network", "address"],
                    },
                },
            },
        ]

    def _normalize_address(self, address: str) -> str:
        if address.startswith("0x"):
            return address.lower()
        return address

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
            "platforms": {k: self._normalize_address(v) for k, v in data.get("platforms", {}).items()},
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

    @with_retry(max_retries=1)
    async def _search_token(self, query: str) -> str | None:
        """Internal helper to search for a token and return its id"""
        try:
            url = f"{self.pro_api_url}/search"
            params = {"query": query}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)

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
            url = f"{self.pro_api_url}/search/trending"
            response = await self._api_request(url=url, headers=self.pro_headers)

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
                        "price_change_percentage_24h": coin_info["data"]
                        .get("price_change_percentage_24h", {})
                        .get("usd", "N/A"),
                    }
                )
            return {"trending_coins": formatted_trending}

        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch trending coins: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=1)
    async def _get_token_info(self, coingecko_id_like: str) -> dict:
        try:
            if coingecko_id_like.islower():
                # All lowercase - treat as coingecko_id directly
                coingecko_id = coingecko_id_like
            else:
                # Has uppercase - check quick lookup map first
                # Try exact match (for names like "Ethereum"), then uppercase (for symbols like "ETH")
                coingecko_id = COINGECKO_ID_MAP.get(coingecko_id_like) or COINGECKO_ID_MAP.get(
                    coingecko_id_like.upper()
                )
                if not coingecko_id:
                    # Not in map - search for it
                    coingecko_id = await self._search_token(coingecko_id_like)
                    if not coingecko_id:
                        return {"error": "Failed to fetch token info"}

            # Try coins API with resolved coingecko_id
            url = f"{self.pro_api_url}/coins/{coingecko_id}"
            response = await super()._api_request(url=url, headers=self.pro_headers)

            if "error" not in response:
                image_urls = response.get("image", {})
                if image_urls:
                    await self.r2_uploader.upload_token_images(coingecko_id, image_urls)
                return self.preprocess_api_response(response)

            # Coins API failed for lowercase input - try search as last resort
            if coingecko_id_like.islower():
                searched_id = await self._search_token(coingecko_id_like)
                if searched_id:
                    url = f"{self.pro_api_url}/coins/{searched_id}"
                    response = await super()._api_request(url=url, headers=self.pro_headers)
                    if "error" not in response:
                        image_urls = response.get("image", {})
                        if image_urls:
                            await self.r2_uploader.upload_token_images(searched_id, image_urls)
                        return self.preprocess_api_response(response)

            return {"error": "Failed to fetch token info"}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch token info: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=1)
    async def _get_categories_list(self) -> dict:
        """Get a list of all CoinGecko categories"""
        try:
            url = f"{self.pro_api_url}/coins/categories/list"
            response = await self._api_request(url=url, headers=self.pro_headers)
            return {"categories": response} if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch categories list: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def _get_category_data(self, order: Optional[str] = "market_cap_change_24h_desc", limit: int = 5) -> dict:
        """Get market data for cryptocurrency categories with limit"""
        limit = max(3, min(limit, 20))

        try:
            url = f"{self.pro_api_url}/coins/categories"
            params = {"order": order} if order else {}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)

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
    @with_retry(max_retries=1)
    async def _get_token_price_multi(
        self,
        ids: str,
    ) -> dict:
        try:
            url = f"{self.pro_api_url}/simple/price"
            params = {
                "ids": ids,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            }

            response = await self._api_request(url=url, headers=self.pro_headers, params=params)
            return response if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch multi-token price data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
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
            url = f"{self.pro_api_url}/coins/markets"
            params = {
                "vs_currency": vs_currency,
                "category": category_id,
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
            }
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)
            return (
                {"category_tokens": {"category_id": category_id, "tokens": response}}
                if "error" not in response
                else {"error": response["error"]}
            )
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": f"Failed to fetch tokens for category '{category_id}': {str(e)}"}

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
                holders=function_args.get("holders", 10),
            ),
            "get_historical_holders": lambda: self._handle_historical_holders(
                network=function_args["network"],
                address=function_args["address"],
                days=function_args.get("days", "7"),
            ),
            "get_recent_large_trades": lambda: self._handle_recent_large_trades(
                network=function_args["network"],
                address=function_args["address"],
                min_amount=function_args.get("min_amount", 3000),
            ),
            "get_token_holders_traders": lambda: self._handle_token_holders_traders(
                network=function_args["network"],
                address=function_args["address"],
                days=function_args.get("days", "7"),
                min_trade_amount=function_args.get("min_trade_amount", 3000),
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
    @with_retry(max_retries=1)
    async def _handle_trending_pools(self, include: str, pools: int) -> Dict[str, Any]:
        valid_includes = ["base_token", "quote_token", "dex", "network"]
        if include not in valid_includes:
            return {"error": f"Invalid include parameter: {include}. Must be one of {valid_includes}"}

        try:
            url = f"{self.pro_api_url}/onchain/pools/trending_search"
            params = {"include": include, "pools": pools}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)
            return {"trending_pools": response} if "error" not in response else {"error": response["error"]}
        except Exception as e:
            logger.error(f"Error getting trending pools: {e}")
            return {"error": f"Failed to fetch trending pools: {str(e)}"}

    @with_cache(ttl_seconds=600)
    async def _handle_top_token_holders(self, network: str, address: str, holders: int = 10) -> Dict[str, Any]:
        try:
            url = f"{self.pro_api_url}/onchain/networks/{network}/tokens/{address}/top_holders"
            params = {"holders": holders}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            holders_list = []
            if "data" in response and "attributes" in response["data"]:
                for holder in response["data"]["attributes"].get("holders", []):
                    processed = {
                        "rank": holder.get("rank"),
                        "address": holder.get("address"),
                        "amount": int(float(holder.get("amount", 0))),
                        "percentage": holder.get("percentage"),
                        "value": holder.get("value"),
                    }
                    if holder.get("label"):
                        processed["label"] = holder["label"]
                    holders_list.append(processed)

            return {"top_holders": holders_list}
        except Exception as e:
            logger.error(f"Error getting top token holders: {e}")
            return {"error": f"Failed to fetch top token holders: {str(e)}"}

    @with_cache(ttl_seconds=3600)
    async def _handle_historical_holders(self, network: str, address: str, days: str = "7") -> Dict[str, Any]:
        try:
            url = f"{self.pro_api_url}/onchain/networks/{network}/tokens/{address}/holders_chart"
            params = {"days": days}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            holders_list = []
            if "data" in response and "attributes" in response["data"]:
                holders_list = response["data"]["attributes"].get("token_holders_list", [])

            daily_data = self._sample_daily_holders(holders_list, int(days))

            trend = self._calculate_trend(daily_data)

            flat_data = []
            for date_str, count in daily_data:
                flat_data.extend([date_str, str(count)])

            return {"historical_holders": {"trend": trend, "data": ",".join(flat_data)}}
        except Exception as e:
            logger.error(f"Error getting historical holders: {e}")
            return {"error": f"Failed to fetch historical holders: {str(e)}"}

    def _sample_daily_holders(self, holders_list: list, num_days: int) -> list:
        """Sample one data point per day from the holders list."""
        if not holders_list:
            return []

        sorted_data = sorted(holders_list, key=lambda x: x[0], reverse=True)

        daily_samples = []
        latest_ts = datetime.fromisoformat(sorted_data[0][0].replace("Z", "+00:00"))
        latest_date = latest_ts.date()
        daily_samples.append((str(latest_date), sorted_data[0][1]))

        current_boundary = datetime.combine(latest_date, datetime.min.time(), tzinfo=timezone.utc)

        for day_offset in range(1, num_days):
            target_boundary = current_boundary - timedelta(days=day_offset)

            best_point = None
            for ts_str, count in sorted_data:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts < target_boundary:
                    best_point = (str(ts.date()), count)
                    break

            if best_point:
                daily_samples.append(best_point)

        return daily_samples

    def _calculate_trend(self, daily_data: list) -> str:
        """Calculate trend based on oldest vs newest holder count."""
        if len(daily_data) < 2:
            return "new_token"

        newest_count = daily_data[0][1]
        oldest_count = daily_data[-1][1]

        if oldest_count == 0:
            return "strong_growth" if newest_count > 0 else "flat"

        pct_change = (newest_count - oldest_count) / oldest_count * 100

        if pct_change < -30:
            return "strong_decline"
        elif pct_change < -8:
            return "decline"
        elif pct_change <= 8:
            return "flat"
        elif pct_change <= 30:
            return "growth"
        else:
            return "strong_growth"

    @with_cache(ttl_seconds=600)
    async def _handle_recent_large_trades(self, network: str, address: str, min_amount: float = 3000) -> Dict[str, Any]:
        try:
            url = f"{self.pro_api_url}/onchain/networks/{network}/tokens/{address}/trades"
            params = {"trade_volume_in_usd_greater_than": min_amount}
            response = await self._api_request(url=url, headers=self.pro_headers, params=params)

            if "error" in response:
                return {"recent_large_trades": "not available"}

            trades = []
            if "data" in response:
                for trade in response["data"]:
                    attrs = trade.get("attributes", {})
                    volume_usd = attrs.get("volume_in_usd", "0")
                    trades.append({
                        "tx_from": attrs.get("tx_from_address", ""),
                        "kind": attrs.get("kind", ""),
                        "volume_usd": int(float(volume_usd)),
                        "timestamp": attrs.get("block_timestamp", ""),
                    })

            return {"recent_large_trades": trades}
        except Exception as e:
            logger.error(f"Error getting recent large trades: {e}")
            return {"recent_large_trades": "not available"}

    async def _handle_token_holders_traders(
        self, network: str, address: str, days: str = "7", min_trade_amount: float = 3000
    ) -> Dict[str, Any]:
        results = await asyncio.gather(
            self._handle_top_token_holders(network, address, 10),
            self._handle_historical_holders(network, address, days),
            self._handle_recent_large_trades(network, address, min_trade_amount),
        )

        return {
            "token_holders_traders": {
                "top_holders": results[0].get("top_holders", []),
                "historical_holders": results[1].get("historical_holders", {}),
                "recent_large_trades": results[2].get("recent_large_trades", []),
            }
        }
