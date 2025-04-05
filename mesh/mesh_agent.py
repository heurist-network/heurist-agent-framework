import asyncio
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import dotenv
from loguru import logger

from clients.mesh_client import MeshClient

os.environ.clear()
dotenv.load_dotenv()

# By default, large and small models are the same
DEFAULT_MODEL_ID = "anthropic/claude-3.5-haiku"  # "nvidia/llama-3.1-nemotron-70b-instruct"

HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
# HEURIST_BASE_URL = os.getenv('OPENROUTER_BASE_URL') #os.getenv('HEURIST_BASE_URL')
# HEURIST_API_KEY = os.getenv('OPENROUTER_API_KEY')


class MeshAgent(ABC):
    """Base class for all mesh agents"""

    def __init__(self):
        self.agent_name: str = self.__class__.__name__
        self._task_id = None

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
            "hidden": False,
            "recommended": False,
            "image_url": "",
            "examples": [],
        }
        self.heurist_base_url = HEURIST_BASE_URL
        self.heurist_api_key = HEURIST_API_KEY
        self._api_clients: Dict[str, Any] = {}

        self.mesh_client = MeshClient(base_url=os.getenv("PROTOCOL_V2_SERVER_URL", "https://sequencer-v2.heurist.xyz"))
        self._api_clients["mesh"] = self.mesh_client

        self._task_id = None
        self._origin_task_id = None

    @property
    def task_id(self) -> Optional[str]:
        """Access the current task ID"""
        return self._task_id

    @abstractmethod
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming message - must be implemented by subclasses"""
        pass

    async def call_agent(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point that handles the message flow with hooks."""
        # Set task tracking IDs
        self._task_id = params.get("origin_task_id") or params.get("task_id")
        self._origin_task_id = params.get("origin_task_id")

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
            logger.error(f"Task failed | Agent: {self.agent_name} | Task: {self._task_id} | Error: {str(e)}")
            raise

    async def _before_handle_message(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Hook called before message handling. Return modified params or None"""
        thinking_msg = f"{self.agent_name} is thinking..."
        self.push_update(params, thinking_msg)
        return None

    async def _after_handle_message(self, response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Hook called after message handling. Return modified response or None"""
        return None

    def set_heurist_api_key(self, api_key: str) -> None:
        self.heurist_api_key = api_key

    def push_update(self, params: Dict[str, Any], content: str) -> None:
        """Always push to origin_task_id if available"""
        update_task_id = self._origin_task_id or self._task_id
        if update_task_id:
            logger.info(f"Pushing update | Task: {update_task_id} | Content: {content}")
            self.mesh_client.push_update(update_task_id, content)

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
