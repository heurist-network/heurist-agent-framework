import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.context_agent import ContextAgent

logger = logging.getLogger(__name__)
load_dotenv()


class ZerionWalletAnalysisAgent(ContextAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("ZERION_API_KEY")
        if not self.api_key:
            raise ValueError("ZERION_API_KEY environment variable is required")

        self.base_url = "https://api.zerion.io/v1"
        self.headers = {"accept": "application/json", "authorization": f"Basic {self.api_key}"}

        self.metadata.update(
            {
                "name": "Zerion Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch and analyze the token and NFT holdings of a crypto wallet (must be EVM chain)",
                "external_apis": ["Zerion"],
                "tags": ["EVM Wallet", "x402"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Zerion.png",
                "examples": [
                    "What tokens does 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D hold?",
                    "Show me all NFT collections owned by 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                    "Analyze the token portfolio of wallet 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                    "What's the total value of tokens in 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D?",
                    "Which tokens held by 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D have had the most price change in the last 24 hours?",
                ],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a crypto wallet analyst that provides factual analysis of wallet holdings based on Zerion API data. Use the appropriate tools to get wallet data.

        Important:
        - NEVER make up data that is not returned from the tool
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
                    "description": "Fetch token holdings of an EVM wallet. The result includes the amount, USD value, 1-day price change, token contract address and the chain of all tokens held by the wallet. Use this tool if you want to know the token portfolio of the wallet or understand a user's onchain behavior.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "wallet_address": {
                                "type": "string",
                                "description": "The EVM wallet address (starting with 0x and 42-character long) to analyze. You can also use 'SELF' for wallet_address to use the user's own wallet address.",
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
                                "description": "The EVM wallet address (starting with 0x and 42-character long) to analyze. You can also use 'SELF' for wallet_address to use the user's own wallet address.",
                            },
                        },
                        "required": ["wallet_address"],
                    },
                },
            },
        ]

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_wallet_tokens(self, wallet_address: str) -> Dict:
        """Fetch fungible token holdings from Zerion API"""
        try:
            url = f"{self.base_url}/wallets/{wallet_address}/positions/"
            params = {
                "filter[positions]": "no_filter",
                "currency": "usd",
                "filter[trash]": "only_non_trash",
                "sort": "value",
            }

            data = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in data:
                return {"error": data["error"]}

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

        except Exception as e:
            logger.error(f"Error fetching wallet tokens: {e}")
            return {"error": f"Failed to fetch wallet tokens: {str(e)} for wallet address {wallet_address}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_wallet_nfts(self, wallet_address: str) -> Dict:
        """Fetch NFT collections from Zerion API"""
        try:
            url = f"{self.base_url}/wallets/{wallet_address}/nft-collections/"
            params = {"currency": "usd"}

            data = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in data:
                return {"error": data["error"]}

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

        except Exception as e:
            logger.error(f"Error fetching wallet NFTs: {e}")
            return {"error": f"Failed to fetch wallet NFTs: {str(e)} for wallet address {wallet_address}"}

    def _is_valid_wallet_address(self, wallet_address: str) -> bool:
        return wallet_address.startswith("0x") and len(wallet_address) == 42

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name not in ["fetch_wallet_tokens", "fetch_wallet_nfts"]:
            return {"error": f"Unsupported tool '{tool_name}'"}

        if function_args.get("wallet_address"):
            wallet_address = function_args.get("wallet_address")

            if wallet_address == "SELF":
                user_id = self._extract_user_id(session_context.get("api_key"))
                if self._is_valid_wallet_address(user_id):
                    wallet_address = user_id
                    await self.update_user_context({"wallet_address": wallet_address}, user_id)
                else:
                    return {"error": "Invalid wallet address for SELF"}

        if not wallet_address:
            return {"error": "Missing 'wallet_address' in tool_arguments"}

        logger.info(f"Using {tool_name} for {wallet_address}")

        thinking_msg = f"Analyzing wallet {wallet_address}..."
        self.push_update(function_args, thinking_msg)

        if tool_name == "fetch_wallet_tokens":
            result = await self.fetch_wallet_tokens(wallet_address)
        else:  # fetch_wallet_nfts
            result = await self.fetch_wallet_nfts(wallet_address)

        if "error" in result:
            return {"error": result["error"]}

        return result
