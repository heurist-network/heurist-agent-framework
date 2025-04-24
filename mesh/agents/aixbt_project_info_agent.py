import os
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()


class AixbtProjectInfoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "AixBT Project Info Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can retrieve trending project information using the aixbt API",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about a crypto project",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "project_id",
                        "description": "Specific project ID to query",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, the agent will only return the raw data without LLM explanation",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Detailed information about the cryptocurrency project",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured project data", "type": "dict"},
                ],
                "external_apis": ["aixbt"],
                "tags": ["Project Analysis"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/aixbt.png",
                "examples": [
                    "Tell me about Heurist",
                    "What are the latest developments for Ethereum?",
                    "Trending projects in the crypto space",
                ],
            }
        )

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
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
                    "description": "Search for cryptocurrency projects with various filtering options. Every field is optional. If not provided, the agent will return all projects. This tool returns project info and notable updates.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of projects to return (max 50)",
                                "default": 10,
                            },
                            "name": {
                                "type": "string",
                                "description": "Filter projects by name (case-insensitive regex match)",
                            },
                            "ticker": {
                                "type": "string",
                                "description": "Filter projects by ticker symbol (case-insensitive match)",
                            },
                            "xHandle": {
                                "type": "string",
                                "description": "Filter projects by X/Twitter handle",
                            },
                            "minScore": {
                                "type": "number",
                                "description": "Minimum score threshold for filtering projects. This is a time-varying value determined by the social trends of the project. Use 0 if a project name / ticker / handle is specified. Use 0.1~0.3 for general trending projects search. Use 0.4~0.5 to find the most popular projects.",
                            },
                            "chain": {
                                "type": "string",
                                "description": "Filter projects by blockchain (e.g., 'ethereum', 'solana', 'base')",
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
    @monitor_execution()
    @with_cache(ttl_seconds=3600)  # Cache for 1 hour
    @with_retry(max_retries=3)
    async def search_projects(
        self,
        limit: Optional[int] = 10,
        name: Optional[str] = None,
        ticker: Optional[str] = None,
        xHandle: Optional[str] = None,
        minScore: Optional[float] = None,
        chain: Optional[str] = None,
    ) -> Dict:
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            base_url = "https://api.aixbt.tech/v1"
            url = f"{base_url}/projects"

            # Build params dict with only non-None values
            params = {}
            if limit is not None:
                params["limit"] = min(limit, 50)  # Cap at API max
            if name is not None:
                params["name"] = name
            if ticker is not None:
                params["ticker"] = ticker
            if xHandle is not None:
                params["xHandle"] = xHandle.replace("@", "")
            if minScore is not None:
                params["minScore"] = minScore
            if chain is not None:
                params["chain"] = chain

            headers = {
                "accept": "*/*",
                "x-api-key": os.getenv("AIXBT_API_KEY"),
            }

            print(f"Searching for projects with params: {params} and headers: {headers}")
            print(f"URL: {url}")

            async with self.session.get(url, headers=headers, params=params) as response:
                # Even if we get an error status, try to parse the response
                status_code = response.status
                response_text = await response.text()

                try:
                    data = await response.json()
                    # Ensure we have a consistent format
                    if "projects" not in data:
                        data = {"projects": []}
                    return data
                except:
                    # If we can't parse as JSON, return an error
                    return {
                        "error": f"Failed to search projects. Status: {status_code}, Response: {response_text[:200]}..."
                    }
        except Exception as e:
            return {"error": f"Failed to search projects: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        if tool_name == "search_projects":
            # Extract all possible parameters with None as default
            limit = function_args.get("limit", 10)
            name = function_args.get("name")
            ticker = function_args.get("ticker")
            xHandle = function_args.get("xHandle")
            minScore = function_args.get("minScore")
            chain = function_args.get("chain")

            result = await self.search_projects(
                limit=limit, name=name, ticker=ticker, xHandle=xHandle, minScore=minScore, chain=chain
            )

            errors = self._handle_error(result)
            if errors:
                return errors

            return {"search_results": result}

        else:
            return {"error": f"Unsupported tool '{tool_name}'"}
