import json
from typing import Any, Dict, List

from dotenv import load_dotenv
from duckduckgo_search import DDGS

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

from .mesh_agent import MeshAgent

load_dotenv()


class DuckDuckGoSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "DuckDuckGo Search Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": (
                    "This agent can fetch and analyze web search results using DuckDuckGo API. "
                    "Analyze content relevance, source credibility, information completeness, "
                    "and provide intelligent summaries."
                ),
                "inputs": [
                    {"name": "query", "description": "The search query to analyze", "type": "str", "required": True},
                    {
                        "name": "max_results",
                        "description": "The maximum number of results to return",
                        "type": "int",
                        "required": False,
                        "default": 5,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, return only raw data without natural language response",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {"name": "response", "description": "Analysis and explanation of search results", "type": "str"},
                    {"name": "data", "description": "The raw search results data", "type": "dict"},
                ],
                "external_apis": ["DuckDuckGo"],
                "tags": ["Search", "Data"],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a web search and analysis agent using DuckDuckGo. For a user question or search query, provide a clean, concise, and accurate answer based on the search results. Respond in a conversational manner, ensuring the content is extremely clear and effective. Avoid mentioning sources.
        Strict formatting rules:
        1. no bullet points or markdown
        2. You don't need to mention the sources
        3. Just provide the answer in a straightforward way.
        Avoid introductory phrases, unnecessary filler, and mentioning sources.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web using DuckDuckGo Search API",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {"type": "string", "description": "The search term to look up"},
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return (default: 5)",
                                "minimum": 1,
                                "maximum": 10,
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    def _handle_error(self, maybe_error: dict) -> dict:
        """Small helper to return the error if present"""
        if "error" in maybe_error:
            return {"error": maybe_error["error"]}
        return {}

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    async def search_web(self, search_term: str, max_results: int = 5) -> Dict:
        """Search the web using DuckDuckGo"""
        try:
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(search_term, max_results=max_results):
                    results.append({"title": r["title"], "link": r["href"], "snippet": r["body"]})

                return {"status": "success", "data": {"search_term": search_term, "results": results}}

        except Exception as e:
            return {"status": "error", "error": f"Failed to fetch search results: {str(e)}", "data": None}

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
    self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
) -> Dict[str, Any]:
        """Handle tool execution and optional LLM explanation"""
        if tool_name == "search_web":
            result = await self.search_web(
                search_term=function_args["search_term"], max_results=function_args.get("max_results", 5)
            )
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        if raw_data_only:
            return {"response": "", "data": result}

        explanation = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query},
                {"role": "tool", "content": str(result), "tool_call_id": tool_call_id},
            ],
            temperature=0.7,
        )

        return {"response": explanation, "data": result}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle both direct tool calls and natural language queries"""
        query = params.get("query")
        if not query:
            raise ValueError("Query parameter is required")

        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)
        max_results = params.get("max_results", 5)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            if "max_results" not in tool_args:
                tool_args["max_results"] = max_results

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

        tool_calls = response.get("tool_calls", [])
        if not tool_calls:
            return {"response": response.get("content", ""), "data": {}}

        # Get the first tool call
        tool_call = tool_calls[0] if isinstance(tool_calls, list) else tool_calls

        # Handle both function call formats
        if hasattr(tool_call, "function"):
            tool_call_name = tool_call.function.name
            try:
                tool_call_args = json.loads(tool_call.function.arguments)
            except Exception:
                # Fallback for string format
                tool_call_args = {"query": query, "max_results": max_results}

        if "max_results" not in tool_call_args:
            tool_call_args["max_results"] = max_results

        return await self._handle_tool_logic(
            tool_name=tool_call_name,
            function_args=tool_call_args,
            query=query,
            tool_call_id=tool_call.id,
            raw_data_only=raw_data_only,
        )
