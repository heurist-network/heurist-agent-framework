import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.elfa_twitter_intelligence_agent import ElfaTwitterIntelligenceAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = ElfaTwitterIntelligenceAgent()
    try:
        # Test with a query for searching mentions
        agent_input_mentions = {"query": "Search for mentions of elonmusk, tesla, and spacex in the last 30 days"}
        print("\nTesting search_mentions with query:", agent_input_mentions["query"])
        agent_output_mentions = await agent.handle_message(agent_input_mentions)
        print(
            f"Result of handle_message (search mentions, endpoint: /v2/data/keyword-mentions):\n{agent_output_mentions}"
        )

        # Test with a query for account analysis
        agent_input_account = {"query": "Analyze the Twitter account @heurist_ai"}
        print("\nTesting search_account with query:", agent_input_account["query"])
        agent_output_account = await agent.handle_message(agent_input_account)
        print(
            f"Result of handle_message (account analysis, endpoint: /v2/account/smart-stats and /v2/data/keyword-mentions):\n{agent_output_account}"
        )

        # Test direct trending tokens tool
        agent_input_trending = {
            "tool": "get_trending_tokens",
            "tool_arguments": {"time_window": "24h"},
            "query": "Get trending tokens for reference",
        }
        print("\nTesting get_trending_tokens with query:", agent_input_trending["query"])
        agent_output_trending = await agent.handle_message(agent_input_trending)
        print(
            f"Result of handle_message (trending tokens direct call, endpoint: /v2/aggregations/trending-tokens):\n{agent_output_trending}"
        )

        # Test Apidance API with get_tweet_detail
        api_dance_test_query1 = {"tweet_id": "1913624766793289972"}  # Replace with a valid tweet ID
        print("\nTesting Apidance API with tweet_id:", api_dance_test_query1["tweet_id"])
        api_dance_output_query1 = await agent.get_tweet_detail(api_dance_test_query1["tweet_id"])
        print(f"Apidance API Response (get_tweet_detail, endpoint: /sapi/TweetDetail):\n{api_dance_output_query1}")

        # Save the test inputs and outputs to a YAML file
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "input_mentions": agent_input_mentions,
            "output_mentions": agent_output_mentions,
            "input_account": agent_input_account,
            "output_account": agent_output_account,
            "input_trending": agent_input_trending,
            "output_trending": agent_output_trending,
            "api_dance_test_query1": api_dance_test_query1,
            "api_dance_output_query1": api_dance_output_query1,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"\nResults saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
