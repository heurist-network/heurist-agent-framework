import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from core.llm import call_llm_async
from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class L2BeatAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")

        self.app = FirecrawlApp(api_key=self.api_key)
        self._api_clients["firecrawl"] = self.app

        self.l2beat_base_urls = {
            "summary": "https://l2beat.com/scaling/summary",
            "activity": "https://l2beat.com/scaling/activity",
            "costs": "https://l2beat.com/scaling/costs",
        }

        self.valid_tabs = {
            "summary": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
            "activity": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
            "costs": ["rollups", "others"],
        }

        self.metadata.update(
            {
                "name": "L2Beat Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Specialized agent for analyzing Layer 2 scaling solutions data from L2Beat. Provides comprehensive insights into L2 TVL, activity metrics, and transaction costs across different chains and categories (Rollups, Validiums & Optimiums, Others, Not Reviewed). Note: Cost data for Validiums & Optimiums is included in the 'Others' category.",
                "external_apis": ["Firecrawl", "L2Beat"],
                "tags": ["L2Beat"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/L2Beat.png",
                "examples": [
                    "What's the current TVL and market share of top L2 solutions?",
                    "Show me the activity comparison between Arbitrum, Optimism, and Base",
                    "Which L2 has the lowest transaction costs right now?",
                    "Compare the costs of sending ETH vs swapping tokens on different L2s",
                    "What are the top Validiums and Optimiums by TVL?",
                    "Show me activity metrics for non-reviewed L2s",
                    "Compare costs across different L2 categories",
                ],
                "credits": 2,
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an expert Layer 2 blockchain data analyst that extracts and interprets L2Beat metrics.

        CRITICAL: Strip out ALL website artifacts and preserve ONLY L2 metrics data:
        - Remove ALL logo URLs, image links (e.g., ![logo], https://l2beat.com/static/icons/)
        - Remove navigation menus, headers, footers, social links, cookie notices
        - Remove "View details", "Details", job postings, donation links
        - Remove duplicate section headers and repeated explanations
        - Remove all HTML artifacts and excessive whitespace

        CAPTURE ESSENTIAL L2 DATA:
        - Chain/Project names (without logo references)
        - TVL values and market share percentages
        - Transaction metrics (UOPS, TPS, counts)
        - Cost data in USD (per operation, calldata, blobs, compute, overhead)
        - Stage information and security status
        - Type classifications (Rollup, Validium, Optimium, etc.)
        - DA Layer information
        - Percentage changes and growth metrics

        FORMAT YOUR ANALYSIS:
        - Use clean markdown tables for data comparison
        - **Bold** chain names and key metrics
        - Present numbers properly formatted ($1.5B for billions, 1.2M for millions)
        - Group data by categories when relevant
        - Calculate and highlight important ratios and trends

        PROVIDE ACTIONABLE INSIGHTS:
        - Identify top performers and underperformers in each category
        - Note significant trends and differences between L2 types
        - Highlight cost-effectiveness and efficiency metrics
        - Compare metrics across different L2s when multiple are present
        - Explain differences between Rollups, Validiums, Optimiums when relevant
        
        Focus on delivering clean, data-focused analysis without website clutter. Extract only the blockchain metrics that matter for informed L2 decisions."""

    async def _process_with_llm(self, raw_content: str, context_info: Dict[str, str]) -> str:
        """Process raw scraped content with LLM and track performance"""
        start_time = time.time()

        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Extract and format the L2Beat data from this {context_info.get("data_type", "page")} content.

                Context:
                - Data Type: {context_info.get("data_type", "unknown")}
                - Category: {context_info.get("category", "unknown")}
                - Source URL: {context_info.get("url", "unknown")}

                Raw Content:
                {raw_content[:50000]}""",  # Limit to avoid token limits
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
            logger.info(
                f"LLM processing completed in {processing_time:.2f}s for {context_info.get('data_type', 'content')}"
            )

            return processed_content

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"LLM processing failed after {processing_time:.2f}s: {str(e)}")
            logger.warning("Falling back to raw content due to LLM processing failure")
            return raw_content

    async def _scrape_and_process(self, url: str, context_info: Dict[str, str]) -> Dict[str, Any]:
        """Common method to scrape URL and process with LLM"""
        try:
            # Increase timeout for larger pages
            category = context_info.get("category", "rollups")
            wait_time = 15000 if category in ["others", "notReviewed"] else 10000
            timeout_time = 30000 if category in ["others", "notReviewed"] else 20000

            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time, timeout=timeout_time)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""

            if not markdown_content:
                return {"status": "error", "error": f"Failed to scrape {context_info['data_type']} page"}

            # Process with LLM to clean and format the content
            processed_content = await self._process_with_llm(markdown_content, context_info)

            logger.info(f"Successfully processed {context_info['data_type']} data")

            return {
                "status": "success",
                "data": {
                    "content": processed_content,
                    "source": url,
                    "data_type": context_info.get("data_type", "L2 Data"),
                    "category": context_info.get("category", "unknown"),
                },
            }

        except Exception as e:
            logger.error(f"Exception in _scrape_and_process for {context_info['data_type']}: {str(e)}")
            return {"status": "error", "error": f"Failed to get {context_info['data_type']} data: {str(e)}"}

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_l2_summary",
                    "description": "Get comprehensive summary data for Layer 2 solutions including TVL, market share, chain type, stage, and security information. Can fetch data for different L2 categories.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums' (Validiums & Optimiums), 'others' (Other scaling solutions), 'notReviewed' (Not yet reviewed L2s)",
                                "default": "rollups",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_l2_activity",
                    "description": "Get activity metrics for Layer 2 solutions including daily transactions, active addresses, TPS, and activity trends. Can fetch data for different L2 categories.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums' (Validiums & Optimiums), 'others' (Other scaling solutions), 'notReviewed' (Not yet reviewed L2s)",
                                "default": "rollups",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_l2_costs",
                    "description": "Get transaction cost comparison across Layer 2 solutions for different operations. Costs are shown in USD. Note: Validiums & Optimiums costs are included in the 'others' category.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "others"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'others' (includes all non-rollup L2s including Validiums & Optimiums)",
                                "default": "rollups",
                            }
                        },
                        "required": [],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      HELPER METHOD FOR URL CONSTRUCTION
    # ------------------------------------------------------------------------

    def _build_url(self, data_type: str, category: str = "rollups") -> str:
        """Build URL with appropriate tab parameter based on category."""
        base_url = self.l2beat_base_urls[data_type]

        # Default to rollups tab (no parameter needed for default)
        if category == "rollups":
            return base_url

        # Validate category for the data type
        if category not in self.valid_tabs[data_type]:
            logger.warning(f"Invalid category '{category}' for {data_type}. Using default 'rollups'")
            return base_url

        # Add tab parameter for non-default categories
        return f"{base_url}?tab={category}"

    # ------------------------------------------------------------------------
    #                      L2BEAT-SPECIFIC METHODS
    # ------------------------------------------------------------------------

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_summary(self, category: str = "rollups") -> Dict[str, Any]:
        """
        Fetch L2 summary data including TVL and market share.

        Args:
            category: Type of L2s to fetch - 'rollups', 'validiumsAndOptimiums', 'others', or 'notReviewed'
        """
        logger.info(f"Fetching L2Beat summary data for category: {category}")

        url = self._build_url("summary", category)
        logger.info(f"Scraping URL: {url}")

        # Determine readable category name for response
        category_names = {
            "rollups": "Rollups",
            "validiumsAndOptimiums": "Validiums & Optimiums",
            "others": "Other L2s",
            "notReviewed": "Not Reviewed L2s",
        }

        context_info = {
            "data_type": f"L2 Summary (TVL & Market Share) - {category_names.get(category, 'Rollups')}",
            "category": category,
            "url": url,
        }

        return await self._scrape_and_process(url, context_info)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_activity(self, category: str = "rollups") -> Dict[str, Any]:
        """
        Fetch L2 activity metrics including transactions and active addresses.

        Args:
            category: Type of L2s to fetch - 'rollups', 'validiumsAndOptimiums', 'others', or 'notReviewed'
        """
        logger.info(f"Fetching L2Beat activity data for category: {category}")

        url = self._build_url("activity", category)
        logger.info(f"Scraping URL: {url}")

        # Determine readable category name for response
        category_names = {
            "rollups": "Rollups",
            "validiumsAndOptimiums": "Validiums & Optimiums",
            "others": "Other L2s",
            "notReviewed": "Not Reviewed L2s",
        }

        context_info = {
            "data_type": f"L2 Activity Metrics - {category_names.get(category, 'Rollups')}",
            "category": category,
            "url": url,
        }

        return await self._scrape_and_process(url, context_info)

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_costs(self, category: str = "rollups") -> Dict[str, Any]:
        """
        Fetch L2 transaction costs for different operations.

        Args:
            category: Type of L2s to fetch - 'rollups' or 'others'
        """
        logger.info(f"Fetching L2Beat costs data for category: {category}")

        url = self._build_url("costs", category)
        logger.info(f"Scraping URL: {url}")

        # Determine readable category name for response
        category_names = {
            "rollups": "Rollups",
            "others": "Other L2s",
        }

        context_info = {
            "data_type": f"L2 Transaction Costs - {category_names.get(category, 'Rollups')}",
            "category": category,
            "url": url,
        }

        return await self._scrape_and_process(url, context_info)

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the data"""

        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        category = function_args.get("category", "rollups")

        if tool_name == "get_l2_summary":
            result = await self.get_l2_summary(category=category)

        elif tool_name == "get_l2_activity":
            result = await self.get_l2_activity(category=category)

        elif tool_name == "get_l2_costs":
            result = await self.get_l2_costs(category=category)

        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        errors = self._handle_error(result)
        if errors:
            return errors

        return result
