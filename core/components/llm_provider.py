import json
import logging
import os
from typing import Dict, List, Optional, Tuple

# Import your LLM functions
from ..llm import LLMError, call_llm, call_llm_with_tools

logger = logging.getLogger(__name__)


class LLMProvider:
    """Handles interactions with LLM services"""

    def __init__(
        self,
        base_url: str = None,
        api_key: str = None,
        large_model_id: str = None,
        small_model_id: str = None,
        tool_manager=None,
    ):
        self.base_url = base_url or os.getenv("HEURIST_BASE_URL")
        self.api_key = api_key or os.getenv("HEURIST_API_KEY")
        self.large_model_id = large_model_id or os.getenv("LARGE_MODEL_ID")
        self.small_model_id = small_model_id or os.getenv("SMALL_MODEL_ID")
        self.tool_manager = tool_manager

    async def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None,
        model_id: str = None,
        skip_tools: bool = True,
        tools: List[Dict] = None,
        tool_choice: str = "auto",
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Make a call to the LLM and process the response"""
        try:
            # Determine which model to use
            use_model = model_id or self.large_model_id
            if not skip_tools and tools:
                response = call_llm_with_tools(
                    base_url=self.base_url,
                    api_key=self.api_key,
                    model_id=use_model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    tools=tools,
                    tool_choice=tool_choice,
                )
            else:
                response = call_llm(
                    base_url=self.base_url,
                    api_key=self.api_key,
                    model_id=use_model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            # Process response
            text_response = ""
            image_url = None
            tool_back = None
            # Extract text response and tool calls
            if isinstance(response, dict):
                # Handle tool calls first if present
                if "tool_calls" in response and response["tool_calls"]:
                    print(f"Tool calls: {response['tool_calls']}")
                    tool_call = response["tool_calls"]
                    args = json.loads(tool_call.function.arguments)
                    tool_name = tool_call.function.name

                    available_tools = [t["function"]["name"] for t in tools] if tools else []
                    if tool_name in available_tools:
                        logger.info(f"Executing tool {tool_name} with args {args}")
                        tool_result = await self.tool_manager.execute_tool(tool_name, args, None)
                        if tool_result:
                            if "image_url" in tool_result:
                                image_url = tool_result["image_url"]
                            if "result" in tool_result:
                                text_response += f"\n{tool_result['result']}"
                            if "tool_call" in tool_result:
                                tool_back = tool_result["tool_call"]
                    else:
                        logger.info(f"Tool {tool_name} not found in tools config")
                        tool_back = json.dumps({"tool_call": tool_name, "processed": False, "args": args}, default=str)

                # Then handle content/text response
                if "content" in response and response["content"]:
                    text_response = (
                        response["content"].strip('"')
                        if isinstance(response["content"], str)
                        else str(response["content"])
                    )

                # Handle any image URLs in the response
                if "image_url" in response:
                    image_url = response["image_url"]
            else:
                # Handle case where response is a string
                text_response = str(response).strip('"')

            return text_response, image_url, tool_back

        except LLMError as e:
            logger.error(f"LLM call failed: {str(e)}")
            return f"LLM processing failed: {str(e)}", None, None
        except Exception as e:
            logger.error(f"Unexpected error in LLM call: {str(e)}")
            return "Sorry, something went wrong.", None, None

    def call_with_tools(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None,
        tools: List[Dict] = None,
        tool_choice: str = "auto",
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Specialized method for tool-based calls"""
        return self.call(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            skip_tools=False,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )

    def classify_text(self, text: str, classification_prompt: str) -> str:
        """Classify text using the small model"""
        try:
            text_response, _, _ = self.call(
                system_prompt=classification_prompt, user_prompt=text, temperature=0.3, model_id=self.small_model_id
            )
            return text_response.strip().upper()

        except Exception as e:
            logger.error(f"Text classification failed: {str(e)}")
            return "UNKNOWN"
