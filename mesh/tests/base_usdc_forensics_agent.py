import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.base_usdc_forensics_agent import BaseUSDCForensicsAgent
from mesh.tests._test_agents import test_agent

PRIMARY_ADDRESS = "0x7d9d1821d15b9e0b8ab98a058361233e255e405d"
SECONDARY_ADDRESS = "0xb2f1c3beb9c4c4bb7fe8e55a9751603c2a3c0e54"

TEST_CASES = {
    "basic_profile_natural": {
        "input": {
            "query": f"Show me the USDC profile for {PRIMARY_ADDRESS}",
            "raw_data_only": False,
        },
        "description": "Natural language query for basic USDC profile",
    },
    "basic_profile_direct": {
        "input": {
            "tool": "usdc_basic_profile",
            "tool_arguments": {"address": PRIMARY_ADDRESS},
        },
        "description": "Direct tool call for USDC basic profile",
    },
    "top_funders_natural": {
        "input": {
            "query": f"Who are the top USDC funders for {PRIMARY_ADDRESS}?",
            "raw_data_only": False,
        },
        "description": "Natural language query for top USDC funders",
    },
    "top_funders_direct": {
        "input": {
            "tool": "usdc_top_funders",
            "tool_arguments": {"address": PRIMARY_ADDRESS, "limit": 10},
        },
        "description": "Direct tool call for top USDC funders with limit",
    },
    "top_sinks_natural": {
        "input": {
            "query": f"Where does {PRIMARY_ADDRESS} send its USDC?",
            "raw_data_only": False,
        },
        "description": "Natural language query for top USDC sinks",
    },
    "top_sinks_direct": {
        "input": {
            "tool": "usdc_top_sinks",
            "tool_arguments": {"address": PRIMARY_ADDRESS, "limit": 10},
        },
        "description": "Direct tool call for top USDC sinks with limit",
    },
    "net_counterparties_natural": {
        "input": {
            "query": f"Show me the net USDC flow for each counterparty of {PRIMARY_ADDRESS}",
            "raw_data_only": False,
        },
        "description": "Natural language query for net counterparties",
    },
    "net_counterparties_direct": {
        "input": {
            "tool": "usdc_net_counterparties",
            "tool_arguments": {"address": PRIMARY_ADDRESS, "limit": 20},
        },
        "description": "Direct tool call for net counterparties",
    },
    "daily_activity_natural": {
        "input": {
            "query": f"Show daily USDC activity for {PRIMARY_ADDRESS}",
            "raw_data_only": False,
        },
        "description": "Natural language query for daily activity",
    },
    "daily_activity_direct": {
        "input": {
            "tool": "usdc_daily_activity",
            "tool_arguments": {"address": PRIMARY_ADDRESS},
        },
        "description": "Direct tool call for daily activity",
    },
    "hourly_pair_natural": {
        "input": {
            "query": f"Show hourly USDC transfers between {PRIMARY_ADDRESS} and {SECONDARY_ADDRESS}",
            "raw_data_only": False,
        },
        "description": "Natural language query for hourly pair activity",
    },
    "hourly_pair_direct": {
        "input": {
            "tool": "usdc_hourly_pair_activity",
            "tool_arguments": {"address_a": PRIMARY_ADDRESS, "address_b": SECONDARY_ADDRESS},
        },
        "description": "Direct tool call for hourly pair activity",
    },
    "raw_data_only": {
        "input": {
            "tool": "usdc_basic_profile",
            "tool_arguments": {"address": PRIMARY_ADDRESS},
            "raw_data_only": True,
        },
        "description": "Raw data mode test",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(BaseUSDCForensicsAgent, TEST_CASES))
