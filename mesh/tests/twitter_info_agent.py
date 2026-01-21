import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.twitter_info_agent import TwitterInfoAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Tweet detail functionality
    "tweet_detail_1": {
        "input": {
            "tool": "get_twitter_detail",
            "tool_arguments": {"tweet_id": "1913624766793289972"},
        },
        "description": "Direct tool call to get tweet details for first test tweet",
    },
    "tweet_detail_2": {
        "input": {
            "tool": "get_twitter_detail",
            "tool_arguments": {"tweet_id": "1914394032169762877"},
        },
        "description": "Direct tool call to get tweet details for second test tweet",
    },
    # X Article functionality - Tweet with article content
    "article_direct_link": {
        "input": {
            "tool": "get_twitter_detail",
            "tool_arguments": {"tweet_id": "2012208491578950089"},
        },
        "description": "Direct article link - WalletConnect Pay Is Available Worldwide",
    },
    "article_embedded_in_post": {
        "input": {
            "tool": "get_twitter_detail",
            "tool_arguments": {"tweet_id": "2013381978544894043"},
        },
        "description": "Article embedded in a post - The Future of Payments",
    },
    # General search functionality
    "search_heurist_ai": {
        "input": {
            "tool": "get_general_search",
            "tool_arguments": {"q": "heurist ai"},
        },
        "description": "Direct tool call to search for 'heurist ai'",
    },
    "search_eth": {
        "input": {
            "tool": "get_general_search",
            "tool_arguments": {"q": "eth"},
        },
        "description": "Direct tool call to search for 'eth' hashtag",
    },
    "search_anthropic_mcp": {
        "input": {
            "tool": "get_general_search",
            "tool_arguments": {"q": "Anthropic MCP", "cursor": ""},
        },
        "description": "Direct tool call to search for 'Anthropic MCP' with pagination cursor",
    },
    # Natural language queries for search
    "crypto_marketplace_query": {
        "input": {"query": "Search for tweets about crypto marketplace"},
        "description": "Natural language query to search for crypto marketplace tweets",
    },
    "heurist_discussions_query": {
        "input": {"query": "Find recent discussions about Heurist AI"},
        "description": "Natural language query to find recent Heurist AI discussions",
    },
    "vitalik_query": {
        "input": {"query": "What are people saying about Vitalik Buterin?"},
        "description": "Natural language query about Vitalik Buterin discussions",
    },
    # User tweets functionality
    "heurist_ai_updates": {
        "input": {"query": "Summarise recent updates of @heurist_ai", "limit": 5},
        "description": "Natural language query to summarize @heurist_ai recent updates",
    },
    "elon_musk_tweets": {
        "input": {"query": "What has @elonmusk been tweeting lately?", "limit": 5},
        "description": "Natural language query for @elonmusk recent tweets",
    },
    "cz_binance_tweets": {
        "input": {"query": "Get the recent tweets from cz_binance", "limit": 5},
        "description": "Natural language query for cz_binance recent tweets",
    },
    "heurist_ai_details": {
        "input": {"query": "Give me details of heurist_ai"},
        "description": "Natural language query for heurist_ai account details",
    },
    "elonmusk_updates": {
        "input": {"query": "Show the latest updates from elonmusk"},
        "description": "Natural language query for elonmusk latest updates",
    },
    "vitalik_posts": {
        "input": {"query": "What vitalikbuterin has been posting about?"},
        "description": "Natural language query about vitalikbuterin posts",
    },
    "jack_info": {
        "input": {"query": "can you get me info about @jack"},
        "description": "Natural language query for @jack account information",
    },
    "naval_twitter_url": {
        "input": {"query": "twitter.com/naval"},
        "description": "Natural language query using twitter.com URL format",
    },
    "pmarca_x_url": {
        "input": {"query": "x.com/pmarca"},
        "description": "Natural language query using x.com URL format",
    },
    "trump_tweets_query": {
        "input": {"query": "I want to see realdonaldtrump's tweets"},
        "description": "Natural language query for realdonaldtrump tweets",
    },
    "naval_profile": {
        "input": {"query": "Check out the profile for naval's account"},
        "description": "Natural language query to check naval's profile",
    },
    # Direct tool calls
    "trump_tweets_direct": {
        "input": {
            "tool": "get_user_tweets",
            "tool_arguments": {"username": "realdonaldtrump", "limit": 5},
        },
        "description": "Direct tool call to get realdonaldtrump tweets with limit 5",
    },
    "user_id_query": {
        "input": {"query": "Get tweets from user_id:778764142412984320", "limit": 5},
        "description": "Natural language query using numeric user ID",
    },
    # Tweet detail queries
    "tweet_details_query_1": {
        "input": {"query": "Show me the details and replies for tweet 1913624766793289972"},
        "description": "Natural language query for tweet details and replies",
    },
    "tweet_info_query_2": {
        "input": {"query": "Get all information about this tweet: 1914394032169762877"},
        "description": "Natural language query for comprehensive tweet information",
    },
    # Search queries
    "ethereum_search": {
        "input": {
            "tool": "get_general_search",
            "tool_arguments": {"q": "ethereum"},
        },
        "description": "Direct tool call to search for 'ethereum'",
    },
    "heurist_ai_search": {
        "input": {"query": "Search Twitter for discussions about Heurist AI"},
        "description": "Natural language query to search Twitter for Heurist AI discussions",
    },
    "heurist_ai_sentiment": {
        "input": {"query": "What are people saying about Heurist AI on Twitter?"},
        "description": "Natural language query for Heurist AI sentiment on Twitter",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(TwitterInfoAgent, TEST_CASES))
