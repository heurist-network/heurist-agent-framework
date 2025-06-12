import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from web3 import Web3

from mesh.eip7702_agent import CallData, EIP7702Agent, SupportedChain

logger = logging.getLogger(__name__)


class ZammTokenLaunchAgent(EIP7702Agent):
    """
    Agent that helps users launch new tokens and create liquidity pools using ZAMM protocol with EIP7702 delegation.

    This agent handles:
    - Token creation with custom name, symbol, and metadata
    - Liquidity pool creation
    - Owner and pool supply allocation
    - Swap fee configuration
    """

    # ZAMM contract address on Ethereum mainnet
    ZAMM_CONTRACT_ADDRESS = "0x00000000007762D8DCADEddD5Aa5E9a5e2B7c6f5"

    # ABI for the make function
    ZAMM_ABI = [
        {
            "inputs": [
                {"name": "name", "type": "string"},
                {"name": "symbol", "type": "string"},
                {"name": "tokenURI", "type": "string"},
                {"name": "poolSupply", "type": "uint256"},
                {"name": "ownerSupply", "type": "uint256"},
                {"name": "swapFee", "type": "uint96"},
                {"name": "owner", "type": "address"}
            ],
            "name": "make",
            "outputs": [
                {"name": "coinId", "type": "uint256"},
                {"name": "amount0", "type": "uint256"},
                {"name": "amount1", "type": "uint256"},
                {"name": "liquidity", "type": "uint256"}
            ],
            "stateMutability": "payable",
            "type": "function"
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
                "description": "Agent that helps users launch new tokens and create liquidity pools using ZAMM protocol with EIP7702 delegation.",
                "tags": ["EIP7702", "Token Launch", "Liquidity", "ZAMM", "DeFi"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/ZammTokenLaunch.png",
                "examples": [
                    "Launch a token called 'MyToken' with symbol 'MTK' and create a liquidity pool with 1000000 tokens and 0.3% swap fee",
                    "Create a new token 'CommunityToken' (COMM) with metadata URI and allocate 500000 tokens to pool, 100000 to owner",
                    "Launch token with custom swap fee and owner address",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a ZAMM token launch assistant that helps users create new tokens and liquidity pools on Ethereum blockchain.

        Key functions:
        - Launch new ERC20 tokens with custom name, symbol, and metadata
        - Create liquidity pools with specified token and ETH amounts
        - Configure swap fees for the liquidity pool
        - Allocate token supply between pool and owner
        - Set token ownership

        When handling token launches:
        - Always validate that all required parameters are provided
        - Confirm token details (name, symbol, supply allocation) before execution
        - Ensure sufficient ETH is provided for liquidity pool creation
        - Validate owner addresses are properly formatted
        - Provide clear confirmation of launch details before execution
        - Explain the tokenomics and liquidity pool setup

        Supported chains: Ethereum Mainnet (default)
        Contract Address: 0x00000000007762D8DCADEddD5Aa5E9a5e2B7c6f5
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "launch_zamm_token",
                    "description": "Launch a new token and create a liquidity pool using ZAMM protocol",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the token to create (e.g., 'My Token')",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "The symbol of the token to create (e.g., 'MTK')",
                            },
                            "token_uri": {
                                "type": "string",
                                "description": "The metadata URI for the token (can be empty string if no metadata)",
                                "default": "",
                            },
                            "pool_supply": {
                                "type": "string",
                                "description": "The amount of tokens to allocate to the liquidity pool (in token units, e.g., '1000000')",
                            },
                            "owner_supply": {
                                "type": "string",
                                "description": "The amount of tokens to allocate to the owner (in token units, e.g., '100000')",
                                "default": "0",
                            },
                            "swap_fee": {
                                "type": "string",
                                "description": "The swap fee for the pool in basis points (e.g., '300' for 0.3%, '500' for 0.5%)",
                                "default": "300",
                            },
                            "owner": {
                                "type": "string",
                                "description": "The address that will own the token (cannot be zero address)",
                            },
                            "eth_amount": {
                                "type": "string",
                                "description": "The amount of ETH to provide for liquidity (in ETH units, e.g., '1.0')",
                            },
                            "chain_id": {
                                "type": "integer",
                                "description": "The blockchain chain ID (1 for mainnet)",
                                "default": 1,
                            },
                        },
                        "required": ["name", "symbol", "pool_supply", "eth_amount"],
                    },
                },
            },
        ]

    def get_supported_functions(self) -> List[str]:
        """Return list of supported function names"""
        return ["launch_zamm_token"]

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
        if function_name == "launch_zamm_token":
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
            name = function_args.get("name")
            symbol = function_args.get("symbol")
            token_uri = function_args.get("token_uri", "")
            pool_supply = function_args.get("pool_supply")
            owner_supply = function_args.get("owner_supply", "0")
            swap_fee = function_args.get("swap_fee", "300")
            
            # Use user_id as default owner (user_id is the user's wallet address)
            # This will be set later in execute_onchain_action by getting the user_id
            owner = function_args.get("owner")
            eth_amount = function_args.get("eth_amount")

            if not all([name, symbol, pool_supply, eth_amount]):
                logger.error("Missing required parameters for token launch")
                raise ValueError("Missing required parameters: name, symbol, pool_supply, or eth_amount")
                
            if not owner:
                logger.error("Owner address is required and cannot be zero address")
                raise ValueError("Owner address is required for token launch")

            # Get Web3 instance for the target chain
            w3 = self._get_web3_instance(chain_id)

            # Validate and convert owner address to checksum format
            try:
                owner = Web3.to_checksum_address(owner)
            except ValueError as e:
                logger.error(f"Invalid owner address format: {e}")
                raise ValueError(
                    "Invalid owner address format. Please ensure address starts with '0x' and is 42 characters long."
                )

            # Convert amounts to wei
            try:
                pool_supply_wei = int(pool_supply) * (10**18)  # Assuming 18 decimals
                owner_supply_wei = int(owner_supply) * (10**18)
                swap_fee_value = int(swap_fee)
                eth_amount_wei = int(float(eth_amount) * (10**18))
            except ValueError as e:
                logger.error(f"Invalid numeric value: {e}")
                raise ValueError("Invalid numeric values. Please ensure all amounts are valid numbers.")

            if pool_supply_wei <= 0:
                logger.error(f"Pool supply must be positive, got: {pool_supply}")
                raise ValueError("Pool supply must be positive")

            if eth_amount_wei <= 0:
                logger.error(f"ETH amount must be positive, got: {eth_amount}")
                raise ValueError("ETH amount must be positive")

            # Create ZAMM contract instance
            zamm_contract = w3.eth.contract(address=self.ZAMM_CONTRACT_ADDRESS, abi=self.ZAMM_ABI)

            # Encode the make function call
            try:
                make_data = zamm_contract.encode_abi(
                    "make", 
                    args=[name, symbol, token_uri, pool_supply_wei, owner_supply_wei, swap_fee_value, owner]
                )
            except Exception as e:
                logger.error(f"Failed to encode make function: {e}")
                raise ValueError("Failed to encode token launch function")

            call_data = CallData(target=self.ZAMM_CONTRACT_ADDRESS, value=eth_amount_wei, data=make_data)

            logger.info(f"Prepared ZAMM token launch: {name} ({symbol}) with {pool_supply} tokens in pool and {eth_amount} ETH")
            return [call_data]

        except Exception as e:
            logger.error(f"Error preparing call data for token launch: {e}")
            # Re-raise validation errors for user-friendly handling
            raise e
        
    # TODO: should owner required to be user_id?
    async def launch_zamm_token(
        self, 
        user_id: str, 
        name: str, 
        symbol: str, 
        pool_supply: str, 
        eth_amount: str,
        token_uri: Optional[str] = "",
        owner_supply: Optional[str] = "0",
        swap_fee: Optional[str] = "300",
        owner: Optional[str] = None,
        chain_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute ZAMM token launch for a user.

        Args:
            user_id: The user launching the token
            name: Token name
            symbol: Token symbol
            pool_supply: Amount of tokens for the pool
            eth_amount: Amount of ETH for liquidity
            token_uri: Token metadata URI (optional)
            owner_supply: Amount of tokens for owner (optional)
            swap_fee: Swap fee in basis points (optional)
            owner: Owner address (optional)
            chain_id: Target chain ID (optional, uses default if not provided)

        Returns:
            Dictionary with launch result or error
        """
        try:
            chain_id = 1 # Ethereum Mainnet

            # Use user_id as default owner if not specified (user_id is the user's wallet address)
            if owner is None:
                owner = user_id

            # Prepare function arguments
            function_args = {
                "name": name,
                "symbol": symbol,
                "token_uri": token_uri,
                "pool_supply": pool_supply,
                "owner_supply": owner_supply,
                "swap_fee": swap_fee,
                "owner": owner,
                "eth_amount": eth_amount
            }

            result = await self.execute_onchain_action(
                user_id=user_id, 
                function_name="launch_zamm_token", 
                function_args=function_args, 
                chain_id=chain_id
            )

            return result

        except Exception as e:
            logger.error(f"Error in launch_zamm_token: {e}")
            return {"error": f"Token launch failed: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        user_id = self._extract_user_id(session_context.get("api_key") if session_context else None)

        if tool_name == "launch_zamm_token":
            name = function_args.get("name")
            symbol = function_args.get("symbol")
            token_uri = function_args.get("token_uri", "")
            pool_supply = function_args.get("pool_supply")
            owner_supply = function_args.get("owner_supply", "0")
            swap_fee = function_args.get("swap_fee", "300")
            owner = function_args.get("owner")
            eth_amount = function_args.get("eth_amount")
            chain_id = function_args.get("chain_id")

            return await self.launch_zamm_token(
                user_id=user_id,
                name=name,
                symbol=symbol,
                pool_supply=pool_supply,
                eth_amount=eth_amount,
                token_uri=token_uri,
                owner_supply=owner_supply,
                swap_fee=swap_fee,
                owner=owner,
                chain_id=chain_id
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"} 