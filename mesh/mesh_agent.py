import asyncio
import json
import os
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any, Dict, List, Optional

import aiohttp
import dotenv
from loguru import logger

from clients.mesh_client import MeshClient
from core.llm import call_llm_async, call_llm_with_tools_async
from decorators import monitor_execution, with_cache, with_retry

os.environ.clear()
dotenv.load_dotenv()

# By default, large and small models are the same
DEFAULT_MODEL_ID = "nvidia/llama-3.1-nemotron-70b-instruct"

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
            "inputs": [
                {
                    "name": "query",
                    "description": "Natural language query to the agent",
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
                    "description": "The text response from the agent",
                    "type": "str",
                },
                # fmt: off
                {
                    "name": "data",
                    "description": "Structured data from the agent",
                    "type": "dict",
                },
                # fmt: on
            ],
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
        self.session = None

    @property
    def task_id(self) -> Optional[str]:
        """Access the current task ID"""
        return self._task_id

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for the agent"""
        pass

    @abstractmethod
    def get_tool_schemas(self) -> List[Dict]:
        """Return the tool schemas for the agent"""
        pass

    @abstractmethod
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and return the raw data"""
        pass

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standard message handling flow, supporting both direct tool calls and natural language queries.

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
        session_context = params.get("session_context", {})

        # ---------------------
        # 1) DIRECT TOOL CALL
        # ---------------------
        if tool_name:
            data = await self._execute_tool_with_policy(
                tool_name=tool_name, function_args=tool_args, session_context=session_context, original_params=params
            )
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

            data = await self._execute_tool_with_policy(
                tool_name=tool_call_name,
                function_args=tool_call_args,
                session_context=session_context,
                original_params=params,
            )

            # If the tool returned an error (including timeout-as-error), do not attempt LLM
            if isinstance(data, dict) and ("error" in data or data.get("status") == "error"):
                return {"response": "", "data": data}

            if raw_data_only:
                return {"response": "", "data": data}

            if (
                hasattr(self.__class__, "_respond_with_llm")
                and self.__class__._respond_with_llm is not MeshAgent._respond_with_llm
            ):
                try:
                    explanation = await self._respond_with_llm(
                        query=query,
                        tool_call_id=tool_call.id,
                        data=data,
                        temperature=0.7,
                    )
                except TypeError:
                    try:
                        explanation = await self._respond_with_llm(
                            model_id=self.metadata["large_model_id"],
                            system_prompt=self.get_system_prompt(),
                            query=query,
                            tool_call_id=tool_call.id,
                            data=data,
                            temperature=0.7,
                        )
                    except Exception as e2:
                        logger.error(f"Error calling custom _respond_with_llm: {str(e2)}")
                        explanation = f"Failed to generate response: {str(e2)}"
                except Exception as e:
                    logger.error(f"Error calling custom _respond_with_llm: {str(e)}")
                    explanation = f"Failed to generate response: {str(e)}"
            else:
                explanation = await self._respond_with_llm(
                    model_id=self.metadata["large_model_id"],
                    system_prompt=self.get_system_prompt(),
                    query=query,
                    tool_call_id=tool_call.id,
                    data=data,
                    temperature=0.7,
                )

            return {"response": explanation, "data": data}

        # ---------------------
        # 3) NEITHER query NOR tool
        # ---------------------
        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}

    # ---------------------
    # Timeout/Fallback policy hooks (overridable by agents)
    # ---------------------
    def get_default_timeout_seconds(self) -> Optional[int]:
        """Default timeout in seconds for tool execution. None means no timeout."""
        return None

    def get_tool_timeout_seconds(self) -> Dict[str, int]:
        """Per-tool timeout overrides in seconds. Keyed by tool name."""
        return {}

    async def get_fallback_for_tool(
        self, tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Return a fallback spec dict or None. The spec should be of the form:
        {
            "module": "mesh.agents.some_agent_module",
            "class": "SomeAgentClass",
            "input": {  # input dict for the fallback agent
                # one of: 'query' or 'tool' + 'tool_arguments', plus optional flags
                ...
            },
        }
        """
        return None

    async def _execute_tool_with_policy(
        self,
        tool_name: str,
        function_args: Dict[str, Any],
        session_context: Optional[Dict[str, Any]],
        original_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run tool logic with timeout and fallback policy."""
        # Resolve timeout
        tool_timeouts = self.get_tool_timeout_seconds() or {}
        timeout_seconds = tool_timeouts.get(tool_name, self.get_default_timeout_seconds())

        async def _run_tool():
            return await self._handle_tool_logic(
                tool_name=tool_name, function_args=function_args, session_context=session_context
            )

        try:
            if timeout_seconds:
                return await asyncio.wait_for(_run_tool(), timeout=timeout_seconds)
            return await _run_tool()
        except asyncio.TimeoutError:
            logger.warning(
                f"Tool '{tool_name}' timed out after {timeout_seconds}s in agent '{self.agent_name}'. Attempting fallback."
            )
            fallback_spec = await self.get_fallback_for_tool(tool_name, function_args, original_params)
            if not fallback_spec:
                # Return explicit timeout error payload if no fallback provided
                return {
                    "status": "error",
                    "error": f"Tool '{tool_name}' timed out after {timeout_seconds}s",
                }
            return await self._invoke_fallback_agent(fallback_spec, session_context, original_params)

    async def _invoke_fallback_agent(
        self, fallback_spec: Dict[str, Any], session_context: Optional[Dict[str, Any]], original_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Instantiate and call a fallback agent locally with provided input."""
        module_name = fallback_spec.get("module")
        class_name = fallback_spec.get("class")
        input_payload = dict(fallback_spec.get("input", {}))

        if not module_name or not class_name:
            raise ValueError("Fallback spec must include 'module' and 'class'")

        # Preserve origin/task id and session context
        if original_params.get("origin_task_id"):
            input_payload.setdefault("origin_task_id", original_params.get("origin_task_id"))
        if original_params.get("task_id") and not input_payload.get("origin_task_id"):
            input_payload.setdefault("origin_task_id", original_params.get("task_id"))

        input_payload.setdefault("session_context", {})
        if session_context:
            input_payload["session_context"].update(session_context)

        # Preserve selected top-level flags from original params
        if "raw_data_only" in original_params and "raw_data_only" not in input_payload:
            input_payload["raw_data_only"] = original_params["raw_data_only"]

        mod = import_module(module_name)
        agent_cls = getattr(mod, class_name)
        agent_instance = agent_cls()
        if self.heurist_api_key:
            agent_instance.set_heurist_api_key(self.heurist_api_key)

        result = await agent_instance.call_agent(input_payload)

        # Annotate fallback in result
        if isinstance(result, dict):
            result.setdefault("data", {})
            if isinstance(result["data"], dict):
                result["data"].setdefault("fallback", {})
                result["data"]["fallback"].update(
                    {"from_agent": self.agent_name, "to_agent": class_name, "reason": "timeout"}
                )
        return result

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

    def _handle_error(self, maybe_error: dict) -> dict:
        """
        Small helper to return the error if present in
        a dictionary with the 'error' key.
        """
        if "error" in maybe_error:
            return {"error": maybe_error["error"]}
        return {}

    async def _respond_with_llm(
        self, model_id: str, system_prompt: str, query: str, tool_call_id: str, data: dict, temperature: float
    ) -> str:
        """
        Reusable helper to ask the LLM to generate a user-friendly explanation
        given a piece of data from a tool call.
        """
        return await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
                # {
                #     "role": "assistant",
                #     "content": None,
                #     "tool_calls": [
                #         {
                #             "id": tool_call_id,
                #             "type": "function",
                #             "function": {"name": tool_name, "arguments": json.dumps(tool_args)},
                #         }
                #     ],
                # },
                {"role": "tool", "content": str(data), "tool_call_id": tool_call_id},
            ],
            temperature=temperature,
        )

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None
        await self.cleanup()

    async def cleanup(self):
        """Cleanup API clients and session"""
        for client in self._api_clients.values():
            if hasattr(client, "close"):
                await client.close()
        self._api_clients.clear()

        if self.session:
            await self.session.close()
            self.session = None

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

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    @monitor_execution()
    async def _api_request(
        self, url: str, method: str = "GET", headers: Dict = None, params: Dict = None, json_data: Dict = None
    ) -> Dict:
        """
        Generic API request method that can be used by child classes.
        This consolidates the common API request pattern found in all agents.

        Args:
            url: The API endpoint URL
            method: HTTP method (GET, POST, etc.)
            headers: HTTP headers
            params: URL parameters
            json_data: JSON payload for POST/PUT requests

        Returns:
            Dict with response data or error
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
            should_close = True
        else:
            should_close = False

        try:
            if method.upper() == "GET":
                async with self.session.get(url, headers=headers, params=params) as response:
                    if response.status == 429:
                        logger.warning(f"Rate limit exceeded for {url}. Retrying after 5 seconds...")
                        await asyncio.sleep(5)
                        async with self.session.get(url, headers=headers, params=params) as retry_response:
                            retry_response.raise_for_status()
                            logger.info(f"Request to {url} succeeded after 429 retry")
                            return await retry_response.json()
                    response.raise_for_status()
                    return await response.json()
            elif method.upper() == "POST":
                async with self.session.post(url, headers=headers, params=params, json=json_data) as response:
                    if response.status == 429:
                        logger.warning(f"Rate limit exceeded for {url}. Retrying after 5 seconds...")
                        await asyncio.sleep(5)
                        async with self.session.post(
                            url, headers=headers, params=params, json=json_data
                        ) as retry_response:
                            retry_response.raise_for_status()
                            logger.info(f"Request to {url} succeeded after 429 retry")
                            return await retry_response.json()
                    response.raise_for_status()
                    return await response.json()

        except Exception as e:
            logger.error(f"API request error: {e}")
            return {"error": f"API request failed: {str(e)}"}
        finally:
            if should_close and self.session:
                await self.session.close()
                self.session = None
