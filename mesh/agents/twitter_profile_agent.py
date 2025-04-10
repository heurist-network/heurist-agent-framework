import asyncio
import logging
import os
import re
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class TwitterProfileAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("APIDANCE_API_KEY")
        if not self.api_key:
            raise ValueError("APIDANCE_API_KEY environment variable is required")

        self.base_url = "https://api.apidance.pro"
        self.headers = {"apikey": self.api_key}

        self.metadata.update(
            {
                "name": "Twitter Profile Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent fetches a Twitter user's profile information and recent tweets. It's useful for getting project updates or tracking key opinion leaders (KOLs) in the space.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Twitter username (with or without @) or user ID to fetch profile and tweets for",
                        "type": "str",
                        "required": False,
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
                        "description": "Natural language summary of the user's profile and recent tweets",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured data containing user profile and recent tweets",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Twitter API"],
                "tags": ["Twitter"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/twitter.png",
                "examples": [
                    "Summarise recent updates of @heurist_ai",
                    "What has @elonmusk been tweeting lately?",
                    "Get the recent tweets from cz_binance",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a specialized Twitter analyst that helps users get information about Twitter profiles and their recent tweets.

        When analyzing a Twitter profile:
        1. Provide a brief overview of the account (name, bio, follower count)
        2. Summarize their recent tweet activity (frequency, topics)
        3. Highlight notable tweets with high engagement

        Keep your analysis factual and concise. Focus on the data provided without making assumptions.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_user_tweets",
                    "description": "Fetch recent tweets from a Twitter user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username (with or without @) or numeric user ID",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tweets to return",
                                "default": 10,
                            },
                        },
                        "required": ["username"],
                    },
                },
            }
        ]

    def get_twitter_user_endpoint(self) -> str:
        return f"{self.base_url}/1.1/users/show.json"

    def get_twitter_tweets_endpoint(self) -> str:
        return f"{self.base_url}/sapi/UserTweets"

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    def _clean_username(self, username: str) -> str:
        """Remove @ symbol if present in username"""
        return username.strip().lstrip("@")

    def _is_numeric_id(self, input_str: str) -> bool:
        """Check if the input is a numeric ID"""
        return bool(re.match(r"^\d+$", input_str))

    def _extract_numeric_id(self, input_str: str) -> str:
        """Extract numeric ID from various formats"""
        # Check for patterns like "user_id:123456789" or "id:123456789"
        id_patterns = [
            r"user_id:(\d+)",
            r"userid:(\d+)",
            r"id:(\d+)",
            r"user:(\d+)",
            r"twitter id (\d+)",
            r"twitter_id (\d+)",
            r"twitter id: (\d+)",
            r"twitter_id: (\d+)",
        ]

        for pattern in id_patterns:
            match = re.search(pattern, input_str, re.IGNORECASE)
            if match:
                return match.group(1)

        # Check if the input itself is just a numeric ID
        if self._is_numeric_id(input_str.strip()):
            return input_str.strip()

        return ""

    def _extract_username_from_query(self, query: str) -> str:
        """Extract username or user ID from a query string"""
        if not query:
            return ""

        # First check if there's a numeric ID in the query
        numeric_id = self._extract_numeric_id(query)
        if numeric_id:
            return numeric_id

        # Common patterns for Twitter username mentions
        username_patterns = [
            r"@(\w+)",  # @username
            r"twitter\.com/(\w+)",  # twitter.com/username
            r"x\.com/(\w+)",  # x.com/username (new Twitter domain)
            r"account (?:for|of) (\w+)",  # account for username or account of username
            r"(\w+)\'s tweets",  # username's tweets
            r"(\w+)\'s twitter",  # username's twitter
            r"(\w+)\'s profile",  # username's profile
            r"(\w+)\'s account",  # username's account
            r"about (\w+)",  # about username
            r"from (\w+)",  # from username
            r"of (\w+)",  # of username
            r"by (\w+)",  # by username
            r"check (?:out )?(\w+)",  # check username or check out username
            r"look (?:at|up) (\w+)",  # look at username or look up username
            r"username (\w+)",  # username xyz
            r"handle (\w+)",  # handle xyz
        ]

        for pattern in username_patterns:
            match = re.search(pattern, query.lower())
            if match:
                username = match.group(1)
                # Filter out common words that might be incorrectly matched
                common_words = [
                    "the",
                    "twitter",
                    "tweets",
                    "account",
                    "profile",
                    "user",
                    "details",
                    "information",
                    "latest",
                    "recent",
                    "timeline",
                    "updates",
                    "posts",
                    "feed",
                    "activity",
                    "content",
                    "info",
                ]
                if username.lower() not in common_words:
                    return username

        account_phrases = [
            "twitter account",
            "account",
            "user",
            "profile",
            "tweets from",
            "tweets by",
            "tweeted by",
            "posted by",
            "check out",
            "look at",
            "view",
        ]
        for phrase in account_phrases:
            if phrase in query.lower():
                parts = query.lower().split(phrase, 1)
                if len(parts) > 1:
                    potential_username = parts[1].strip().split()[0] if parts[1].strip() else ""
                    if potential_username and (potential_username.isalnum() or "_" in potential_username):
                        # Filter out common words
                        common_words = [
                            "the",
                            "twitter",
                            "tweets",
                            "account",
                            "profile",
                            "user",
                            "details",
                            "information",
                            "latest",
                            "recent",
                            "timeline",
                        ]
                        if potential_username.lower() not in common_words:
                            return potential_username

        # Try to find any word that looks like a username
        words = query.split()
        for word in words:
            clean_word = word.strip().lstrip("@")
            if re.match(r"^[A-Za-z0-9_]+$", clean_word):
                common_words = [
                    "the",
                    "twitter",
                    "tweets",
                    "account",
                    "profile",
                    "user",
                    "details",
                    "information",
                    "latest",
                    "recent",
                    "timeline",
                    "updates",
                    "posts",
                    "feed",
                    "activity",
                    "what",
                    "about",
                    "show",
                    "me",
                    "get",
                    "find",
                    "search",
                    "look",
                    "check",
                ]
                if clean_word.lower() not in common_words:
                    return clean_word

        # Last resort: just return the last word
        words = [w for w in query.split() if w.strip()]
        if words:
            last_word = self._clean_username(words[-1])
            common_words = [
                "the",
                "twitter",
                "tweets",
                "account",
                "profile",
                "user",
                "details",
                "information",
                "latest",
                "recent",
                "timeline",
                "feed",
                "activity",
                "what",
                "about",
                "for",
                "from",
                "by",
            ]
            if last_word.lower() not in common_words:
                return last_word

        return ""

    async def _make_api_request(self, endpoint: str, params: Dict, max_retries: int = 3) -> Dict:
        """
        Make API request with retry logic for 429 errors

        Args:
            endpoint: API endpoint URL
            params: Request parameters
            max_retries: Maximum number of retries (default: 3)

        Returns:
            API response as dictionary
        """
        retries = 0
        backoff_time = 2

        while retries <= max_retries:
            try:
                response = requests.get(endpoint, params=params, headers=self.headers)

                if response.status_code == 200:
                    return response.json()
                if response.status_code == 429:
                    retries += 1
                    if retries > max_retries:
                        response.raise_for_status()
                    wait_time = (
                        backoff_time
                        * (2 ** (retries - 1))
                        * (0.8 + 0.4 * asyncio.get_event_loop().create_future().get_loop().time() % 1)
                    )
                    logger.warning(
                        f"Rate limit hit. Retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})"
                    )
                    await asyncio.sleep(wait_time)
                    continue
                response.raise_for_status()

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {str(e)}")
                retries += 1
                if retries > max_retries:
                    return {"status": "error", "error": f"API request failed after {max_retries} retries: {str(e)}"}

                wait_time = backoff_time * (2 ** (retries - 1))
                logger.warning(f"Request failed. Retrying in {wait_time} seconds (Attempt {retries}/{max_retries})")
                await asyncio.sleep(wait_time)

        return {"status": "error", "error": "Maximum retries exceeded"}

    async def _make_api_request(self, endpoint: str, params: Dict, max_retries: int = 3) -> Dict:
        """
        Make API request with retry logic for 429 errors

        Args:
            endpoint: API endpoint URL
            params: Request parameters
            max_retries: Maximum number of retries (default: 3)

        Returns:
            API response as dictionary
        """
        retries = 0
        backoff_time = 2

        while retries <= max_retries:
            try:
                response = requests.get(endpoint, params=params, headers=self.headers)

                if response.status_code == 200:
                    return response.json()
                if response.status_code == 429:
                    retries += 1
                    if retries > max_retries:
                        response.raise_for_status()
                    wait_time = (
                        backoff_time
                        * (2 ** (retries - 1))
                        * (0.8 + 0.4 * asyncio.get_event_loop().create_future().get_loop().time() % 1)
                    )
                    logger.warning(
                        f"Rate limit hit. Retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})"
                    )
                    await asyncio.sleep(wait_time)
                    continue
                response.raise_for_status()

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {str(e)}")
                retries += 1
                if retries > max_retries:
                    return {"status": "error", "error": f"API request failed after {max_retries} retries: {str(e)}"}

                wait_time = backoff_time * (2 ** (retries - 1))
                logger.warning(f"Request failed. Retrying in {wait_time} seconds (Attempt {retries}/{max_retries})")
                await asyncio.sleep(wait_time)

        return {"status": "error", "error": "Maximum retries exceeded"}

    # ------------------------------------------------------------------------
    #                      TWITTER API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def apidance_get_user_id(self, identifier: str) -> Dict:
        """
        Fetch Twitter user ID and profile information using screen name or user ID

        Args:
            identifier: Either a screen name or numeric user ID
        """
        try:
            params = {}
            if self._is_numeric_id(identifier):
                params = {"user_id": identifier}
            else:
                clean_username = self._clean_username(identifier)
                params = {"screen_name": clean_username}

            user_data = await self._make_api_request(endpoint=self.get_twitter_user_endpoint(), params=params)

            if "status" in user_data and user_data["status"] == "error":
                return user_data

            profile_info = {
                "id_str": user_data.get("id_str"),
                "name": user_data.get("name"),
                "screen_name": user_data.get("screen_name"),
                "description": user_data.get("description"),
                "followers_count": user_data.get("followers_count"),
                "friends_count": user_data.get("friends_count"),
                "statuses_count": user_data.get("statuses_count"),
                "profile_image_url": user_data.get("profile_image_url_https"),
                "verified": user_data.get("verified", False),
                "created_at": user_data.get("created_at"),
            }

            return {"status": "success", "profile": profile_info}

        except Exception as e:
            logger.error(f"Unexpected error in apidance_get_user_id: {e}")
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def apidance_get_tweets(self, user_id: str, limit: int = 10) -> Dict:
        """Fetch recent tweets for a user by ID"""
        try:
            params = {"user_id": user_id, "count": limit}

            tweets_data = await self._make_api_request(endpoint=self.get_twitter_tweets_endpoint(), params=params)

            if "status" in tweets_data and tweets_data["status"] == "error":
                return tweets_data

            tweets = tweets_data.get("tweets", [])

            cleaned_tweets = []
            for tweet in tweets:
                cleaned_tweet = {
                    "text": tweet.get("text", ""),
                    "created_at": tweet.get("created_at", ""),
                    "engagement": {
                        "retweets": tweet.get("retweet_count", 0),
                        "likes": tweet.get("favorite_count", 0),
                        "replies": tweet.get("reply_count", 0) if "reply_count" in tweet else 0,
                    },
                }
                cleaned_tweets.append(cleaned_tweet)

            return {"status": "success", "tweets": cleaned_tweets}
        except Exception as e:
            logger.error(f"Unexpected error in apidance_get_tweets: {e}")
            return {"status": "error", "error": f"Unexpected error: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle tool execution logic"""
        if tool_name == "get_user_tweets":
            identifier = function_args.get("username")
            limit = function_args.get("limit", 10)

            if not identifier:
                return {"error": "Missing 'username' in tool_arguments"}

            logger.info(f"Fetching tweets for identifier '{identifier}' with limit={limit}")

            profile_result = await self.apidance_get_user_id(identifier)
            if profile_result.get("status") == "error":
                return {"error": profile_result.get("error", "Failed to fetch user profile")}

            user_id = profile_result.get("profile", {}).get("id_str")
            if not user_id:
                return {"error": "Could not retrieve user ID"}

            tweets_result = await self.apidance_get_tweets(user_id, limit)
            if tweets_result.get("status") == "error":
                return {"error": tweets_result.get("error", "Failed to fetch user tweets")}

            return {"profile": profile_result.get("profile", {}), "tweets": tweets_result.get("tweets", [])}
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

    # ------------------------------------------------------------------------
    #                      MAIN MESSAGE HANDLER
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for handling messages.
        Either 'query' or 'tool' is required in params.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)
        limit = params.get("limit", 10)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            if "limit" in params and tool_name == "get_user_tweets":
                tool_args["limit"] = limit

            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
            return {"response": "", "data": data}

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY
        # ---------------------
        if query:
            identifier = self._extract_username_from_query(query)

            if not identifier:
                return {"error": "Could not extract a valid username or user ID from the query"}

            logger.info(f"Extracted identifier: '{identifier}' from query: '{query}'")

            function_args = {"username": identifier, "limit": limit}
            data = await self._handle_tool_logic(tool_name="get_user_tweets", function_args=function_args)

            if "error" in data:
                return {"response": f"Error: {data['error']}", "data": data}

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                query=query,
                tool_call_id="twitter_profile_query",
                data=data,
                temperature=0.7,
            )

            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
