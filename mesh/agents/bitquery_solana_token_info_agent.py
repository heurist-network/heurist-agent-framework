import datetime
import logging
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class BitquerySolanaTokenInfoAgent(MeshAgent):
    # Token address constants
    USDC_ADDRESS = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    SOL_ADDRESS = "So11111111111111111111111111111111111111112"
    VIRTUAL_ADDRESS = "3iQL8BFS2vE7mww4ehAqQHAsbmRNCrPxizWAT2Zfyr9y"
    NATIVE_SOL_ADDRESS = "11111111111111111111111111111111"

    # Supported quote tokens
    SUPPORTED_QUOTE_TOKENS = {
        "usdc": USDC_ADDRESS,
        "sol": SOL_ADDRESS,
        "virtual": VIRTUAL_ADDRESS,
        "native_sol": NATIVE_SOL_ADDRESS,
    }

    # Default settings
    DEFAULT_LIMIT = 10

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("BITQUERY_API_KEY")
        if not self.api_key:
            raise ValueError("BITQUERY_API_KEY environment variable is required")

        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        self.bitquery_url = "https://streaming.bitquery.io/eap"

        self.metadata.update(
            {
                "name": "Solana Token Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides comprehensive analysis of Solana tokens using Bitquery API. It can analyze token metrics (volume, price, liquidity), track holders and buyers, monitor trading activity, and identify trending tokens. The agent supports both specific token analysis and market-wide trend discovery.",
                "external_apis": ["Bitquery"],
                "tags": ["Solana"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Solana.png",
                "examples": [
                    "Analyze trending tokens on Solana",
                    "Get token info for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
                    "Show top 10 most active tokens on Solana network",
                    "Get top buyers for token EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    "Show token holders for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You are a specialized assistant that analyzes Solana token data using the Bitquery API. "
            "Your capabilities include:\n\n"
            "1. Token Metrics Analysis: Get detailed trading metrics including volume, price movements, and liquidity\n"
            "2. Holder Analysis: Track token holders and their distribution patterns\n"
            "3. Buyer Tracking: Identify first buyers and early investors (potential insiders/smart money)\n"
            "4. Top Traders: Find the most active traders by volume for any token\n"
            "5. Holder Status: Check if specific addresses are still holding, sold, or bought more\n"
            "6. Trending Discovery: Identify the most popular and actively traded tokens\n\n"
            "Guidelines:\n"
            "- Present data in a clear, concise, and data-driven manner\n"
            "- Focus on actionable insights for traders and investors\n"
            "- For token addresses, use this format: [Mint Address](https://solscan.io/token/Mint_Address)\n"
            "- Use natural language in responses\n"
            "- Highlight key metrics that indicate trading activity and market interest\n"
            "- Only mention missing data if it's critical to answer the user's question\n"
            "- All data is sourced from Bitquery API with real-time updates\n"
            "- If information is insufficient to answer a question, acknowledge the limitation"
        )

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_token_metrics",
                    "description": "Get detailed token trading metrics using Solana mint address. This tool fetches trading data including volume, price movements, and liquidity for any Solana token. Use this when you need to analyze a specific Solana token's performance.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {"type": "string", "description": "The Solana token mint address"},
                            "quote_token": {
                                "type": "string",
                                "description": "Quote token to use ('usdc', 'sol', 'virtual', 'native_sol', or the token address)",
                                "default": "sol",
                            },
                        },
                        "required": ["token_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_token_holders",
                    "description": "Fetch top token holders data and distribution for any Solana token. This tool provides detailed information about token holders including their balances and percentage of total supply. Use this when you need to analyze the distribution of token ownership.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {"type": "string", "description": "Token mint address on Solana"}
                        },
                        "required": ["token_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_token_buyers",
                    "description": "Fetch first buyers of a Solana token since its launch. This tool is useful to identify the early buyers who are likely insiders or smart money.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {"type": "string", "description": "Token mint address on Solana"},
                            "limit": {"type": "number", "description": "Number of buyers to fetch", "default": 10},
                        },
                        "required": ["token_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_top_traders",
                    "description": "Fetch top traders (based on volume) for a Solana token. The top traders might include the whales actively trading the token, and arbitrage bots.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {"type": "string", "description": "Token mint address on Solana"},
                            "limit": {"type": "number", "description": "Number of traders to fetch", "default": 10},
                        },
                        "required": ["token_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_holder_status",
                    "description": "Check if a list of token buyers are still holding, sold, or bought more for a specific Solana token. Use this tool to analyze the behavior of token buyers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {"type": "string", "description": "Token mint address on Solana"},
                            "buyer_addresses": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of buyer wallet addresses to check",
                            },
                        },
                        "required": ["token_address", "buyer_addresses"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_trending_tokens",
                    "description": "Get the current top trending tokens on Solana. This tool retrieves a list of the most popular and actively traded tokens on Solana. It provides key metrics for each trending token including price, volume, and recent price changes. Use this when you want to discover which tokens are currently gaining attention in the Solana ecosystem.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "minimum": 1,
                                "default": 10,
                                "description": "Number of trending tokens to return (default 10)",
                            },
                        },
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    async def _execute_query(self, query: str, variables: Dict = None) -> Dict:
        """
        Execute a GraphQL query against the Bitquery API with improved error handling.

        Args:
            query (str): GraphQL query to execute
            variables (Dict, optional): Variables for the query

        Returns:
            Dict: Query results
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            result = await self._api_request(
                url=self.bitquery_url, method="POST", headers=self.headers, json_data=payload
            )

            if "error" in result:
                logger.error(f"API request error: {result['error']}")
                return result

            if "errors" in result:
                error_messages = [error.get("message", "Unknown error") for error in result["errors"]]
                logger.error(f"GraphQL errors: {error_messages}")
                return {"error": f"GraphQL errors: {', '.join(error_messages)}"}

            return result

        except Exception as e:
            logger.error(f"Error in _execute_query: {str(e)}")
            return {"error": f"Query execution failed: {str(e)}"}

    def _safe_float_conversion(self, value, default=0.0) -> float:
        """Safely convert a value to float with proper error handling."""
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def _safe_int_conversion(self, value, default=0) -> int:
        """Safely convert a value to int with proper error handling."""
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def _validate_limit(self, limit: Optional[int], default: int = None) -> int:
        """Validate and normalize limit parameter."""
        if default is None:
            default = self.DEFAULT_LIMIT

        if limit is None:
            return default
        elif limit < 1:
            return 1
        return limit

    @monitor_execution()
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def query_token_metrics(self, token_address: str, quote_token: str = "sol") -> Dict:
        """
        Get detailed token trading information including metrics like volume and market cap.

        Args:
            token_address (str): The mint address of the token
            quote_token (str): The quote token to use (usdc, sol, virtual, native_sol, or token address)

        Returns:
            Dict: Dictionary containing token trading info and metrics
        """
        try:
            # Get the quote token address
            if quote_token.lower() in self.SUPPORTED_QUOTE_TOKENS:
                quote_token_address = self.SUPPORTED_QUOTE_TOKENS[quote_token.lower()]
            else:
                quote_token_address = quote_token  # Assume it's a direct address if not a key

            time_1h_ago = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            query = "query ($time_1h_ago: DateTime!, $token: String!, $quote_token: String!) { Solana { volume: DEXTradeByTokens( where: { Trade: { Currency: { MintAddress: { is: $token } } Side: { Currency: { MintAddress: { is: $quote_token } } } } Block: { Time: { since: $time_1h_ago } } Transaction: { Result: { Success: true } } } limit: {count: 10} ) { sum(of: Trade_Side_AmountInUSD) } buyVolume: DEXTradeByTokens( where: { Trade: { Currency: { MintAddress: { is: $token } } Side: { Currency: { MintAddress: { is: $quote_token } } } } Block: { Time: { since: $time_1h_ago } } Transaction: { Result: { Success: true } } } limit: {count: 10} ) { sum(of: Trade_Side_AmountInUSD, if: {Trade: {Side: {Type: {is: buy}}}}) } sellVolume: DEXTradeByTokens( where: { Trade: { Currency: { MintAddress: { is: $token } } Side: { Currency: { MintAddress: { is: $quote_token } } } } Block: { Time: { since: $time_1h_ago } } Transaction: { Result: { Success: true } } } limit: {count: 10} ) { sum(of: Trade_Side_AmountInUSD, if: {Trade: {Side: {Type: {is: sell}}}}) } marketcap: TokenSupplyUpdates( where: { TokenSupplyUpdate: { Currency: { MintAddress: { is: $token } } } Block: { Time: { till: $time_1h_ago } } Transaction: { Result: { Success: true } } } limitBy: { by: TokenSupplyUpdate_Currency_MintAddress, count: 10 } orderBy: { descending: Block_Time } ) { TokenSupplyUpdate { PostBalanceInUSD Currency { Name MintAddress Symbol } } } tokenInfo: DEXTradeByTokens( where: { Trade: { Currency: { MintAddress: { is: $token } } } Transaction: { Result: { Success: true } } } limit: {count: 1} orderBy: {descending: Block_Time} ) { Trade { Currency { Name Symbol MintAddress } PriceInUSD } Block { Time } } } }"

            variables = {"time_1h_ago": time_1h_ago, "token": token_address, "quote_token": quote_token_address}

            result = await self._execute_query(query, variables)

            if "error" in result:
                return result

            # If no data found with primary quote token, try alternatives
            if (
                "data" not in result
                or not result["data"]["Solana"]["volume"]
                or self._safe_float_conversion(
                    result["data"]["Solana"]["volume"][0] if result["data"]["Solana"]["volume"] else None
                )
                == 0
            ):
                if quote_token.lower() != "sol" and quote_token != self.SOL_ADDRESS:
                    logger.info(f"No data found with {quote_token}, trying SOL as fallback")
                    sol_variables = {
                        "time_1h_ago": time_1h_ago,
                        "token": token_address,
                        "quote_token": self.SOL_ADDRESS,
                    }
                    result = await self._execute_query(query, sol_variables)

                    if "data" in result:
                        result["data"]["fallback_used"] = "Used SOL as fallback quote token"

            # Get trading data for price movements
            if "data" in result and "Solana" in result["data"]:
                try:
                    trading_data = self.fetch_and_organize_dex_trade_data(token_address)
                    if trading_data:
                        latest_data = trading_data[-1]
                        first_data = trading_data[0]

                        price_change = self._safe_float_conversion(
                            latest_data.get("close", 0)
                        ) - self._safe_float_conversion(first_data.get("open", 0))
                        first_open = self._safe_float_conversion(first_data.get("open", 0))
                        price_change_percent = (price_change / first_open) * 100 if first_open != 0 else 0
                        total_volume = sum(
                            self._safe_float_conversion(bucket.get("volume", 0)) for bucket in trading_data
                        )

                        result["data"]["price_movements"] = {
                            "current_price": self._safe_float_conversion(latest_data.get("close", 0)),
                            "price_change_1h": price_change,
                            "price_change_percentage_1h": price_change_percent,
                            "highest_price_1h": max(
                                self._safe_float_conversion(bucket.get("high", 0)) for bucket in trading_data
                            ),
                            "lowest_price_1h": min(
                                self._safe_float_conversion(bucket.get("low", 0))
                                for bucket in trading_data
                                if self._safe_float_conversion(bucket.get("low", 0)) > 0
                            ),
                            "total_volume_1h": total_volume,
                            "last_updated": datetime.datetime.utcnow().isoformat(),
                        }
                except Exception as e:
                    logger.warning(f"Could not fetch price movement data: {str(e)}")

            return result

        except Exception as e:
            logger.error(f"Error in query_token_metrics: {str(e)}")
            return {"error": f"Failed to fetch token trading info: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=180)
    @with_retry(max_retries=3)
    async def get_top_trending_tokens(self, limit: int = None) -> Dict:
        """
        Get the current top trending tokens on Solana.

        Args:
            limit (int): Number of trending tokens to return (defaults to 10)

        Returns:
            Dict: Dictionary containing trending tokens
        """
        limit = self._validate_limit(limit, default=self.DEFAULT_LIMIT)

        try:
            trending_tokens = self.get_trending_tokens(limit)
            return {"trending_tokens": trending_tokens, "total_count": len(trending_tokens), "query_limit": limit}
        except Exception as e:
            logger.error(f"Error in get_top_trending_tokens: {str(e)}")
            return {"error": f"Failed to fetch top trending tokens: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_token_holders(self, token_address: str, limit: int = None) -> Dict:
        """
        Query top token holders for a specific token.

        Args:
            token_address (str): The mint address of the token
            limit (int): Number of top holders to return (defaults to 10)

        Returns:
            Dict: Dictionary containing holder information
        """
        limit = self._validate_limit(limit)

        query = 'query ($token: String!, $limit: Int!) { Solana(dataset: realtime) { BalanceUpdates( limit: { count: $limit } orderBy: { descendingByField: "BalanceUpdate_Holding_maximum" } where: { BalanceUpdate: { Currency: { MintAddress: { is: $token } } } Transaction: { Result: { Success: true } } } ) { BalanceUpdate { Currency { Name MintAddress Symbol Decimals } Account { Owner } Holding: PostBalance(maximum: Block_Slot) } } TotalSupply: TokenSupplyUpdates( limit: {count: 10} orderBy: {descending: Block_Time} where: { TokenSupplyUpdate: { Currency: { MintAddress: {is: $token} } } Transaction: { Result: { Success: true } } } ) { TokenSupplyUpdate { PostBalance Currency { Decimals } } } } }'

        variables = {"token": token_address, "limit": limit}

        result = await self._execute_query(query, variables)

        if "error" in result:
            return result

        if "data" in result and "Solana" in result["data"]:
            holders = result["data"]["Solana"]["BalanceUpdates"]
            formatted_holders = []

            # Get total supply if available
            total_supply = 0
            total_supply_data = result["data"]["Solana"].get("TotalSupply", [])
            if total_supply_data and len(total_supply_data) > 0:
                total_supply_update = total_supply_data[0].get("TokenSupplyUpdate", {})
                if "PostBalance" in total_supply_update:
                    total_supply = self._safe_float_conversion(total_supply_update["PostBalance"])

            for holder in holders:
                if "BalanceUpdate" not in holder:
                    continue

                balance_update = holder["BalanceUpdate"]
                currency = balance_update.get("Currency", {})
                account = balance_update.get("Account", {})

                holding = self._safe_float_conversion(balance_update.get("Holding", 0))

                percentage = 0
                if total_supply > 0 and holding > 0:
                    percentage = (holding / total_supply) * 100

                formatted_holder = {
                    "address": account.get("Owner", ""),
                    "holding": holding,
                    "percentage_of_supply": round(percentage, 6),
                    "token_info": {
                        "name": currency.get("Name", "Unknown"),
                        "symbol": currency.get("Symbol", "Unknown"),
                        "mint_address": currency.get("MintAddress", ""),
                        "decimals": self._safe_int_conversion(currency.get("Decimals", 0)),
                    },
                }
                formatted_holders.append(formatted_holder)

            return {
                "holders": formatted_holders,
                "total_supply": total_supply,
                "total_count": len(formatted_holders),
                "token_address": token_address,
            }

        return {"holders": [], "total_supply": 0, "total_count": 0}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_token_buyers(self, token_address: str, limit: int = None) -> Dict:
        """
        Query first buyers of a specific token.

        Args:
            token_address (str): The mint address of the token
            limit (int): Number of buyers to return (defaults to 30)

        Returns:
            Dict: Dictionary containing buyer information
        """
        limit = self._validate_limit(limit, default=30)

        query = "query ($token: String!, $limit: Int!) { Solana { DEXTrades( where: { Trade: { Buy: { Currency: { MintAddress: { is: $token } } } } Transaction: { Result: { Success: true } } } limit: { count: $limit } orderBy: { ascending: Block_Time } ) { Trade { Buy { Amount AmountInUSD Account { Token { Owner } } Currency { Symbol Name Decimals } } Sell { Currency { Symbol Name MintAddress } } } Block { Time } Transaction { Index Signature } } } }"

        variables = {"token": token_address, "limit": limit}

        result = await self._execute_query(query, variables)

        if "error" in result:
            return result

        if "data" in result and "Solana" in result["data"]:
            trades = result["data"]["Solana"]["DEXTrades"]
            formatted_buyers = []
            unique_buyers = set()  # Track unique buyers

            for trade in trades:
                if "Trade" not in trade or "Buy" not in trade["Trade"]:
                    continue

                buy = trade["Trade"]["Buy"]
                sell_currency = trade["Trade"]["Sell"]["Currency"]
                owner = buy["Account"]["Token"]["Owner"]

                # Only add unique buyers
                if owner not in unique_buyers:
                    unique_buyers.add(owner)

                    formatted_buyer = {
                        "owner": owner,
                        "amount": self._safe_float_conversion(buy.get("Amount", 0)),
                        "amount_usd": self._safe_float_conversion(buy.get("AmountInUSD", 0)),
                        "buy_currency": {
                            "name": buy["Currency"].get("Name", "Unknown"),
                            "symbol": buy["Currency"].get("Symbol", "Unknown"),
                            "decimals": self._safe_int_conversion(buy["Currency"].get("Decimals", 0)),
                        },
                        "sell_currency": {
                            "name": sell_currency.get("Name", "Unknown"),
                            "symbol": sell_currency.get("Symbol", "Unknown"),
                            "mint_address": sell_currency.get("MintAddress", ""),
                        },
                        "currency_pair": f"{buy['Currency'].get('Symbol', 'Unknown')}/{sell_currency.get('Symbol', 'Unknown')}",
                        "time": trade["Block"]["Time"],
                        "transaction_index": self._safe_int_conversion(trade["Transaction"].get("Index", 0)),
                        "transaction_signature": trade["Transaction"].get("Signature", ""),
                    }
                    formatted_buyers.append(formatted_buyer)

            return {
                "buyers": formatted_buyers,
                "unique_buyer_count": len(unique_buyers),
                "total_count": len(formatted_buyers),
                "token_address": token_address,
            }

        return {"buyers": [], "unique_buyer_count": 0, "total_count": 0}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_top_traders(self, token_address: str, limit: int = None) -> Dict:
        """
        Query top traders for a specific token on Solana DEXs.

        Args:
            token_address (str): The mint address of the token
            limit (int): Number of traders to return (defaults to 30)

        Returns:
            Dict: Dictionary containing top trader information
        """
        limit = self._validate_limit(limit, default=30)

        query = 'query ($token: String!, $limit: Int!) { Solana { DEXTradeByTokens( orderBy: {descendingByField: "volumeUsd"} limit: {count: $limit} where: { Trade: { Currency: { MintAddress: {is: $token} } }, Transaction: { Result: {Success: true} } } ) { Trade { Account { Owner } Currency { Name Symbol MintAddress } Side { Account { Address } Currency { Symbol Name } } } bought: sum(of: Trade_Amount, if: {Trade: {Side: {Type: {is: buy}}}}) sold: sum(of: Trade_Amount, if: {Trade: {Side: {Type: {is: sell}}}}) volume: sum(of: Trade_Amount) volumeUsd: sum(of: Trade_Side_AmountInUSD) count: count } } }'

        variables = {"token": token_address, "limit": limit}

        result = await self._execute_query(query, variables)

        if "error" in result:
            return result

        if "data" in result and "Solana" in result["data"]:
            trades = result["data"]["Solana"]["DEXTradeByTokens"]
            formatted_traders = []

            for trade in trades:
                bought = self._safe_float_conversion(trade.get("bought", 0))
                sold = self._safe_float_conversion(trade.get("sold", 0))

                buy_sell_ratio = 0
                if sold > 0:
                    buy_sell_ratio = bought / sold

                trade_info = trade.get("Trade", {})
                currency = trade_info.get("Currency", {})
                side_currency = trade_info.get("Side", {}).get("Currency", {})

                formatted_trader = {
                    "owner": trade_info.get("Account", {}).get("Owner", ""),
                    "bought": bought,
                    "sold": sold,
                    "buy_sell_ratio": round(buy_sell_ratio, 4),
                    "total_volume": self._safe_float_conversion(trade.get("volume", 0)),
                    "volume_usd": self._safe_float_conversion(trade.get("volumeUsd", 0)),
                    "transaction_count": self._safe_int_conversion(trade.get("count", 0)),
                    "token_info": {
                        "name": currency.get("Name", "Unknown"),
                        "symbol": currency.get("Symbol", "Unknown"),
                        "mint_address": currency.get("MintAddress", ""),
                    },
                    "side_currency_info": {
                        "name": side_currency.get("Name", "Unknown"),
                        "symbol": side_currency.get("Symbol", "Unknown"),
                    },
                }
                formatted_traders.append(formatted_trader)

            total_volume_usd = sum(trader["volume_usd"] for trader in formatted_traders)

            return {
                "traders": formatted_traders,
                "total_count": len(formatted_traders),
                "total_volume_usd": total_volume_usd,
                "token_address": token_address,
                "stats": {
                    "largest_trader_volume": formatted_traders[0]["volume_usd"] if formatted_traders else 0,
                    "average_volume_per_trader": total_volume_usd / len(formatted_traders) if formatted_traders else 0,
                },
            }

        return {"traders": [], "total_count": 0, "total_volume_usd": 0}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_holder_status(self, token_address: str, buyer_addresses: List[str]) -> Dict:
        """
        Query holder status for specific addresses for a token.

        Args:
            token_address (str): The mint address of the token
            buyer_addresses (list[str]): List of buyer addresses to check

        Returns:
            Dict: Dictionary containing holder status information
        """
        if not buyer_addresses:
            return {"error": "No buyer addresses provided"}

        # Split addresses into chunks of 50 to avoid query limitations
        max_addresses_per_query = 50
        address_chunks = [
            buyer_addresses[i : i + max_addresses_per_query]
            for i in range(0, len(buyer_addresses), max_addresses_per_query)
        ]

        all_holder_statuses = []
        status_counts = {"holding": 0, "sold": 0, "not_found": 0}

        for address_chunk in address_chunks:
            query = "query ($token: String!, $addresses: [String!]!) { Solana { BalanceUpdates( where: { BalanceUpdate: { Account: { Token: { Owner: { in: $addresses } } } Currency: { MintAddress: { is: $token } } } Transaction: { Result: { Success: true } } } limit: {count: 100} orderBy: {descending: Block_Time} ) { BalanceUpdate { Account { Token { Owner } } balance: PostBalance(maximum: Block_Slot) Currency { Decimals Name Symbol } } Transaction { Index } Block { Time } } } }"

            variables = {"token": token_address, "addresses": address_chunk}

            result = await self._execute_query(query, variables)

            if "error" in result:
                # Continue with other chunks even if one fails
                logger.warning(f"Error querying address chunk: {result['error']}")
                continue

            if "data" in result and "Solana" in result["data"]:
                balance_updates = result["data"]["Solana"]["BalanceUpdates"]

                # Track found addresses
                found_addresses = set()
                for update in balance_updates:
                    if "BalanceUpdate" not in update:
                        continue

                    balance_update = update["BalanceUpdate"]
                    owner = balance_update["Account"]["Token"]["Owner"]
                    found_addresses.add(owner)

                    balance = self._safe_float_conversion(balance_update.get("balance", 0))
                    currency = balance_update.get("Currency", {})

                    status = "holding" if balance > 0 else "sold"
                    status_counts[status] += 1

                    holder_status = {
                        "address": owner,
                        "current_balance": balance,
                        "status": status,
                        "token_info": {
                            "name": currency.get("Name", "Unknown"),
                            "symbol": currency.get("Symbol", "Unknown"),
                            "decimals": self._safe_int_conversion(currency.get("Decimals", 0)),
                        },
                        "last_update": {
                            "time": update["Block"]["Time"],
                            "transaction_index": self._safe_int_conversion(update["Transaction"].get("Index", 0)),
                        },
                    }
                    all_holder_statuses.append(holder_status)

                # Add not found addresses
                for address in address_chunk:
                    if address not in found_addresses:
                        status_counts["not_found"] += 1
                        all_holder_statuses.append(
                            {
                                "address": address,
                                "current_balance": 0,
                                "status": "not_found",
                                "token_info": None,
                                "last_update": None,
                            }
                        )

        return {
            "holder_statuses": all_holder_statuses,
            "summary": status_counts,
            "total_addresses_checked": len(buyer_addresses),
            "total_found": len(all_holder_statuses),
            "token_address": token_address,
        }

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        """
        try:
            if tool_name == "query_token_metrics":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "Missing 'token_address' parameter"}
                quote_token = function_args.get("quote_token", "sol")
                result = await self.query_token_metrics(token_address=token_address, quote_token=quote_token)

            elif tool_name == "query_token_holders":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "Missing 'token_address' parameter"}
                limit = function_args.get("limit")
                result = await self.query_token_holders(token_address=token_address, limit=limit)

            elif tool_name == "query_token_buyers":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "Missing 'token_address' parameter"}
                limit = function_args.get("limit")
                result = await self.query_token_buyers(token_address=token_address, limit=limit)

            elif tool_name == "query_top_traders":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "Missing 'token_address' parameter"}
                limit = function_args.get("limit")
                result = await self.query_top_traders(token_address=token_address, limit=limit)

            elif tool_name == "get_top_trending_tokens":
                limit = function_args.get("limit")
                result = await self.get_top_trending_tokens(limit=limit)

            elif tool_name == "query_holder_status":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "Missing 'token_address' parameter"}
                buyer_addresses = function_args.get("buyer_addresses", [])
                if not buyer_addresses:
                    return {"error": "Missing 'buyer_addresses' parameter"}
                result = await self.query_holder_status(token_address=token_address, buyer_addresses=buyer_addresses)

            else:
                return {"error": f"Unsupported tool: {tool_name}"}

            # Handle errors using the parent class method
            if errors := self._handle_error(result):
                return errors

            return result

        except Exception as e:
            logger.error(f"Error in _handle_tool_logic for {tool_name}: {str(e)}")
            return {"error": f"Tool execution failed: {str(e)}"}

    def fetch_and_organize_dex_trade_data(self, base_address: str) -> List[Dict]:
        """
        Fetches DEX trade data from Bitquery for the given base token address,
        setting the time_ago parameter to one hour before the current UTC time,
        and returns a list of dictionaries representing time buckets.

        Args:
            base_address (str): The token address for the base token.

        Returns:
            list of dict: Each dictionary contains keys: 'time', 'open', 'high',
                        'low', 'close', 'volume'.
        """
        try:
            # Calculate time_ago as one hour before the current UTC time.
            time_ago = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

            # GraphQL query using list filtering for tokens.
            query = 'query ( $tokens: [String!], $base: String, $dataset: dataset_arg_enum, $time_ago: DateTime, $interval: Int ) { Solana(dataset: $dataset) { DEXTradeByTokens( orderBy: { ascendingByField: "Block_Time" } where: { Transaction: { Result: { Success: true } }, Trade: { Side: { Amount: { gt: "0" }, Currency: { MintAddress: { in: $tokens } } }, Currency: { MintAddress: { is: $base } } }, Block: { Time: { after: $time_ago } } } ) { Block { Time(interval: { count: $interval, in: minutes }) } min: quantile(of: Trade_PriceInUSD, level: 0.05) max: quantile(of: Trade_PriceInUSD, level: 0.95) close: median(of: Trade_PriceInUSD) open: median(of: Trade_PriceInUSD) volume: sum(of: Trade_Side_AmountInUSD) } } }'

            # Set up the variables for the query.
            variables = {
                "tokens": [
                    self.SOL_ADDRESS,  # wSOL
                    self.USDC_ADDRESS,  # USDC
                    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT
                ],
                "base": base_address,
                "dataset": "combined",
                "time_ago": time_ago,
                "interval": 5,
            }

            # Send the POST request.
            response = requests.post(
                self.bitquery_url, json={"query": query, "variables": variables}, headers=self.headers, timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Query failed with status code {response.status_code}: {response.text}")
                return []

            raw_data = response.json()

            try:
                buckets = raw_data["data"]["Solana"]["DEXTradeByTokens"]
            except (KeyError, TypeError):
                logger.warning("Unexpected data format received from the API.")
                return []

            organized_data = []
            for bucket in buckets:
                time_bucket = bucket.get("Block", {}).get("Time")
                open_price = self._safe_float_conversion(bucket.get("open"))
                high_price = self._safe_float_conversion(bucket.get("max"))
                low_price = self._safe_float_conversion(bucket.get("min"))
                close_price = self._safe_float_conversion(bucket.get("close"))
                volume = self._safe_float_conversion(bucket.get("volume"))

                organized_data.append(
                    {
                        "time": time_bucket,
                        "open": open_price,
                        "high": high_price,
                        "low": low_price,
                        "close": close_price,
                        "volume": volume,
                    }
                )

            organized_data.sort(key=lambda x: x["time"] if x["time"] else "")
            return organized_data

        except Exception as e:
            logger.error(f"Error in fetch_and_organize_dex_trade_data: {str(e)}")
            return []

    def get_trending_tokens(self, limit: int = 10):
        """
        Fetches trade summary data from Bitquery using the provided GraphQL query,
        and organizes the returned data into a list of dictionaries for the latest 1-hour data.

        Args:
            limit (int): Number of trending tokens to return

        Returns:
            list of dict: Each dictionary contains organized trading data.

        Raises:
            Exception: If the API request fails or the returned data format is not as expected.
        """
        try:
            # Calculate the time one hour ago in ISO format.
            time_since = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

            # Define the GraphQL query with the dynamic time filter.
            query = f'query MyQuery {{ Solana {{ DEXTradeByTokens( where: {{ Transaction: {{Result: {{Success: true}}}}, Trade: {{Side: {{Currency: {{MintAddress: {{is: "{self.SOL_ADDRESS}"}}}}}}}}, Block: {{Time: {{since: "{time_since}"}}}} }} orderBy: {{descendingByField: "total_trades"}} limit: {{count: {limit}}} ) {{ Trade {{ Currency {{ Name MintAddress Symbol }} start: PriceInUSD(minimum: Block_Time) min5: PriceInUSD( minimum: Block_Time, if: {{Block: {{Time: {{after: "2024-08-15T05:14:00Z"}}}}}} ) end: PriceInUSD(maximum: Block_Time) Dex {{ ProtocolName ProtocolFamily ProgramAddress }} Market {{ MarketAddress }} Side {{ Currency {{ Symbol Name MintAddress }} }} }} makers: count(distinct:Transaction_Signer) total_trades: count total_traded_volume: sum(of: Trade_Side_AmountInUSD) total_buy_volume: sum( of: Trade_Side_AmountInUSD, if: {{Trade: {{Side: {{Type: {{is: buy}}}}}}}} ) total_sell_volume: sum( of: Trade_Side_AmountInUSD, if: {{Trade: {{Side: {{Type: {{is: sell}}}}}}}} ) total_buys: count(if: {{Trade: {{Side: {{Type: {{is: buy}}}}}}}} ) total_sells: count(if: {{Trade: {{Side: {{Type: {{is: sell}}}}}}}} ) }} }} }}'

            # Execute the HTTP POST request.
            response = requests.post(self.bitquery_url, json={"query": query}, headers=self.headers, timeout=30)

            if response.status_code != 200:
                logger.error(f"Query failed with status code {response.status_code}: {response.text}")
                raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

            raw_data = response.json()

            try:
                trade_summaries = raw_data["data"]["Solana"]["DEXTradeByTokens"]
            except (KeyError, TypeError) as err:
                logger.error("Unexpected data format received from the API.")
                raise Exception("Unexpected data format received from the API.") from err

            organized_data = []
            # Process each trade summary item.
            for summary in trade_summaries:
                trade_info = summary.get("Trade", {})
                currency = trade_info.get("Currency", {})
                dex = trade_info.get("Dex", {})
                market = trade_info.get("Market", {})
                side = trade_info.get("Side", {}).get("Currency", {})

                # Parse numeric summary fields with safe conversion.
                makers = self._safe_int_conversion(summary.get("makers", 0))
                total_trades = self._safe_int_conversion(summary.get("total_trades", 0))
                total_traded_volume = self._safe_float_conversion(summary.get("total_traded_volume", 0))
                total_buy_volume = self._safe_float_conversion(summary.get("total_buy_volume", 0))
                total_sell_volume = self._safe_float_conversion(summary.get("total_sell_volume", 0))
                total_buys = self._safe_int_conversion(summary.get("total_buys", 0))
                total_sells = self._safe_int_conversion(summary.get("total_sells", 0))

                organized_item = {
                    "currency": {
                        "Name": currency.get("Name"),
                        "MintAddress": currency.get("MintAddress"),
                        "Symbol": currency.get("Symbol"),
                    },
                    "price": {
                        "start": self._safe_float_conversion(trade_info.get("start")),
                        "min5": self._safe_float_conversion(trade_info.get("min5")),
                        "end": self._safe_float_conversion(trade_info.get("end")),
                    },
                    "dex": {
                        "ProtocolName": dex.get("ProtocolName"),
                        "ProtocolFamily": dex.get("ProtocolFamily"),
                        "ProgramAddress": dex.get("ProgramAddress"),
                    },
                    "market": {"MarketAddress": market.get("MarketAddress")},
                    "side_currency": {
                        "Name": side.get("Name"),
                        "MintAddress": side.get("MintAddress"),
                        "Symbol": side.get("Symbol"),
                    },
                    "makers": makers,
                    "total_trades": total_trades,
                    "total_traded_volume": total_traded_volume,
                    "total_buy_volume": total_buy_volume,
                    "total_sell_volume": total_sell_volume,
                    "total_buys": total_buys,
                    "total_sells": total_sells,
                }
                organized_data.append(organized_item)

            return organized_data

        except Exception as e:
            logger.error(f"Error in get_trending_tokens: {str(e)}")
            raise Exception(f"Failed to fetch trending tokens: {str(e)}")
