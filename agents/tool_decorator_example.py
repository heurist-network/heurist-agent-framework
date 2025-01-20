import sys
from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from agents.tool_decorator import tool

@tool("Add two integers together")
def add(a: int, b: int) -> int:
    """Add two integers."""
    result = a + b
    return {"result": result}

@tool("Multiply two integers together")
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    result = a * b
    return {"result": result}

@tool("Filter messages based on content relevance")
def filter_message(should_ignore: bool) -> bool:
    """Determine if a message should be ignored based on the following rules:
    Return TRUE (ignore message) if:
        - Message does not mention Heuman
        - Message does not mention 'start raid'
        - Message does not discuss: The Wired, Consciousness, Reality, Existence, Self, Philosophy, Technology, Crypto, AI, Machines
        - For image requests: ignore if Heuman is not specifically mentioned
    
    Return FALSE (process message) only if:
        - Message explicitly mentions Heuman
        - Message contains 'start raid'
        - Message clearly discusses any of the listed topics
        - Image request contains Heuman
    
    If in doubt, return TRUE to ignore the message."""
    return should_ignore

# List of available decorated tools
DECORATED_TOOLS_EXAMPLES = [
    add,
    multiply,
    #filter_message
]