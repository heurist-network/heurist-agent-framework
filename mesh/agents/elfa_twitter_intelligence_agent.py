import json
import os
import random
import time
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()


class ElfaTwitterIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        api_keys_str = os.getenv("ELFA_API_KEY")
        if not api_keys_str:
            raise ValueError("ELFA_API_KEY environment variable is required")

        self.api_keys = [key.strip() for key in api_keys_str.split(",") if key.strip()]
        if not self.api_keys:
            raise ValueError("No valid API keys found in ELFA_API_KEY")

        self.current_api_key = random.choice(self.api_keys)
        self.last_rotation_time = time.time()
        self.rotation_interval = 300  # Rotate every 5 minutes

        self.base_url = "https://api.elfa.ai/v1"
        self._update_headers()

        self.metadata.update(
            {
                "name": "Elfa Twitter Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes a token or a topic or a Twitter account using Twitter data and Elfa API. It highlights smart influencers.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about token mentions, trends, topics, or a Twitter account",
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
                        "description": "Natural language explanation of the Twitter analysis",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured data from ELFA API", "type": "dict"},
                ],
                "external_apis": ["Elfa"],
                "tags": ["Social", "Twitter"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Elfa.png",
                "examples": [
                    "Search for mentions of Heurist, HEU, and heurist_ai in the last 30 days",
                    "Analyze the Twitter account @heurist_ai",
                    "Get trending tokens on Twitter in the last 24 hours",
                    "What are people talking about ETH and SOL this week?",
                ],
            }
        )

    def _update_headers(self):
        """Update headers with current API key"""
        self.headers = {"x-elfa-api-key": self.current_api_key, "Accept": "application/json"}

    def _rotate_api_key(self):
        """Rotate API key if enough time has passed"""
        current_time = time.time()
        if current_time - self.last_rotation_time >= self.rotation_interval:
            self.current_api_key = random.choice(self.api_keys)
            self._update_headers()
            self.last_rotation_time = current_time

    def get_system_prompt(self) -> str:
        return (
            "You are a specialized assistant that analyzes Twitter data for crypto tokens using ELFA API. "
            "Your responses should be clear, concise, and data-driven.\n\n"
            "When analyzing mentions:\n"
            "1. Summarize the overall sentiment and engagement\n"
            "2. Highlight key influencers and their impact\n"
            "3. Identify notable trends or patterns\n\n"
            "When analyzing accounts:\n"
            "1. Summarize engagement metrics\n"
            "2. Highlight influential connections\n"
            "3. Note posting patterns and impact"
        )

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_mentions",
                    "description": "Search for mentions of specific tokens or topics on Twitter. This tool finds discussions about cryptocurrencies, blockchain projects, or other topics of interest. It provides the tweets and mentions of smart accounts (only influential ones) and does not contain all tweets. Use this when you want to understand what influential people are saying about a particular token or topic on Twitter. Each of the search keywords should be one word or phrase. A maximum of 5 keywords are allowed. One key word should be one concept. Never use long sentences or phrases as keywords.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords to search for",
                            },
                            "days_ago": {
                                "type": "number",
                                "description": "Number of days to look back",
                                "default": 20,
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results (minimum: 20)",
                                "default": 20,
                            },
                        },
                        "required": ["keywords"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_account",
                    "description": "Search for a Twitter account with both mention search and account statistics. This tool provides engagement metrics, follower growth, and mentions by smart users. It does not contain all tweets, but only those of influential users. It also identifies the topics and cryptocurrencies they frequently discuss. Data comes from ELFA API and can analyze several weeks of historical activity.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "Twitter username to analyze (without @)"},
                            "days_ago": {
                                "type": "number",
                                "description": "Number of days to look back for mentions",
                                "default": 30,
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of mention results",
                                "default": 20,
                            },
                        },
                        "required": ["username"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_trending_tokens",
                    "description": "Get current trending tokens on Twitter. This tool identifies which cryptocurrencies and tokens are generating the most buzz on Twitter right now. The results include token names, their relative popularity, and sentiment indicators. Use this when you want to discover which cryptocurrencies are currently being discussed most actively on social media. Data comes from ELFA API and represents real-time trends.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time_window": {
                                "type": "string",
                                "description": "Time window to analyze",
                                "default": "24h",
                            }
                        },
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None) -> Dict:
        self._rotate_api_key()  # Check and rotate API key if needed
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method=method, url=url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"ELFA API request failed: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    async def search_mentions(self, keywords: List[str], days_ago: int = 29, limit: int = 20) -> Dict:
        if limit < 20:
            limit = 20
        if days_ago > 29:
            # The 'from' and 'to' timestamps must be within 30 days of each other and at least 1 day apart.
            days_ago = 29
        if len(keywords) > 5:
            keywords = keywords[:5]

        try:
            end_time = int(time.time() - 60)  # Current time minus 60 seconds
            start_time = int(end_time - (days_ago * 86400))  # end_time minus days_ago in seconds

            params = {"keywords": ",".join(keywords), "from": start_time, "to": end_time, "limit": limit}

            result = await self._make_request("mentions/search", params=params)
            if "data" in result:
                for tweet in result["data"]:
                    if "id" in tweet:
                        tweet.pop("id", None)
                    if "twitter_id" in tweet:
                        tweet.pop("twitter_id", None)
                    if "twitter_user_id" in tweet:
                        tweet.pop("twitter_user_id", None)

            if "metadata" in result:
                # remove metadata from result
                result.pop("metadata", None)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=300)
    async def get_account_stats(self, username: str) -> Dict:
        try:
            params = {"username": username}
            result = await self._make_request("account/smart-stats", params=params)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=300)
    async def search_account(self, username: str, days_ago: int = 29, limit: int = 20) -> Dict:
        try:
            # Get account stats
            account_stats_result = await self.get_account_stats(username)
            if "error" in account_stats_result:
                return account_stats_result

            # Search for mentions of the account
            mentions_result = await self.search_mentions([username], days_ago, limit)
            if "error" in mentions_result:
                return mentions_result

            # Combine both results
            return {
                "status": "success",
                "data": {
                    "account_stats": account_stats_result.get("data", {}),
                    "mentions": mentions_result.get("data", {}),
                },
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=300)
    async def get_trending_tokens(self, time_window: str = "24h") -> Dict:
        try:
            params = {"timeWindow": time_window, "page": 1, "pageSize": 50, "minMentions": 5}
            result = await self._make_request("trending-tokens", params=params)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle tool execution and optional LLM explanation"""

        if tool_name == "search_mentions":
            result = await self.search_mentions(**function_args)
        elif tool_name == "search_account":
            result = await self.search_account(**function_args)
        elif tool_name == "get_trending_tokens":
            result = await self.get_trending_tokens(**function_args)
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors
        return result

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
            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
            return {"response": "", "data": data}

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY (LLM decides the tool)
        # ---------------------
        # Only use search_mentions and search_account for LLM tool selection
        llm_tools = [
            tool
            for tool in self.get_tool_schemas()
            if tool["function"]["name"] in ["search_mentions", "search_account"]
        ]

        response = await call_llm_with_tools_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            system_prompt=self.get_system_prompt(),
            user_prompt=query,
            temperature=0.1,
            tools=llm_tools,
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

        explanation = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query},
                {"role": "tool", "content": str(data), "tool_call_id": tool_call.id},
            ],
            temperature=0.6,
        )

        return {"response": explanation, "data": data}
