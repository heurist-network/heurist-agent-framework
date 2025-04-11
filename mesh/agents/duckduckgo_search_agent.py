from typing import Any, Dict, List

from dotenv import load_dotenv
from duckduckgo_search import DDGS

from decorators import with_cache
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
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Duckduckgo.png",
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
