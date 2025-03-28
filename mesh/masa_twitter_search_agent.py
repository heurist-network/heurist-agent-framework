import logging
import os
import time
from typing import Any, Dict, List

import requests

from core.llm import call_llm_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class MasaTwitterSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api1.dev.masalabs.ai/v1"
        self.headers = {"Authorization": f"Bearer {os.getenv('MASA_API_KEY')}", "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Masa Twitter Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search on Twitter through Masa API and analyze the results by identifying trending topics and sentiment related to a topic.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query to search Twitter.",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "max_results",
                        "description": "Maximum number of results to return.",
                        "type": "int",
                        "required": False,
                        "default": 25,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw or base structured data without additional LLM explanation.",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of the Twitter search results (empty if a direct tool call).",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured Twitter search results data.", "type": "dict"},
                ],
                "external_apis": ["Masa"],
                "tags": ["Social", "Twitter"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Masa.png",  # use the logo of masa
                "examples": [
                    "Search for tweets about @heurist_ai",
                    "What are people saying about $BTC on Twitter?",
                    "Find recent discussions about Elon Musk",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
    IDENTITY:
    You are a social media data analyst that can search and analyze Twitter data using the Masa API.

    CAPABILITIES:
    - Search Twitter for specific keywords or phrases
    - Analyze Twitter search results and extract meaningful insights
    - Identify trending topics and sentiment related to a query

    RESPONSE GUIDELINES:
    - Keep responses focused on what was specifically asked
    - Provide context about the volume and recency of tweets found
    - Highlight notable patterns or insights from the data

    DOMAIN-SPECIFIC RULES:
    For Twitter search queries, use the search_twitter tool to fetch recent tweets containing the specified keywords.
    When analyzing search results, consider:
    1. Volume of mentions and engagement metrics
    2. Common themes or topics in the tweets
    3. Notable users or accounts engaging with the topic
    4. Sentiment trends if apparent from the content

    IMPORTANT:
    - Do not make claims about data that isn't present in the search results
    - Keep responses concise and relevant"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_twitter",
                    "description": "Search on Twitter to identify what people are saying about a topic. The search term must be a single word or a short phrase, or an account name or hashtag. Never use a search term that is longer than 2 words. The results contain the tweet content and the impression metrics of the tweet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "The search term to find tweets"},
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 25)",
                            },
                        },
                        "required": ["search_term"],
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
    #                      MASA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)
    async def search_twitter(self, search_term: str, max_results: int = 25) -> dict:
        try:
            # Note: The API still expects 'query' as the parameter name
            payload = {"query": search_term, "max_results": max_results}

            response = requests.post(f"{self.api_url}/search/live/twitter", headers=self.headers, json=payload)
            response.raise_for_status()

            search_data = response.json()
            uuid = search_data.get("uuid")

            if not uuid:
                return {"error": "Failed to initialize search: No UUID returned"}

            max_attempts = 30
            wait_time = 2

            for attempt in range(max_attempts):
                status_response = requests.get(
                    f"{self.api_url}/search/live/twitter/status/{uuid}", headers=self.headers
                )
                status_response.raise_for_status()
                status_data = status_response.json()
                if status_data.get("status") == "done":
                    break
                if status_data.get("error"):
                    return {"error": f"Search failed: {status_data.get('error')}"}
                time.sleep(wait_time)
            else:
                return {"error": "Search timed out after maximum attempts"}
            result_response = requests.get(f"{self.api_url}/search/live/twitter/result/{uuid}", headers=self.headers)
            result_response.raise_for_status()
            return self.format_twitter_results(result_response.json())
        except requests.RequestException as e:
            logger.error(f"Error during Twitter search: {e}")
            return {"error": f"Failed to search Twitter: {str(e)}"}

    def format_twitter_results(self, data: List) -> Dict:
        """Format Twitter search results in a structured way"""
        valid_tweets = [tweet for tweet in data if tweet.get("Content")]

        formatted_results = {
            "search_stats": {"total_results": len(valid_tweets), "has_results": len(valid_tweets) > 0},
            "tweets": [],
        }

        for tweet in valid_tweets:
            metadata = tweet.get("Metadata", {})
            created_at = metadata.get("created_at") if metadata else None
            metrics = metadata.get("public_metrics", {}) if metadata else {}

            formatted_tweet = {
                # "id": tweet.get("ExternalID"),
                "content": tweet.get("Content"),
                "created_at": created_at,
                "language": metadata.get("lang") if metadata else None,
                "metrics": {
                    "likes": metrics.get("LikeCount", 0),
                    "retweets": metrics.get("RetweetCount", 0),
                    "replies": metrics.get("ReplyCount", 0),
                    "quotes": metrics.get("QuoteCount", 0),
                    "bookmarks": metrics.get("BookmarkCount", 0),
                },
                # "author_id": metadata.get("user_id") if metadata else None,
                # "conversation_id": metadata.get("conversation_id") if metadata else None,
            }

            formatted_results["tweets"].append(formatted_tweet)

        return formatted_results

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data
        """
        if tool_name == "search_twitter":
            search_term = function_args.get("search_term")
            max_results = function_args.get("max_results", 25)

            if not search_term:
                return {"error": "Missing 'search_term' in tool_arguments"}

            logger.info(f"Searching Twitter for: '{search_term}' with max_results={max_results}")
            result = await self.search_twitter(search_term, max_results)

            errors = self._handle_error(result)
            if errors:
                return errors

            return result
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
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
        if "max_results" in params and (tool_name == "search_twitter" or query):
            tool_args["max_results"] = params.get("max_results")

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
            # For Twitter search, we'll directly map the query to the search_twitter tool
            # without requiring LLM to decide, since this is a specialized agent
            search_args = {"search_term": query, "max_results": params.get("max_results", 25)}

            data = await self._handle_tool_logic(tool_name="search_twitter", function_args=search_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id="natural_language_query", data=data, temperature=0.7
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
