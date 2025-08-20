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
                "version": "1.1.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Specialized agent for analyzing Layer 2 scaling solutions data from L2Beat. Provides comprehensive insights into L2 TVL, activity metrics, and transaction costs across different chains and categories (Rollups, Validiums & Optimiums, Others, Not Reviewed). Note: Cost data for Validiums & Optimiums is included in the 'Others' category.",
                "external_apis": ["Firecrawl", "L2Beat"],
                "tags": ["L2Beat"],
                "recommended": True,
                "image_url": "https://raw.githubusecontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/L2Beat.png",
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
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an expert Layer 2 blockchain analyst specializing in L2Beat data interpretation.

        Analyze Layer 2 scaling data focusing on:
        1. **Summary Data**: TVL (Total Value Locked), market share, chain types, security models across different categories (Rollups, Validiums & Optimiums, Others, Not Reviewed)
        2. **Activity Metrics**: Transaction counts, active addresses, TPS (transactions per second) across all L2 categories
        3. **Cost Analysis**: Transaction costs in USD for different operations across various L2 types

        For all data:
        - Present numbers with proper formatting (e.g., $1.5B for billions, 1.2M for millions)
        - Calculate percentages and changes where relevant
        - Compare metrics across different L2s when multiple are present
        - Use **bold** for chain names and important metrics
        - Format data in tables when comparing multiple chains
        - Clearly identify the category of L2 being analyzed (Rollup, Validium, Optimium, etc.)
        - Focus on actionable insights

        When analyzing:
        - Identify top performers and underperformers in each category
        - Note significant trends and differences between L2 types
        - Provide context for the numbers based on L2 architecture type
        - Highlight cost-effectiveness and efficiency metrics
        - Explain differences between Rollups, Validiums, Optimiums when relevant
        
        Return clear, concise analysis that helps users make informed decisions about L2 usage."""

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

        try:
            url = self._build_url("summary", category)
            logger.info(f"Scraping URL: {url}")

            # Increase timeout for larger pages
            wait_time = 15000 if category in ["others", "notReviewed"] else 10000
            timeout_time = 30000 if category in ["others", "notReviewed"] else 20000

            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time, timeout=timeout_time)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""

            if not markdown_content:
                return {"status": "error", "error": f"Failed to scrape L2Beat summary data for category: {category}"}

            # Determine readable category name for response
            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
                "others": "Other L2s",
                "notReviewed": "Not Reviewed L2s",
            }

            logger.info(f"Successfully fetched L2Beat summary data for {category}")
            return {
                "status": "success",
                "data": {
                    "content": markdown_content,
                    "source": url,
                    "data_type": f"L2 Summary (TVL & Market Share) - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            logger.error(f"Exception in get_l2_summary: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch L2 summary data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_activity(self, category: str = "rollups") -> Dict[str, Any]:
        """
        Fetch L2 activity metrics including transactions and active addresses.

        Args:
            category: Type of L2s to fetch - 'rollups', 'validiumsAndOptimiums', 'others', or 'notReviewed'
        """
        logger.info(f"Fetching L2Beat activity data for category: {category}")

        try:
            url = self._build_url("activity", category)
            logger.info(f"Scraping URL: {url}")

            # Increase timeout for larger pages
            wait_time = 15000 if category in ["others", "notReviewed"] else 10000
            timeout_time = 30000 if category in ["others", "notReviewed"] else 20000

            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time, timeout=timeout_time)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""

            if not markdown_content:
                return {"status": "error", "error": f"Failed to scrape L2Beat activity data for category: {category}"}

            # Determine readable category name for response
            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
                "others": "Other L2s",
                "notReviewed": "Not Reviewed L2s",
            }

            logger.info(f"Successfully fetched L2Beat activity data for {category}")
            return {
                "status": "success",
                "data": {
                    "content": markdown_content,
                    "source": url,
                    "data_type": f"L2 Activity Metrics - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            logger.error(f"Exception in get_l2_activity: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch L2 activity data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_costs(self, category: str = "rollups") -> Dict[str, Any]:
        """
        Fetch L2 transaction costs for different operations.

        Args:
            category: Type of L2s to fetch - 'rollups', 'validiumsAndOptimiums', or 'others'
        """
        logger.info(f"Fetching L2Beat costs data for category: {category}")

        try:
            url = self._build_url("costs", category)
            logger.info(f"Scraping URL: {url}")

            # Increase timeout for larger pages
            wait_time = 15000 if category == "others" else 10000
            timeout_time = 30000 if category == "others" else 20000

            scrape_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.scrape_url(url, formats=["markdown"], wait_for=wait_time, timeout=timeout_time)
            )

            markdown_content = getattr(scrape_result, "markdown", "") if hasattr(scrape_result, "markdown") else ""

            if not markdown_content:
                return {"status": "error", "error": f"Failed to scrape L2Beat costs data for category: {category}"}

            # Determine readable category name for response
            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
                "others": "Other L2s",
            }

            logger.info(f"Successfully fetched L2Beat costs data for {category}")
            return {
                "status": "success",
                "data": {
                    "content": markdown_content,
                    "source": url,
                    "data_type": f"L2 Transaction Costs - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            logger.error(f"Exception in get_l2_costs: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch L2 costs data: {str(e)}"}

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
