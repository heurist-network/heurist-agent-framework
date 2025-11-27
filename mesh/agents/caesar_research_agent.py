import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

# Configuration
COMPUTE_UNITS = 4  # CU (Compute Units)


class CaesarResearchAgent(MeshAgent):
    _active_calls = 0

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CAESAR_API_KEY")
        if not self.api_key:
            raise ValueError("CAESAR_API_KEY environment variable is required")

        self.base_url = "https://api.caesar.xyz"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Caesar Research Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Advanced research agent using Caesar AI to find and analyze academic papers, articles, and authoritative sources.",
                "external_apis": ["Caesar"],
                "tags": ["Research", "Academic", "Citations"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Caesar.png",
                "examples": [
                    "What is Heurist Mesh?",
                    "What is x402-vending machine by Heurist Mesh?",
                    "How does Heurist decentralized AI infrastructure work?",
                    "Latest developments in AI safety research",
                ],
                "credits": 10,
                "x402_config": {
                    "enabled": True,
                    "tool_prices": {"caesar_research": "0.1", "get_research_result": "0.001"},
                },
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an AI research assistant that helps users find and analyze authoritative academic and research sources using Caesar AI.

You have two tools:
1. caesar_research: Submit a research query and get a research_id back immediately
2. get_research_result: Check the status and retrieve the result using the research_id

Research typically takes 2-3 minutes to complete. When a user asks for research, submit it with caesar_research, inform them it will take several minutes, and then use get_research_result to check the status and retrieve the result."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "caesar_research",
                    "description": "Submit a research query to perform in-depth research on a topic using Caesar AI. Returns a research ID immediately. Use get_research_result with the returned ID to retrieve result when ready.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The research question or topic to investigate. Be specific and clear.",
                            }
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_research_result",
                    "description": "Retrieve the results of a Caesar research query by its research ID. Returns the research status and result if completed. Status can be 'queued', 'researching', 'completed', or 'failed'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "research_id": {
                                "type": "string",
                                "description": "The research ID returned by caesar_research tool.",
                            }
                        },
                        "required": ["research_id"],
                    },
                },
            },
        ]

    async def _create_research_object(self, query: str) -> Dict[str, Any]:
        """Create a research object and return the job ID"""
        logger.info(f"Creating Caesar research object for query: {query}")

        url = f"{self.base_url}/research"
        payload = {"query": query, "compute_units": COMPUTE_UNITS}

        response = await self._api_request(url=url, method="POST", headers=self.headers, json_data=payload)

        if "error" in response:
            logger.error(f"Caesar API error: {response['error']}")
            return {"status": "error", "error": response["error"]}

        research_id = response.get("id")
        status = response.get("status")

        if not research_id:
            logger.error("No research ID returned from Caesar API")
            return {"status": "error", "error": "Failed to create research object"}

        logger.info(f"Research object created: {research_id}, status: {status}")
        return {"status": "success", "id": research_id, "initial_status": status}

    async def _get_research_object(self, research_id: str) -> Dict[str, Any]:
        """Retrieve research object by ID"""
        logger.info(f"Retrieving Caesar research object: {research_id}")

        url = f"{self.base_url}/research/{research_id}"

        response = await self._api_request(url=url, method="GET", headers=self.headers)

        if "error" in response:
            logger.error(f"Caesar API error: {response['error']}")
            return {"status": "error", "error": response["error"]}

        return {"status": "success", "data": response}

    @with_retry(max_retries=3)
    async def caesar_research(self, query: str) -> Dict[str, Any]:
        """
        Submit a research query to Caesar AI and return the research ID immediately.
        The research will process in the background.
        """
        logger.info(f"Submitting Caesar research for: {query} with {COMPUTE_UNITS} CU")

        create_result = await self._create_research_object(query)

        if create_result.get("status") != "success":
            return create_result

        research_id = create_result["id"]
        initial_status = create_result.get("initial_status", "queued")

        logger.info(f"Research submitted with ID: {research_id}, initial status: {initial_status}")

        return {
            "status": "success",
            "data": {
                "research_id": research_id,
                "query": query,
                "initial_status": initial_status,
                "message": f"Research submitted successfully. Use get_research_result with research_id '{research_id}' to retrieve result (typically takes 2-3 minutes with CU=4).",
            },
        }

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_research_result(self, research_id: str) -> Dict[str, Any]:
        """
        Retrieve the results of a Caesar research query by its research ID.
        Returns the current status and result if completed.
        """
        logger.info(f"Fetching research result for ID: {research_id}")

        retrieve_result = await self._get_research_object(research_id)

        if retrieve_result.get("status") != "success":
            return retrieve_result

        data = retrieve_result["data"]
        research_status = data.get("status")

        logger.info(f"Research status: {research_status}")

        if research_status == "completed":
            content = data.get("content", "")
            logger.info(f"Research completed with content length: {len(content)} characters")

            return {
                "status": "success",
                "data": {
                    "research_status": research_status,
                    "id": data.get("id"),
                    "query": data.get("query"),
                    "created_at": data.get("created_at"),
                    "completed_at": data.get("completed_at"),
                    "content": content,
                },
            }

        elif research_status == "failed":
            error_msg = data.get("error", "Research failed")
            logger.error(f"Research failed: {error_msg}")
            return {"status": "error", "error": f"Research failed: {error_msg}"}

        elif research_status in ["queued", "researching"]:
            logger.info(f"Research still in progress: {research_status}")
            return {
                "status": "success",
                "data": {
                    "research_status": research_status,
                    "id": data.get("id"),
                    "query": data.get("query"),
                    "created_at": data.get("created_at"),
                    "message": f"Research is still {research_status}. Please check again in a few minutes.",
                },
            }

        else:
            logger.warning(f"Unknown research status: {research_status}")
            return {"status": "error", "error": f"Unknown status: {research_status}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "caesar_research":
            query = function_args.get("query")
            if not query:
                return {"error": "Missing 'query' parameter"}

            CaesarResearchAgent._active_calls += 1
            logger.info(f"Active Caesar API calls: {CaesarResearchAgent._active_calls}")

            try:
                result = await self.caesar_research(query)

                if errors := self._handle_error(result):
                    return errors

                return result
            finally:
                CaesarResearchAgent._active_calls -= 1
                logger.info(f"Active Caesar API calls: {CaesarResearchAgent._active_calls}")

        elif tool_name == "get_research_result":
            research_id = function_args.get("research_id")
            if not research_id:
                return {"error": "Missing 'research_id' parameter"}

            result = await self.get_research_result(research_id)

            if errors := self._handle_error(result):
                return errors

            return result

        else:
            return {"error": f"Unsupported tool: {tool_name}"}
