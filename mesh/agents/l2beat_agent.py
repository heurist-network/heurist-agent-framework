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
            "costs": "https://l2beat.com/scaling/costs",
        }

        self.valid_tabs = {
            "summary": ["rollups", "validiumsAndOptimiums"],
            "costs": ["rollups", "validiumsAndOptimiums"],
        }

        self.metadata.update(
            {
                "name": "L2Beat Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Specialized agent for analyzing Layer 2 scaling solutions data from L2Beat. Provides comprehensive insights into L2 TVL, market share, and transaction costs across different chains and categories (Rollups, Validiums & Optimiums).",
                "external_apis": ["L2Beat"],
                "tags": ["L2Beat"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/L2Beat.png",
                "examples": [
                    "What's the current TVL and market share of top L2 solutions?",
                    "Which L2 has the lowest transaction costs right now?",
                    "What are the average transaction costs for ZK chains?",
                    "Compare the costs of different L2 solutions",
                    "What are the top Validiums and Optimiums by TVL?",
                ],
                "credits": {"default": 1},
            }
        )

    def get_system_prompt(self) -> str:
        return """Analyze Layer 2 scaling data from L2Beat focusing on:
        1. **Summary Data**: TVL (Total Value Locked), market share, chain types, security models, stages
        2. **Cost Analysis**: Average transaction costs per user operation in USD

        Present data in clear, formatted tables with proper analysis and insights. Focus on practical comparisons that help users choose the most suitable Layer 2 solution for their needs."""

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
                                "enum": ["rollups", "validiumsAndOptimiums"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums'",
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
                    "description": "Get simplified transaction cost data showing L2 name and average cost per user operation in USD.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["rollups", "validiumsAndOptimiums"],
                                "description": "Category of L2s to fetch. Options: 'rollups' (default), 'validiumsAndOptimiums'",
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

    def filter_and_optimize_summary_data(self, raw_data: Dict, requested_category: str) -> Dict:
        """
        Filter and optimize summary data to only include requested category
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

    def filter_and_optimize_costs_data(self, raw_data: Dict, requested_category: str) -> Dict:
        """
        Filter and optimize costs data to only include L2 name and average cost per user operation
        Uses costOrder field which represents the cost in USD per operation
        """
        if not isinstance(raw_data, dict):
            return raw_data

        entries = None
        costs_data = None
        if "entries" in raw_data:
            entries = raw_data["entries"]
        elif (
            "pageProps" in raw_data
            and "l2Data" in raw_data["pageProps"]
            and "entries" in raw_data["pageProps"]["l2Data"]
        ):
            entries = raw_data["pageProps"]["l2Data"]["entries"]
        if "pageProps" in raw_data and "costsData" in raw_data["pageProps"]:
            costs_data = raw_data["pageProps"]["costsData"]
        elif "costsData" in raw_data:
            costs_data = raw_data["costsData"]

        if costs_data and isinstance(costs_data, dict):
            if "entries" in costs_data:
                entries = costs_data["entries"]
            elif requested_category in costs_data:
                entries = {requested_category: costs_data[requested_category]}

        if not entries:
            logger.warning("No entries found in costs data")
            return {"entries": {requested_category: []}}

        if requested_category not in entries:
            logger.warning(f"Requested category '{requested_category}' not found in costs data")
            return {"entries": {requested_category: []}}

        category_entries = entries[requested_category]
        if not isinstance(category_entries, list):
            logger.warning(f"Category costs data is not a list: {type(category_entries)}")
            return {"entries": {requested_category: []}}

        optimized_entries = []

        for i, entry in enumerate(category_entries):
            if not isinstance(entry, dict):
                continue

            entry_name = entry.get("name", f"Entry_{i}")
            avg_cost_usd = 0.0
            if "costOrder" in entry:
                cost_value = entry["costOrder"]
                if isinstance(cost_value, (int, float)):
                    avg_cost_usd = float(cost_value)
            if avg_cost_usd == 0.0:
                possible_cost_fields = [
                    "avgCostPerL2Tx",
                    "averageCostPerUserOp",
                    "avgCost",
                    "costPerTx",
                    "totalCost",
                    "cost",
                    "UOPS",
                ]

                for field in possible_cost_fields:
                    if field in entry:
                        value = entry[field]
                        if isinstance(value, (int, float)):
                            avg_cost_usd = float(value)
                            break
                        elif isinstance(value, dict) and "usd" in value:
                            avg_cost_usd = float(value["usd"])
                            break

                if avg_cost_usd == 0.0:
                    nested_structures = ["costs", "data", "metrics", "fees"]
                    for struct in nested_structures:
                        if struct in entry and isinstance(entry[struct], dict):
                            costs_obj = entry[struct]

                            if "costOrder" in costs_obj:
                                cost_value = costs_obj["costOrder"]
                                if isinstance(cost_value, (int, float)):
                                    avg_cost_usd = float(cost_value)
                                    break
                            for field in possible_cost_fields:
                                if field in costs_obj:
                                    value = costs_obj[field]
                                    if isinstance(value, (int, float)):
                                        avg_cost_usd = float(value)
                                        break
                                    elif isinstance(value, dict) and "usd" in value:
                                        avg_cost_usd = float(value["usd"])
                                        break
                            if avg_cost_usd != 0.0:
                                break

                            for summary_field in ["total", "average", "avg"]:
                                if summary_field in costs_obj:
                                    summary_data = costs_obj[summary_field]
                                    if isinstance(summary_data, dict) and "usd" in summary_data:
                                        avg_cost_usd = float(summary_data["usd"])
                                        break
                                    elif isinstance(summary_data, (int, float)):
                                        avg_cost_usd = float(summary_data)
                                        break
                            if avg_cost_usd != 0.0:
                                break

            optimized_entry = {
                "id": entry.get("id"),
                "name": entry_name,
                "averageCostPerUserOp": avg_cost_usd,
            }

            optimized_entries.append(optimized_entry)

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
            optimized_data = self.filter_and_optimize_summary_data(raw_props, category)
            content = json.dumps(optimized_data, separators=(",", ":"))
            optimized_size = len(content)

            reduction_percent = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
            logger.info(f"   Summary data reduction: {reduction_percent:.1f}%")

            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
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
            original_size = len(json.dumps(raw_props))
            optimized_data = self.filter_and_optimize_costs_data(raw_props, category)
            content = json.dumps(optimized_data, separators=(",", ":"))
            optimized_size = len(content)
            reduction_percent = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
            logger.info(f"   Costs data reduction: {reduction_percent:.1f}%")

            category_names = {
                "rollups": "Rollups",
                "validiumsAndOptimiums": "Validiums & Optimiums",
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
        elif tool_name == "get_l2_costs":
            result = await self.get_l2_costs(category=category)
        else:
            return {"status": "error", "error": f"Unsupported tool: {tool_name}"}
        errors = self._handle_error(result)
        if errors:
            return errors
        return result
