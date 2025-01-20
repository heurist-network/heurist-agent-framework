import requests
import json
import time
import os
import logging
from openai import OpenAI, AsyncOpenAI
from typing import Dict, List, Union
import requests
from types import SimpleNamespace
import re
import asyncio
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMError(Exception):
    """Custom exception for LLM-related errors"""
    pass

def call_llm(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int = 500,
    max_retries: int = 3,
    initial_retry_delay: int = 1
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
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    retry_delay = initial_retry_delay
    
    for attempt in range(max_retries):
        try:
            result = client.chat.completions.create(
                model=model_id,
                messages=messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return result.choices[0].message.content
        
        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.warning(f"Response parsing failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
        except Exception as e:
            logger.warning(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
        
        # Wait before next retry if there are attempts left
        if attempt < max_retries - 1:
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
    
    # Raise error if all attempts fail
    raise LLMError("All retry attempts failed")


def call_llm_with_tools(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int = None,
    max_retries: int = 3,
    tools: List[Dict] = None,
    tool_choice: str = "auto"
) -> Union[str, Dict]:
    client = OpenAI(base_url=base_url, api_key=api_key)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice if tools else None,
            max_tokens=max_tokens
        )

        message = response.choices[0].message

        # If there are tool calls, return both tool calls and content
        if hasattr(message, 'tool_calls') and message.tool_calls:
            return {
                'tool_calls': message.tool_calls[0],
                'content': message.content
            }
        if hasattr(message, 'content') and message.content:
            text_response = message.content
            #text_response = '<function=handle_image_generation>{"prompt": "a cat", "agent_context": "None"} </function>'
            tool_calls = extract_function_calls_to_tool_calls(text_response)
            if tool_calls:
                logger.info("found tool calls in response")
                return {
                    'tool_calls': tool_calls,
                    'content': ""
                }
            else:
                return {
                    'content': text_response
                }
        # Otherwise return just the content
        return message

    except Exception as e:
        raise LLMError(f"LLM API call failed: {str(e)}")
    
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
        

        function_obj = SimpleNamespace(
            name=function_name,
            arguments=json.dumps(parsed_args)
        )
        # Build the structure that your existing code expects
        return SimpleNamespace(function=function_obj)
    
    # If no matches, return an empty dict or whatever fallback you need
    return None

async def call_llm_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int = 500,
    max_retries: int = 3,
    initial_retry_delay: int = 1
) -> str:
    """Async version of call_llm"""
    
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    retry_delay = initial_retry_delay
    
    for attempt in range(max_retries):
        try:
            result = await client.chat.completions.create(
                model=model_id,
                messages=messages,
                stream=False,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return result.choices[0].message.content
        
        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.warning(f"Response parsing failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
        except Exception as e:
            logger.warning(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
        
        if attempt < max_retries - 1:
            logger.info(f"Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2
    
    raise LLMError("All retry attempts failed")

async def call_llm_with_tools_async(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int = 500,
    max_retries: int = 3,
    tools: List[Dict] = None
) -> Union[str, Dict]:
    """Async version of call_llm_with_tools"""
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = await client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if hasattr(message, 'tool_calls') and message.tool_calls:
            return {
                'tool_calls': message.tool_calls[0],
                'content': message.content
            }
        if hasattr(message, 'content') and message.content:
            text_response = message.content
            tool_calls = extract_function_calls_to_tool_calls(text_response)
            if tool_calls:
                logger.info("found tool calls in response")
                return {
                    'tool_calls': tool_calls,
                    'content': ""
                }
            else:
                return {
                    'content': text_response
                }
        return message

    except Exception as e:
        raise LLMError(f"LLM API call failed: {str(e)}")