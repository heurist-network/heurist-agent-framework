import logging
import os
import threading
from datetime import datetime
from pathlib import Path
from queue import Queue
from typing import Dict, Optional, Tuple

import dotenv

from agents.base_agent import BaseAgent
from agents.tools.default_tool_box import DefaultToolBox
from core.clients.search_client import SearchClient
from core.components.conversation_manager import ConversationManager
from core.components.knowledge_provider import KnowledgeProvider
from core.components.llm_provider import LLMProvider
from core.components.media_handler import MediaHandler
from core.components.personality_provider import PersonalityProvider
from core.components.validation_manager import ValidationManager
from core.embedding import MessageStore, PostgresConfig, PostgresVectorStorage, SQLiteConfig, SQLiteVectorStorage
from core.tools.tools_mcp import Tools
from core.workflows.augmented_llm import AugmentedLLMCall
from core.workflows.chain_of_thought import ChainOfThoughtReasoning
from core.workflows.deep_research import ResearchWorkflow

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
os.environ.clear()
dotenv.load_dotenv(override=True)
logger.info("Environment variables reloaded")

# Constants
HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")
IMAGE_GENERATION_PROBABILITY = float(os.getenv("IMAGE_GENERATION_PROBABILITY", 0.3))
BASE_IMAGE_PROMPT = os.getenv("BASE_IMAGE_PROMPT", "")


class CoreAgent(BaseAgent):
    """Refactored core agent implementation using modular components"""

    def __init__(self):
        super().__init__()

        # Initialize storage
        self.message_store = self._initialize_vector_storage()

        self.personality_provider = PersonalityProvider()
        self.prompt_config = self.personality_provider.prompt_config
        self.knowledge_provider = KnowledgeProvider(self.message_store)
        self.conversation_manager = ConversationManager(self.message_store)

        # Initialize managers
        self.tools = Tools(DefaultToolBox)
        self.llm_provider = LLMProvider(
            base_url=HEURIST_BASE_URL,
            api_key=HEURIST_API_KEY,
            large_model_id=LARGE_MODEL_ID,
            small_model_id=SMALL_MODEL_ID,
            tool_manager=self.tools,
        )
        self.validation_manager = ValidationManager(self.llm_provider)
        self.media_handler = MediaHandler(self.llm_provider)

        # Initialize reasoning patterns
        self.augmented_llm = AugmentedLLMCall(
            self.knowledge_provider, self.conversation_manager, self.tools, self.llm_provider
        )

        self.chain_of_thought = ChainOfThoughtReasoning(self.llm_provider, self.tools, self.augmented_llm)

        # Interface management
        self.interfaces = {}
        self._message_queue = Queue()
        self._lock = threading.Lock()

    def register_interface(self, name, interface):
        """Register a communication interface"""
        with self._lock:
            self.interfaces[name] = interface

    async def initialize(self, server_url: str = "http://localhost:8000/sse"):
        await self.tools.initialize(server_url=server_url)

    async def handle_message(
        self,
        message: str,
        message_type: str = "user_message",
        source_interface: str = None,
        chat_id: str = None,
        system_prompt: str = None,
        skip_pre_validation: bool = False,
        skip_embedding: bool = False,
        skip_similar: bool = True,
        skip_conversation_context: bool = False,
        skip_tools: bool = False,
        max_tokens: int = None,
        model_id: str = None,
        temperature: float = 0.4,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Main message handler - delegates to appropriate workflow"""

        logger.info(f"Handling message from {source_interface}: {message[:100]}...")

        # Convert chat_id to string to ensure consistent typing
        chat_id = str(chat_id) if chat_id else "default"

        # Pre-processing: validation and embedding generation
        if not await self.pre_process(message, skip_pre_validation, source_interface):
            logger.info(f"Message failed pre-validation, skipping: {message[:100]}...")
            return None, None, None

        # Override system prompt if provided
        if system_prompt is None:
            system_prompt = self.personality_provider.get_formatted_personality()

        # Workflow options
        workflow_options = {
            "use_knowledge": not skip_embedding,
            "use_conversation": not skip_conversation_context,
            "store_interaction": not skip_embedding,
            "use_similar": not skip_similar,
            "use_tools": not skip_tools,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model_id": model_id or LARGE_MODEL_ID,
        }

        # Standard augmented LLM processing
        logger.info("Using standard augmented LLM processing")
        response, image_url, tool_result = await self.augmented_llm.process(
            message=message,
            personality_provider=self.personality_provider,
            chat_id=chat_id,
            workflow_options=workflow_options,
            metadata={"message_type": message_type, "source_interface": source_interface},
            agent=self,
            **kwargs,
        )

        return response, image_url, tool_result

    async def smart_message(
        self,
        message: str,
        message_type: str = "user_message",
        source_interface: str = None,
        chat_id: str = None,
        system_prompt: str = None,
        skip_pre_validation: bool = False,
        skip_embedding: bool = False,
        skip_similar: bool = True,
        skip_conversation_context: bool = False,
        skip_tools: bool = False,
        max_tokens: int = None,
        model_id: str = None,
        temperature: float = 0.4,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Main message handler - delegates to appropriate workflow"""

        logger.info(f"Handling message from {source_interface}: {message[:100]}...")

        # Convert chat_id to string to ensure consistent typing
        chat_id = str(chat_id) if chat_id else "default"

        # Pre-processing: validation and embedding generation
        if not await self.pre_process(message, skip_pre_validation, source_interface):
            logger.info(f"Message failed pre-validation, skipping: {message[:100]}...")
            return None, None, None

        # Override system prompt if provided
        if system_prompt is None:
            system_prompt = self.personality_provider.get_formatted_personality()

        # Workflow options
        workflow_options = {
            "use_knowledge": not skip_embedding,
            "use_conversation": not skip_conversation_context,
            "store_interaction": not skip_embedding,
            "use_similar": not skip_similar,
            "use_tools": not skip_tools,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model_id": model_id or LARGE_MODEL_ID,
        }

        # Decide if image should be generated alongside text
        should_generate_image = self.media_handler.should_generate_image(message)

        # Check if deep research is requested or should be used
        if kwargs.get("force_research", False) or self._should_use_research(message):
            logger.info("Using deep research workflow")
            # Configure research options
            research_options = {
                "interactive": kwargs.get("interactive", False),
                "breadth": kwargs.get("breadth", 3),
                "depth": kwargs.get("depth", 2),
                "concurrency": kwargs.get("concurrency", 3),
                "temperature": workflow_options["temperature"],
                "raw_data_only": False,
            }

            response, research_data = await self.deep_research(query=message, chat_id=chat_id, **research_options)

            # Store in conversation history if available
            # if not skip_conversation_context:
            #     await self.conversation_manager.add_message(
            #         chat_id=chat_id,
            #         role="user",
            #         content=message,
            #         embedding=message_embedding,
            #         metadata={"message_type": message_type, "source_interface": source_interface},
            #     )
            #     await self.conversation_manager.add_message(
            #         chat_id=chat_id,
            #         role="assistant",
            #         content=response,
            #         metadata={
            #             "workflow": "deep_research",
            #             "research_data": {"url_count": len(research_data.get("visited_urls", []))},
            #         },
            #     )

            # No image for research responses by default
            return response, None, {"research_data": research_data}

        # Choose reasoning pattern
        elif kwargs.get("force_cot", False) or self._should_use_cot(message):
            logger.info("Using chain of thought reasoning")
            response, image_url, tool_result = await self.chain_of_thought.process(
                message=message,
                personality_provider=self.personality_provider,
                chat_id=chat_id,
                workflow_options=workflow_options,
                metadata={"message_type": message_type, "source_interface": source_interface},
                agent=self,
                conversation_provider=self.conversation_manager,
                **kwargs,
            )
        else:
            # Standard augmented LLM processing
            logger.info("Using standard augmented LLM processing")
            response, image_url, tool_result = await self.augmented_llm.process(
                message=message,
                personality_provider=self.personality_provider,
                chat_id=chat_id,
                workflow_options=workflow_options,
                metadata={"message_type": message_type, "source_interface": source_interface},
                agent=self,
                **kwargs,
            )

        # Generate image if needed and no image was already generated by a tool
        if should_generate_image and not image_url:
            try:
                image_prompt = await self.media_handler.generate_image_prompt(message + " " + response)
                image_url = await self.media_handler.generate_image(image_prompt)
            except Exception as e:
                logger.error(f"Failed to generate image: {str(e)}")

        # Post-process the response
        final_response = response  # await self.post_process(response, **kwargs)

        return final_response, image_url, tool_result

    async def pre_process(
        self, message: str, skip_pre_validation: bool = False, source_interface: str = None, **kwargs
    ) -> bool:
        """Pre-process and validate incoming messages"""
        if not message or not message.strip():
            return False

        # Skip validation if explicitly requested or for specific interfaces
        if skip_pre_validation:
            return True

        do_pre_validation = (
            False
            if source_interface
            in ["api", "twitter", "twitter_reply", "farcaster", "farcaster_reply", "telegram", "terminal"]
            else True
        )

        if do_pre_validation:
            return await self.validation_manager.validate(message, agent_name=self.personality_provider.get_name())

        return True

    async def post_process(self, response: str, **kwargs) -> str:
        """Post-process agent responses"""
        if not response:
            return "I apologize, but I couldn't generate a proper response."

        # Any additional post-processing logic here
        return response

    async def send_to_interface(self, target_interface: str, message: dict) -> bool:
        """Send a message to a specific interface"""
        try:
            with self._lock:
                if target_interface not in self.interfaces:
                    logger.error(f"Interface {target_interface} not registered")
                    return False

                # Validate message format
                if not isinstance(message, dict) or "type" not in message or "content" not in message:
                    logger.error("Invalid message format")
                    return False

                # Add timestamp and target
                message["timestamp"] = datetime.now().isoformat()
                message["target"] = target_interface

                # Queue the message
                self._message_queue.put(message)

                # Get interface instance
                interface = self.interfaces[target_interface]

                # Handle different message types
                if message["type"] == "message":
                    if hasattr(interface, "send_message"):
                        await interface.send_message(
                            chat_id=message.get("chat_id", "default"),
                            message=message["content"],
                            image_url=message.get("image_url"),
                        )

                logger.info(f"Message sent to {target_interface}: {message['type']}")
                return True

        except Exception as e:
            logger.error(f"Error sending message to {target_interface}: {str(e)}")
            return False

    async def agent_cot(
        self,
        message: str,
        user: str = "User",
        display_name: str = None,
        chat_id: str = "General",
        source_interface: str = "None",
        final_format_prompt: str = "",
        skip_conversation_context: bool = False,
    ) -> Tuple[str, Optional[str], Optional[Dict]]:
        """Chain of thought processing (for backward compatibility)"""
        chat_id = str(chat_id) if chat_id else "General"
        response, image_url_final, _ = await self.chain_of_thought.process(
            message=message,
            personality_provider=self.personality_provider,
            chat_id=chat_id,
            workflow_options={
                "use_conversation": not skip_conversation_context,
            },
            user=user,
            display_name=display_name,
            source_interface=source_interface,
            final_format_prompt=final_format_prompt,
            agent=self,
            conversation_provider=self.conversation_manager,
        )
        return response, image_url_final, None

    def _should_use_cot(self, message: str) -> bool:
        """Determine if message should use chain of thought"""
        # Simple heuristic based on message complexity
        complexity_indicators = [
            "why",
            "how",
            "explain",
            "analyze",
            "compare",
            "difference",
            "similarities",
            "pros and cons",
            "advantages",
            "disadvantages",
        ]

        # Check message length - longer messages may benefit from CoT
        if len(message.split()) > 50:
            return True

        # Check for complexity indicators
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in complexity_indicators)

    def _should_use_research(self, message: str) -> bool:
        """Determine if message should use deep research workflow"""
        # Check for explicit research indicators
        research_indicators = [
            "research",
            "deep dive",
            "investigate",
            "find information about",
            "comprehensive analysis",
            "thorough investigation",
            "deep research",
            "detailed report",
            "find out about",
            "learn about",
        ]

        # Check for research question patterns
        research_patterns = [
            "what are the latest",
            "what is the current state of",
            "how has the field of",
            "compare and contrast",
            "what developments have occurred",
            "what's the history of",
            "explain the evolution of",
            "analyze the trends in",
        ]

        # Check for complex topic indicators that benefit from research
        complex_topics = [
            "economics",
            "politics",
            "technology trends",
            "scientific advances",
            "market analysis",
            "industry overview",
            "historical context",
            "latest developments",
            "future predictions",
            "state of the art",
        ]

        # Weighted scoring system
        score = 0

        # Check for explicit research keywords (stronger signals)
        message_lower = message.lower()
        for indicator in research_indicators:
            if indicator in message_lower:
                score += 2

        # Check for research patterns (moderate signals)
        for pattern in research_patterns:
            if pattern in message_lower:
                score += 1

        # Check for complex topics (weaker signals but add context)
        for topic in complex_topics:
            if topic in message_lower:
                score += 0.5

        # Length also matters - longer, more complex queries benefit from research
        if len(message.split()) > 25:
            score += 1

        # Higher threshold to avoid false positives
        return score >= 2

    def _initialize_vector_storage(self):
        """Initialize appropriate vector storage based on environment"""
        # DB configuration logic from original code
        if all([os.getenv(env) for env in ["VECTOR_DB_NAME", "VECTOR_DB_USER", "VECTOR_DB_PASSWORD"]]):
            vdb_config = PostgresConfig(
                host=os.getenv("VECTOR_DB_HOST", "localhost"),
                port=int(os.getenv("VECTOR_DB_PORT", 5432)),
                database=os.getenv("VECTOR_DB_NAME"),
                user=os.getenv("VECTOR_DB_USER"),
                password=os.getenv("VECTOR_DB_PASSWORD"),
                table_name=os.getenv("VECTOR_DB_TABLE", "message_embeddings"),
            )
            storage = PostgresVectorStorage(vdb_config)
        else:
            config = SQLiteConfig()
            storage = SQLiteVectorStorage(config)

        return MessageStore(storage)

    # Methods added for backward compatibility
    async def update_knowledge_base(self, json_file_path: str = "data/data.json") -> None:
        """Update knowledge base from JSON file"""
        return await self.knowledge_provider.update_knowledge_base(json_file_path)

    async def generate_image_prompt(self, message: str) -> str:
        """Generate image prompt based on message"""
        return await self.media_handler.generate_image_prompt(message)

    async def handle_image_generation(self, prompt: str, base_prompt: str = "") -> Optional[str]:
        """Handle image generation with retry"""
        return await self.media_handler.generate_image(prompt, base_prompt)

    async def transcribe_audio(self, audio_file_path: Path) -> str:
        """Transcribe audio to text"""
        return await self.media_handler.transcribe_audio(audio_file_path)

    async def handle_text_to_speech(self, text: str) -> Optional[Path]:
        """Handle text-to-speech conversion"""
        return await self.media_handler.text_to_speech(text)

    async def deep_research(
        self,
        query: str,
        chat_id: str = None,
        interactive: bool = False,
        breadth: int = 3,
        depth: int = 2,
        concurrency: int = 3,
        temperature: float = 0.7,
        raw_data_only: bool = False,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Perform deep research on a query using the research workflow.

        Args:
            query: The research query or topic to investigate
            chat_id: Unique identifier for the conversation
            interactive: Whether to ask clarifying questions first
            breadth: Number of parallel searches to perform (1-5)
            depth: How deep to go in research (1-3)
            concurrency: Maximum concurrent requests
            temperature: Temperature for LLM calls
            raw_data_only: Whether to return only raw data without report

        Returns:
            Tuple of (research report, research results data)
        """
        research_model = os.environ.get("RESEARCH_MODEL", "mistralai/mixtral-8x22b-instruct")
        try:
            exa_search_client = SearchClient(client_type="exa", api_key=os.environ.get("EXA_API_KEY", ""), rate_limit=1)
            search_client = SearchClient(
                client_type="firecrawl", api_key=os.environ.get("FIRECRAWL_KEY", ""), rate_limit=1
            )
            duckduckgo_search_client = SearchClient(client_type="duckduckgo", rate_limit=5)
            # Initialize the research workflow
            research_workflow = ResearchWorkflow(
                llm_provider=self.llm_provider,
                tool_manager=self.tools,
                search_clients={
                    "exa": exa_search_client,
                    "firecrawl": search_client,
                    "duckduckgo": duckduckgo_search_client,
                },
            )

            # Configure workflow options
            workflow_options = {
                "interactive": interactive,
                "breadth": min(max(breadth, 1), 5),  # Ensure within valid range (1-5)
                "depth": min(max(depth, 1), 3),  # Ensure within valid range (1-3)
                "concurrency": min(max(concurrency, 1), 9),
                "temperature": temperature,
                "raw_data_only": raw_data_only,
                "report_model": research_model,
            }
            print(f"workflow_options: {workflow_options}")
            # Process the research request
            report, _, research_result = await research_workflow.process(
                message=query,
                personality_provider=self.personality_provider,
                chat_id=chat_id,
                workflow_options=workflow_options,
                search_providers=["firecrawl", "exa", "duckduckgo"],
                **kwargs,
            )

            return report, research_result

        except Exception as e:
            logger.error(f"Deep research failed: {str(e)}")
            return f"Research failed: {str(e)}", None

    async def deeper_research(
        self,
        query: str,
        chat_id: str = None,
        interactive: bool = False,
        breadth: int = 3,
        depth: int = 2,
        concurrency: int = 3,
        temperature: float = 0.7,
        raw_data_only: bool = False,
        **kwargs,
    ) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Perform deep research on a query using the research workflow.

        Args:
            query: The research query or topic to investigate
            chat_id: Unique identifier for the conversation
            interactive: Whether to ask clarifying questions first
            breadth: Number of parallel searches to perform (1-5)
            depth: How deep to go in research (1-3)
            concurrency: Maximum concurrent requests
            temperature: Temperature for LLM calls
            raw_data_only: Whether to return only raw data without report

        Returns:
            Tuple of (research report, research results data)
        """
        try:
            exa_search_client = SearchClient(client_type="exa", api_key=os.environ.get("EXA_API_KEY", ""), rate_limit=1)
            search_client = SearchClient(
                client_type="firecrawl", api_key=os.environ.get("FIRECRAWL_KEY", ""), rate_limit=1
            )
            duckduckgo_search_client = SearchClient(client_type="duckduckgo", rate_limit=5)
            # Initialize the research workflow
            research_workflow = ResearchWorkflow(
                llm_provider=self.llm_provider,
                tool_manager=self.tools,
                search_clients={
                    "exa": exa_search_client,
                    "firecrawl": search_client,
                    "duckduckgo": duckduckgo_search_client,
                },
            )

            # Configure workflow options
            workflow_options = {
                "interactive": interactive,
                "breadth": min(max(breadth, 1), 5),  # Ensure within valid range (1-5)
                "depth": min(max(depth, 1), 3),  # Ensure within valid range (1-3)
                "concurrency": min(max(concurrency, 1), 6),
                "temperature": temperature,
                "raw_data_only": raw_data_only,
                "report_model": "mistralai/mixtral-8x22b-instruct",
            }
            print(f"workflow_options: {workflow_options}")
            # Process the research request
            report, _, research_result = await research_workflow.process(
                message=query,
                personality_provider=self.personality_provider,
                chat_id=chat_id,
                workflow_options=workflow_options,
                search_providers=["firecrawl"],
                **kwargs,
            )
            print(report[:200])
            cot_prompt = f"""
            You are a helpful assistant that can answer questions and help with tasks.
            You are given a report and a question.
            You need to answer the question based on the report. See if there's tools relevevant to the question and use them to enhance the report.
            Report: {report}
            Question: {query}
            Keep the Response as a report folowing the original format of the report.
            """

            logger.info("Using chain of thought reasoning")
            response, image_url, tool_result = await self.chain_of_thought.process(
                message=query,
                system_prompt=cot_prompt,
                chat_id=chat_id,
                workflow_options=workflow_options,
                agent=self,
                skip_store=True,
                conversation_provider=self.conversation_manager,
                **kwargs,
            )
            final_report_prompt = f"""
            You are a helpful assistant that can answer questions and help with tasks.
            You are given a report and a question.
            You need to enhance the report based on the extra information.
            Report: {report}
            Question: {query}
            Extra information: {response}
            Keep the Response as a report folowing the original format of the report. Make sure it's a valid markdown and all original content is included.
            """
            response, _, _ = await self.llm_provider.call(
                message=query,
                system_prompt=final_report_prompt,
                user_prompt=query,
                temperature=0.3,
                model_id=workflow_options["report_model"],
            )

            return response, tool_result

        except Exception as e:
            logger.error(f"Deep research failed: {str(e)}")
            return f"Research failed: {str(e)}", None
