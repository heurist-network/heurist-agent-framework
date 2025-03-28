import json
import logging
from typing import List

from core.embedding import MessageData, get_embedding

logger = logging.getLogger(__name__)


class KnowledgeProvider:
    """Manages knowledge storage and retrieval"""

    def __init__(self, message_store):
        self.message_store = message_store

    def get_embedding(self, message: str) -> List[float]:
        return get_embedding(message)

    async def get_knowledge_context(self, message: str, message_embedding: List[float]) -> str:
        """
        Get knowledge base data from the message embedding
        """
        if message_embedding is None:
            message_embedding = get_embedding(message)

        system_prompt_context = ""
        knowledge_base_data = self.message_store.find_similar_messages(
            message_embedding, threshold=0.6, message_type="knowledge_base"
        )

        logger.info(f"Found {len(knowledge_base_data)} relevant items from knowledge base")

        if knowledge_base_data:
            system_prompt_context = "\n\nConsider the Following As Facts and use them to answer the question if applicable and relevant:\nKnowledge base data:\n"
            for data in knowledge_base_data:
                system_prompt_context += f"{data['message']}\n"

        return system_prompt_context

    async def update_knowledge_base(self, json_file_path: str = "data/data.json") -> None:
        """
        Updates the knowledge base by processing JSON data and storing embeddings.
        Handles any JSON structure by treating each key-value pair as knowledge.
        """
        logger.info(f"Updating knowledge base from {json_file_path}")

        try:
            # Read JSON file
            with open(json_file_path, "r") as f:
                data = json.load(f)

            # Handle both list and dict formats
            items = data if isinstance(data, list) else [data]

            # Process each item
            for item in items:
                if not isinstance(item, dict):
                    continue

                # Create message content by combining all key-value pairs
                message_parts = []
                for key, value in item.items():
                    if isinstance(value, (str, int, float, bool)):
                        message_parts.append(f"{key}: {value}")
                    elif isinstance(value, (list, dict)):
                        # Handle nested structures by converting to string
                        message_parts.append(f"{key}: {json.dumps(value)}")

                message = "\n\n".join(message_parts)

                # Generate embedding for the message
                message_embedding = get_embedding(message)

                # Check if this exact message already exists
                existing_entries = self.message_store.find_similar_messages(
                    message_embedding,
                    threshold=0.99,  # Very high threshold to match nearly identical content
                )

                if existing_entries:
                    logger.info("Similar content already exists in knowledge base, skipping...")
                    continue

                # Store the message with metadata
                self.message_store.add_message(
                    MessageData(
                        message=message,
                        embedding=message_embedding,
                        timestamp=None,
                        message_type="knowledge_base",
                        chat_id=None,
                        source_interface=None,
                        original_query=None,
                        original_embedding=None,
                        response_type=None,
                        key_topics=None,
                        tool_call=None,
                    )
                )

            logger.info(f"Successfully updated knowledge base from {json_file_path}")

        except FileNotFoundError:
            logger.error(f"Knowledge base file not found: {json_file_path}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in knowledge base file: {json_file_path}")
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
