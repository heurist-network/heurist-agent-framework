import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv
from spaceandtime import SpaceAndTime

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class SpaceTimeAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("SPACE_AND_TIME_API_KEY")
        if not self.api_key:
            raise ValueError("SPACE_AND_TIME_API_KEY environment variable is required")
        self.client = None
        self.access_token = None
        self.refresh_token = None
        self.sql_generate_url = "https://api.spaceandtime.dev/v1/ai/sql/generate"
        self.sql_execute_url = "https://proxy.api.spaceandtime.dev/v1/sql"

        self.metadata.update(
            {
                "name": "Space and Time Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can analyze blockchain data by executing SQL queries from natural language using Space and Time, a database with ZK proofs.",
                "external_apis": ["Space and Time"],
                "tags": ["Onchain Data"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/SpacenTime.png",
                "examples": [
                    "Get the number of blocks created on Ethereum per day over the last month",
                    "Tell me top 10 GPUs from HEURIST",
                    "How many transactions occurred on Ethereum yesterday?",
                    "What's the largest transaction value on Ethereum in the past 24 hours?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        IDENTITY:
        You are a blockchain data analyst with expertise in generating SQL queries for Space and Time.

        CAPABILITIES:
        - Generate SQL queries from natural language descriptions
        - Execute SQL queries against blockchain data
        - Analyze and explain query results in an accessible way

        RESPONSE GUIDELINES:
        - Present time-series data with appropriate aggregation (daily, weekly, etc.)
        - Identify trends and patterns in the data
        - Explain technical blockchain terms in accessible language
        - Format numeric data appropriately (use K, M, B suffixes for large numbers)

        DOMAIN-SPECIFIC RULES:
        When analyzing blockchain data:
        1. Clearly state the time period covered by the analysis
        2. Be precise about which blockchain networks the data comes from
        3. Highlight significant changes or anomalies in the data
        4. Provide context for blockchain metrics when relevant

        IMPORTANT:
        - Never invent or assume data that isn't present in the query results
        - If the query results are empty or unexpected, suggest possible reasons
        - Keep explanations concise but informative
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "generate_and_execute_sql",
                    "description": "Use this to analyze blockchain data including transactions, blocks, and wallet activities. Internally, this tool generates a SQL query from natural language and execute it against blockchain data. Supported chains: Ethereum, Bitcoin, Polygon, Avalanche, Sui, ZKsync Era.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "nl_query": {
                                "type": "string",
                                "description": "Natural language description of the blockchain data query",
                            },
                        },
                        "required": ["nl_query"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    @with_retry(max_retries=3)
    async def _authenticate(self):
        """Authenticate with Space and Time API if not already authenticated"""
        if not self.client:
            try:
                logger.info("Authenticating with Space and Time API")
                self.client = SpaceAndTime(api_key=self.api_key)
                self.client.authenticate()
                self.access_token = self.client.access_token
                self.refresh_token = self.client.refresh_token
                logger.info("Authentication successful")
            except Exception as e:
                logger.error(f"Authentication failed: {str(e)}")
                raise

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def generate_sql(self, nl_query: str) -> Dict:
        """Generate SQL from natural language using Space and Time API"""
        await self._authenticate()

        try:
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            payload = {"prompt": nl_query, "metadata": {}}

            result = await self._api_request(
                url=self.sql_generate_url, method="POST", headers=headers, json_data=payload
            )
            if "error" in result:
                return result

            # Check for both "sql" and "SQL" keys
            sql_query = result.get("sql") or result.get("SQL")
            if not sql_query:
                return {"error": "The response did not contain a SQL query."}

            return {"status": "success", "sql_query": sql_query}

        except Exception as e:
            logger.error(f"SQL generation error: {str(e)}")
            return {"error": f"Failed to generate SQL query: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def execute_sql(self, sql_query: str) -> Dict:
        """Execute SQL query using Space and Time API"""
        try:
            headers = {"accept": "application/json", "apikey": self.api_key, "content-type": "application/json"}
            payload = {"sqlText": sql_query}
            async with aiohttp.ClientSession() as session:
                async with session.post(self.sql_execute_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {"status": "success", "result": result}
                    else:
                        error_text = await response.text()
                        logger.error(f"SQL execution error: {response.status}, {error_text}")
                        return {"error": f"Failed to execute SQL query: HTTP {response.status}"}

        except Exception as e:
            logger.error(f"SQL execution error: {str(e)}")
            return {"error": f"Failed to execute SQL query: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def generate_and_execute_sql(self, nl_query: str) -> Dict:
        """Generate SQL from natural language and execute it"""
        # Generate SQL
        sql_result = await self.generate_sql(nl_query)
        if errors := self._handle_error(sql_result):
            return errors

        sql_query = sql_result.get("sql_query")

        # Execute SQL
        execution_result = await self.execute_sql(sql_query)
        if errors := self._handle_error(execution_result):
            return errors

        # Combine results
        return {
            "status": "success",
            "nl_query": nl_query,
            "sql_query": sql_query,
            "result": execution_result.get("result"),
        }

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle tool execution based on the tool name"""
        if tool_name == "generate_and_execute_sql":
            nl_query = function_args.get("nl_query")
            if not nl_query:
                return {"error": "Missing 'nl_query' in tool_arguments"}

            logger.info(f"Generating and executing SQL for: {nl_query}")
            result = await self.generate_and_execute_sql(nl_query)

            if errors := self._handle_error(result):
                return errors

            return result
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}
