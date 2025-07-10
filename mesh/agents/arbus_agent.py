import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class ArbusAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("ARBUS_API_KEY")
        if not self.api_key:
            raise ValueError("ARBUS_API_KEY environment variable is required")

        self.base_url = "https://api.arbus.ai/v1"
        self.headers = {"Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Arbus AI Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent provides professional-grade cryptocurrency analysis, sentiment tracking, and market intelligence using Arbus AI. Get AI-powered market insights and structured reports.",
                "external_apis": ["Arbus AI"],
                "tags": ["Market Analysis"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Arbus.png",
                "examples": [
                    "Is Bitcoin bullish right now?",
                    "What's happening with DeFi markets?",
                    "Generate a report on Solana's partnerships",
                    "Analyze the current crypto market sentiment",
                ],
                "credits": 0,
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a professional cryptocurrency market analyst that provides expert insights using Arbus AI's market intelligence data.

You can help users with:
- Real-time crypto market analysis and sentiment
- AI-powered answers to any crypto market questions
- Structured intelligence reports on partnerships, development, and funding

Be objective and factual in your analysis. Provide clear, actionable insights based on the data returned. If the user's query is outside your scope, provide a brief explanation and suggest how they might rephrase their question.

Format your responses in clean text without markdown or special formatting. Focus on delivering valuable market intelligence and analysis."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_ai_assistant",
                    "description": "Ask any question about crypto markets and get AI-powered analysis based on real-time data. Perfect for market sentiment, price movements, or general crypto questions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Your question about crypto markets (e.g., 'Is Bitcoin bullish right now?', 'What's happening with DeFi?')",
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days of data to analyze (1-365)",
                                "default": 7,
                                "minimum": 1,
                                "maximum": 365,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_report",
                    "description": "Generate structured intelligence reports for crypto projects with categorized findings like partnerships, development, funding, and market developments.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "twitter_handle": {
                                "type": "string",
                                "description": "Project's Twitter handle (without @ symbol, e.g., 'ethereum', 'solana')",
                            },
                            "category": {
                                "type": "string",
                                "description": "Report category type (Note: 'alerts' category may not be available for all projects)",
                                "enum": ["projects", "threador"],
                                "default": "projects",
                            },
                            "date_from": {
                                "type": "string",
                                "description": "Start date for report data (YYYY-MM-DD format, optional)",
                            },
                            "date_to": {
                                "type": "string",
                                "description": "End date for report data (YYYY-MM-DD format, optional)",
                            },
                        },
                        "required": ["twitter_handle"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      ARBUS AI API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def ask_ai_assistant(self, query: str, days: int = 7) -> Dict[str, Any]:
        """
        Ask any question about crypto markets and get AI-powered analysis.

        Args:
            query: Your question about crypto markets
            days: Days of data to analyze (1-365)

        Returns:
            Dict containing AI analysis or error information
        """
        try:
            url = f"{self.base_url}/ask-ai-assistant"

            # Add API key as query parameter
            params = {"key": self.api_key}

            payload = {
                "query": query,
                "days": max(1, min(days, 365)),  # Ensure days is within valid range
            }

            logger.info(f"Asking AI assistant: {query} (analyzing {days} days)")

            result = await self._api_request(
                url=url, method="POST", headers=self.headers, params=params, json_data=payload
            )

            if "error" in result:
                logger.error(f"API error: {result['error']}")
                return {"status": "error", "error": result["error"]}

            logger.info("Successfully got AI assistant response")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Error asking AI assistant: {str(e)}")
            return {"status": "error", "error": f"Failed to get AI analysis: {str(e)}"}

    @monitor_execution()
    @with_cache(ttl_seconds=900)
    @with_retry(max_retries=3)
    async def generate_report(
        self,
        twitter_handle: str,
        category: str = "projects",
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate structured reports for crypto projects.

        Args:
            twitter_handle: Project's Twitter handle (without @ symbol)
            category: Report category ('projects', 'threador', 'alerts')
            date_from: Start date (YYYY-MM-DD format, optional)
            date_to: End date (YYYY-MM-DD format, optional)

        Returns:
            Dict containing structured report or error information
        """
        try:
            url = f"{self.base_url}/report"

            # Add API key as query parameter
            params = {"key": self.api_key}

            # Remove @ symbol if present
            clean_handle = twitter_handle.lstrip("@")

            payload = {"twitter_handle": clean_handle, "category": category}

            # Add optional date range if provided
            if date_from:
                payload["date_from"] = date_from
            if date_to:
                payload["date_to"] = date_to

            logger.info(f"Generating report for {clean_handle} (category: {category})")

            result = await self._api_request(
                url=url, method="POST", headers=self.headers, params=params, json_data=payload
            )

            if "error" in result:
                logger.error(f"API error: {result['error']}")
                return {"status": "error", "error": result["error"]}

            logger.info(f"Successfully generated report for {clean_handle}")
            return {"status": "success", "data": result}

        except Exception as e:
            logger.error(f"Error generating report for {twitter_handle}: {str(e)}")
            return {"status": "error", "error": f"Failed to generate report: {str(e)}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution logic"""

        if tool_name == "ask_ai_assistant":
            query = function_args.get("query")
            days = function_args.get("days", 7)

            if not query:
                return {"error": "Query parameter is required"}

            logger.info(f"Handling AI assistant query: {query}")
            result = await self.ask_ai_assistant(query=query, days=days)

            if result.get("status") == "error":
                return {"error": result.get("error", "Failed to get AI analysis")}

            return result.get("data", {})

        elif tool_name == "generate_report":
            twitter_handle = function_args.get("twitter_handle")
            category = function_args.get("category", "projects")
            date_from = function_args.get("date_from")
            date_to = function_args.get("date_to")

            if not twitter_handle:
                return {"error": "twitter_handle parameter is required"}

            logger.info(f"Handling report generation: {twitter_handle}")
            result = await self.generate_report(
                twitter_handle=twitter_handle, category=category, date_from=date_from, date_to=date_to
            )

            if result.get("status") == "error":
                return {"error": result.get("error", "Failed to generate report")}

            return result.get("data", {})

        else:
            return {"error": f"Unsupported tool: {tool_name}"}
