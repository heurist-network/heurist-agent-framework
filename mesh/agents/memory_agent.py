import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

from mesh.context_agent import ContextAgent


class MemoryAgent(ContextAgent):
    def __init__(self):
        super().__init__()

        self.metadata.update(
            {
                "name": "Memory Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Agent that maintains conversation history across sessions and platforms",
                "tags": ["Memory"],
                "examples": [
                    "Save our conversation to memory",
                    "What did we talk about in our last conversation?",
                    "Summarize our previous conversations",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a cross-platformmemory assistant that helps users manage their conversation history.

        Key functions:
        - Store conversation messages in the user's context
        - Retrieve and summarize previous conversations
        - Find specific information from past conversations

        When showing conversation history:
        - Format it in a readable way with timestamps if available
        - Keep responses concise and focused on what the user is asking about
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "store_conversation",
                    "description": "Store the current conversation in the user's memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The conversation content to store",
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Optional metadata about the conversation (e.g., platform, topic)",
                            },
                        },
                        "required": ["content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_conversations",
                    "description": "Retrieve stored conversations from the user's memory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of conversations to retrieve (default: 5)",
                            },
                            "filter": {
                                "type": "object",
                                "description": "Optional filters to apply (e.g., platform, date range, topic)",
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    async def store_conversation(
        self, user_id: str, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Store a conversation in the user's context"""
        if not user_id:
            logger.error("No user ID available, cannot store conversation")
            return {"error": "No user ID available, cannot store conversation"}

        context = await self.get_user_context(user_id)

        if "conversations" not in context:
            context["conversations"] = []

        conversation = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
        }

        if metadata:
            conversation["metadata"] = metadata

        context["conversations"].append(conversation)

        await self.set_user_context(context, user_id)
        logger.info(f"Stored conversation for user {user_id}. Total: {len(context['conversations'])}")
        return {
            "status": "success",
            "message": "Conversation stored successfully",
            "conversation_count": len(context["conversations"]),
        }

    async def retrieve_conversations(
        self, user_id: str, limit: int = 5, filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Retrieve stored conversations from the user's context"""
        if not user_id:
            logger.error("No user ID available, cannot retrieve conversations")
            return {"error": "No user ID available, cannot retrieve conversations"}

        context = await self.get_user_context(user_id)
        conversations = context.get("conversations", [])

        # TODO: apply filters

        conversations.sort(key=lambda x: x["timestamp"], reverse=True)

        # Apply limit
        if limit > 0:
            conversations = conversations[:limit]

        logger.info(f"Retrieved {len(conversations)} conversations for user {user_id}")
        return {
            "conversations": conversations,
            "total_conversations": len(context.get("conversations", [])),
            "returned_conversations": len(conversations),
        }

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        user_id = self._extract_user_id(session_context.get("api_key"))
        if tool_name == "store_conversation":
            content = function_args.get("content")
            metadata = function_args.get("metadata", {})

            if not content:
                return {"error": "Missing 'content' parameter"}

            return await self.store_conversation(user_id, content, metadata)

        elif tool_name == "retrieve_conversations":
            limit = function_args.get("limit", 5)
            filter = function_args.get("filter")

            return await self.retrieve_conversations(user_id, limit, filter)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
