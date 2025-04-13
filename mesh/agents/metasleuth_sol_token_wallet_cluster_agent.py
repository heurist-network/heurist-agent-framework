import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class MetaSleuthSolTokenWalletClusterAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "MetaSleuth Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can analyze the wallet clusters holding a specific Solana token, and identify top holder behavior, concentration, and potential market manipulation.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "The query containing token address to analyze.",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, returns only raw data without analysis",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {"name": "response", "description": "Token wallet cluster analysis and explanation", "type": "str"},
                    {"name": "data", "description": "The token wallet cluster details", "type": "dict"},
                ],
                "external_apis": ["MetaSleuth"],
                "tags": ["Solana"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/MetaSleuth.png",
                "examples": [
                    "Analyze the wallet clusters of this Solana token: 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN",
                    "What percentage of the supply of 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN is held by the top wallet clusters?",
                ],
            }
        )
        self.base_url = "https://bot.metasleuth.io"
        self.ms_bot_api_key = os.getenv("MS_BOT_API_KEY")  # get from environment variable

    def get_system_prompt(self) -> str:
        return """You are a blockchain wallet cluster analyzer that provides factual analysis of Solana token holders based on MetaSleuth API data.

WHEN ANALYZING A TOKEN ADDRESS:
1. Extract the token address from the user's query
2. Use the fetch_token_clusters tool to get the wallet cluster data
3. Present the findings in this structured format:
   - Basic Token Info: Token name, symbol, price, market cap, total holders
   - Top 10 Holders Concentration: Percentage of supply held by top 10 addresses
   - Creator Information: Creator address and creation time
   - Wallet Clusters: Identify and explain significant holder clusters (focus on the top 5-10)
   - Risk Assessment: Analyze token distribution and whale concentration

WHEN ANALYZING A SPECIFIC CLUSTER UUID (NOTE: this is exclusive of token address analysis):
1. Extract the cluster UUID from the user's query
2. Use the fetch_cluster_details tool to get detailed information about this specific cluster
3. Present the findings in this different structured format:
   - Cluster Overview: UUID, rank, total wallets in cluster, total percentage of token supply
   - Holdings Analysis: Total holding amount, percentage of total token supply
   - Wallet Breakdown: List all wallets in the cluster with their individual holdings and percentages
   - Entity Identification: Identify any known entities (exchanges, projects, etc.)
   - Centralization Analysis: Assess if holdings are concentrated within the cluster or evenly distributed

FORMATTING INSTRUCTIONS:
- For fund flow links, ALWAYS format them as "@https://metasleuth.io/result/{fundFlowLink}" when fundFlowLink is provided
- Use markdown formatting for better readability
- Present numerical data in both scientific notation (when provided) and readable format
- Always clearly distinguish between token-level analysis and cluster-level analysis
- Use the available data only for the final analysis

Note: Currently only Solana chain is supported.
"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_token_clusters",
                    "description": "Fetch wallet clusters that hold a specific Solana token. A cluster means a group of wallets that have transacted with each other. The results contain the wallets in the cluster with their individual holdings and percentages. Use this to analyze the holder behavior of a token and identify potential market manipulation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {"type": "string", "description": "The Solana token address to analyze"},
                            "page": {
                                "type": "integer",
                                "description": "Page number for paginated results",
                                "default": 1,
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of clusters to return per page",
                                "default": 20,
                            },
                            "query_id": {
                                "type": "string",
                                "description": "Optional query ID for historical analysis",
                                "default": "",
                            },
                        },
                        "required": ["address"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_cluster_details",
                    "description": "Fetch detailed information about a specific wallet cluster. You must obtain the cluster UUID from the fetch_token_clusters tool. It's expensive to fetch cluster details, so only use this tool when there's a particular reason to deep dive into a cluster, otherwise the results from fetch_token_clusters tool are sufficient.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cluster_uuid": {"type": "string", "description": "The unique identifier of the cluster"},
                            "page": {
                                "type": "integer",
                                "description": "Page number for paginated results",
                                "default": 1,
                            },
                            "page_size": {
                                "type": "integer",
                                "description": "Number of holders to return per page",
                                "default": 20,
                            },
                        },
                        "required": ["cluster_uuid"],
                    },
                },
            },
        ]

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_token_clusters(self, address: str, page: int = 1, page_size: int = 20, query_id: str = "") -> Dict:
        """Fetch token wallet clusters from MetaSleuth API"""
        try:
            headers = {"MS-Bot-Api-Key": self.ms_bot_api_key, "Content-Type": "application/json"}

            payload = {"chain": "solana", "address": address, "page": page, "pageSize": page_size, "queryID": query_id}

            response = requests.post(f"{self.base_url}/api/v1/tgbot/cluster", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("code", -1) != 0:
                logger.error(f"API error: {data.get('message')}")
                return {"error": data.get("message", "API Error")}

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching token clusters: {e}")
            return {"error": f"Failed to fetch token clusters: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_cluster_details(self, cluster_uuid: str, page: int = 1, page_size: int = 20) -> Dict:
        """Fetch detailed information about a specific wallet cluster"""
        try:
            headers = {"MS-Bot-Api-Key": self.ms_bot_api_key, "Content-Type": "application/json"}

            payload = {"clusterUUID": cluster_uuid, "page": page, "pageSize": page_size}

            response = requests.post(f"{self.base_url}/api/v1/tgbot/cluster-detail", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("code", -1) != 0:
                logger.error(f"API error: {data.get('message')}")
                return {"error": data.get("message", "API Error")}

            # Format the fundFlowLink as specified
            if data.get("fundFlowLink"):
                data["fundFlowUrl"] = f"@https://metasleuth.io/result/{data['fundFlowLink']}"

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching cluster details: {e}")
            return {"error": f"Failed to fetch cluster details: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""

        if tool_name == "fetch_token_clusters":
            address = function_args.get("address")
            page = function_args.get("page", 1)
            page_size = function_args.get("page_size", 20)
            query_id = function_args.get("query_id", "")

            if not address:
                return {"error": "Missing 'address' in tool arguments"}

            logger.info(f"Fetching token clusters for {address}")
            result = await self.fetch_token_clusters(address, page, page_size, query_id)

        elif tool_name == "fetch_cluster_details":
            cluster_uuid = function_args.get("cluster_uuid")
            page = function_args.get("page", 1)
            page_size = function_args.get("page_size", 20)

            if not cluster_uuid:
                return {"error": "Missing 'cluster_uuid' in tool arguments"}

            logger.info(f"Fetching cluster details for {cluster_uuid}")
            result = await self.fetch_cluster_details(cluster_uuid, page, page_size)

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
