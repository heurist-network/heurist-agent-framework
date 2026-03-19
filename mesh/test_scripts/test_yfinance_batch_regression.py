import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.yahoo_finance_agent import YahooFinanceAgent


TEST_CASES = [
    {
        "name": "quote_snapshot_one_item_list",
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": ["NVDA"]},
            "raw_data_only": True,
        },
        "expected_top_status": "success",
        "expected_symbol_statuses": {"NVDA": "success"},
    },
    {
        "name": "price_history_batch_equities",
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["AAPL", "MSFT"], "interval": "1d", "period": "1mo", "limit_bars": 5},
            "raw_data_only": True,
        },
        "expected_top_status": "success",
        "expected_symbol_statuses": {"AAPL": "success", "MSFT": "success"},
    },
    {
        "name": "technical_snapshot_batch_equities",
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbols": ["TSLA", "NVDA"], "interval": "1d", "period": "1y"},
            "raw_data_only": True,
        },
        "expected_top_status": "success",
        "expected_symbol_statuses": {"TSLA": "success", "NVDA": "success"},
    },
    {
        "name": "company_fundamentals_mixed_assets",
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbols": ["AAPL", "SPY"]},
            "raw_data_only": True,
        },
        "expected_top_status": "success",
        "expected_symbol_statuses": {"AAPL": "success", "SPY": "error"},
    },
    {
        "name": "fund_snapshot_mixed_assets",
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbols": ["SPY", "AAPL"]},
            "raw_data_only": True,
        },
        "expected_top_status": "success",
        "expected_symbol_statuses": {"SPY": "success", "AAPL": "error"},
    },
]


def _contains_rate_limit(payload) -> bool:
    if not isinstance(payload, dict):
        return False
    error = str(payload.get("error") or "").lower()
    if "rate limited" in error:
        return True
    nested = payload.get("data")
    if isinstance(nested, dict):
        for item in nested.get("results") or []:
            if "rate limited" in str(item.get("error") or "").lower():
                return True
    return False


async def main() -> None:
    agent = YahooFinanceAgent()
    failures = []
    rate_limited = []

    try:
        for case in TEST_CASES:
            result = await agent.handle_message(case["input"])
            payload = result.get("data") or {}
            if _contains_rate_limit(payload):
                rate_limited.append(case["name"])
                continue

            top_status = payload.get("status")
            data = payload.get("data") or {}
            results = data.get("results") or []
            result_map = {item.get("symbol"): item for item in results}

            if top_status != case["expected_top_status"]:
                failures.append(
                    f"{case['name']}: expected top status {case['expected_top_status']}, got {top_status}"
                )
                continue

            if data.get("symbols") != case["input"]["tool_arguments"]["symbols"]:
                failures.append(f"{case['name']}: response symbols did not preserve request order")
                continue

            summary = data.get("summary") or {}
            if summary.get("requested") != len(case["input"]["tool_arguments"]["symbols"]):
                failures.append(f"{case['name']}: summary.requested mismatch")
                continue

            for symbol, expected_status in case["expected_symbol_statuses"].items():
                actual = (result_map.get(symbol) or {}).get("status")
                if actual != expected_status:
                    failures.append(
                        f"{case['name']}: expected {symbol} status {expected_status}, got {actual}"
                    )

        if rate_limited:
            print("Yahoo Finance rate limited batch regression checks:", ", ".join(rate_limited))

        if failures:
            raise SystemExit("\n".join(failures))

        print("All Yahoo Finance batch regression checks passed.")
    finally:
        if hasattr(agent, "cleanup"):
            await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
