import asyncio
import os
import sys
from importlib import import_module
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))

TwitterInfoAgent = import_module("mesh.agents.twitter_info_agent").TwitterInfoAgent


PROFILE = {
    "id": "42",
    "username": "xquikcom",
    "name": "Xquik",
    "description": "X automation API",
    "followers": 1200,
    "following": 100,
    "verified": True,
    "createdAt": "2026-05-01T00:00:00Z",
}

MAIN_TWEET = {
    "id": "1234567890",
    "text": "Xquik timeline item",
    "createdAt": "2026-05-16T12:00:00Z",
    "url": "https://x.com/xquikcom/status/1234567890",
    "likeCount": 4,
    "retweetCount": 2,
    "replyCount": 1,
    "quoteCount": 0,
    "viewCount": 100,
    "author": PROFILE,
}


async def run_xquik_agent_examples() -> dict:
    os.environ.pop("APIDANCE_API_KEY", None)
    os.environ.pop("APIFY_API_KEY", None)
    os.environ["XQUIK_API_KEY"] = "test-xquik-key"

    agent = TwitterInfoAgent()
    requests = []

    async def fake_xquik_request(path: str, params: dict | None = None) -> dict:
        requests.append((path, params))
        if path == "/x/users/xquikcom":
            return PROFILE
        if path == "/x/users/xquikcom/tweets":
            return {"tweets": [MAIN_TWEET], "has_next_page": False, "next_cursor": ""}
        if path == "/x/tweets/search":
            return {"tweets": [MAIN_TWEET], "has_next_page": False, "next_cursor": ""}
        if path == "/x/tweets/1234567890":
            return {"tweet": MAIN_TWEET, "author": PROFILE}
        if path == "/x/tweets/1234567890/thread":
            return {
                "tweets": [
                    MAIN_TWEET,
                    {
                        **MAIN_TWEET,
                        "id": "1234567891",
                        "text": "Thread follow-up",
                        "url": "https://x.com/xquikcom/status/1234567891",
                    },
                ],
                "has_next_page": False,
                "next_cursor": "",
            }
        if path == "/x/tweets/1234567890/replies":
            return {
                "tweets": [
                    {
                        **MAIN_TWEET,
                        "id": "1234567892",
                        "text": "Reply item",
                        "url": "https://x.com/xquikcom/status/1234567892",
                        "isReply": True,
                    }
                ],
                "has_next_page": False,
                "next_cursor": "",
            }
        return {"error": f"Unexpected Xquik path: {path}"}

    agent._xquik_request = fake_xquik_request

    test_cases = {
        "xquik_user_tweets": {
            "tool": "get_user_tweets",
            "tool_arguments": {"username": "xquikcom", "limit": 5},
        },
        "xquik_search": {
            "tool": "get_general_search",
            "tool_arguments": {"q": "xquik", "limit": 5},
        },
        "xquik_tweet_detail": {
            "tool": "get_twitter_detail",
            "tool_arguments": {"tweet_id": "1234567890"},
        },
    }

    results = {}
    for name, params in test_cases.items():
        output = await agent.handle_message(params)
        results[name] = {"input": params, "output": output}

    timeline = results["xquik_user_tweets"]["output"]["data"]["twitter_data"]
    assert timeline["profile"]["screen_name"] == "xquikcom"
    assert timeline["tweets"][0]["author"]["username"] == "xquikcom"
    assert ("/x/users/xquikcom/tweets", {"includeReplies": "false", "limit": 5}) in requests
    assert results["xquik_search"]["output"]["data"]["search_data"]["result_count"] == 1
    assert results["xquik_tweet_detail"]["output"]["data"]["tweet_data"]["thread_tweets"][0]["id"] == "1234567891"

    return results


if __name__ == "__main__":
    example_results = asyncio.run(run_xquik_agent_examples())
    output_path = Path(__file__).with_name("twitter_info_agent_xquik_example.yaml")
    output_path.write_text(yaml.safe_dump(example_results, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Saved {output_path}")
