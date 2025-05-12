import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class FirecrawlSearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

        self.app = FirecrawlApp(api_key=self.api_key)
        self.metadata.update(
            {
                "name": "Firecrawl Search Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Advanced search agent that uses Firecrawl to perform research with intelligent query generation and content analysis.",
                "external_apis": ["Firecrawl"],
                "tags": ["Search"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Firecrawl.png",
                "examples": [
                    "What are the most bizarre crypto projects that actually succeeded?",
                    "Find stories of people who became millionaires from meme coins",
                    "The biggest scams in crypto history",
                    "Search for the weirdest NFT collections that sold for huge amounts",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an expert research analyst that processes web search results.

        Your capabilities:
        1. Execute targeted web searches on specific topics
        2. Analyze search results for key findings and patterns

        For search results:
        1. Only use relevant, good quality, credible information
        2. Extract key facts and statistics
        3. Present the information like a human, not a robot

        Return analyses in clear natural language with concrete findings. Do not make up any information."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "firecrawl_web_search",
                    "description": "Execute a web search query by reading the web pages using Firecrawl. It provides more comprehensive information than standard web search by extracting the full contents from the pages. Use this when you need in-depth information on a topic. Data comes from Firecrawl search API. It may fail to find information of niche topics such like small cap crypto projects.",
                    "parameters": {
                        "type": "object",
                        "properties": {"search_term": {"type": "string", "description": "The search term to execute"}},
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "firecrawl_extract_web_data",
                    "description": "Extract structured data from one or multiple web pages using natural language instructions using Firecrawl. This tool can process single URLs or entire domains (using wildcards like example.com/*). Use this when you need specific information from websites rather than general search results. You must specify what data to extract from the pages using the 'extraction_prompt' parameter.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "urls": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of URLs to extract data from. Can include wildcards (e.g., 'example.com/*') to crawl entire domains.",
                            },
                            "extraction_prompt": {
                                "type": "string",
                                "description": "Natural language description of what data to extract from the pages.",
                            },
                        },
                        "required": ["urls", "extraction_prompt"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      FIRECRAWL-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def firecrawl_web_search(self, search_term: str) -> Dict[str, Any]:
        """
        Execute a web search using Firecrawl and return formatted results.
        """
        logger.info(f"Executing Firecrawl web search for '{search_term}'")

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.search(query=search_term, params={"scrapeOptions": {"formats": ["markdown"]}})
            )

            if isinstance(response, dict) and "data" in response:
                logger.info(f"Search completed successfully with {len(response.get('data', []))} results")
                return {
                    "status": "success",
                    "data": {"results": response.get("data", []), "metadata": response.get("metadata", {})},
                }
            elif isinstance(response, dict) and "success" in response:
                logger.info(f"Search completed with {len(response.get('data', []))} results")
                return {"status": "success", "data": {"results": response.get("data", [])}}
            elif isinstance(response, list):
                formatted_data = []
                for item in response:
                    if isinstance(item, dict):
                        formatted_data.append(item)
                    else:
                        formatted_data.append(
                            {
                                "url": getattr(item, "url", ""),
                                "markdown": getattr(item, "markdown", "") or getattr(item, "content", ""),
                                "title": getattr(item, "title", "") or getattr(item, "metadata", {}).get("title", ""),
                            }
                        )
                logger.info(f"Search completed with {len(formatted_data)} formatted results")
                return {"status": "success", "data": {"results": formatted_data}}
            else:
                logger.warning("Search completed but no results were found")
                return {"status": "no_data", "data": {"results": []}}

        except Exception as e:
            logger.error(f"Exception in firecrawl_web_search: {str(e)}")
            return {"status": "error", "error": f"Failed to execute search: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def firecrawl_extract_web_data(
        self, urls: List[str], extraction_prompt: str, enable_web_search: bool = False
    ) -> Dict[str, Any]:
        """
        Extract structured data from web pages using Firecrawl.
        """
        urls_str = ", ".join(urls[:3]) + ("..." if len(urls) > 3 else "")
        logger.info(f"Extracting web data from '{urls_str}' with prompt '{extraction_prompt}'")

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.app.extract(
                    urls=urls, params={"prompt": extraction_prompt, "enableWebSearch": enable_web_search}
                ),
            )

            if isinstance(response, dict):
                if "data" in response:
                    logger.info("Data extraction completed successfully")
                    return {
                        "status": "success",
                        "data": {"extracted_data": response.get("data", {}), "metadata": response.get("metadata", {})},
                    }
                elif "success" in response and response.get("success"):
                    logger.info("Data extraction completed successfully")
                    return {"status": "success", "data": {"extracted_data": response.get("data", {})}}
                else:
                    logger.warning(f"Data extraction failed: {response.get('message', 'Unknown error')}")
                    return {"status": "error", "error": "Extraction failed", "details": response}
            else:
                logger.info("Data extraction completed successfully")
                return {"status": "success", "data": {"extracted_data": response}}

        except Exception as e:
            logger.error(f"Exception in firecrawl_extract_web_data: {str(e)}")
            return {"status": "error", "error": f"Failed to extract data: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""

        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "firecrawl_web_search":
            search_term = function_args.get("search_term")
            if not search_term:
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            result = await self.firecrawl_web_search(search_term)

        elif tool_name == "firecrawl_extract_web_data":
            urls = function_args.get("urls")
            extraction_prompt = function_args.get("extraction_prompt")
            enable_web_search = function_args.get("enable_web_search", False)

            if not urls:
                return {"status": "error", "error": "Missing 'urls' parameter"}
            if not extraction_prompt:
                return {"status": "error", "error": "Missing 'extraction_prompt' parameter"}

            result = await self.firecrawl_extract_web_data(urls, extraction_prompt, enable_web_search)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
