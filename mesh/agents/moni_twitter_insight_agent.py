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
                "tags": ["Twitter", "Social Media", "Intelligence"],
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
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
    ) -> Dict[str, Any]:
        """
        A single method that calls the appropriate function, handles
        errors/formatting, and optionally calls the LLM to explain the result.
        """
        username = function_args.get("username", "")
        if not username:
            return {"error": "Username is required for all Twitter intelligence tools"}

        # Call the appropriate tool based on tool_name
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
        formatted_data = {"tool": tool_name, "username": username, "data": result}
        if raw_data_only:
            return {"response": "", "data": formatted_data}

        explanation = await self._respond_with_llm(
            query=query, tool_call_id=tool_call_id, data=formatted_data, temperature=0.3
        )

        return {"response": explanation, "data": formatted_data}

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

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
