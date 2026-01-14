import asyncio
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

import dotenv
from loguru import logger

os.environ.clear()
dotenv.load_dotenv()

# By default, large and small models are the same
DEFAULT_MODEL_ID = "nvidia/llama-3.1-nemotron-70b-instruct"

HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")


class BaseAgent(ABC):
    """Base class defining core agent functionality and interface."""

    def __init__(self):
        self.agent_name: str = self.__class__.__name__

        self.metadata: Dict[str, Any] = {
            "name": self.agent_name,
            "version": "1.0.0",
            "author": "unknown",
            "author_address": "0x0000000000000000000000000000000000000000",
            "description": "",
            "inputs": [],
            "outputs": [],
            "external_apis": [],
            "tags": [],
            "large_model_id": DEFAULT_MODEL_ID,
            "small_model_id": DEFAULT_MODEL_ID,
            "mcp_tool_name": None,
        }
        self.heurist_base_url = HEURIST_BASE_URL
        self.heurist_api_key = HEURIST_API_KEY
        self._api_clients: Dict[str, Any] = {}

    @abstractmethod
    async def handle_message(
        self,
        message: str,
        message_type: str = "user_message",
        source_interface: str = None,
        chat_id: str = None,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Handle incoming messages and return (text_response, image_url, tool_result)"""
        pass

    @abstractmethod
    def register_interface(self, name: str, interface: Any) -> None:
        """Register communication interfaces"""
        pass

    @abstractmethod
    async def send_to_interface(self, target: str, message: Dict) -> bool:
        """Send messages to registered interfaces"""
        pass

    async def call_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point that handles the message flow with hooks."""
        task_id = params.get("task_id")

        try:
            # Pre-process params through hook
            modified_params = await self._before_handle_message(params)
            input_params = modified_params or params

            # Process message through main handler
            handler_response = await self.handle_message(input_params)

            # Post-process response through hook
            modified_response = await self._after_handle_message(handler_response)
            return modified_response or handler_response

        except Exception as e:
            logger.error(f"Task failed | Agent: {self.agent_name} | Task: {task_id} | Error: {str(e)}")
            raise

    async def _before_handle_message(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Hook called before message handling. Return modified params or None"""
        return None

    async def _after_handle_message(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Hook called after message handling. Return modified response or None"""
        return None

    def set_heurist_api_key(self, api_key: str) -> None:
        self.heurist_api_key = api_key

    async def cleanup(self):
        """Cleanup API clients"""
        for client in self._api_clients.values():
            await client.close()
        self._api_clients.clear()

    def __del__(self):
        """Destructor to ensure cleanup of resources"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.cleanup())
            else:
                loop.run_until_complete(self.cleanup())
        except Exception as e:
            logger.error(f"Cleanup failed | Agent: {self.agent_name} | Error: {str(e)}")

    # Utility methods that can be overridden
    async def pre_process(self, message: str, **kwargs) -> bool:
        """Pre-process and validate incoming messages"""
        return True

    async def post_process(self, response: Any, **kwargs) -> str:
        """Post-process agent responses"""
        return response if isinstance(response, str) else str(response)
