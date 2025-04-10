import json
import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from spaceandtime import SpaceAndTime

from core.llm import call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class SpaceTimeAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("SPACE_AND_TIME_API_KEY")
        if not self.api_key:
            raise ValueError("SPACE_AND_TIME_API_KEY environment variable is required")

        # Initialize SxT client but don't authenticate yet (we'll do this on first request)
        self.client = None
        self.access_token = None
        self.refresh_token = None

        self.metadata.update(
            {
                "name": "Space and Time Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can analyze blockchain data by executing SQL queries from natural language using Space and Time, a database with ZK proofs.",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query to generate SQL from",
                        "type": "str",
                        "required": False,
                    },
                    {
                        "name": "raw_data_only",
                        "description": "If true, returns only raw data without analysis",
                        "type": "bool",
                        "required": False,
                        "default": False,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Natural language explanation of the query results",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Structured data from SQL execution including the generated query",
                        "type": "dict",
                    },
                ],
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
            url_generate = "https://api.spaceandtime.dev/v1/ai/sql/generate"
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
            payload = {"prompt": nl_query, "metadata": {}}

            response = requests.post(url_generate, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Check for both "sql" and "SQL" keys
            sql_query = result.get("sql") or result.get("SQL")
            if not sql_query:
                return {"error": "The response did not contain a SQL query."}

            return {"status": "success", "sql_query": sql_query}

        except requests.exceptions.RequestException as e:
            logger.error(f"SQL generation error: {str(e)}")
            return {"error": f"Failed to generate SQL query: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error during SQL generation: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def execute_sql(self, sql_query: str) -> Dict:
        """Execute SQL query using Space and Time API"""
        try:
            url_execute = "https://proxy.api.spaceandtime.dev/v1/sql"
            headers = {"accept": "application/json", "apikey": self.api_key, "content-type": "application/json"}
            payload = {"sqlText": sql_query}

            response = requests.post(url_execute, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            return {"status": "success", "result": result}

        except requests.exceptions.RequestException as e:
            logger.error(f"SQL execution error: {str(e)}")
            return {"error": f"Failed to execute SQL query: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error during SQL execution: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def generate_and_execute_sql(self, nl_query: str) -> Dict:
        """Generate SQL from natural language and execute it"""
        # Generate SQL
        sql_result = await self.generate_sql(nl_query)
        errors = self._handle_error(sql_result)
        if errors:
            return errors

        sql_query = sql_result.get("sql_query")

        # Execute SQL
        execution_result = await self.execute_sql(sql_query)
        errors = self._handle_error(execution_result)
        if errors:
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
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle tool execution based on the tool name"""
        if tool_name == "generate_and_execute_sql":
            nl_query = function_args.get("nl_query")
            if not nl_query:
                return {"error": "Missing 'nl_query' in tool_arguments"}

            logger.info(f"Generating and executing SQL for: {nl_query}")
            result = await self.generate_and_execute_sql(nl_query)
            errors = self._handle_error(result)
            if errors:
                return errors
            return result
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle both direct tool calls and natural language queries.
        Either 'query' or 'tool' must be provided in params.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            # Direct tool call mode - no LLM calls
            data = await self._handle_tool_logic(tool_name=tool_name, function_args=tool_args)
            return {"response": "", "data": data}

        # ---------------------
        # 2) NATURAL LANGUAGE QUERY (LLM decides the tool)
        # ---------------------
        if query:
            response = await call_llm_with_tools_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                user_prompt=query,
                temperature=0.1,
                tools=self.get_tool_schemas(),
            )

            if not response:
                return {"error": "Failed to process query"}

            if not response.get("tool_calls"):
                return {"response": response["content"], "data": {}}

            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            data = await self._handle_tool_logic(tool_name=tool_call_name, function_args=tool_call_args)

            if raw_data_only:
                return {"response": "", "data": data}

            explanation = await self._respond_with_llm(
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                query=query,
                tool_call_id=tool_call.id,
                data=data,
                temperature=0.4,
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
