import json
import logging
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3

from mesh.context_agent import ContextAgent

load_dotenv()

logger = logging.getLogger(__name__)


class SupportedChain(Enum):
    """Supported blockchain networks"""

    ETHEREUM_MAINNET = 1
    ETHEREUM_SEPOLIA = 11155111
    BASE_MAINNET = 8453


@dataclass
class ChainConfig:
    """Configuration for blockchain networks"""

    chain_id: int
    name: str
    rpc_url_env_var: str
    explorer_base_url: str
    is_testnet: bool = False


@dataclass
class CallData:
    """Structure for contract call data"""

    target: str  # Contract address
    value: int  # ETH value to send (in wei)
    data: bytes  # Encoded function call data


@dataclass
class SessionInfo:
    """Session information for EIP7702 execution"""

    id: int
    executor: str
    validator: str
    valid_until: int
    valid_after: int
    pre_hook: str
    post_hook: str
    signature: str


class EIP7702Agent(ContextAgent, ABC):
    """
    Abstract base class for agents that can execute onchain transactions via EIP7702.
    It uses OKX Wallet Core Implementation for Session-Based Execution (https://github.com/okx/wallet-core?tab=readme-ov-file#type-3-execute-from-executor).

    This agent provides infrastructure for:
    - Chain validation and configuration
    - Executor management and authentication
    - Transaction building and execution
    - Session management for EIP7702 delegated execution
    """

    # Supported blockchain configurations
    CHAIN_CONFIGS = {
        SupportedChain.ETHEREUM_MAINNET: ChainConfig(
            chain_id=1,
            name="Ethereum Mainnet",
            rpc_url_env_var=os.getenv("ETHEREUM_RPC_URL"),
            explorer_base_url="https://etherscan.io",
            is_testnet=False,
        ),
        SupportedChain.ETHEREUM_SEPOLIA: ChainConfig(
            chain_id=11155111,
            name="Ethereum Sepolia",
            rpc_url_env_var=os.getenv("SEPOLIA_RPC_URL"),
            explorer_base_url="https://sepolia.etherscan.io",
            is_testnet=True,
        ),
        SupportedChain.BASE_MAINNET: ChainConfig(
            chain_id=8453,
            name="Base Mainnet",
            rpc_url_env_var=os.getenv("BASE_RPC_URL"),
            explorer_base_url="https://basescan.org",
            is_testnet=False,
        ),
    }

    # Wallet Core Contract ABI for EIP7702 execution
    WALLET_CORE_ABI = [
        {
            "inputs": [
                {
                    "components": [
                        {"internalType": "address", "name": "target", "type": "address"},
                        {"internalType": "uint256", "name": "value", "type": "uint256"},
                        {"internalType": "bytes", "name": "data", "type": "bytes"},
                    ],
                    "internalType": "struct Call[]",
                    "name": "calls",
                    "type": "tuple[]",
                },
                {
                    "components": [
                        {"internalType": "uint256", "name": "id", "type": "uint256"},
                        {"internalType": "address", "name": "executor", "type": "address"},
                        {"internalType": "address", "name": "validator", "type": "address"},
                        {"internalType": "uint256", "name": "validUntil", "type": "uint256"},
                        {"internalType": "uint256", "name": "validAfter", "type": "uint256"},
                        {"internalType": "bytes", "name": "preHook", "type": "bytes"},
                        {"internalType": "bytes", "name": "postHook", "type": "bytes"},
                        {"internalType": "bytes", "name": "signature", "type": "bytes"},
                    ],
                    "internalType": "struct Session",
                    "name": "session",
                    "type": "tuple",
                },
            ],
            "name": "executeFromExecutor",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "components": [
                        {"internalType": "uint256", "name": "id", "type": "uint256"},
                        {"internalType": "address", "name": "executor", "type": "address"},
                        {"internalType": "address", "name": "validator", "type": "address"},
                        {"internalType": "uint256", "name": "validUntil", "type": "uint256"},
                        {"internalType": "uint256", "name": "validAfter", "type": "uint256"},
                        {"internalType": "bytes", "name": "preHook", "type": "bytes"},
                        {"internalType": "bytes", "name": "postHook", "type": "bytes"},
                        {"internalType": "bytes", "name": "signature", "type": "bytes"},
                    ],
                    "internalType": "struct Session",
                    "name": "session",
                    "type": "tuple",
                }
            ],
            "name": "getSessionTypedHash",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    def __init__(self, default_chain: SupportedChain = SupportedChain.ETHEREUM_SEPOLIA):
        super().__init__()
        self.default_chain = default_chain
        self._web3_instances: Dict[int, Web3] = {}
        self._aws_secrets_client = None

        # Initialize AWS Secrets Manager client if credentials are available
        try:
            self._aws_secrets_client = boto3.client("secretsmanager")
        except Exception as e:
            logger.warning(f"Failed to initialize AWS Secrets Manager client: {e}")

    def _get_web3_instance(self, chain_id: int) -> Web3:
        """Get or create Web3 instance for the specified chain"""
        if chain_id in self._web3_instances:
            return self._web3_instances[chain_id]

        # Find chain config
        chain_config = None
        for supported_chain in SupportedChain:
            if self.CHAIN_CONFIGS[supported_chain].chain_id == chain_id:
                chain_config = self.CHAIN_CONFIGS[supported_chain]
                break

        if not chain_config:
            raise ValueError(f"Unsupported chain ID: {chain_id}")

        rpc_url = chain_config.rpc_url_env_var
        if not rpc_url:
            raise ValueError(f"RPC URL not found in environment variable: {chain_config.rpc_url_env_var}")

        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to {chain_config.name}")

        self._web3_instances[chain_id] = w3
        logger.info(f"Connected to {chain_config.name} (Chain ID: {chain_id})")
        return w3

    def _validate_chain_id(self, chain_id: int) -> bool:
        """Validate if the chain ID is supported"""
        supported_chain_ids = [config.chain_id for config in self.CHAIN_CONFIGS.values()]
        return chain_id in supported_chain_ids

    async def _get_session_info(self, user_id: str, chain_id: int) -> Optional[SessionInfo]:
        """Extract session information from user context for specific chain
        sessionInfos is a dictionary with chain_id as key and sessionInfo as value
        sessionInfo is a dictionary with the following keys:
        - id
        - executor
        - validator
        - validUntil
        - validAfter
        - preHook
        - postHook
        - signature
        """
        try:
            context = await self.get_user_context(user_id)
            session_infos = context.get("sessionInfos", {})
            chain_id_str = str(chain_id)
            session_data = session_infos.get(chain_id_str)
            print(f"session_data for chain {chain_id}: {session_data}")

            if not session_data:
                logger.error(f"No sessionInfo found for chain {chain_id} in context for user {user_id}")
                return None

            # Create SessionInfo object first
            session_info = SessionInfo(
                id=session_data["id"],
                executor=session_data["executor"],
                validator=session_data["validator"],
                valid_until=session_data["validUntil"],
                valid_after=session_data["validAfter"],
                pre_hook=session_data["preHook"],
                post_hook=session_data["postHook"],
                signature=session_data["signature"],
            )

            # Then validate session time using the SessionInfo object
            if not self._validate_session_time(session_info):
                logger.error(f"Session expired or not yet valid for user {user_id} on chain {chain_id}")
                return None

            return session_info
        except Exception as e:
            logger.error(f"Error extracting session info for user {user_id} on chain {chain_id}: {e}")
            return None

    async def _validate_session_for_chain(self, user_id: str, chain_id: int) -> bool:
        """Check if a valid session exists for the user for the specified chain"""
        try:
            session_info = await self._get_session_info(user_id, chain_id)
            return session_info is not None
        except Exception as e:
            logger.error(f"Error validating session for user {user_id} on chain {chain_id}: {e}")
            return False

    async def _check_smart_wallet_deployment(self, user_id: str, chain_id: int) -> bool:
        """Check if a smart wallet contract is deployed for the user on the specified chain"""
        try:
            w3 = self._get_web3_instance(chain_id)
            user_address = Web3.to_checksum_address(user_id)
            
            # Get the contract code at the user's address
            contract_code = w3.eth.get_code(user_address)
            
            # If contract_code is empty (0x or 0x0), no smart wallet is deployed
            # If there's actual bytecode, a smart wallet exists
            is_deployed = contract_code != b'' and contract_code.hex() not in ['0x', '0x0']
            
            if is_deployed:
                logger.info(f"Smart wallet found for user {user_id} on chain {chain_id}")
            else:
                logger.warning(f"No smart wallet deployed for user {user_id} on chain {chain_id}")
                
            return is_deployed
            
        except Exception as e:
            logger.error(f"Error checking smart wallet deployment for user {user_id} on chain {chain_id}: {e}")
            return False

    async def _get_executor_private_key(self, executor_address: str) -> Optional[str]:
        """Retrieve executor private key from AWS Secrets Manager"""
        if not self._aws_secrets_client:
            logger.error("AWS Secrets Manager client not initialized")
            return None

        try:
            # Use executor address as secret name
            secret_name = f"executor-private-key-{executor_address.lower()}"

            response = self._aws_secrets_client.get_secret_value(SecretId=secret_name)
            secret_data = json.loads(response["SecretString"])
            return secret_data.get("private_key")

        except ClientError as e:
            logger.error(f"Failed to retrieve executor private key from AWS: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving executor private key: {e}")
            return None

    def _prepare_session_tuple(self, session_info: SessionInfo) -> Tuple:
        """Convert SessionInfo to tuple format for contract call"""
        return (
            session_info.id,
            Web3.to_checksum_address(session_info.executor),
            Web3.to_checksum_address(session_info.validator),
            session_info.valid_until,
            session_info.valid_after,
            bytes.fromhex(session_info.pre_hook[2:]) if session_info.pre_hook.startswith("0x") else b"",
            bytes.fromhex(session_info.post_hook[2:]) if session_info.post_hook.startswith("0x") else b"",
            bytes.fromhex(session_info.signature[2:]) if session_info.signature.startswith("0x") else b"",
        )

    def _prepare_call_tuple(self, call_data: CallData) -> Tuple:
        """Convert CallData to tuple format for contract call"""
        return (call_data.target, call_data.value, call_data.data)

    def _validate_session_time(self, session_info: SessionInfo) -> bool:
        current_time = int(time.time())
        if current_time < session_info.valid_after:
            return False
        if current_time > session_info.valid_until:
            return False
        return True

    def _get_chain_enum(self, chain_id: int) -> SupportedChain:
        """Get SupportedChain enum from chain_id"""
        for supported_chain in SupportedChain:
            if self.CHAIN_CONFIGS[supported_chain].chain_id == chain_id:
                return supported_chain
        raise ValueError(f"Unsupported chain ID: {chain_id}")

    def _get_revert_reason(self, w3: Web3, tx: dict, receipt: Any) -> Optional[str]:
        """Try to extract revert reason from failed transaction"""
        try:
            # Try to replay the transaction to get revert reason
            w3.eth.call(tx, receipt.blockNumber)
            return "Unknown reason"
        except Exception as e:
            error_str = str(e)

            # Extract revert reason from different error formats
            if "execution reverted:" in error_str:
                # Extract reason after "execution reverted:"
                reason_start = error_str.find("execution reverted:") + len("execution reverted:")
                reason = error_str[reason_start:].strip()
                return reason if reason else "No revert reason provided"
            elif "revert" in error_str.lower():
                # General revert error
                return error_str
            else:
                return f"Transaction failed: {error_str}"

    async def _execute_transaction(
        self,
        user_id: str,
        call_data_list: List[CallData],
        chain_id: int,
        gas_limit: int = 500000,
        max_fee_per_gas_gwei: float = 2.0,
        max_priority_fee_per_gas_gwei: float = 0.1,
    ) -> Dict[str, Any]:
        """
        Execute transaction on behalf of user using EIP7702 delegation

        Args:
            user_id: User identifier
            call_data_list: List of contract calls to execute
            chain_id: Target blockchain chain ID
            gas_limit: Maximum gas to use
            max_fee_per_gas_gwei: Maximum fee per gas in Gwei
            max_priority_fee_per_gas_gwei: Maximum priority fee per gas in Gwei

        Returns:
            Dictionary with transaction result or error. The result contains user-friendly message about the transaction status or error.
        """
        try:
            # Get Web3 instance
            w3 = self._get_web3_instance(chain_id)

            # Get session info
            session_info = await self._get_session_info(user_id, chain_id)
            if not session_info:
                return {
                    "error": "Failed to find an active session for your wallet. You need to create a new session to authorize this transaction at https://heurist.ai/eip7702"
                }

            # Get executor private key
            executor_private_key = await self._get_executor_private_key(session_info.executor)
            if not executor_private_key:
                return {"error": "Transaction executor is temporarily unavailable. Please try again later."}

            # Create executor account
            executor_account = Account.from_key(executor_private_key)
            if executor_account.address.lower() != session_info.executor.lower():
                return {
                    "error": "There's a configuration issue with your session. Please create a new session at https://heurist.ai/eip7702"
                }

            user_wallet_address = user_id

            # Create wallet contract instance
            user_smart_wallet = w3.eth.contract(
                address=Web3.to_checksum_address(user_wallet_address), abi=self.WALLET_CORE_ABI
            )

            # Prepare call data tuples
            call_tuples = [self._prepare_call_tuple(call_data) for call_data in call_data_list]

            # Prepare session tuple
            session_tuple = self._prepare_session_tuple(session_info)

            # Get nonce
            nonce = w3.eth.get_transaction_count(executor_account.address)

            # Build transaction
            tx = user_smart_wallet.functions.executeFromExecutor(call_tuples, session_tuple).build_transaction(
                {
                    "from": executor_account.address,
                    "nonce": nonce,
                    "gas": gas_limit,
                    "maxFeePerGas": w3.to_wei(max_fee_per_gas_gwei, "gwei"),
                    "maxPriorityFeePerGas": w3.to_wei(max_priority_fee_per_gas_gwei, "gwei"),
                    "chainId": chain_id,
                }
            )

            # Sign and send transaction
            signed_tx = w3.eth.account.sign_transaction(tx, executor_private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            logger.info(f"Transaction sent: {tx_hash.hex()}")

            # Wait for transaction receipt to check success/failure
            try:
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

                if receipt.status == 1:
                    # Transaction succeeded
                    logger.info(f"Transaction successful: {tx_hash.hex()}")
                    # TODO: consider charging for the gas used
                    return {
                        "success": True,
                        "message": f"Transaction executed successfully! Gas used: {receipt.gasUsed}. View on {self.CHAIN_CONFIGS[self._get_chain_enum(chain_id)].explorer_base_url}/tx/{tx_hash.hex()}",
                        "tx_hash": tx_hash.hex(),
                        "chain_id": chain_id,
                        "executor": executor_account.address,
                        "gas_used": receipt.gasUsed,
                        "block_number": receipt.blockNumber,
                    }
                else:
                    # Transaction failed, try to get revert reason
                    revert_reason = self._get_revert_reason(w3, tx, receipt)
                    error_msg = (
                        f"Transaction reverted: {revert_reason}"
                        if revert_reason
                        else "Transaction reverted with unknown reason"
                    )
                    logger.error(f"{error_msg}. Tx hash: {tx_hash.hex()}")

                    return {
                        "error": f"{error_msg}. View failed transaction: {self.CHAIN_CONFIGS[self._get_chain_enum(chain_id)].explorer_base_url}/tx/{tx_hash.hex()}",
                        "tx_hash": tx_hash.hex(),
                        "chain_id": chain_id,
                        "revert_reason": revert_reason,
                        "gas_used": receipt.gasUsed,
                    }

            except Exception as receipt_error:
                logger.error(f"Error waiting for transaction receipt: {receipt_error}")
                return {
                    "error": f"Transaction was sent but receipt could not be confirmed: {str(receipt_error)}. View transaction: {self.CHAIN_CONFIGS[self._get_chain_enum(chain_id)].explorer_base_url}/tx/{tx_hash.hex()}",
                    "tx_hash": tx_hash.hex(),
                    "chain_id": chain_id,
                }

        except Exception as e:
            logger.error(f"Transaction execution failed: {e}")
            return {"error": f"Transaction execution failed: {str(e)}"}

    @abstractmethod
    async def prepare_call_data(
        self, function_name: str, function_args: dict, chain_id: int, user_context: Dict[str, Any]
    ) -> List[CallData]:
        """
        Prepare call data for specific transaction type.

        This method must be implemented by subclasses to define how to prepare
        the contract call data for their specific use case.

        Args:
            function_name: Name of the function of the subclass that is being called
            function_args: Arguments from the tool call
            chain_id: Target blockchain chain ID
            user_context: User's stored context

        Returns:
            List of CallData objects representing the contract calls to execute
        """
        pass

    @abstractmethod
    def get_supported_functions(self) -> List[str]:
        """
        Return list of supported function names that this agent can handle.

        Returns:
            List of function names that can be processed by this agent
        """
        pass

    async def execute_onchain_action(
        self, user_id: str, function_name: str, function_args: dict, chain_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute an onchain action for the user.

        Args:
            user_id: User identifier
            function_name: Name of the function to execute
            function_args: Arguments for the function
            chain_id: Target chain ID (uses default if not specified)

        Returns:
            Dictionary with execution result or error
        """
        try:
            # Validate function
            if function_name not in self.get_supported_functions():
                return {"error": f"Unsupported function: {function_name}"}

            # Use default chain if not specified
            if chain_id is None:
                chain_id = self.CHAIN_CONFIGS[self.default_chain].chain_id

            if not self._validate_chain_id(chain_id):
                return {"error": f"Unsupported chain ID: {chain_id}"}

            # Get user context
            user_context = await self.get_user_context(user_id)

            # Check if a valid session exists for the user for the chain
            if not await self._validate_session_for_chain(user_id, chain_id):
                chain_name = self.CHAIN_CONFIGS[self._get_chain_enum(chain_id)].name
                return {
                    "error": f"No valid session found for {chain_name}. Please create a session for this chain at https://heurist.ai/eip7702"
                }

            # Check if smart wallet is deployed for the user on the chain
            if not await self._check_smart_wallet_deployment(user_id, chain_id):
                chain_name = self.CHAIN_CONFIGS[self._get_chain_enum(chain_id)].name
                return {
                    "error": f"No smart wallet found for your address on {chain_name}. Please deploy a smart wallet first at https://heurist.ai/eip7702"
                }

            # Prepare call data
            call_data_list = await self.prepare_call_data(function_name, function_args, chain_id, user_context)

            if not call_data_list:
                return {"error": "Failed to prepare call data"}

            # Execute transaction
            result = await self._execute_transaction(user_id, call_data_list, chain_id)

            # Update user context with transaction info if successful
            if result.get("success"):
                await self._update_transaction_history(user_id, function_name, function_args, result)

            return result

        except Exception as e:
            logger.error(f"Error executing onchain action: {e}")
            return {"error": f"Failed to execute onchain action: {str(e)}"}

    async def _update_transaction_history(
        self, user_id: str, function_name: str, function_args: dict, tx_result: Dict[str, Any]
    ) -> None:
        """Update user context with transaction history"""
        try:
            context = await self.get_user_context(user_id)

            if "transaction_history" not in context:
                context["transaction_history"] = []

            transaction_record = {
                "timestamp": datetime.now().isoformat(),
                "function": function_name,
                "args": function_args,
                "tx_hash": tx_result.get("tx_hash"),
                "chain_id": tx_result.get("chain_id"),
                "status": "success" if tx_result.get("success") else "failed",
            }

            context["transaction_history"].append(transaction_record)

            # Keep only last 100 transactions
            # if len(context["transaction_history"]) > 100:
            #     context["transaction_history"] = context["transaction_history"][-100:]

            await self.set_user_context(context, user_id)

        except Exception as e:
            logger.error(f"Failed to update transaction history: {e}")

    async def cleanup(self):
        """Cleanup Web3 instances and parent resources"""
        self._web3_instances.clear()
        await super().cleanup()
