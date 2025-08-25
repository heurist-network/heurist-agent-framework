import json
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class L2BeatAgent(MeshAgent):
    def __init__(self):
        super().__init__()

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
                "external_apis": ["L2Beat"],
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
        return """You are an expert Layer 2 blockchain analyst specializing in L2Beat data interpretation.

        Analyze Layer 2 scaling data focusing on:
        1. **Summary Data**: TVL (Total Value Locked), market share, chain types, security models
        2. **Activity Metrics**: Transaction counts, active addresses, TPS (transactions per second)
        3. **Cost Analysis**: Transaction costs in USD for different operations

        Present data in clear, formatted tables with proper analysis and insights."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_l2_summary",
                    "description": "Get comprehensive summary data for Layer 2 solutions including TVL, market share, chain type, and stage information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums', 'others', 'notReviewed'",
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
                    "description": "Get activity metrics for Layer 2 solutions including daily transactions and TPS data.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "validiumsAndOptimiums", "others", "notReviewed"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums', 'others', 'notReviewed'",
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
                    "description": "Get transaction cost comparison across Layer 2 solutions for different operations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "others"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'others'",
                                "default": "rollups",
                            }
                        },
                        "required": [],
                    },
                },
            },
        ]

    def _build_url(self, data_type: str, category: str = "rollups") -> str:
        """Build URL with appropriate tab parameter based on category."""
        base_url = self.l2beat_base_urls[data_type]

        if category == "rollups":
            return base_url

        if category not in self.valid_tabs[data_type]:
            logger.warning(f"Invalid category '{category}' for {data_type}. Using default 'rollups'")
            return base_url

        return f"{base_url}?tab={category}"

    def filter_and_optimize_data(self, raw_data: Dict, requested_category: str) -> Dict:
        """
        STEP 1: Filter data to only include requested category
        STEP 2: Apply all optimizations to that category
        """
        if not isinstance(raw_data, dict):
            return raw_data
        entries = None
        if "entries" in raw_data:
            entries = raw_data["entries"]
        elif (
            "pageProps" in raw_data
            and "l2Data" in raw_data["pageProps"]
            and "entries" in raw_data["pageProps"]["l2Data"]
        ):
            entries = raw_data["pageProps"]["l2Data"]["entries"]
        else:
            logger.warning("No entries found in data")
            return raw_data
        if requested_category not in entries:
            logger.warning(f"Requested category '{requested_category}' not found in data")
            return raw_data

        category_entries = entries[requested_category]
        if not isinstance(category_entries, list):
            logger.warning(f"Category data is not a list: {type(category_entries)}")
            return raw_data

        optimized_entries = []
        processed_count = 0

        for i, entry in enumerate(category_entries):
            if not isinstance(entry, dict):
                continue

            entry_name = entry.get("name", f"Entry_{i}")
            tvs_order = entry.get("tvsOrder", 0)

            stage_value = "Unknown"
            if "stage" in entry and isinstance(entry["stage"], dict):
                stage_value = entry["stage"].get("stage", "Unknown")
            elif "stage" in entry:
                stage_value = str(entry["stage"])
            daily_change = 0.0
            if "tvs" in entry and isinstance(entry["tvs"], dict):
                daily_change = entry["tvs"].get("change", 0.0)

            # Create optimized entry
            optimized_entry = {
                "id": entry.get("id"),
                "name": entry_name,
                "stage": stage_value,
                "capability": entry.get("capability"),
                "proofSystem": entry.get("proofSystem", {}).get("type")
                if isinstance(entry.get("proofSystem"), dict)
                else entry.get("proofSystem"),
                "purposes": entry.get("purposes", []),
                "totalValueSecured": {
                    "tvs": tvs_order,
                    "dailyChange": daily_change,
                },
                "activity": {
                    "pastDayUops": entry.get("activity", {}).get("pastDayUops", 0),
                    "change": entry.get("activity", {}).get("change", 0),
                },
            }

            optimized_entries.append(optimized_entry)
            processed_count += 1

        result = {"entries": {requested_category: optimized_entries}}

        return result

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_summary(self, category: str = "rollups") -> Dict[str, Any]:
        try:
            url = self._build_url("summary", category)

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    text = await response.text()

            soup = BeautifulSoup(text, "html.parser")
            script = soup.find("script", string=lambda s: s and "__SSR_DATA__" in s)

            if not script:
                return {"status": "error", "error": f"__SSR_DATA__ script not found in {url}"}

            script_content = script.string.strip()
            if "=" not in script_content:
                return {"status": "error", "error": f"No assignment in script in {url}"}

            data_str = script_content.split("=", 1)[1].strip()
            if data_str.endswith(";"):
                data_str = data_str[:-1].strip()

            ssr_data = json.loads(data_str)
            raw_props = ssr_data.get("props", {})

            original_size = len(json.dumps(raw_props))
            optimized_data = self.filter_and_optimize_data(raw_props, category)

            # Generate final JSON
            content = json.dumps(optimized_data, separators=(",", ":"))
            optimized_size = len(content)

            reduction_percent = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
            logger.info(f"   Reduction: {reduction_percent:.1f}%")

            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
                "others": "Other L2s",
                "notReviewed": "Not Reviewed L2s",
            }

            return {
                "status": "success",
                "data": {
                    "content": content,
                    "source": url,
                    "data_type": f"L2 Summary (TVL & Market Share) - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            return {"status": "error", "error": f"Failed to fetch L2 summary data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_activity(self, category: str = "rollups") -> Dict[str, Any]:
        try:
            url = self._build_url("activity", category)

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    text = await response.text()

            soup = BeautifulSoup(text, "html.parser")
            script = soup.find("script", string=lambda s: s and "__SSR_DATA__" in s)

            if not script:
                return {"status": "error", "error": f"__SSR_DATA__ script not found in {url}"}

            script_content = script.string.strip()
            if "=" not in script_content:
                return {"status": "error", "error": f"No assignment in script in {url}"}

            data_str = script_content.split("=", 1)[1].strip()
            if data_str.endswith(";"):
                data_str = data_str[:-1].strip()

            ssr_data = json.loads(data_str)
            raw_props = ssr_data.get("props", {})
            optimized_data = self.filter_and_optimize_data(raw_props, category)
            content = json.dumps(optimized_data, separators=(",", ":"))

            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
                "others": "Other L2s",
                "notReviewed": "Not Reviewed L2s",
            }

            return {
                "status": "success",
                "data": {
                    "content": content,
                    "source": url,
                    "data_type": f"L2 Activity Metrics - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch L2 activity data: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_l2_costs(self, category: str = "rollups") -> Dict[str, Any]:
        logger.info(f"Fetching L2Beat costs for category: {category}")

        try:
            url = self._build_url("costs", category)

            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    text = await response.text()

            soup = BeautifulSoup(text, "html.parser")
            script = soup.find("script", string=lambda s: s and "__SSR_DATA__" in s)

            if not script:
                return {"status": "error", "error": f"__SSR_DATA__ script not found in {url}"}

            script_content = script.string.strip()
            if "=" not in script_content:
                return {"status": "error", "error": f"No assignment in script in {url}"}

            data_str = script_content.split("=", 1)[1].strip()
            if data_str.endswith(";"):
                data_str = data_str[:-1].strip()

            ssr_data = json.loads(data_str)
            raw_props = ssr_data.get("props", {})
            optimized_data = self.filter_and_optimize_data(raw_props, category)
            content = json.dumps(optimized_data, separators=(",", ":"))

            category_names = {
                "rollups": "Rollups",
                "others": "Other L2s",
            }

            return {
                "status": "success",
                "data": {
                    "content": content,
                    "source": url,
                    "data_type": f"L2 Transaction Costs - {category_names.get(category, 'Rollups')}",
                    "category": category,
                },
            }

        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return {"status": "error", "error": f"Failed to fetch L2 costs data: {str(e)}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Tool call: {tool_name} with args: {function_args}")

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
