import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class AugmentedLLMCall:
    """Standard RAG + tools pattern"""

    def __init__(self, knowledge_provider, conversation_provider, tool_manager, llm_provider):
        self.knowledge_provider = knowledge_provider
        self.conversation_provider = conversation_provider
        self.tool_manager = tool_manager
        self.llm_provider = llm_provider

    async def process(
        self,
        message: str,
        system_prompt: str = "",
        personality_provider=None,
        chat_id: str = None,
        workflow_options: Dict = None,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Process message using RAG + tools"""

        # Set default workflow options
        options = {
            "use_knowledge": True,
            "use_conversation": True,
            "store_interaction": True,
            "use_similar": True,
            "use_tools": True,
            "max_tokens": None,
            "temperature": 0.7,
            "model_id": None,
            "tool_choice": "auto",
        }

        # Override with provided options
        if workflow_options:
            options.update(workflow_options)

        # Get message embedding if not provided
        message_embedding = None

        # Add personality if provided
        if personality_provider and system_prompt != "":
            system_prompt = personality_provider.get_formatted_personality()

        if options["use_knowledge"] or options["use_similar"]:
            try:
                message_embedding = self.conversation_provider.get_embedding(message)
            except Exception as e:
                logger.error(f"Failed to generate embedding: {str(e)}")

        # Get knowledge context if enabled
        if options["use_knowledge"] and message_embedding:
            knowledge_context = await self.knowledge_provider.get_knowledge_context(message, message_embedding)
            if knowledge_context:
                system_prompt += f"\n\n{knowledge_context}"

        # Get conversation context if enabled
        if options["use_conversation"] and chat_id:
            conversation_context = await self.conversation_provider.get_conversation_context(chat_id)
            if conversation_context:
                system_prompt += f"\n\n{conversation_context}"

        # Get similar messages if enabled
        if options["use_similar"] and message_embedding:
            similar_context = await self.conversation_provider.get_similar_messages(
                message_embedding, chat_id=chat_id, threshold=0.9, limit=10
            )
            if similar_context:
                system_prompt += f"\n\n{similar_context}"

        # Make LLM call with tools if enabled
        try:
            text_response, image_url, tool_back = await self.llm_provider.call(
                system_prompt=system_prompt,
                user_prompt=message,
                temperature=options["temperature"],
                max_tokens=options["max_tokens"],
                model_id=options["model_id"],
                skip_tools=not options["use_tools"],
                tools=self.tool_manager.get_tools_config() if options["use_tools"] else None,
                tool_choice=options["tool_choice"] if options["use_tools"] else None,
            )

            # Store interaction if needed
            if options["store_interaction"] and chat_id:
                metadata = kwargs.get("metadata", {})
                if tool_back:
                    metadata["tool_call"] = tool_back

                await self.conversation_provider.store_interaction(message, text_response, chat_id, metadata)

            return text_response, image_url, tool_back

        except Exception as e:
            logger.error(f"LLM processing failed: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}", None, None
