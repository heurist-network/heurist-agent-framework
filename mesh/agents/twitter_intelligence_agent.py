import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

DEFAULT_TIMELINE_LIMIT = 20  # user_timeline default page size
DEFAULT_REPLIES_LIMIT = 25  # tweet_detail default replies size
MIN_AUTHOR_FOLLOWERS = 50  # default author filter
MIN_TOTAL_ENGAGEMENT = 1  # likes+replies+retweets+quotes >= 1

SEARCH_LIMIT_MIN = 5
SEARCH_LIMIT_MAX = 15
SEARCH_LIMIT_DEFAULT = 10


class TwitterIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Twitter Intelligence Agent",
                "version": "2.1.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Twitter/X tools (timeline, tweet detail, search)",
                "external_apis": ["Twitter/X", "Influential mentions"],
                "tags": ["Twitter", "Social"],
                "verified": True,
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/twitter-agent.png",
                "examples": [
                    "user_timeline(identifier='@heurist_ai')",
                    "tweet_detail(tweet_id='1975788185671389308')",
                    "tweet_detail(tweet_id='1975788185671389308', show_thread=true)",
                    "twitter_search(queries=['#ETH','SOL'], limit=15)",
                ],
                "credits": 10,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
                "erc8004": {
                    "enabled": True,
                    "supported_trust": ["reputation"],
                    "wallet_chain_id": 1,
                },
            }
        )

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 50

    def get_system_prompt(self) -> str:
        return """You are a Twitter/X intelligence specialist that helps users retrieve and analyze Twitter data.
You have access to tools for fetching user timelines, tweet details with threads/replies, and searching Twitter content.
Provide clear, structured information from Twitter/X to help users understand social media discussions and activity."""

    # -----------------------------
    # Tool surface
    # -----------------------------
    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "user_timeline",
                    "description": "Fetch a Twitter/X user's recent posts. Use when you want their latest activity or official announcements.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "identifier": {"type": "string", "description": "User handle (with @) or numeric user_id"},
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tweets to return",
                                "minimum": 5,
                                "maximum": 50,
                                "default": DEFAULT_TIMELINE_LIMIT,
                            },
                            "cursor": {"type": "string", "description": "Pagination cursor from a prior call"},
                        },
                        "required": ["identifier"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tweet_detail",
                    "description": "Get a tweet with its thread context and replies. Use this to read a single tweet or the full conversation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tweet_id": {"type": "string", "description": "The tweet ID"},
                            "cursor": {"type": "string", "description": "Pagination cursor for next replies page"},
                            "replies_limit": {
                                "type": "integer",
                                "description": "Max number of replies to return",
                                "default": DEFAULT_REPLIES_LIMIT,
                                "minimum": 1,
                                "maximum": 50,
                            },
                            "show_thread": {
                                "type": "boolean",
                                "description": "If true, include the entire thread including all replies; default shows only the main tweet.",
                                "default": False,
                            },
                        },
                        "required": ["tweet_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "twitter_search",
                    "description": "Search Twitter/X for posts and influential mentions of the query. Use this tool to find discussions about news, crypto, blockchain projects, or any other topic of interest.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "1-3 search terms (e.g., 'bitcoin', '$ETH', '@coinbase', '\"exact phrase\"'). Case insensitive. Do not query the same term with variations of case or synonyms. Each of the queries should be within [English: one word or two-word phrase] [Chinese or Korean: one word, no more than 5 characters]. One query should be one concept only. Never use long sentences or long phrases as keywords.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of tweets to return.",
                                "default": SEARCH_LIMIT_DEFAULT,
                                "minimum": SEARCH_LIMIT_MIN,
                                "maximum": SEARCH_LIMIT_MAX,
                            },
                        },
                        "required": ["queries"],
                    },
                },
            },
        ]

    async def _get_user_tweets(self, username: str, limit: int, cursor: Optional[str]) -> Dict[str, Any]:
        args = {"username": username, "limit": limit}
        if cursor:
            args["cursor"] = cursor
        return await self._call_agent_tool(
            "mesh.agents.twitter_info_agent",
            "TwitterInfoAgent",
            "get_user_tweets",
            args,
        )

    async def _tweet_detail(self, tweet_id: str, cursor: Optional[str]) -> Dict[str, Any]:
        args = {"tweet_id": tweet_id}
        if cursor:
            args["cursor"] = cursor
        return await self._call_agent_tool(
            "mesh.agents.twitter_info_agent",
            "TwitterInfoAgent",
            "get_twitter_detail",
            args,
        )

    async def _search(self, q: str, limit: int) -> Dict[str, Any]:
        return await self._call_agent_tool(
            "mesh.agents.twitter_info_agent",
            "TwitterInfoAgent",
            "get_general_search",
            {"q": q, "limit": limit, "sort_by": "Latest"},
        )

    async def _elfa_mentions(self, keywords: List[str], limit: int) -> Dict[str, Any]:
        # default days_ago=29
        return await self._call_agent_tool(
            "mesh.agents.elfa_twitter_intelligence_agent",
            "ElfaTwitterIntelligenceAgent",
            "search_mentions",
            {"keywords": keywords, "limit": max(SEARCH_LIMIT_MIN, min(SEARCH_LIMIT_MAX, limit))},
        )

    def _simplify_tweet(self, t: Dict[str, Any], include_replies: bool = False) -> Optional[Dict[str, Any]]:
        """
        Normalize a single tweet from TwitterInfoAgent's simplified tweet.
        Expects keys: id, text, created_at, author{username,name,verified,followers}, engagement{likes,replies,retweets,quotes,views}, type, media{type,urls}

        Args:
            t: The tweet dictionary to simplify
            include_replies: If True, don't filter out reply tweets (useful for tweet_detail)
        """
        if not t or not t.get("id"):
            return None
        # Enforce defaults: exclude retweets & replies (unless include_replies=True); include quotes
        tweet_type = t.get("type")
        if tweet_type == "retweet":
            return None
        if tweet_type == "reply" and not include_replies:
            return None
        if (t.get("author", {}) or {}).get("followers", 0) < MIN_AUTHOR_FOLLOWERS:
            return None
        eng = t.get("engagement", {}) or {}
        total = (
            int(eng.get("likes", 0))
            + int(eng.get("replies", 0))
            + int(eng.get("retweets", 0))
            + int(eng.get("quotes", 0))
        )
        if total < MIN_TOTAL_ENGAGEMENT:
            return None

        # Build engagement dict with only non-zero values
        engagement = {}
        for key in ["likes", "replies", "retweets", "quotes", "views"]:
            value = int(eng.get(key, 0))
            if value > 0:
                engagement[key] = value

        # Keep ID internally for deduplication but mark it as internal
        result = {
            "_id": str(t["id"]),  # Internal ID for deduplication
            "text": t.get("text", ""),
            "created_at": t.get("created_at", ""),
            "source": t.get("source", ""),
            "author": {
                "name": (t.get("author") or {}).get("name"),
                "followers": (t.get("author") or {}).get("followers", 0),
            },
            "type": t.get("type", "tweet"),
            # "media": t.get("media", {"type": "", "urls": []}),
        }

        result["engagement"] = engagement

        if t.get("urls"):
            space_urls = [url for url in t.get("urls", []) if "/spaces/" in url]
            if space_urls:
                result["space_urls"] = space_urls

        if t.get("quoted_tweet"):
            result["quoted_tweet"] = t.get("quoted_tweet")

        if t.get("in_reply_to_tweet_id"):
            result["in_reply_to"] = {
                "text": t.get("in_reply_to_tweet_text", ""),
            }

        if t.get("article"):
            result["article"] = t.get("article")

        return result

    def _remove_internal_ids(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove internal _id field from final output."""
        for item in items:
            if item and "_id" in item:
                del item["_id"]
        return items

    def _dedupe_keep_best(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate by _id; if duplicates exist, keep the one with higher total engagement."""
        best: Dict[str, Dict[str, Any]] = {}
        for x in items:
            if not x:
                continue
            tid = x.get("_id")
            if not tid:
                continue
            cur = best.get(tid)
            score = sum(
                int(x.get("engagement", {}).get(k, 0) or 0) for k in ("likes", "replies", "retweets", "quotes", "views")
            )
            if not cur:
                best[tid] = x
            else:
                old = sum(
                    int(cur.get("engagement", {}).get(k, 0) or 0)
                    for k in ("likes", "replies", "retweets", "quotes", "views")
                )
                if score > old:
                    best[tid] = x
        return list(best.values())

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "user_timeline":
            identifier = function_args["identifier"]
            limit = int(function_args.get("limit", DEFAULT_TIMELINE_LIMIT))
            cursor = function_args.get("cursor")

            raw = await self._get_user_tweets(identifier, limit=limit, cursor=cursor)
            if "error" in raw:
                return raw

            profile = ((raw.get("twitter_data") or {}).get("profile")) or raw.get("profile") or {}
            tweets = ((raw.get("twitter_data") or {}).get("tweets")) or raw.get("tweets") or []
            next_cursor = raw.get("next_cursor")

            normalized = [self._simplify_tweet(t) for t in tweets]
            items = [x for x in normalized if x is not None]
            if limit and len(items) > limit:
                items = items[:limit]

            self._remove_internal_ids(items)

            data = {
                "profile": {
                    "username": profile.get("screen_name") or profile.get("username"),
                    "name": profile.get("name"),
                    "description": profile.get("description"),
                    "verified": bool(profile.get("verified", False)),
                    "followers": profile.get("followers_count") or profile.get("followers", 0),
                },
                "items": items,
                "next_cursor": next_cursor,
            }
            if next_cursor:
                data["next_tool_tips"] = [f"Call user_timeline again with cursor={next_cursor} to load more."]
            return {"status": "success", "data": data}

        if tool_name == "tweet_detail":
            tweet_id = function_args["tweet_id"]
            cursor = function_args.get("cursor")
            replies_limit = int(function_args.get("replies_limit", DEFAULT_REPLIES_LIMIT))
            show_thread = bool(function_args.get("show_thread", False))

            raw = await self._tweet_detail(tweet_id, cursor=cursor)
            if "error" in raw:
                return raw

            data = raw.get("tweet_data") or raw
            main = data.get("main_tweet")
            in_reply_to = data.get("in_reply_to")  # Parent tweet if main is a reply
            thread = data.get("thread_tweets") or data.get("thread") or []
            replies = data.get("replies") or []
            next_cursor = data.get("next_cursor") or raw.get("next_cursor")

            # Always include the main tweet even if it's a reply (don't filter it out)
            main_item = self._simplify_tweet(main, include_replies=True) if main else None
            in_reply_to_item = self._simplify_tweet(in_reply_to, include_replies=True) if in_reply_to else None

            # Apply filters to thread/replies and clamp replies
            # Note: thread tweets can be replies in a thread, so include_replies=True
            thread_items = [self._simplify_tweet(t, include_replies=True) for t in thread]
            thread_items = [x for x in thread_items if x is not None]

            reply_items = [self._simplify_tweet(t, include_replies=True) for t in replies]
            reply_items = [x for x in reply_items if x is not None][:replies_limit]

            self._remove_internal_ids([main_item, in_reply_to_item] + thread_items + reply_items)

            data: Dict[str, Any] = {"main": main_item}

            # If main is a reply, include the parent tweet
            if in_reply_to_item:
                data["in_reply_to"] = in_reply_to_item

            if show_thread:
                # Only include non-empty fields
                if thread_items:
                    data["thread"] = thread_items
                if reply_items:
                    data["replies"] = reply_items
                if next_cursor:
                    data["next_cursor"] = next_cursor
                    data["next_tool_tips"] = [
                        f"Call tweet_detail again with cursor={next_cursor} to fetch more replies."
                    ]
            else:
                # If there is more context but we're not showing it, add a helpful tip.
                needs_tip = (len(thread_items) + len(reply_items)) > 0 or bool(next_cursor) or in_reply_to_item
                if needs_tip:
                    data["next_tool_tips"] = ["Pass show_thread=true to load the full thread and top replies."]

            return {"status": "success", "data": data}

        if tool_name == "twitter_search":
            # Retweets & replies removed; quotes included
            queries: List[str] = function_args.get("queries")
            if not queries:
                return {"status": "error", "error": "Missing required parameter: queries"}
            limit = int(function_args.get("limit", SEARCH_LIMIT_DEFAULT))
            limit = max(SEARCH_LIMIT_MIN, min(SEARCH_LIMIT_MAX, limit))

            # Query both sources: API Dance and Elfa
            # 1) Public search (per query) - run in parallel
            public_items: List[Dict[str, Any]] = []
            search_tasks = [self._search(q, limit=limit) for q in queries[:3]]
            search_results = await asyncio.gather(*search_tasks, return_exceptions=True)

            for i, pub_res in enumerate(search_results):
                if isinstance(pub_res, Exception) or "error" in pub_res:
                    logger.info(f"Public search error for '{queries[i]}': {pub_res}")
                    continue
                pub_tweets = (
                    (pub_res.get("search_data") or pub_res.get("tweets") or pub_res.get("items") or {}).get("tweets")
                    or (pub_res.get("search_data") or {}).get("tweets")
                    or pub_res.get("tweets")
                    or []
                )
                if pub_tweets:
                    public_items.extend([self._simplify_tweet(t) for t in pub_tweets])

            # 2) Influential mentions (batch)
            elfa_res = await self._elfa_mentions(queries[:3], limit=max(limit, 10))
            elfa_items = []
            if "error" not in elfa_res:
                # Elfa returns {"status":"success","data":[...]} with unwrapped tweet array
                data = elfa_res.get("data", [])
                candidates = data if isinstance(data, list) else []
                for t in candidates:
                    simplified = self._simplify_tweet(t)
                    if simplified:
                        elfa_items.append(simplified)
            else:
                logger.info(f"Elfa mentions warning: {elfa_res.get('error')}")

            # Deduplication: separate influential mentions from general search
            # Build a set of tweet IDs from elfa results
            elfa_tweet_ids = {item["_id"] for item in elfa_items if item.get("_id")}

            # Filter out public items that are already in elfa results
            general_items = []
            for item in public_items:
                if item and item.get("_id") not in elfa_tweet_ids:
                    general_items.append(item)

            # Sort both lists by newest first
            elfa_items.sort(key=lambda x: (x.get("created_at") or ""), reverse=True)
            general_items.sort(key=lambda x: (x.get("created_at") or ""), reverse=True)

            self._remove_internal_ids(elfa_items)
            self._remove_internal_ids(general_items)

            # Prepare response
            influential_mentions = elfa_items if elfa_items else "No influential account mentioning this topic is found"

            return {
                "status": "success",
                "data": {
                    "influential_mentions": influential_mentions,
                    "general_search_result": general_items,
                },
            }

        return {"status": "error", "error": f"Unsupported tool: {tool_name}"}
