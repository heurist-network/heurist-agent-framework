import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

from mesh.mesh_agent import MeshAgent


class ContextStorage(ABC):
    """Abstract base class for context storage backends"""

    @abstractmethod
    async def get_context(self, user_id: str) -> Dict[str, Any]:
        """Get the context for a specific user"""
        pass

    @abstractmethod
    async def set_context(self, user_id: str, context: Dict[str, Any]) -> None:
        """Set the context for a specific user"""
        pass


class FileContextStorage(ContextStorage):
    def __init__(self, storage_dir: str = "./mesh/context"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Context storage initialized at {self.storage_dir.absolute()}")

    def _get_context_path(self, user_id: str) -> Path:
        """Get the file path for a specific user context"""
        sanitized_user_id = user_id.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{sanitized_user_id}.json"

    async def get_context(self, user_id: str) -> Dict[str, Any]:
        context_path = self._get_context_path(user_id)
        if not context_path.exists():
            return {}
        try:
            with open(context_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in context file {context_path}")
            return {}
        except Exception as e:
            logger.error(f"Error reading context from {context_path}: {e}")
            return {}

    async def set_context(self, user_id: str, context: Dict[str, Any]) -> None:
        context_path = self._get_context_path(user_id)
        try:
            with open(context_path, "w") as f:
                json.dump(context, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing context to {context_path}: {e}")


class ContextAgent(MeshAgent):
    """
    Base class for agents that need to maintain context for each user.

    Context is stored using a pluggable storage backend, defaulting to local file storage.
    """

    def __init__(self, storage: Optional[ContextStorage] = None):
        super().__init__()
        self.storage = storage or FileContextStorage()

    def _extract_user_id(self, api_key: str) -> Optional[str]:
        """Extract user_id from API key"""
        if not api_key:
            return None

        try:
            user_id = api_key.split("-", 1)[0]
            return user_id
        except Exception:
            logger.warning(f"Invalid API key format: {api_key}")
            return None

    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        return await self.storage.get_context(user_id)

    async def set_user_context(self, context: Dict[str, Any], user_id: str) -> None:
        await self.storage.set_context(user_id, context)

    async def update_user_context(self, updates: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        context = await self.get_user_context(user_id)
        context.update(updates)
        await self.set_user_context(context, user_id)
        return context
