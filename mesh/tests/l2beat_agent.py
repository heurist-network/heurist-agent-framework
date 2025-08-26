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
        print("Starting L2Beat Agent tests (Updated - Summary & Costs only)...\n")

        # ====================================================================
        # Test 1: L2 Summary - Rollups (Default, Natural Language)
        # ====================================================================
        print("Test 1: L2 Summary for Rollups (natural language)")
        rollups_summary_input = {
            "query": "What's the current TVL and market share of the top Layer 2 Rollups?",
            "raw_data_only": False,
        }
        rollups_summary_output = await agent.handle_message(rollups_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 2: L2 Summary - Validiums and Optimiums (Direct Tool)
        # ====================================================================
        print("Test 2: L2 Summary for Validiums and Optimiums")
        validiums_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        }
        validiums_summary_output = await agent.handle_message(validiums_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 3: L2 Costs - Rollups (Natural Language)
        # ====================================================================
        print("Test 3: L2 Costs for Rollups (natural language)")
        rollups_costs_input = {
            "query": "Which Layer 2 Rollup has the lowest transaction costs right now?",
            "raw_data_only": False,
        }
        rollups_costs_output = await agent.handle_message(rollups_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 4: L2 Costs - Validiums and Optimiums (Direct Tool)
        # ====================================================================
        print("Test 4: L2 Costs for Validiums and Optimiums")
        validiums_costs_input = {
            "tool": "get_l2_costs",
            "tool_arguments": {"category": "validiumsAndOptimiums"},
        }
        validiums_costs_output = await agent.handle_message(validiums_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 5: Complex Analysis Query - ZK Chains Costs
        # ====================================================================
        print("Test 5: Complex query - Average transaction costs for ZK chains")
        zk_costs_input = {
            "query": "What are the average transaction costs for ZK chains (validity proof systems)?",
            "raw_data_only": False,
        }
        zk_costs_output = await agent.handle_message(zk_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 6: Cost Comparison Query
        # ====================================================================
        print("Test 6: Cost comparison between major L2s")
        cost_comparison_input = {
            "query": "Compare the transaction costs between Arbitrum, Base, Optimism, and ZKsync Era",
            "raw_data_only": False,
        }
        cost_comparison_output = await agent.handle_message(cost_comparison_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 7: TVL vs Cost Analysis
        # ====================================================================
        print("Test 7: TVL vs Cost analysis")
        tvl_cost_analysis_input = {
            "query": "Which L2s have both high TVL and low transaction costs?",
            "raw_data_only": False,
        }
        tvl_cost_analysis_output = await agent.handle_message(tvl_cost_analysis_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 8: Default Parameters Test
        # ====================================================================
        print("Test 8: Default parameters test (backward compatibility)")
        default_summary_input = {
            "tool": "get_l2_summary",
            "tool_arguments": {},  # No category specified, should default to rollups
        }
        default_summary_output = await agent.handle_message(default_summary_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 9: Default Parameters Test - Costs
        # ====================================================================
        print("Test 9: Default parameters test - costs (backward compatibility)")
        default_costs_input = {
            "tool": "get_l2_costs",
            "tool_arguments": {},  # No category specified, should default to rollups
        }
        default_costs_output = await agent.handle_message(default_costs_input)
        print("✅ Completed\n")

        # ====================================================================
        # Test 10: Proof System Analysis
        # ====================================================================
        print("Test 10: Proof system analysis query")
        proof_system_input = {
            "query": "Compare the TVL and costs between Optimistic Rollups and Validity (ZK) Rollups",
            "raw_data_only": False,
        }
        proof_system_output = await agent.handle_message(proof_system_input)
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
                    "default_backward_compatibility": {
                        "direct_tool": {
                            "input": default_summary_input,
                            "output": default_summary_output,
                        },
                    },
                },
                "validiums_and_optimiums": {
                    "direct_tool": {
                        "input": validiums_summary_input,
                        "output": validiums_summary_output,
                    },
                },
            },
            "l2_costs": {
                "rollups": {
                    "natural_language": {
                        "input": rollups_costs_input,
                        "output": rollups_costs_output,
                    },
                    "default_backward_compatibility": {
                        "direct_tool": {
                            "input": default_costs_input,
                            "output": default_costs_output,
                        },
                    },
                },
                "validiums_and_optimiums": {
                    "direct_tool": {
                        "input": validiums_costs_input,
                        "output": validiums_costs_output,
                    },
                },
            },
            "complex_analysis_queries": {
                "zk_chains_costs": {
                    "natural_language": {
                        "input": zk_costs_input,
                        "output": zk_costs_output,
                    },
                },
                "cost_comparison": {
                    "natural_language": {
                        "input": cost_comparison_input,
                        "output": cost_comparison_output,
                    },
                },
                "tvl_vs_cost_analysis": {
                    "natural_language": {
                        "input": tvl_cost_analysis_input,
                        "output": tvl_cost_analysis_output,
                    },
                },
                "proof_system_comparison": {
                    "natural_language": {
                        "input": proof_system_input,
                        "output": proof_system_output,
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
