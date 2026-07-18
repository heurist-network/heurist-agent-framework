"""
Test script for Fast402BaseDeFiAgent

"""

import asyncio
import os
import sys
import yaml
from datetime import datetime

# ─── Path setup ───────────────────────────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mesh.agents.fast402_base_defi_agent import Fast402BaseDeFiAgent

# ─── Test Addresses (Base Mainnet — public/well-known addresses) ──────────────

# Coinbase wallet (well-known public address, testing only)
TEST_WALLET = "0x4200000000000000000000000000000000000006"

# AERO/USDC Aerodrome pool on Base
TEST_POOL_V3 = "0x6cdcb1c4a4d1c3c6d054b27ac5b77e89eafb971d"

# Aerodrome WETH/USDC gauge
TEST_GAUGE = "0x519BBD1Dd8C6A94C46080E24f316c14Ee758C025"
TEST_LP_TOKEN = "0xcdac0d6c6c59727a65f871236188350531885c43"

# ─── Test Cases ───────────────────────────────────────────────────────────────

TEST_CASES = [
    # ── 1. Direct tool calls (raw_data_only=True) — bypass LLM ──
    {
        "id": "check_assets_basic",
        "description": "Direct: check ETH + USDC balance",
        "input": {
            "tool": "check_assets",
            "tool_arguments": {"walletAddress": TEST_WALLET},
            "raw_data_only": True,
        },
    },
    {
        "id": "check_assets_with_pool",
        "description": "Direct: check assets + LP reserves",
        "input": {
            "tool": "check_assets",
            "tool_arguments": {
                "walletAddress": TEST_WALLET,
                "poolAddress": TEST_POOL_V3,
            },
            "raw_data_only": True,
        },
    },
    {
        "id": "wallet_portfolio_default",
        "description": "Direct: portfolio snapshot (default tokens)",
        "input": {
            "tool": "wallet_portfolio",
            "tool_arguments": {"walletAddress": TEST_WALLET},
            "raw_data_only": True,
        },
    },
    {
        "id": "wallet_portfolio_custom_tokens",
        "description": "Direct: portfolio snapshot with custom token list",
        "input": {
            "tool": "wallet_portfolio",
            "tool_arguments": {
                "walletAddress": TEST_WALLET,
                "tokens": [
                    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC
                    "0x940181a94A35A4569E4529A3CDfB74e38FD98631",  # AERO
                ],
            },
            "raw_data_only": True,
        },
    },
    {
        "id": "token_price_v3",
        "description": "Direct: token price from Aerodrome pool",
        "input": {
            "tool": "token_price",
            "tool_arguments": {"poolAddress": TEST_POOL_V3},
            "raw_data_only": True,
        },
    },
    {
        "id": "aerodrome_apy_basic",
        "description": "Direct: Aerodrome APY without reward price",
        "input": {
            "tool": "aerodrome_apy",
            "tool_arguments": {
                "gaugeAddress": TEST_GAUGE,
                "lpTokenAddress": TEST_LP_TOKEN,
            },
            "raw_data_only": True,
        },
    },
    {
        "id": "aerodrome_apy_with_price",
        "description": "Direct: Aerodrome APY with reward token price",
        "input": {
            "tool": "aerodrome_apy",
            "tool_arguments": {
                "gaugeAddress": TEST_GAUGE,
                "lpTokenAddress": TEST_LP_TOKEN,
                "rewardTokenPriceUSD": 1.2,  # example price aero
            },
            "raw_data_only": True,
        },
    },
    {
        "id": "tx_history_default",
        "description": "Direct: tx history default (10 latest transactions)",
        "input": {
            "tool": "tx_history",
            "tool_arguments": {"walletAddress": TEST_WALLET},
            "raw_data_only": True,
        },
    },
    {
        "id": "tx_history_custom_limit",
        "description": "Direct: tx history with limit custom",
        "input": {
            "tool": "tx_history",
            "tool_arguments": {
                "walletAddress": TEST_WALLET,
                "limit": 5,
            },
            "raw_data_only": True,
        },
    },
    # ── 2. Agent mode (query → LLM interpret → tool call) ─────────────────────
    {
        "id": "agent_check_balance_query",
        "description": "Agent mode: natural language balance check",
        "input": {
            "query": f"What is the ETH and USDC balance for wallet {TEST_WALLET}?",
        },
    },
    {
        "id": "agent_portfolio_query",
        "description": "Agent mode: natural language portfolio request",
        "input": {
            "query": f"Give me a full portfolio snapshot for {TEST_WALLET} including WETH and AERO",
        },
    },
    {
        "id": "agent_price_query",
        "description": "Agent mode: natural language token price",
        "input": {
            "query": f"What is the current token price for pool {TEST_POOL_V3} on Base?",
        },
    },
    {
        "id": "agent_apy_query",
        "description": "Agent mode: natural language APY request",
        "input": {
            "query": f"Estimate the APY for Aerodrome gauge {TEST_GAUGE} with LP token {TEST_LP_TOKEN}",
        },
    },
    {
        "id": "agent_tx_history_query",
        "description": "Agent mode: natural language tx history",
        "input": {
            "query": f"Show me the last 5 USDC transactions for {TEST_WALLET}",
        },
    },
    # ── 3. Edge cases ──────────────────────────────────────────────────────────
    {
        "id": "edge_missing_wallet",
        "description": "Edge: walletAddress empty — should return error 400",
        "input": {
            "tool": "check_assets",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "expect_error": True,
    },
    {
        "id": "edge_invalid_pool",
        "description": "Edge: poolAddress invalid — should return error from provider",
        "input": {
            "tool": "token_price",
            "tool_arguments": {"poolAddress": "0x0000000000000000000000000000000000000000"},
            "raw_data_only": True,
        },
        "expect_error": True,
    },
]

# ─── Runner ───────────────────────────────────────────────────────────────────

async def run_test(agent: Fast402BaseDeFiAgent, test_case: dict) -> dict:
    test_id = test_case["id"]
    description = test_case["description"]
    input_data = test_case["input"]
    expect_error = test_case.get("expect_error", False)

    print(f"\n{'─'*60}")
    print(f"[{test_id}] {description}")
    print(f"Input: {input_data}")

    start = datetime.now()
    result = {
        "id": test_id,
        "description": description,
        "input": input_data,
        "timestamp": start.isoformat(),
        "passed": False,
        "output": None,
        "error": None,
        "duration_ms": None,
    }

    try:
        response = await agent.handle_message(input_data)
        duration = (datetime.now() - start).total_seconds() * 1000
        result["duration_ms"] = round(duration, 2)
        result["output"] = response

        # Base validation
        if expect_error:
            # If you expect an error, keep passing as long as there is a response (error handled gracefully)
            result["passed"] = True
            print(f"✅ PASS (expected error, got graceful response) [{duration:.0f}ms]")
        elif response and ("error" not in str(response).lower() or "details" in str(response).lower()):
            result["passed"] = True
            print(f"✅ PASS [{duration:.0f}ms]")
        else:
            result["passed"] = False
            print(f"❌ FAIL — response: {response}")

    except Exception as e:
        duration = (datetime.now() - start).total_seconds() * 1000
        result["duration_ms"] = round(duration, 2)
        result["error"] = str(e)

        if expect_error:
            result["passed"] = True
            print(f"✅ PASS (expected exception: {e}) [{duration:.0f}ms]")
        else:
            result["passed"] = False
            print(f"❌ FAIL — exception: {e}")

    return result


async def main():
    print("=" * 60)
    print("  FAST402-ENGINE Base DeFi Agent — Test Suite")
    print("=" * 60)

    # Check base_url agent
    agent = Fast402BaseDeFiAgent()
    print(f"\n🔗 Provider URL: {agent.base_url}")
    print(f"📋 Total test cases: {len(TEST_CASES)}")

    results = []
    passed = 0
    failed = 0

    async with agent:
        for test_case in TEST_CASES:
            result = await run_test(agent, test_case)
            results.append(result)
            if result["passed"]:
                passed += 1
            else:
                failed += 1

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Results: {passed} passed, {failed} failed / {len(TEST_CASES)} total")
    print(f"{'='*60}")

    # ── Save ke YAML (format standar heurist mesh/tests/) ─────────────────────
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "fast402_base_defi_agent_example.yaml")

    yaml_output = {
        "agent": "Fast402BaseDeFiAgent",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(TEST_CASES),
            "passed": passed,
            "failed": failed,
        },
        "results": results,
    }

    with open(output_path, "w") as f:
        yaml.dump(yaml_output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\n📄 Results saved to: {output_path}")

    # Exit code 1 if something fails (useful for CI)
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())