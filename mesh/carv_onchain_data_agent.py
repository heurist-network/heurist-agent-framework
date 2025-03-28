import json
import logging
import os
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class CarvOnchainDataAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.session = None
        self.api_url = "https://interface.carv.io/ai-agent-backend/sql_query_by_llm"
        self.supported_chains = ["ethereum", "base", "bitcoin", "solana"]

        self.metadata.update(
            {
                "name": "CARV Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can query on-chain data from multiple blockchains using natural language through the CARV API.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about on-chain data for Ethereum, Base, Bitcoin, or Solana",
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
                        "description": "Natural language explanation of the on-chain data",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured on-chain data response",
                        "type": "dict",
                    },
                ],
                "external_apis": ["CARV"],
                "tags": ["Onchain Data"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Carv.png",
                "examples": [
                    "What's the most active address on Ethereum during the last 24 hours?",
                    "What is the total transaction volume on Ethereum in the past week?",
                    "Which Ethereum address has the highest balance right now?",
                    "What are the top 5 most popular smart contracts on Ethereum?",
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
        return """You are a blockchain data analyst that can access on-chain data from various blockchain networks.

        IMPORTANT GUIDELINES:
        - You can only analyze data from Ethereum, Base, Bitcoin, and Solana blockchains.
        - Always ensure the user specifies which blockchain they want data from.
        - If the blockchain is not specified or is unsupported, politely explain the limitation.
        - Parse the user's query to identify the requested blockchain and the specific data they want.
        - Formulate your responses in a clear, concise manner with relevant on-chain metrics.
        - When possible, explain patterns or trends that might explain the data.

        For example query "What's the most active address on Ethereum during the past 24 hours?" clearly specifies Ethereum blockchain.

        Ensure your query is specific enough to return meaningful data. Include time periods when relevant.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_onchain_data",
                    "description": "Query real-time on-chain data from Ethereum, Base, Bitcoin, or Solana. Retrieves insights on transaction activity, smart contract interactions, wallet movements, and network analytics for the specified blockchain. Use this when structured blockchain data is needed based on a natural language request.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "blockchain": {
                                "type": "string",
                                "description": "The blockchain to query (ethereum, base, bitcoin, solana). Only these four blockchains are supported.",
                                "enum": ["ethereum", "base", "bitcoin", "solana"],
                            },
                            "query": {
                                "type": "string",
                                "description": "A natural language query describing the on-chain data request.",
                            },
                        },
                        "required": ["blockchain", "query"],
                    },
                },
            }
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
    #                      CARV API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def query_onchain_data(self, blockchain: str, query: str) -> Dict:
        """
        Query the CARV API with a natural language question about on-chain data.
        """
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            # Validate blockchain
            blockchain = blockchain.lower()
            if blockchain not in self.supported_chains:
                return {
                    "error": f"Unsupported blockchain '{blockchain}'. Supported chains are {', '.join(self.supported_chains)}."
                }

            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "Authorization": os.getenv("CARV_API_KEY"),
            }

            processed_query = query
            if blockchain not in query.lower():
                processed_query = f"On {blockchain} blockchain, {query}"

            data = {"question": processed_query}

            logger.info(f"Querying CARV API for blockchain {blockchain}: {processed_query}")

            async with self.session.post(self.api_url, json=data, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return {"error": f"CARV API error ({response.status}): {error_text}"}

                result = await response.json()
                return result

        except Exception as e:
            logger.error(f"Error querying CARV API: {str(e)}")
            return {"error": f"Failed to query on-chain data: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        """
        if tool_name != "query_onchain_data":
            return {"error": f"Unsupported tool '{tool_name}'"}

        blockchain = function_args.get("blockchain")
        user_query = function_args.get("query")

        if not blockchain or not user_query:
            return {"error": "Both 'blockchain' and 'query' are required parameters"}

        result = await self.query_onchain_data(blockchain, user_query)

        errors = self._handle_error(result)
        if errors:
            return errors

        formatted_data = {
            "blockchain": blockchain,
            "query": user_query,
            "results": result,
        }

        return formatted_data

    # ------------------------------------------------------------------------
    #                      MAIN HANDLER
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages, supporting both direct tool calls and natural language queries.

        Either 'query' or 'tool' is required in params.
        - If 'query' is present, it means "agent mode", we use LLM to interpret the query and call tools
          - if 'raw_data_only' is present, we return tool results without another LLM call
        - If 'tool' is present, it means "direct tool call mode", we bypass LLM and directly call the API
          - never run another LLM call, this minimizes latency and reduces error
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
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

            data = await self._handle_tool_logic(tool_name=tool_call_name, function_args=tool_call_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call.id, data=data, temperature=0.3
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
