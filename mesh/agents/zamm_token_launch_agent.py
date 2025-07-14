import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import time
import json
import uuid
import os
import requests
from urllib.parse import urlparse

from web3 import Web3
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from mesh.eip7702_agent import CallData, EIP7702Agent, SupportedChain

load_dotenv()

logger = logging.getLogger(__name__)


class ZammTokenLaunchAgent(EIP7702Agent):
    """
    Agent that helps users launch new tokens and create liquidity pools using ZAMM protocol with EIP7702 delegation.

    This agent handles:
    - Token creation with custom metadata URI
    - Creator supply allocation with unlock timing
    - Tranche configuration for token distribution
    - Pricing configuration for token sales
    - Metadata storage
    """

    # ZAMM contract address on Ethereum mainnet
    # TODO: replace with new contract address
    ZAMM_CONTRACT_ADDRESS = "0x000000000077A9C733B9ac3781fB5A1BC7701FBc"
    
    # Default image URL when no image is provided
    DEFAULT_IMAGE_URL = "https://zamm.heurist.xyz/default.jpg"
    
    # R2 bucket configuration
    R2_BUCKET_NAME = "zamm"
    R2_ENDPOINT_URL = "https://zamm.heurist.xyz"

    # ABI for the launch function and Launch event
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
            "outputs": [{"name": "coinId", "type": "uint256"}],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "creator", "type": "address"},
                {"indexed": True, "name": "coinId", "type": "uint256"},
                {"indexed": False, "name": "saleSupply", "type": "uint96"},
            ],
            "name": "Launch",
            "type": "event",
        }
    ]

    def __init__(self):
        super().__init__(default_chain=SupportedChain.ETHEREUM_MAINNET)
        
        # Initialize R2 client
        self.r2_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            endpoint_url=os.getenv("S3_ENDPOINT"),
            region_name="auto",
        )

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
                    "Launch a token with name, symbol and metadata",
                    "Create a token with custom creator supply and unlock schedule",
                    "Launch token with custom tranche configuration",
                    "Update token image after launch",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a ZAMM token launch assistant that helps users create new tokens on Ethereum blockchain.

        Key functions:
        - Launch new tokens with custom metadata (name, symbol, description, image)
        - Configure creator supply with unlock timing (default: 1 week + 12 hours)
        - Set up token distribution tranches
        - Configure pricing for token sales
        - Update token images after launch

        When handling token launches:
        - Always validate that name and symbol are provided
        - Use default image URL if no image is provided
        - Generate and store metadata JSON
        - Confirm token details before execution
        - Explain the tokenomics and unlock schedule

        Default values:
        - Creator Supply: 100,000,000 tokens (100000000000000000000000000 wei)
        - Creator Unlock: 1 week + 12 hours from launch time
        - Tranche Coins: 150,000 tokens (150000000000000000000000 wei)
        - Tranche Price: 0.001 ETH (1000000000000000 wei)
        - Image: https://zamm.heurist.xyz/default.jpg

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
                            "name": {
                                "type": "string",
                                "description": "The name of the token (required)",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "The symbol of the token (required)",
                            },
                            "description": {
                                "type": "string",
                                "description": "The description of the token (optional)",
                                "default": "",
                            },
                            "image": {
                                "type": "string",
                                "description": "The image URL for the token (optional, defaults to https://zamm.heurist.xyz/default.jpg)",
                                "default": "",
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
                        "required": ["name", "symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "update_image",
                    "description": "Update the image URL in an existing token metadata",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "image_url": {
                                "type": "string",
                                "description": "The new image URL for the token (required)",
                            },
                            "metadata_url": {
                                "type": "string",
                                "description": "The metadata JSON file URL to update (required)",
                            },
                        },
                        "required": ["image_url", "metadata_url"],
                    },
                },
            },
        ]

    def get_supported_functions(self) -> List[str]:
        """Return list of supported function names"""
        return ["launch", "update_image"]

    async def _store_metadata_in_r2(self, user_id: str, metadata: Dict[str, Any]) -> str:
        """
        Store metadata JSON in Cloudflare R2 bucket.
        
        Args:
            user_id: User ID (wallet address)
            metadata: Metadata dictionary to store
            
        Returns:
            The public URL to the stored metadata
        """
        try:
            # Generate unique filename
            metadata_filename = f"{uuid.uuid4().hex}.json"
            
            # Create object key: user_id (lowercase) / filename
            object_key = f"{user_id.lower()}/{metadata_filename}"
            
            # Store in R2 bucket
            self.r2_client.put_object(
                Bucket=self.R2_BUCKET_NAME,
                Key=object_key,
                Body=json.dumps(metadata, indent=2).encode("utf-8"),
                ContentType="application/json",
            )
            
            # Return public URL
            metadata_url = f"{self.R2_ENDPOINT_URL}/{object_key}"
            logger.info(f"Stored metadata in R2: {metadata_url}")
            return metadata_url
            
        except Exception as e:
            logger.error(f"Error storing metadata in R2: {e}")
            raise ValueError(f"Failed to store metadata: {str(e)}")

    async def _update_metadata_in_r2(self, metadata_url: str, new_image_url: str, requesting_user_id: str) -> Dict[str, Any]:
        """
        Update image URL in existing metadata stored in R2.
        
        Args:
            metadata_url: URL of the metadata file to update
            new_image_url: New image URL to set
            requesting_user_id: User ID making the update request
            
        Returns:
            Updated metadata dictionary
        """
        try:
            # Extract object key from URL
            if not metadata_url.startswith(self.R2_ENDPOINT_URL):
                raise ValueError("Invalid metadata URL")
                
            object_key = metadata_url.replace(f"{self.R2_ENDPOINT_URL}/", "")
            
            # Extract user_id from object key path (format: user_id/filename.json)
            if "/" not in object_key:
                raise ValueError("Invalid metadata URL format")
            
            metadata_owner_user_id = object_key.split("/")[0]
            
            # Security check: only the same user can update their own metadata
            if requesting_user_id.lower() != metadata_owner_user_id.lower():
                raise ValueError("Access denied: You can only update your own metadata")
            
            # Get existing metadata
            response = self.r2_client.get_object(Bucket=self.R2_BUCKET_NAME, Key=object_key)
            existing_metadata = json.loads(response["Body"].read().decode("utf-8"))
            
            # Update image URL
            existing_metadata["image"] = new_image_url
            
            # Store updated metadata
            self.r2_client.put_object(
                Bucket=self.R2_BUCKET_NAME,
                Key=object_key,
                Body=json.dumps(existing_metadata, indent=2).encode("utf-8"),
                ContentType="application/json",
            )
            
            logger.info(f"Updated metadata image in R2: {metadata_url} by user: {requesting_user_id}")
            return existing_metadata
            
        except ClientError as e:
            logger.error(f"Error updating metadata in R2: {e}")
            raise ValueError(f"Failed to update metadata: {str(e)}")
        except Exception as e:
            logger.error(f"Error updating metadata in R2: {e}")
            raise ValueError(f"Failed to update metadata: {str(e)}")

    async def _upload_external_image_to_r2(self, image_url: str, user_id: str) -> str:
        """
        Download external image and upload to R2 bucket with same pattern as metadata URL.
        
        Args:
            image_url: URL of the external image
            user_id: User ID (wallet address)
            
        Returns:
            The public URL to the uploaded image in R2
        """
        try:
            # Check if it's already an R2 URL
            if image_url.startswith(self.R2_ENDPOINT_URL):
                return image_url
            
            # Check if it's a valid URL
            parsed_url = urlparse(image_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid image URL")
            
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Check if it's an image (basic check)
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise ValueError("URL does not point to an image")
            
            # Get file extension from content type
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                ext = '.jpg'  # Default fallback
            
            # Generate unique filename
            image_filename = f"{uuid.uuid4().hex}{ext}"
            
            # Create object key: user_id (lowercase) / filename
            object_key = f"{user_id.lower()}/{image_filename}"
            
            # Upload to R2 bucket
            self.r2_client.put_object(
                Bucket=self.R2_BUCKET_NAME,
                Key=object_key,
                Body=response.content,
                ContentType=content_type,
            )
            
            # Return public URL
            uploaded_image_url = f"{self.R2_ENDPOINT_URL}/{object_key}"
            logger.info(f"Uploaded external image to R2: {uploaded_image_url}")
            return uploaded_image_url
            
        except Exception as e:
            logger.error(f"Error uploading external image to R2: {e}")
            raise ValueError(f"Failed to upload image: {str(e)}")

    def _parse_launch_event_logs(self, w3: Web3, tx_receipt) -> Optional[int]:
        """
        Parse the Launch event logs from transaction receipt to extract coinId.
        
        Args:
            w3: Web3 instance
            tx_receipt: Transaction receipt
            
        Returns:
            coinId if found, None otherwise
        """
        try:
            # Create contract instance to parse logs
            zamm_contract = w3.eth.contract(address=self.ZAMM_CONTRACT_ADDRESS, abi=self.ZAMM_ABI)
            
            # Get Launch event logs
            launch_events = zamm_contract.events.Launch().process_receipt(tx_receipt)
            
            if launch_events:
                # Get the first Launch event (there should only be one per transaction)
                launch_event = launch_events[0]
                coin_id = launch_event['args']['coinId']
                logger.info(f"Extracted coinId from Launch event: {coin_id}")
                return coin_id
            else:
                logger.warning("No Launch event found in transaction receipt")
                return None
                
        except Exception as e:
            logger.error(f"Error parsing Launch event logs: {e}")
            return None

    async def _execute_transaction(
        self,
        user_id: str,
        call_data_list: List[CallData],
        chain_id: int,
        gas_buffer_percent: float = 20.0,
    ) -> Dict[str, Any]:
        """
        Override parent method to extract coinId from Launch event logs.
        """
        # Call parent method to execute transaction
        result = await super()._execute_transaction(user_id, call_data_list, chain_id, gas_buffer_percent)
        
        # If transaction was successful, try to extract coinId from event logs
        if result.get("success") and result.get("tx_hash"):
            try:
                w3 = self._get_web3_instance(chain_id)
                tx_hash = result["tx_hash"]
                
                # Get transaction receipt
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                
                # Parse Launch event logs to extract coinId
                coin_id = self._parse_launch_event_logs(w3, tx_receipt)

                # Add metadata URL to result if available
                if hasattr(self, '_current_metadata_url'):
                    result["metadata_url"] = self._current_metadata_url
                    # Clean up the temporary storage
                    delattr(self, '_current_metadata_url')
                
                if coin_id is not None:
                    # Create ZAMM finance link
                    zamm_link = f"https://www.zamm.finance/c/{coin_id}"
                    result["coin_id"] = coin_id
                    result["zamm_link"] = zamm_link
                    # Update success message to include ZAMM link
                    result["message"] = f"Token launch successful! View your token at: {zamm_link}. " + result["message"]
                    logger.info(f"Successfully extracted coinId {coin_id} from transaction {tx_hash}")
                else:
                    logger.warning(f"Could not extract coinId from transaction {tx_hash}")
                    
            except Exception as e:
                logger.error(f"Error extracting coinId from transaction receipt: {e}")
                # Don't fail the whole transaction if coinId extraction fails
                pass
                
        return result

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
            # Extract required parameters
            name = function_args.get("name")
            symbol = function_args.get("symbol")
            description = function_args.get("description", "")
            image = function_args.get("image", "")
            
            # Validate required parameters
            if not name:
                raise ValueError("Token name is required")
            if not symbol:
                raise ValueError("Token symbol is required")
            
            # Get user ID from context
            user_id = user_context.get("user_id")
            if not user_id:
                raise ValueError("User ID is required for metadata storage")
            
            # Handle image upload to R2 if it's an external URL
            if image and image != self.DEFAULT_IMAGE_URL:
                try:
                    # Upload external image to R2
                    image = await self._upload_external_image_to_r2(image, user_id)
                except ValueError as e:
                    logger.warning(f"Failed to upload external image, using default: {e}")
                    image = self.DEFAULT_IMAGE_URL
            elif not image:
                image = self.DEFAULT_IMAGE_URL
            
            # Create metadata object
            metadata = {
                "name": name,
                "symbol": symbol,
                "description": description,
                "image": image,
            }

            # Store metadata in R2 and get URI
            uri = await self._store_metadata_in_r2(user_id, metadata)
            
            # Store metadata URL for later retrieval in result
            self._current_metadata_url = uri
            
            # Continue with existing launch logic
            creator_supply = function_args.get("creator_supply", "100000000000000000000000000")
            creator_unlock_days = function_args.get("creator_unlock_days", 7.5)
            tranche_coins = function_args.get("tranche_coins", ["150000000000000000000000"])
            tranche_price = function_args.get("tranche_price", ["1000000000000000"])

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
                f"Prepared ZAMM token launch for '{name}' ({symbol}) with URI: {uri}, creator supply: {creator_supply}, unlock: {unlock_date}"
            )
            return [call_data]

        except Exception as e:
            logger.error(f"Error preparing call data for token launch: {e}")
            # Re-raise validation errors for user-friendly handling
            raise e

    async def launch(
        self,
        user_id: str,
        name: str,
        symbol: str,
        description: Optional[str] = "",
        image: Optional[str] = "",
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
            name: Token name
            symbol: Token symbol  
            description: Token description (optional)
            image: Token image URL (optional)
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
                "name": name,
                "symbol": symbol,
                "description": description,
                "image": image,
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
    
    async def update_image(
        self, user_id: str, image_url: str, metadata_url: str
    ) -> Dict[str, Any]:
        """
        Update the image URL in existing token metadata.
        External images will be uploaded to R2 first.

        Args:
            user_id: The user updating the metadata
            image_url: New image URL to set (will be uploaded to R2 if external)
            metadata_url: URL of the metadata file to update

        Returns:
            Dictionary with update result or error
        """
        try:
            # Upload external image to R2 first if it's not already an R2 URL
            r2_image_url = image_url
            if not image_url.startswith(self.R2_ENDPOINT_URL):
                try:
                    r2_image_url = await self._upload_external_image_to_r2(image_url, user_id)
                    logger.info(f"Uploaded external image to R2: {r2_image_url}")
                except ValueError as e:
                    logger.error(f"Failed to upload external image to R2: {e}")
                    return {"error": f"Failed to upload image to R2: {str(e)}"}
            
            # Update metadata with R2 image URL
            updated_metadata = await self._update_metadata_in_r2(metadata_url, r2_image_url, user_id)
            
            return {
                "success": True,
                "message": "Image updated successfully",
                "metadata_url": metadata_url,
                "r2_image_url": r2_image_url,
                "updated_metadata": updated_metadata,
            }
            
        except Exception as e:
            logger.error(f"Error updating image: {e}")
            return {"error": f"Image update failed: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        user_id = self._extract_user_id(session_context.get("api_key") if session_context else None)

        if tool_name == "launch":
            name = function_args.get("name")
            symbol = function_args.get("symbol")
            description = function_args.get("description", "")
            image = function_args.get("image", "")
            creator_supply = function_args.get("creator_supply", "100000000000000000000000000")
            creator_unlock_days = function_args.get("creator_unlock_days", 7.5)
            tranche_coins = function_args.get("tranche_coins")
            tranche_price = function_args.get("tranche_price")
            chain_id = function_args.get("chain_id")

            return await self.launch(
                user_id=user_id,
                name=name,
                symbol=symbol,
                description=description,
                image=image,
                creator_supply=creator_supply,
                creator_unlock_days=creator_unlock_days,
                tranche_coins=tranche_coins,
                tranche_price=tranche_price,
                chain_id=chain_id,
            )

        elif tool_name == "update_image":
            image_url = function_args.get("image_url")
            metadata_url = function_args.get("metadata_url")

            return await self.update_image(
                user_id=user_id,
                image_url=image_url,
                metadata_url=metadata_url,
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"}
