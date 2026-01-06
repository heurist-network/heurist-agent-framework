import json
import logging
import os
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple, Union

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

DEFAULT_MODEL_ID = "gemini-2.5-flash"


class GeminiError(Exception):
    pass


def _get_api_key(api_key: Optional[str]) -> str:
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiError("GEMINI_API_KEY is required for Gemini calls")
    return key


def _messages_to_system_and_contents(
    messages: List[Dict[str, Any]],
) -> Tuple[Optional[str], List[types.Content]]:
    """
    Convert OpenAI-ish messages into:
      - system_instruction (string)
      - contents (list[types.Content] with role user/model)
    """
    system_chunks: List[str] = []
    contents: List[types.Content] = []

    for message in messages:
        role = (message.get("role") or "user").lower()
        text = message.get("content") or ""

        if role == "system":
            if text.strip():
                system_chunks.append(text.strip())
            continue

        gem_role = "model" if role in ("assistant", "model") else "user"
        contents.append(types.Content(role=gem_role, parts=[types.Part(text=text)]))

    system_instruction = "\n\n".join(system_chunks).strip() or None
    return system_instruction, contents


def _build_generate_config(
    *,
    temperature: float,
    max_tokens: Optional[int],
    system_instruction: Optional[str] = None,
    tools: Optional[List[types.Tool]] = None,
    tool_config: Optional[types.ToolConfig] = None,
) -> types.GenerateContentConfig:
    config: Dict[str, Any] = {"temperature": temperature}

    if max_tokens is not None:
        config["max_output_tokens"] = max_tokens

    if system_instruction:
        config["system_instruction"] = system_instruction

    if tools:
        config["tools"] = tools
    if tool_config:
        config["tool_config"] = tool_config

    return types.GenerateContentConfig(**config)


def _convert_openai_tools_to_gemini(tools: Optional[List[Dict[str, Any]]]) -> Optional[List[types.Tool]]:
    if not tools:
        return None

    declarations: List[Dict[str, Any]] = []

    for tool in tools:
        if tool.get("type") == "function" and isinstance(tool.get("function"), dict):
            declarations.append(tool["function"])
            continue

        if isinstance(tool.get("function"), dict):
            declarations.append(tool["function"])
            continue

        if isinstance(tool.get("function_declarations"), list):
            declarations.extend(tool["function_declarations"])
            continue

        if isinstance(tool.get("functionDeclarations"), list):
            declarations.extend(tool["functionDeclarations"])
            continue

        if isinstance(tool, dict) and "name" in tool and "parameters" in tool:
            declarations.append(tool)
            continue

        raise GeminiError(f"Unsupported tool format: {tool!r}")

    return [types.Tool(function_declarations=declarations)]


def _convert_tool_choice_to_tool_config(
    tool_choice: Union[str, Dict[str, Any], None],
) -> Optional[types.ToolConfig]:
    if tool_choice is None or tool_choice == "auto":
        return types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode="AUTO"))

    if isinstance(tool_choice, str):
        choice = tool_choice.lower()
        if choice == "none":
            return types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode="NONE"))
        if choice in ("any", "required", "force"):
            return types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode="ANY"))
        raise GeminiError(f"Unknown tool_choice: {tool_choice}")

    if isinstance(tool_choice, dict):
        name = None
        if tool_choice.get("type") == "function":
            name = (tool_choice.get("function") or {}).get("name")
        name = name or tool_choice.get("name")

        if not name:
            raise GeminiError(f"Unsupported tool_choice dict: {tool_choice}")

        return types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="ANY",
                allowed_function_names=[name],
            )
        )

    raise GeminiError(f"Unsupported tool_choice type: {type(tool_choice)}")


def _extract_text(response: Any) -> str:
    text = getattr(response, "text", None)
    return text or ""


def _extract_function_calls(response: Any) -> List[Any]:
    calls = getattr(response, "function_calls", None)
    if calls:
        return list(calls)

    out: List[Any] = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            function_call = getattr(part, "function_call", None)
            if function_call:
                out.append(function_call)
    return out


async def call_gemini_async(
    api_key: str = None,
    model_id: str = None,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> str:
    key = _get_api_key(api_key)
    client = genai.Client(api_key=key)

    if messages is not None:
        system_instruction, contents = _messages_to_system_and_contents(messages)
    else:
        system_instruction = system_prompt.strip() if system_prompt else None
        contents = [types.Content(role="user", parts=[types.Part(text=user_prompt or "")])]

    config = _build_generate_config(
        temperature=temperature,
        max_tokens=max_tokens,
        system_instruction=system_instruction,
    )

    response = await client.aio.models.generate_content(
        model=model_id or DEFAULT_MODEL_ID,
        contents=contents,
        config=config,
    )

    text = _extract_text(response)
    if not text:
        raise GeminiError("Empty response from Gemini")
    return text


async def call_gemini_with_tools_async(
    api_key: str = None,
    model_id: str = None,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Union[str, Dict[str, Any], None] = "auto",
) -> Dict[str, Any]:
    key = _get_api_key(api_key)
    client = genai.Client(api_key=key)

    if messages is not None:
        system_instruction, contents = _messages_to_system_and_contents(messages)
    else:
        system_instruction = system_prompt.strip() if system_prompt else None
        contents = [types.Content(role="user", parts=[types.Part(text=user_prompt or "")])]

    gemini_tools = _convert_openai_tools_to_gemini(tools)
    tool_config = _convert_tool_choice_to_tool_config(tool_choice) if gemini_tools else None

    config = _build_generate_config(
        temperature=temperature,
        max_tokens=max_tokens,
        system_instruction=system_instruction,
        tools=gemini_tools,
        tool_config=tool_config,
    )

    response = await client.aio.models.generate_content(
        model=model_id or DEFAULT_MODEL_ID,
        contents=contents,
        config=config,
    )

    function_calls = _extract_function_calls(response)
    if function_calls:
        function_call = function_calls[0]
        function_obj = SimpleNamespace(
            name=function_call.name,
            arguments=json.dumps(getattr(function_call, "args", {}) or {}),
        )
        return {"tool_calls": SimpleNamespace(id="gemini-tool-call", function=function_obj), "content": ""}

    return {"content": _extract_text(response)}


class GeminiProvider:
    def __init__(self, api_key: str = None, model_id: str = None):
        self.api_key = api_key
        self.model_id = model_id or DEFAULT_MODEL_ID
        self.large_model_id = self.model_id
        self.small_model_id = self.model_id

    async def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model_id: str = None,
        skip_tools: bool = True,
        tools: List[Dict[str, Any]] = None,
        tool_choice: Union[str, Dict[str, Any], None] = "auto",
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        use_model = model_id or self.model_id

        if not skip_tools and tools:
            response = await call_gemini_with_tools_async(
                api_key=self.api_key,
                model_id=use_model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response.get("content", ""), None, response.get("tool_calls")

        text = await call_gemini_async(
            api_key=self.api_key,
            model_id=use_model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return text, None, None

    async def call_with_tools(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: List[Dict[str, Any]] = None,
        tool_choice: Union[str, Dict[str, Any], None] = "auto",
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        return await self.call(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            skip_tools=False,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )
