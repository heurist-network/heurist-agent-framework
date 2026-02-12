import asyncio
import logging
import os
import re
from html import unescape
from typing import Any, Dict, List, Optional

from apify_client import ApifyClient
from dotenv import load_dotenv

from decorators import with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class TruthSocialAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        api_token = os.getenv("APIFY_API_KEY")
        if not api_token:
            raise ValueError("APIFY_API_KEY not found in environment variables.")
        self.client = ApifyClient(api_token)

        self.metadata.update(
            {
                "name": "Truth Social Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can retrieve and analyze posts from Donald Trump on Truth Social.",
                "external_apis": ["Apify"],
                "tags": ["Politics"],
                "verified": True,
                "hidden": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Trump.png",
                "examples": [
                    "Get the latest posts from Donald Trump",
                    "Analyze recent Truth Social content from Trump",
                ],
                "credits": {"default": 2},
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a Truth Social data analyst.

        CAPABILITIES:
        - Retrieve posts from Donald Trump's Truth Social profile
        - Summarize content from Trump's Truth Social
        - Identify key themes in Trump's posts

        RESPONSE GUIDELINES:
        - Provide objective analysis of the content
        - Focus on factual information without political bias
        - Format responses in a clear, readable way

        IMPORTANT:
        - NEVER make up data that is not returned from the tool
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_trump_posts",
                    "description": "Retrieve recent posts from Donald Trump's Truth Social profile. This tool fetches public posts from Trump's Truth Social feed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "profile": {
                                "type": "string",
                                "description": "Truth Social profile handle with @ symbol (defaults to @realDonaldTrump)",
                                "default": "@realDonaldTrump",
                            },
                            "max_posts": {
                                "type": "integer",
                                "description": "Maximum number of posts to retrieve",
                                "default": 20,
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    def _strip_html(self, html_text):
        """Remove HTML tags and unescape HTML entities from text"""
        clean = re.sub(r"<.*?>", "", html_text or "")
        return unescape(clean).strip()

    # ------------------------------------------------------------------------
    #                      APIFY API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_retry(max_retries=3)
    async def get_trump_posts(self, profile: str = "@realDonaldTrump", max_posts: int = 20) -> Dict:
        """
        Retrieve recent posts from Donald Trump's Truth Social profile using Apify.
        The Apify client library is synchronous so we run it in a thread.
        """
        try:
            run_input = {
                "profiles": [profile],
                "resultsType": "posts",  # Available options : posts, replies, posts-and-replies, profile-details
                "maxPostsAndReplies": max_posts,
                "includeMuted": False,
            }

            # Run the actor call in a background thread.
            run = await asyncio.to_thread(lambda: self.client.actor("wFKNJUPPLyEg7pdgv").call(run_input=run_input))
            dataset_id = run.get("defaultDatasetId")
            if not dataset_id:
                return {"error": "Failed to retrieve posts: No dataset returned"}

            dataset = self.client.dataset(dataset_id)
            items = list(dataset.iterate_items())

            posts = []
            for item in items:
                if "content" in item:
                    post = {
                        "content": self._strip_html(item.get("content", "")),
                        "created_at": item.get("createdAt", ""),
                        "likes": item.get("likeCount", 0),
                        "replies": item.get("replyCount", 0),
                        "reposts": item.get("repostCount", 0),
                        "url": item.get("url", ""),
                    }
                    posts.append(post)

            return {
                "profile": profile,
                "post_count": len(posts),
                "posts": posts,
            }

        except Exception as e:
            logger.error(f"Error retrieving Truth Social posts: {str(e)}")
            return {"error": f"Failed to retrieve Truth Social posts: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        Enforce a minimum of 20 posts regardless of user input.
        """
        if tool_name == "get_trump_posts":
            profile = function_args.get("profile", "@realDonaldTrump")
            user_supplied = function_args.get("max_posts", 20)
            # Enforce at least 20 posts.
            max_posts = user_supplied if user_supplied >= 20 else 20

            logger.info(f"Retrieving Truth Social posts for profile: {profile} with max_posts: {max_posts}")
            result = await self.get_trump_posts(profile, max_posts)

            errors = self._handle_error(result)
            if errors:
                return errors

            return result

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}
