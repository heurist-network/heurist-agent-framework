import asyncio
import json
import logging
import re
import time
from types import SimpleNamespace
from typing import Dict, List, Union

import requests
from openai import AsyncOpenAI, OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMError(Exception):
    """Custom exception for LLM-related errors"""

    pass


def _format_messages(system_prompt: str = None, user_prompt: str = None, messages: List[Dict] = None) -> List[Dict]:
    """Convert between different message formats while maintaining backward compatibility"""
    if messages is not None:
        return messages
    if system_prompt is not None and user_prompt is not None:
        return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    raise ValueError("Either (system_prompt, user_prompt) or messages must be provided")


def call_llm(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    max_retries: int = 3,
    initial_retry_delay: int = 1,
) -> str:
    """
    Call LLM with retry mechanism.

    Parameters:
        model_id (str): The model identifier for the LLM.
        system_prompt (str): The system prompt.
        user_prompt (str): The user input prompt.
        temperature (float): The temperature setting for response generation.
        max_tokens (int): Maximum number of tokens to generate.
        max_retries (int): Number of retry attempts on failure.
        initial_retry_delay (int): Initial delay between retries, with exponential backoff.

    Returns:
        str: Generated text from LLM.

    Raises:
        LLMError: If all retry attempts fail.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    retry_delay = initial_retry_delay

    for attempt in range(max_retries):
        try:
            result = client.chat.completions.create(
                model=model_id,
                messages=formatted_messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return _handle_tool_response(result.choices[0].message)

        except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError, Exception) as e:
            logger.warning(f"{type(e).__name__} (attempt {attempt + 1}/{max_retries}): {str(e)}")

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2

    raise LLMError("All retry attempts failed")


def call_llm_with_tools(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = None,
    max_retries: int = 3,
    tools: List[Dict] = None,
    tool_choice: str = "auto",
) -> Union[str, Dict]:
    client = OpenAI(base_url=base_url, api_key=api_key)
    formatted_messages = _format_messages(system_prompt, user_prompt, messages)

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice if tools else None,
            max_tokens=max_tokens,
        )
        return _handle_tool_response(response.choices[0].message)

    except Exception as e:
        raise LLMError(f"LLM API call failed: {str(e)}")


async def call_llm_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 25000,
    max_retries: int = 3,
    initial_retry_delay: int = 1,
) -> str:
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    retry_delay = initial_retry_delay

    for attempt in range(max_retries):
        try:
            result = await client.chat.completions.create(
                model=model_id,
                messages=formatted_messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return result.choices[0].message.content

        except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError, Exception) as e:
            logger.warning(f"{type(e).__name__} (attempt {attempt + 1}/{max_retries}): {str(e)}")

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2

    raise LLMError("All retry attempts failed")


async def call_llm_with_tools_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    max_retries: int = 3,
    tools: List[Dict] = None,
    tool_choice: str = "auto",
) -> Union[str, Dict]:
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    formatted_messages = _format_messages(system_prompt, user_prompt, messages)

    try:
        response = await client.chat.completions.create(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice if tools else None,
            max_tokens=max_tokens,
        )
        return _handle_tool_response(response.choices[0].message)

    except Exception as e:
        raise LLMError(f"LLM API call failed: {str(e)}")


# ---------------------------------------------------------------------------
# LiteLLM gateway path
#
# Same call-site contract as call_llm / call_llm_with_tools but routes through
# the LiteLLM SDK (`litellm.completion` / `litellm.acompletion`) so a single
# LLMProvider can talk to OpenAI, Anthropic, Vertex AI, Bedrock, Azure, Groq,
# Mistral, Ollama, and 90+ other backends. The model is selected via the
# standard LiteLLM provider-prefixed name ("anthropic/claude-...", "azure/...",
# "vertex_ai/...", etc.) and credentials are resolved either from the api_key
# / base_url passed here or from provider-specific env vars (ANTHROPIC_API_KEY,
# OPENAI_API_KEY, AWS_*, AZURE_*, ...).
#
# `drop_params=True` is enabled by default so kwargs that some providers reject
# (frequency_penalty / presence_penalty on Anthropic, Gemini, Bedrock; etc.)
# are silently dropped instead of raising UnsupportedParamsError.
# ---------------------------------------------------------------------------


def _litellm_kwargs(api_key, base_url, max_retries, extra):
    kwargs = {"drop_params": True}
    if max_retries is not None:
        kwargs["num_retries"] = max_retries
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["api_base"] = base_url
    if extra:
        kwargs.update(extra)
    return kwargs


def call_llm_litellm(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    max_retries: int = 3,
    litellm_kwargs: Dict = None,
):
    import litellm

    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    kwargs = _litellm_kwargs(api_key, base_url, max_retries, litellm_kwargs)

    try:
        result = litellm.completion(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return _handle_tool_response(result.choices[0].message)
    except Exception as e:
        raise LLMError(f"LiteLLM API call failed: {str(e)}")


def call_llm_with_tools_litellm(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = None,
    max_retries: int = 3,
    tools: List[Dict] = None,
    tool_choice: str = "auto",
    litellm_kwargs: Dict = None,
) -> Union[str, Dict]:
    import litellm

    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    kwargs = _litellm_kwargs(api_key, base_url, max_retries, litellm_kwargs)

    try:
        response = litellm.completion(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice if tools else None,
            **kwargs,
        )
        return _handle_tool_response(response.choices[0].message)
    except Exception as e:
        raise LLMError(f"LiteLLM API call failed: {str(e)}")


async def call_llm_litellm_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 25000,
    max_retries: int = 3,
    litellm_kwargs: Dict = None,
) -> str:
    import litellm

    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    kwargs = _litellm_kwargs(api_key, base_url, max_retries, litellm_kwargs)

    try:
        result = await litellm.acompletion(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return result.choices[0].message.content
    except Exception as e:
        raise LLMError(f"LiteLLM API call failed: {str(e)}")


async def call_llm_with_tools_litellm_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str = None,
    user_prompt: str = None,
    messages: List[Dict] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    max_retries: int = 3,
    tools: List[Dict] = None,
    tool_choice: str = "auto",
    litellm_kwargs: Dict = None,
) -> Union[str, Dict]:
    import litellm

    formatted_messages = _format_messages(system_prompt, user_prompt, messages)
    kwargs = _litellm_kwargs(api_key, base_url, max_retries, litellm_kwargs)

    try:
        response = await litellm.acompletion(
            model=model_id,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice if tools else None,
            **kwargs,
        )
        return _handle_tool_response(response.choices[0].message)
    except Exception as e:
        raise LLMError(f"LiteLLM API call failed: {str(e)}")


def extract_function_calls_to_tool_calls(llm_text: str) -> SimpleNamespace:
    """
    Scan the LLM's text output for a <function=NAME>{...}</function> pattern,
    and convert to appropriate format for tool calls
    """
    pattern = r"<function=([^>]+)>(.*?)(?:</function>|<function>|<function/>|></function>)"
    matches = re.findall(pattern, llm_text)

    # If we find at least one match
    if matches:
        function_name, args_json_str = matches[0]  # Just take the first match
        # Parse the JSON to ensure it's valid
        parsed_args = json.loads(args_json_str.strip())

        function_obj = SimpleNamespace(name=function_name, arguments=json.dumps(parsed_args))
        # Build the structure that your existing code expects
        return SimpleNamespace(function=function_obj)

    # If no matches, return an empty dict or whatever fallback you need
    return None


def _handle_tool_response(message):
    if hasattr(message, "tool_calls") and message.tool_calls:
        return {"tool_calls": message.tool_calls[0], "content": message.content}
    if hasattr(message, "content") and message.content:
        text_response = message.content
        tool_calls = extract_function_calls_to_tool_calls(text_response)
        if tool_calls:
            logger.info("found tool calls in response")
            return {"tool_calls": tool_calls, "content": ""}
        else:
            return {"content": text_response}
    return message
