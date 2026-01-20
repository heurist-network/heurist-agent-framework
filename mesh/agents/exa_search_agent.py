import logging
import os
import random
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

NON_ROTATABLE_ERRORS = ["500", "404", "422", "not found", "unprocessable"]


class ExaSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        api_keys_str = os.getenv("EXA_API_KEY")
        if not api_keys_str:
            raise ValueError("EXA_API_KEY environment variable is required")

        self.api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]
        if not self.api_keys:
            raise ValueError("No valid API keys found in EXA_API_KEY")

        self.current_key_index = random.randint(0, len(self.api_keys) - 1)
        self.current_api_key = self.api_keys[self.current_key_index]

        logger.info(
            f"Exa agent initialized with {len(self.api_keys)} API key(s), "
            f"starting with index {self.current_key_index} (key: {self._mask_key(self.current_api_key)})"
        )

        self.base_url = "https://api.exa.ai"
        self._update_headers()

        self.metadata.update(
            {
                "name": "Exa Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search the web using Exa's API and provide direct answers to questions.",
                "external_apis": ["Exa"],
                "tags": ["Search"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Exa.png",
                "examples": [
                    "What is the latest news on Bitcoin?",
                    "Recent developments in quantum computing",
                    "Search for articles about the latest trends in AI",
                ],
            }
        )

    def _mask_key(self, key: str) -> str:
        """Returns masked API key for safe logging (e.g., 'abc1...xyz9')."""
        if len(key) <= 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"

    def _update_headers(self):
        """Updates request headers with the current API key."""
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.current_api_key}"}

    def _rotate_key(self) -> bool:
        """
        Rotates to the next API key in the list.

        Returns:
            True if rotation occurred, False if only one key is available.
        """
        if len(self.api_keys) <= 1:
            logger.warning("Only one API key available, cannot rotate")
            return False

        previous_index = self.current_key_index
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.current_api_key = self.api_keys[self.current_key_index]
        self._update_headers()

        logger.info(
            f"Rotated API key: index {previous_index} -> {self.current_key_index} "
            f"(key: {self._mask_key(self.current_api_key)})"
        )
        return True

    def _should_rotate(self, error_msg: str) -> bool:
        """
        Determines if the error should trigger key rotation.

        Returns:
            True if rotation should occur, False for non-rotatable errors (500/404/422).
        """
        error_lower = error_msg.lower()
        return not any(code in error_lower for code in NON_ROTATABLE_ERRORS)

    async def _request_with_key_rotation(
        self,
        url: str,
        method: str = "GET",
        headers: Dict = None,
        params: Dict = None,
        json_data: Dict = None,
        timeout: int = 30,
    ) -> Dict:
        """
        Makes an API request with automatic key rotation on rotatable errors.

        Tries each available API key once before giving up. Rotates on errors
        like 429 (rate limit) but not on 500, 404, or 422 errors.

        Args:
            url: API endpoint URL
            method: HTTP method (GET, POST, etc.)
            headers: Request headers (uses self.headers if None)
            params: URL query parameters
            json_data: JSON request body
            timeout: Request timeout in seconds

        Returns:
            API response dict or error dict
        """
        request_headers = headers or self.headers
        attempted_keys = set()
        last_error = None

        while len(attempted_keys) < len(self.api_keys):
            attempted_keys.add(self.current_key_index)
            logger.info(
                f"Exa API request with key index {self.current_key_index} "
                f"(key: {self._mask_key(self.current_api_key)})"
            )

            try:
                result = await super()._api_request(
                    url=url,
                    method=method,
                    headers=request_headers,
                    params=params,
                    json_data=json_data,
                    timeout=timeout,
                )

                if "error" in result:
                    error_msg = str(result.get("error", ""))
                    if not self._should_rotate(error_msg):
                        logger.error(f"Non-rotatable error: {result['error']}")
                        return result

                    logger.warning(f"Rotatable error encountered: {result['error']}")
                    last_error = result

                    if self._rotate_key():
                        request_headers = self.headers
                        continue
                    return result

                return result

            except Exception as e:
                error_msg = str(e)
                if not self._should_rotate(error_msg):
                    logger.error(f"Non-rotatable exception: {e}")
                    return {"error": error_msg}

                logger.warning(f"Exception during request, rotating key: {e}")
                last_error = {"error": error_msg}

                if self._rotate_key():
                    request_headers = self.headers
                    continue
                return {"error": error_msg}

        logger.error(f"All {len(self.api_keys)} API keys exhausted")
        return last_error or {"error": "All API keys exhausted"}

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
                    "description": "Search for webpages using Exa's neural search. Returns relevant results with titles, snippets, and URLs. Unlike traditional search, Exa uses semantic understanding (not boolean operators like AND/OR). Supports domain filtering and date filtering. Use includeDomains to restrict search to specific sites. Use date filters for time-sensitive queries.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "The search term or natural language query",
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of results to return (default: 10)",
                            },
                            "include_domains": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of domains to include in search (e.g., ['arxiv.org', 'papers.com']). Supports paths (e.g., 'example.com/blog') and wildcards (e.g., '*.substack.com')",
                            },
                            "start_published_date": {
                                "type": "string",
                                "description": "Only return results published after this date (ISO 8601 format: '2024-01-01T00:00:00.000Z')",
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
    async def exa_web_search(
        self,
        search_term: str,
        limit: int = 10,
        include_domains: Optional[List[str]] = None,
        start_published_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Uses Exa's /search endpoint to find webpages related to the search term.

        Args:
            search_term: The search query
            limit: Maximum number of results
            include_domains: List of domains to include (e.g., ['arxiv.org'])
            start_published_date: ISO 8601 format date string for filtering results published after this date
        """
        logger.info(f"Executing Exa web search for '{search_term}' with limit {limit}")

        try:
            url = f"{self.base_url}/search"
            payload = {"query": search_term, "numResults": limit, "contents": {"text": True}}

            # Add domain filters if specified
            if include_domains:
                payload["includeDomains"] = include_domains
                logger.info(f"Including domains: {include_domains}")

            # Add date filters if specified
            if start_published_date:
                payload["startPublishedDate"] = start_published_date
                logger.info(f"Filtering results published after: {start_published_date}")

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
            include_domains = function_args.get("include_domains")
            start_published_date = function_args.get("start_published_date")

            if not search_term:
                logger.error("Missing 'search_term' parameter")
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            # Ensure limit is at least 10
            if limit < 10:
                limit = 10

            result = await self.exa_web_search(search_term, limit, include_domains, start_published_date)

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
