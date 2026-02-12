import logging
import os
import re
import ssl
import subprocess
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class AIXBTProjectInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.session = None
        self.api_key = os.getenv("AIXBT_API_KEY")
        if not self.api_key:
            raise ValueError("AIXBT_API_KEY environment variable is required")

        self.base_url = "https://api.aixbt.tech/v1"
        self.headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {self.api_key}",
        }

        self.metadata.update(
            {
                "name": "AIXBT Project Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can retrieve trending project information including fundamental analysis, social activity, and recent developments using the aixbt API",
                "external_apis": ["aixbt"],
                "tags": ["Project Analysis"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Aixbt.png",
                "examples": [
                    "Tell me about Heurist",
                    "What are the latest developments for Ethereum?",
                    "Trending projects in the crypto space",
                    "What's happening in the crypto market today?",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    # Timeout policy: 10s, no fallback (return error on timeout)
    def get_default_timeout_seconds(self) -> Optional[int]:
        return 10

    async def get_fallback_for_tool(
        self, tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return None

    # Keep the original session management to maintain SSL behavior
    async def __aenter__(self):
        # Create session with SSL verification disabled
        # This is needed specifically for the aixbt API due to certificate issues
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def cleanup(self):
        """Close any open resources"""
        if self.session:
            await self.session.close()
            self.session = None

    def get_system_prompt(self) -> str:
        return """You are a helpful assistant that can access external tools to provide detailed cryptocurrency project information. The project data is provided by aixbt (a crypto AI agent).

        If the user's query is out of your scope, return a brief error message.

        The AixBT API may have limitations and may not contain information for all cryptocurrency projects.
        If information about a specific project is not available, suggest that the user try searching for
        name, ticker or Twitter handle.

        IMPORTANT: For market summary requests:
        - The market summary tool can provide data for 1-3 days maximum
        - If a user requests more than 3 days (e.g., week, month), inform them that only the last 3 days of data are available and provide those 3 days
        - Always mention the actual number of days returned when providing market summaries

        Format your response in clean text without markdown or special formatting. Be objective and informative in your analysis.
        If the information is not available or incomplete, clearly state what is missing but remain helpful.

        Note that the AixBT API is primarily focused on cryptocurrency and blockchain projects. If users ask about
        non-crypto projects, explain the limitations of this service."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_projects",
                    "description": "Search for cryptocurrency projects with comprehensive details including fundamental analysis, market performance, social activity, and recent developments. Returns detailed insights on project names, descriptions, token contracts across multiple chains, Twitter handles, ticker symbols, CoinGecko IDs, and chronological signals/updates of notable project events. Perfect for discovering trending projects, researching specific tokens by name/ticker/Twitter handle, or filtering projects by blockchain network and popularity scores.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of projects to return (max 50).",
                                "default": 10,
                            },
                            "name": {
                                "type": "string",
                                "description": "Filter projects by name (case-insensitive regex match). Effective for finding specific projects or related projects sharing similar naming conventions.",
                            },
                            "ticker": {
                                "type": "string",
                                "description": "Filter projects by ticker symbol (case-insensitive match). Useful when you know the exact trading symbol of a token.",
                            },
                            "xHandle": {
                                "type": "string",
                                "description": "Filter projects by X/Twitter handle. Ideal for finding projects from their social media identities, with or without the @ symbol.",
                            },
                            "minScore": {
                                "type": "number",
                                "description": "Minimum score threshold for filtering projects based on social trends and market activity. Use 0 if a project name/ticker/handle is specified. For trending projects, use 0.1-0.3. For the most popular projects only, use 0.4-0.5. Higher scores indicate more significant current market attention.",
                            },
                            "chain": {
                                "type": "string",
                                "description": "Filter projects by blockchain (e.g., 'ethereum', 'solana', 'base'). Returns projects with tokens deployed on the specified chain, useful for ecosystem-specific research.",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_summary",
                    "description": "Get a summary of recent market-wide news including macroeconomics, major crypto tokens important updates of trending crypto projects. This tool returns 10~15 bite-sized news about various topics like market trends, opportunities and catalysts. Useful for knowing what's going on in crypto.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lookback_days": {
                                "type": "integer",
                                "description": "Number of days of market summaries to retrieve (1-3 days).",
                                "default": 1,
                                "minimum": 1,
                                "maximum": 3,
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      AIXBT API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=10000)
    @with_retry(max_retries=3)
    async def search_projects(
        self,
        limit: Optional[int] = 10,
        name: Optional[str] = None,
        ticker: Optional[str] = None,
        xHandle: Optional[str] = None,
        minScore: Optional[float] = None,
        chain: Optional[str] = None,
    ) -> Dict[str, Any]:
        should_close = False
        if not self.session:
            # Create a session with SSL verification disabled if needed
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))
            should_close = True

        try:
            url = f"{self.base_url}/projects"

            params = {
                "limit": min(limit, 50) if limit else None,
                "name": name,
                "ticker": ticker,
                "xHandle": xHandle.replace("@", "") if xHandle else None,
                "minScore": minScore,
                "chain": chain.lower() if chain else None,
            }
            params = {k: v for k, v in params.items() if v is not None}
            logger.info(f"Searching projects with params: {params}")

            # Keep the original request implementation for consistency
            async with self.session.get(url, headers=self.headers, params=params) as response:
                text = await response.text()
                if response.status != 200:
                    logger.error(f"API Error {response.status}: {text[:200]}")
                    return {"error": f"API Error {response.status}: {text[:200]}", "projects": []}

                try:
                    data = await response.json()
                except Exception as e:
                    logger.error(f"JSON decode error: {e}")
                    return {"error": f"Failed to parse API response: {e}", "projects": []}

                if isinstance(data, list):
                    return {"projects": data}

                if isinstance(data, dict):
                    if data.get("status") == 200 and "data" in data:
                        return {"projects": data["data"]}
                    if "projects" in data:
                        return data
                    return {"error": data.get("error", "Unexpected API response"), "projects": []}

                logger.warning(f"Unexpected format: {data}")
                return {"projects": []}

        except Exception as e:
            logger.error(f"Exception during project search: {e}")
            return {"error": f"Failed to search projects: {e}", "projects": []}

        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    def _is_date_stale(self, date_str: str, max_age_days: int = 3) -> bool:
        """Check if a date string is older than max_age_days"""
        try:
            clean_date = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)
            clean_date = clean_date.split(",")[0].strip()
            parsed_date = datetime.strptime(clean_date, "%d %B %Y")
            age_days = (datetime.now() - parsed_date).days
            return age_days > max_age_days
        except Exception as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return True

    def _fetch_day_page(self, date_str: str) -> Optional[Dict[str, Any]]:
        """Fetch and parse a single day's market insights page.
        date_str: format YYYY-MM-DD
        Returns dict with date and news items, or None if failed/empty.
        """
        url = f"https://aixbt.tech/market-insights/{date_str}"
        try:
            result = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-L",
                    "-H",
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0 or not result.stdout:
                return None

            html = result.stdout

            # Extract list items from the HTML
            li_items = re.findall(r'<li>(.*?)</li>', html, re.DOTALL)

            if not li_items:
                return None

            # Clean HTML tags from each item
            news_items = []
            for item in li_items:
                # Remove HTML tags
                clean_item = re.sub(r'<[^>]+>', '', item).strip()
                # Remove extra whitespace
                clean_item = re.sub(r'\s+', ' ', clean_item)

                if clean_item and len(clean_item) > 50:  # Filter out short/empty items
                    news_items.append(clean_item)

            if not news_items:
                return None

            return {"date": date_str, "news": news_items}

        except subprocess.TimeoutExpired:
            logger.warning(f"Timeout fetching {url}")
            return None
        except Exception as e:
            logger.warning(f"Error fetching {url}: {e}")
            return None

    @with_cache(ttl_seconds=10000)
    @with_retry(max_retries=3)
    async def get_market_summary(self, lookback_days: Optional[int] = 1) -> Dict[str, Any]:
        """Fetch market summary from individual day pages at aixbt.tech/market-insights/YYYY-MM-DD"""
        lookback_days = max(1, min(lookback_days or 1, 3))

        try:
            summaries = []
            today = datetime.now()

            # Try today first, then go back. Due to timezone delays, today's page may not exist yet.
            # We'll try up to lookback_days + 1 dates to account for this.
            for days_ago in range(lookback_days + 1):
                if len(summaries) >= lookback_days:
                    break

                target_date = today - timedelta(days=days_ago)
                date_str = target_date.strftime("%Y-%m-%d")
                day_data = self._fetch_day_page(date_str)

                if day_data:
                    summaries.append(day_data)

            return {
                "lookback_days": lookback_days,
                "summaries": summaries,
            }
        except Exception as e:
            logger.error(f"Market summary error: {e}")
            return {"error": str(e), "summaries": []}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle AIXBT tool calls."""
        if tool_name == "search_projects":
            result = await self.search_projects(
                limit=int(function_args.get("limit", 10)),
                name=function_args.get("name"),
                ticker=function_args.get("ticker"),
                xHandle=function_args.get("xHandle"),
                minScore=float(function_args.get("minScore")) if function_args.get("minScore") is not None else None,
                chain=function_args.get("chain"),
            )

            if result.get("error"):
                logger.warning(f"AIXBT error: {result['error']}")
                return {"error": result["error"], "data": {"projects": []}}

            # Clean up response to reduce size
            if "projects" in result:
                for project in result["projects"]:
                    if not project:
                        continue
                    if "id" in project:
                        del project["id"]
                    for summary in project.get("summaries", []):
                        if "id" in summary:
                            del summary["id"]
                        if "date" in summary and summary["date"]:
                            summary["date"] = summary["date"][:10]

            return {"data": result}

        elif tool_name == "get_market_summary":
            result = await self.get_market_summary(lookback_days=int(function_args.get("lookback_days", 1)))

            if result.get("error"):
                logger.warning(f"Market summary error: {result['error']}")
                return {"error": result["error"], "data": {"summaries": []}}

            return {"data": result}

        else:
            return {"error": f"Unsupported tool: {tool_name}", "data": {}}
