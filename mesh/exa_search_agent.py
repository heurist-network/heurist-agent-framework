import json
import logging
import os
from typing import Any, Dict, List

import requests

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class ExaSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("EXA_API_KEY")
        self.base_url = "https://api.exa.ai"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

        # Add required metadata
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
                "external_apis": ["Exa.ai"],
                "tags": ["Search", "Data"],
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
    2. Include source URLs and timestamps where available
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
                    "name": "search",
                    "description": "Search for webpages related to a query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "The search term"},
                            "limit": {
                                "type": "integer",
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
                    "name": "answer",
                    "description": "Get a direct answer to a question using Exa's answer API",
                    "parameters": {
                        "type": "object",
                        "properties": {"question": {"type": "string", "description": "The question to answer"}},
                        "required": ["question"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_and_answer",
                    "description": "Perform both search and answer operations for a query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "The topic to search for and answer"}
                        },
                        "required": ["topic"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
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
    #                      EXA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    async def search(self, search_term: str, limit: int = 10) -> dict:
        """
        Uses Exa's /search endpoint to find webpages related to the search term.
        """
        try:
            url = f"{self.base_url}/search"
            payload = {"query": search_term, "limit": limit}  # API still uses 'query'

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
                        "text": result.get("text", "")[:500] + "..."
                        if len(result.get("text", "")) > 500
                        else result.get("text", ""),
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

    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    async def search_and_answer(self, topic: str) -> dict:
        """
        Combines both search and answer functionalities.
        """
        search_results = await self.search(topic)
        search_error = self._handle_error(search_results)
        if search_error:
            return search_error

        answer_results = await self.answer(topic)
        answer_error = self._handle_error(answer_results)
        if answer_error:
            return answer_error

        # Combine both results
        return {
            "search_results": search_results.get("search_results", []),
            "answer": answer_results.get("answer", "No direct answer available"),
            "sources": answer_results.get("sources", []),
        }

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
    ) -> Dict[str, Any]:
        """
        A single method that calls the appropriate function, handles
        errors/formatting, and optionally calls the LLM to explain the result.
        """
        # Default temperature for explanations
        temp_for_explanation = 0.7

        if tool_name == "search":
            search_term = function_args.get("search_term")
            limit = function_args.get("limit", 10)

            if not search_term:
                return {"error": "Missing 'search_term' in tool_arguments"}

            logger.info(f"Executing search for '{search_term}'")
            result = await self.search(search_term, limit)
            errors = self._handle_error(result)
            if errors:
                return errors

            if raw_data_only:
                return {"response": "", "data": result}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call_id, data=result, temperature=temp_for_explanation
            )
            return {"response": explanation, "data": result}

        elif tool_name == "answer":
            question = function_args.get("question")

            if not question:
                return {"error": "Missing 'question' in tool_arguments"}

            logger.info(f"Getting direct answer for '{question}'")
            result = await self.answer(question)
            errors = self._handle_error(result)
            if errors:
                return errors

            if raw_data_only:
                return {"response": "", "data": result}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call_id, data=result, temperature=temp_for_explanation
            )
            return {"response": explanation, "data": result}

        elif tool_name == "search_and_answer":
            topic = function_args.get("topic")

            if not topic:
                return {"error": "Missing 'topic' in tool_arguments"}

            logger.info(f"Performing search and answer for '{topic}'")
            result = await self.search_and_answer(topic)
            errors = self._handle_error(result)
            if errors:
                return errors

            if raw_data_only:
                return {"response": "", "data": result}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call_id, data=result, temperature=temp_for_explanation
            )
            return {"response": explanation, "data": result}

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
            # For a direct tool call, we do NOT use call_llm_with_tools_async
            # We simply call our helper. We'll pass an empty `query` or something placeholder
            # if user hasn't given a `query`.
            # We'll also pass tool_call_id = "direct_tool" for consistency.
            return await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
                query=query or "Direct tool call without LLM.",
                tool_call_id="direct_tool",
                raw_data_only=raw_data_only,
            )

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

            # Use the same _handle_tool_logic
            return await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
                query=query,
                tool_call_id=tool_call.id,
                raw_data_only=raw_data_only,
            )

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}