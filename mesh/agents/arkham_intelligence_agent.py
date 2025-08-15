import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

# Define supported chains in a single place
SUPPORTED_CHAINS = [
    "ethereum",
    "polygon",
    "bsc",
    "optimism",
    "avalanche",
    "arbitrum_one",
    "base",
    "bitcoin",
    "tron",
    "flare",
    "linea",
    "manta",
    "blast",
    "solana",
    "ton",
    "mantle",
    "dogecoin",
    "sonic",
]

# EVM-only chains for contract metadata
EVM_CHAINS = [
    "ethereum",
    "polygon",
    "bsc",
    "optimism",
    "avalanche",
    "arbitrum_one",
    "base",
    "flare",
    "linea",
    "manta",
    "blast",
    "mantle",
]


class ArkhamIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("ARKHAM_INTEL_API_KEY")
        if not self.api_key:
            raise ValueError("ARKHAM_INTEL_API_KEY environment variable is required")

        self.base_url = "https://api.arkm.com"
        self.headers = {
            "API-Key": self.api_key,
            "accept": "application/json",
        }

        # Use the centrally defined supported chains
        self.supported_chains = SUPPORTED_CHAINS

        self.metadata.update(
            {
                "name": "Arkham Intelligence Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides blockchain intelligence using Arkham's API including address analysis, entity identification, portfolio snapshots, and token holder data across 18+ chains",
                "external_apis": ["Arkham Intelligence"],
                "tags": ["Intelligence"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Arkham.png",
                "examples": [
                    "Analyze address 0x742d35Cc6634C0532925a3b8D84c5d146D4B6bb2 on Ethereum",
                    "Get portfolio snapshot for 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                    "Show token holders for USDC on Base",
                    "Check contract metadata for 0x22aF33FE49fD1Fa80c7149773dDe5890D3c76F3b on Base",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a blockchain intelligence assistant that can analyze addresses, entities, portfolios, and token holders across multiple blockchains using Arkham Intelligence data.

        You can provide information about:
        - Address intelligence including entity identification and labels
        - Contract metadata for EVM chains
        - Portfolio snapshots showing token balances and USD values
        - Token holder distributions and top holders

        For portfolio snapshots, if the user specifies a time, convert it to a Unix timestamp in milliseconds (UTC day start). If no time is provided, default to 7 days ago from the current UTC day start.

        If the user's query is out of your scope or references unsupported chains, return a brief error message.
        Format your response in clean text without markdown formatting. Be objective and informative in your analysis.
        Always validate addresses and chain parameters before making API calls."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_address_intelligence",
                    "description": "Get comprehensive intelligence about a blockchain address including entity identification, labels, and classification. Works across all supported chains including Bitcoin, Ethereum, Solana, and others.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "The blockchain address to analyze (can be wallet address, contract address, etc.)",
                            },
                            "chain": {
                                "type": "string",
                                "description": "The blockchain network",
                                "enum": SUPPORTED_CHAINS,
                            },
                        },
                        "required": ["address", "chain"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_contract_metadata",
                    "description": "Get detailed metadata about smart contracts on EVM chains including proxy information, deployer details, and implementation addresses. Only works for EVM-compatible chains (not Bitcoin, Solana, etc.).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "The EVM blockchain network",
                                "enum": EVM_CHAINS,
                            },
                            "address": {
                                "type": "string",
                                "description": "The smart contract address to analyze",
                            },
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_portfolio_snapshot",
                    "description": "Get a complete portfolio snapshot showing all token balances and their USD values across all chains for a given address at a specific point in time. If no time is provided, defaults to 7 days ago from the current UTC day start.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "The address or name of Entity ID to get portfolio data",
                            },
                            "time": {
                                "type": "integer",
                                "description": "Unix timestamp in milliseconds (UTC day start). If not provided, defaults to 7 days ago from the current UTC day start.",
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_holders",
                    "description": "Get the top holders of a specific token, including their balances, USD values, and percentage of total supply. Optionally group results by known entities.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "The blockchain network where the token exists",
                                "enum": SUPPORTED_CHAINS,
                            },
                            "address": {
                                "type": "string",
                                "description": "The token contract address",
                            },
                            "groupByEntity": {
                                "type": "boolean",
                                "description": "Whether to group holders by known entities (e.g., exchanges, institutions)",
                                "default": True,
                            },
                        },
                        "required": ["chain", "address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      ARKHAM API-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_address_intelligence(self, address: str, chain: str) -> Dict[str, Any]:
        """Get intelligence data for a blockchain address."""
        logger.info(f"Getting address intelligence for {address} on {chain}")

        if chain not in SUPPORTED_CHAINS:
            return {"error": f"Unsupported chain: {chain}. Supported chains: {', '.join(SUPPORTED_CHAINS)}"}

        try:
            url = f"{self.base_url}/intelligence/address/{address}"
            params = {"chain": chain}

            result = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in result:
                logger.error(f"Error getting address intelligence: {result['error']}")
                return result

            logger.info(f"Successfully retrieved address intelligence for {address}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Exception in get_address_intelligence: {str(e)}")
            return {"status": "error", "error": f"Failed to get address intelligence: {str(e)}"}

    @with_cache(ttl_seconds=600)  # Cache for 10 minutes (contract data changes rarely)
    @with_retry(max_retries=3)
    async def get_contract_metadata(self, chain: str, address: str) -> Dict[str, Any]:
        """Get contract metadata for EVM chains only."""
        logger.info(f"Getting contract metadata for {address} on {chain}")

        if chain not in EVM_CHAINS:
            return {
                "error": f"Contract metadata only available for EVM chains. {chain} is not supported for this endpoint."
            }

        try:
            url = f"{self.base_url}/intelligence/contract/{chain}/{address}"

            result = await self._api_request(url=url, method="GET", headers=self.headers)

            if "error" in result:
                logger.error(f"Error getting contract metadata: {result['error']}")
                return result

            logger.info(f"Successfully retrieved contract metadata for {address}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Exception in get_contract_metadata: {str(e)}")
            return {"status": "error", "error": f"Failed to get contract metadata: {str(e)}"}

    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def get_portfolio_snapshot(self, address: str, time: Optional[int] = None) -> Dict[str, Any]:
        """Get portfolio snapshot for an address."""
        logger.info(f"Getting portfolio snapshot for {address}")

        try:
            url = f"{self.base_url}/portfolio/address/{address}"
            params = {}
            if time:
                params["time"] = time
            else:
                utc_day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                default_time = int((utc_day_start - timedelta(days=7)).timestamp() * 1000)
                params["time"] = default_time

            result = await self._api_request(url=url, method="GET", headers=self.headers, params=params)

            if "error" in result:
                logger.error(f"Error getting portfolio snapshot: {result['error']}")
                return result

            logger.info(f"Successfully retrieved portfolio snapshot for {address}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Exception in get_portfolio_snapshot: {str(e)}")
            return {"status": "error", "error": f"Failed to get portfolio snapshot: {str(e)}"}

    @with_cache(ttl_seconds=600)  # Cache for 10 minutes
    @with_retry(max_retries=3)
    async def get_token_holders(self, chain: str, address: str, groupByEntity: bool = False) -> Dict[str, Any]:
        """Get token holders data."""
        logger.info(f"Getting token holders for {address} on {chain}")

        if chain not in SUPPORTED_CHAINS:
            return {"error": f"Unsupported chain: {chain}. Supported chains: {', '.join(SUPPORTED_CHAINS)}"}

        try:
            url = f"{self.base_url}/token/holders/{chain}/{address}"
            params = {}
            if groupByEntity:
                params["groupByEntity"] = "true"

            result = await self._api_request(
                url=url, method="GET", headers=self.headers, params=params if params else None
            )

            if "error" in result:
                logger.error(f"Error getting token holders: {result['error']}")
                return result

            # Process the result to clean up the response
            processed_result = self._process_token_holders_response(result)

            logger.info(f"Successfully retrieved and processed token holders for {address}")
            return {"status": "success", "data": processed_result}

        except Exception as e:
            logger.error(f"Exception in get_token_holders: {str(e)}")
            return {"status": "error", "error": f"Failed to get token holders: {str(e)}"}

    def _process_token_holders_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process token holders response to clean up and limit data."""
        try:
            processed_data = {}
            
            # Copy token information if it exists
            if "token" in data:
                processed_data["token"] = data["token"]
            
            # Copy total supply if it exists
            if "totalSupply" in data:
                processed_data["totalSupply"] = data["totalSupply"]
            
            # Process addressTopHolders - limit to 20 items
            if "addressTopHolders" in data and isinstance(data["addressTopHolders"], dict):
                processed_data["addressTopHolders"] = {}
                for chain, holders in data["addressTopHolders"].items():
                    if isinstance(holders, list):
                        # Limit to first 20 holders
                        processed_data["addressTopHolders"][chain] = holders[:20]
            
            # Process entityTopHolders - only keep name and type fields
            if "entityTopHolders" in data and isinstance(data["entityTopHolders"], dict):
                processed_data["entityTopHolders"] = {}
                for chain, entities in data["entityTopHolders"].items():
                    if isinstance(entities, list):
                        processed_entities = []
                        for entity_holder in entities:
                            if isinstance(entity_holder, dict) and "entity" in entity_holder:
                                entity = entity_holder.get("entity", {})
                                # Only keep name and type fields
                                cleaned_entity = {
                                    "entity": {
                                        "name": entity.get("name", "Unknown"),
                                        "type": entity.get("type", "Unknown")
                                    }
                                }
                                # Copy other fields from entity_holder if they exist
                                for key in ["balance", "usd", "pctOfCap"]:
                                    if key in entity_holder:
                                        cleaned_entity[key] = entity_holder[key]
                                processed_entities.append(cleaned_entity)
                        processed_data["entityTopHolders"][chain] = processed_entities
            
            return processed_data
            
        except Exception as e:
            logger.warning(f"Error processing token holders response: {str(e)}")
            # Return original data if processing fails
            return data

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle Arkham Intelligence tool calls."""
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_address_intelligence":
            address = function_args.get("address")
            chain = function_args.get("chain")

            if not address or not chain:
                return {"error": "Both 'address' and 'chain' are required parameters"}

            result = await self.get_address_intelligence(address, chain)

        elif tool_name == "get_contract_metadata":
            chain = function_args.get("chain")
            address = function_args.get("address")

            if not chain or not address:
                return {"error": "Both 'chain' and 'address' are required parameters"}

            result = await self.get_contract_metadata(chain, address)

        elif tool_name == "get_portfolio_snapshot":
            address = function_args.get("address")
            time = function_args.get("time")

            if not address:
                return {"error": "Address parameter is required"}

            result = await self.get_portfolio_snapshot(address, time)

        elif tool_name == "get_token_holders":
            chain = function_args.get("chain")
            address = function_args.get("address")
            groupByEntity = function_args.get("groupByEntity", False)

            if not chain or not address:
                return {"error": "Both 'chain' and 'address' are required parameters"}

            result = await self.get_token_holders(chain, address, groupByEntity)

        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
