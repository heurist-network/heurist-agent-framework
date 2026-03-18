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
    "quote_snapshot_aapl": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbol": "AAPL"},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for AAPL.",
        "expected_status": "success",
    },
    "quote_snapshot_btc": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbol": "BTC-USD"},
            "raw_data_only": True,
        },
        "description": "Compact quote snapshot for BTC-USD.",
        "expected_status": "success",
    },
    "quote_snapshot_invalid_symbol": {
        "input": {
            "tool": "quote_snapshot",
            "tool_arguments": {"symbol": "NOTAREALSYMBOL123"},
            "raw_data_only": True,
        },
        "description": "Invalid symbol returns a structured no-data response instead of an exception.",
        "expected_status": "error",
    },
    "price_history_aapl": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbol": "AAPL", "interval": "1d", "period": "6mo", "limit_bars": 10},
            "raw_data_only": True,
        },
        "description": "Normalized daily price history for AAPL.",
        "expected_status": "success",
    },
    "price_history_btc_intraday": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbol": "BTC-USD", "interval": "1h", "period": "1mo", "limit_bars": 12},
            "raw_data_only": True,
        },
        "description": "Normalized intraday price history for BTC-USD.",
        "expected_status": "success",
    },
    "price_history_explicit_range": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {
                "symbol": "AAPL",
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
            "tool_arguments": {"symbol": "AAPL", "interval": "4h"},
            "raw_data_only": True,
        },
        "description": "Unsupported interval fails directly.",
        "expected_status": "error",
    },
    "price_history_invalid_symbol": {
        "input": {
            "tool": "price_history",
            "tool_arguments": {"symbol": "NOTAREALSYMBOL123", "interval": "1d", "period": "1mo"},
            "raw_data_only": True,
        },
        "description": "Invalid symbol returns structured no-data for history requests.",
        "expected_status": "error",
    },
    "technical_snapshot_tsla": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbol": "TSLA", "interval": "1d", "period": "1y"},
            "raw_data_only": True,
        },
        "description": "Agent-ergonomic technical snapshot for TSLA.",
        "expected_status": "success",
    },
    "technical_snapshot_eth": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbol": "ETH-USD", "interval": "1h", "period": "3mo"},
            "raw_data_only": True,
        },
        "description": "Agent-ergonomic technical snapshot for ETH-USD.",
        "expected_status": "success",
    },
    "technical_snapshot_short_window": {
        "input": {
            "tool": "technical_snapshot",
            "tool_arguments": {"symbol": "AAPL", "interval": "1h", "period": "3d"},
            "raw_data_only": True,
        },
        "description": "Short history window returns no-data when there are not enough completed bars.",
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
            "tool_arguments": {"symbol": "AAPL"},
            "raw_data_only": True,
        },
        "description": "Compact company fundamentals for AAPL.",
        "expected_status": "success",
    },
    "company_fundamentals_invalid_asset": {
        "input": {
            "tool": "company_fundamentals",
            "tool_arguments": {"symbol": "SPY"},
            "raw_data_only": True,
        },
        "description": "Company fundamentals rejects ETF symbols directly.",
        "expected_status": "error",
    },
    "analyst_snapshot_msft": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbol": "MSFT"},
            "raw_data_only": True,
        },
        "description": "Compact analyst snapshot for MSFT.",
        "expected_status": "success",
    },
    "analyst_snapshot_invalid_asset": {
        "input": {
            "tool": "analyst_snapshot",
            "tool_arguments": {"symbol": "BTC-USD"},
            "raw_data_only": True,
        },
        "description": "Analyst snapshot rejects non-equity symbols directly.",
        "expected_status": "error",
    },
    "fund_snapshot_spy": {
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbol": "SPY"},
            "raw_data_only": True,
        },
        "description": "Compact ETF snapshot for SPY.",
        "expected_status": "success",
    },
    "fund_snapshot_invalid_asset": {
        "input": {
            "tool": "fund_snapshot",
            "tool_arguments": {"symbol": "AAPL"},
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
