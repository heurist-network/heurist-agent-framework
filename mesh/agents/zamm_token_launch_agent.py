import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import time

from web3 import Web3

from mesh.eip7702_agent import CallData, EIP7702Agent, SupportedChain

logger = logging.getLogger(__name__)


class ZammTokenLaunchAgent(EIP7702Agent):
    """
    Agent that helps users launch new tokens and create liquidity pools using ZAMM protocol with EIP7702 delegation.

    This agent handles:
    - Token creation with custom metadata URI
    - Creator supply allocation with unlock timing
    - Tranche configuration for token distribution
    - Pricing configuration for token sales
    """

    # ZAMM contract address on Ethereum mainnet
    # TODO: replace with new contract address
    ZAMM_CONTRACT_ADDRESS = "0x000000000077A9C733B9ac3781fB5A1BC7701FBc"

    # ABI for the launch function
    ZAMM_ABI = [
        {
            "inputs": [
                {"name": "creatorSupply", "type": "uint96"},
                {"name": "creatorUnlock", "type": "uint256"},
                {"name": "uri", "type": "string"},
                {"name": "trancheCoins", "type": "uint96[]"},
                {"name": "tranchePrice", "type": "uint96[]"},
            ],
            "name": "launch",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ]

    def __init__(self):
        super().__init__(default_chain=SupportedChain.ETHEREUM_MAINNET)

        self.metadata.update(
            {
                "name": "ZAMM Token Launch Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Agent that helps users launch new tokens using ZAMM protocol with EIP7702 delegation.",
                "tags": ["EIP7702", "Token Launch", "ZAMM", "DeFi"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/ZammTokenLaunch.png",
                "examples": [
                    "Launch a token with metadata URI and default settings",
                    "Create a token with custom creator supply and unlock schedule",
                    "Launch token with custom tranche configuration",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a ZAMM token launch assistant that helps users create new tokens on Ethereum blockchain.

        Key functions:
        - Launch new tokens with custom metadata URIs
        - Configure creator supply with unlock timing (default: 1 week + 12 hours)
        - Set up token distribution tranches
        - Configure pricing for token sales

        When handling token launches:
        - Always validate that the metadata URI is provided
        - Use default values for optional parameters when not specified
        - Confirm token details before execution
        - Explain the tokenomics and unlock schedule

        Default values:
        - Creator Supply: 100,000,000 tokens (100000000000000000000000000 wei)
        - Creator Unlock: 1 week + 12 hours from launch time
        - Tranche Coins: 150,000 tokens (150000000000000000000000 wei)
        - Tranche Price: 0.001 ETH (1000000000000000 wei)

        Supported chains: Ethereum Mainnet (default)
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "launch",
                    "description": "Launch a new token using ZAMM protocol",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "uri": {
                                "type": "string",
                                "description": "The metadata URI for the token (required)",
                            },
                            "creator_supply": {
                                "type": "string",
                                "description": "The amount of tokens for the creator in wei (default: 100000000000000000000000000)",
                                "default": "100000000000000000000000000",
                            },
                            "creator_unlock_days": {
                                "type": "number",
                                "description": "Number of days from now when creator tokens unlock (default: 7.5 days = 1 week + 12 hours)",
                                "default": 7.5,
                            },
                            "tranche_coins": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of token amounts for each tranche in wei (default: ['150000000000000000000000'])",
                                "default": ["150000000000000000000000"],
                            },
                            "tranche_price": {
                                "type": "array", 
                                "items": {"type": "string"},
                                "description": "Array of prices for each tranche in wei (default: ['1000000000000000'])",
                                "default": ["1000000000000000"],
                            },
                            "chain_id": {
                                "type": "integer",
                                "description": "The blockchain chain ID (1 for mainnet)",
                                "default": 1,
                            },
                        },
                        "required": ["uri"],
                    },
                },
            },
        ]

    def get_supported_functions(self) -> List[str]:
        """Return list of supported function names"""
        return ["launch"]

    async def prepare_call_data(
        self, function_name: str, function_args: dict, chain_id: int, user_context: Dict[str, Any]
    ) -> List[CallData]:
        """
        Prepare call data for ZAMM token launch.

        Args:
            function_name: Name of the function being executed
            function_args: Contains token launch parameters
            chain_id: Target blockchain chain ID
            user_context: User's stored context

        Returns:
            List containing a single CallData object for the token launch
        """
        if function_name == "launch":
            logger.info(f"Preparing call data for token launch: {function_name}")
            logger.info(f"Preparing call data for token launch: {function_args}")
            logger.info(f"User context: {user_context}")
            logger.info(f"Chain ID: {chain_id}")
            return await self._prepare_launch_call_data(function_args, chain_id, user_context)
        else:
            raise ValueError(f"Unsupported function: {function_name}")

    async def _prepare_launch_call_data(
        self, function_args: dict, chain_id: int, user_context: Dict[str, Any]
    ) -> List[CallData]:
        """
        Prepare call data for ZAMM token launch.
        """
        try:
            uri = function_args.get("uri")
            creator_supply = function_args.get("creator_supply", "100000000000000000000000000")
            creator_unlock_days = function_args.get("creator_unlock_days", 7.5)
            tranche_coins = function_args.get("tranche_coins", ["150000000000000000000000"])
            tranche_price = function_args.get("tranche_price", ["1000000000000000"])

            if not uri:
                logger.error("Missing required parameter: uri")
                raise ValueError("URI is required for token launch")

            # Get Web3 instance for the target chain
            w3 = self._get_web3_instance(chain_id)

            # Convert creator_supply to uint96
            try:
                creator_supply_value = int(creator_supply)
                if creator_supply_value <= 0:
                    raise ValueError("Creator supply must be positive")
            except ValueError as e:
                logger.error(f"Invalid creator supply: {e}")
                raise ValueError("Invalid creator supply value")

            # Calculate creator unlock timestamp (current time + creator_unlock_days)
            current_timestamp = int(time.time())
            unlock_seconds = int(creator_unlock_days * 24 * 60 * 60)  # Convert days to seconds
            creator_unlock = current_timestamp + unlock_seconds

            # Convert tranche arrays
            try:
                tranche_coins_values = [int(coin) for coin in tranche_coins]
                tranche_price_values = [int(price) for price in tranche_price]
                
                if len(tranche_coins_values) != len(tranche_price_values):
                    raise ValueError("Tranche coins and prices arrays must have the same length")
                    
                if any(coin <= 0 for coin in tranche_coins_values):
                    raise ValueError("All tranche coin values must be positive")
                    
                if any(price <= 0 for price in tranche_price_values):
                    raise ValueError("All tranche price values must be positive")
                    
            except ValueError as e:
                logger.error(f"Invalid tranche values: {e}")
                raise ValueError(f"Invalid tranche values: {str(e)}")

            # Create ZAMM contract instance
            zamm_contract = w3.eth.contract(address=self.ZAMM_CONTRACT_ADDRESS, abi=self.ZAMM_ABI)

            # Encode the launch function call
            try:
                launch_data = zamm_contract.encode_abi(
                    "launch", 
                    args=[creator_supply_value, creator_unlock, uri, tranche_coins_values, tranche_price_values]
                )
            except Exception as e:
                logger.error(f"Failed to encode launch function: {e}")
                raise ValueError("Failed to encode token launch function")

            call_data = CallData(target=self.ZAMM_CONTRACT_ADDRESS, value=0, data=launch_data)

            unlock_date = datetime.fromtimestamp(creator_unlock).strftime('%Y-%m-%d %H:%M:%S')
            logger.info(
                f"Prepared ZAMM token launch with URI: {uri}, creator supply: {creator_supply}, unlock: {unlock_date}"
            )
            return [call_data]

        except Exception as e:
            logger.error(f"Error preparing call data for token launch: {e}")
            # Re-raise validation errors for user-friendly handling
            raise e

    async def launch(
        self,
        user_id: str,
        uri: str,
        creator_supply: Optional[str] = "100000000000000000000000000",
        creator_unlock_days: Optional[float] = 7.5,
        tranche_coins: Optional[List[str]] = None,
        tranche_price: Optional[List[str]] = None,
        chain_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Execute ZAMM token launch for a user.

        Args:
            user_id: The user launching the token
            uri: Token metadata URI
            creator_supply: Amount of tokens for creator (optional)
            creator_unlock_days: Days until creator tokens unlock (optional)
            tranche_coins: Array of token amounts for tranches (optional)
            tranche_price: Array of prices for tranches (optional)  
            chain_id: Target chain ID (optional, uses default if not provided)

        Returns:
            Dictionary with launch result or error
        """
        try:
            chain_id = 1  # Ethereum Mainnet

            # Set defaults for optional parameters
            if tranche_coins is None:
                tranche_coins = ["150000000000000000000000"]
            if tranche_price is None:
                tranche_price = ["1000000000000000"]

            # Prepare function arguments
            function_args = {
                "uri": uri,
                "creator_supply": creator_supply,
                "creator_unlock_days": creator_unlock_days,
                "tranche_coins": tranche_coins,
                "tranche_price": tranche_price,
            }

            result = await self.execute_onchain_action(
                user_id=user_id, function_name="launch", function_args=function_args, chain_id=chain_id
            )

            return result

        except Exception as e:
            logger.error(f"Error in launch: {e}")
            return {"error": f"Token launch failed: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        user_id = self._extract_user_id(session_context.get("api_key") if session_context else None)

        if tool_name == "launch":
            uri = function_args.get("uri")
            creator_supply = function_args.get("creator_supply", "100000000000000000000000000")
            creator_unlock_days = function_args.get("creator_unlock_days", 7.5)
            tranche_coins = function_args.get("tranche_coins")
            tranche_price = function_args.get("tranche_price")
            chain_id = function_args.get("chain_id")

            return await self.launch(
                user_id=user_id,
                uri=uri,
                creator_supply=creator_supply,
                creator_unlock_days=creator_unlock_days,
                tranche_coins=tranche_coins,
                tranche_price=tranche_price,
                chain_id=chain_id,
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"}
