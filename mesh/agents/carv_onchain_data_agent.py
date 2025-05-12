import logging
import os
from typing import Any, Dict, List, Optional

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class CarvOnchainDataAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://interface.carv.io/ai-agent-backend/sql_query_by_llm"
        self.supported_chains = ["ethereum", "base", "bitcoin", "solana"]

        self.api_key = os.getenv("CARV_API_KEY")
        if not self.api_key:
            raise ValueError("CARV_API_KEY environment variable is required")
        self.headers = {"Content-Type": "application/json", "Authorization": self.api_key}

        self.metadata.update(
            {
                "name": "CARV Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can query blockchain metrics of Ethereum, Base, Bitcoin, or Solana using natural language through the CARV API.",
                "external_apis": ["CARV"],
                "tags": ["Onchain Data"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Carv.png",
                "examples": [
                    "Identify the biggest transaction of ETH in the past 30 days",
                    "How many Bitcoins have been mined since the beginning of 2025?",
                    "What are the top 5 most popular smart contracts on Ethereum in the past 30 days?",
                ],
                "large_model_id": "openai/gpt-4o-mini",
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a blockchain data analyst that can access blockchain metrics from various blockchain networks.

        IMPORTANT GUIDELINES:
        - You can only analyze data from Ethereum, Base, Bitcoin, and Solana blockchains.
        - Always infer the blockchain from the user's query.
        - If the blockchain is not supported, explain the limitation.
        - Convert the user's query to a clear and accurate natural language query such as "What's the most active address on Ethereum during the past 24 hours?" or "Identify the biggest transaction of ETH in the past 30 days" to be used as the input for your tool.
        - Respond with natural language in a clear, concise manner with relevant data returned from the tool. Do not use markdown formatting or bullet points unless requested.
        - Remember, ETH has 18 decimals, so if ETH amounts are returned, you should consider 10E18 as the denominator.
        - Never make up data that is not returned from the tool.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_onchain_data",
                    "description": "Query blockchain data from Ethereum, Base, Bitcoin, or Solana with natural language. Access detailed metrics including: block data (timestamps, hash, miner, gas used/limit), transaction details (hash, from/to addresses, values, gas prices), and network utilization statistics. Can calculate aggregate statistics like daily transaction counts, average gas prices, top wallet activities, and blockchain growth trends. Results can be filtered by time periods, address types, transaction values, and more.",
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
                                "description": "A natural language query describing the blockchain metrics request.",
                            },
                        },
                        "required": ["blockchain", "query"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                      CARV API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)  # Cache for 5 minutes
    @with_retry(max_retries=3)
    async def query_onchain_data(self, blockchain: str, query: str) -> Dict:
        """
        Query the CARV API with a natural language question about blockchain metrics.
        """
        try:
            blockchain = blockchain.lower()
            if blockchain not in self.supported_chains:
                return {
                    "error": f"Unsupported blockchain '{blockchain}'. Supported chains are {', '.join(self.supported_chains)}."
                }

            processed_query = query
            if blockchain not in query.lower():
                processed_query = f"On {blockchain} blockchain, {query}"

            data = {"question": processed_query}

            logger.info(f"Querying CARV API for blockchain {blockchain}: {processed_query}")

            response = await self._api_request(
                url=self.api_url,
                method="POST",
                headers=self.headers,
                json_data=data,
            )

            if "error" in response:
                return {"error": response["error"]}

            return response

        except Exception as e:
            logger.error(f"Error querying CARV API: {str(e)}")
            return {"error": f"Failed to query blockchain metrics: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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
