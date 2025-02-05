import json
import logging
import os
import random
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import dotenv
from core.config import PromptConfig
from core.llm import call_llm_with_tools, call_llm, LLMError
from core.imgen import generate_image_with_retry, generate_image_prompt, generate_image_with_retry_smartgen
from core.voice import transcribe_audio, speak_text
from core.embedding import get_embedding, MessageStore, PostgresConfig, PostgresVectorStorage, EmbeddingError, SQLiteConfig, SQLiteVectorStorage, MessageData
import threading
from queue import Queue
import asyncio
from agents.tools import Tools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# os.reload_environ()
# dotenv.load_dotenv(override=True)


os.environ.clear()
dotenv.load_dotenv(override=True)
logger.info("Environment variables reloaded")
# Constants
HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")
TWEET_WORD_LIMITS = [15, 20, 30, 35]
IMAGE_GENERATION_PROBABILITY = 0.3
BASE_IMAGE_PROMPT = ""

class CoreAgent:
    def __init__(self):
        self.prompt_config = PromptConfig()
        self.tools = Tools()
        self.interfaces = {}
        self._message_queue = Queue()
        self._lock = threading.Lock()
        self.last_tweet_id = 0
        self.last_raid_tweet_id = 0

        # Use PostgreSQL if configured, otherwise default to SQLite
        if all([os.getenv(env) for env in ["VECTOR_DB_NAME", "VECTOR_DB_USER", "VECTOR_DB_PASSWORD"]]):
            vdb_config = PostgresConfig(
                host=os.getenv("VECTOR_DB_HOST", "localhost"),
                port=int(os.getenv("VECTOR_DB_PORT", 5432)),
                database=os.getenv("VECTOR_DB_NAME"),
                user=os.getenv("VECTOR_DB_USER"),
                password=os.getenv("VECTOR_DB_PASSWORD"),
                table_name=os.getenv("VECTOR_DB_TABLE", "message_embeddings")
            )
            storage = PostgresVectorStorage(vdb_config)
        else:
            config = SQLiteConfig()
            storage = SQLiteVectorStorage(config)
        
        self.message_store = MessageStore(storage)
    
    def register_interface(self, name, interface):
        with self._lock:
            self.interfaces[name] = interface
    def basic_personality_settings(self) -> str:
        system_prompt = "Use the following settings as part of your personality and voice if applicable in the conversation context: "
        basic_options = random.sample(
            self.prompt_config.get_basic_settings(), 2)
        style_options = random.sample(
            self.prompt_config.get_interaction_styles(), 2)
        system_prompt = system_prompt + ' '.join(
            basic_options) + ' ' + ' '.join(style_options)
        return system_prompt
    
    async def pre_validation(self, message: str) -> bool:
        """
        Pre-validation of the message
        
        Args:
            message: The user's message
            
        Returns:
            True if the message is valid, False otherwise
        """
        name = self.prompt_config.get_name()
        filter_message_tool = [
            {
                "type": "function",
                "function": {
                    "name": "filter_message",
                    "description": f"""Determine if a message should be ignored based on the following rules:
                        Return TRUE (ignore message) if:
                            - Message does not mention {name}
                            - Message does not mention 'start raid'
                            - Message does not discuss: The Wired, Consciousness, Reality, Existence, Self, Philosophy, Technology, Crypto, AI, Machines
                            - For image requests: ignore if {name} is not specifically mentioned
                        
                        Return FALSE (process message) only if:
                            - Message explicitly mentions {name}
                            - Message contains 'start raid'
                            - Message clearly discusses any of the listed topics
                            - Image request contains {name}
                        
                        If in doubt, return TRUE to ignore the message.""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "should_ignore": {
                                "type": "boolean",
                                "description": "TRUE to ignore message, FALSE to process message"
                            }
                        },
                        "required": ["should_ignore"]
                    }
                }
            }
        ]
        try:
            response = call_llm_with_tools(
                HEURIST_BASE_URL,
                HEURIST_API_KEY, 
                SMALL_MODEL_ID,
                system_prompt="",#"Always call the filter_message tool with the message as the argument",#self.prompt_config.get_telegram_rules(),
                user_prompt=message,
                temperature=0.5,
                tools=filter_message_tool
            )
            print(response)
            #response = response.lower()
            #validation = False if "false" in response else True if "true" in response else False
            validation = False
            if 'tool_calls' in response and response['tool_calls']:
                tool_call = response['tool_calls']
                args = json.loads(tool_call.function.arguments)
                filter_result = str(args['should_ignore']).lower()
                validation = False if filter_result == "true" else True
            print("validation: ", validation)
            return validation
        except Exception as e:
            logger.error(f"Pre-validation failed: {str(e)}")
            return False
    async def generate_image_prompt(self, message: str) -> str:
        """Generate an image prompt based on the tweet content"""
        logger.info("Generating image prompt")
        prompt = self.prompt_config.get_template_image_prompt().format(tweet=message)
        logger.info("Prompt: %s", prompt)
        try:
            image_prompt = call_llm(
                HEURIST_BASE_URL,
                HEURIST_API_KEY, 
                SMALL_MODEL_ID,
                system_prompt=self.prompt_config.get_system_prompt(),
                user_prompt=prompt,
                temperature=0.7,
            )
        except Exception as e:
            logger.error(f"Failed to generate image prompt: {str(e)}")
            return None
        logger.info("Generated image prompt: %s", image_prompt)
        return image_prompt
    
    async def handle_image_generation(self, prompt: str, base_prompt: str = "") -> Optional[str]:
        """
        Handle image generation requests with retry logic
        
        Args:
            prompt: The image generation prompt
            base_prompt: Optional base prompt to prepend
            
        Returns:
            Generated image URL or None if failed
        """
        try:
            full_prompt = base_prompt + prompt if base_prompt else prompt
            #result = generate_image_with_retry(prompt=full_prompt)
            #SMARTGEN
            print("full_image_prompt: ", full_prompt)
            result = await generate_image_with_retry_smartgen(prompt=full_prompt)
            print(result)
            return result
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return None



    async def transcribe_audio(self, audio_file_path: Path) -> str:
        """
        Handle voice transcription requests
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            return transcribe_audio(audio_file_path)
        except Exception as e:
            logger.error(f"Voice transcription failed: {str(e)}")
            raise

    async def handle_text_to_speech(self, text: str) -> Path:
        """
        Handle text-to-speech conversion
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Path to generated audio file
        """
        try:
            return speak_text(text)
        except Exception as e:
            logger.error(f"Text-to-speech conversion failed: {str(e)}")
            raise

    async def handle_message(self, 
                             message: str, 
                             message_type: str = "user_message",
                             source_interface: str = None, 
                             chat_id: str = None, 
                             system_prompt: str = None, 
                             skip_embedding: bool = False, 
                             skip_similar: bool = True,
                             skip_tools: bool = False,
                             skip_conversation_context: bool = True,
                             external_tools: List[str] = [],
                             max_tokens: int = None,
                             model_id: str = LARGE_MODEL_ID,
                             temperature: float = 0.4,
                             skip_pre_validation: bool = False,
                             tool_choice: str = "auto"
                             ):
        """
        Handle message and optionally notify other interfaces.        
        Args:
            message: The message to process
            source_interface: Optional name of the interface that sent the message
            chat_id: Optional chat ID for the conversation
            skip_validation: Optional flag to skip pre-validation
            skip_embedding: Optional flag to skip embedding
            skip_tools: Optional flag to skip tools

        Returns:
            tuple: (text_response, image_url, tool_back)
        """
        logger.info(f"Handling message from {source_interface}")
        logger.info(f"registered interfaces: {self.interfaces}")

        chat_id = str(chat_id)
        self.current_message = message

        system_prompt_context = ""
        system_prompt_conversation_context = ""

        if system_prompt is None:
            system_prompt = self.basic_personality_settings()
            
        system_prompt = self.prompt_config.get_system_prompt() + system_prompt

        do_pre_validation = False if source_interface in [
            "api", "twitter", "twitter_reply", "farcaster", "farcaster_reply", "telegram",
            "terminal"
        ] else True
        if not skip_pre_validation and do_pre_validation and not await self.pre_validation(message):
            logger.debug(f"Message failed pre-validation: {message[:100]}...")
            return None, None, None
        
        try:
            message_embedding = get_embedding(message)
            logger.info(f"Generated embedding for message: {message[:50]}...")
            system_prompt_context = self.get_knowledge_base(message, message_embedding)
            
            if not skip_conversation_context:
                system_prompt += self.get_conversation_context(chat_id)

            if not skip_similar:
                system_prompt_context += self.get_similar_messages(message, message_embedding, message_type, chat_id)
                    
            system_prompt += system_prompt_context
            
            response = call_llm_with_tools(
                HEURIST_BASE_URL,
                HEURIST_API_KEY,
                model_id,
                system_prompt=system_prompt,
                user_prompt=message,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=self.tools.get_tools_config() + external_tools if not skip_tools else None,
                tool_choice=tool_choice if not skip_tools else None
            )
            
            # Process response and handle tools
            text_response = ""
            image_url = None
            tool_back = None
            logger.info("response: ", response)
            print("response: ", response)
            if not response:
                return "Sorry, I couldn't process your message.", None
            
            if 'content' in response and response['content']:  # Add null check
                text_response = response['content'].strip('"') if isinstance(response['content'], str) else str(response['content'])

            # Handle tool calls
            
            if 'tool_calls' in response and response['tool_calls']:
                tool_call = response['tool_calls']
                args = json.loads(tool_call.function.arguments)
                tool_name = tool_call.function.name
                available_tools = [t["function"]["name"] for t in self.tools.get_tools_config()]
                if tool_name in available_tools:
                    logger.info(f"Executing tool {tool_name} with args {args}")
                    tool_result = await self.tools.execute_tool(
                        tool_name,
                        args,
                        self
                    )
                    if tool_result:
                        print("tool_result: ", tool_result)
                        if 'image_url' in tool_result:
                            image_url = tool_result['image_url']
                        if 'result' in tool_result:
                            text_response += f"\n{tool_result['result']}"
                        if 'tool_call' in tool_result:
                            tool_back = tool_result['tool_call']
                else:
                    logger.info(f"Tool {tool_name} not found in tools config")
                    tool_back = json.dumps({
                        "tool_call": tool_name,
                        "processed": False,
                        "args": args
                    }, default=str)  # default=str handles any non-JSON serializable objects
            
            if not skip_embedding:
                #moved to post post processing as it is not relevant until finished processing
                # Create MessageData for incoming message
                message_data = MessageData(
                    message=message,
                    embedding=message_embedding,
                    timestamp=datetime.now().isoformat(),
                    message_type=message_type,
                    chat_id=chat_id,
                    source_interface=source_interface,
                    original_query=None,
                    original_embedding=None,
                    response_type=None,
                    key_topics=None, 
                    tool_call=None
                )
                
                # Store the incoming message
                self.message_store.add_message(message_data)
                logger.info("Stored message and embedding in database")
                # Create and store MessageData for the response
                response_data = MessageData(
                    message=text_response,
                    embedding=get_embedding(text_response),
                    timestamp=datetime.now().isoformat(),
                    message_type="agent_response",
                    chat_id=chat_id,
                    source_interface=source_interface,
                    original_query=message,
                    original_embedding=message_embedding,
                    response_type=await self._classify_response_type(text_response),
                    key_topics=await self._extract_key_topics(text_response),
                    tool_call=tool_back
                )
                
                # Store the response
                self.message_store.add_message(response_data)
            
            # Notify other interfaces if needed
            # if source_interface and chat_id:
            #     for interface_name, interface in self.interfaces.items():
            #         if interface_name != source_interface:
            #             await self.send_to_interface(interface_name, {
            #                 'type': 'message',
            #                 'content': text_response,
            #                 'image_url': image_url,
            #                 'source': source_interface,
            #                 'chat_id': chat_id
            #             })
            
            return text_response, image_url, tool_back
            
        except LLMError as e:
            logger.error(f"LLM processing failed: {str(e)}")
            return "Sorry, I encountered an error processing your message.", None, None
        except Exception as e:
            logger.error(f"Message handling failed: {str(e)}")
            return "Sorry, something went wrong.", None, None
        
    async def agent_cot(self, message: str, user: str = "User", display_name: str = None, chat_id: str = "General", source_interface: str = "None", final_format_prompt: str = "") -> str:
        message_info = message,
        username = user or "Unknown"
        display_name = display_name or username
        message_data = message
        chat_id = chat_id
        message_info = f"User: {display_name}, Username: {username}, \nMessage: {message_data}"
        image_url_final = None

        steps_responses = []
        prompt_final = ""
        text_response = ""
        try:
            print("USING COT")
            prompt = f"""<SYSTEM_PROMPT> I want you to give analyze the question {message_info}. 
                    IMPORTANT: DON'T USE TOOLS RIGHT NOW. ANALYZE AND Give me a list of steps with the tools you'd use in each step, if the step is not a specific tool you have to use, just put the tool name as "None". 
                    The most important thing to tell me is what different calls you'd do or processes as a list. Your answer should be a valid JSON and ONLY the JSON.
                    Make sure you analyze what outputs from previous steps you'd need to use in the next step if applicable.
                    IMPORTANT: RETURN THE JSON ONLY.
                    IMPORTANT: DO NOT USE TOOLS.
                    IMPORTANT: ONLY USE VALID TOOLS."""
            
            prompt += """
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
            text_response, _, _ = await self.handle_message(
                message=message_info,
                system_prompt=prompt,
                source_interface=source_interface,
                chat_id=chat_id,
                skip_pre_validation=True,
                skip_conversation_context=False,
                skip_tools=False
            )

            json_response = json.loads(text_response)
            print("json_response: ", json_response)
            thinking_text = "Thinking...\n\n"
            for step in json_response:
                if step['step'] != "None":
                    thinking_text = f"Step: {step['step']}\n"
                    print("\nthinking_text: ", thinking_text)

            for step in json_response:
                print("step: ", step)
                system_prompt = f"""CONTEXT: YOU ARE RUNNING STEPS FOR THE ORIGINAL QUESTION: {message_data}.
                PREVIOUS STEP RESPONSES: {steps_responses}"""
                skip_tools = False
                skip_conversation_context = True
                if step['tool'] == "None":
                    skip_tools = True
                    skip_conversation_context = False

                text_response, image_url, tool_calls = await self.handle_message(
                    system_prompt=system_prompt,
                    message=str(step),
                    message_type="REASONING_STEP",
                    source_interface=source_interface,
                    skip_conversation_context=skip_conversation_context,
                    skip_embedding=True,
                    skip_pre_validation=True,
                    skip_tools=skip_tools,
                    tool_choice="required" if not skip_tools else None
                )
                retries = 5
                while retries > 0:
                    if "<function" in text_response or (not tool_calls and step['tool'] != "None"):
                        print("Found function in text_response or failed to call tool")
                        text_response, image_url, tool_calls = await self.handle_message(
                            system_prompt=text_response,
                            message=str(text_response),
                            message_type="REASONING_STEP",
                            source_interface=source_interface,
                            skip_conversation_context=True,
                            skip_similar=True,
                            skip_embedding=True,
                            skip_pre_validation=True,
                            skip_tools=False,
                            tool_choice="required"
                        )
                        retries -= 1
                        await asyncio.sleep(5)
                    else:
                        break
                step_response = {
                    "step": step,
                    "response": text_response
                }
                print("image_url: ", image_url)
                if image_url:
                    image_url_final = image_url
                steps_responses.append(step_response)
                
            print("steps_responses: ", steps_responses)
            print("image_url_final: ", image_url_final)
            prompt_final = f""" <REASONING_CONTEXT> {message_data}\n
                                    ONLY USE THE REASONING CONTEXT IF YOU NEED TO.
                                    <STEPS_RESPONSES> 
                                        {steps_responses}
                                    </STEPS_RESPONSES>
                                </REASONING_CONTEXT>"""
        except Exception as e:
            logger.error(f"Error processing reply: {str(e)}")
            text_response, image_url, _ = await self.handle_message(
                message_info,
                source_interface=source_interface,
                chat_id=chat_id,
                skip_conversation_context=False,
                skip_pre_validation=True
            )
        try:
            message_final = f"User: {display_name}, Username: {username}, \nMessage: {message_data}"
            prompt_final += f"Generate the final response for the user. Given the context of your reasoning, and the steps you've taken, generate a final response for the user. {text_response}"
            if final_format_prompt:
                prompt_final += final_format_prompt
            else:
                prompt_final += self.basic_personality_settings()
            response, _, _ = await self.handle_message(
                message=message_final,
                system_prompt=prompt_final,
                source_interface=source_interface,
                chat_id=chat_id,
                skip_embedding=False,
                skip_conversation_context=False,
                skip_pre_validation=True,
                skip_tools=True #skip tools as tools should have been called already
            )
            return response, image_url_final, None
        except Exception as e:
            logger.error(f"Error processing reply: {str(e)}")
            return None, None
    def get_knowledge_base(self, message: str, message_embedding: List[float]) -> str:
        """
        Get knowledge base data from the message embedding
        """
        if message_embedding is None:
            message_embedding = get_embedding(message)
        system_prompt_context = ""
        knowledge_base_data = self.message_store.find_similar_messages(
                message_embedding, 
                threshold=0.6,
                message_type="knowledge_base"            
            )
        logger.info(f"Found {len(knowledge_base_data)} relevant items from knowledge base")
        if knowledge_base_data:
            system_prompt_context = "\n\nConsider the Following As Facts and use them to answer the question if applicable and relevant:\nKnowledge base data:\n"
            for data in knowledge_base_data:
                system_prompt_context += f"{data['message']}\n"
        return system_prompt_context
    
    
    def get_conversation_context(self, chat_id: str) -> str:
        """
        Get conversation context from the chat ID
        """
        if chat_id is None:
            return ""
        system_prompt_conversation_context = "\n\nPrevious conversation history (in chronological order):\n"
        # Get last 10 messages (will be in DESC order)
        conversation_messages = self.message_store.find_messages(
            message_type="agent_response",
            chat_id=chat_id,
            limit=10
        )
        
        # Sort by timestamp and reverse to get chronological order
        conversation_messages.sort(key=lambda x: x['timestamp'], reverse=True)
        conversation_messages.reverse()
        
        # Build conversation history
        for msg in conversation_messages:
            if msg.get('original_query'):  # Ensure we have both question and answer
                system_prompt_conversation_context += f"User: {msg['original_query']}\n"
                system_prompt_conversation_context += f"Assistant: {msg['message']}\n\n"
        #print("system_prompt_conversation_context: ", system_prompt_conversation_context)
        return system_prompt_conversation_context

    def get_similar_messages(self, message: str, message_embedding: List[float], message_type: str = None, chat_id: str = None) -> List[Dict[str, Any]]:
        """
        Get similar messages from the message embedding
        """
        if message_embedding is None:
            message_embedding = get_embedding(message)
        similar_messages = self.message_store.find_similar_messages(
                    message_embedding, 
                    threshold=0.9,
                    message_type=message_type,
                    chat_id=chat_id        
                )
        logger.info(f"Found {len(similar_messages)} similar messages")
        if similar_messages:
            context = "\n\nRelated previous conversations and responses\nNOTE: Please provide a response that differs from these recent replies, don't use the same words:\n"
            seen_responses = set()  # Track unique responses
            message_count = 0
            for similar_msg in similar_messages:
                # Find the agent's response where this similar message was the original_query
                agent_responses = self.message_store.find_messages(
                    message_type='agent_response',
                    original_query=similar_msg['message'])

                for response in agent_responses:
                    if response['message'] in seen_responses:
                        continue
                    seen_responses.add(response['message'])
                    context += f"""
                        Previous similar question: {similar_msg['message']}
                        My response: {response['message']}
                        Similarity score: {similar_msg.get('similarity', 0):.2f}
                        """
                    message_count += 1
                    if message_count >= 10:  # Check limit after adding each message
                        break
            context += "\nConsider the above responses for context, but provide a fresh perspective that adds value to the conversation, don't repeat the same responses.\n"
            return context
        else:
            return ""



    logger.info("Added context from similar conversations")

    async def _classify_response_type(self, response: str) -> str:
        """Classify the type of response (factual, opinion, question, etc.)"""
        classify_prompt = {
            "role": "system",
            "content": "Classify this response as one of: FACTUAL, OPINION, QUESTION, EMOTIONAL, ACTION. Response:"
        }
        try:
            classification = await call_llm(
                HEURIST_BASE_URL,
                HEURIST_API_KEY,
                SMALL_MODEL_ID,  # Use smaller model for classification
                system_prompt=classify_prompt["content"],
                user_prompt=response,
                temperature=0.3
            )
            return classification.strip().upper()
        except:
            return "general"

    async def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from the response for better similarity matching"""
        topic_prompt = {
            "role": "system",
            "content": "Extract 2-3 main topics from this text as comma-separated keywords:"
        }
        try:
            topics = await call_llm(
                HEURIST_BASE_URL,
                HEURIST_API_KEY,
                SMALL_MODEL_ID,
                system_prompt=topic_prompt["content"],
                user_prompt=text,
                temperature=0.3
            )
            return [t.strip() for t in topics.split(',')]
        except:
            return []

    async def send_to_interface(self, target_interface: str, message: dict):
        """
        Send a message to a specific interface
        
        Args:
            target_interface (str): Name of the interface to send to
            message (dict): Message data containing at minimum:
                {
                    'type': str,  # Type of message (e.g., 'message', 'image', 'voice')
                    'content': str,  # Main content
                    'image_url': Optional[str],  # Optional image URL
                    'source': Optional[str]  # Source interface name
                }
        
        Returns:
            bool: True if message was queued successfully, False otherwise
        """
        try:
            with self._lock:
                if target_interface not in self.interfaces:
                    logger.error(f"Interface {target_interface} not registered")
                    return False
                
                # Validate message format
                if not isinstance(message, dict) or 'type' not in message or 'content' not in message:
                    logger.error("Invalid message format")
                    return False
                
                # Add timestamp and target
                message['timestamp'] = datetime.now().isoformat()
                message['target'] = target_interface
                
                # Queue the message
                self._message_queue.put(message)
                
                # Get interface instance
                interface = self.interfaces[target_interface]
                logger.info(f"Interface: {interface}")
                logger.info(f"Message: {message}")
                logger.info("trying to send message")
                # Handle different message types
                logger.info(f"Message type: {message['type']}")
                if message['type'] == 'message':
                    logger.info(f"interface has method {hasattr(interface, 'send_message')}")
                    if hasattr(interface, 'send_message'):
                        try:
                            logger.info(f"Attempting to send message via {target_interface} interface")
                            await interface.send_message(
                                chat_id=message['chat_id'],
                                message=message['content'],
                                image_url=message['image_url']
                            )
                            logger.info("Message sent successfully")
                        except Exception as e:
                            logger.error(f"Failed to send message via {target_interface}: {str(e)}")
                            raise
                # Log successful queue
                logger.info(f"Message queued for {target_interface}: {message['type']}")
                return True
                
        except Exception as e:
            logger.error(f"Error sending message to {target_interface}: {str(e)}")
            return False
