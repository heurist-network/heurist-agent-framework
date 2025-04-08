import json
import logging
import os
from typing import Any, Dict, List

import requests

from core.llm import call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class ExaSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("EXA_API_KEY")
        self.base_url = "https://api.exa.ai"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

        self.metadata.update(
            {
                "name": "Exa Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can search the web using Exa's API and provide direct answers to questions.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query to search for on the web.",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw or base structured data without additional LLM explanation.",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of search results (empty if a direct tool call).",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured search results or direct answer data.", "type": "dict"},
                ],
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
    async def search(self, search_term: str, limit: int = 10) -> dict:
        """
        Uses Exa's /search endpoint to find webpages related to the search term.
        """
        try:
            url = f"{self.base_url}/search"
            payload = {"query": search_term, "numResults": limit, "contents": {"text": True}}

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            search_results = response.json()

            # Format the search results data
            formatted_results = []
            for result in search_results.get("results", []):
                formatted_results.append(
                    {
                        "title": result.get("title", "N/A"),
                        "url": result.get("url", "N/A"),
                        "published_date": result.get("published_date", "N/A"),
                        "text": result.get("text", ""),
                    }
                )

            return {"search_results": formatted_results}

        except requests.RequestException as e:
            logger.error(f"Search API error: {e}")
            return {"error": f"Failed to execute search: {str(e)}"}

    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    async def answer(self, question: str) -> dict:
        """
        Uses Exa's /answer endpoint to generate a direct answer based on the question.
        """
        try:
            url = f"{self.base_url}/answer"
            payload = {"query": question}  # API still uses 'query'

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            answer_result = response.json()

            # Return the formatted answer result
            return {
                "answer": answer_result.get("answer", "No direct answer available"),
                "sources": [
                    {"title": source.get("title", "N/A"), "url": source.get("url", "N/A")}
                    for source in answer_result.get("sources", [])
                ],
            }

        except requests.RequestException as e:
            logger.error(f"Answer API error: {e}")
            return {"error": f"Failed to get answer: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        if tool_name == "exa_web_search":
            search_term = function_args.get("search_term")
            limit = function_args.get("limit", 10)

            if not search_term:
                return {"error": "Missing 'search_term' in tool_arguments"}

            logger.info(f"Executing search for '{search_term}'")
            result = await self.search(search_term, limit)
            errors = self._handle_error(result)
            if errors:
                return errors
            return result

        elif tool_name == "exa_answer_question":
            question = function_args.get("question")

            if not question:
                return {"error": "Missing 'question' in tool_arguments"}

            logger.info(f"Getting direct answer for '{question}'")
            result = await self.answer(question)
            errors = self._handle_error(result)
            if errors:
                return errors

            return result
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

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
            # For a direct tool call, we do NOT use LLM, just return the result
            response = ""
            data = await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
            )
            return {"response": response, "data": data}

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
                # No tool calls => the LLM just answered
                return {"response": response["content"], "data": {}}

            # LLM provided a single tool call (or the first if multiple).
            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            data = await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
            )

            if raw_data_only:
                return {"response": "", "data": data}

            response = await self._respond_with_llm(
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                query=query,
                tool_call_id=tool_call.id,
                data=data,
                temperature=0.7,
            )
            return {"response": response, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
