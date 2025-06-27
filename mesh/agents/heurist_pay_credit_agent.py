import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from web3 import Web3

from mesh.eip7702_agent import CallData, EIP7702Agent, SupportedChain

logger = logging.getLogger(__name__)


class HeuristPayCreditAgent(EIP7702Agent):
    """
    Agent that helps users purchase API credits using USDC on Base chain via EIP7702 delegation.

    This agent handles:
    - Purchasing API credits using USDC tokens
    - Automatic approval of USDC spending if needed
    - Batching approval and purchase transactions
    """

    # Contract addresses on Base chain
    API_CREDIT_PURCHASER_ADDRESS = "0x59d944b7ff8c432ff395683f5c95d97ca0237986"
    USDC_TOKEN_ADDRESS = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
    USDC_DECIMALS = 6

    # ERC20 ABI for approval
    ERC20_ABI = [
        {
            "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
            "name": "allowance",
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"name": "account", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    # ApiCreditPurchaser ABI
    API_CREDIT_PURCHASER_ABI = [
        {
            "inputs": [
                {"name": "tokenAddress", "type": "address"},
                {"name": "creditedAddress", "type": "address"},
                {"name": "amount", "type": "uint256"},
            ],
            "name": "purchaseCredits",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ]

    def __init__(self):
        super().__init__(default_chain=SupportedChain.BASE_MAINNET)

        self.metadata.update(
            {
                "name": "Heurist Pay Credit Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Agent that helps users purchase API credits using USDC on Base chain with EIP7702 delegation.",
                "tags": ["EIP7702"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/HeuristPay.png",
                "examples": [
                    "Purchase 10 USDC worth of API credits",
                    "Buy credits for $5 USDC and credit them to another address",
                    "Purchase API credits for 25.50 USDC",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a Heurist API credit purchase assistant that helps users buy API credits using USDC on Base chain.

        Key functions:
        - Purchase API credits using USDC tokens
        - Automatically handle USDC token approvals if needed
        - Support crediting purchased credits to different addresses
        - Execute transactions efficiently using batched approvals and purchases

        When handling credit purchases:
        - Always validate that the user has sufficient USDC balance
        - Check current allowance and approve additional tokens if needed
        - Confirm purchase details (amount, credited address) before execution
        - Provide clear confirmation of purchase details and costs
        - Explain any approval transactions that will be executed

        Supported chain: Base Mainnet (default)
        Payment token: USDC (6 decimals)
        Contract Address: 0x59d944b7ff8c432ff395683f5c95d97ca0237986
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "purchase_api_credits",
                    "description": "Purchase API credits using USDC on Base chain",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "amount_usdc": {
                                "type": "string",
                                "description": "The amount of USDC to spend on credits (e.g., '100.50' for 100.50 USDC)",
                            },
                            "credited_address": {
                                "type": "string",
                                "description": "The address that will receive the purchased credits (optional, defaults to buyer's address)",
                                "default": "",
                            },
                            "chain_id": {
                                "type": "integer",
                                "description": "The blockchain chain ID (8453 for Base mainnet)",
                                "default": 8453,
                            },
                        },
                        "required": ["amount_usdc"],
                    },
                },
            },
        ]

    def get_supported_functions(self) -> List[str]:
        """Return list of supported function names"""
        return ["purchase_api_credits"]

    async def prepare_call_data(
        self, function_name: str, function_args: dict, chain_id: int, user_context: Dict[str, Any]
    ) -> List[CallData]:
        """
        Prepare call data for API credit purchase.

        Args:
            function_name: Name of the function being executed
            function_args: Contains purchase parameters
            chain_id: Target blockchain chain ID
            user_context: User's stored context

        Returns:
            List containing CallData objects for approval (if needed) and purchase
        """
        if function_name == "purchase_api_credits":
            logger.info(f"Preparing call data for credit purchase: {function_name}")
            logger.info(f"Function args: {function_args}")
            logger.info(f"User context: {user_context}")
            logger.info(f"Chain ID: {chain_id}")

            # Extract user_id from the function args since it gets passed through execute_onchain_action
            user_id = function_args.get("user_id")
            return await self._prepare_purchase_call_data(function_args, chain_id, user_id)
        else:
            raise ValueError(f"Unsupported function: {function_name}")

    async def _prepare_purchase_call_data(self, function_args: dict, chain_id: int, user_id: str) -> List[CallData]:
        """
        Prepare call data for API credit purchase with automatic approval handling.
        """
        try:
            amount_usdc = function_args.get("amount_usdc")
            credited_address = function_args.get("credited_address", "")

            if not amount_usdc:
                logger.error("Missing required parameter: amount_usdc")
                raise ValueError("Missing required parameter: amount_usdc")

            # Get Web3 instance for the target chain
            w3 = self._get_web3_instance(chain_id)

            # In EIP7702Agent, user_id is the wallet address
            user_wallet_address = user_id

            # Use user's address as credited address if not specified
            if not credited_address:
                credited_address = user_wallet_address

            # Validate and convert credited address to checksum format
            try:
                credited_address = Web3.to_checksum_address(credited_address)
                user_wallet_address = Web3.to_checksum_address(user_wallet_address)
            except ValueError as e:
                logger.error(f"Invalid address format: {e}")
                raise ValueError(
                    "Invalid address format. Please ensure address starts with '0x' and is 42 characters long."
                )

            # Convert USDC amount to wei (6 decimals for USDC)
            try:
                amount_usdc_wei = int(float(amount_usdc) * (10**self.USDC_DECIMALS))
            except ValueError as e:
                logger.error(f"Invalid USDC amount: {e}")
                raise ValueError("Invalid USDC amount. Please ensure it's a valid number.")

            if amount_usdc_wei <= 0:
                logger.error(f"USDC amount must be positive, got: {amount_usdc}")
                raise ValueError("USDC amount must be positive")

            # Create contract instances
            usdc_contract = w3.eth.contract(address=self.USDC_TOKEN_ADDRESS, abi=self.ERC20_ABI)
            purchaser_contract = w3.eth.contract(
                address=self.API_CREDIT_PURCHASER_ADDRESS, abi=self.API_CREDIT_PURCHASER_ABI
            )

            # Check user's USDC balance
            try:
                usdc_balance = usdc_contract.functions.balanceOf(user_wallet_address).call()
                if usdc_balance < amount_usdc_wei:
                    logger.error(f"Insufficient USDC balance. Required: {amount_usdc_wei}, Available: {usdc_balance}")
                    raise ValueError(
                        f"Insufficient USDC balance. You need {float(amount_usdc_wei) / (10**self.USDC_DECIMALS):.6f} USDC but only have {float(usdc_balance) / (10**self.USDC_DECIMALS):.6f} USDC"
                    )
            except Exception as e:
                if "Insufficient USDC balance" in str(e):
                    raise e
                logger.error(f"Failed to check USDC balance: {e}")
                raise ValueError("Failed to check USDC balance. Please try again.")

            # Check current allowance
            call_data_list = []
            try:
                current_allowance = usdc_contract.functions.allowance(
                    user_wallet_address, self.API_CREDIT_PURCHASER_ADDRESS
                ).call()

                # If allowance is insufficient, add approval transaction
                if current_allowance < amount_usdc_wei:
                    # Approve a bit more than needed for future transactions (add 10%)
                    approval_amount = int(amount_usdc_wei * 1.1)

                    approval_data = usdc_contract.encode_abi(
                        "approve", args=[self.API_CREDIT_PURCHASER_ADDRESS, approval_amount]
                    )

                    approval_call_data = CallData(target=self.USDC_TOKEN_ADDRESS, value=0, data=approval_data)
                    call_data_list.append(approval_call_data)

                    logger.info(f"Added approval for {float(approval_amount) / (10**self.USDC_DECIMALS):.6f} USDC")
            except Exception as e:
                logger.error(f"Failed to check allowance: {e}")
                raise ValueError("Failed to check token allowance. Please try again.")

            # Prepare purchase transaction
            try:
                purchase_data = purchaser_contract.encode_abi(
                    "purchaseCredits", args=[self.USDC_TOKEN_ADDRESS, credited_address, amount_usdc_wei]
                )

                purchase_call_data = CallData(target=self.API_CREDIT_PURCHASER_ADDRESS, value=0, data=purchase_data)
                call_data_list.append(purchase_call_data)

                logger.info(f"Prepared API credit purchase: {amount_usdc} USDC for address {credited_address}")

            except Exception as e:
                logger.error(f"Failed to encode purchase function: {e}")
                raise ValueError("Failed to prepare credit purchase transaction")

            return call_data_list

        except Exception as e:
            logger.error(f"Error preparing call data for credit purchase: {e}")
            # Re-raise validation errors for user-friendly handling
            raise e

    async def purchase_api_credits(
        self, user_id: str, amount_usdc: str, credited_address: Optional[str] = None, chain_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute API credit purchase for a user.

        Args:
            user_id: The user purchasing credits (wallet address)
            amount_usdc: Amount of USDC to spend
            credited_address: Address to credit the purchased credits to (optional)
            chain_id: Target chain ID (optional, uses default if not provided)

        Returns:
            Dictionary with purchase result or error
        """
        try:
            chain_id = chain_id or 8453  # Base Mainnet

            # Use user_id as credited address if not specified (user_id is the user's wallet address)
            if credited_address is None:
                credited_address = user_id

            # Prepare function arguments
            function_args = {
                "amount_usdc": amount_usdc,
                "credited_address": credited_address,
                "user_id": user_id,  # Pass user_id in function_args so prepare_call_data can access it
            }

            result = await self.execute_onchain_action(
                user_id=user_id, function_name="purchase_api_credits", function_args=function_args, chain_id=chain_id
            )

            return result

        except Exception as e:
            logger.error(f"Error in purchase_api_credits: {e}")
            return {"error": f"Credit purchase failed: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        user_id = self._extract_user_id(session_context.get("api_key") if session_context else None)

        if tool_name == "purchase_api_credits":
            amount_usdc = function_args.get("amount_usdc")
            credited_address = function_args.get("credited_address")
            chain_id = function_args.get("chain_id")

            return await self.purchase_api_credits(
                user_id=user_id, amount_usdc=amount_usdc, credited_address=credited_address, chain_id=chain_id
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"}
