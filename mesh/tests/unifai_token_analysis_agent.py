import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.unifai_token_analysis_agent import UnifaiTokenAnalysisAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "gmgn_trend_natural": {
        "input": {
            "query": "Show me trending tokens on GMGN for the last 24 hours",
            "raw_data_only": False,
        },
        "description": "Natural language query for GMGN trending tokens in last 24 hours",
    },
    "gmgn_trend_direct": {
        "input": {
            "tool": "get_gmgn_trend",
            "tool_arguments": {"time_window": "4h", "limit": 10},
            "raw_data_only": True,
        },
        "description": "Direct tool call for GMGN trends with 4h window and limit 10",
    },
    "gmgn_token_info_natural": {
        "input": {
            "query": "Get token information for 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 on Ethereum",
            "raw_data_only": False,
        },
        "description": "Natural language query for GMGN token info on Ethereum",
    },
    "gmgn_token_info_direct": {
        "input": {
            "tool": "get_gmgn_token_info",
            "tool_arguments": {
                "chain": "eth",
                "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for GMGN token info (WETH on Ethereum)",
    },
    "token_analysis_natural": {
        "input": {
            "query": "Analyze ETH token for me",
            "raw_data_only": False,
        },
        "description": "Natural language query for ETH token analysis",
    },
    "token_analysis_direct": {
        "input": {
            "tool": "analyze_token",
            "tool_arguments": {"ticker": "BTC"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for BTC token analysis",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(UnifaiTokenAnalysisAgent, TEST_CASES))
