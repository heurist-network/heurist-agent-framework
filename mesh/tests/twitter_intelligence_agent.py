import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.twitter_intelligence_agent import TwitterIntelligenceAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # -------------------------
    # Profile + Timeline Tests (verifies description field)
    # -------------------------
    "user_timeline_heurist": {
        "input": {
            "tool": "user_timeline",
            "tool_arguments": {"identifier": "@heurist_ai", "limit": 10},
        },
        "description": "Fetch recent tweets from @heurist_ai (should include profile description)",
    },
    "user_timeline_drhinofficial": {
        "input": {
            "tool": "user_timeline",
            "tool_arguments": {"identifier": "@drhinofficial", "limit": 5},
        },
        "description": "Fetch recent tweets from @drhinofficial (should include profile description)",
    },
    "user_timeline_mattprd": {
        "input": {
            "tool": "user_timeline",
            "tool_arguments": {"identifier": "@MattPRD", "limit": 5},
        },
        "description": "Fetch recent tweets from @MattPRD - CEO/Co-Founder octane.ai (should include profile description)",
    },
    "user_timeline_elonmusk": {
        "input": {
            "tool": "user_timeline",
            "tool_arguments": {"identifier": "@elonmusk", "limit": 5},
        },
        "description": "Fetch recent tweets from @elonmusk (should include profile description)",
    },
    # -------------------------
    # Tweet Detail Tests
    # -------------------------
    "tweet_detail_basic": {
        "input": {
            "tool": "tweet_detail",
            "tool_arguments": {"tweet_id": "1913624766793289972"},
        },
        "description": "Fetch a single tweet detail (basic)",
    },
    "tweet_detail_thread": {
        "input": {
            "tool": "tweet_detail",
            "tool_arguments": {"tweet_id": "1914394032169762877", "show_thread": True, "replies_limit": 10},
        },
        "description": "Fetch tweet detail with thread + top replies",
    },
    # -------------------------
    # Search Tests
    # -------------------------
    "twitter_search_bitcoin": {
        "input": {
            "tool": "twitter_search",
            "tool_arguments": {"queries": ["bitcoin", "$BTC"], "limit": 10},
        },
        "description": "Search for bitcoin related tweets (public + ELFA mentions)",
    },
    # -------------------------
    # Natural Language Query Tests
    # -------------------------
    "nl_profile_mattprd": {
        "input": {"query": "Tell me about @MattPRD's profile and recent activity"},
        "description": "Natural language query to get profile info for @MattPRD",
    },
    "nl_profile_drhinofficial": {
        "input": {"query": "Who is @drhinofficial and what do they tweet about?"},
        "description": "Natural language query to get profile info for @drhinofficial",
    },
    "nl_search": {
        "input": {"query": "Find recent tweets mentioning Bitcoin and summarize the discussion"},
        "description": "Natural language query using twitter_search",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(TwitterIntelligenceAgent, TEST_CASES, delay_seconds=1.0))
