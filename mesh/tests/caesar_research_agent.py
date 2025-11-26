import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.caesar_research_agent import CaesarResearchAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "heurist_mesh_query": {
        "input": {
            "query": "What is Heurist Mesh?",
            "raw_data_only": False,
        },
        "description": "Research query about Heurist Mesh platform and ecosystem",
    },
    "x402_vending_machine": {
        "input": {
            "query": "What is x402-vending machine by Heurist Mesh?",
            "raw_data_only": True,
        },
        "description": "Research query about x402-vending machine system with raw data",
    },
    "heurist_ai_infrastructure": {
        "input": {
            "tool": "caesar_research",
            "tool_arguments": {"query": "How does Heurist decentralized AI infrastructure work?"},
        },
        "description": "Direct tool call researching Heurist's decentralized AI infrastructure",
    },
    "ai_agent_frameworks": {
        "input": {
            "query": "What are the latest developments in AI agent frameworks and autonomous agents?",
            "raw_data_only": False,
        },
        "description": "Research on modern AI agent frameworks and autonomous systems",
    },
    "blockchain_ai_integration": {
        "input": {
            "query": "How are blockchain and AI being integrated in decentralized systems?",
            "raw_data_only": True,
        },
        "description": "Research on blockchain and AI integration with raw results",
    },
    "zero_knowledge_proofs": {
        "input": {
            "tool": "caesar_research",
            "tool_arguments": {
                "query": "What are zero-knowledge proofs and their applications in privacy-preserving AI?"
            },
        },
        "description": "Direct tool call researching zero-knowledge proofs in AI applications",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(CaesarResearchAgent, TEST_CASES))
