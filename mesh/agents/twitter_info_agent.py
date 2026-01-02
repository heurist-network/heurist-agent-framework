import asyncio
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from apify_client import ApifyClient
from dotenv import load_dotenv
from loguru import logger

from decorators import with_cache
from mesh.mesh_agent import MeshAgent

load_dotenv()

DEFAULT_TIMELINE_LIMIT = 20


def _clean_tweet_text(text: str) -> str:
    if not text:
        return text
    cleaned = re.sub(r"https://t\.co/\S+", "", text)
    cleaned = re.sub(r"#\w+", "", cleaned) # remove hashtags
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _to_int(value) -> int:
    """Safely convert a value to int."""
    if value is None:
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _format_date_only(timestamp: str) -> str:
    if not timestamp:
        return ""
    # Already formatted as YYYY-MM-DD
    if len(timestamp) == 10 and timestamp.count("-") == 2:
        return timestamp
    try:
        if "T" in timestamp and timestamp[4] == "-":
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        else:
            dt = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return timestamp.split("T")[0] if "T" in timestamp and timestamp[4] == "-" else timestamp


class TwitterInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("APIDANCE_API_KEY")
        if not self.api_key:
            raise ValueError("APIDANCE_API_KEY environment variable is required")

        self.base_url = "https://api.apidance.pro"
        self.headers = {"apikey": self.api_key}

        self.apify_api_key = os.getenv("APIFY_API_KEY")
        if not self.apify_api_key:
            raise ValueError("APIFY_API_KEY environment variable is required")
        self.apify_client = ApifyClient(self.apify_api_key)
        self.apify_actor_id = "practicaltools/cheap-simple-twitter-api"

        self.metadata.update(
            {
                "name": "Twitter Profile Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent fetches a Twitter user's profile information and recent tweets. It's useful for getting project updates or tracking key opinion leaders (KOLs) in the space.",
                "external_apis": ["Twitter API"],
                "tags": ["Twitter"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Twitter.png",
                "examples": [
                    "Summarise recent updates of @heurist_ai",
                    "What has @elonmusk been tweeting lately?",
                    "Get the recent tweets from cz_binance",
                    "Search for 'bitcoin' (single word search)",
                    "Search for '#ETH' (hashtag search)",
                ],
                "credits": 5,
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a specialized Twitter analyst that helps users get information about Twitter profiles and their recent tweets.

        IMPORTANT RULES:
        1. When using get_general_search, ONLY use single keywords, hashtags, or mentions. Multi-word searches will likely return empty results.
        2. Keep your analysis factual and concise. Only use the data provided.
        3. NEVER make up data that is not returned from the tool.
        4. If a search returns no results, suggest using a single keyword instead of multiple words.

        Search examples that work: 'bitcoin', '#ETH', '@username', '"exact phrase"'
        Search examples that fail: 'latest bitcoin news', 'what people think about ethereum'
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_user_tweets",
                    "description": "Fetch recent tweets from a specific Twitter user's timeline. This tool retrieves the most recent posts from a user's profile, including their own tweets and retweets. Use this when you want to see what a specific person or organization has been posting recently, track their updates, or analyze their Twitter activity patterns. The tool returns tweet content, engagement metrics (likes, retweets, replies), and timestamps. Maximum 50 tweets can be retrieved per request.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Twitter username (with or without @) or numeric user ID",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tweets to return (max: 50)",
                                "default": 10,
                            },
                            "cursor": {
                                "type": "string",
                                "description": "Cursor to fetch the next page of tweets",
                            },
                        },
                        "required": ["username"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_twitter_detail",
                    "description": "Fetch detailed information about a specific tweet, including the full thread context and replies. This tool provides comprehensive data about a single tweet, including the original tweet content, any tweets in the same thread (if it's part of a conversation), and replies to the tweet. Use this when you need to understand the full context of a discussion, see how people are responding to a specific tweet, or analyze a Twitter thread. The tool returns the complete thread structure and engagement metrics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tweet_id": {
                                "type": "string",
                                "description": "The ID of the tweet to fetch details for",
                            },
                            "cursor": {
                                "type": "string",
                                "description": "Cursor to fetch the next page of tweets",
                            },
                        },
                        "required": ["tweet_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_general_search",
                    "description": "Search for tweets using a SINGLE keyword, hashtag, or mention. WARNING: Multi-word searches often return EMPTY results on X/Twitter. ONLY use: single words (e.g., 'bitcoin'), hashtags (e.g., '#ETH'), mentions (e.g., '@username'), or exact phrases in quotes (e.g., '\"market crash\"'). NEVER use sentences or multiple unquoted words like 'latest bitcoin news' or 'what people think'. If you need to search for a complex topic, break it down into single keyword searches. This tool searches Twitter's public timeline for tweets matching your query. Each search query should be ONE concept only.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "q": {
                                "type": "string",
                                "description": "The search query - MUST be a single keyword, hashtag (#example), mention (@username), or exact phrase in quotes. DO NOT use multiple words or sentences.",
                            },
                            "cursor": {
                                "type": "string",
                                "description": "Cursor to fetch the next page of tweets",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tweets to return",
                                "default": 20,
                            },
                        },
                        "required": ["q"],
                    },
                },
            },
        ]

    def get_twitter_user_endpoint(self) -> str:
        return f"{self.base_url}/1.1/users/show.json"

    def get_twitter_tweets_endpoint(self) -> str:
        return f"{self.base_url}/sapi/UserTweets"

    def get_twitter_detail_endpoint(self) -> str:
        return f"{self.base_url}/sapi/TweetDetail"

    def get_twitter_search_endpoint(self) -> str:
        return f"{self.base_url}/sapi/Search"

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    def _clean_username(self, username: str) -> str:
        """Remove @ symbol if present in username"""
        return username.strip().lstrip("@")

    def _is_numeric_id(self, input_str: str) -> bool:
        """Check if the input is a numeric ID"""
        return input_str.strip().isdigit()

    def _simplify_tweet_data(self, tweet: Dict) -> Dict:
        user = tweet.get("user", {}) or {}
        username = user.get("screen_name", "")
        tid = str(tweet.get("tweet_id") or tweet.get("id_str") or tweet.get("id") or "")
        text = tweet.get("text", "")
        created = tweet.get("created_at", "")
        # media_type = tweet.get("media_type") or ""
        # medias = tweet.get("medias") or []

        def _type(t: Dict) -> str:
            if t.get("is_retweet"):
                return "retweet"
            if t.get("is_reply"):
                return "reply"
            if t.get("is_quote"):
                return "quote"
            return "tweet"

        result = {
            "id": tid,
            "text": _clean_tweet_text(text),
            "created_at": _format_date_only(created),
            "source": f"x.com/{username}/status/{tid}" if username and tid else "",
            "author": {
                "id": user.get("id_str") or "",
                "name": user.get("name", ""),
                "verified": bool(user.get("verified", False)),
                "followers": _to_int(user.get("followers_count")),
            },
            "engagement": {
                "likes": _to_int(tweet.get("favorite_count")),
                "replies": _to_int(tweet.get("reply_count")),
                "retweets": _to_int(tweet.get("retweet_count")),
                "quotes": _to_int(tweet.get("quote_count")),
                "views": _to_int(tweet.get("view_count")),
            },
            "type": _type(tweet),
            # "media": {"type": media_type, "urls": medias},
        }

        # Include URLs if they exist (for x spaces)
        if tweet.get("urls"):
            result["urls"] = tweet.get("urls")

        if tweet.get("in_reply_to_status_id_str"):
            result["in_reply_to_tweet_id"] = tweet.get("in_reply_to_status_id_str")
            result["in_reply_to_user"] = tweet.get("in_reply_to_status", {}).get("user", {}).get("screen_name", "")
            result["in_reply_to_tweet_text"] = _clean_tweet_text(tweet.get("in_reply_to_status", {}).get("text", ""))
        # Store the ID so it can be fetched later if fetch_quoted=True
        if tweet.get("is_quote") and tweet.get("related_tweet_id"):
            result["quoted_tweet_id"] = str(tweet["related_tweet_id"])

        return result

    # ------------------------------------------------------------------------
    #                      APIFY FALLBACK METHODS
    # ------------------------------------------------------------------------
    def _simplify_apify_tweet(self, tweet: Dict) -> Dict:
        """Convert practicaltools Apify tweet format to our standard format."""
        author = tweet.get("author") or {}
        username = author.get("userName") or ""
        tid = str(tweet.get("id") or "")

        def _tweet_type(t: Dict) -> str:
            if t.get("isRetweet"):
                return "retweet"
            if t.get("isReply"):
                return "reply"
            if t.get("isQuote"):
                return "quote"
            return "tweet"

        return {
            "id": tid,
            "text": _clean_tweet_text(tweet.get("text") or tweet.get("fullText") or ""),
            "created_at": _format_date_only(tweet.get("createdAt") or ""),
            "source": f"x.com/{username}/status/{tid}" if username and tid else "",
            "author": {
                "id": str(author.get("id") or ""),
                "name": author.get("name") or "",
                "verified": bool(author.get("isVerified") or author.get("isBlueVerified") or False),
                "followers": _to_int(author.get("followers")),
            },
            "engagement": {
                "likes": _to_int(tweet.get("likeCount")),
                "replies": _to_int(tweet.get("replyCount")),
                "retweets": _to_int(tweet.get("retweetCount")),
                "quotes": _to_int(tweet.get("quoteCount")),
                "views": _to_int(tweet.get("viewCount")),
            },
            "type": _tweet_type(tweet),
        }

    async def _apify_get_user_timeline(self, username: str, limit: int = 20) -> Dict:
        """Fallback: Get user timeline using Apify practicaltools actor."""
        clean_username = self._clean_username(username)
        logger.info(f"Apify fallback: fetching timeline for @{clean_username}")

        run_input = {"endpoint": "user/last_tweets", "parameters": {"userName": clean_username}}
        run = await asyncio.to_thread(lambda: self.apify_client.actor(self.apify_actor_id).call(run_input=run_input))
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            return {"error": "Apify actor returned no dataset"}

        items = list(self.apify_client.dataset(dataset_id).iterate_items())
        if not items:
            return {"error": f"No tweets found for user @{clean_username}"}
        first_author = (items[0].get("author") or {}) if items else {}
        profile = {
            "id_str": str(first_author.get("id") or ""),
            "name": first_author.get("name") or "",
            "screen_name": first_author.get("userName") or clean_username,
            "description": first_author.get("description") or "",
            "followers_count": first_author.get("followers") or 0,
            "friends_count": first_author.get("following") or 0,
            "statuses_count": first_author.get("statusesCount") or 0,
            "verified": bool(first_author.get("isVerified") or first_author.get("isBlueVerified")),
            "created_at": first_author.get("createdAt") or "",
        }

        tweets = [self._simplify_apify_tweet(t) for t in items[:limit]]
        logger.info(f"Apify fallback: retrieved {len(tweets)} tweets for @{clean_username}")
        return {"profile": profile, "tweets": tweets}

    # ------------------------------------------------------------------------
    #                      TWITTER API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    async def get_user_id(self, identifier: str) -> Dict:
        """Fetch Twitter user ID and profile information using _api_request"""
        try:
            params = {}
            if self._is_numeric_id(identifier):
                params = {"user_id": identifier}
            else:
                clean_username = self._clean_username(identifier)
                params = {"screen_name": clean_username}

            logger.info(f"Fetching user profile for identifier: {identifier}")
            user_data = await self._api_request(
                url=self.get_twitter_user_endpoint(), method="GET", headers=self.headers, params=params
            )

            if "error" in user_data:
                logger.error(f"Error fetching user profile: {user_data['error']}")
                return user_data

            profile_info = {
                "id_str": user_data.get("id_str"),
                "name": user_data.get("name"),
                "screen_name": user_data.get("screen_name"),
                "description": user_data.get("description"),
                "followers_count": user_data.get("followers_count"),
                "friends_count": user_data.get("friends_count"),
                "statuses_count": user_data.get("statuses_count"),
                "verified": user_data.get("verified", False),
                "created_at": user_data.get("created_at"),
            }

            logger.info(f"Successfully fetched profile for user: {profile_info.get('screen_name')}")
            return {"profile": profile_info}

        except Exception as e:
            logger.error(f"Error in get_user_id: {e}")
            return {"error": f"Failed to fetch user profile: {str(e)}"}

    @with_cache(ttl_seconds=300)
    async def get_tweets(self, user_id: str, limit: int = DEFAULT_TIMELINE_LIMIT, cursor: Optional[str] = None) -> Dict:
        params = {"user_id": user_id, "count": min(limit, 50)}
        if cursor:
            params["cursor"] = cursor
        tweets_data = await self._api_request(
            url=self.get_twitter_tweets_endpoint(), method="GET", headers=self.headers, params=params
        )
        if "error" in tweets_data:
            return tweets_data

        # accept either {tweets:[...]} or {data:{tweets:[...], cursor:...}}
        root = tweets_data.get("data") if isinstance(tweets_data, dict) else None
        tweets = (root or tweets_data).get("tweets", [])
        next_cursor = (root or tweets_data).get("cursor")

        cleaned = [self._simplify_tweet_data(t) for t in tweets]
        return {"tweets": cleaned, "next_cursor": next_cursor}

    @with_cache(ttl_seconds=300)
    async def get_tweet_detail(self, tweet_id: str, cursor: Optional[str] = None) -> Dict:
        params = {"tweet_id": tweet_id}
        if cursor:
            params["cursor"] = cursor
        tweet_data = await self._api_request(
            url=self.get_twitter_detail_endpoint(), method="GET", headers=self.headers, params=params
        )
        if not tweet_data:
            return {"error": "get_twitter_detail_endpoint failed or empty response"}
        if "error" in tweet_data:
            return tweet_data

        root = tweet_data.get("data") or tweet_data
        tweets = root.get("tweets", [])
        next_cursor = root.get("cursor")

        result = {"main_tweet": None}

        # First pass: find the main tweet and identify if it's a reply
        is_main_a_reply = False
        parent_tweet_id = None

        for t in tweets:
            tid = str(t.get("tweet_id") or t.get("id_str") or t.get("id") or "")
            if tid == tweet_id:
                is_main_a_reply = t.get("is_reply", False)
                if is_main_a_reply:
                    parent_tweet_id = t.get("related_tweet_id")
                break

        # Get main tweet author for thread detection
        main_tweet_author = None
        for t in tweets:
            tid = str(t.get("tweet_id") or t.get("id_str") or t.get("id") or "")
            if tid == tweet_id:
                main_tweet_author = (t.get("user", {}) or {}).get("screen_name")
                break

        # Temporary lists for categorization
        thread_tweets = []
        replies = []

        # Second pass: categorize all tweets
        for t in tweets:
            s = self._simplify_tweet_data(t)
            tid = s["id"]
            tweet_author = s.get("author", {}).get("username")

            if tid == tweet_id:
                # This is the main tweet we requested
                result["main_tweet"] = s
            elif is_main_a_reply and tid == parent_tweet_id:
                # This is the parent tweet that the main tweet is replying to
                result["in_reply_to"] = s
            elif s["type"] == "reply" and tweet_author == main_tweet_author:
                # Thread tweet: reply by the same author (continuing their own thread)
                thread_tweets.append(s)
            elif s["type"] == "reply":
                # Actual reply: reply by a different author (commenting on the tweet)
                replies.append(s)
            else:
                # Regular tweet (not a reply), could be part of a thread
                thread_tweets.append(s)

        # Only include fields with data
        if thread_tweets:
            result["thread_tweets"] = thread_tweets
        if replies:
            result["replies"] = replies
        if next_cursor:
            result["next_cursor"] = next_cursor

        if result["main_tweet"] and result["main_tweet"].get("quoted_tweet_id"):
            quoted_id = result["main_tweet"]["quoted_tweet_id"]
            try:
                quoted_result = await self.get_tweet_detail(quoted_id, cursor=None)
                if "error" not in quoted_result and quoted_result.get("main_tweet"):
                    quoted_tweet = quoted_result["main_tweet"]
                    result["main_tweet"]["quoted_tweet"] = quoted_tweet
                else:
                    result["main_tweet"]["quoted_tweet"] = {"id": quoted_id}
            except Exception as e:
                logger.warning(f"Failed to fetch quoted tweet {quoted_id}: {e}")
                result["main_tweet"]["quoted_tweet"] = {"id": quoted_id}

            del result["main_tweet"]["quoted_tweet_id"]

        return result

    @with_cache(ttl_seconds=300)
    async def general_search(
        self, query: str, sort_by: str = "Latest", cursor: Optional[str] = None, limit: Optional[int] = None
    ) -> Dict:
        if " " in query and not (query.startswith('"') and query.endswith('"')):
            logger.warning(f"Multi-word search query detected: '{query}' (likely sparse results).")
        params = {"q": query, "sort_by": sort_by}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["count"] = limit

        search_data = await self._api_request(
            url=self.get_twitter_search_endpoint(), method="GET", headers=self.headers, params=params
        )
        if "error" in search_data:
            return search_data

        root = search_data.get("data") if isinstance(search_data, dict) else None
        tweets = (root or search_data).get("tweets", [])
        next_cursor = (root or search_data).get("cursor")

        simplified = [self._simplify_tweet_data(t) for t in tweets]
        return {"query": query, "tweets": simplified, "result_count": len(simplified), "next_cursor": next_cursor}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution logic"""
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_user_tweets":
            identifier = function_args.get("username")
            limit = min(function_args.get("limit", 10), 50)
            cursor = function_args.get("cursor")

            if not identifier:
                return {"error": "Missing 'username' parameter"}

            logger.info(f"Fetching tweets for identifier '{identifier}' with limit={limit}")
            self.push_update(
                {"identifier": identifier}, f"Looking up Twitter user: @{self._clean_username(identifier)}..."
            )

            # Try apidance first
            profile_result = await self.get_user_id(identifier)
            apidance_failed = "error" in profile_result

            if not apidance_failed:
                user_id = profile_result.get("profile", {}).get("id_str")
                if user_id:
                    tweets_result = await self.get_tweets(user_id, limit, cursor)
                    if "error" not in tweets_result:
                        return {
                            "twitter_data": {
                                "profile": profile_result.get("profile", {}),
                                "tweets": tweets_result.get("tweets", []),
                            },
                            "next_cursor": tweets_result.get("next_cursor"),
                        }
                    apidance_failed = True
                else:
                    apidance_failed = True

            if apidance_failed:
                logger.warning(f"Primary API unavailable for @{self._clean_username(identifier)}, using Apify fallback")
                self.push_update({"identifier": identifier}, "Primary API failed, trying fallback...")
                fallback_result = await self._apify_get_user_timeline(identifier, limit)
                if "error" in fallback_result:
                    return fallback_result
                logger.warning(
                    f"Fallback success: retrieved {len(fallback_result.get('tweets', []))} tweets for @{self._clean_username(identifier)}"
                )
                return {
                    "twitter_data": {
                        "profile": fallback_result.get("profile", {}),
                        "tweets": fallback_result.get("tweets", []),
                    },
                    "next_cursor": None,
                }

        elif tool_name == "get_twitter_detail":
            tweet_id = function_args.get("tweet_id")
            cursor = function_args.get("cursor")
            if not tweet_id:
                return {"error": "Missing 'tweet_id' parameter"}

            logger.info(f"Fetching tweet details for tweet_id '{tweet_id}'")

            tweet_detail_result = await self.get_tweet_detail(tweet_id, cursor)
            errors = self._handle_error(tweet_detail_result)
            if errors:
                return errors

            return {"tweet_data": tweet_detail_result}

        elif tool_name == "get_general_search":
            query = function_args.get("q")
            cursor = function_args.get("cursor")
            limit = function_args.get("limit")
            sort_by = function_args.get("sort_by", "Latest")
            if not query:
                return {"error": "Missing 'q' parameter"}

            # Log warning for multi-word queries
            if " " in query and not (query.startswith('"') and query.endswith('"')):
                logger.warning(f"Multi-word search query: '{query}'. Suggesting single keyword search.")
                self.push_update(
                    {"query": query}, "Warning: Multi-word searches often return empty results. Searching anyway..."
                )

            logger.info(f"Performing general search for query '{query}'")

            search_result = await self.general_search(query, sort_by=sort_by, cursor=cursor, limit=limit)
            errors = self._handle_error(search_result)
            if errors:
                return errors

            return {"search_data": search_result}

        else:
            error_msg = f"Unsupported tool: {tool_name}"
            logger.error(error_msg)
            return {"error": error_msg}
