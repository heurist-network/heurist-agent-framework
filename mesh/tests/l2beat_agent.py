import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.l2beat_agent import L2BeatAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Natural language tests
    "tvl_growth_analysis": {
        "input": {
            "query": "Show me the Layer 2 rollups with highest TVL growth in the last day. Which ones are gaining the most traction?",
            "raw_data_only": False,
        },
        "description": "TVL and growth analysis for Layer 2 rollups",
    },
    "security_stage_comparison": {
        "input": {
            "query": "Compare Stage 0 vs Stage 1 rollups. Which ZK rollups offer the best security guarantees currently?",
            "raw_data_only": False,
        },
        "description": "Security and stage comparison between rollup types",
    },
    "cost_efficiency_analysis": {
        "input": {
            "query": "Which Layer 2 solutions offer the most cost-effective transactions for DeFi users? Compare gas fees across different rollup types.",
            "raw_data_only": False,
        },
        "description": "Cost efficiency analysis for Layer 2 solutions",
    },
    # Tool call tests
    "rollups_summary_default": {
        "input": {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "rollups"},
        },
        "description": "Default rollups summary via direct tool call",
    },
    "validiums_summary": {
        "input": {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        },
        "description": "Validiums and optimiums summary via direct tool call",
    },
    "rollups_costs": {
        "input": {
            "tool": "get_l2_costs",
            "tool_arguments": {"category": "rollups"},
        },
        "description": "Rollups transaction costs via direct tool call",
    },
    "validiums_costs": {
        "input": {
            "tool": "get_l2_costs",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        },
        "description": "Validiums transaction costs via direct tool call",
    },
    "summary_empty_args": {
        "input": {
            "tool": "get_l2_summary",
            "tool_arguments": {},
        },
        "description": "Summary with empty args (should default to rollups)",
    },
    "costs_empty_args": {
        "input": {
            "tool": "get_l2_costs",
            "tool_arguments": {},
        },
        "description": "Costs with empty args (should default to rollups)",
    },
    "rollups_summary_cached": {
        "input": {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "rollups"},
        },
        "description": "Rollups summary (duplicate to test caching)",
    },
    "validiums_costs_cached": {
        "input": {
            "tool": "get_l2_costs",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        },
        "description": "Validiums costs (duplicate to test caching)",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(L2BeatAgent, TEST_CASES))
