import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from ens import ENS
from web3 import Web3

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class ChainbaseAddressLabelAgent(MeshAgent):
    def __init__(self):
        super().__init__()

        self.api_key = os.getenv("CHAINBASE_API_KEY")
        if not self.api_key:
            raise ValueError("CHAINBASE_API_KEY environment variable is required")

        self.headers = {
            "x-api-key": self.api_key,
            "accept": "application/json",
        }

        self.w3 = Web3(Web3.HTTPProvider("https://eth.llamarpc.com"))
        self.ens_resolver = ENS.from_web3(self.w3)

        self.metadata.update(
            {
                "name": "Chainbase Address Label Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Get all available labels for an ETH or Base address. Labels include owner identity, smart contract name, wallet behavior patterns and other properties. Also resolves ENS and Base names.",
                "external_apis": ["Chainbase"],
                "tags": ["Blockchain", "Identity"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Chainbase.png",
                "examples": [
                    "Get labels for address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
                    "What is the owner of 0x2211d1D0020DAEA8039E46Cf1367962070d77DA9?",
                    "Get information about vitalik.eth address",
                ],
                "credits": 2,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                },
            }
        )

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 10

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that can access Chainbase API to provide address labels for Ethereum and Base blockchain addresses.
        You can get labels that describe owner identity, smart contract names, wallet behavior patterns, and also resolve ENS and Base names.
        If the user provides an ENS name like 'vitalik.eth', let them know they need to provide the 0x address instead.
        Format your response in clean text. Be objective and informative."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_address_labels",
                    "description": "Get all available labels for an ETH or Base 0x address. Labels may describe owner identity, smart contract name, wallet behavior patterns and other properties. Also resolves ENS and Base names if available.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "The 0x address to get labels for (e.g., 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045)",
                            },
                        },
                        "required": ["address"],
                    },
                },
            }
        ]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _resolve_ens_name(self, address: str) -> Optional[str]:
        """Resolve ENS or Base name for an address using web3+ens library."""
        try:
            name = self.ens_resolver.name(address)
            return name
        except Exception:
            return None

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def _fetch_chainbase_labels(self, address: str, chain_id: int) -> Dict[str, Any]:
        """Fetch address labels from Chainbase API for a specific chain."""
        url = "https://api.chainbase.online/v1/address/labels"
        params = {"chain_id": chain_id, "address": address}

        try:
            response = await self._api_request(url=url, method="GET", headers=self.headers, params=params)
            if not isinstance(response, dict):
                logger.error(f"Chainbase API returned non-dict: {type(response).__name__}, value: {response}")
                return {"error": f"Invalid response type from Chainbase API: {type(response).__name__}"}
            logger.debug(f"Chainbase API response for chain {chain_id}: {response}")
            return response
        except Exception as e:
            logger.error(f"Chainbase API exception for chain {chain_id}: {e}")
            return {"error": f"Chainbase API error for chain {chain_id}: {e}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def get_address_labels(self, address: str) -> Dict[str, Any]:
        """Get address labels from both Ethereum and Base chains, plus ENS/Base name resolution."""
        if not address or not address.startswith("0x"):
            return {"error": "Invalid address format. Address must start with 0x"}

        eth_task = self._fetch_chainbase_labels(address, 1)
        base_task = self._fetch_chainbase_labels(address, 8453)
        ens_task = self._resolve_ens_name(address)

        eth_result, base_result, ens_name = await asyncio.gather(eth_task, base_task, ens_task)

        logger.debug(f"ETH result type: {type(eth_result).__name__}, value: {eth_result}")
        logger.debug(f"Base result type: {type(base_result).__name__}, value: {base_result}")

        labels = []

        if isinstance(eth_result, dict) and "error" not in eth_result:
            data = eth_result.get("data")
            if isinstance(data, dict):
                label = self._extract_label_fields(data, address, "ethereum")
                if label:
                    labels.append(label)

        if isinstance(base_result, dict) and "error" not in base_result:
            data = base_result.get("data")
            if isinstance(data, dict):
                label = self._extract_label_fields(data, address, "base")
                if label:
                    labels.append(label)

        if not labels:
            return {"error": "No labels found for this address on Ethereum or Base"}

        result = {"address": address, "labels": labels}

        if ens_name:
            result["ens"] = ens_name

        return result

    def _extract_label_fields(self, data: Dict[str, Any], address: str, blockchain: str) -> Optional[Dict[str, Any]]:
        """Extract category and tag information from Chainbase API response."""
        address_key = address.lower()
        category_tags = data.get(address_key)

        if not category_tags or not isinstance(category_tags, list):
            logger.warning(f"No label data found for {address} on {blockchain}")
            return None

        label = {"blockchain": blockchain, address_key: category_tags}
        return label

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle address label tool logic."""
        if tool_name != "get_address_labels":
            return {"error": f"Unsupported tool '{tool_name}'"}

        address = function_args.get("address")
        if not address:
            return {"error": "Address parameter is required"}

        result = await self.get_address_labels(address)

        if errors := self._handle_error(result):
            return errors

        return {"address_labels": result}
