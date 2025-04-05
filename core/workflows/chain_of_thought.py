import asyncio
import json
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ChainOfThoughtReasoning:
    """Chain of thought reasoning pattern"""

    def __init__(self, llm_provider, tool_manager, augmented_llm):
        self.llm_provider = llm_provider
        self.tool_manager = tool_manager
        self.augmented_llm = augmented_llm

    async def process(
        self, message: str, personality_provider=None, chat_id: str = None, workflow_options: Dict = None, **kwargs
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Process with chain of thought reasoning"""

        # Set default options
        options = {
            "temperature": 0.7,
            "planning_temperature": 0.1,
            "execution_temperature": 0.7,
            "final_temperature": 0.7,
            "use_conversation": False,
            "use_knowledge": False,
            "use_similar": False,
            "store_interaction": False,
        }
        # Override with provided options
        if workflow_options:
            options.update(workflow_options)

        # Format user info
        user = kwargs.get("user", "User")
        display_name = kwargs.get("display_name", user)
        message_data = message
        message_info = f"User: {display_name}, Username: {user}, \nMessage: {message_data}"

        image_url_final = None
        steps_responses = []

        try:
            # Planning phase
            planning_prompt = f"""
            <MAIN_INSTRUCTION>
            You are a helpful assistant that can analyze the question/message or request and give me a list of steps with the tools you'd use in each step, if the step is not a specific tool you have to use, just put the tool name as "None", DO NOT ANSWER THE USER MESSAGE FOLLOW THE SYSTEM PROMPT INSTRUCTIONS.
            </MAIN_INSTRUCTION>
            <SYSTEM_PROMPT> I want you to give analyze the question/message or request {message_info}. Make sure you follow the following rules to answer the inital request.
                    IMPORTANT: DON'T USE TOOLS RIGHT NOW. ANALYZE AND Give me a list of steps with the tools you'd use in each step, if the step is not a specific tool you have to use, just put the tool name as "None".
                    The most important thing to tell me is what different calls you'd do or processes as a list. Your answer should be a valid JSON and ONLY the JSON.
                    Make sure you analyze what outputs from previous steps you'd need to use in the next step if applicable.
                    IMPORTANT: RETURN THE JSON ONLY.
                    IMPORTANT: DO NOT USE TOOLS.
                    IMPORTANT: ONLY USE VALID TOOLS.
                    IMPORTANT: WHEN STEPS DEPEND ON EACH OTHER, MAKE SURE YOU ANALYZE THE INPUTS SO YOU KNOW WHAT TO PASS TO THE NEXT TOOL CALL. IF NEEDED TAKE A STEP TO MAKE SURE YOU KNOW WHAT TO PASS TO THE NEXT TOOL CALL AND FORMAT THE INPUTS CORRECTLY.
                    IMPORTANT: FOR NEXT TOOL CALLS MAKE SURE YOU ANALYZE THE INPUTS SO YOU KNOW WHAT TO PASS TO THE NEXT TOOL CALL. IF NEEDED TAKE A STEP TO MAKE SURE YOU KNOW WHAT TO PASS TO THE NEXT TOOL CALL AND FORMAT THE INPUTS CORRECTLY.
                    IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
                    DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or any other comments or markup.
                    """

            planning_prompt += """
                    EXAMPLE:
                    [
                        {
                            "step": "Step one of the process thought for the question",
                            "tool": "tool to call",
                            "parameters": {
                                "arg1": "value1",
                                "arg2": "value2"
                            }
                        },
                        {
                            "step": "Step two of the process thought for the question",
                            "tool": "tool to call",
                            "parameters": {
                                "arg1": "value1",
                                "arg2": "value2"
                            }
                        }
                    ]
                    </SYSTEM_PROMPT>"""

            # Get planning steps
            # text_response, _, _ = await self.llm_provider.call(
            #     system_prompt=planning_prompt,
            #     user_prompt=message_info,
            #     temperature=options["planning_temperature"],
            #     skip_tools=True,
            # )
            allm_options = {
                "use_conversation": options["use_conversation"],
                "use_knowledge": options["use_knowledge"],
                "use_similar": options["use_similar"],
                "store_interaction": options["store_interaction"],
                "use_tools": True,
            }
            text_response, _, _ = await self.augmented_llm.process(
                message=message_info,
                system_prompt=planning_prompt,
                chat_id=chat_id,
                temperature=options["planning_temperature"],
                workflow_options=allm_options,
            )

            # Parse the JSON response
            try:
                json_response = json.loads(text_response)
                print("json_response: ", json_response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {text_response}")
                return await self._json_fallback(message, personality_provider, chat_id, text_response, **kwargs)

            # Execute each step
            for step in json_response:
                system_prompt = f"""CONTEXT: YOU ARE RUNNING STEPS FOR THE ORIGINAL QUESTION: {message_data}.
                PREVIOUS STEP RESPONSES: {steps_responses}"""

                skip_tools = False
                # skip_conversation_context = True
                if step["tool"] == "None":
                    skip_tools = True
                    # skip_conversation_context = False

                # Execute step
                text_response, image_url, tool_calls = await self.llm_provider.call(
                    system_prompt=system_prompt,
                    user_prompt=str(step),
                    temperature=options["execution_temperature"],
                    skip_tools=skip_tools,
                    tools=self.tool_manager.get_tools_config() if not skip_tools else None,
                    tool_choice="auto",  # "required" if not skip_tools else None,
                )

                # Retry logic if tool calls are expected but not found
                retries = 5
                while retries > 0:
                    if "<function" in text_response or (not tool_calls and step["tool"] != "None"):
                        logger.info("Retrying step due to missing tool call")
                        text_response, image_url, tool_calls = await self.llm_provider.call(
                            system_prompt=text_response,
                            user_prompt=str(text_response),
                            temperature=options["execution_temperature"],
                            skip_tools=False,
                            tool_choice="auto",
                        )
                        retries -= 1
                        await asyncio.sleep(5)
                    else:
                        break

                # Record step results
                step_response = {"step": step, "response": text_response}
                if image_url:
                    image_url_final = image_url
                steps_responses.append(step_response)

            # Generate final response
            final_format_prompt = kwargs.get("final_format_prompt", "")
            final_reasoning_prompt = f"""Generate the final response for the user.
            Given the context of your reasoning, and the steps you've taken, generate a final response for the user.
            Your final reasoning is: {text_response}
            You already have the final reasoning, just generate the final response for the user, don't do more steps or request more information.
            You are responding to the user message: {message_data}"""

            # Add personality if provided
            if personality_provider:
                prompt_final = personality_provider.get_formatted_personality() + final_reasoning_prompt
            else:
                prompt_final = final_reasoning_prompt

            # If custom format provided, use it
            if final_format_prompt:
                prompt_final = final_format_prompt + final_reasoning_prompt

            # Generate final response
            response, _, _ = await self.llm_provider.call(
                system_prompt=prompt_final,
                user_prompt=final_reasoning_prompt,
                temperature=options["final_temperature"],
                skip_tools=True,
            )

            # Store interaction if needed
            if not kwargs.get("skip_store", False) and chat_id:
                await kwargs.get("conversation_provider").store_interaction(
                    message, response, chat_id, kwargs.get("metadata", {})
                )

            return response, image_url_final, None

        except Exception as e:
            logger.error(f"Chain of thought processing failed: {str(e)}")
            return await self._fallback(message, personality_provider, chat_id, **kwargs)

    async def _json_fallback(self, message, personality_provider, chat_id, text_response, **kwargs):
        """Special fallback for JSON parsing errors that attempts to fix the JSON format"""
        logger.info("Attempting to fix malformed JSON response")

        fix_json_prompt = """
        The following text was supposed to be in valid JSON format but contains errors.
        Please convert it to a valid JSON array of steps with the same information.
        Each step should have "step", "tool", and "parameters" fields.

        Original text:
        ```
        {text}
        ```

        Return ONLY the fixed JSON with no additional text, explanations, or markdown formatting.
        """

        try:
            # Try to fix the JSON
            fixed_json_text, _, _ = await self.llm_provider.call(
                system_prompt=fix_json_prompt.format(text=text_response),
                user_prompt="Please fix the JSON format issues in the text above.",
                temperature=0.1,  # Low temperature for more deterministic output
                skip_tools=True,
            )

            # Try to parse the fixed JSON
            try:
                json_response = json.loads(fixed_json_text)
                logger.info("Successfully fixed JSON format")
                return json_response
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON even after attempted fix")
                return await self._fallback(message, personality_provider, chat_id, **kwargs)

        except Exception as e:
            logger.error(f"JSON fix attempt failed: {str(e)}")
            return await self._fallback(message, personality_provider, chat_id, **kwargs)

    async def _fallback(self, message, personality_provider, chat_id, **kwargs):
        """Fallback to simpler processing if CoT fails"""
        try:
            logger.info("Using fallback processing for failed CoT")
            # Simple direct call
            system_prompt = ""
            if personality_provider:
                system_prompt = personality_provider.get_formatted_personality()

            response, image_url, _ = await self.llm_provider.call(
                system_prompt=system_prompt,
                user_prompt=message,
                temperature=0.7,
                skip_tools=True,
            )

            return response, image_url, None

        except Exception as e:
            logger.error(f"Fallback processing failed: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your request.", None, None
