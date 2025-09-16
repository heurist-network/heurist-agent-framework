import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.metasleuth_sol_token_wallet_cluster_agent import MetaSleuthSolTokenWalletClusterAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "direct_token_clusters": {
        "input": {
            "tool": "fetch_token_clusters",
            "tool_arguments": {"address": "tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump", "page": 1, "page_size": 10},
            "raw_data_only": True,
        },
        "description": "Direct tool call to fetch token clusters with pagination",
    },
    "direct_cluster_details": {
        "input": {
            "tool": "fetch_cluster_details",
            "tool_arguments": {"cluster_uuid": "13axGrDoFlaj8E0ruhYfi1", "page": 1, "page_size": 10},
            "raw_data_only": True,
        },
        "description": "Direct tool call to fetch cluster details with pagination",
    },
    "nl_token_analysis": {
        "input": {
            "query": "Analyze the wallet clusters of this Solana token: tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump",
            "raw_data_only": False,
        },
        "description": "Natural language query for token wallet cluster analysis",
    },
    "nl_cluster_details": {
        "input": {
            "query": "Show me the details of wallet cluster with UUID 0j7eWWwixWixBYPg5oeVX6",
            "raw_data_only": False,
        },
        "description": "Natural language query for specific cluster details",
    },
    "raw_data_query": {
        "input": {
            "query": "Get token cluster data for tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump",
            "raw_data_only": True,
        },
        "description": "Natural language query with raw data flag for token clusters",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(MetaSleuthSolTokenWalletClusterAgent, TEST_CASES))
