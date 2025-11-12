import asyncio
import logging
import os
import random
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
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

        self.base_url = "https://api.elfa.ai/v2"
        self._update_headers()

        self.apidance_api_key = os.getenv("APIDANCE_API_KEY")
        if not self.apidance_api_key:
            raise ValueError("APIDANCE_API_KEY environment variable is required")
        self.apidance_base_url = "https://api.apidance.pro"

        self.metadata.update(
            {
                "name": "Elfa Twitter Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent analyzes a token or a topic or a Twitter account using Twitter data and Elfa API. It highlights smart influencers.",
                "external_apis": ["Elfa", "Apidance"],
                "tags": ["Twitter", "x402"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Elfa.png",
                "examples": [
                    "Search for mentions of Heurist, HEU, and heurist_ai in the last 30 days",
                    "Analyze the Twitter account @heurist_ai",
                    "Get trending tokens on Twitter in the last 24 hours",
                    "What are people talking about ETH and SOL this week?",
                ],
                "credits": 10,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
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
            logger.info("Rotated API key")

    def get_system_prompt(self) -> str:
        return (
            "You are a specialized assistant that analyzes Twitter data for crypto tokens using ELFA API. "
            "Your responses should be clear, concise, and data-driven.\n"
            "NEVER make up data that is not returned from the tool."
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
                                "description": "Maximum number of results (minimum: 10, maximum: 20)",
                                "default": 10,
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
    #  Tweet enrichment using TwitterInfoAgent
    # ------------------------------------------------------------------------

    async def _fetch_single_tweet_detail(self, tweet_id: str) -> Optional[Dict]:
        try:
            result = await self._call_agent_tool(
                "mesh.agents.twitter_info_agent",
                "TwitterInfoAgent",
                "get_twitter_detail",
                {"tweet_id": tweet_id}
            )
            if "error" in result:
                logger.warning(f"Error fetching tweet {tweet_id}: {result.get('error')}")
                return None

            tweet_data = result.get("tweet_data") or result
            return tweet_data.get("main_tweet")
        except Exception as e:
            logger.warning(f"Failed to fetch tweet {tweet_id}: {str(e)}")
            return None

    async def _fetch_batch_tweet_details(
        self, tweet_ids: List[str], batch_size: int = 5, delay: float = 0.5
    ) -> List[Optional[Dict]]:
        """
        Fetch full tweet details with controlled parallelism.

        Args:
            tweet_ids: List of tweet IDs to fetch
            batch_size: Number of tweets to fetch in parallel
            delay: Delay between batches in seconds

        Returns:
            List of simplified tweet dicts in TwitterInfoAgent format
        """
        all_results = []

        for i in range(0, len(tweet_ids), batch_size):
            batch = tweet_ids[i : i + batch_size]
            logger.info(
                f"Processing batch {i // batch_size + 1}/{(len(tweet_ids) + batch_size - 1) // batch_size}: {len(batch)} tweets"
            )

            batch_tasks = [self._fetch_single_tweet_detail(tweet_id) for tweet_id in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            processed_results = []
            for tweet_id, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.warning(f"Exception fetching tweet {tweet_id}: {result}")
                    processed_results.append(None)
                else:
                    processed_results.append(result)

            all_results.extend(processed_results)

            if i + batch_size < len(tweet_ids):
                logger.debug(f"Waiting {delay}s before next batch...")
                await asyncio.sleep(delay)

        return all_results

    async def _enrich_tweets_with_text(self, tweets: List[Dict]) -> List[Dict]:
        """
        Enrich ELFA tweets using TwitterInfoAgent to get full tweet details.
        """
        tweet_ids = [tweet.get("tweetId") for tweet in tweets if tweet.get("tweetId")]

        if not tweet_ids:
            return []

        logger.info(f"Fetching full details for {len(tweet_ids)} tweets using TwitterInfoAgent")

        enriched_tweets = await self._fetch_batch_tweet_details(tweet_ids, batch_size=5, delay=2.0)

        result = [tweet for tweet in enriched_tweets if tweet is not None]

        logger.info(f"Successfully enriched {len(result)} out of {len(tweet_ids)} tweets")
        return result

    # ------------------------------------------------------------------------
    #                      ELFA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None) -> Dict:
        self._rotate_api_key()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"Making request to ELFA API: {endpoint}")
        return await self._api_request(url=url, method=method, headers=self.headers, params=params)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_mentions(self, keywords: List[str], days_ago: int = 29, limit: int = 10) -> Dict:
        if limit < 10:
            limit = 10
        elif limit > 20:
            limit = 20
        if days_ago > 29:
            days_ago = 29
        if len(keywords) > 5:
            keywords = keywords[:5]
            logger.warning(f"Truncated keywords to 5: {keywords}")

        try:
            end_time = int(time.time() - 60)
            start_time = int(end_time - (days_ago * 86400))

            params = {"keywords": ",".join(keywords), "from": start_time, "to": end_time, "limit": limit}

            result = await self._make_request("data/keyword-mentions", params=params)
            if "error" in result:
                logger.error(f"Error searching mentions: {result['error']}")
                return result
            if "data" in result:
                for tweet in result["data"]:
                    tweet.pop("id", None)
                    tweet.pop("twitter_id", None)
                    tweet.pop("twitter_user_id", None)

                result["data"] = await self._enrich_tweets_with_text(result["data"][:limit]) # seems api returns more than limit
            result.pop("metadata", None)

            logger.info(f"Successfully retrieved and enriched {len(result.get('data', []))} mentions")
            return {"status": "success", "data": result.get("data", [])}
        except Exception as e:
            logger.error(f"Exception in search_mentions: {str(e)}")
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_account_stats(self, username: str) -> Dict:
        logger.info(f"Getting account stats for username: {username}")
        try:
            if username.startswith("@"):
                username = username[1:]
            params = {"username": username}
            result = await self._make_request("account/smart-stats", params=params)
            if "error" in result:
                logger.error(f"Error getting account stats: {result['error']}")
                return result
            logger.info(f"Successfully retrieved account stats for {username}")
            return {"status": "success", "data": result}
        except Exception as e:
            logger.error(f"Exception in get_account_stats: {str(e)}")
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search_account(self, username: str, days_ago: int = 29, limit: int = 20) -> Dict:
        logger.info(f"Searching account for username: {username}, days_ago: {days_ago}, limit: {limit}")

        try:
            if username.startswith("@"):
                username = username[1:]
            account_stats_result = await self.get_account_stats(username)
            if "error" in account_stats_result:
                return account_stats_result
            mentions_result = await self.search_mentions([username], days_ago, limit)
            if "error" in mentions_result:
                return mentions_result
            logger.info(f"Successfully retrieved combined account data for {username}")
            return {
                "status": "success",
                "data": {
                    "account_stats": account_stats_result.get("data", {}),
                    "mentions": mentions_result.get("data", {}),
                },
            }

        except Exception as e:
            logger.error(f"Exception in search_account: {str(e)}")
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=3)
    async def get_trending_tokens(self, time_window: str = "24h") -> Dict:
        logger.info(f"Getting trending tokens for time window: {time_window}")

        try:
            params = {"timeWindow": time_window, "page": 1, "pageSize": 50, "minMentions": 5}
            result = await self._make_request("aggregations/trending-tokens", params=params)
            if "error" in result:
                logger.error(f"Error getting trending tokens: {result['error']}")
                return result

            # Extract token names only
            tokens = []
            if result.get("data") and result["data"].get("data"):
                tokens = [item.get("token") for item in result["data"]["data"] if item.get("token")]

            logger.info(f"Successfully retrieved {len(tokens)} trending tokens")
            return {"status": "success", "data": {"tokens": tokens}}
        except Exception as e:
            logger.error(f"Exception in get_trending_tokens: {str(e)}")
            return {"status": "error", "error": str(e)}

    # ------------------------------------------------------------------------
    #                      APIDANCE API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    async def get_tweet_detail(self, tweet_id: str, cursor: str = "") -> Dict:
        endpoint = "sapi/TweetDetail"
        params = {"tweet_id": tweet_id}
        if cursor:
            params["cursor"] = cursor
        headers = {"apikey": self.apidance_api_key}
        url = f"{self.apidance_base_url}/{endpoint}"
        try:
            result = await self._api_request(url=url, method="GET", headers=headers, params=params)
            return result if result else {"error": "Empty response from API"}
        except Exception as e:
            logger.error(f"Error fetching tweet {tweet_id}: {str(e)}")
            return {"error": f"Failed to fetch tweet details: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution and optional LLM explanation"""

        if "limit" in function_args:
            function_args["limit"] = max(function_args["limit"], 20)

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
