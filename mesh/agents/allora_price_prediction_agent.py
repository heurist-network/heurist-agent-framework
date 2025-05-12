import os
from typing import Any, Dict, List, Optional

from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent


class AlloraPricePredictionAgent(MeshAgent):
    def __init__(self):
        super().__init__()

        self.api_key = os.getenv("ALLORA_API_KEY")
        if not self.api_key:
            raise ValueError("ALLORA_API_KEY environment variable is required")
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key,
        }

        self.metadata.update(
            {
                "name": "Allora Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent can predict the price of ETH/BTC with confidence intervals using Allora price prediction API",
                "external_apis": ["Allora"],
                "tags": ["Prediction"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Allora.png",
                "examples": [
                    "What is the price prediction for BTC in the next 5 minutes?",
                    "Price prediction for ETH in the next 8 hours",
                ],
            }
        )

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
    #                      ALLORA API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def get_allora_prediction(self, token: str, timeframe: str) -> Dict[str, Any]:
        """Fetch normalized price prediction data from Allora API."""
        if not token or not timeframe:
            return {"error": "Both 'token' and 'timeframe' are required"}

        url = f"https://api.upshot.xyz/v2/allora/consumer/price/ethereum-11155111/{token.upper()}/{timeframe}"

        try:
            response = await self._api_request(url=url, method="GET", headers=self.headers)

            if "error" in response:
                return {"error": response["error"]}

            inference = response["data"]["inference_data"]

            return {
                "prediction": float(inference["network_inference_normalized"]),
                "confidence_intervals": inference["confidence_interval_percentiles_normalized"],
                "confidence_interval_values": inference["confidence_interval_values_normalized"],
            }
        except Exception as e:
            return {"error": f"Allora API error: {e}"}

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle Allora prediction tool logic."""
        if tool_name != "get_allora_prediction":
            return {"error": f"Unsupported tool '{tool_name}'"}

        token = function_args.get("token")
        timeframe = function_args.get("timeframe")

        result = await self.get_allora_prediction(token, timeframe)

        if errors := self._handle_error(result):
            return errors

        return {
            "prediction_data": {
                "token": token,
                "timeframe": timeframe,
                **{k: result[k] for k in ("prediction", "confidence_intervals", "confidence_interval_values")},
            }
        }
