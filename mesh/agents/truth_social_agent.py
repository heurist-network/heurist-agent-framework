import json
import logging
import os
import re
from html import unescape
from typing import Any, Dict, List

from apify_client import ApifyClient
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
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
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about Trump's Truth Social posts",
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
                        "description": "Natural language explanation of Trump's Truth Social posts",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured Truth Social post data",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Apify"],
                "tags": ["Politics"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/trump.png",
                "examples": [
                    "Get the latest posts from Donald Trump",
                    "Analyze recent Truth Social content from Trump",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a Truth Social data analyst specializing in retrieving and analyzing content from Donald Trump's Truth Social account.

        CAPABILITIES:
        - Retrieve posts from Donald Trump's Truth Social profile
        - Summarize content from Trump's Truth Social
        - Identify key themes in Trump's posts

        RESPONSE GUIDELINES:
        - Provide objective analysis of the content
        - Focus on factual information without political bias
        - Format responses in a clear, readable way
        - When analyzing posts, highlight recurring themes and topics

        IMPORTANT:
        - Always provide context when referencing specific posts
        - Be aware that you're accessing publicly available information only
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
    #                      APIFY API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=1800)  # Cache for 30 minutes
    @with_retry(max_retries=3)
    async def get_trump_posts(self, profile: str = "@realDonaldTrump", max_posts: int = 20) -> Dict:
        """
        Retrieve recent posts from Donald Trump's Truth Social profile using Apify.
        """
        try:
            run_input = {
                "profiles": [profile],
                "resultsType": "posts",  # Available options : posts, replies, posts-and-replies, profile-details
                "maxPostsAndReplies": max_posts,
                "includeMuted": False,
            }

            run = self.client.actor("wFKNJUPPLyEg7pdgv").call(run_input=run_input)
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
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data
        """
        if tool_name == "get_trump_posts":
            profile = function_args.get("profile", "@realDonaldTrump")
            max_posts = function_args.get("max_posts", 20)

            logger.info(f"Retrieving Truth Social posts for profile: {profile}")
            result = await self.get_trump_posts(profile, max_posts)

            errors = self._handle_error(result)
            if errors:
                return errors

            return result

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

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
            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
            return {"response": "", "data": data}

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

            data = await self._handle_tool_logic(tool_name=tool_call_name, function_args=tool_call_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call.id, data=data, temperature=0.7
            )

            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}

    async def cleanup(self):
        pass
