import json
import logging
import os
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class AlloraPricePredictionAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.session = None
        self.metadata.update(
            {
                "name": "Allora Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can predict the price of ETH/BTC with confidence intervals using Allora price prediction API",
                "inputs": [
                    {
                        "name": "query",
                        "description": "Natural language query about price prediction for ETH or BTC",
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
                        "description": "The price prediction with confidence intervals",
                        "type": "str",
                    },
                    {"name": "data", "description": "Structured prediction data", "type": "dict"},
                ],
                "external_apis": ["Allora"],
                "tags": ["Trading", "Prediction"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Allora.png",
                "examples": [
                    "What is the price prediction for BTC in the next 5 minutes?",
                    "Price prediction for ETH in the next 8 hours",
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
        return """You are a helpful assistant that can access external tools to provide Bitcoin and Ethereum price prediction data.
        The price prediction is provided by Allora. You only have access to BTC and ETH data with 5-minute and 8-hour time frames.
        You don't have the ability to tell anything else. If the user's query is out of your scope, return a brief error message.
        If the user's query doesn't mention the time frame, use 5-minute by default.
        If the tool call successfully returns the data, limit your response to 50 words like a professional financial analyst,
        and output in CLEAN text format with no markdown or other formatting. Only return your response, no other text."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_allora_prediction",
                    "description": "Get price prediction for ETH or BTC with confidence intervals",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token": {
                                "type": "string",
                                "description": "The cryptocurrency symbol (ETH or BTC)",
                                "enum": ["ETH", "BTC"],
                            },
                            "timeframe": {
                                "type": "string",
                                "description": "Time period for prediction",
                                "enum": ["5m", "8h"],
                            },
                        },
                        "required": ["token", "timeframe"],
                    },
                },
            }
        ]

    # ------------------------------------------------------------------------
    #                       SHARED / UTILITY METHODS
    # ------------------------------------------------------------------------
    async def _respond_with_llm(self, query: str, tool_call_id: str, data: dict, temperature: float) -> str:
        """Generate a natural language response using the LLM"""
        return await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query},
                {"role": "tool", "content": str(data), "tool_call_id": tool_call_id},
            ],
            temperature=temperature,
        )

    def _handle_error(self, maybe_error: dict) -> dict:
        """Check for and return any errors in the response"""
        if "error" in maybe_error:
            return {"error": maybe_error["error"]}
        return {}

    # ------------------------------------------------------------------------
    #                      ALLORA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_allora_prediction(self, token: str, timeframe: str) -> Dict:
        """Fetch price prediction data from Allora API"""
        should_close = False
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True

        try:
            base_url = "https://api.upshot.xyz/v2/allora/consumer/price/ethereum-11155111"
            url = f"{base_url}/{token.upper()}/{timeframe}"

            headers = {
                "accept": "application/json",
                "x-api-key": os.getenv("ALLORA_API_KEY"),
            }

            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()

                prediction = float(data["data"]["inference_data"]["network_inference_normalized"])
                confidence_intervals = data["data"]["inference_data"]["confidence_interval_percentiles_normalized"]
                confidence_interval_values_normalized = data["data"]["inference_data"][
                    "confidence_interval_values_normalized"
                ]

                return {
                    "prediction": prediction,
                    "confidence_intervals": confidence_intervals,
                    "confidence_interval_values_normalized": confidence_interval_values_normalized,
                }
        except Exception as e:
            return {"error": f"Failed to fetch prediction: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None

    # ------------------------------------------------------------------------
    #                      COMMON HANDLER LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""

        if tool_name != "get_allora_prediction":
            return {"error": f"Unsupported tool '{tool_name}'"}

        token = function_args.get("token")
        timeframe = function_args.get("timeframe")

        if not token or not timeframe:
            return {"error": "Both 'token' and 'timeframe' are required in tool_arguments"}

        logger.info(f"Getting prediction for {token} with {timeframe} timeframe")
        result = await self.get_allora_prediction(token, timeframe)

        errors = self._handle_error(result)
        if errors:
            return errors

        formatted_data = {
            "prediction_data": {
                "token": token,
                "timeframe": timeframe,
                "prediction": result["prediction"],
                "confidence_intervals": result["confidence_intervals"],
                "confidence_interval_values": result["confidence_interval_values_normalized"],
            }
        }

        return formatted_data

    # ------------------------------------------------------------------------
    #                      MAIN HANDLER
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages, supporting both direct tool calls and natural language queries.

        Either 'query' or 'tool' is required in params.
        - If 'query' is present, it means "agent mode", we use LLM to interpret the query and call tools
          - if 'raw_data_only' is present, we return tool results without another LLM call
        - If 'tool' is present, it means "direct tool call mode", we bypass LLM and directly call the API
          - never run another LLM call, this minimizes latency and reduces error
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
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
                query=query, tool_call_id=tool_call.id, data=data, temperature=0.1
            )
            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}
