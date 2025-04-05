"""
Heurist Core - Core components of the Heurist Agent Framework
"""

__version__ = "0.1.0"

# Import and export main modules
# Import and export subpackages
from . import (
    clients,
    components,
    config,
    custom_smolagents,
    embedding,
    heurist_image,
    imgen,
    llm,
    tools,
    utils,
    videogen,
    voice,
    workflows,
)
from .clients import SearchClient
from .config import PromptConfig
from .embedding import MessageData, MessageStore, PostgresVectorStorage, SQLiteVectorStorage, get_embedding
from .imgen import generate_image, generate_image_with_retry_smartgen

# Export commonly used functions and classes directly
from .llm import LLMError, call_llm, call_llm_async, call_llm_with_tools, call_llm_with_tools_async
from .voice import speak_text, transcribe_audio

# Define what's available in the public API
__all__ = [
    # Modules
    "clients",
    "config",
    "embedding",
    "llm",
    "imgen",
    "voice",
    "videogen",
    "custom_smolagents",
    # Subpackages
    "components",
    "tools",
    "utils",
    "workflows",
    "heurist_image",
    # Common functions and classes
    "SearchClient",
    "call_llm",
    "call_llm_async",
    "call_llm_with_tools",
    "call_llm_with_tools_async",
    "LLMError",
    "get_embedding",
    "VectorStorage",
    "SQLiteVectorStorage",
    "PostgresVectorStorage",
    "MessageData",
    "MessageStore",
    "generate_image",
    "generate_image_with_retry_smartgen",
    "speak_text",
    "transcribe_audio",
    "PromptConfig",
]
