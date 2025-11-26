import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

# Configuration
COMPUTE_UNITS = 4  # CU (Compute Units) for Caesar API - controls research depth/quality
TIMEOUT_SECONDS = 100  # Total timeout for research completion
INITIAL_WAIT_SECONDS = 30  # Wait before first status check
RETRY_WAIT_SECONDS = 10  # Wait between retry attempts
MAX_RETRY_ATTEMPTS = 3  # Maximum number of status check retries


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
                "description": "Advanced research agent using Caesar AI to find and analyze academic papers, articles, and authoritative sources with citation scoring.",
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
                "credits": 2,
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an AI research assistant that helps users find and analyze authoritative academic and research sources using Caesar AI.
Your role is to facilitate research queries and present citation-scored results in a clear format."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "caesar_research",
                    "description": "Perform in-depth research on a topic using Caesar AI. Returns authoritative sources with citation scores. This operation may take 4-7 minutes to complete as it searches across academic databases and research papers.",
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
            }
        ]

    def get_default_timeout_seconds(self) -> Optional[int]:
        return TIMEOUT_SECONDS

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

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def caesar_research(self, query: str) -> Dict[str, Any]:
        """
        Perform research using Caesar AI with automatic polling for results.
        Uses configurable compute units and timeout settings.
        """
        logger.info(f"Executing Caesar research for: {query} with {COMPUTE_UNITS} CU")

        create_result = await self._create_research_object(query)

        if create_result.get("status") != "success":
            return create_result

        research_id = create_result["id"]
        logger.info(f"Research queued with ID: {research_id}, waiting {INITIAL_WAIT_SECONDS}s before first check")

        await asyncio.sleep(INITIAL_WAIT_SECONDS)

        for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
            logger.info(f"Checking research status (attempt {attempt}/{MAX_RETRY_ATTEMPTS})")

            retrieve_result = await self._get_research_object(research_id)

            if retrieve_result.get("status") != "success":
                return retrieve_result

            data = retrieve_result["data"]
            research_status = data.get("status")

            logger.info(f"Research status: {research_status}")

            if research_status == "completed":
                results = data.get("results", [])
                logger.info(f"Research completed with {len(results)} results")

                return {
                    "status": "success",
                    "data": {
                        "id": data.get("id"),
                        "query": data.get("query"),
                        "created_at": data.get("created_at"),
                        "completed_at": data.get("completed_at"),
                        "results": results,
                        "result_count": len(results),
                    },
                }

            elif research_status == "failed":
                error_msg = data.get("error", "Research failed")
                logger.error(f"Research failed: {error_msg}")
                return {"status": "error", "error": f"Research failed: {error_msg}"}

            elif research_status in ["queued", "researching"]:
                if attempt < MAX_RETRY_ATTEMPTS:
                    logger.info(f"Research in progress, waiting {RETRY_WAIT_SECONDS}s before retry")
                    await asyncio.sleep(RETRY_WAIT_SECONDS)
                else:
                    logger.warning(f"Research timeout after {TIMEOUT_SECONDS}s")
                    return {
                        "status": "error",
                        "error": f"Research timeout after {TIMEOUT_SECONDS}s. Research ID: {research_id}",
                    }
            else:
                logger.warning(f"Unknown research status: {research_status}")
                return {"status": "error", "error": f"Unknown status: {research_status}"}

        logger.warning("Max retries reached")
        return {"status": "error", "error": f"Research timeout. Research ID: {research_id}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name != "caesar_research":
            return {"error": f"Unsupported tool: {tool_name}"}

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
