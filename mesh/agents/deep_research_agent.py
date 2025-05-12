import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from core.clients.search_client import SearchClient
from core.components import LLMProvider
from core.tools.tools_mcp import Tools
from core.workflows import ResearchWorkflow
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class DeepResearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Deep Research Agent",
                "version": "2.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Advanced research agent that performs multi-level web searches with recursive exploration, analyzes content across sources, and produces comprehensive research reports with key insights",
                "inputs": [
                    # fmt: off
                    # keeping these here as they differ from the base class
                    {
                        "name": "query",
                        "description": "Research query or topic",
                        "type": "str",
                        "required": True,
                    },
                    # fmt: on
                    {
                        "name": "depth",
                        "description": "Research depth (1-3)",
                        "type": "int",
                        "required": False,
                        "default": 2,
                    },
                    {
                        "name": "breadth",
                        "description": "Search breadth per level (1-5)",
                        "type": "int",
                        "required": False,
                        "default": 3,
                    },
                    {
                        "name": "concurrency",
                        "description": "Number of concurrent searches",
                        "type": "int",
                        "required": False,
                        "default": 9,
                    },
                ],
                "external_apis": ["Firecrawl"],
                "tags": ["Research"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/DeepResearch.png",
                "examples": [
                    "What is the latest news on Bitcoin?",
                    "Find information about the Ethereum blockchain",
                    "Search for articles about the latest trends in AI",
                    "What are the latest developments in zero knowledge proofs?",
                ],
            }
        )
        self._last_request_time = 0

        self.search_model = os.getenv("SEARCH_MODEL", self.metadata["large_model_id"])
        self.research_model = os.getenv("RESEARCH_MODEL", self.metadata["large_model_id"])

        if not os.getenv("SEARCH_MODEL"):
            logger.info(f"SEARCH_MODEL not set, using {self.search_model}")
        if not os.getenv("RESEARCH_MODEL"):
            logger.info(f"RESEARCH_MODEL not set, using {self.research_model}")

        self.search_clients = {}

        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "")
        self.exa_api_key = os.getenv("EXA_API_KEY", "")

        if self.firecrawl_api_key:
            self.firecrawl_client = SearchClient(client_type="firecrawl", api_key=self.firecrawl_api_key, rate_limit=1)
            self.search_clients["firecrawl"] = self.firecrawl_client
        else:
            logger.warning("FIRECRAWL_API_KEY not found in environment variables")

        if self.exa_api_key:
            self.exa_client = SearchClient(client_type="exa", api_key=self.exa_api_key, rate_limit=1)
            self.search_clients["exa"] = self.exa_client
        else:
            logger.warning("EXA_API_KEY not found in environment variables")

        self.duckduckgo_client = SearchClient(client_type="duckduckgo", rate_limit=5)
        self.search_clients["duckduckgo"] = self.duckduckgo_client
        self.tools = Tools()
        self.llm_provider = LLMProvider(
            self.heurist_base_url, self.heurist_api_key, self.search_model, self.metadata["small_model_id"], self.tools
        )
        self.research_workflow = ResearchWorkflow(self.llm_provider, self.tools, search_clients=self.search_clients)

    def get_system_prompt(self) -> str:
        return """You are an expert research analyst that processes can use a deep research tool to get a comprehensive report on a topic.
        Enhance the user query if needed to get a more accurate report. The deep research tool will return a report and a list of sources.
        If the tool call is successful, returns the response (report) and the data. Give a breif summary of the report and the key points.
        Make sure your reponse is concise and to the point. No more than 1 or 2 paragraphs.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "deep_research",
                    "description": "Perform comprehensive multi-level web research on a topic with recursive exploration. This function analyzes content across multiple sources, explores various research paths, and synthesizes findings into a structured report. It's slow and expensive, so use it sparingly and only when you need to explore a broad topic in depth.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # fmt: off
                            "query": {
                                "type": "string",
                                "description": "Research query or topic",
                            },
                            "depth": {
                                "type": "number",
                                "description": "Research depth (1-3)",
                                "default": 2,
                            },
                            # fmt: on
                            "breadth": {
                                "type": "number",
                                "description": "Search breadth per level (1-5)",
                                "default": 3,
                            },
                            "concurrency": {
                                "type": "number",
                                "description": "Number of concurrent searches",
                                "default": 9,
                            },
                        },
                        "required": ["query"],
                    },
                },
            }
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and format responses"""

        if tool_name == "deep_research":
            query = function_args.get("query")
            depth = min(max(function_args.get("depth", 2), 1), 3)
            breadth = min(max(function_args.get("breadth", 3), 1), 5)
            concurrency = min(max(function_args.get("concurrency", 9), 1), 9)

            if not query:
                return {"error": "Missing 'query' in tool_arguments"}

            # Prepare workflow options for ResearchWorkflow
            workflow_options = {
                "depth": depth,
                "breadth": breadth,
                "concurrency": concurrency,
                "raw_data_only": False,
                "report_model": self.research_model,
                "multi_provider": True,
            }

            # Run the research workflow
            report, _, research_result = await self.research_workflow.process(
                message=query, workflow_options=workflow_options
            )

            return {
                "response": report,
                "data": research_result,
            }
        else:
            return {"error": f"Unsupported tool: {tool_name}"}
