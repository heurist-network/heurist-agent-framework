# test_deep_research_agent.py
"""Test suite for Deep Research Agent"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.deep_research_agent import DeepResearchAgent
from mesh.tests._test_agents import test_agent

# Define test cases - exact conversion from original file
TEST_CASES = {
    "zero_knowledge_proofs_research": {
        "input": {
            "query": "What are the latest developments in zero knowledge proofs?",
            "depth": 2,
            "breadth": 3,
            "concurrency": 9,
        },
        "description": "Deep research query on zero knowledge proofs with specific depth, breadth, and concurrency parameters",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(DeepResearchAgent, TEST_CASES))
