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
        print("Starting L2Beat Agent tests with extended features...\n")

        # ====================================================================
        # Test 1: L2 Summary - Rollups (Default)
        # ====================================================================
        print("Test 1: L2 Summary for Rollups (default category)")
        rollups_summary_input = {
            "query": "What's the current TVL and market share of the top Layer 2 Rollups?",
            "raw_data_only": False,
        }
        rollups_summary_output = await agent.handle_message(rollups_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 2: L2 Summary - Validiums and Optimiums
        # ====================================================================
        print("Test 2: L2 Summary for Validiums and Optimiums")
        validiums_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        }
        validiums_summary_output = await agent.handle_message(validiums_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 3: L2 Summary - Others
        # ====================================================================
        print("Test 3: L2 Summary for Other L2s")
        others_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "others"},
        }
        others_summary_output = await agent.handle_message(others_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 4: L2 Summary - Not Reviewed
        # ====================================================================
        print("Test 4: L2 Summary for Not Reviewed L2s")
        not_reviewed_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "notReviewed"},
        }
        not_reviewed_summary_output = await agent.handle_message(not_reviewed_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 5: L2 Activity - Rollups (Natural Language)
        # ====================================================================
        print("Test 5: L2 Activity for Rollups (natural language)")
        rollups_activity_input = {
            "query": "Show me the transaction activity comparison between Arbitrum, Optimism, and Base",
            "raw_data_only": False,
        }
        rollups_activity_output = await agent.handle_message(rollups_activity_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 6: L2 Activity - Validiums and Optimiums
        # ====================================================================
        print("Test 6: L2 Activity for Validiums and Optimiums")
        validiums_activity_input = {
            "tool": "get_l2_activity",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        }
        validiums_activity_output = await agent.handle_message(validiums_activity_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 7: L2 Activity - Others
        # ====================================================================
        print("Test 7: L2 Activity for Other L2s")
        others_activity_input = {
            "tool": "get_l2_activity",
            "tool_arguments": {"category": "others"},
        }
        others_activity_output = await agent.handle_message(others_activity_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 8: L2 Activity - Not Reviewed
        # ====================================================================
        print("Test 8: L2 Activity for Not Reviewed L2s")
        not_reviewed_activity_input = {
            "tool": "get_l2_activity",
            "tool_arguments": {"category": "notReviewed"},
        }
        not_reviewed_activity_output = await agent.handle_message(not_reviewed_activity_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 9: L2 Costs - Rollups (Natural Language)
        # ====================================================================
        print("Test 9: L2 Costs for Rollups (natural language)")
        rollups_costs_input = {
            "query": "Which Layer 2 Rollup has the lowest transaction costs for token swaps?",
            "raw_data_only": False,
        }
        rollups_costs_output = await agent.handle_message(rollups_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 10: L2 Costs - Others (includes Validiums & Optimiums)
        # ====================================================================
        print("Test 10: L2 Costs for Others (includes Validiums & Optimiums)")
        others_costs_input = {
            "tool": "get_l2_costs",
            "tool_arguments": {"category": "others"},
        }
        others_costs_output = await agent.handle_message(others_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 11: Natural Language Query - Cross-Category Comparison
        # ====================================================================
        print("Test 11: Natural language query for cross-category comparison")
        cross_category_input = {
            "query": "Compare the TVL between top Rollups and top Validiums/Optimiums. Which category has higher total value locked?",
            "raw_data_only": False,
        }
        cross_category_output = await agent.handle_message(cross_category_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 12: Natural Language Query - Not Reviewed Projects
        # ====================================================================
        print("Test 12: Natural language query about not reviewed projects")
        not_reviewed_query_input = {
            "query": "What are the not reviewed L2 projects and what's their activity level?",
            "raw_data_only": False,
        }
        not_reviewed_query_output = await agent.handle_message(not_reviewed_query_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 13: Direct Tool Call with Default (Backward Compatibility)
        # ====================================================================
        print("Test 13: Direct tool call without category (backward compatibility test)")
        default_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {},  # No category specified, should default to rollups
        }
        default_summary_output = await agent.handle_message(default_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Save Results to YAML
        # ====================================================================
        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        output_file = script_dir / f"{current_file}_example.yaml"

        yaml_content = {
            "l2_summary": {
                "rollups": {
                    "natural_language": {
                        "input": rollups_summary_input,
                        "output": rollups_summary_output,
                    },
                },
                "validiums_and_optimiums": {
                    "direct_tool": {
                        "input": validiums_summary_input,
                        "output": validiums_summary_output,
                    },
                },
                "others": {
                    "direct_tool": {
                        "input": others_summary_input,
                        "output": others_summary_output,
                    },
                },
                "not_reviewed": {
                    "direct_tool": {
                        "input": not_reviewed_summary_input,
                        "output": not_reviewed_summary_output,
                    },
                },
                "default_backward_compatibility": {
                    "direct_tool": {
                        "input": default_summary_input,
                        "output": default_summary_output,
                    },
                },
            },
            "l2_activity": {
                "rollups": {
                    "natural_language": {
                        "input": rollups_activity_input,
                        "output": rollups_activity_output,
                    },
                },
                "validiums_and_optimiums": {
                    "direct_tool": {
                        "input": validiums_activity_input,
                        "output": validiums_activity_output,
                    },
                },
                "others": {
                    "direct_tool": {
                        "input": others_activity_input,
                        "output": others_activity_output,
                    },
                },
                "not_reviewed": {
                    "direct_tool": {
                        "input": not_reviewed_activity_input,
                        "output": not_reviewed_activity_output,
                    },
                },
            },
            "l2_costs": {
                "rollups": {
                    "natural_language": {
                        "input": rollups_costs_input,
                        "output": rollups_costs_output,
                    },
                },
                "others": {
                    "direct_tool": {
                        "input": others_costs_input,
                        "output": others_costs_output,
                    },
                },
            },
            "cross_category_queries": {
                "tvl_comparison": {
                    "natural_language": {
                        "input": cross_category_input,
                        "output": cross_category_output,
                    },
                },
                "not_reviewed_analysis": {
                    "natural_language": {
                        "input": not_reviewed_query_input,
                        "output": not_reviewed_query_output,
                    },
                },
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False, width=120)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
