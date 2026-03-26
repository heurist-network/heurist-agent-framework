import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.yahoo_finance_agent import YahooFinanceAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "resolve_apple": {
        "input": {
            "tool": "resolve_symbol",
            "tool_arguments": {"query": "Apple", "asset_type": "stock", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Resolve Apple into a compact list of stock candidates.",
        "expected_status": "success",
    },
    "resolve_invalid_asset_type": {
        "input": {
            "tool": "resolve_symbol",
            "tool_arguments": {"query": "Apple", "asset_type": "bond", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Direct error for unsupported asset-type filter.",
        "expected_status": "error",
    },
    "resolve_no_matches": {
        "input": {
            "tool": "resolve_symbol",
            "tool_arguments": {"query": "zxqwvut nonexistent corp 123456789", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Honest no-data response when symbol search finds nothing.",
        "expected_status": "error",
    },
    "resolve_future_gold": {
        "input": {
            "tool": "resolve_symbol",
            "tool_arguments": {"query": "gold", "asset_type": "future", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Resolve a commodity intent into compact futures candidates via Lookup.",
        "expected_status": "success",
    },
    "quote_snapshot_aapl": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": ["AAPL"]},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for AAPL using a one-item list.",
        "expected_status": "success",
    },
    "quote_snapshot_aapl_single_string": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": "AAPL"},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for AAPL using a plain single-symbol string.",
        "expected_status": "success",
    },
    "quote_snapshot_aapl_legacy_symbol": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbol": "AAPL"},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for AAPL using the legacy singular symbol argument.",
        "expected_status": "success",
    },
    "quote_snapshot_btc": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": ["BTC-USD"]},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for BTC-USD using a one-item list.",
        "expected_status": "success",
    },
    "quote_snapshot_batch_mixed": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": ["AAPL", "MSFT", "NOTAREALSYMBOL123"]},
            "raw_data_only": True,
        },
        "description": "Batch quote snapshot returns per-symbol success and no-data rows in one response.",
        "expected_status": "success",
    },
    "quote_snapshot_invalid_symbol": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbols": ["NOTAREALSYMBOL123"]},
            "raw_data_only": True,
        },
        "description": "Invalid symbol returns a structured no-data response instead of an exception.",
        "expected_status": "error",
    },
    "price_history_aapl": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["AAPL"], "interval": "1d", "period": "6mo", "limit_bars": 10},
            "raw_data_only": True,
        },
        "description": "Normalized daily price history for AAPL using a one-item list.",
        "expected_status": "success",
    },
    "price_history_aapl_single_string": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": "AAPL", "interval": "1d", "period": "6mo", "limit_bars": 10},
            "raw_data_only": True,
        },
        "description": "Normalized daily price history for AAPL using a plain single-symbol string.",
        "expected_status": "success",
    },
    "price_history_btc_intraday": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["BTC-USD"], "interval": "1h", "period": "1mo", "limit_bars": 12},
            "raw_data_only": True,
        },
        "description": "Normalized intraday price history for BTC-USD using a one-item list.",
        "expected_status": "success",
    },
    "price_history_batch_equities": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["AAPL", "MSFT"], "interval": "1d", "period": "1mo", "limit_bars": 5},
            "raw_data_only": True,
        },
        "description": "Batch daily price history returns bounded bars for multiple equities.",
        "expected_status": "success",
    },
    "price_history_explicit_range": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {
                "symbols": ["AAPL"],
                "interval": "1d",
                "start_date": "2026-01-01",
                "end_date": "2026-02-01",
                "limit_bars": 5,
            },
            "raw_data_only": True,
        },
        "description": "Explicit start/end range is respected and reported cleanly.",
        "expected_status": "success",
    },
    "price_history_unsupported_interval": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["AAPL"], "interval": "4h"},
            "raw_data_only": True,
        },
        "description": "Unsupported interval fails directly.",
        "expected_status": "error",
    },
    "price_history_invalid_symbol": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbols": ["NOTAREALSYMBOL123"], "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Invalid symbol returns structured no-data for history requests.",
        "expected_status": "error",
    },
    "technical_snapshot_tsla": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbols": ["TSLA"], "interval": "1d", "period": "1y"},
            "raw_data_only": True,
        },
        "description": "Agent-ergonomic technical snapshot for TSLA using a one-item list.",
        "expected_status": "success",
    },
    "technical_snapshot_eth": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbols": ["ETH-USD"], "interval": "1h", "period": "3mo"},
            "raw_data_only": True,
        },
        "description": "Agent-ergonomic technical snapshot for ETH-USD using a one-item list.",
        "expected_status": "success",
    },
    "technical_snapshot_batch_equities": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbols": ["TSLA", "NVDA"], "interval": "1d", "period": "1y"},
            "raw_data_only": True,
        },
        "description": "Batch technical snapshots return compact per-symbol signals.",
        "expected_status": "success",
    },
    "technical_snapshot_short_window": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbols": ["AAPL"], "interval": "1h", "period": "3d"},
            "raw_data_only": True,
        },
        "description": "Short history window returns no-data when there are not enough completed bars.",
        "expected_status": "error",
    },
    "options_expirations_aapl": {
        "input": {
            "tool": "options_expirations",
            "tool_arguments": {"symbol": "AAPL", "limit": 8},
            "raw_data_only": True,
        },
        "description": "Discover available AAPL option expirations before selecting a chain.",
        "expected_status": "success",
    },
    "options_expirations_aapl_dte_window": {
        "input": {
            "tool": "options_expirations",
            "tool_arguments": {"symbol": "AAPL", "min_days_to_expiration": 20, "max_days_to_expiration": 120, "limit": 6},
            "raw_data_only": True,
        },
        "description": "Discover AAPL expirations within a bounded days-to-expiration window.",
        "expected_status": "success",
    },
    "options_expirations_invalid_symbol": {
        "input": {
            "tool": "options_expirations",
            "tool_arguments": {"symbol": "NOTAREALSYMBOL123"},
            "raw_data_only": True,
        },
        "description": "Invalid symbol returns structured no-data for expiration discovery.",
        "expected_status": "error",
    },
    "options_chain_aapl": {
        "input": {
            "tool": "options_chain",
            "tool_arguments": {"symbol": "AAPL", "side": "both", "moneyness": "atm", "limit_contracts": 6},
            "raw_data_only": True,
        },
        "description": "options_chain requires an explicit expiration chosen via options_expirations.",
        "expected_status": "error",
    },
    "options_chain_aapl_strike_window": {
        "input": {
            "tool": "options_chain",
            "tool_arguments": {"symbol": "AAPL", "side": "both", "expiration": "2026-04-17", "min_strike": 240, "max_strike": 270, "limit_contracts": 6},
            "raw_data_only": True,
        },
        "description": "Filter AAPL options chain discovery by strike range.",
        "expected_status": "success",
    },
    "options_chain_invalid_expiration": {
        "input": {
            "tool": "options_chain",
            "tool_arguments": {"symbol": "AAPL", "expiration": "2099-01-01"},
            "raw_data_only": True,
        },
        "description": "Unsupported expiration fails directly for options chains.",
        "expected_status": "error",
    },
    "options_chain_invalid_strike_window": {
        "input": {
            "tool": "options_chain",
            "tool_arguments": {"symbol": "AAPL", "min_strike": 300, "max_strike": 250},
            "raw_data_only": True,
        },
        "description": "Invalid strike filter range fails directly for options chains.",
        "expected_status": "error",
    },
    "futures_snapshot_gold": {
        "input": {
            "tool": "futures_snapshot",
            "tool_arguments": {"symbols": ["GC=F"], "include_history": True, "interval": "1d", "period": "1mo", "limit_bars": 5},
            "raw_data_only": True,
        },
        "description": "Compact futures snapshot for gold with recent history context.",
        "expected_status": "success",
    },
    "futures_snapshot_invalid_asset": {
        "input": {
            "tool": "futures_snapshot",
            "tool_arguments": {"symbols": ["AAPL"]},
            "raw_data_only": True,
        },
        "description": "Futures snapshot rejects non-futures symbols directly.",
        "expected_status": "error",
    },
    "news_search_nvidia": {
        "input": {
            "tool": "news_search",
            "tool_arguments": {"query": "Nvidia", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Recent news search for Nvidia.",
        "expected_status": "success",
    },
    "news_search_no_results": {
        "input": {
            "tool": "news_search",
            "tool_arguments": {"query": "zxqwvut nonexistent corp 123456789", "limit": 3},
            "raw_data_only": True,
        },
        "description": "No-results news query returns structured no-data.",
        "expected_status": "error",
    },
    "market_overview_us": {
        "input": {
            "tool": "market_overview",
            "tool_arguments": {"market": "US"},
            "raw_data_only": True,
        },
        "description": "US market overview.",
        "expected_status": "success",
    },
    "market_overview_invalid": {
        "input": {
            "tool": "market_overview",
            "tool_arguments": {"market": "MARS"},
            "raw_data_only": True,
        },
        "description": "Honest failure for unsupported market name.",
        "expected_status": "error",
    },
    "company_fundamentals_aapl": {
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbols": ["AAPL"]},
            "raw_data_only": True,
        },
        "description": "Compact company fundamentals for AAPL using a one-item list.",
        "expected_status": "success",
    },
    "company_fundamentals_aapl_single_string": {
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbols": "AAPL"},
            "raw_data_only": True,
        },
        "description": "Compact company fundamentals for AAPL using a plain single-symbol string.",
        "expected_status": "success",
    },
    "company_fundamentals_batch_mixed": {
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbols": ["AAPL", "MSFT", "SPY"]},
            "raw_data_only": True,
        },
        "description": "Batch company fundamentals keeps per-symbol asset mismatch errors scoped to the offending symbol.",
        "expected_status": "success",
    },
    "company_fundamentals_invalid_asset": {
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbols": ["SPY"]},
            "raw_data_only": True,
        },
        "description": "Company fundamentals rejects ETF symbols directly.",
        "expected_status": "error",
    },
    "analyst_snapshot_msft": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbols": ["MSFT"]},
            "raw_data_only": True,
        },
        "description": "Compact analyst snapshot for MSFT using a one-item list.",
        "expected_status": "success",
    },
    "analyst_snapshot_msft_single_string": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbols": "MSFT"},
            "raw_data_only": True,
        },
        "description": "Compact analyst snapshot for MSFT using a plain single-symbol string.",
        "expected_status": "success",
    },
    "analyst_snapshot_batch_mixed": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbols": ["MSFT", "AMZN", "BTC-USD"]},
            "raw_data_only": True,
        },
        "description": "Batch analyst snapshot returns per-symbol equity-only validation.",
        "expected_status": "success",
    },
    "analyst_snapshot_invalid_asset": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbols": ["BTC-USD"]},
            "raw_data_only": True,
        },
        "description": "Analyst snapshot rejects non-equity symbols directly.",
        "expected_status": "error",
    },
    "fund_snapshot_spy": {
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbols": ["SPY"]},
            "raw_data_only": True,
        },
        "description": "Compact ETF snapshot for SPY using a one-item list.",
        "expected_status": "success",
    },
    "fund_snapshot_batch_mixed": {
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbols": ["SPY", "QQQ", "AAPL"]},
            "raw_data_only": True,
        },
        "description": "Batch fund snapshots return per-symbol fund-only validation.",
        "expected_status": "success",
    },
    "fund_snapshot_invalid_asset": {
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbols": ["AAPL"]},
            "raw_data_only": True,
        },
        "description": "Fund snapshot rejects equity symbols directly.",
        "expected_status": "error",
    },
    "equity_screen_day_gainers": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "day_gainers", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Curated Yahoo day gainers screen.",
        "expected_status": "success",
    },
    "equity_screen_aggressive_small_caps": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "aggressive_small_caps", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Curated Yahoo aggressive small caps screen.",
        "expected_status": "success",
    },
    "equity_screen_most_shorted_stocks": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "most_shorted_stocks", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Curated Yahoo most shorted stocks screen.",
        "expected_status": "success",
    },
    "equity_screen_small_cap_gainers": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "small_cap_gainers", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Curated Yahoo small cap gainers screen.",
        "expected_status": "success",
    },
    "equity_screen_undervalued_growth_stocks": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "undervalued_growth_stocks", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Curated Yahoo undervalued growth stocks screen.",
        "expected_status": "success",
    },
    "equity_screen_invalid": {
        "input": {
            "tool": "equity_screen",
            "tool_arguments": {"screen_name": "moonshots", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Unsupported equity screen fails directly.",
        "expected_status": "error",
    },
}


def _result_status(result):
    output = result.get("output") or {}
    data = output.get("data") or {}
    if data.get("status") == "no_data":
        return "error"
    if data.get("status"):
        return data.get("status")
    error = (data.get("error") or "").lower()
    if "rate limited" in error:
        return "rate_limited"
    if "error" in data:
        return "error"
    return None


if __name__ == "__main__":
    results = asyncio.run(test_agent(YahooFinanceAgent, TEST_CASES, delay_seconds=1.0))
    failures = []
    rate_limited = []
    for name, case in TEST_CASES.items():
        actual_status = _result_status(results.get(name, {}))
        if actual_status == "rate_limited":
            rate_limited.append(name)
            continue
        if actual_status != case["expected_status"]:
            failures.append(f"{name}: expected {case['expected_status']}, got {actual_status}")

    if rate_limited:
        print("Yahoo Finance rate limited live success-path checks:", ", ".join(rate_limited))

    if failures:
        raise SystemExit("\n".join(failures))
