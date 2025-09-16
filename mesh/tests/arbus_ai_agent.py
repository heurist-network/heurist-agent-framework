import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.arbus_agent import ArbusAgent
from mesh.tests._test_agents import test_agent

load_dotenv()

TEST_CASES = {
    "ai_assistant_direct": {
        "input": {
            "tool": "ask_ai_assistant",
            "tool_arguments": {"query": "What's happening with DeFi markets?", "days": 7},
        },
        "description": "Direct AI assistant call for DeFi market analysis",
    },
    "btc_sentiment": {
        "input": {"query": "Is Bitcoin bullish right now?"},
        "description": "Natural language Bitcoin sentiment query",
    },
    "market_sentiment_14days": {
        "input": {"query": "Analyze the current crypto market sentiment over the last 14 days"},
        "description": "14-day market sentiment analysis",
    },
    "ethereum_report": {
        "input": {"tool": "generate_report", "tool_arguments": {"twitter_handle": "ethereum", "category": "projects"}},
        "description": "Generate Ethereum project report",
    },
    "eth_partnerships": {
        "input": {"query": "Generate a report on Ethereum's partnerships"},
        "description": "Natural language query for Ethereum partnerships report",
    },
    "solana_yearly_report": {
        "input": {
            "tool": "generate_report",
            "tool_arguments": {
                "twitter_handle": "solana",
                "category": "projects",
                "date_from": "2024-01-01",
                "date_to": "2024-12-31",
            },
        },
        "description": "Solana project report with date range",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(ArbusAgent, TEST_CASES))
