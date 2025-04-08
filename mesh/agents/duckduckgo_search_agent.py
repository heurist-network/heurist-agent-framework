import json
from typing import Any, Dict, List

from dotenv import load_dotenv
from duckduckgo_search import DDGS

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()


class DuckDuckGoSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "DuckDuckGo Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": (
                    "This agent can fetch and analyze web search results using DuckDuckGo API and provide intelligent summaries."
                ),
                "inputs": [
                    {
                        "name": "query",
                        "description": "The search query or question or keyword",
                        "type": "str",
                        "required": False,
                    },
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
                "tags": ["Search"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Duckduckgo.png",  # use a duckduckgo logo
                "examples": [
                    "What happens if you put a mirror in front of a black hole?",
                    "Could octopuses be considered alien life forms?",
                    "Why don't birds get electrocuted when sitting on power lines?",
                    "How do fireflies produce light?",
                ],
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
                                "type": "number",
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
    async def _respond_with_llm(self, query: str, tool_call_id: str, data: dict, temperature: float) -> str:
        """Generate a natural language response using the LLM"""
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
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""

        if tool_name != "search_web":
            return {"error": f"Unsupported tool: {tool_name}"}

        search_term = function_args.get("search_term")
        max_results = function_args.get("max_results", 5)

        if not search_term:
            return {"error": "Missing 'search_term' in tool_arguments"}

        result = await self.search_web(search_term=search_term, max_results=max_results)

        errors = self._handle_error(result)
        if errors:
            return errors

        return result

    # ------------------------------------------------------------------------
    #                      MAIN HANDLER
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages, supporting both direct tool calls and natural language queries.

        Either 'query' or 'tool' is required in params.
        - If 'query' is present, it means "agent mode", we use LLM to interpret the query and call tools
          - if 'raw_data_only' is present, we return tool results without another LLM call
        - If 'tool' is present, it means "direct tool call mode", we bypass LLM and directly call the API
          - never run another LLM call, this minimizes latency and reduces error
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)
        max_results = params.get("max_results", 5)

        # Validate input
        if not query and not (tool_name and tool_args.get("search_term")):
            return {"error": "Either 'query' or 'tool' with valid 'tool_arguments' must be provided"}

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            # Ensure max_results is set
            if "max_results" not in tool_args:
                tool_args["max_results"] = max_results

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
                    tool_call_args = {"search_term": query, "max_results": max_results}

            # Ensure max_results is set
            if "max_results" not in tool_call_args:
                tool_call_args["max_results"] = max_results

            data = await self._handle_tool_logic(tool_name=tool_call_name, function_args=tool_call_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                query=query, tool_call_id=tool_call.id, data=data, temperature=0.7
            )
            return {"response": explanation, "data": data}

        # This should never be reached given the validation at the beginning
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
