import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class ZerionWalletAnalysisAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Zerion Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch and analyze the token and NFT holdings of a crypto wallet (must be EVM chain)",
                "inputs": [
                    {
                        "name": "query",
                        "description": "The query containing wallet address and a natural language request for analysis containing the wallet address and a request for token or NFT holdings",
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
                    {"name": "response", "description": "Wallet holding details and analysis", "type": "str"},
                    {"name": "data", "description": "The wallet details", "type": "dict"},
                ],
                "external_apis": ["Zerion"],
                "tags": ["EVM Wallet"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Zerion.png",
                "examples": [
                    "What tokens does 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D hold?",
                    "Show me all NFT collections owned by 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                    "Analyze the token portfolio of wallet 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                    "What's the total value of tokens in 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D?",
                    "Which tokens held by 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D have had the most price change in the last 24 hours?",
                ],
            }
        )

        # Zerion API credentials - should be loaded from environment variables in production
        self.zerion_auth_key = "Basic " + os.getenv("ZERION_API_KEY")

    def get_system_prompt(self) -> str:
        return """You are a crypto wallet analyst that provides factual analysis of wallet holdings based on Zerion API data.
        1. Extract the wallet address from the user's query. It must be a valid EVM wallet address. Otherwise, return an error.
        2. Use the appropriate tools to get wallet data
        3. Present the findings in this structured format:
            - Wallet Overview: Total value, number of tokens, number of NFT collections
            - Token Holdings: List of tokens with quantity, value, and 24h change
            - NFT Collections: List of NFT collections with count and floor price
            - Portfolio Analysis: Distribution of assets, major holdings, recent changes
        4. Other comments and insights: only if requested by the user in the query

        Important:
        - Highlight the most valuable holdings
        - Note any significant price changes in the last 24 hours
        - Identify any interesting or rare tokens or NFT collections if present
        - Don't mention any data that is not provided or missing
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_wallet_tokens",
                    "description": "Fetch token holdings of an EVM wallet. The result includes the amount, USD value, 1-day price change, token contract address and the chain of all tokens held by the wallet. Use this tool if you want to know the token portfolio of the wallet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "wallet_address": {
                                "type": "string",
                                "description": "The EVM wallet address to analyze. Must start with 0x and be 42 characters long.",
                            },
                        },
                        "required": ["wallet_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_wallet_nfts",
                    "description": "Fetch NFT collections held by an EVM wallet. The result includes the number of NFTs, the collection name and description of the NFTs. Use this tool if you want to know the NFT portfolio of the wallet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "wallet_address": {
                                "type": "string",
                                "description": "The EVM wallet address to analyze. Must start with 0x and be 42 characters long.",
                            },
                        },
                        "required": ["wallet_address"],
                    },
                },
            },
        ]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_wallet_tokens(self, wallet_address: str) -> Dict:
        """Fetch fungible token holdings from Zerion API"""
        try:
            base_url = f"https://api.zerion.io/v1/wallets/{wallet_address}/positions/"
            params = {
                "filter[positions]": "no_filter",
                "currency": "usd",
                "filter[trash]": "only_non_trash",
                "sort": "value",
            }
            headers = {"accept": "application/json", "authorization": self.zerion_auth_key}

            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Process the response data to extract relevant information
            tokens = []
            total_value = 0

            for item in data.get("data", []):
                attributes = item.get("attributes", {})
                fungible_info = attributes.get("fungible_info", {})

                # Skip non-displayable items
                if not attributes.get("flags", {}).get("displayable", False):
                    continue

                # Get the chain from relationships
                chain = item.get("relationships", {}).get("chain", {}).get("data", {}).get("id", "unknown")

                # Find the correct token address for this chain
                token_address = None
                implementations = fungible_info.get("implementations", [])
                for impl in implementations:
                    if impl.get("chain_id") == chain:
                        token_address = impl.get("address")
                        break

                token_data = {
                    "name": fungible_info.get("name", "Unknown"),
                    "symbol": fungible_info.get("symbol", "Unknown"),
                    "quantity": attributes.get("quantity", {}).get("float", 0),
                    "value": attributes.get("value", 0),
                    "price": attributes.get("price", 0),
                    "change_24h_percent": attributes.get("changes", {}).get("percent_1d", 0)
                    if attributes.get("changes") is not None
                    else 0,
                    "chain": chain,
                    "token_address": token_address,
                }

                # Handle case where value might be None
                token_value = 0
                if token_data["value"] is not None:
                    token_value = token_data["value"]
                    total_value += token_value
                else:
                    token_value = 0
                    # Use price * quantity as fallback or default to 0
                    if token_data["price"] is not None and token_data["quantity"] is not None:
                        token_value = token_data["price"] * token_data["quantity"]
                    total_value += token_value
                    token_data["value"] = token_value

                # Skip tokens with value less than 1
                if token_value < 1:
                    continue
                tokens.append(token_data)

            # Sort tokens by value (descending)
            tokens.sort(key=lambda x: x["value"] if x["value"] is not None else 0, reverse=True)

            return {"total_value": total_value, "token_count": len(tokens), "tokens": tokens}

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching wallet tokens: {e}")
            return {"error": f"Failed to fetch wallet tokens: {str(e)} for wallet address {wallet_address}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)} for wallet address {wallet_address}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_wallet_nfts(self, wallet_address: str) -> Dict:
        """Fetch NFT collections from Zerion API"""
        try:
            base_url = f"https://api.zerion.io/v1/wallets/{wallet_address}/nft-collections/"
            params = {"currency": "usd"}
            headers = {"accept": "application/json", "authorization": self.zerion_auth_key}

            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Process the response data to extract relevant information
            collections = []
            total_floor_price = 0
            total_nfts = 0

            for item in data.get("data", []):
                attributes = item.get("attributes", {})
                collection_info = attributes.get("collection_info", {})

                nfts_count = int(attributes.get("nfts_count", "0"))
                floor_price = attributes.get("total_floor_price", 0)

                collection_data = {
                    "name": collection_info.get("name", "Unknown Collection"),
                    "description": collection_info.get("description", ""),
                    "nfts_count": nfts_count,
                    "floor_price": floor_price,
                    "chains": [
                        chain["id"] for chain in item.get("relationships", {}).get("chains", {}).get("data", [])
                    ],
                }

                collections.append(collection_data)
                total_floor_price += floor_price
                total_nfts += nfts_count

            # Sort collections by floor price (descending)
            collections.sort(key=lambda x: x["floor_price"], reverse=True)

            return {
                "total_collections": len(collections),
                "total_nfts": total_nfts,
                "total_floor_price": total_floor_price,
                "collections": collections,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching wallet NFTs: {e}")
            return {"error": f"Failed to fetch wallet NFTs: {str(e)} for wallet address {wallet_address}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)} for wallet address {wallet_address}"}

    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        if tool_name not in ["fetch_wallet_tokens", "fetch_wallet_nfts"]:
            return {"error": f"Unsupported tool '{tool_name}'"}

        wallet_address = function_args.get("wallet_address")

        if not wallet_address:
            return {"error": "Missing 'wallet_address' in tool_arguments"}

        logger.info(f"Using {tool_name} for {wallet_address}")

        thinking_msg = f"Analyzing wallet {wallet_address}..."
        self.push_update(function_args, thinking_msg)

        if tool_name == "fetch_wallet_tokens":
            result = await self.fetch_wallet_tokens(wallet_address)
        else:  # fetch_wallet_nfts
            result = await self.fetch_wallet_nfts(wallet_address)

        errors = self._handle_error(result)
        if errors:
            return errors
        return result
