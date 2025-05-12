import logging
import os
import ssl
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
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Aixbt.png",
                "examples": [
                    "Tell me about Heurist",
                    "What are the latest developments for Ethereum?",
                    "Trending projects in the crypto space",
                ],
            }
        )

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
                    "description": "Search for cryptocurrency projects with comprehensive details including fundamental analysis, market performance, social activity, and recent developments. Return detailed insights on project descriptions, token contracts across multiple chains, Twitter handles, community metrics, price movements, and chronological timelines of notable updates. Perfect for discovering trending projects, researching specific tokens by name/ticker/Twitter handle, or filtering projects by blockchain network and popularity scores.",
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
        ]

    # ------------------------------------------------------------------------
    #                      AIXBT API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=3600)
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

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle AIXBT tool calls."""
        if tool_name != "search_projects":
            return {"error": f"Unsupported tool: {tool_name}", "data": {"projects": []}}

        result = await self.search_projects(
            limit=function_args.get("limit", 10),
            name=function_args.get("name"),
            ticker=function_args.get("ticker"),
            xHandle=function_args.get("xHandle"),
            minScore=function_args.get("minScore"),
            chain=function_args.get("chain"),
        )

        if result.get("error"):
            logger.warning(f"AIXBT error: {result['error']}")
            return {"error": result["error"], "data": {"projects": []}}

        return {"data": result}
