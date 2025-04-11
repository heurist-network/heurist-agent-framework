import asyncio
import logging
import os
import uuid
from typing import Any, Dict, List

import aiohttp
import pydash as _py
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from decorators import with_cache
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class SolWalletAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://mainnet.helius-rpc.com"
        self.request_semaphore = asyncio.Semaphore(2)
        self.metadata.update(
            {
                "name": "SolWallet Agent",
                "version": "1.0.0",
                "author": "QuantVela",
                "author_address": "0x53cc700f818DD0b440598c666De2D630F9d47273",
                "description": "This agent can query Solana wallet assets and recent swap transactions using Helius API.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about Solana wallet assets and transactions",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw data without LLM explanation",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of the wallet data",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured wallet data including assets and transactions",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Helius"],
                "tags": ["Solana"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Solana.png",
            }
        )

    async def _request(self, method, url, data=None, json=None, headers=None, params=None, timeout=30):
        """Make a request to the Helius API using a new session for each request with rate limiting"""
        try:
            async with self.request_semaphore:  # Use semaphore to limit concurrent requests
                async with aiohttp.ClientSession() as session:
                    await asyncio.sleep(0.5)

                    async with session.request(
                        method,
                        url,
                        data=data,
                        json=json,
                        headers=headers,
                        params=params,
                        timeout=aiohttp.ClientTimeout(total=timeout),
                    ) as response:
                        match response.status:
                            case 200:
                                return await response.json()
                            case 429:
                                logger.warning("Rate limit hit, waiting before retry...")
                                await asyncio.sleep(2.0)
                                raise aiohttp.ClientError("Rate limit exceeded")
                            case _:
                                # should add better error log
                                txt = await response.text()
                                logger.error(txt)
                                return {}

        except aiohttp.ClientResponseError as e:
            error_msg = f"HTTP error {e.status}: {e.message}"
            raise aiohttp.ClientResponseError(e.request_info, e.history, status=e.status, message=error_msg)
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Request failed: {str(e)}")

    async def _post(self, url: str, json: dict):
        headers = {"Content-Type": "application/json"}
        return await self._request("POST", url=url, json=json, headers=headers, timeout=10)

    async def _get(self, url: str, params: dict):
        headers = {"Content-Type": "application/json"}
        return await self._request("GET", url=url, params=params, headers=headers, timeout=10)

    def _format_amount(self, amount: int, decimals: int) -> str:
        """Helper function to format token amounts"""
        return str(amount / (10**decimals))

    def get_system_prompt(self) -> str:
        return """You are a Solana blockchain data expert who can access wallet assets and transaction information through the Helius API.

        CAPABILITIES:
        - Query wallet token holdings
        - Analyze token holder patterns
        - View wallet swap transaction history

        RESPONSE GUIDELINES:
        - Keep responses concise and focused on the specific data requested
        - Format monetary values in a readable way (e.g. "$150.4M")
        - Only provide metrics relevant to the query
        - Highlight any anomalies or significant patterns if found
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_wallet_assets",
                    "description": "Query and retrieve all token holdings for a specific Solana wallet address. This tool helps you get detailed information about each asset including token amounts, current prices and total holding values. Use this when you need to analyze a wallet's portfolio or track significant token holdings.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner_address": {"type": "string", "description": "The Solana wallet address to query"}
                        },
                        "required": ["owner_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_common_holdings_of_top_holders",
                    "description": "Analyze the top tokens commonly held by the holders of a specific token. This tool provides insights into the top 5 most valuable tokens (by total holding value) that are held by the token holders. Use this when you need to understand what other tokens are popular among the holders of a specific token.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {
                                "type": "string",
                                "description": "The Solana token mint address to analyze",
                            },
                            "top_n": {
                                "type": "integer",
                                "description": "Number of top holders to analyze for token holdings (default: 20)",
                                "default": 20,
                            },
                        },
                        "required": ["token_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_tx_history",
                    "description": "Fetch and analyze recent SWAP transactions for a Solana wallet. This tool helps you track trading activity by providing detailed information about token swaps, including amounts, prices, and transaction types (BUY/SELL). Use this when you need to understand a wallet's trading behavior or monitor specific swap activities.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner_address": {
                                "type": "string",
                                "description": "The Solana wallet address to query transaction history for",
                            }
                        },
                        "required": ["owner_address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      HELIUS API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=600)
    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        wait=wait_exponential(multiplier=1.0, min=1.0, max=20.0),  # Increased wait times
        stop=stop_after_attempt(5),
    )
    async def _get_holders(self, token_address: str, top_n: int = 20) -> List[Dict]:
        """
        Query the HELIUS API to get the token top holders for a given token address.
        """
        try:
            logger.info(f"Querying token holders for address: {token_address}")
            all_holders = []
            cursor = None

            while True:
                payload = {
                    "jsonrpc": "2.0",
                    "id": f"get-token-accounts-{uuid.uuid4()}",
                    "method": "getTokenAccounts",
                    "params": {"mint": token_address, "limit": 1000, "cursor": cursor},
                }

                data = await self._post(url=f"{self.api_url}/?api-key={os.getenv('HELIUS_API_KEY')}", json=payload)

                if not data.get("result", {}).get("token_accounts"):
                    break

                all_holders.extend(data["result"]["token_accounts"])
                cursor = data["result"].get("cursor")

                if not cursor:
                    break

            if not all_holders:
                return []

            total_supply = sum(float(account["amount"]) for account in all_holders)

            holders = [
                {
                    "address": account["owner"],
                    "amount": float(account["amount"]),
                    "percentage": f"{(float(account['amount']) / total_supply * 100):.2f}",
                }
                for account in all_holders
            ]

            return sorted(holders, key=lambda x: x["amount"], reverse=True)[:top_n]

        except Exception as e:
            logger.error(f"Error querying token holders: {str(e)}")
            return []

    @with_cache(ttl_seconds=600)
    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        wait=wait_exponential(multiplier=1.0, min=1.0, max=20.0),  # Increased wait times
        stop=stop_after_attempt(5),
    )
    async def get_wallet_assets(self, owner_address: str) -> List[Dict]:
        """
        Query the HELIUS API to get the wallet assets for a given owner address.
        """
        try:
            logger.info(f"Querying wallet assets for address: {owner_address}")
            payload = {
                "jsonrpc": "2.0",
                "id": f"search-assets-{uuid.uuid4()}",
                "method": "searchAssets",
                "params": {
                    "ownerAddress": owner_address,
                    "tokenType": "fungible",
                    "page": 1,
                    "limit": 100,
                    "sortBy": {"sortBy": "recent_action", "sortDirection": "desc"},
                    "options": {"showNativeBalance": True},
                },
            }

            data = await self._post(url=f"{self.api_url}/?api-key={os.getenv('HELIUS_API_KEY')}", json=payload)

            if data is None:
                return []
            if isinstance(data, dict) and not data.get("result"):
                return []

            # filter assets with price info and total price > 100
            filtered_assets = [
                item
                for item in data["result"]["items"]
                if (
                    item.get("token_info", {}).get("price_info")
                    and item["token_info"]["price_info"].get("total_price", 0) > 100
                )
            ]
            # filter non mutable assets
            non_mutable_assets = [asset for asset in filtered_assets if not asset.get("mutable", False)]

            hold_tokens = []

            # Add other token balances
            hold_tokens.extend(
                [
                    {
                        "token_address": asset["id"],
                        # "token_img": (
                        #     asset.get("content", {}).get("files", [{}])[0]
                        #     if asset.get("content", {}).get("files")
                        #     else {}
                        # ).get("cdn_uri", ""),
                        "symbol": asset.get("token_info", {}).get("symbol", ""),
                        "price_per_token": asset.get("token_info", {}).get("price_info", {}).get("price_per_token", 0),
                        "total_holding_value": asset.get("token_info", {}).get("price_info", {}).get("total_price", 0),
                    }
                    for asset in non_mutable_assets
                ]
            )

            return hold_tokens

        except Exception as e:
            logger.error(f"Error querying HELIUS API: {str(e)}")
            return []

    @with_cache(ttl_seconds=600)
    @retry(
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        wait=wait_exponential(multiplier=1.0, min=1.0, max=20.0),  # Increased wait times
        stop=stop_after_attempt(5),
    )
    async def analyze_common_holdings_of_top_holders(self, token_address: str, top_n: int = 20) -> Dict:
        """
        Analyze the token holders and find the top 5 most valuable tokens they hold.
        """
        try:
            holders = await self._get_holders(token_address, top_n)

            if not holders:
                return {"error": "No holders found"}

            raydium_address = "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"
            top_holders = [h for h in holders if h["address"] != raydium_address]

            if not top_holders:
                return {"error": "No valid holders found after filtering"}

            batch_size = 3
            common_tokens = {}

            for i in range(0, len(top_holders), batch_size):
                batch = top_holders[i : i + batch_size]
                for holder in batch:
                    assets = await self.get_wallet_assets(holder["address"])

                    if assets is None or (isinstance(assets, dict) and "error" in assets):
                        continue

                    for token in assets:
                        token_address = token["token_address"]
                        if token_address not in common_tokens:
                            common_tokens[token_address] = {
                                "token_address": token_address,
                                "symbol": token["symbol"],
                                "price_per_token": token["price_per_token"],
                                "total_holding_value": 0,
                                "holder_count": 0,
                            }

                        common_tokens[token_address]["total_holding_value"] += token["total_holding_value"]
                        common_tokens[token_address]["holder_count"] += 1

                await asyncio.sleep(1.0)

            # sort by total_holding_value and get top 5
            sorted_tokens = sorted(common_tokens.values(), key=lambda x: x["total_holding_value"], reverse=True)[:5]

            logger.info(f"Successfully analyzed holders for token: {token_address}")

            # If there are no common tokens found, return a more detailed error
            if not sorted_tokens:
                return {"common_tokens": [], "message": "No common tokens found among token holders"}

            return {"common_tokens": sorted_tokens, "analyzed_holders": len(top_holders)}

        except Exception as e:
            logger.error(f"Error analyzing holders: {str(e)}")
            return {"error": f"Failed to analyze token holders: {str(e)}"}

    @with_cache(ttl_seconds=600)
    @retry(
        wait=wait_exponential(multiplier=1.0, min=1.0, max=20.0),  # Increased wait times
        stop=stop_after_attempt(5),
    )
    async def get_tx_history(self, owner_address: str) -> Dict:
        """
        Query the HELIUS API to get swap transaction history for a given wallet address.
        """
        try:
            logger.info(f"Querying transaction history for address: {owner_address}")

            api_key = os.getenv("HELIUS_API_KEY")
            if not api_key:
                return {"error": "HELIUS_API_KEY not set in environment variables"}

            params = {"api-key": api_key, "type": ["SWAP"], "limit": 100}

            url = f"https://api.helius.xyz/v0/addresses/{owner_address}/transactions"

            data = await self._get(url=url, params=params)

            if not data:
                logger.warning(f"No data returned for address: {owner_address}")
                return {"transactions": [], "message": "No transaction data found"}

            if not isinstance(data, list):
                logger.warning(f"Unexpected data format: {type(data)}")
                return {"error": f"Unexpected data format: {type(data)}"}

            swap_txs = []
            SOL_ADDRESS = "So11111111111111111111111111111111111111112"

            swap_type = [tx for tx in data if _py.get(tx, "type") == "SWAP"]

            for tx in swap_type:
                swap_event = _py.get(tx, "events.swap")
                if not swap_event:
                    continue

                processed_data = {
                    "account": _py.get(tx, "feePayer", ""),
                    "timestamp": _py.get(tx, "timestamp", 0),
                    "description": _py.get(tx, "description", ""),
                }

                # Process token_in information
                if _py.get(swap_event, "nativeInput.amount", 0):
                    processed_data.update(
                        {
                            "token_in_address": SOL_ADDRESS,
                            "token_in_amount": self._format_amount(
                                int(_py.get(swap_event, "nativeInput.amount", 0)), 9
                            ),
                        }
                    )
                elif _py.get(swap_event, "tokenInputs"):
                    token_input = _py.get(swap_event, "tokenInputs.0", {})
                    processed_data.update(
                        {
                            "token_in_address": _py.get(token_input, "mint", ""),
                            "token_in_amount": self._format_amount(
                                int(_py.get(token_input, "rawTokenAmount.tokenAmount", 0)),
                                _py.get(token_input, "rawTokenAmount.decimals", 0),
                            ),
                        }
                    )

                # Process token_out information
                if _py.get(swap_event, "nativeOutput.amount", 0):
                    processed_data.update(
                        {
                            "token_out_address": SOL_ADDRESS,
                            "token_out_amount": self._format_amount(
                                int(_py.get(swap_event, "nativeOutput.amount", 0)), 9
                            ),
                        }
                    )
                elif _py.get(swap_event, "tokenOutputs"):
                    token_output = _py.get(swap_event, "tokenOutputs.0", {})
                    processed_data.update(
                        {
                            "token_out_address": _py.get(token_output, "mint", ""),
                            "token_out_amount": self._format_amount(
                                int(_py.get(token_output, "rawTokenAmount.tokenAmount", 0)),
                                _py.get(token_output, "rawTokenAmount.decimals", 0),
                            ),
                        }
                    )

                # Determine transaction type
                if _py.get(processed_data, "token_in_address") == SOL_ADDRESS:
                    processed_data["type"] = "BUY"
                elif _py.get(processed_data, "token_out_address") == SOL_ADDRESS:
                    processed_data["type"] = "SELL"
                else:
                    processed_data["type"] = "SWAP"

                swap_txs.append(processed_data)

            # Return a structured response
            return {"transactions": swap_txs, "count": len(swap_txs)}

        except Exception as e:
            logger.error(f"Error querying transaction history: {str(e)}")
            return {"error": f"Failed to query transaction history: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        try:
            if tool_name == "get_wallet_assets":
                owner_address = function_args.get("owner_address")
                if not owner_address:
                    return {"error": "owner_address is required"}

                result = await self.get_wallet_assets(owner_address)
                if not result:
                    return {"assets": [], "message": "No assets found"}

                return {"assets": result}

            elif tool_name == "analyze_common_holdings_of_top_holders":
                token_address = function_args.get("token_address")
                if not token_address:
                    return {"error": "token_address is required"}

                top_n = function_args.get("top_n", 20)
                result = await self.analyze_common_holdings_of_top_holders(token_address, top_n)
                return result

            elif tool_name == "get_tx_history":
                owner_address = function_args.get("owner_address")
                if not owner_address:
                    return {"error": "owner_address is required"}

                result = await self.get_tx_history(owner_address)

                return result

            else:
                return {"error": f"Unsupported tool: {tool_name}"}

        except Exception as e:
            logger.error(f"Error in _handle_tool_logic for {tool_name}: {str(e)}")
            return {"error": f"Tool execution failed: {str(e)}"}
