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
from mesh.agents.exa_search_agent import build_firecrawl_to_exa_fallback
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class FirecrawlSearchDigestAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

        self.app = FirecrawlApp(api_key=self.api_key)
        self.metadata.update(
            {
                "name": "Firecrawl Search Digest Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Advanced web search agent that uses Firecrawl to perform research with intelligent query generation and content analysis, then processes results with a small and fast LLM for concise, relevant summaries.",
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
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
            }
        )

    def get_system_prompt(self) -> str:
        return """You are to extract and summarize information from the provided web search results based on the user's query.

Task:
- Extract and Summarize: Identify the most relevant information from the search results.
- Highlight and Contextualize: Highlight the key information by bolding it, and provide context from the original text for each extracted fact.
- Quote: Always quote the original text for each piece of information you extract.
- Timestamp: Always include a human-readable date/time of the article if available, add it to the end of each source URL.
- Strictly Batch by Source URL: You MUST combine all extracted facts from a single source URL into a single, cohesive block. Do not list facts from the same source on separate lines with individual URLs. The format MUST be [Fact A] [Fact B] [Fact C] [Source URL].
- Disregard Irrelevant Info: Completely ignore any information that is not directly related to the query.
- Mention Related Info: Note any other related, but less direct, information found in the results.
- Concise Relevancy Evaluation: Conclude with a single, concise paragraph evaluating the overall relevancy of the search results to the original query. State whether the results are relevant, somewhat relevant, or irrelevant, and briefly explain why.

Return clear, focused summaries that extract only the most relevant information."""

    async def _process_search_results_with_llm(self, search_results: List[Dict], search_query: str) -> str:
        """Process search results with Gemini 2.5 Flash for concise summaries"""
        start_time = time.time()

        try:
            # Just pass the raw results data to LLM - let it figure out the structure
            formatted_content = f'Query: "{search_query}"\n\nWeb contents:\n\n{str(search_results)}'

            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": formatted_content},
            ]

            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["small_model_id"],
                messages=messages,
                max_tokens=4000,
                temperature=0.7,
            )

            processed_content = (
                response if isinstance(response, str) else response.get("content", "Failed to process search results")
            )
            processing_time = time.time() - start_time
            logger.info(f"LLM processing completed in {processing_time:.2f}s for search results")

            return processed_content

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM processing failed after {processing_time:.2f}s: {str(e)}")
            logger.warning("Falling back to raw search results due to LLM processing failure")
            return f"Search results for: {search_query}\n\n{str(search_results)}"

    async def _process_scraped_content_with_llm(self, scraped_content: str) -> str:
        """Process scraped content with Gemini 2.5 Flash"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": f"Web contents:\n\n{scraped_content}"},
            ]

            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["small_model_id"],
                messages=messages,
                max_tokens=4000,
                temperature=0.7,
            )

            return response if isinstance(response, str) else response.get("content", scraped_content)

        except Exception as e:
            logger.error(f"LLM processing failed: {str(e)}")
            return scraped_content

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "firecrawl_web_search",
                    "description": "Execute a web search query with advanced filtering using Firecrawl. MANDATORY: Use time_filter parameter for ANY time-sensitive requests (recent, today, past week, etc.). Supports Google search operators in search_term. Examples: For 'recent coinbase listings' use search_term='coinbase listings' + time_filter='qdr:w'. For 'today's bitcoin news' use search_term='bitcoin news' + time_filter='qdr:d'. For site-specific searches use search_term='site:coinbase.com announcements'. Always set limit for result count control. Results are processed by AI to provide concise, relevant summaries.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "Search query WITHOUT time words. Remove 'recent', 'today', 'past week' from query - use time_filter instead. Supports operators: OR, AND, site:domain.com, quotes. Examples: 'coinbase listings' (not 'recent coinbase listings'), 'site:coinbase.com announcements', 'bitcoin OR ethereum price'.",
                            },
                            "time_filter": {
                                "type": "string",
                                "description": "REQUIRED for time-sensitive queries. Map: 'recent/past week'→'qdr:w', 'today/past day'→'qdr:d', 'past hour'→'qdr:h', 'past month'→'qdr:m', 'past year'→'qdr:y'. Always use when user mentions time periods.",
                                "enum": ["qdr:h", "qdr:d", "qdr:w", "qdr:m", "qdr:y"],
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to return. Set based on user request: '5 results'�5, '10 items'�10, etc. Default is 10.",
                                "minimum": 5,
                                "maximum": 10,
                                "default": 10,
                            },
                        },
                        "required": ["search_term"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "firecrawl_extract_web_data",
                    "description": "Extract structured data from one or multiple web pages using natural language instructions. This tool can process single URLs or entire domains (using wildcards like example.com/*). Use this when you need specific information from websites rather than general search results. You must specify what data to extract from the pages using the 'extraction_prompt' parameter. Firecrawl extract already uses AI internally so results are processed and structured.",
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
                    "description": "Scrape full contents from a specific URL. This provides complete raw web contents from individual web pages, processed by AI to provide concise, relevant summaries instead of overwhelming raw data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to scrape and analyze",
                            },
                            "wait_time": {
                                "type": "integer",
                                "description": "Time to wait for page to load in milliseconds (default: 7500)",
                                "default": 7500,
                            },
                        },
                        "required": ["url"],
                    },
                },
            },
        ]

    # Timeout and fallback policy: 60s default; use shared fallback mapping
    def get_default_timeout_seconds(self) -> Optional[int]:
        return 60

    async def get_fallback_for_tool(
        self, tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return build_firecrawl_to_exa_fallback(tool_name, function_args, original_params)

    # ------------------------------------------------------------------------
    #                      FIRECRAWL-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def firecrawl_web_search(
        self, search_term: str, time_filter: Optional[str] = None, limit: int = 10
    ) -> Dict[str, Any]:
        """
        Execute a web search using Firecrawl with advanced filtering options and AI processing.

        Args:
            search_term: Search query with optional operators (OR, AND, site:, quotes)
            time_filter: Time filter (qdr:h/d/w/m/y for past hour/day/week/month/year)
            limit: Number of results to return (5-10)
        """
        logger.info(
            f"Executing Firecrawl web search for '{search_term}' with time_filter='{time_filter}', limit={limit}"
        )

        try:
            scrape_options = ScrapeOptions(formats=["markdown"])

            # Build search parameters
            search_params = {"query": search_term, "limit": limit, "scrape_options": scrape_options, "timeout": 30000}

            # Add time filter if specified
            if time_filter:
                search_params["tbs"] = time_filter
                logger.info(f"Applied time filter: {time_filter}")

            response = await asyncio.get_event_loop().run_in_executor(None, lambda: self.app.search(**search_params))

            data = getattr(response, "data", None) or (response.get("data") if isinstance(response, dict) else None)

            if isinstance(data, list) and data:
                logger.info(f"Search completed successfully with {len(data)} results")

                # Process results with LLM
                processed_summary = await self._process_search_results_with_llm(data, search_term)

                return {"status": "success", "data": {"processed_summary": processed_summary}}
            elif isinstance(response, list):
                logger.info(f"Search completed with {len(response)} results")

                # Process results with LLM
                processed_summary = await self._process_search_results_with_llm(response, search_term)

                return {"status": "success", "data": {"processed_summary": processed_summary}}
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
        Extract structured data from web pages using Firecrawl (already uses AI for extraction).
        No additional processing needed since Firecrawl extract already uses AI.
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
    async def firecrawl_scrape_url(self, url: str, wait_time: int = 7500) -> Dict[str, Any]:
        """
        Scrape and analyze content from a specific URL using Firecrawl with AI processing.
        """
        logger.info(f"Scraping content from URL: {url}")

        try:
            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time, timeout=15000)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""
            if not markdown_content:
                return {"status": "error", "error": "Failed to scrape URL - no content returned"}

            # Process scraped content with LLM
            processed_summary = await self._process_scraped_content_with_llm(markdown_content)
            logger.info("Successfully processed scraped content")

            return {
                "status": "success",
                "data": {
                    "processed_content": processed_summary,
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
        """Handle execution of specific tools and return the processed data"""

        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "firecrawl_web_search":
            search_term = function_args.get("search_term")
            time_filter = function_args.get("time_filter")
            limit = function_args.get("limit", 10)

            if not search_term:
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            result = await self.firecrawl_web_search(search_term, time_filter, limit)

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
            wait_time = function_args.get("wait_time", 7500)

            if not url:
                return {"status": "error", "error": "Missing 'url' parameter"}

            result = await self.firecrawl_scrape_url(url, wait_time)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
