import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from web3 import Web3
from mesh.eip7702_agent import EIP7702Agent, CallData, SupportedChain

logger = logging.getLogger(__name__)


class ERC20TokenTransferAgent(EIP7702Agent):
    """
    Agent that helps users transfer ERC20 tokens between accounts using EIP7702 delegation.
    
    This agent handles:
    - ERC20 token transfers
    - Balance checking
    - Transfer history tracking
    """

    # Standard ERC20 ABI for transfer function
    ERC20_ABI = [
        {
            "constant": False,
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "amount", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]

    def __init__(self):
        super().__init__(default_chain=SupportedChain.ETHEREUM_SEPOLIA)

        self.metadata.update({
            "name": "ERC20 Token Transfer Agent",
            "version": "1.0.0",
            "author": "Heurist team",
            "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
            "description": "Agent that helps users transfer ERC20 tokens between accounts using EIP7702 delegation.",
            "tags": ["EIP7702", "ERC20", "Token Transfer", "DeFi"],
            "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/ERC20TokenTransfer.png",
            "examples": [
                "Transfer 100 USDC to 0x1234567890123456789012345678901234567890",
                "Send 0.5 WETH to alice.eth",
                "Transfer 1000 tokens of contract 0xA0b86a33E6441B7c8AF82F84e748f34E5d7bF41E to 0x742..."
            ],
        })

    def get_system_prompt(self) -> str:
        return """You are an ERC20 token transfer assistant that helps users transfer tokens on Ethereum blockchain.

        Key functions:
        - Transfer ERC20 tokens between addresses
        - Check token balances before transfers
        - Provide transaction confirmations and history
        - Support both mainnet and testnet operations

        When handling token transfers:
        - Always validate addresses are properly formatted
        - Confirm token contract addresses are valid
        - Check that amounts are reasonable and user has sufficient balance
        - Provide clear confirmation of transfer details before execution
        - Keep track of transfer history for the user

        Supported chains: Ethereum Mainnet and Sepolia Testnet
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "transfer_erc20_token",
                    "description": "Transfer an ERC20 token from user's wallet to another address",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {
                                "type": "string",
                                "description": "The contract address of the ERC20 token to transfer",
                            },
                            "amount": {
                                "type": "string",
                                "description": "The amount of tokens to transfer (in human-readable format, e.g., '100.5')",
                            },
                            "recipient": {
                                "type": "string",
                                "description": "The address to transfer the tokens to",
                            },
                            "chain_id": {
                                "type": "integer",
                                "description": "The blockchain chain ID (1 for mainnet, 11155111 for Sepolia)",
                                "default": 11155111
                            }
                        },
                        "required": ["token_address", "amount", "recipient"],
                    },
                },
            },
        ]

    def get_supported_functions(self) -> List[str]:
        """Return list of supported function names"""
        return ["transfer_erc20_token"]

    async def prepare_call_data(
        self, 
        function_args: dict, 
        chain_id: int,
        user_context: Dict[str, Any]
    ) -> List[CallData]:
        """
        Prepare call data for ERC20 token transfer.
        
        Args:
            function_args: Contains token_address, amount, recipient
            chain_id: Target blockchain chain ID
            user_context: User's stored context
            
        Returns:
            List containing a single CallData object for the ERC20 transfer
        """
        try:
            token_address = function_args.get("token_address")
            amount = function_args.get("amount")
            recipient = function_args.get("recipient")

            if not all([token_address, amount, recipient]):
                logger.error("Missing required parameters for ERC20 transfer")
                return []

            # Get Web3 instance for the target chain
            w3 = self._get_web3_instance(chain_id)

            # Validate and convert addresses to checksum format
            try:
                token_address = Web3.to_checksum_address(token_address)
                recipient = Web3.to_checksum_address(recipient)
            except ValueError as e:
                logger.error(f"Invalid address format: {e}")
                return []

            # Create ERC20 contract instance
            erc20_contract = w3.eth.contract(address=token_address, abi=self.ERC20_ABI)

            # Get token decimals
            try:
                decimals = erc20_contract.functions.decimals().call()
            except Exception as e:
                logger.error(f"Failed to get decimals for token {token_address}: {e}")
                return []

            # Convert amount to wei (smallest unit)
            try:
                amount_wei = int(float(amount) * (10 ** decimals))
            except (ValueError, OverflowError) as e:
                logger.error(f"Invalid amount format: {amount}, error: {e}")
                return []

            if amount_wei <= 0:
                logger.error(f"Amount must be positive, got: {amount}")
                return []

            # Encode the transfer function call
            try:
                transfer_data = erc20_contract.encode_abi("transfer", args=[recipient, amount_wei])
            except Exception as e:
                logger.error(f"Failed to encode transfer function: {e}")
                return []

            # Create CallData object
            call_data = CallData(
                target=token_address,
                value=0,  # No ETH value for ERC20 transfer
                data=transfer_data
            )

            logger.info(f"Prepared ERC20 transfer: {amount} tokens from {token_address} to {recipient}")
            return [call_data]

        except Exception as e:
            logger.error(f"Error preparing call data for ERC20 transfer: {e}")
            return []

    async def transfer_erc20_token(
        self, 
        user_id: str, 
        token_address: str, 
        amount: str, 
        recipient: str,
        chain_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute ERC20 token transfer for a user.
        
        Args:
            user_id: User identifier
            token_address: Contract address of the ERC20 token
            amount: Amount to transfer (human-readable format)
            recipient: Recipient address
            chain_id: Target chain ID (optional, uses default if not provided)
            
        Returns:
            Dictionary with transfer result or error
        """
        if not user_id:
            logger.error("No user ID available, cannot transfer ERC20 token")
            return {"error": "No user ID available, cannot transfer ERC20 token"}

        try:
            # Use default chain if not specified
            if chain_id is None:
                chain_id = self.CHAIN_CONFIGS[self.default_chain].chain_id

            # Prepare function arguments
            function_args = {
                "token_address": token_address,
                "amount": amount,
                "recipient": recipient
            }

            # Execute the onchain action
            result = await self.execute_onchain_action(
                user_id=user_id,
                function_name="transfer_erc20_token",
                function_args=function_args,
                chain_id=chain_id
            )

            if result.get("success"):
                # Update local context with transfer info
                # await self._record_transfer(user_id, token_address, amount, recipient, result.get("tx_hash"))
                
                return {
                    "status": "success",
                    "message": f"Successfully transferred {amount} tokens to {recipient}",
                    "tx_hash": result.get("tx_hash"),
                    "chain_id": chain_id,
                    "token_address": token_address,
                    "amount": amount,
                    "recipient": recipient
                }
            else:
                return result  # Return error from execute_onchain_action

        except Exception as e:
            logger.error(f"Error in transfer_erc20_token: {e}")
            return {"error": f"Transfer failed: {str(e)}"}

    async def _handle_tool_logic(
        self, 
        tool_name: str, 
        function_args: dict, 
        session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        user_id = self._extract_user_id(session_context.get("api_key") if session_context else None)
        
        if tool_name == "transfer_erc20_token":
            token_address = function_args.get("token_address")
            amount = function_args.get("amount")
            recipient = function_args.get("recipient")
            chain_id = function_args.get("chain_id")

            if not all([token_address, amount, recipient]):
                return {"error": "Missing required parameters: 'token_address', 'amount', or 'recipient'"}

            return await self.transfer_erc20_token(
                user_id=user_id,
                token_address=token_address,
                amount=amount,
                recipient=recipient,
                chain_id=chain_id
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"}