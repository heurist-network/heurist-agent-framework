import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.truth_social_agent import TruthSocialAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "trump_posts_query": {
        "input": {"query": "What has Donald Trump posted recently on Truth Social?"},
        "description": "Natural language query for Donald Trump's recent Truth Social posts",
    },
    "trump_posts_direct": {
        "input": {
            "tool": "get_trump_posts",
            "tool_arguments": {"max_posts": 5},
            "raw_data_only": False,
        },
        "description": "Direct tool call for Trump posts with max 5 posts and formatted response",
    },
    "trump_posts_direct_raw": {
        "input": {
            "tool": "get_trump_posts",
            "tool_arguments": {"max_posts": 5},
            "raw_data_only": True,
        },
        "description": "Direct tool call for Trump posts with max 5 posts and raw data",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(TruthSocialAgent, TEST_CASES))
