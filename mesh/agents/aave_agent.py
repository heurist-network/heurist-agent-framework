import json
import logging
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv
from eth_defi.aave_v3.reserve import AaveContractsNotConfigured, fetch_reserve_data, get_helper_contracts
from web3 import Web3

from core.llm import call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class AaveAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.session = None
        self.metadata.update(
            {
                "name": "Aave Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can report the status of Aave v3 protocols deployed on Ethereum, Polygon, Avalanche, and Arbitrum with details on liquidity, borrowing rates, and more",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about Aave reserves",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw data without LLM explanation",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "The explanation of Aave reserve data",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured Aave reserve data", "type": "dict"},
                ],
                "external_apis": ["Aave"],
                "tags": ["DeFi", "Lending"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Aave.png",
                "examples": [
                    "What is the current borrow rate for USDC on Polygon?",
                    "Show me all assets on Ethereum with their lending and borrowing rates",
                    "Available liquidity for ETH on Arbitrum",
                ],
            }
        )

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

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
    def _initialize_web3(self, chain_id: int = 137):
        """
        Initialize Web3 connection for the specified chain.

        Args:
            chain_id: Blockchain network ID (default: 137 for Polygon)

        Returns:
            Web3 instance connected to the appropriate RPC
        """
        # handle string chain_id
        if isinstance(chain_id, str):
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

        if chain_id not in rpc_urls:
            raise ValueError(f"Chain ID {chain_id} not supported or RPC URL not configured")

        rpc_url = rpc_urls[chain_id]

        request_kwargs = {
            "timeout": 60,
            "headers": {"Content-Type": "application/json", "User-Agent": "AaveReserveAgent/1.0.0"},
        }

        w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs=request_kwargs))

        if not w3.is_connected():
            raise ConnectionError(f"Failed to connect to RPC for chain ID {chain_id}")

        return w3

    def _initialize_aave_contracts(self, web3: Web3):
        """
        Initialize Aave helper contracts for the connected Web3 instance.
        Args:
            web3: Connected Web3 instance
        Returns:
            Aave helper contracts
        """
        try:
            return get_helper_contracts(web3)
        except AaveContractsNotConfigured as e:
            chain_id = web3.eth.chain_id
            raise RuntimeError(f"Aave v3 not supported on chain ID {chain_id}") from e

    def _process_reserve(self, reserve: Dict) -> Dict:
        """
        Process reserve data for better readability and API compatibility.

        Args:
            reserve: Raw reserve data

        Returns:
            Processed reserve data with friendlier format
        """
        processed = {}
        for key, value in reserve.items():
            if isinstance(value, int) and abs(value) > 2**53 - 1:
                processed[key] = str(value)
            else:
                processed[key] = value

        if "variableBorrowRate" in reserve:
            apr = float(reserve["variableBorrowRate"]) / 1e25
            processed["variableBorrowAPR"] = round(apr, 2)

        if "liquidityRate" in reserve:
            apr = float(reserve["liquidityRate"]) / 1e25
            processed["depositAPR"] = round(apr, 2)

        return processed

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_aave_reserves(
        self, chain_id: int = 137, block_identifier: str = None, asset_filter: str = None
    ) -> Dict:
        """
        Fetch Aave reserve data asynchronously.

        Args:
            chain_id: Blockchain network ID
            block_identifier: Optional block number or hash for historical data
            asset_filter: Optional asset symbol to filter results

        Returns:
            Dictionary with reserve data and base currency info
        """
        try:
            block_id = None
            if block_identifier:
                try:
                    block_id = int(block_identifier)
                except ValueError:
                    block_id = block_identifier
            web3 = self._initialize_web3(chain_id)
            helper_contracts = self._initialize_aave_contracts(web3)

            if chain_id == 1:  # Ethereum mainnet
                web3.eth.default_block_identifier = "latest"
                logger.info("Using latest block for Ethereum mainnet query")

            try:
                raw_reserves, base_currency = fetch_reserve_data(helper_contracts, block_identifier=block_id)
            except Exception as contract_error:
                logger.error(f"Contract error when fetching reserve data: {str(contract_error)}")

                # for demonstration, fall back to Polygon data if Ethereum fails
                if chain_id == 1:
                    logger.info("Ethereum query failed, falling back to Polygon data")
                    fallback_message = (
                        "Ethereum data temporarily unavailable. Consider using Polygon network data instead."
                    )
                    return {"error": fallback_message}
                else:
                    raise

            processed_reserves = {}
            for reserve in raw_reserves:
                symbol = reserve.get("symbol", "").upper()
                if asset_filter and asset_filter.upper() != symbol:
                    continue

                asset_address = reserve["underlyingAsset"].lower()
                processed_reserves[asset_address] = self._process_reserve(reserve)

            processed_base_currency = {
                "marketReferenceCurrencyUnit": str(base_currency["marketReferenceCurrencyUnit"]),
                "marketReferenceCurrencyPriceInUsd": str(base_currency["marketReferenceCurrencyPriceInUsd"]),
                "networkBaseTokenPriceInUsd": str(base_currency["networkBaseTokenPriceInUsd"]),
            }

            return {
                "reserves": processed_reserves,
                "base_currency": processed_base_currency,
                "chain_id": chain_id,
                "total_reserves": len(processed_reserves),
            }

        except Exception as e:
            logger.error(f"Error fetching Aave reserves: {str(e)}")
            return {"error": f"Failed to fetch Aave reserves: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle tool execution without LLM"""
        if tool_name != "get_aave_reserves":
            return {"error": f"Unsupported tool '{tool_name}'"}

        chain_id = function_args.get("chain_id", 137)
        block_identifier = function_args.get("block_identifier")
        asset_filter = function_args.get("asset_filter")

        logger.info(f"Getting Aave reserves for chain ID {chain_id}")
        result = await self.get_aave_reserves(
            chain_id=chain_id, block_identifier=block_identifier, asset_filter=asset_filter
        )

        errors = self._handle_error(result)
        if errors:
            return errors

        return {
            "reserve_data": {
                "chain_id": chain_id,
                "reserves": result["reserves"],
                "base_currency": result["base_currency"],
                "total_reserves": result["total_reserves"],
            }
        }

    # ------------------------------------------------------------------------
    #                      MAIN HANDLER
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Either 'query' or 'tool' is required in params.
          - If 'tool' is provided, call that tool directly with 'tool_arguments' (bypassing the LLM).
          - If 'query' is provided, route via LLM for dynamic tool selection.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            data = await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
            )
            return {"response": "", "data": data}

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY (LLM decides the tool)
        # ---------------------
        if query:
            response = await call_llm_with_tools_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                user_prompt=query,
                temperature=0.1,
                tools=self.get_tool_schemas(),
            )

            if not response:
                return {"error": "Failed to process query"}
            if not response.get("tool_calls"):
                return {"response": response["content"], "data": {}}

            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            data = await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
            )

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await super()._respond_with_llm(
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                query=query,
                tool_call_id=tool_call.id,
                data=data,
                temperature=0.1,
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
