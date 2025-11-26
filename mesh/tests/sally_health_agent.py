import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.sally_health_agent import SallyHealthAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "fitness_query": {
        "input": {
            "query": "How can I stay fit with a work from home routine?",
            "raw_data_only": False,
        },
        "description": "Query about fitness tips for remote workers",
    },
    "heart_health": {
        "input": {
            "query": "What are good foods for heart health?",
            "raw_data_only": True,
        },
        "description": "Query about heart-healthy nutrition with raw data",
    },
    "direct_tool_call": {
        "input": {
            "tool": "ask_health_advice",
            "tool_arguments": {"message": "Tips for better sleep quality"},
        },
        "description": "Direct tool call asking Sally about sleep tips",
    },
    "stress_management": {
        "input": {
            "tool": "ask_health_advice",
            "tool_arguments": {"message": "How to manage stress naturally?"},
        },
        "description": "Direct tool call asking Sally about stress management",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(SallyHealthAgent, TEST_CASES))
