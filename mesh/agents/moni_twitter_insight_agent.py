import logging
import os
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class MoniTwitterInsightAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.session = None
        self.base_url = "https://api.discover.getmoni.io"
        self.api_key = os.getenv("MONI_API_KEY")

        self.metadata.update(
            {
                "name": "Moni Twitter Insight Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes Twitter accounts providing insights on smart followers, mentions, and account activity.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about a Twitter account or mentions",
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
                        "description": "Natural language explanation of the Twitter data",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured Twitter data",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Moni"],
                "tags": ["Twitter"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Moni.png",
                "examples": [
                    "Show me the follower growth trends for heurist_ai over the last week",
                    "What categories of followers does heurist_ai have",
                    "Show me the recent smart mentions for ethereum",
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

    async def cleanup(self):
        """Close the session if it exists"""
        if self.session:
            await self.session.close()
            self.session = None

    def get_system_prompt(self) -> str:
        return """
        You are a Twitter intelligence specialist that can analyze Twitter accounts and mentions.

        CAPABILITIES:
        - Track smart follower metrics and trends for any Twitter account
        - Analyze smart followers by categories
        - Provide insights on Twitter account feed and smart mentions

        RESPONSE GUIDELINES:
        - Focus on insights rather than raw data
        - Highlight key trends and patterns
        - Format numbers in a readable way (e.g., "2.5K followers" instead of "2500 followers")
        - Provide concise, actionable insights

        IMPORTANT:
        - Always ensure you have a valid Twitter username (without the @ symbol)
        - For historical data, focus on trends and changes over time
        - When analyzing smart followers, explain what makes them "smart followers" (quality accounts with meaningful engagement)
        - When no timeframe is specified, assume the most recent available data
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_smart_followers_history",
                    "description": "Get historical data on smart followers count for a Twitter account",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username without the @ symbol",
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Time range for the data (H1=Last hour, H24=Last 24 hours, D7=Last 7 days, D30=Last 30 days, Y1=Last year)",
                                "enum": ["H1", "H24", "D7", "D30", "Y1"],
                                "default": "D7",
                            },
                        },
                        "required": ["username"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_smart_followers_categories",
                    "description": "Get categories of smart followers for a Twitter account",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username without the @ symbol",
                            }
                        },
                        "required": ["username"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_smart_mentions_feed",
                    "description": "Get recent smart mentions feed for a Twitter account",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username without the @ symbol",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of mentions to return",
                                "default": 100,
                            },
                            "fromDate": {
                                "type": "integer",
                                "description": "Unix timestamp of the earliest event to include",
                            },
                            "toDate": {
                                "type": "integer",
                                "description": "Unix timestamp of the most recent post to include",
                            },
                        },
                        "required": ["username"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    def _clean_username(self, username: str) -> str:
        """
        Remove @ symbol if present in the username
        """
        return username.replace("@", "")

    # ------------------------------------------------------------------------
    #                      MONI API-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    @with_retry(max_retries=3)
    async def get_smart_followers_history(self, username: str, timeframe: str = "D7") -> Dict:
        """Get historical data on smart followers count"""
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            clean_username = self._clean_username(username)
            url = f"{self.base_url}/api/v2/twitters/{clean_username}/history/smart_followers_count/"
            params = {"timeframe": timeframe}

            headers = {"accept": "application/json", "Api-Key": self.api_key}

            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    return {"error": f"Failed to get followers history for {clean_username}: {response.status}"}

                data = await response.json()
                return data
        except Exception as e:
            logger.error(f"Error getting smart followers history: {str(e)}")
            return {"error": f"Failed to fetch smart followers history: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    @with_retry(max_retries=3)
    async def get_smart_followers_categories(self, username: str) -> Dict:
        """Get categories of smart followers"""
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            clean_username = self._clean_username(username)
            url = f"{self.base_url}/api/v2/twitters/{clean_username}/smart_followers/categories/"

            headers = {"accept": "application/json", "Api-Key": self.api_key}

            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    return {"error": f"Failed to get follower categories for {clean_username}: {response.status}"}

                data = await response.json()
                return data
        except Exception as e:
            logger.error(f"Error getting smart followers categories: {str(e)}")
            return {"error": f"Failed to fetch smart followers categories: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    @with_cache(ttl_seconds=1800)  # Cache for 30 minutes
    @with_retry(max_retries=3)
    async def get_smart_mentions_feed(
        self, username: str, limit: int = 100, fromDate: int = None, toDate: int = None
    ) -> Dict:
        """Get recent smart mentions feed"""
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            clean_username = self._clean_username(username)
            url = f"{self.base_url}/api/v2/twitters/{clean_username}/feed/smart_mentions/"

            params = {"limit": limit}
            if fromDate:
                params["fromDate"] = fromDate
            if toDate:
                params["toDate"] = toDate

            headers = {"accept": "application/json", "Api-Key": self.api_key}

            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    return {"error": f"Failed to get mentions feed for {clean_username}: {response.status}"}

                data = await response.json()
                return data
        except Exception as e:
            logger.error(f"Error getting smart mentions feed: {str(e)}")
            return {"error": f"Failed to fetch smart mentions feed: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        This method matches the signature expected by the base MeshAgent class.
        """
        username = function_args.get("username", "")
        if not username:
            return {"error": "Username is required for all Twitter intelligence tools"}

        if tool_name == "get_smart_followers_history":
            timeframe = function_args.get("timeframe", "D7")
            result = await self.get_smart_followers_history(username, timeframe)
        elif tool_name == "get_smart_followers_categories":
            result = await self.get_smart_followers_categories(username)
        elif tool_name == "get_smart_mentions_feed":
            limit = function_args.get("limit", 100)
            fromDate = function_args.get("fromDate", None)
            toDate = function_args.get("toDate", None)
            result = await self.get_smart_mentions_feed(username, limit, fromDate, toDate)
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return {"tool": tool_name, "username": username, "data": result}

    async def _respond_with_llm(
        self, model_id: str, system_prompt: str, query: str, tool_call_id: str, data: dict, temperature: float
    ) -> str:
        """
        Custom implementation to generate user-friendly explanations from the Twitter data.
        """

        return await super()._respond_with_llm(
            model_id=model_id,
            system_prompt=system_prompt,
            query=query,
            tool_call_id=tool_call_id,
            data=data,
            temperature=temperature,
        )
