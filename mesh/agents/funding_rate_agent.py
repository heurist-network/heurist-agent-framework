import logging
from typing import Any, Dict, List

import requests

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
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about funding rates, specific trading pairs, or requests to find arbitrage opportunities.",
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
                        "description": "Natural language explanation of the funding rate data or arbitrage opportunities.",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured funding rate data or arbitrage opportunities.",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Coinsider"],
                "tags": ["Arbitrage"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/FundingRate.png",  # crop this pic https://coinpedia.org/price-analysis/crypto-market-trends-why-prices-are-up-but-activity-slows/
                "examples": [
                    "What is the funding rate for BTC on Binance?",
                    "Find arbitrage opportunities between Binance and Bybit",
                    "Best opportunities for arbitraging funding rates of SOL",
                    "Get the latest funding rates for SOL across all exchanges",
                ],
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
    async def get_all_funding_rates(self) -> dict:
        try:
            response = requests.get(f"{self.api_url}/funding_rate/all")
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
                return {"funding_rates": data["data"]}
            else:
                return {"error": "Unexpected API response format"}

        except requests.RequestException as e:
            logger.error(f"Error fetching funding rates: {e}")
            return {"error": f"Failed to fetch funding rates: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_symbol_funding_rates(self, symbol: str) -> dict:
        try:
            all_rates = await self.get_all_funding_rates()
            if "error" in all_rates:
                return all_rates

            funding_rates = all_rates.get("funding_rates", [])
            symbol_rates = [rate for rate in funding_rates if rate.get("symbol") == symbol.upper()]

            if not symbol_rates:
                return {"error": f"No funding rate data found for symbol {symbol}"}

            return {"symbol": symbol, "funding_rates": symbol_rates}

        except Exception as e:
            logger.error(f"Error fetching symbol funding rates: {e}")
            return {"error": f"Failed to fetch funding rates for {symbol}: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def find_cross_exchange_opportunities(self, min_funding_rate_diff: float = 0.0003) -> dict:
        try:
            all_rates = await self.get_all_funding_rates()
            if "error" in all_rates:
                return all_rates

            funding_data = all_rates.get("funding_rates", [])

            # Group by trading pair symbol
            symbols_map = {}
            for item in funding_data:
                symbol = item.get("symbol")
                if not symbol:
                    continue

                if symbol not in symbols_map:
                    symbols_map[symbol] = []

                exchange_id = item.get("exchange")
                item_copy = item.copy()
                if isinstance(exchange_id, dict) and "id" in exchange_id:
                    item_copy["exchange"] = exchange_id.get("id")

                symbols_map[symbol].append(item_copy)

            # Filter out trading pairs with arbitrage opportunities
            opportunities = []
            funding_rate_period = "1d"  # Using 1-day average funding rate

            for symbol, exchanges_data in symbols_map.items():
                # Skip if the trading pair is only listed on one exchange
                if len(exchanges_data) < 2:
                    continue

                # Sort by funding rate
                exchanges_data.sort(
                    key=lambda x: x["rates"][funding_rate_period]
                    if "rates" in x
                    and funding_rate_period in x["rates"]
                    and x["rates"][funding_rate_period] is not None
                    else 0
                )

                # Get the exchanges with the lowest and highest funding rates
                lowest_rate_exchange = exchanges_data[0]
                highest_rate_exchange = exchanges_data[-1]

                # Safely get funding rates
                lowest_rate = (
                    lowest_rate_exchange["rates"][funding_rate_period]
                    if "rates" in lowest_rate_exchange
                    and funding_rate_period in lowest_rate_exchange["rates"]
                    and lowest_rate_exchange["rates"][funding_rate_period] is not None
                    else 0
                )
                highest_rate = (
                    highest_rate_exchange["rates"][funding_rate_period]
                    if "rates" in highest_rate_exchange
                    and funding_rate_period in highest_rate_exchange["rates"]
                    and highest_rate_exchange["rates"][funding_rate_period] is not None
                    else 0
                )

                # Calculate funding rate difference
                rate_diff = highest_rate - lowest_rate

                # If the difference exceeds the threshold, consider it an arbitrage opportunity
                if rate_diff >= min_funding_rate_diff:
                    lowest_exchange_id = lowest_rate_exchange.get("exchange")
                    highest_exchange_id = highest_rate_exchange.get("exchange")

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
                            "name": self.exchange_map.get(lowest_exchange_id, "Unknown"),
                            "rate": lowest_rate,
                            "funding_interval": lowest_funding_interval,
                            "quote_currency": lowest_rate_exchange.get("quote_currency", "USDT"),
                        },
                        "short_exchange": {
                            "id": highest_exchange_id,
                            "name": self.exchange_map.get(highest_exchange_id, "Unknown"),
                            "rate": highest_rate,
                            "funding_interval": highest_funding_interval,
                            "quote_currency": highest_rate_exchange.get("quote_currency", "USDT"),
                        },
                    }

                    opportunities.append(opportunity)

            return {"cross_exchange_opportunities": opportunities}

        except Exception as e:
            logger.error(f"Error finding cross-exchange opportunities: {e}")
            return {"error": f"Failed to find cross-exchange opportunities: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def find_spot_futures_opportunities(self, min_funding_rate: float = 0.0003) -> dict:
        try:
            all_rates = await self.get_all_funding_rates()
            if "error" in all_rates:
                return all_rates

            funding_data = all_rates.get("funding_rates", [])
            opportunities = []
            funding_rate_period = "1d"  # Using 1-day average funding rate
            excluded_symbols = ["1000LUNC", "1000SHIB", "1000BTT"]  # Symbols to exclude

            for item in funding_data:
                symbol = item.get("symbol")
                if not symbol or symbol in excluded_symbols:
                    continue

                if (
                    "rates" not in item
                    or funding_rate_period not in item["rates"]
                    or item["rates"][funding_rate_period] is None
                ):
                    continue
                funding_rate = item["rates"][funding_rate_period]

                if not funding_rate or funding_rate <= 0:
                    continue

                if funding_rate >= min_funding_rate:
                    exchange_id = item.get("exchange")
                    if isinstance(exchange_id, dict) and "id" in exchange_id:
                        exchange_id = exchange_id.get("id")

                    if exchange_id is None:
                        continue

                    exchange_name = self.exchange_map.get(exchange_id, "Unknown")
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

            return {"spot_futures_opportunities": opportunities}

        except Exception as e:
            logger.error(f"Error finding spot-futures opportunities: {e}")
            return {"error": f"Failed to find spot-futures opportunities: {str(e)}"}

    def format_funding_rates(self, data: List[Dict]) -> List[Dict]:
        """Format funding rate information in a structured way"""
        formatted_rates = []

        for rate in data:
            exchange_id = rate.get("exchange")
            exchange_name = "Unknown"
            if isinstance(exchange_id, int):
                exchange_name = self.exchange_map.get(exchange_id, "Unknown")
            elif isinstance(exchange_id, dict) and "id" in exchange_id:
                exchange_id_value = exchange_id.get("id")
                if isinstance(exchange_id_value, int):
                    exchange_name = self.exchange_map.get(exchange_id_value, "Unknown")
                    exchange_id = exchange_id_value

            formatted_rate = {
                "symbol": rate.get("symbol", "N/A"),
                "exchange": {
                    "id": exchange_id,
                    "name": exchange_name,
                },
                "rates": {
                    "1h": rate.get("rates", {}).get("1h", "N/A"),
                    "1d": rate.get("rates", {}).get("1d", "N/A"),
                    "7d": rate.get("rates", {}).get("7d", "N/A"),
                },
                "funding_interval": rate.get("funding_interval", 8),
                "last_updated": rate.get("updated_at", "N/A"),
            }
            formatted_rates.append(formatted_rate)

        return formatted_rates

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        A single method that calls the appropriate function, handles errors/formatting
        """
        if tool_name == "get_all_funding_rates":
            logger.info("Getting all funding rates")
            result = await self.get_all_funding_rates()
            errors = self._handle_error(result)
            if errors:
                return errors

            # Format the data before returning
            if "funding_rates" in result:
                result["funding_rates"] = self.format_funding_rates(result["funding_rates"])

            return result

        elif tool_name == "get_symbol_funding_rates":
            symbol = function_args.get("symbol")
            if not symbol:
                return {"error": "Missing 'symbol' in tool_arguments"}

            logger.info(f"Getting funding rates for {symbol}")
            result = await self.get_symbol_funding_rates(symbol)
            errors = self._handle_error(result)
            if errors:
                return errors

            # Format the data before returning
            if "funding_rates" in result:
                result["funding_rates"] = self.format_funding_rates(result["funding_rates"])

            return result

        elif tool_name == "find_cross_exchange_opportunities":
            min_funding_rate_diff = function_args.get("min_funding_rate_diff", 0.0003)
            logger.info(f"Finding cross-exchange opportunities with min diff of {min_funding_rate_diff}")

            result = await self.find_cross_exchange_opportunities(min_funding_rate_diff)
            errors = self._handle_error(result)
            if errors:
                return errors

            return result

        elif tool_name == "find_spot_futures_opportunities":
            min_funding_rate = function_args.get("min_funding_rate", 0.0003)
            logger.info(f"Finding spot-futures opportunities with min rate of {min_funding_rate}")

            result = await self.find_spot_futures_opportunities(min_funding_rate)
            errors = self._handle_error(result)
            if errors:
                return errors

            return result

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}
