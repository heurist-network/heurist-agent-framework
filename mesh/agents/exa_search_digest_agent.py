import logging
import os
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv  # type: ignore

from core.llm import call_llm_async
from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class ExaSearchDigestAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable is required")

        self.base_url = "https://api.exa.ai"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}

        self.metadata.update(
            {
                "name": "Exa Search Digest Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Web search agent using Exa API with concise LLM summarization.",
                "external_apis": ["Exa"],
                "tags": ["Search"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Exa.png",
                "examples": [
                    "What are the latest developments in AI safety?",
                    "Recent breakthroughs in quantum computing",
                    "Find information about the newest crypto projects",
                    "Search for analysis on current market trends",
                ],
                "credits": 2,
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an AI assistant tasked with synthesizing information from provided web search results into a single, concise, and integrated summary. Your goal is to minimize output length while retaining the most crucial information.
            - Synthesize, Don't Segregate: Instead of summarizing each source individually, group related information from across all sources into thematic paragraphs.
            - Use Inline Numerical Citations: Cite sources using inline numerical markers (e.g., [1], [2]). At the end of the entire summary, provide a numbered list of the source URLs corresponding to the markers. Only cite the most relevant sources that contribute unique, non-redundant information. Disregard vague, duplicate, irrelevant information.
            - Do not quote the original text unless it's part of a very important headline. Rephrase and summarize to be as brief as possible.
            - No bold formatting (**). No markdowns. Only basic bullet points and plain texts.
            - Focus on Key Details: Extract specific names, terms, numbers, and key concepts.
            - No opening or closing paragraphs. Just focus on representing the search results based on user query.
            - Strictly under 1000 words. No minimum length requirement. Be as brief as possible."""

    async def _process_search_results_with_llm(self, search_results: List[Dict], search_query: str) -> str:
        """
        Process search results with LLM for concise summaries.

        Args:
            search_results: List of search result dictionaries from Exa API
            search_query: Original search query for context

        Returns:
            str: LLM-generated summary with inline citations or fallback text
        """
        start_time = time.time()

        try:
            formatted_results = []
            for i, result in enumerate(search_results, 1):
                formatted_results.append(
                    {
                        "index": i,
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "text": result.get("text", "")[:2000] if result.get("text") else "",
                        "published_date": result.get("published_date", ""),
                    }
                )

            formatted_content = f'Query: "{search_query}"\n\nWeb search results:\n\n{str(formatted_results)}'

            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": formatted_content},
            ]

            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["small_model_id"],
                messages=messages,
                max_tokens=2000,
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

            fallback = f"Search results for: {search_query}\n\n"
            for i, result in enumerate(search_results[:5], 1):
                fallback += f"{i}. {result.get('title', 'N/A')}\n"
                fallback += f"   URL: {result.get('url', 'N/A')}\n"
                fallback += f"   {result.get('text', '')[:200]}...\n\n"
            return fallback

    async def _process_scraped_content_with_llm(self, scraped_content: str, url: str) -> str:
        """
        Process scraped content with LLM for summarization.

        Args:
            scraped_content: Raw text content from scraped URL
            url: Source URL for context

        Returns:
            str: LLM-generated summary or truncated fallback content
        """
        start_time = time.time()

        try:
            content_to_process = scraped_content[:10000] if len(scraped_content) > 10000 else scraped_content

            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": f"URL: {url}\n\nWeb content:\n\n{content_to_process}"},
            ]

            response = await call_llm_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["small_model_id"],
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
            )

            processed_content = (
                response if isinstance(response, str) else response.get("content", scraped_content[:1000])
            )
            processing_time = time.time() - start_time
            logger.info(f"LLM processing completed in {processing_time:.2f}s for scraped content")

            return processed_content

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM processing failed after {processing_time:.2f}s: {str(e)}")
            return f"Content from {url}:\n\n{scraped_content[:1000]}..."

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "exa_web_search",
                    "description": "Search the web for any topics. MANDATORY: Use time_filter for ANY time-sensitive requests. Supports domain filtering. Results are automatically summarized by AI with inline citations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "Natural language search query. Exa uses semantic/neural search, so phrase naturally. Boolean operators (AND/OR) are not supported.",
                            },
                            "time_filter": {
                                "type": "string",
                                "description": "REQUIRED for time-sensitive queries.",
                                "enum": ["past_week", "past_month", "past_year"],
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to retrieve and summarize.",
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
                    "name": "exa_scrape_url",
                    "description": "Scrape full contents from a specific URL and return AI-processed summary with key information extracted.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to scrape and analyze",
                            }
                        },
                        "required": ["url"],
                    },
                },
            },
        ]

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 45

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def exa_web_search(
        self,
        search_term: str,
        time_filter: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        logger.info(f"Executing Exa web search for '{search_term}' with time_filter='{time_filter}', limit={limit}")

        try:
            url = f"{self.base_url}/search"
            payload = {"query": search_term, "numResults": limit, "contents": {"text": {"maxCharacters": 2000}}}

            if time_filter:
                from datetime import datetime, timedelta

                if time_filter == "past_week":
                    start_date = datetime.now() - timedelta(days=7)
                elif time_filter == "past_month":
                    start_date = datetime.now() - timedelta(days=30)
                elif time_filter == "past_year":
                    start_date = datetime.now() - timedelta(days=365)
                else:
                    start_date = None

                if start_date:
                    payload["startPublishedDate"] = start_date.strftime("%Y-%m-%dT00:00:00.000Z")
                    logger.info(f"Applied time filter: {time_filter} (from {start_date})")

            response = await self._api_request(url=url, method="POST", headers=self.headers, json_data=payload)

            if "error" in response:
                logger.error(f"Exa search API error: {response['error']}")
                return {"status": "error", "error": response["error"]}

            results = response.get("results", [])

            if not results:
                logger.warning("Search completed but no results were found")
                result = {"status": "no_data", "data": {"processed_summary": "No results found for your search query."}}
                if time_filter == "past_week":
                    result["next_step"] = "Try a broader search with past_month or past_year"
                elif time_filter == "past_month":
                    result["next_step"] = "Try a broader search with past_year"
                return result

            formatted_results = []
            for result in results:
                formatted_results.append(
                    {
                        "title": result.get("title", "N/A"),
                        "url": result.get("url", "N/A"),
                        "published_date": result.get("publishedDate", "N/A"),
                        "text": result.get("text", ""),
                    }
                )

            logger.info(f"Search completed successfully with {len(formatted_results)} results")

            processed_summary = await self._process_search_results_with_llm(formatted_results, search_term)

            return {"status": "success", "data": {"processed_summary": processed_summary}}

        except Exception as e:
            logger.error(f"Exception in exa_web_search: {str(e)}")
            return {"status": "error", "error": f"Failed to execute search: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def exa_scrape_url(self, url: str) -> Dict[str, Any]:
        logger.info(f"Scraping URL with Exa: {url}")

        try:
            api_url = f"{self.base_url}/contents"
            payload = {"urls": [url], "text": {"maxCharacters": 10000}, "livecrawl": "fallback"}

            response = await self._api_request(url=api_url, method="POST", headers=self.headers, json_data=payload)

            if "error" in response:
                logger.error(f"Exa contents API error: {response['error']}")
                return {"status": "error", "error": response["error"]}

            results = response.get("results", [])

            if not results:
                logger.warning("No content retrieved from URL")
                return {"status": "no_data", "data": {"processed_summary": f"Could not retrieve content from {url}"}}

            content_data = results[0]

            statuses = response.get("statuses", [])
            if statuses and statuses[0].get("status") != "success":
                error_msg = statuses[0].get("error", "Unknown error")
                logger.error(f"Failed to scrape URL: {error_msg}")
                return {"status": "error", "error": f"Failed to scrape URL: {error_msg}"}

            scraped_text = content_data.get("text", "")

            if not scraped_text:
                logger.warning("No text content found in scraped page")
                return {"status": "no_data", "data": {"processed_summary": f"No readable content found at {url}"}}

            logger.info(f"Successfully scraped {len(scraped_text)} characters from URL")

            processed_summary = await self._process_scraped_content_with_llm(scraped_text, url)

            return {"status": "success", "data": {"processed_summary": processed_summary}}

        except Exception as e:
            logger.error(f"Exception in exa_scrape_url: {str(e)}")
            return {"status": "error", "error": f"Failed to scrape URL: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "exa_web_search":
            search_term = function_args.get("search_term")
            time_filter = function_args.get("time_filter")
            limit = function_args.get("limit", 10)

            if not search_term:
                logger.error("Missing 'search_term' parameter")
                return {"status": "error", "error": "Missing 'search_term' parameter"}

            limit = max(5, min(10, limit))

            result = await self.exa_web_search(search_term, time_filter, limit)

        elif tool_name == "exa_scrape_url":
            url = function_args.get("url")

            if not url:
                logger.error("Missing 'url' parameter")
                return {"status": "error", "error": "Missing 'url' parameter"}

            result = await self.exa_scrape_url(url)

        else:
            logger.error(f"Unsupported tool: {tool_name}")
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        return result
