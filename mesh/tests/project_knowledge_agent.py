import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.project_knowledge_agent import ProjectKnowledgeAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Natural language queries
    "natural_language_uniswap": {
        "input": {"query": "Tell me about Uniswap"},
        "description": "Natural language query for Uniswap - has 11 investors with logos",
    },
    "natural_language_arbitrum": {
        "input": {"query": "What is Arbitrum and who invested in it?"},
        "description": "Natural language query about Arbitrum investors - has 10 investors with logos",
    },
    # Direct tool calls - get_project by name
    "get_project_by_name": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {"name": "Aave"},
            "raw_data_only": True,
        },
        "description": "Get Aave by name - has 6 investors with logos, verify logo_url in response",
    },
    "get_project_by_name_ripple": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {"name": "Ripple"},
            "raw_data_only": True,
        },
        "description": "Get Ripple by name - has 29 investors with logos, verify structured investor data",
    },
    # Direct tool calls - get_project by symbol
    "get_project_by_symbol": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {"symbol": "UNI"},
            "raw_data_only": True,
        },
        "description": "Get Uniswap by symbol - verify project logo_url and investor logo_urls",
    },
    # Direct tool calls - get_project by x_handle
    "get_project_by_x_handle": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {"x_handle": "@ethereum"},
            "raw_data_only": True,
        },
        "description": "Get Ethereum by X handle",
    },
    # Semantic search
    "semantic_search_defi": {
        "input": {
            "tool": "semantic_search_projects",
            "tool_arguments": {"query": "DeFi projects funded by Paradigm", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Semantic search for DeFi projects funded by Paradigm",
    },
    "semantic_search_ai": {
        "input": {
            "tool": "semantic_search_projects",
            "tool_arguments": {"query": "AI projects listed on Binance", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Semantic search for AI projects on Binance",
    },
    # Edge cases
    "get_project_not_found": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {"name": "ThisProjectDoesNotExist12345"},
            "raw_data_only": True,
        },
        "description": "Get non-existent project - should return not found",
    },
    "get_project_empty_args": {
        "input": {
            "tool": "get_project",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "description": "Get project with empty arguments - should return error",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ProjectKnowledgeAgent, TEST_CASES))
