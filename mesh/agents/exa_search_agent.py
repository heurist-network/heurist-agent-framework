import logging
import os
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class ExaSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")

        self.base_url = "https://api.exa.ai"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

        self.metadata.update(
            {
                "name": "Exa Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search the web using Exa's API and provide direct answers to questions.",
                "external_apis": ["Exa"],
                "tags": ["Search"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Exa.png",
                "examples": [
                    "What is the latest news on Bitcoin?",
                    "Recent developments in quantum computing",
                    "Search for articles about the latest trends in AI",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
    IDENTITY:
    You are a web search specialist that can find information using Exa's search and answer APIs.

    CAPABILITIES:
    - Search for webpages related to a query
    - Get direct answers to questions
    - Provide combined search-and-answer responses

    RESPONSE GUIDELINES:
    - Keep responses focused on what was specifically asked
    - Format information in a clear, readable way
    - Prioritize relevant, credible sources
    - Provide direct answers where possible, with supporting search results

    DOMAIN-SPECIFIC RULES:
    For search queries, use the search tool to find relevant webpages.
    For specific questions that need direct answers, use the answer tool.
    For complex queries, consider using both tools to provide comprehensive information.

    When presenting search results, apply these criteria:
    1. Prioritize recency and relevance
    2. Include source URLs where available
    3. Organize information logically and highlight key insights

    IMPORTANT:
    - Never invent or assume information not found in search results
    - Clearly indicate when information might be outdated
    - Keep responses concise and relevant"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "exa_web_search",
                    "description": "Search for webpages related to a query using Exa search. This tool performs a web search and returns relevant results including titles, snippets, and URLs. It's useful for finding up-to-date information on any topic, but may fail to find information of niche topics such like small cap crypto projects. Use this when you need to gather information from across the web.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "The search term"},
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 10)",
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "exa_answer_question",
                    "description": "Get a direct answer to a question using Exa's answer API. This tool provides concise, factual answers to specific questions by searching and analyzing content from across the web. Use this when you need a direct answer to a specific question rather than a list of search results. It may fail to find information of niche topics such like small cap crypto projects.",
                    "parameters": {
                        "type": "object",
                        "properties": {"question": {"type": "string", "description": "The question to answer"}},
                        "required": ["question"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      EXA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    @with_retry(max_retries=3)
    async def exa_web_search(self, search_term: str, limit: int = 10) -> Dict[str, Any]:
        """
        Uses Exa's /search endpoint to find webpages related to the search term.
        """
        logger.info(f"Executing Exa web search for '{search_term}' with limit {limit}")

        try:
            url = f"{self.base_url}/search"
            payload = {"query": search_term, "numResults": limit, "contents": {"text": True}}

            response = await self._api_request(url=url, method="POST", headers=self.headers, json_data=payload)

            if "error" in response:
                logger.error(f"Exa search API error: {response['error']}")
                return {"status": "error", "error": response["error"]}

            # Format the search results data
            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append(
                    {
                        "title": result.get("title", "N/A"),
                        "url": result.get("url", "N/A"),
                        "published_date": result.get("published_date", "N/A"),
                        "text": result.get("text", ""),
                    }
                )

            logger.info(f"Successfully retrieved {len(formatted_results)} search results")
            return {"status": "success", "data": {"search_results": formatted_results}}

        except Exception as e:
            logger.error(f"Exception in exa_web_search: {str(e)}")
            return {"status": "error", "error": f"Failed to execute search: {str(e)}"}

    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    @with_retry(max_retries=3)
    async def exa_answer_question(self, question: str) -> Dict[str, Any]:
        """
        Uses Exa's /answer endpoint to generate a direct answer based on the question.
        """
        logger.info(f"Getting Exa direct answer for '{question}'")

        try:
            url = f"{self.base_url}/answer"
            payload = {"query": question}  # API still uses 'query'

            response = await self._api_request(url=url, method="POST", headers=self.headers, json_data=payload)

            if "error" in response:
                logger.error(f"Exa answer API error: {response['error']}")
                return {"status": "error", "error": response["error"]}

            # Format the answer result
            answer_data = {
                "answer": response.get("answer", "No direct answer available"),
                "sources": [
                    {"title": source.get("title", "N/A"), "url": source.get("url", "N/A")}
                    for source in response.get("sources", [])
                ],
            }

            logger.info("Successfully retrieved direct answer")
            return {"status": "success", "data": answer_data}

        except Exception as e:
            logger.error(f"Exception in exa_answer_question: {str(e)}")
            return {"status": "error", "error": f"Failed to get answer: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle execution of specific tools and return the raw data.
        """
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "exa_web_search":
            search_term = function_args.get("search_term")
            limit = function_args.get("limit", 10)

            if not search_term:
                logger.error("Missing 'search_term' parameter")
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            # Ensure limit is at least 10
            if limit < 10:
                limit = 10

            result = await self.exa_web_search(search_term, limit)

        elif tool_name == "exa_answer_question":
            question = function_args.get("question")

            if not question:
                logger.error("Missing 'question' parameter")
                return {"status": "error", "error": "Missing 'question' parameter"}

            result = await self.exa_answer_question(question)

        else:
            logger.error(f"Unsupported tool: {tool_name}")
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result


# ---------------------
# Shared fallback helpers (used to fallback to Exa search when Firecrawl tools fail)
# ---------------------
def build_exa_search_fallback(search_term: str, limit: int = 10) -> Dict[str, Any]:
    """Build a fallback spec targeting Exa web search."""
    return {
        "module": "mesh.agents.exa_search_agent",
        "class": "ExaSearchAgent",
        "input": {"tool": "exa_web_search", "tool_arguments": {"search_term": search_term, "limit": limit}},
    }


def build_firecrawl_to_exa_fallback(
    tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Standard mapping from Firecrawl tools or NL queries to Exa search fallback.
    Returns a fallback spec or None when not applicable.
    """
    if tool_name == "firecrawl_web_search":
        search_term = function_args.get("search_term") or original_params.get("query") or ""
        limit = function_args.get("limit", 10)
        return build_exa_search_fallback(search_term, limit)
    if tool_name == "firecrawl_scrape_url":
        url = function_args.get("url") or ""
        return build_exa_search_fallback(url, 10)
    if tool_name == "firecrawl_extract_web_data":
        urls = function_args.get("urls") or []
        search_term = urls[0] if urls else (original_params.get("query") or "")
        return build_exa_search_fallback(search_term, 10)

    # Natural language mode (no explicit tool)
    if not tool_name:
        query = original_params.get("query") or ""
        return build_exa_search_fallback(query, 10)

    return None
