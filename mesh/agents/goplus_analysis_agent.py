import logging
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class GoplusAnalysisAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "GoPlus Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can fetch and analyze security details of blockchain token contracts using GoPlus API.",
                "external_apis": ["GoPlus"],
                "tags": ["Security"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Goplus.png",
                "examples": [
                    "Check the safety of this token: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 on Ethereum",
                    "Analyze the security of this Solana token: AcmFHCquGwbrPxh9b3sUPMtAtXKMjkEzKnqkiHEnpump",
                    "Is 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 safe on ETH mainnet?",
                    "Check the security details of token 0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb on Base chain",
                ],
            }
        )

        self.supported_blockchains = {
            "1": "Ethereum",
            "10": "Optimism",
            "25": "Cronos",
            "56": "BSC",
            "100": "Gnosis",
            "128": "HECO",
            "137": "Polygon",
            "250": "Fantom",
            "321": "KCC",
            "324": "zkSync Era",
            "10001": "ETHW",
            "201022": "FON",
            "42161": "Arbitrum",
            "43114": "Avalanche",
            "59144": "Linea Mainnet",
            "8453": "Base",
            "tron": "Tron",
            "534352": "Scroll",
            "204": "opBNB",
            "5000": "Mantle",
            "42766": "ZKFair",
            "81457": "Blast",
            "169": "Manta Pacific",
            "80085": "Berachain Artio Testnet",
            "4200": "Merlin",
            "200901": "Bitlayer Mainnet",
            "810180": "zkLink Nova",
            "196": "X Layer Mainnet",
            "solana": "Solana",
        }

    def get_system_prompt(self) -> str:
        return f"""You are a blockchain security analyst that provides factual analysis of token contracts based on GoPlus API data.
        1. Extract the contract address and chain ID from the user's query
        2. Use the fetch_security_details tool to get the security data
        3. Risk Assessment: Provide a risk assessment based on the data

        Supported chains: {", ".join([f"{name} (Chain ID: {id})" for id, name in self.supported_blockchains.items()])}

        For most tokens, include these specific details if available:
        - Token Metadata: Name, symbol, description, URI
        - Mintable status and authority
        - Metadata mutability and upgrade authority
        - Freezable status and authority
        - Balance mutability and authority
        - Closable status and authority
        - Default account state
        - Non-transferable status
        - Security Assessment: Analyze authority settings and trusted token status
    """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_security_details",
                    "description": "Fetch security details of a blockchain token contract",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "contract_address": {"type": "string", "description": "The token contract address"},
                            "chain_id": {
                                "type": "string",
                                # hardcoding it so it can be easily picked up by the github action metadata generator
                                "description": "The blockchain chain ID or 'solana' for Solana tokens. Supported chains: Ethereum (1), Optimism (10), Cronos (25), BSC (56), Gnosis (100), HECO (128), Polygon (137), Fantom (250), KCC (321), zkSync Era (324), ETHW (10001), FON (201022), Arbitrum (42161), Avalanche (43114), Linea Mainnet (59144), Base (8453), Tron (tron), Scroll (534352), opBNB (204), Mantle (5000), ZKFair (42766), Blast (81457), Manta Pacific (169), Berachain Artio Testnet (80085), Merlin (4200), Bitlayer Mainnet (200901), zkLink Nova (810180), X Layer Mainnet (196), Solana (solana)",
                                "default": 1,
                            },
                        },
                        "required": ["contract_address"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                      GOPLUS API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_security_details(self, contract_address: str, chain_id: str = "1") -> Dict[str, Any]:
        """
        Fetch security details of a blockchain token contract from GoPlus API.
        """
        logger.info(f"Fetching security details for token: {contract_address} on chain: {chain_id}")

        try:
            # Handle Solana tokens specifically
            if chain_id == "solana":
                return await self._fetch_solana_security_details(contract_address)

            # Standard EVM chain handling
            base_url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
            params = {"contract_addresses": contract_address}
            headers = {"accept": "*/*"}

            response = await self._api_request(url=base_url, method="GET", params=params, headers=headers)

            if "error" in response:
                logger.error(f"Error fetching security details: {response['error']}")
                return {"status": "error", "error": response["error"]}

            # Process the response data
            token_data = response.get("result", {}).get(contract_address.lower(), {})

            if not token_data:
                logger.warning(f"No data found for token: {contract_address} on chain: {chain_id}")
                return {
                    "status": "no_data",
                    "error": f"No data found for token: {contract_address} on chain: {chain_id}",
                }

            essential_security_info = {
                "token_info": {
                    "name": token_data.get("token_name"),
                    "symbol": token_data.get("token_symbol"),
                    "total_supply": token_data.get("total_supply"),
                    "holder_count": token_data.get("holder_count"),
                },
                "security_metrics": {
                    "is_honeypot": bool(int(token_data.get("is_honeypot", "0"))),
                    "is_blacklisted": bool(int(token_data.get("is_blacklisted", "0"))),
                    "is_open_source": bool(int(token_data.get("is_open_source", "0"))),
                    "buy_tax": token_data.get("buy_tax", "0"),
                    "sell_tax": token_data.get("sell_tax", "0"),
                    "can_take_back_ownership": bool(int(token_data.get("can_take_back_ownership", "0"))),
                    "is_proxy": bool(int(token_data.get("is_proxy", "0"))),
                    "is_mintable": bool(int(token_data.get("is_mintable", "0"))),
                },
                "liquidity_info": {
                    "is_in_dex": bool(int(token_data.get("is_in_dex", "0"))),
                    "dex": token_data.get("dex", []),
                    "lp_holder_count": token_data.get("lp_holder_count"),
                },
                "ownership": {
                    "creator_address": token_data.get("creator_address"),
                    "owner_address": token_data.get("owner_address"),
                    "top_holders": token_data.get("holders", [])[:3],
                },
            }

            logger.info(f"Successfully retrieved security details for token: {contract_address}")
            return {"status": "success", "data": essential_security_info}

        except Exception as e:
            logger.error(f"Exception in fetch_security_details: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch security details: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _fetch_solana_security_details(self, contract_address: str) -> Dict[str, Any]:
        """
        Fetch Solana token security details from GoPlus API.
        """
        logger.info(f"Fetching Solana token security details for: {contract_address}")

        try:
            base_url = "https://api.gopluslabs.io/api/v1/solana/token_security"
            params = {"contract_addresses": contract_address}
            headers = {"accept": "*/*"}

            response = await self._api_request(url=base_url, method="GET", params=params, headers=headers)

            if "error" in response:
                logger.error(f"Error fetching Solana token details: {response['error']}")
                return {"status": "error", "error": response["error"]}

            # Process the response data
            token_data = response.get("result", {}).get(contract_address, {})

            if not token_data:
                logger.warning(f"No data found for Solana token: {contract_address}")
                return {"status": "no_data", "error": f"No data found for Solana token: {contract_address}"}

            # Extract metadata
            metadata = token_data.get("metadata", {})

            # Map Solana-specific data structures
            essential_security_info = {
                "token_info": {
                    "name": metadata.get("name"),
                    "symbol": metadata.get("symbol"),
                    "decimals": None,  # Not directly in API response
                    "supply": token_data.get("total_supply"),
                    "holder_count": None,  # Not directly in API response
                    "description": metadata.get("description"),
                    "uri": metadata.get("uri"),
                },
                "solana_specific": {
                    "mint": contract_address,  # Using the provided contract address
                    "default_account_state": token_data.get("default_account_state"),
                    "non_transferable": token_data.get("non_transferable"),
                    # Authority mappings
                    "metadata_mutable": {
                        "status": token_data.get("metadata_mutable", {}).get("status"),
                        "metadata_upgrade_authority": token_data.get("metadata_mutable", {}).get(
                            "metadata_upgrade_authority", []
                        ),
                    },
                    "mintable": {
                        "status": token_data.get("mintable", {}).get("status"),
                        "authority": token_data.get("mintable", {}).get("authority", []),
                    },
                    "freezable": {
                        "status": token_data.get("freezable", {}).get("status"),
                        "authority": token_data.get("freezable", {}).get("authority", []),
                    },
                    "closable": {
                        "status": token_data.get("closable", {}).get("status"),
                        "authority": token_data.get("closable", {}).get("authority", []),
                    },
                    "balance_mutable_authority": {
                        "status": token_data.get("balance_mutable_authority", {}).get("status"),
                        "authority": token_data.get("balance_mutable_authority", {}).get("authority", []),
                    },
                },
                "security_metrics": {
                    "is_verified": False,  # This might be equivalent to trusted_token
                    "is_mintable": token_data.get("mintable", {}).get("status") == "1",
                    "is_freezable": token_data.get("freezable", {}).get("status") == "1",
                    "is_metadata_mutable": token_data.get("metadata_mutable", {}).get("status") == "1",
                    "trusted_token": bool(int(token_data.get("trusted_token", "0"))),
                },
                "ownership": {
                    "creators": token_data.get("creators", []),
                    "metadata_upgrade_authority": token_data.get("metadata_mutable", {}).get(
                        "metadata_upgrade_authority", []
                    ),
                },
            }

            logger.info(f"Successfully retrieved security details for Solana token: {contract_address}")
            return {"status": "success", "data": essential_security_info}

        except Exception as e:
            logger.error(f"Exception in _fetch_solana_security_details: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch Solana token details: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        """
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name != "fetch_security_details":
            logger.error(f"Unsupported tool: {tool_name}")
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        contract_address = function_args.get("contract_address")
        chain_id = function_args.get("chain_id", "1")

        if not contract_address:
            logger.error("Missing 'contract_address' parameter")
            return {"status": "error", "error": "Missing 'contract_address' parameter"}

        if str(chain_id) not in self.supported_blockchains:
            logger.error(f"Unsupported chain ID: {chain_id}")
            return {"status": "error", "error": f"Unsupported chain ID: {chain_id}"}

        logger.info(f"Fetching security details for {contract_address} on chain {chain_id}")
        result = await self.fetch_security_details(contract_address, chain_id)

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
