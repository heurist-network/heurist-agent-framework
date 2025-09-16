import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.memory_agent import MemoryAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "natural_language_store": {
        "input": {
            "query": "Save our conversation to memory. We discussed about Imagine not having much users.",
            "raw_data_only": False,
            "session_context": {"api_key": "xxxxxx-xxxxxxx"},
        },
        "description": "Natural language query to store conversation with session context",
    },
    "direct_store_with_metadata": {
        "input": {
            "tool": "store_conversation",
            "tool_arguments": {
                "content": "User asked about NFT marketplace development. Explained ERC-721 standards, IPFS storage, and smart contract deployment.",
                "metadata": {"platform": "discord", "topic": "NFTs", "sentiment": "educational"},
            },
            "session_context": {"api_key": "xxxxxx-xxxxxxx"},
        },
        "description": "Direct tool call to store conversation with metadata",
    },
    "natural_language_retrieve": {
        "input": {
            "query": "What did we talk about in our previous conversations?",
            "raw_data_only": False,
            "session_context": {"api_key": "xxxxxx-xxxxxxx"},
        },
        "description": "Natural language query to retrieve previous conversations",
    },
    "direct_retrieve": {
        "input": {
            "tool": "retrieve_conversations",
            "tool_arguments": {"limit": 5},
            "session_context": {"api_key": "xxxxxx-xxxxxxx"},
        },
        "description": "Direct tool call to retrieve conversations with limit",
    },
    "raw_data_query": {
        "input": {
            "query": "Show me all stored conversations",
            "raw_data_only": False,
            "session_context": {"api_key": "xxxxxx-xxxxxxx"},
        },
        "description": "Natural language query for all stored conversations",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(MemoryAgent, TEST_CASES))
