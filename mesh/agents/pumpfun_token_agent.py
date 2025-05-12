import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class PumpFunTokenAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("BITQUERY_API_KEY")
        if not self.api_key:
            raise ValueError("BITQUERY_API_KEY environment variable is required")
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        self.bitquery_url = "https://streaming.bitquery.io/eap"

        self.metadata.update(
            {
                "name": "PumpFun Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes Pump.fun token on Solana using Bitquery API. It tracks token creation and graduation events on Pump.fun.",
                "external_apis": ["Bitquery"],
                "tags": ["Solana"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Pumpfun.png",
                "examples": [
                    "Latest token launched on Pump.fun in the last 24 hours",
                ],
            }
        )

        self.VALID_INTERVALS = {"hours", "days"}

    def get_system_prompt(self) -> str:
        return """You are a specialized assistant that analyzes Pump.fun tokens on Solana using Bitquery API. Your capabilities include:

1. Token Creation Tracking: Monitor and analyze newly created tokens on Pump.fun, including:
   - Token basic information (name, symbol, mint address)
   - Initial supply amount
   - Creation timestamp and signer

2. Token Graduation Analysis: Track tokens that have recently graduated on Pump.fun, including:
   - Token identification details
   - Initial price data after graduation
   - Market cap calculation based on initial price
   - Graduation timestamp

Guidelines:
- Present data in a clear, concise, and data-driven manner
- Only mention missing data if it's critical to answer the user's question
- Focus on insights rather than raw data repetition
- For token addresses, use this format: [Mint Address](https://solscan.io/token/Mint_Address)
- Use natural language in responses
- If information is insufficient to answer a question, acknowledge the limitation
- All data is sourced from Bitquery API with real-time updates"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_recent_token_creation",
                    "description": "Fetch data of tokens recently created on Pump.fun on Solana. Results include the basic info like name, symbol, mint address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "interval": {
                                "type": "string",
                                "enum": ["hours", "days"],
                                "default": "hours",
                                "description": "Time interval (hours/days)",
                            },
                            "offset": {
                                "type": "number",
                                "minimum": 1,
                                "maximum": 99,
                                "default": 1,
                                "description": "Time offset for interval",
                            },
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "query_latest_graduated_tokens",
                    "description": "Fetch recently graduated tokens from Pump.fun on Solana with their latest prices and market caps. Graduation means that the token hits a certain market cap threshold, and that it has gained traction and liquidity.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timeframe": {
                                "type": "number",
                                "description": "Timeframe in hours to look back for graduated tokens",
                                "default": 24,
                            },
                        },
                    },
                },
            },
        ]

    async def _execute_query(self, query: str, variables: Dict = None) -> Dict:
        """
        Execute a GraphQL query against the Bitquery API using the base class's _api_request method.

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
                return result

            if "errors" in result:
                error_messages = [error.get("message", "Unknown error") for error in result["errors"]]
                return {"error": f"GraphQL errors: {', '.join(error_messages)}"}

            return result

        except Exception as e:
            logger.error(f"Error in _execute_query: {str(e)}")
            return {"error": f"Query execution failed: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_recent_token_creation(self, interval: str = "hours", offset: int = 1) -> Dict:
        if interval not in self.VALID_INTERVALS:
            return {"error": f"Invalid interval. Must be one of: {', '.join(self.VALID_INTERVALS)}"}

        query = """
        query {
          Solana {
            TokenSupplyUpdates(
              where: {
                Instruction: {
                  Program: {
                    Address: {is: "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"},
                    Method: {is: "create"}
                  }
                }
              }
              limit: {count: 10}
            ) {
              Block {
                Time(interval: {in: INTERVAL_PLACEHOLDER, offset: OFFSET_PLACEHOLDER})
              }
              TokenSupplyUpdate {
                Amount
                Currency {
                  Symbol
                  Name
                  MintAddress
                  ProgramAddress
                  Decimals
                }
                PostBalance
              }
              Transaction {
                Signer
              }
            }
          }
        }
        """.replace("INTERVAL_PLACEHOLDER", interval).replace("OFFSET_PLACEHOLDER", str(offset))

        result = await self._execute_query(query)

        if "error" in result:
            return result

        if "data" in result and "Solana" in result["data"]:
            tokens = result["data"]["Solana"]["TokenSupplyUpdates"]
            filtered_tokens = []

            for token in tokens:
                if "TokenSupplyUpdate" not in token or "Currency" not in token["TokenSupplyUpdate"]:
                    continue

                currency = token["TokenSupplyUpdate"]["Currency"]
                filtered_token = {
                    "block_time": token["Block"]["Time"],
                    "token_info": {
                        "name": currency.get("Name", "Unknown"),
                        "symbol": currency.get("Symbol", "Unknown"),
                        "mint_address": currency.get("MintAddress", ""),
                        "program_address": currency.get("ProgramAddress", ""),
                        "decimals": currency.get("Decimals", 0),
                    },
                    "amount": token["TokenSupplyUpdate"]["Amount"],
                    "signer": token["Transaction"]["Signer"],
                }
                filtered_tokens.append(filtered_token)

            return {"tokens": filtered_tokens[:10]}

        return {"tokens": []}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def query_latest_graduated_tokens(self, timeframe: int = 24) -> Dict:
        """
        Query tokens that have recently graduated on Pump.fun with their prices and market caps.

        Args:
            timeframe (int): Number of hours to look back for graduated tokens

        Returns:
            Dict: Dictionary containing graduated tokens with price and market cap data
        """
        # Calculate the start time as the beginning of the day (00:00 UTC), timeframe hours ago
        now = datetime.now(timezone.utc)
        start_time = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc) - timedelta(hours=timeframe)
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # First query to get graduated tokens
        graduated_query = """
        query ($since: DateTime!) {
          Solana {
            DEXPools(
              where: {
                Block: {
                  Time: {
                    since: $since
                  }
                }
                Pool: {
                  Dex: { ProtocolName: { is: "pump" } }
                  Base: { PostAmount: { eq: "206900000" } }  # This is a specific amount that indicates graduation
                }
                Transaction: { Result: { Success: true } }
              }
              orderBy: { descending: Block_Time }
            ) {
              Block {
                Time
              }
              Pool {
                Market {
                  BaseCurrency {
                    Name
                    Symbol
                    MintAddress
                  }
                  QuoteCurrency {
                    Name
                    Symbol
                  }
                }
              }
            }
          }
        }
        """

        variables = {"since": start_time_str}

        first_result = await self._execute_query(graduated_query, variables)

        if "error" in first_result:
            return {"graduated_tokens": [], "error": first_result["error"]}

        if "data" not in first_result or "Solana" not in first_result["data"]:
            return {"graduated_tokens": [], "error": "Failed to fetch graduated tokens"}

        # Extract token addresses from the first query
        graduated_pools = first_result["data"]["Solana"]["DEXPools"]
        token_addresses = []

        for pool in graduated_pools:
            if "Pool" in pool and "Market" in pool["Pool"] and "BaseCurrency" in pool["Pool"]["Market"]:
                mint_address = pool["Pool"]["Market"]["BaseCurrency"].get("MintAddress")
                if mint_address:
                    token_addresses.append(mint_address)

        if not token_addresses:
            return {"graduated_tokens": [], "message": "No graduated tokens found in the specified timeframe"}

        # Second query to get price data for the graduated tokens from pump swap dex
        price_query = """
        query ($since: DateTime!, $token_addresses: [String!]) {
          Solana {
            DEXTrades(
              limitBy: { by: Trade_Buy_Currency_MintAddress, count: 1 }
              orderBy: { descending: Trade_Buy_Price }
              where: {
                Trade: {
                  Dex: {
                    ProgramAddress: { in: ["pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"] }
                  },
                  Buy: {
                    Currency: {
                      MintAddress: { in: $token_addresses }
                    }
                  },
                  PriceAsymmetry: { le: 0.1 },
                  Sell: { AmountInUSD: { gt: "10" } }
                },
                Transaction: { Result: { Success: true } },
                Block: { Time: { since: $since } }
              }
            ) {
              Trade {
                Buy {
                  Price(maximum: Block_Time)
                  PriceInUSD(maximum: Block_Time)
                  Currency {
                    Name
                    Symbol
                    MintAddress
                    Decimals
                    Fungible
                    Uri
                  }
                }
              }
            }
          }
        }
        """

        price_variables = {"since": start_time_str, "token_addresses": token_addresses}

        second_result = await self._execute_query(price_query, price_variables)

        if "error" in second_result:
            return {"graduated_tokens": [], "token_addresses": token_addresses, "error": second_result["error"]}

        if "data" not in second_result or "Solana" not in second_result["data"]:
            return {
                "graduated_tokens": [],
                "token_addresses": token_addresses,
                "error": "Failed to fetch price data for graduated tokens",
            }

        # Process and format the results
        price_trades = second_result["data"]["Solana"]["DEXTrades"]
        graduated_tokens_with_price = []

        for trade in price_trades:
            if "Trade" in trade and "Buy" in trade["Trade"]:
                buy = trade["Trade"]["Buy"]
                price_usd = buy.get("PriceInUSD", 0)

                try:
                    price_usd_float = float(price_usd) if price_usd else 0
                    market_cap = price_usd_float * 1_000_000_000  # 1 billion as specified
                except (ValueError, TypeError):
                    price_usd_float = 0
                    market_cap = 0

                currency = buy.get("Currency", {})

                token_data = {
                    "price_usd": price_usd_float,
                    "market_cap_usd": market_cap,
                    "token_info": {
                        "name": currency.get("Name", "Unknown"),
                        "symbol": currency.get("Symbol", "Unknown"),
                        "mint_address": currency.get("MintAddress", ""),
                        "decimals": currency.get("Decimals", 0),
                        "fungible": currency.get("Fungible", True),
                        "uri": currency.get("Uri", ""),
                    },
                }
                graduated_tokens_with_price.append(token_data)

        # Find addresses that have graduated but don't have price data
        addresses_with_price = {
            token["token_info"]["mint_address"]
            for token in graduated_tokens_with_price
            if token["token_info"]["mint_address"]
        }
        addresses_without_price = [addr for addr in token_addresses if addr not in addresses_with_price]

        return {
            "graduated_tokens": graduated_tokens_with_price,
            "tokens_without_price_data": addresses_without_price,
            "timeframe_hours": timeframe,
            "start_time": start_time_str,
        }

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        This method is required by the MeshAgent abstract base class.
        """
        if tool_name == "query_recent_token_creation":
            interval = function_args.get("interval", "hours")
            offset = function_args.get("offset", 1)
            result = await self.query_recent_token_creation(interval=interval, offset=offset)
        elif tool_name == "query_latest_graduated_tokens":
            timeframe = function_args.get("timeframe", 24)
            result = await self.query_latest_graduated_tokens(timeframe=timeframe)
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

        if errors := self._handle_error(result):
            return errors

        return result
