import logging
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class FundingRateAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.coinsider.app/api"

        self.metadata.update(
            {
                "name": "Funding Rate Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch funding rate data and identify arbitrage opportunities across cryptocurrency exchanges.",
                "external_apis": ["Coinsider"],
                "tags": ["Arbitrage"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/FundingRate.png",
                "examples": [
                    "What is the funding rate for BTC on Binance?",
                    "Find arbitrage opportunities between Binance and Bybit",
                    "Best opportunities for arbitraging funding rates of SOL",
                    "Get the latest funding rates for SOL across all exchanges",
                ],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": {
                        "get_all_funding_rates": "0.02",
                        "get_symbol_funding_rates": "0.01",
                    },
                },
            }
        )

        # Exchange mapping for reference
        self.exchange_map = {
            1: "Binance",
            2: "OKX",
            3: "Bybit",
            4: "Gate.io",
            5: "Bitget",
            6: "dYdX",
            7: "Bitmex",
        }

    def get_system_prompt(self) -> str:
        return """
    IDENTITY:
    You are a cryptocurrency funding rate specialist that can fetch and analyze funding rate data from Coinsider.

    CAPABILITIES:
    - Fetch all current funding rates across exchanges
    - Identify cross-exchange funding rate arbitrage opportunities
    - Identify spot-futures funding rate arbitrage opportunities
    - Analyze specific trading pairs' funding rates

    RESPONSE GUIDELINES:
    - Keep responses focused on what was specifically asked
    - Format funding rates as percentages with 4 decimal places (e.g., "0.0123%")
    - Provide only relevant metrics for the query context
    - For arbitrage opportunities, clearly explain the strategy and potential risks

    DOMAIN-SPECIFIC RULES:
    When analyzing funding rates, consider these important factors:
    1. Funding intervals vary by exchange (typically 8h, but can be 1h, 4h, etc.)
    2. Cross-exchange arbitrage requires going long on the exchange with lower/negative funding and short on the exchange with higher/positive funding
    3. Spot-futures arbitrage requires holding the spot asset and shorting the perpetual futures contract
    4. Always consider trading fees, slippage, and minimum viable position sizes in recommendations

    For cross-exchange opportunities, a significant opportunity typically requires at least 0.03% funding rate difference.
    For spot-futures opportunities, a significant opportunity typically requires at least 0.01% positive funding rate.

    IMPORTANT:
    - Always indicate funding intervals in hours when comparing rates
    - Mention exchange names rather than just IDs in explanations
    - Consider risk factors like liquidity and counterparty risk"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_all_funding_rates",
                    "description": "Get all current funding rates across exchanges",
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
                    "name": "get_symbol_funding_rates",
                    "description": "Get funding rates for a specific trading pair across all exchanges",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "The trading pair symbol (e.g., BTC, ETH, SOL)"}
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "find_cross_exchange_opportunities",
                    "description": "Find cross-exchange funding rate arbitrage opportunities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min_funding_rate_diff": {
                                "type": "number",
                                "description": "Minimum funding rate difference to consider (default: 0.0003)",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "find_spot_futures_opportunities",
                    "description": "Find spot-futures funding rate arbitrage opportunities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min_funding_rate": {
                                "type": "number",
                                "description": "Minimum funding rate to consider (default: 0.0003)",
                            }
                        },
                        "required": [],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      COINSIDER API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_all_funding_rates(self) -> Dict[str, Any]:
        """
        Get all current funding rates across exchanges.
        """
        logger.info("Fetching all funding rates")

        try:
            url = f"{self.api_url}/funding_rate/all"
            response = await self._api_request(url=url, method="GET")

            if "error" in response:
                logger.error(f"Error fetching all funding rates: {response['error']}")
                return {"error": response["error"]}

            if isinstance(response, dict) and "data" in response and isinstance(response["data"], list):
                # Filter for Binance only (exchange = 1)
                binance_data = [rate for rate in response["data"] if rate.get("exchange") == 1]
                formatted_rates = self.format_funding_rates(binance_data)
                logger.info(f"Successfully retrieved {len(formatted_rates)} funding rates")
                # Return minimal format: ["symbol", rate, "4h"] for token efficiency
                return {"rates": formatted_rates, "format": ["symbol", "rate", "interval"]}
            else:
                logger.error("Unexpected API response format for all funding rates")
                return {"status": "error", "error": "Unexpected API response format"}

        except Exception as e:
            logger.error(f"Exception in get_all_funding_rates: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch funding rates: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_symbol_funding_rates(self, symbol: str) -> Dict[str, Any]:
        """
        Get funding rates for a specific trading pair across all exchanges.
        """
        logger.info(f"Fetching funding rates for symbol: {symbol}")

        try:
            all_rates_result = await self.get_all_funding_rates()
            if "error" in all_rates_result:
                return all_rates_result

            all_rates = all_rates_result.get("data", {}).get("funding_rates", [])
            symbol_rates = [rate for rate in all_rates if rate.get("symbol") == symbol.upper()]

            if not symbol_rates:
                logger.warning(f"No funding rate data found for symbol {symbol}")
                return {"status": "no_data", "error": f"No funding rate data found for symbol {symbol}"}

            logger.info(f"Found {len(symbol_rates)} funding rates for symbol {symbol}")
            return {"status": "success", "data": {"symbol": symbol, "funding_rates": symbol_rates}}

        except Exception as e:
            logger.error(f"Exception in get_symbol_funding_rates: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch funding rates for {symbol}: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def find_cross_exchange_opportunities(self, min_funding_rate_diff: float = 0.0003) -> Dict[str, Any]:
        """
        Find cross-exchange funding rate arbitrage opportunities.
        """
        logger.info(f"Finding cross-exchange opportunities with min diff: {min_funding_rate_diff}")

        try:
            all_rates_result = await self.get_all_funding_rates()
            if "error" in all_rates_result:
                return all_rates_result

            funding_data = all_rates_result.get("data", {}).get("funding_rates", [])

            # Group by trading pair symbol
            symbols_map = {}
            for item in funding_data:
                symbol = item.get("symbol")
                if not symbol:
                    continue

                if symbol not in symbols_map:
                    symbols_map[symbol] = []

                exchange_id = item.get("exchange", {}).get("id")
                if exchange_id:
                    symbols_map[symbol].append(item)

            # Filter out trading pairs with arbitrage opportunities
            opportunities = []
            funding_rate_period = "latest"  # Changed from "1d" to "latest"

            for symbol, exchanges_data in symbols_map.items():
                # Skip if the trading pair is only listed on one exchange
                if len(exchanges_data) < 2:
                    continue

                # Sort by funding rate
                exchanges_data.sort(key=lambda x: x.get("rates", {}).get(funding_rate_period, 0) or 0)

                # Get the exchanges with the lowest and highest funding rates
                lowest_rate_exchange = exchanges_data[0]
                highest_rate_exchange = exchanges_data[-1]

                # Safely get funding rates
                lowest_rate = lowest_rate_exchange.get("rates", {}).get(funding_rate_period, 0) or 0
                highest_rate = highest_rate_exchange.get("rates", {}).get(funding_rate_period, 0) or 0

                # Calculate funding rate difference
                rate_diff = highest_rate - lowest_rate

                # If the difference exceeds the threshold, consider it an arbitrage opportunity
                if rate_diff >= min_funding_rate_diff:
                    lowest_exchange_id = lowest_rate_exchange.get("exchange", {}).get("id")
                    lowest_exchange_name = lowest_rate_exchange.get("exchange", {}).get("name", "Unknown")

                    highest_exchange_id = highest_rate_exchange.get("exchange", {}).get("id")
                    highest_exchange_name = highest_rate_exchange.get("exchange", {}).get("name", "Unknown")

                    # Skip if missing necessary information
                    if lowest_exchange_id is None or highest_exchange_id is None:
                        continue

                    lowest_funding_interval = lowest_rate_exchange.get("funding_interval", 8)
                    highest_funding_interval = highest_rate_exchange.get("funding_interval", 8)

                    opportunity = {
                        "symbol": symbol,
                        "rate_diff": rate_diff,
                        "long_exchange": {
                            "id": lowest_exchange_id,
                            "name": lowest_exchange_name,
                            "rate": lowest_rate,
                            "funding_interval": lowest_funding_interval,
                            "quote_currency": lowest_rate_exchange.get("quote_currency", "USDT"),
                        },
                        "short_exchange": {
                            "id": highest_exchange_id,
                            "name": highest_exchange_name,
                            "rate": highest_rate,
                            "funding_interval": highest_funding_interval,
                            "quote_currency": highest_rate_exchange.get("quote_currency", "USDT"),
                        },
                    }

                    opportunities.append(opportunity)

            logger.info(f"Found {len(opportunities)} cross-exchange opportunities")
            return {"status": "success", "data": {"cross_exchange_opportunities": opportunities}}

        except Exception as e:
            logger.error(f"Exception in find_cross_exchange_opportunities: {str(e)}")
            return {"status": "error", "error": f"Failed to find cross-exchange opportunities: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def find_spot_futures_opportunities(self, min_funding_rate: float = 0.0003) -> Dict[str, Any]:
        """
        Find spot-futures funding rate arbitrage opportunities.
        """
        logger.info(f"Finding spot-futures opportunities with min rate: {min_funding_rate}")

        try:
            all_rates_result = await self.get_all_funding_rates()
            if "error" in all_rates_result:
                return all_rates_result

            funding_data = all_rates_result.get("data", {}).get("funding_rates", [])
            opportunities = []
            funding_rate_period = "latest"  # Changed from "1d" to "latest"
            excluded_symbols = ["1000LUNC", "1000SHIB", "1000BTT"]  # Symbols to exclude

            for item in funding_data:
                symbol = item.get("symbol")
                if not symbol or symbol in excluded_symbols:
                    continue

                funding_rate = item.get("rates", {}).get(funding_rate_period)
                if not funding_rate or funding_rate <= 0:
                    continue

                if funding_rate >= min_funding_rate:
                    exchange_id = item.get("exchange", {}).get("id")
                    exchange_name = item.get("exchange", {}).get("name", "Unknown")

                    if exchange_id is None:
                        continue

                    funding_interval = item.get("funding_interval", 8)  # Default to 8 hours

                    opportunity = {
                        "symbol": symbol,
                        "exchange_id": exchange_id,
                        "exchange_name": exchange_name,
                        "funding_rate": funding_rate,
                        "funding_interval": funding_interval,
                        "quote_currency": item.get("quote_currency", "USDT"),
                    }

                    opportunities.append(opportunity)

            logger.info(f"Found {len(opportunities)} spot-futures opportunities")
            return {"status": "success", "data": {"spot_futures_opportunities": opportunities}}

        except Exception as e:
            logger.error(f"Exception in find_spot_futures_opportunities: {str(e)}")
            return {"status": "error", "error": f"Failed to find spot-futures opportunities: {str(e)}"}

    def format_funding_rates(self, data: List[Dict]) -> List[Dict]:
        """Format funding rate information in a token-efficient way"""
        formatted_rates = []

        for rate in data:
            # Get rate value, skip if invalid
            latest_rate = rate.get("rates", {}).get("latest")
            if latest_rate is None:
                continue

            # Use minimal format: [symbol, rate, interval_string]
            formatted_rates.append([
                rate.get("symbol", "?"),
                latest_rate,
                f"{rate.get('funding_interval', 8)}h"
            ])

        # Sort by rate descending for most relevant data first
        formatted_rates.sort(key=lambda x: abs(x[1]) if x[1] is not None else 0, reverse=True)
        return formatted_rates

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution and return the raw data"""

        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_all_funding_rates":
            result = await self.get_all_funding_rates()

        elif tool_name == "get_symbol_funding_rates":
            symbol = function_args.get("symbol")
            if not symbol:
                return {"error": "Missing 'symbol' parameter"}

            result = await self.get_symbol_funding_rates(symbol)

        elif tool_name == "find_cross_exchange_opportunities":
            min_funding_rate_diff = function_args.get("min_funding_rate_diff", 0.0003)
            result = await self.find_cross_exchange_opportunities(min_funding_rate_diff)

        elif tool_name == "find_spot_futures_opportunities":
            min_funding_rate = function_args.get("min_funding_rate", 0.0003)
            result = await self.find_spot_futures_opportunities(min_funding_rate)

        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
