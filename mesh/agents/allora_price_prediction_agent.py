import os
from typing import Any, Dict, List

import aiohttp
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()


class AlloraPricePredictionAgent(MeshAgent):
    def __init__(self):
        super().__init__()
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
                "tags": ["Prediction"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Allora.png",
                "examples": [
                    "What is the price prediction for BTC in the next 5 minutes?",
                    "Price prediction for ETH in the next 8 hours",
                ],
            }
        )

    async def __aenter__(self):
        """Initialize session for API calls"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when context is exited"""
        if self.session:
            await self.session.close()
            self.session = None

    def get_system_prompt(self) -> str:
        """Return the system prompt for Allora price prediction"""
        return """You are a helpful assistant that can access external tools to provide Bitcoin and Ethereum price prediction data.
        The price prediction is provided by Allora. You only have access to BTC and ETH data with 5-minute and 8-hour time frames.
        You don't have the ability to tell anything else. If the user's query is out of your scope, return a brief error message.
        If the user's query doesn't mention the time frame, use 5-minute by default.
        If the tool call successfully returns the data, limit your response to 50 words like a professional financial analyst,
        and output in CLEAN text format with no markdown or other formatting. Only return your response, no other text."""

    def get_tool_schemas(self) -> List[Dict]:
        """Return the available tool schemas for Allora API"""
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
    #                      ALLORA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
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
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle execution of tools and return the raw data"""
        if tool_name != "get_allora_prediction":
            return {"error": f"Unsupported tool '{tool_name}'"}

        token = function_args.get("token")
        timeframe = function_args.get("timeframe")

        if not token or not timeframe:
            return {"error": "Both 'token' and 'timeframe' are required in tool_arguments"}

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
