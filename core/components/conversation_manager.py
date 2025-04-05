import logging
from datetime import datetime
from typing import Dict, List, Optional

from ..embedding import MessageData, get_embedding

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation context and history"""

    def __init__(self, message_store):
        self.message_store = message_store

    def get_embedding(self, message: str) -> List[float]:
        return get_embedding(message)

    async def get_conversation_context(self, chat_id: str, limit: int = 10) -> str:
        """Get conversation history context"""
        if not chat_id:
            return ""

        try:
            # Get conversation history
            system_prompt_conversation_context = "\n\nPrevious conversation history (in chronological order):\n"

            # Get last messages (will be in DESC order)
            conversation_messages = self.message_store.find_messages(
                message_type="agent_response", chat_id=chat_id, limit=limit
            )

            # Sort by timestamp and reverse to get chronological order
            conversation_messages.sort(key=lambda x: x["timestamp"], reverse=True)
            conversation_messages.reverse()

            # Build conversation history
            for msg in conversation_messages:
                if msg.get("original_query"):  # Ensure we have both question and answer
                    system_prompt_conversation_context += f"User: {msg['original_query']}\n"
                    system_prompt_conversation_context += f"Assistant: {msg['message']}\n\n"

            return system_prompt_conversation_context

        except Exception as e:
            logger.error(f"Error retrieving conversation context: {str(e)}")
            return ""

    async def get_similar_messages(
        self, embedding: List[float], chat_id: Optional[str] = None, threshold: float = 0.9, limit: int = 10
    ) -> str:
        """Get context from similar previous conversations"""
        if not embedding:
            return ""

        try:
            similar_messages = self.message_store.find_similar_messages(
                embedding, threshold=threshold, message_type="user_message", chat_id=chat_id
            )

            if not similar_messages:
                return ""

            context = "\n\nRelated previous conversations and responses\nNOTE: Please provide a response that differs from these recent replies, don't use the same words:\n"
            seen_responses = set()
            message_count = 0

            for similar_msg in similar_messages:
                # Find the agent's response where this similar message was the original_query
                agent_responses = self.message_store.find_messages(
                    message_type="agent_response", original_query=similar_msg["message"]
                )

                for response in agent_responses:
                    if response["message"] in seen_responses:
                        continue

                    seen_responses.add(response["message"])
                    context += f"""
                        Previous similar question: {similar_msg["message"]}
                        My response: {response["message"]}
                        Similarity score: {similar_msg.get("similarity", 0):.2f}
                        """
                    message_count += 1
                    if message_count >= limit:
                        break

            if message_count > 0:
                context += "\nConsider the above responses for context, but provide a fresh perspective that adds value to the conversation, don't repeat the same responses.\n"
                return context

            return ""

        except Exception as e:
            logger.error(f"Error retrieving similar messages: {str(e)}")
            return ""

    async def store_interaction(self, message: str, response: str, chat_id: str, metadata: Dict = None) -> None:
        """Store a conversation interaction"""
        if not message or not response:
            return

        try:
            # Generate message embedding
            message_embedding = get_embedding(message)

            # Store user message
            message_data = MessageData(
                message=message,
                embedding=message_embedding,
                timestamp=datetime.now().isoformat(),
                message_type="user_message",
                chat_id=chat_id,
                source_interface=metadata.get("source_interface"),
                original_query=None,
                original_embedding=None,
                tool_call=None,
                response_type=None,
                key_topics=None,
            )
            self.message_store.add_message(message_data)

            # Store agent response
            response_data = MessageData(
                message=response,
                embedding=get_embedding(response),
                timestamp=datetime.now().isoformat(),
                message_type="agent_response",
                chat_id=chat_id,
                source_interface=metadata.get("source_interface"),
                original_query=message,
                original_embedding=message_embedding,
                tool_call=metadata.get("tool_call"),
                response_type=metadata.get("response_type"),
                key_topics=metadata.get("key_topics"),
            )
            self.message_store.add_message(response_data)

        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
