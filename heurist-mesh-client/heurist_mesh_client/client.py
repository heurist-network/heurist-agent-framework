import os
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel


class MeshTaskResponse(BaseModel):
    task_id: str
    msg: str


class ReasoningStep(BaseModel):
    timestamp: int
    content: str
    is_sent: bool


class TaskResult(BaseModel):
    response: Any
    success: bool
    data: Optional[Dict[str, Any]] = None

    def model_dump(self) -> Dict[str, Any]:
        data = super().model_dump()
        if isinstance(data["success"], str):
            data["success"] = data["success"].lower() == "true"
        return data


class MeshTaskQueryResponse(BaseModel):
    status: str
    reasoning_steps: Optional[List[ReasoningStep]] = None
    result: Optional[Union[TaskResult, Dict[str, Any]]] = None

    def model_dump(self) -> Dict[str, Any]:
        data = super().model_dump()
        if data.get("result") and isinstance(data["result"], dict):
            data["result"] = TaskResult(**data["result"]).model_dump()
        return data


class MeshClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = os.getenv("MESH_SERVER_URL", "https://mesh.heurist.xyz"),
        timeout: int = 90,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("HEURIST_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through constructor or HEURIST_API_KEY environment variable"
            )
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)

    def _prepare_payload(self, **kwargs: Any) -> Dict[str, Any]:
        """Prepare request payload with API key."""
        return {"api_key": self.api_key, **kwargs}

    def _prepare_input(
        self,
        query: Optional[str] = None,
        tool: Optional[str] = None,
        tool_arguments: Optional[Dict[str, Any]] = None,
        raw_data_only: bool = False,
    ) -> Dict[str, Any]:
        """Prepare input data for both sync and async requests."""
        if not query and not tool:
            raise ValueError("Either query or tool must be provided")

        input_data = {"raw_data_only": raw_data_only}
        if query:
            input_data["query"] = query
        if tool:
            input_data["tool"] = tool
        if tool_arguments:
            input_data["tool_arguments"] = tool_arguments
        return input_data

    def create_task(
        self,
        agent_id: str,
        query: Optional[str] = None,
        tool: Optional[str] = None,
        tool_arguments: Optional[Dict[str, Any]] = None,
        raw_data_only: bool = False,
        agent_type: str = "AGENT",
    ) -> MeshTaskResponse:
        """Create a new asynchronous task."""
        input_data = self._prepare_input(query, tool, tool_arguments, raw_data_only)
        payload = self._prepare_payload(
            agent_id=agent_id,
            agent_type=agent_type,
            task_details=input_data,
        )

        response = self.client.post(f"{self.base_url}/mesh_task_create", json=payload)
        response.raise_for_status()
        return MeshTaskResponse(**response.json())

    def query_task(self, task_id: str) -> MeshTaskQueryResponse:
        """Query the status and result of an asynchronous task."""
        payload = self._prepare_payload(task_id=task_id)

        response = self.client.post(f"{self.base_url}/mesh_task_query", json=payload)
        response.raise_for_status()
        return MeshTaskQueryResponse(**response.json())

    def sync_request(
        self,
        agent_id: str,
        query: Optional[str] = None,
        tool: Optional[str] = None,
        tool_arguments: Optional[Dict[str, Any]] = None,
        raw_data_only: bool = False,
    ) -> Dict[str, Any]:
        """Make a synchronous request to an agent."""
        input_data = self._prepare_input(query, tool, tool_arguments, raw_data_only)
        payload = self._prepare_payload(agent_id=agent_id, input=input_data)

        response = self.client.post(f"{self.base_url}/mesh_request", json=payload)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self) -> "MeshClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
