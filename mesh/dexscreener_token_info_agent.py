import json
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

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
                "name": "DexScreener Token Info Agent",
                "version": "1.0.0",
                "author": "dyt9qc",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "created_at": "2025-02-13 07:43:15",
                "description": "This agent fetches real-time DEX trading data and token information across multiple chains using DexScreener API",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Search query for token name, symbol or address",
                        "type": "str",
                        "required": True,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, return only raw data without natural language response",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of token/pair data",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured token/pair data from DexScreener", "type": "dict"},
                ],
                "external_apis": ["DexScreener"],
                "tags": ["DeFi", "Trading", "Multi-chain", "DEX"],
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You are DexScreener Assistant, a professional analyst providing concise token/pair information.\n\n"
            "Strict Data Presentation Rules:\n"
            "1. OMIT ENTIRE SECTIONS if no data exists for that category\n"
            "2. NEVER show 'Not Provided' or similar placeholders\n"
            "3. If only partial data exists, show ONLY available fields\n\n"
            "Data Presentation Hierarchy:\n"
            "[Only display sections with available data]\n"
            "Core Token Information (Mandatory if available):\n"
            "   - Base/Quote token names, symbols and addresses\n"
            "   - Chain/DEX platform\n"
            "   - Contract addresses (full format)\n\n"
            "Market Metrics (Conditional):\n"
            "   - Price (USD and native token)\n"
            "   - 24h Volume\n"
            "   - Liquidity\n"
            "   - Market Cap/FDV\n\n"
            "Trading Activity (Conditional):\n"
            "   - Price change (24h)\n"
            "   - Volume distribution\n"
            "   - Transaction ratio (24h Buy/Sell)\n\n"
            "Project Links (Conditional):\n"
            "   - Website\n"
            "   - Social media links\n"
            "Response Protocol:\n"
            "1. STRUCTURED OMISSION: If a main category has no data, exclude its entire section\n"
            "2. PRECISION FORMAT:\n"
            "   - Decimals: 2-4 significant figures\n"
            "   - URLs: https://dexscreener.com/{chain}/{address}\n"
            "   - Percentages: 5.25% format\n"
            "3. DENSITY CONTROL:\n"
            "   - 1 token info = ~200 words\n"
            "   - Multi-token = tabular comparison\n\n"
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
                    "description": "Search for trading pairs by token name, symbol, or address",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "Search term (token name, symbol, or address)"}
                        },
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_specific_pair_info",
                    "description": "Get pair info by chain and pair address",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain identifier (e.g., solana, bsc, ethereum)",
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
                    "description": "Get the trading pairs by chain and token address",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain identifier (e.g., solana, bsc, ethereum)",
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
            {
                "type": "function",
                "function": {
                    "name": "get_token_profiles",
                    "description": "Get the latest token profiles from DexScreener",
                },
            },
        ]
    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    async def _respond_with_llm(self, query: str, tool_call_id: str, data: dict, temperature: float) -> str:
        """
        Reusable helper to ask the LLM to generate a user-friendly explanation
        given a piece of data from a tool call.
        """
        return await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query},
                {"role": "tool", "content": str(data), "tool_call_id": tool_call_id},
            ],
            temperature=temperature,
        )

    def _handle_error(self, maybe_error: dict) -> dict:
        """
        Small helper to return the error if present in
        a dictionary with the 'error' key.
        """
        if "error" in maybe_error:
            return {"error": maybe_error["error"]}
        return {}

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    async def search_pairs(self, search_term: str) -> Dict:
        """
        Search for trading pairs (up to 30) using DexScreener API.

        Args:
            search_term (str): Search term for token name, symbol, or address

        Returns:
            Dict: Top 30 matching pairs with status information
        """
        try:
            result = fetch_dex_pairs(search_term)

            if result["status"] == "success":
                return {
                    "status": "success",
                    "data": {
                        "pairs": result["pairs"],
                    },
                }

            return {"status": result["status"], "error": result.get("error", "Unknown error occurred"), "data": None}

        except Exception as e:
            return {"status": "error", "error": f"Failed to search pairs: {str(e)}", "data": None}


    @with_cache(ttl_seconds=300)
    async def get_specific_pair_info(self, chain: str, pair_address: str) -> Dict:
        """
        Get detailed information for a specific trading pair.

        Args:
            chain (str): Chain identifier (e.g., solana, bsc, ethereum)
            pair_address (str): The pair contract address to look up

        Returns:
            Dict: Detailed pair information with status
        """
        try:
            result = fetch_pair_info(chain, pair_address)

            if result["status"] == "success":
                if result.get("pair"):
                    return {
                        "status": "success",
                        "data": {
                            "pair": result["pair"],
                        },
                    }
                return {"status": "no_data", "error": "No matching pair found", "data": None}

            return {"status": "error", "error": result.get("error", "Unknown error occurred"), "data": None}

        except Exception as e:
            return {"status": "error", "error": f"Failed to get pair info: {str(e)}", "data": None}

    @with_cache(ttl_seconds=300)
    async def get_token_pairs(self, chain: str, token_address: str) -> Dict:
        """
        Get trading pairs (up to 30) for a specific token on a chain.

        Args:
            chain (str): Chain identifier (e.g., solana, bsc, ethereum)
            token_address (str): Token contract address

        Returns:
            Dict: Top 30 trading pairs for the token with status
        """
        try:
            result = fetch_token_pairs(chain, token_address)

            if result["status"] == "success":
                return {
                    "status": "success",
                    "data": {"pairs": result["pairs"], "dex_url": f"https://dexscreener.com/{chain}/{token_address}"},
                }

            return {"status": result["status"], "error": result.get("error", "Unknown error occurred"), "data": None}

        except Exception as e:
            return {"status": "error", "error": f"Failed to get token pairs: {str(e)}", "data": None}

    @with_cache(ttl_seconds=300)
    async def get_token_profiles(self) -> Dict:
        """
        Get the latest token profiles from DexScreener.

        Returns:
            Dict: Latest token profiles with status
        """
        try:
            result = fetch_token_profiles()

            if result["status"] == "success":
                return {"status": "success", "data": {"profiles": result["profiles"]}}

            return {"status": result["status"], "error": result.get("error", "Unknown error occurred"), "data": None}

        except Exception as e:
            return {"status": "error", "error": f"Failed to get token profiles: {str(e)}", "data": None}

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
    ) -> Dict[str, Any]:
        """
        A single method that calls the appropriate function, handles
        errors/formatting, and optionally calls the LLM to explain the result.
        """
        temp = 0.3 if tool_name == "get_token_profiles" else 0.7

        if tool_name == "search_pairs":
            result_data = await self.search_pairs(function_args["search_term"])
        elif tool_name == "get_specific_pair_info":
            result_data = await self.get_specific_pair_info(
                chain=function_args["chain"], pair_address=function_args["pair_address"]
            )
        elif tool_name == "get_token_pairs":
            result_data = await self.get_token_pairs(
                chain=function_args["chain"], token_address=function_args["token_address"]
            )
        elif tool_name == "get_token_profiles":
            result_data = await self.get_token_profiles()
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result_data)
        if errors:
            return errors

        if raw_data_only:
            return {"response": "", "data": result_data}

        explanation = await self._respond_with_llm(
            query=query, tool_call_id=tool_call_id, data=result_data, temperature=temp
        )

        return {"response": explanation, "data": result_data}

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
            return await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
                query=query or "Direct tool call without LLM.",
                tool_call_id="direct_tool",
                raw_data_only=raw_data_only,
            )

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
                # No tool calls => the LLM just answered
                return {"response": response["content"], "data": {}}

            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            return await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
                query=query,
                tool_call_id=tool_call.id,
                raw_data_only=raw_data_only,
            )

        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}


# ------------------------- Helper Functions ------------------------- #


def fetch_dex_pairs(search_term: str) -> Dict:
    """
    Fetches trading pair information from DexScreener API.

    Args:
        search_term (str): Search term (token name, symbol, or address)

    Returns:
        Dict: Processed pair information with status
    """
    try:
        response = requests.get(
            f"https://api.dexscreener.com/latest/dex/search/?q={search_term}",
            headers={},
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "error": f"Query failed with status code {response.status_code}: {response.text}",
            }

        data = response.json()

        if not data.get("pairs"):
            return {"status": "no_data", "error": "No pairs found for this query"}

        # Limit the number of pairs
        limit = 5
        pairs = data["pairs"][:limit] if len(data["pairs"]) > limit else data["pairs"]

        return {"status": "success", "pairs": pairs}

    except Exception as e:
        return {"status": "error", "error": f"Failed to fetch pairs: {str(e)}"}

def fetch_pair_info(chain: str, pair_address: str) -> Dict:
    """
    Fetches detailed information for a specific trading pair from DexScreener API.

    Args:
        chain (str): Chain identifier (e.g., 'solana, bsc, base, ethereum...')
        pair_address (str): Pair contract address

    Returns:
        Dict: Pair information with status and data
    """
    try:
        response = requests.get(
            f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{pair_address}",
            headers={},
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "error": f"Query failed with status code {response.status_code}: {response.text}",
            }

        data = response.json()
        pairs = data.get("pairs", [])

        # Get first matching pair
        matching_pair = next(
            (pair for pair in pairs if pair.get("pairAddress", "").lower() == pair_address.lower()), None
        )

        if matching_pair:
            return {"status": "success", "pair": matching_pair}

        return {"status": "success", "message": "No matching pair found"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def fetch_token_pairs(chain: str, token_address: str) -> Dict:
    """
    Fetches all trading pairs for a specific token on a given chain from DexScreener API.

    Args:
        chain (str): Chain identifier (e.g., solana, bsc, ethereum)
        token_address (str): Token contract address

    Returns:
        Dict: Trading pairs information for the token
    """
    try:
        response = requests.get(
            f"https://api.dexscreener.com/tokens/v1/{chain}/{token_address}",
            headers={},
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "error": f"Query failed with status code {response.status_code}: {response.text}",
            }

        pairs = response.json()

        if not pairs:
            return {"status": "no_data", "error": "No pairs found for this token"}

        # Limit the number of pairs
        limit = 5
        limited_pairs = pairs[:limit] if len(pairs) > limit else pairs

        return {"status": "success", "pairs": limited_pairs}
    except Exception as e:
        return {"status": "error", "error": f"Failed to fetch token pairs: {str(e)}"}


def fetch_token_profiles() -> Dict:
    """
    Fetches the latest token profiles from DexScreener API.

    Returns:
        Dict: Token profiles information with status
    """
    try:
        response = requests.get(
            "https://api.dexscreener.com/token-profiles/latest/v1",
            headers={},
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "error": f"Query failed with status code {response.status_code}: {response.text}",
            }

        data = response.json()

        limit = 5
        # Limit the number of profiles
        profiles = data[:limit] if len(data) > limit else data

        return {"status": "success", "profiles": profiles}

    except Exception as e:
        return {"status": "error", "error": f"Failed to fetch token profiles: {str(e)}"}
