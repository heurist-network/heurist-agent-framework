import logging
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class DexScreenerTokenInfoAgent(MeshAgent):
    """
    An agent that integrates with DexScreener API to fetch real-time DEX trading data
    and token information across multiple chains.
    """

    def __init__(self):
        super().__init__()

        self.metadata.update(
            {
                "name": "DexScreener Agent",
                "version": "1.0.0",
                "author": "Scattering team",
                "author_address": "0xa7DeBb68F2684074Ec4354B68E36C34AF363Fd57",
                "description": "This agent fetches real-time DEX trading data and token information across multiple chains using DexScreener API",
                "external_apis": ["DexScreener"],
                "tags": ["Trading"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Dexscreener.png",
                "examples": [
                    "Show me information about UNI on Uniswap",
                    "Recent price movement for HEU",
                    "Recent trading activity for TRUMP token on Solana?",
                    "Analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN on Solana",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You are DexScreener Assistant, a professional analyst providing concise token/trading pair information.\n\n"
            "Response Protocol:\n"
            "   - Decimals for price: 2-4 significant figures\n"
            "   - URLs: https://dexscreener.com/{chain}/{address}\n"
            "   - Percentages: Keep two decimal places like 5.25% format\n"
            "   - Do not use markdown formatting unless requested\n"
            "Exception Handling:\n"
            "When the requested data cannot be retrieved, strictly follow the process below:\n"
            "1. Confirm the validity of the base contract address.\n"
            "2. Check the corresponding chain's trading pairs.\n"
            "3. If no data is ultimately found, return:\n"
            "No on-chain data for [Token Symbol] was found at this time. Please verify the validity of the contract address.\n\n"
        )

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_pairs",
                    "description": "Search for trading pairs on decentralized exchanges by token name, symbol, or address. This tool helps you find specific trading pairs across multiple DEXs and blockchains. It returns information about the pairs including price, volume, liquidity, and the exchanges where they're available. Data comes from DexScreener and covers major DEXs on most blockchains. The search results may be incomplete if the token is not traded on any of the supported chains.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "Search term (token name, symbol, or address)",
                            }
                        },
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_specific_pair_info",
                    "description": "Get detailed information about a specific trading pair on a decentralized exchange by chain and pair address. This tool provides comprehensive data about a DEX trading pair including current price, 24h volume, liquidity, price changes, and trading history. Data comes from DexScreener and is updated in real-time. You must specify both the blockchain and the exact pair contract address. The pair address is the LP contract address, not the quote token address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain identifier (e.g., solana, bsc, ethereum, base)",
                            },
                            "pair_address": {"type": "string", "description": "The pair contract address to look up"},
                        },
                        "required": ["chain", "pair_address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_pairs",
                    "description": "Get all trading pairs for a specific token across decentralized exchanges by chain and token address. This tool retrieves a comprehensive list of all DEX pairs where the specified token is traded on a particular blockchain. It provides data on each pair including the paired token, exchange, price, volume, and liquidity. Data comes from DexScreener and is updated in real-time. You must specify both the blockchain and the exact token contract address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain identifier (e.g., solana, bsc, ethereum, base)",
                            },
                            "token_address": {
                                "type": "string",
                                "description": "The token contract address to look up all pairs for",
                            },
                        },
                        "required": ["chain", "token_address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      DEXSCREENER API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_pairs(self, search_term: str) -> Dict:
        """
        Search for trading pairs (up to 30) using DexScreener API.
        """
        logger.info(f"Searching pairs with term: {search_term}")

        url = f"https://api.dexscreener.com/latest/dex/search?q={search_term}"
        result = await self._api_request(url=url)

        if "error" in result:
            logger.error(f"Error searching pairs: {result['error']}")
            return result

        if "pairs" in result and result["pairs"]:
            logger.info(f"Found {len(result['pairs'])} pairs for search term: {search_term}")
            return {"status": "success", "data": {"pairs": result["pairs"]}}
        else:
            logger.warning(f"No pairs found for search term: {search_term}")
            return {"status": "no_data", "error": "No matching pairs found", "data": {"pairs": []}}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_specific_pair_info(self, chain: str, pair_address: str) -> Dict:
        """
        Get detailed information for a specific trading pair.
        """
        logger.info(f"Getting pair info for chain: {chain}, pair address: {pair_address}")

        url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}"
        result = await self._api_request(url=url)

        if "error" in result:
            logger.error(f"Error getting pair info: {result['error']}")
            return result

        if "pairs" in result and result["pairs"] and len(result["pairs"]) > 0:
            logger.info(f"Found pair info for chain: {chain}, pair address: {pair_address}")
            return {"status": "success", "data": {"pair": result["pairs"][0]}}
        else:
            logger.warning(f"No pair found for chain: {chain}, pair address: {pair_address}")
            return {"status": "no_data", "error": "No matching pair found", "data": None}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_token_pairs(self, chain: str, token_address: str) -> Dict:
        """
        Get trading pairs (up to 30) for a specific token on a chain.
        """
        logger.info(f"Getting token pairs for chain: {chain}, token address: {token_address}")

        url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
        result = await self._api_request(url=url)

        if "error" in result:
            logger.error(f"Error getting token pairs: {result['error']}")
            return result

        if "pairs" in result and result["pairs"]:
            if chain and chain.lower() != "all":
                pairs = [pair for pair in result["pairs"] if pair.get("chainId") == chain.lower()]
            else:
                pairs = result["pairs"]

            if pairs:
                logger.info(f"Found {len(pairs)} pairs for token on chain: {chain}")
                return {
                    "status": "success",
                    "data": {"pairs": pairs, "dex_url": f"https://dexscreener.com/{chain}/{token_address}"},
                }
            else:
                logger.warning(f"No pairs found for token on chain: {chain}")
                return {
                    "status": "no_data",
                    "error": f"No pairs found for token on chain {chain}",
                    "data": {"pairs": []},
                }
        else:
            logger.warning(f"No pairs found for token address: {token_address}")
            return {"status": "no_data", "error": "No pairs found for token", "data": {"pairs": []}}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return raw data.
        """
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "search_pairs":
            search_term = function_args.get("search_term")
            if not search_term:
                return {"error": "Missing 'search_term' parameter"}

            result = await self.search_pairs(search_term)

        elif tool_name == "get_specific_pair_info":
            chain = function_args.get("chain")
            pair_address = function_args.get("pair_address")

            if not chain:
                return {"error": "Missing 'chain' parameter"}
            if not pair_address:
                return {"error": "Missing 'pair_address' parameter"}

            result = await self.get_specific_pair_info(chain, pair_address)

        elif tool_name == "get_token_pairs":
            chain = function_args.get("chain")
            token_address = function_args.get("token_address")

            if not chain:
                return {"error": "Missing 'chain' parameter"}
            if not token_address:
                return {"error": "Missing 'token_address' parameter"}

            result = await self.get_token_pairs(chain, token_address)

        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        if errors := self._handle_error(result):
            return errors

        return result
