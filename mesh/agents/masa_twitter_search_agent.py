import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class MasaTwitterSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_url = "https://data.dev.masalabs.ai/api/v1"
        self.api_key = os.getenv("MASA_API_KEY")
        if not self.api_key:
            raise ValueError("MASA_API_KEY environment variable is required")

        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Masa Twitter Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search on Twitter through Masa API and analyze the results by identifying trending topics and sentiment related to a topic.",
                "external_apis": ["Masa"],
                "tags": ["Twitter"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Masa.png",
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
    #                      MASA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def search_twitter(self, search_term: str, max_results: int = 25) -> dict:
        try:
            # https://data.dev.masalabs.ai/endpoints
            payload = {"type": "twitter-scraper", "arguments": {"query": search_term, "max_results": max_results}}

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
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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
