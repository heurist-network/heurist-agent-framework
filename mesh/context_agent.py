import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from mesh.mesh_agent import MeshAgent

load_dotenv()

logger = logging.getLogger(__name__)


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
        sanitized_user_id = user_id.lower().replace("/", "_").replace("\\", "_")
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


class S3ContextStorage(ContextStorage):
    def __init__(self):
        self.bucket = "mesh-context"
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            endpoint_url=os.getenv("S3_ENDPOINT"),
            region_name=os.getenv("S3_REGION", "auto"),
        )
        logger.info(f"S3 context storage initialized with bucket {self.bucket}")

    def _get_key(self, user_id: str) -> str:
        sanitized_user_id = user_id.lower().replace("/", "_").replace("\\", "_")
        return f"{sanitized_user_id}.json"

    async def get_context(self, user_id: str) -> Dict[str, Any]:
        key = self._get_key(user_id)
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            return json.loads(obj["Body"].read())
        except self.s3.exceptions.NoSuchKey:
            return {}
        except ClientError as e:
            logger.error(f"Error fetching context from S3: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            return {}

    async def set_context(self, user_id: str, context: Dict[str, Any]) -> None:
        key = self._get_key(user_id)
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=json.dumps(context, indent=2).encode("utf-8"),
                ContentType="application/json",
            )
        except Exception as e:
            logger.error(f"Error writing context to S3: {e}")


class NillionContextStorage(ContextStorage):
    def __init__(self):
        self.api_key = os.getenv("CONTEXT_API_KEY")
        self.base_url = "https://yhxy0iuhih.execute-api.us-east-1.amazonaws.com/staging/nillion-context"
        if not self.api_key:
            raise ValueError("CONTEXT_API_KEY environment variable is required for Nillion storage")
        logger.info("Nillion context storage initialized")

    async def get_context(self, user_id: str) -> Dict[str, Any]:
        """Get context from Nillion API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/{user_id}"
                headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        if isinstance(data, dict) and "credentials" in data:
                            credentials = data["credentials"]
                            if isinstance(credentials, list) and len(credentials) > 0:
                                latest_credential = max(credentials, key=lambda x: x.get("_updated", ""))
                                return latest_credential.get("content", {})
                            else:
                                return {}
                        else:
                            if isinstance(data, list) and len(data) > 0:
                                return data[0].get("content", {})
                            elif isinstance(data, dict):
                                return data.get("content", {})
                            else:
                                return {}
                    elif response.status == 404:
                        return {}
                    else:
                        logger.error(
                            f"Error fetching context from Nillion: {response.status} - {await response.text()}"
                        )
                        return {}
        except Exception as e:
            logger.error(f"Error fetching context from Nillion: {e}")
            return {}

    async def set_context(self, user_id: str, context: Dict[str, Any]) -> None:
        """Set context in Nillion API"""
        try:
            # Use the exact Nillion schema format
            payload = [
                {
                    "user_id": user_id,
                    "content": context,
                }
            ]

            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/{user_id}"
                headers = {"Content-Type": "application/json", "x-api-key": self.api_key}
                async with session.put(url, headers=headers, json=payload) as response:
                    if response.status not in [200, 201]:
                        logger.error(f"Error writing context to Nillion: {response.status} - {await response.text()}")
        except Exception as e:
            logger.error(f"Error writing context to Nillion: {e}")


def _has_s3_env():
    return all(os.getenv(k) for k in ["S3_ACCESS_KEY", "S3_SECRET_KEY", "S3_ENDPOINT"])


def _has_nillion_env():
    """Check if Nillion environment variables are present"""
    return os.getenv("CONTEXT_API_KEY") is not None


class ContextAgent(MeshAgent, ABC):
    """
    Base class for agents that need to maintain context for each user.

    Context is stored using a pluggable storage backend, defaulting to local file storage.
    """

    def __init__(self, storage: Optional[ContextStorage] = None):
        super().__init__()
        if storage:
            self.storage = storage
        elif _has_nillion_env():
            self.storage = NillionContextStorage()
        elif _has_s3_env():
            self.storage = S3ContextStorage()
        else:
            self.storage = FileContextStorage()

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

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def get_tool_schemas(self) -> List[Dict]:
        pass

    @abstractmethod
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass
