import json
import logging
from typing import List, Dict, Callable, Any

logger = logging.getLogger(__name__)

class ValidationManager:
    """Handles pre-validation of messages"""
    
    def __init__(self, llm_provider):
        self.llm_provider = llm_provider
        
    async def validate(
        self, 
        message: str, 
        agent_name: str = None, 
        strategies: List[str] = None, 
        **kwargs
    ) -> bool:
        """Validates a message against selected strategies"""
        
        # Default to relevance check if no strategies specified
        if not strategies:
            strategies = ["relevance"]
            
        # Skip validation for certain message types
        if kwargs.get("skip_validation", False):
            return True
            
        # For explicit mention strategy
        if "mention" in strategies and agent_name:
            # Check if message explicitly mentions the agent
            if agent_name.lower() in message.lower():
                return True
                
        # For topic relevance strategy
        if "relevance" in strategies:
            return await self._validate_relevance(message, agent_name, **kwargs)
            
        # Default to true if no strategies matched
        return True
        
    async def _validate_relevance(self, message: str, agent_name: str = None, **kwargs) -> bool:
        """Validate message relevance"""
        filter_message_tool = [
            {
                "type": "function",
                "function": {
                    "name": "filter_message",
                    "description": f"""Determine if a message should be ignored based on the following rules:
                        Return TRUE (ignore message) if:
                            - Message does not mention {agent_name or 'the assistant'}
                            - Message does not mention 'start raid'
                            - Message does not discuss: The Wired, Consciousness, Reality, Existence, Self, Philosophy, Technology, Crypto, AI, Machines
                            - For image requests: ignore if {agent_name or 'the assistant'} is not specifically mentioned

                        Return FALSE (process message) only if:
                            - Message explicitly mentions {agent_name or 'the assistant'}
                            - Message contains 'start raid'
                            - Message clearly discusses any of the listed topics
                            - Image request contains {agent_name or 'the assistant'}

                        If in doubt, return TRUE to ignore the message.""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "should_ignore": {
                                "type": "boolean",
                                "description": "TRUE to ignore message, FALSE to process message",
                            }
                        },
                        "required": ["should_ignore"],
                    },
                },
            }
        ]
        
        try:
            response = await self.llm_provider.call_with_tools(
                system_prompt="",
                user_prompt=message,
                temperature=0.5,
                tools=filter_message_tool,
            )
            
            # Extract result from tool call
            validation = False
            if "tool_calls" in response and response["tool_calls"]:
                tool_call = response["tool_calls"]
                args = json.loads(tool_call.function.arguments)
                filter_result = str(args["should_ignore"]).lower()
                validation = False if filter_result == "true" else True
                
            logger.info(f"Message validation result: {validation}")
            return validation
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return False  # Default to False on error 