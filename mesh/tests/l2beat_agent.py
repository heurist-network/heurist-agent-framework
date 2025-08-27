import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.l2beat_agent import L2BeatAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = L2BeatAgent()
    try:
        # ====================================================================
        # Natural Language Tests (3 different queries)
        # ====================================================================

        # Test 1: TVL and growth analysis
        nl_tvl_input = {
            "query": "Show me the Layer 2 rollups with highest TVL growth in the last day. Which ones are gaining the most traction?",
            "raw_data_only": False,
        }
        nl_tvl_output = await agent.handle_message(nl_tvl_input)

        # Test 2: Security and stage comparison
        nl_security_input = {
            "query": "Compare Stage 0 vs Stage 1 rollups. Which ZK rollups offer the best security guarantees currently?",
            "raw_data_only": False,
        }
        nl_security_output = await agent.handle_message(nl_security_input)

        # Test 3: Cost efficiency analysis
        nl_cost_input = {
            "query": "Which Layer 2 solutions offer the most cost-effective transactions for DeFi users? Compare gas fees across different rollup types.",
            "raw_data_only": False,
        }
        nl_cost_output = await agent.handle_message(nl_cost_input)

        # ====================================================================
        # Tool Call Tests (8 different combinations)
        # ====================================================================

        # Tool 1: Default rollups summary
        tool_1_output = await agent.handle_message(
            {
                "tool": "get_l2_summary",
                "tool_arguments": {"category": "rollups"},
            }
        )

        # Tool 2: Validiums and optimiums summary
        tool_2_output = await agent.handle_message(
            {
                "tool": "get_l2_summary",
                "tool_arguments": {"category": "validiumsAndOptimiums"},
            }
        )

        # Tool 3: Rollups transaction costs
        tool_3_output = await agent.handle_message(
            {
                "tool": "get_l2_costs",
                "tool_arguments": {"category": "rollups"},
            }
        )

        # Tool 4: Validiums transaction costs
        tool_4_output = await agent.handle_message(
            {
                "tool": "get_l2_costs",
                "tool_arguments": {"category": "validiumsAndOptimiums"},
            }
        )

        # Tool 5: Empty args summary (should default to rollups)
        tool_5_output = await agent.handle_message(
            {
                "tool": "get_l2_summary",
                "tool_arguments": {},
            }
        )

        # Tool 6: Empty args costs
        tool_6_output = await agent.handle_message(
            {
                "tool": "get_l2_costs",
                "tool_arguments": {},
            }
        )

        # Tool 7: Rollups summary (duplicate to test caching)
        await asyncio.sleep(1)  # Small delay
        tool_7_output = await agent.handle_message(
            {
                "tool": "get_l2_summary",
                "tool_arguments": {"category": "rollups"},
            }
        )

        # Tool 8: Validiums costs (duplicate to test caching)
        await asyncio.sleep(1)
        tool_8_output = await agent.handle_message(
            {
                "tool": "get_l2_costs",
                "tool_arguments": {"category": "validiumsAndOptimiums"},
            }
        )

        # ====================================================================
        # Save Results
        # ====================================================================
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        output_file = script_dir / f"{current_file}_example.yaml"

        yaml_content = {
            "natural_language_tests": {
                "tvl_growth_analysis": {
                    "input": nl_tvl_input,
                    "output": nl_tvl_output,
                },
                "security_stage_comparison": {
                    "input": nl_security_input,
                    "output": nl_security_output,
                },
                "cost_efficiency_analysis": {
                    "input": nl_cost_input,
                    "output": nl_cost_output,
                },
            },
            "tool_call_tests": {
                "rollups_summary_default": {
                    "input": {"tool": "get_l2_summary", "tool_arguments": {"category": "rollups"}},
                    "output": tool_1_output,
                },
                "validiums_summary": {
                    "input": {"tool": "get_l2_summary", "tool_arguments": {"category": "validiumsAndOptimiums"}},
                    "output": tool_2_output,
                },
                "rollups_costs": {
                    "input": {"tool": "get_l2_costs", "tool_arguments": {"category": "rollups"}},
                    "output": tool_3_output,
                },
                "validiums_costs": {
                    "input": {"tool": "get_l2_costs", "tool_arguments": {"category": "validiumsAndOptimiums"}},
                    "output": tool_4_output,
                },
                "summary_empty_args": {
                    "input": {"tool": "get_l2_summary", "tool_arguments": {}},
                    "output": tool_5_output,
                },
                "costs_empty_args": {
                    "input": {"tool": "get_l2_costs", "tool_arguments": {}},
                    "output": tool_6_output,
                },
                "rollups_summary_cached": {
                    "input": {"tool": "get_l2_summary", "tool_arguments": {"category": "rollups"}},
                    "output": tool_7_output,
                },
                "validiums_costs_cached": {
                    "input": {"tool": "get_l2_costs", "tool_arguments": {"category": "validiumsAndOptimiums"}},
                    "output": tool_8_output,
                },
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False, width=120)

        print(f"Results saved to {output_file}")
    except Exception:
        raise
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
