import json
import logging
from typing import Any, Dict, List, Optional

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class ZoraAgent(MeshAgent):
    def __init__(self):
        super().__init__()

        self.base_url = "https://api-sdk.zora.engineering"
        self.headers = {"accept": "application/json", "User-Agent": "ZoraAgent/1.0.0"}

        self.metadata.update(
            {
                "name": "Zora Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides access to Zora protocol data including trending collections, coin holders, coin information, community comments, and user profiles",
                "external_apis": ["Zora"],
                "tags": ["Social"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Zora.png",
                "examples": [
                    "Show me the top gainers on Zora",
                    "Who are the most valuable creators?",
                    "Get coin holders for address 0xd769d56f479e9e72a77bb1523e866a33098feec5 on Base",
                    "Show me comments for this Zora coin",
                    "What's the coin info for collection 0xd769d56f479e9e72a77bb1523e866a33098feec5?",
                    "Show me the top volume collections in the last 24 hours",
                    "Get profile information for user balraj",
                    "Show me coins created by kazonomics",
                    "What coins does kazonomics hold?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that can access Zora protocol data to provide information about NFT collections, coins, holders, community activity, and user profiles.

        You can help users with:
        - Exploring trending collections (top gainers, most valuable creators, top volume, featured)
        - Getting coin holder information for specific addresses
        - Retrieving detailed coin/collection information
        - Showing community comments on coins
        - Getting user profile information (handle, display name, bio)
        - Retrieving coins created by users
        - Showing coin balances held by users

        When users ask about Zora data without specifying counts, default to 10 items.
        For chain IDs, Base = 8453 is the most common, but confirm with users if unclear.

        If the user's query is out of your scope, return a brief error message.
        Format your response in clean text without markdown or special formatting.
        Present data in a clear, organized manner focusing on the most relevant information."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "explore_collections",
                    "description": "Explore Zora collections by different metrics like top gainers, most valuable creators, top volume, or featured collections",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "list_type": {
                                "type": "string",
                                "description": "Type of collection list to retrieve",
                                "enum": [
                                    "TOP_GAINERS",
                                    "MOST_VALUABLE_CREATORS",
                                    "TOP_VOLUME_24H",
                                    "LAST_TRADED",
                                    "FEATURED",
                                ],
                                "default": "TOP_GAINERS",
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of collections to retrieve",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 100,
                            },
                        },
                        "required": ["list_type"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_coin_holders",
                    "description": "Get the list of holders for a specific Zora coin/collection",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain_id": {
                                "type": "integer",
                                "description": "Blockchain chain ID (e.g., 8453 for Base)",
                                "default": 8453,
                            },
                            "address": {
                                "type": "string",
                                "description": "Collection/coin contract address (e.g., 0xd769d56f479e9e72a77bb1523e866a33098feec5)",
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of holders to retrieve",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 100,
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_coin_info",
                    "description": "Get detailed information about a specific Zora coin/collection",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain_id": {
                                "type": "integer",
                                "description": "Blockchain chain ID (e.g., 8453 for Base)",
                                "default": 8453,
                            },
                            "collection_address": {
                                "type": "string",
                                "description": "Collection contract address (e.g., 0xd769d56f479e9e72a77bb1523e866a33098feec5)",
                            },
                        },
                        "required": ["collection_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_coin_comments",
                    "description": "Get community comments for a specific Zora coin/collection",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Collection/coin contract address (e.g., 0xd769d56f479e9e72a77bb1523e866a33098feec5)",
                            },
                            "chain": {
                                "type": "integer",
                                "description": "Blockchain chain ID (e.g., 8453 for Base)",
                                "default": 8453,
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of comments to retrieve",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50,
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_profile",
                    "description": "Get detailed information about a user's profile including handle, display name, and bio",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "identifier": {
                                "type": "string",
                                "description": "User identifier (username/handle, e.g., 'balraj' or 'kazonomics')",
                            },
                        },
                        "required": ["identifier"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_profile_coins",
                    "description": "Get coins created by a specific user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "identifier": {
                                "type": "string",
                                "description": "User identifier (username/handle, e.g., 'balraj' or 'kazonomics')",
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of coins to retrieve",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                            },
                            "chain_ids": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Array of chain IDs to filter by (e.g., [8453] for Base)",
                                "default": [8453],
                            },
                        },
                        "required": ["identifier"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_profile_balances",
                    "description": "Get all coin balances held by a specific user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "identifier": {
                                "type": "string",
                                "description": "User identifier (username/handle, e.g., 'balraj' or 'kazonomics')",
                            },
                            "count": {
                                "type": "integer",
                                "description": "Number of balances to retrieve",
                                "default": 30,
                                "minimum": 1,
                                "maximum": 100,
                            },
                            "sort_option": {
                                "type": "string",
                                "description": "Sort option for the results",
                                "enum": ["BALANCE", "MARKET_CAP", "USD_VALUE", "PRICE_CHANGE"],
                                "default": "USD_VALUE",
                            },
                            "exclude_hidden": {
                                "type": "boolean",
                                "description": "Whether to exclude hidden coins",
                                "default": True,
                            },
                            "chain_ids": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Array of chain IDs to filter by (e.g., [8453] for Base)",
                                "default": [8453],
                            },
                        },
                        "required": ["identifier"],
                    },
                },
            },
        ]

    def _preprocess(self, data: Any) -> Any:
        """
        Recursively remove mediaContent fields from response data.

        Args:
            data: The data to clean (can be dict, list, or primitive)

        Returns:
            Cleaned data with mediaContent removed
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                if key == "mediaContent":
                    continue
                else:
                    cleaned[key] = self._preprocess(value)
            return cleaned
        elif isinstance(data, list):
            return [self._preprocess(item) for item in data]
        else:
            return data

    # ------------------------------------------------------------------------
    #                      ZORA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def explore_collections(self, list_type: str = "TOP_GAINERS", count: int = 10) -> Dict[str, Any]:
        """
        Explore Zora collections by different metrics.

        Args:
            list_type: Type of list (TOP_GAINERS, MOST_VALUABLE_CREATORS, etc.)
            count: Number of collections to retrieve

        Returns:
            Dict containing collections data or error
        """
        try:
            url = f"{self.base_url}/explore"
            params = {"listType": list_type, "count": min(count, 100)}
            logger.info(f"Exploring Zora collections: {list_type} (count={count})")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            cleaned_response = self._preprocess(response)

            return {
                "list_type": list_type,
                "count": len(cleaned_response) if isinstance(cleaned_response, list) else 0,
                "collections": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error exploring collections: {e}")
            return {"error": f"Failed to explore collections: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=600)
    @with_retry(max_retries=3)
    async def get_coin_holders(self, address: str, chain_id: int = 8453, count: int = 10) -> Dict[str, Any]:
        """
        Get holders for a specific Zora coin/collection.

        Args:
            address: Collection contract address
            chain_id: Blockchain chain ID
            count: Number of holders to retrieve

        Returns:
            Dict containing holders data or error
        """
        try:
            address = address.lower() if address.startswith("0x") else f"0x{address.lower()}"
            url = f"{self.base_url}/coinHolders"
            params = {"chainId": chain_id, "address": address, "count": min(count, 100)}
            logger.info(f"Getting coin holders for {address} on chain {chain_id}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            # Remove mediaContent from response
            cleaned_response = self._preprocess(response)

            return {
                "address": address,
                "chain_id": chain_id,
                "holder_count": len(cleaned_response) if isinstance(cleaned_response, list) else 0,
                "holders": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error getting coin holders: {e}")
            return {"error": f"Failed to get coin holders: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=600)
    @with_retry(max_retries=3)
    async def get_coin_info(self, collection_address: str, chain_id: int = 8453) -> Dict[str, Any]:
        """
        Get detailed information about a Zora coin/collection.

        Args:
            collection_address: Collection contract address
            chain_id: Blockchain chain ID

        Returns:
            Dict containing coin information or error
        """
        try:
            collection_address = (
                collection_address.lower() if collection_address.startswith("0x") else f"0x{collection_address.lower()}"
            )
            coins_param = json.dumps({"chainId": chain_id, "collectionAddress": collection_address})
            url = f"{self.base_url}/coins"
            params = {"coins": coins_param}
            logger.info(f"Getting coin info for {collection_address} on chain {chain_id}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            # Remove mediaContent from response
            cleaned_response = self._preprocess(response)

            return {"collection_address": collection_address, "chain_id": chain_id, "coin_data": cleaned_response}

        except Exception as e:
            logger.error(f"Error getting coin info: {e}")
            return {"error": f"Failed to get coin info: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_coin_comments(self, address: str, chain: int = 8453, count: int = 10) -> Dict[str, Any]:
        """
        Get community comments for a Zora coin/collection.

        Args:
            address: Collection contract address
            chain: Blockchain chain ID
            count: Number of comments to retrieve

        Returns:
            Dict containing comments data or error
        """
        try:
            address = address.lower() if address.startswith("0x") else f"0x{address.lower()}"
            url = f"{self.base_url}/coinComments"
            params = {"address": address, "chain": chain, "count": min(count, 50)}
            logger.info(f"Getting coin comments for {address} on chain {chain}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            cleaned_response = self._preprocess(response)

            return {
                "address": address,
                "chain": chain,
                "comment_count": len(cleaned_response) if isinstance(cleaned_response, list) else 0,
                "comments": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error getting coin comments: {e}")
            return {"error": f"Failed to get coin comments: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=600)
    @with_retry(max_retries=3)
    async def get_profile(self, identifier: str) -> Dict[str, Any]:
        """
        Get detailed information about a user's profile.

        Args:
            identifier: User identifier (username/handle)

        Returns:
            Dict containing profile data (excluding image URL and mediaContent) or error
        """
        try:
            url = f"{self.base_url}/profile"
            params = {"identifier": identifier}
            logger.info(f"Getting profile for {identifier}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            cleaned_response = self._preprocess(response)

            return {
                "identifier": identifier,
                "profile_data": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error getting profile: {e}")
            return {"error": f"Failed to get profile: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=600)
    @with_retry(max_retries=3)
    async def get_profile_coins(self, identifier: str, count: int = 30, chain_ids: List[int] = None) -> Dict[str, Any]:
        """
        Get coins created by a specific user.

        Args:
            identifier: User identifier (username/handle)
            count: Number of coins to retrieve
            chain_ids: List of chain IDs to filter by

        Returns:
            Dict containing user's created coins or error
        """
        try:
            if chain_ids is None:
                chain_ids = [8453]

            url = f"{self.base_url}/profileCoins"
            params = {
                "identifier": identifier,
                "count": min(count, 100),
                "chainIds": ",".join(str(id) for id in chain_ids),
            }
            logger.info(f"Getting coins created by {identifier}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            cleaned_response = self._preprocess(response)
            return {
                "identifier": identifier,
                "coin_count": len(cleaned_response) if isinstance(cleaned_response, list) else 0,
                "coins": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error getting profile coins: {e}")
            return {"error": f"Failed to get profile coins: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=600)
    @with_retry(max_retries=3)
    async def get_profile_balances(
        self,
        identifier: str,
        count: int = 30,
        sort_option: str = "USD_VALUE",
        exclude_hidden: bool = True,
        chain_ids: List[int] = None,
    ) -> Dict[str, Any]:
        """
        Get all coin balances held by a specific user.

        Args:
            identifier: User identifier (username/handle)
            count: Number of balances to retrieve
            sort_option: Sort option (BALANCE, MARKET_CAP, USD_VALUE, PRICE_CHANGE)
            exclude_hidden: Whether to exclude hidden coins
            chain_ids: List of chain IDs to filter by

        Returns:
            Dict containing user's coin balances or error
        """
        try:
            if chain_ids is None:
                chain_ids = [8453]

            url = f"{self.base_url}/profileBalances"
            params = {
                "identifier": identifier,
                "count": min(count, 100),
                "sortOption": sort_option,
                "excludeHidden": str(exclude_hidden).lower(),
                "chainIds": ",".join(str(id) for id in chain_ids),
            }
            logger.info(f"Getting coin balances for {identifier}")
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in response:
                return {"error": response["error"]}

            cleaned_response = self._preprocess(response)
            return {
                "identifier": identifier,
                "balance_count": len(cleaned_response) if isinstance(cleaned_response, list) else 0,
                "sort_option": sort_option,
                "balances": cleaned_response,
            }

        except Exception as e:
            logger.error(f"Error getting profile balances: {e}")
            return {"error": f"Failed to get profile balances: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle Zora tool calls."""

        if tool_name == "explore_collections":
            list_type = function_args.get("list_type", "TOP_GAINERS")
            count = function_args.get("count", 10)
            result = await self.explore_collections(list_type=list_type, count=count)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_coin_holders":
            address = function_args.get("address")
            chain_id = function_args.get("chain_id", 8453)
            count = function_args.get("count", 10)
            if not address:
                return {"error": "Address parameter is required"}
            result = await self.get_coin_holders(address=address, chain_id=chain_id, count=count)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_coin_info":
            collection_address = function_args.get("collection_address")
            chain_id = function_args.get("chain_id", 8453)
            if not collection_address:
                return {"error": "Collection address parameter is required"}
            result = await self.get_coin_info(collection_address=collection_address, chain_id=chain_id)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_coin_comments":
            address = function_args.get("address")
            chain = function_args.get("chain", 8453)
            count = function_args.get("count", 10)
            if not address:
                return {"error": "Address parameter is required"}
            result = await self.get_coin_comments(address=address, chain=chain, count=count)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_profile":
            identifier = function_args.get("identifier")
            if not identifier:
                return {"error": "Identifier parameter is required"}
            result = await self.get_profile(identifier=identifier)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_profile_coins":
            identifier = function_args.get("identifier")
            count = function_args.get("count", 10)
            chain_ids = function_args.get("chain_ids", [8453])
            if not identifier:
                return {"error": "Identifier parameter is required"}
            result = await self.get_profile_coins(identifier=identifier, count=count, chain_ids=chain_ids)
            if errors := self._handle_error(result):
                return errors
            return result

        elif tool_name == "get_profile_balances":
            identifier = function_args.get("identifier")
            count = function_args.get("count", 10)
            sort_option = function_args.get("sort_option", "USD_VALUE")
            exclude_hidden = function_args.get("exclude_hidden", True)
            chain_ids = function_args.get("chain_ids", [8453])
            if not identifier:
                return {"error": "Identifier parameter is required"}
            result = await self.get_profile_balances(
                identifier=identifier,
                count=count,
                sort_option=sort_option,
                exclude_hidden=exclude_hidden,
                chain_ids=chain_ids,
            )
            if errors := self._handle_error(result):
                return errors
            return result

        else:
            return {"error": f"Unsupported tool: {tool_name}"}
