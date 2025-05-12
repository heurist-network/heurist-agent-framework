import logging
from typing import Any, Dict, List, Optional

from eth_defi.aave_v3.reserve import AaveContractsNotConfigured, fetch_reserve_data, get_helper_contracts
from web3 import Web3

from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class AaveAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Aave Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can report the status of Aave v3 protocols deployed on Ethereum, Polygon, Avalanche, and Arbitrum with details on liquidity, borrowing rates, and more",
                "external_apis": ["Aave"],
                "tags": ["DeFi"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Aave.png",
                "examples": [
                    "What is the current borrow rate for USDC on Polygon?",
                    "Show me all assets on Ethereum with their lending and borrowing rates",
                    "Available liquidity for ETH on Arbitrum",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that can access external tools to provide Aave v3 reserve data.
        You can provide information about liquidity pools, including deposit/borrow rates, total liquidity, utilization,
        and other important metrics for DeFi users and analysts.
        You currently have access to Aave v3 data on supported chains like Polygon, Ethereum, Avalanche, and others.
        If the user's query is out of your scope, return a brief error message.
        If the tool call successfully returns the data, explain the key metrics in a concise manner,
        focusing on the most relevant information for liquidity providers and borrowers.
        Output in CLEAN text format with no markdown or other formatting."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_aave_reserves",
                    "description": "Get Aave v3 reserve data including liquidity, rates, and asset information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain_id": {
                                "type": "number",
                                "description": "Blockchain network ID (137=Polygon, 1=Ethereum, 43114=Avalanche C-Chain, 42161=Arbitrum One.)",
                                "enum": [1, 137, 43114, 42161],
                            },
                            "block_identifier": {
                                "type": "string",
                                "description": "Optional block number or hash for historical data",
                            },
                            "asset_filter": {
                                "type": "string",
                                "description": "Optional filter to get data for a specific asset symbol (e.g., 'USDC')",
                            },
                        },
                        "required": ["chain_id"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                      AAVE API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    def _initialize_web3(self, chain_id: int = 137) -> Web3:
        """Initialize Web3 connection for a supported chain."""
        try:
            chain_id = int(chain_id)
        except ValueError:
            raise ValueError(f"Invalid chain ID format: {chain_id}")

        rpc_urls = {
            1: "https://rpc.ankr.com/eth",
            137: "https://polygon-rpc.com",
            43114: "https://api.avax.network/ext/bc/C/rpc",
            42161: "https://arb1.arbitrum.io/rpc",
        }

        rpc_url = rpc_urls.get(chain_id)
        if not rpc_url:
            raise ValueError(f"Unsupported chain ID: {chain_id}")

        w3 = Web3(
            Web3.HTTPProvider(
                rpc_url,
                request_kwargs={
                    "timeout": 60,
                    "headers": {
                        "Content-Type": "application/json",
                        "User-Agent": "AaveReserveAgent/1.0.0",
                    },
                },
            )
        )

        if not w3.is_connected():
            raise ConnectionError(f"Web3 failed to connect for chain ID {chain_id}")

        return w3

    def _initialize_aave_contracts(self, web3: Web3):
        """Initialize Aave contracts for a given Web3 instance."""
        try:
            return get_helper_contracts(web3)
        except AaveContractsNotConfigured as e:
            raise RuntimeError(f"Aave v3 not supported on chain ID {web3.eth.chain_id}") from e

    def _process_reserve(self, reserve: Dict) -> Dict:
        result = {k: str(v) if isinstance(v, int) and abs(v) > 2**53 - 1 else v for k, v in reserve.items()}

        if "variableBorrowRate" in reserve:
            result["variableBorrowAPR"] = round(float(reserve["variableBorrowRate"]) / 1e25, 2)

        if "liquidityRate" in reserve:
            result["depositAPR"] = round(float(reserve["liquidityRate"]) / 1e25, 2)

        return result

    async def get_aave_reserves(
        self, chain_id: int = 137, block_identifier: str = None, asset_filter: str = None
    ) -> Dict:
        """Fetch and process Aave reserve data."""
        # Could use self._api_request() from base class instead of implementing web3 calls
        try:
            block_id = int(block_identifier) if block_identifier and block_identifier.isdigit() else block_identifier
            web3 = self._initialize_web3(chain_id)
            if chain_id == 1:
                web3.eth.default_block_identifier = "latest"
                logger.info("Using latest block for Ethereum mainnet")

            helper_contracts = self._initialize_aave_contracts(web3)

            try:
                raw_reserves, base_currency = fetch_reserve_data(helper_contracts, block_identifier=block_id)
            except Exception as e:
                logger.error(f"Contract fetch error: {e}")
                if chain_id == 1:
                    logger.info("Fallback to Polygon due to Ethereum failure")
                    return {"error": "Ethereum data unavailable. Try Polygon instead."}
                raise

            processed_reserves = {
                reserve["underlyingAsset"].lower(): self._process_reserve(reserve)
                for reserve in raw_reserves
                if not asset_filter or reserve.get("symbol", "").upper() == asset_filter.upper()
            }

            return {
                "reserves": processed_reserves,
                "base_currency": {
                    k: str(v)
                    for k, v in base_currency.items()
                    if k
                    in {
                        "marketReferenceCurrencyUnit",
                        "marketReferenceCurrencyPriceInUsd",
                        "networkBaseTokenPriceInUsd",
                    }
                },
                "chain_id": chain_id,
                "total_reserves": len(processed_reserves),
            }

        except Exception as e:
            logger.error(f"Aave reserve fetch error: {e}")
            return {"error": f"Failed to fetch Aave reserves: {e}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle supported Aave tool logic."""
        if tool_name != "get_aave_reserves":
            return {"error": f"Unsupported tool '{tool_name}'"}

        chain_id = function_args.get("chain_id", 137)
        block_identifier = function_args.get("block_identifier")
        asset_filter = function_args.get("asset_filter")

        logger.info(f"Fetching Aave reserves (chain_id={chain_id})")
        result = await self.get_aave_reserves(chain_id, block_identifier, asset_filter)

        if errors := self._handle_error(result):
            return errors

        return {
            "reserve_data": {
                "chain_id": chain_id,
                "reserves": result["reserves"],
                "base_currency": result["base_currency"],
                "total_reserves": result["total_reserves"],
            }
        }
