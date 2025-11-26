import logging
import os
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class SallyHealthAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("SALLY_API_KEY")
        if not self.api_key:
            raise ValueError("SALLY_API_KEY environment variable is required")

        self.base_url = "https://api-dev-a1c.sallya1c.com/conversations/v1/terminal/heurist"
        self.headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Sally Health Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Sally is a health and medical AI assistant. This agent talks to Sally about medical and health topics, providing helpful information and guidance.",
                "external_apis": ["Sally"],
                "tags": ["Health"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Sally.png",
                "examples": [
                    "How can I stay fit with a work from home routine?",
                    "What are good foods for heart health?",
                    "Tips for better sleep quality",
                    "How to manage stress naturally?",
                ],
                "credits": 0,
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are an AI assistant that helps users with health and medical questions using Sally AI.
Your role is to facilitate health-related queries and present the information clearly."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_health_advice",
                    "description": "Sally is a health and medical AI assistant. This tool talks to Sally about medical and health topics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Message in natural language to talk to Sally agent. It can be a question or a prompt for information about health and medical topics.",
                            },
                        },
                        "required": ["message"],
                    },
                },
            }
        ]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def ask_health_advice(self, message: str) -> Dict[str, Any]:
        logger.info(f"Sending message to Sally: {message}")

        payload = {"message": message}

        response = await self._api_request(url=self.base_url, method="POST", headers=self.headers, json_data=payload)
        if response.get("error") and not isinstance(response.get("error"), dict):
            logger.error(f"Sally API error: {response['error']}")
            return {"status": "error", "error": response["error"]}
        error_info = response.get("error", {})
        if isinstance(error_info, dict) and error_info.get("status"):
            logger.error(f"Sally API error: {error_info.get('message')}")
            return {"status": "error", "error": error_info.get("message", "Unknown error")}
        data = response.get("data", {})
        meta = response.get("meta", {})

        return {
            "status": "success",
            "data": {
                "message": data.get("message", ""),
                "conversation_id": meta.get("conversation_uuid"),
            },
        }

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name != "ask_health_advice":
            return {"error": f"Unsupported tool: {tool_name}"}

        message = function_args.get("message")
        if not message:
            return {"error": "Missing 'message' parameter"}

        result = await self.ask_health_advice(message)

        if errors := self._handle_error(result):
            return errors

        return result
