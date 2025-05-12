import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class CookieProjectInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.cookie.fun"
        self.api_key = os.getenv("COOKIE_FUN_API_KEY")
        if not self.api_key:
            raise ValueError("COOKIE_FUN_API_KEY environment variable is required")

        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Cookie Project Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides information about crypto projects using Cookie API, including project details by Twitter username and contract address.",
                "external_apis": ["Cookie API"],
                "tags": ["Projects"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/CookieFun.png",
                "examples": [
                    "Tell me about the project with Twitter handle @heurist_ai",
                    "Tell me about the project with Twitter handle @cookiedotfun",
                    "Get details for the contract 0xc0041ef357b183448b235a8ea73ce4e4ec8c265f",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a crypto project information specialist that provides insights on blockchain projects using Cookie API data.

        Focus on delivering factual information and insights that help users understand:
        - Project details including information from Twitter username
        - Project information from contract addresses

        Important instructions on time intervals:
        - Only use "_3Days" or "_7Days" for interval parameter
        - If the user asks for 1-4 days of data, use "_3Days" interval
        - If the user asks for 5 days or more, always use "_7Days" interval
        - Even if the user asks for data over a longer period (30, 90 days), always cap it at 7 days and inform the user that data has been capped at 7 days for consistency

        If a user asks about a specific project, try to identify whether they've provided a Twitter username
        or contract address and use the appropriate tool.

        Keep your responses concise and data-driven while making the information accessible. NEVER make up data that is not returned from the tool.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_project_by_twitter_username",
                    "description": "Get comprehensive information about a crypto project by its Twitter username. Returns detailed market metrics (market cap, price, 24h volume, liquidity, holder counts), performance trends with percentage changes, Twitter engagement statistics (follower counts, average impressions, engagement rates), and top engaging tweets with smart engagement points and impression counts. Perfect for analyzing a project's market performance, social media reach, and community engagement.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "twitter_username": {
                                "type": "string",
                                "description": "Twitter username without the @ symbol",
                            },
                            "interval": {
                                "type": "string",
                                "description": "Time interval for the data (_3Days, _7Days)",
                                "enum": ["_3Days", "_7Days"],
                                "default": "_7Days",
                            },
                        },
                        "required": ["twitter_username"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_project_by_contract_address",
                    "description": "Get comprehensive information about a crypto project by its contract address. Returns detailed market metrics (market cap, price, 24h volume, liquidity, holder counts), performance trends with percentage changes, associated Twitter accounts, Twitter engagement statistics (follower counts, average impressions, engagement rates), and top engaging tweets with smart engagement points and impression counts. Perfect for analyzing a project's market performance across different chains, social media reach, and community engagement when you have the token contract address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "contract_address": {
                                "type": "string",
                                "description": "Token contract address",
                            },
                            "interval": {
                                "type": "string",
                                "description": "Time interval for the data (_3Days, _7Days)",
                                "enum": ["_3Days", "_7Days"],
                                "default": "_7Days",
                            },
                        },
                        "required": ["contract_address"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      COOKIE API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_project_by_twitter_username(self, twitter_username: str, interval: str = "_7Days") -> Dict:
        """
        Get information about a crypto project by its Twitter username.
        """
        logger.info(f"Fetching project data for Twitter username: {twitter_username}, interval: {interval}")

        url = f"{self.base_url}/v2/agents/twitterUsername/{twitter_username}"
        params = {"interval": interval}

        result = await self._api_request(url, headers=self.headers, params=params)

        if result.get("error"):
            logger.error(f"Error fetching project data: {result['error']}")
        else:
            logger.info(f"Successfully retrieved project details for {twitter_username}")

        return {"status": "success", "data": result} if not result.get("error") else result

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_project_by_contract_address(self, contract_address: str, interval: str = "_7Days") -> Dict:
        """
        Get information about a crypto project by its contract address.
        """
        logger.info(f"Fetching project data for contract address: {contract_address}, interval: {interval}")

        url = f"{self.base_url}/v2/agents/contractAddress/{contract_address}"
        params = {"interval": interval}

        result = await self._api_request(url, headers=self.headers, params=params)

        if result.get("error"):
            logger.error(f"Error fetching project data: {result['error']}")
        else:
            logger.info(f"Successfully retrieved project details for contract {contract_address}")

        return {"status": "success", "data": result} if not result.get("error") else result

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution and return results."""
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_project_by_twitter_username":
            twitter_username = function_args.get("twitter_username")
            if not twitter_username:
                return {"error": "Missing 'twitter_username' parameter"}
            twitter_username = twitter_username.lstrip("@")
            result = await self.get_project_by_twitter_username(
                twitter_username=twitter_username,
                interval=function_args.get("interval", "_7Days"),
            )

        elif tool_name == "get_project_by_contract_address":
            contract_address = function_args.get("contract_address")
            if not contract_address:
                return {"error": "Missing 'contract_address' parameter"}

            result = await self.get_project_by_contract_address(
                contract_address=contract_address,
                interval=function_args.get("interval", "_7Days"),
            )
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        if errors := self._handle_error(result):
            return errors

        return result
