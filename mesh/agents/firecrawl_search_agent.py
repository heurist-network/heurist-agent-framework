import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from firecrawl.firecrawl import ScrapeOptions

from core.llm import call_llm_async
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
                "credits": 2,
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an expert research analyst that processes web search results and scraped content.

        Your capabilities:
        1. Execute targeted web searches on specific topics
        2. Analyze search results for key findings and patterns
        3. Extract and process structured data from web pages
        4. Scrape specific URLs for detailed content analysis

        For search results and scraped content:
        1. Only use relevant, good quality, credible information
        2. Extract key facts and statistics
        3. Present the information like a human, not a robot

        Return analyses in clear natural language with concrete findings. Do not make up any information."""

    async def _process_with_llm(self, raw_content: str, context_info: Dict[str, str]) -> str:
        """Process raw scraped content with LLM and track performance"""
        start_time = time.time()

        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Extract and format the relevant information from this web content.

                Context:
                - URL: {context_info.get("url", "unknown")}
                - Content Type: {context_info.get("type", "unknown")}
                - Purpose: {context_info.get("purpose", "general analysis")}

                Raw Content:
                {raw_content}""",
                },
            ]

            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["small_model_id"],
                messages=messages,
                max_tokens=25000,
                temperature=0.1,
            )

            processed_content = response if isinstance(response, str) else response.get("content", raw_content)
            processing_time = time.time() - start_time
            logger.info(f"LLM processing completed in {processing_time:.2f}s for {context_info.get('type', 'content')}")

            return processed_content

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM processing failed after {processing_time:.2f}s: {str(e)}")
            logger.warning("Falling back to raw content due to LLM processing failure")
            return raw_content

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
            {
                "type": "function",
                "function": {
                    "name": "firecrawl_scrape_url",
                    "description": "Scrape and analyze content from a specific URL using Firecrawl. This provides detailed content extraction and processing from individual web pages with intelligent content analysis.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to scrape and analyze",
                            },
                            "wait_time": {
                                "type": "integer",
                                "description": "Time to wait for page to load in milliseconds (default: 5000)",
                                "default": 5000,
                            },
                        },
                        "required": ["url"],
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
            scrape_options = ScrapeOptions(formats=["markdown"])

            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.search(query=search_term, scrape_options=scrape_options)
            )

            data = getattr(response, "data", None) or (response.get("data") if isinstance(response, dict) else None)

            if isinstance(data, list) and data:
                logger.info(f"Search completed successfully with {len(data)} results")
                return {"status": "success", "data": {"results": data}}
            elif isinstance(response, list):
                logger.info(f"Search completed with {len(response)} results")
                return {"status": "success", "data": {"results": response}}
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
                lambda: self.app.extract(urls=urls, prompt=extraction_prompt, enable_web_search=enable_web_search),
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

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def firecrawl_scrape_url(self, url: str, wait_time: int = 5000) -> Dict[str, Any]:
        """
        Scrape and analyze content from a specific URL using Firecrawl.
        """
        logger.info(f"Scraping content from URL: {url}")

        try:
            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""
            if not markdown_content:
                return {"status": "error", "error": "Failed to scrape URL - no content returned"}

            context_info = {"type": "webpage", "url": url, "purpose": "content analysis"}

            processed_content = await self._process_with_llm(markdown_content, context_info)
            logger.info("Successfully processed scraped content")

            return {
                "status": "success",
                "data": {
                    "processed_content": processed_content,
                    "raw_markdown": markdown_content,
                    "url": url,
                },
            }

        except Exception as e:
            logger.error(f"Exception in firecrawl_scrape_url: {str(e)}")
            return {"status": "error", "error": f"Failed to scrape URL: {str(e)}"}

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

        elif tool_name == "firecrawl_scrape_url":
            url = function_args.get("url")
            wait_time = function_args.get("wait_time", 5000)

            if not url:
                return {"status": "error", "error": "Missing 'url' parameter"}

            result = await self.firecrawl_scrape_url(url, wait_time)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
