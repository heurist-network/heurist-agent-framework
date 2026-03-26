# Yahoo Finance Agent Feature Summary

This document maps the integrated Yahoo Finance agent tools to the underlying `yfinance` API surface they use.

The current agent entrypoint is [mesh/agents/yahoo_finance_agent.py](/home/appuser/heurist-agent-framework/mesh/agents/yahoo_finance_agent.py).

## Integrated Features

| Agent tool | What it returns | Original `yfinance` API |
| --- | --- | --- |
| `resolve_symbol` | Candidate tickers for a company name, fragment, or market term | `yfinance.Search(query, max_results=..., news_count=0, lists_count=0, include_cb=False).quotes` |
| `quote_snapshot` | Compact latest quote view for one symbol | `yfinance.Ticker(symbol).history(...)`, `Ticker.fast_info`, `Ticker.info` |
| `price_history` | Normalized OHLCV history with metadata and latest completed bars | `yfinance.Ticker(symbol).history(...)`, `Ticker.get_history_metadata()` |
| `technical_snapshot` | Technical indicators and signal summary | `yfinance.Ticker(symbol).history(...)` plus `stockstats.wrap(...)` over the returned OHLCV frame |
| `options_expirations` | Compact option-expiration discovery with days-to-expiration, monthly or weekly hints, and optional DTE filtering | `yfinance.Ticker(symbol).options` |
| `options_chain` | Compact options chain for one exact expiration, with filtered contracts, open-interest or volume summary, and optional strike-range filtering | `yfinance.Ticker(symbol).options`, `Ticker.option_chain(date)` |
| `futures_snapshot` | Compact futures quote snapshot with optional recent trend context | `yfinance.Ticker(symbol).history(...)`, `Ticker.fast_info`, `Ticker.info` |
| `news_search` | Recent news items for a symbol, company, or topic | `yfinance.Search(query, max_results=..., news_count=...).news` |
| `market_overview` | Market status and benchmark summary | `yfinance.Market(market).status`, `yfinance.Market(market).summary` |
| `company_fundamentals` | Compact equity fundamentals | `Ticker.info`, `Ticker.calendar`, `Ticker.sec_filings`, `Ticker.income_stmt`, `Ticker.quarterly_income_stmt`, `Ticker.balance_sheet`, `Ticker.quarterly_balance_sheet`, `Ticker.cashflow`, `Ticker.quarterly_cashflow` |
| `analyst_snapshot` | Compact analyst estimates and price targets | `Ticker.recommendations_summary`, `Ticker.analyst_price_targets`, `Ticker.earnings_estimate`, `Ticker.revenue_estimate`, `Ticker.eps_trend`, `Ticker.eps_revisions` |
| `fund_snapshot` | ETF or mutual fund overview and holdings | `Ticker.funds_data` and its properties: `description`, `fund_overview`, `fund_operations`, `asset_classes`, `top_holdings`, `equity_holdings`, `bond_holdings`, `sector_weightings` |
| `equity_screen` | Curated predefined equity screen results | `yfinance.screen(screen_name, count=...)` |

## Notes

- `fetch_price_history` is a legacy alias for `price_history`.
- `indicator_snapshot` is a legacy alias for `technical_snapshot`.
- The agent intentionally avoids exposing raw Yahoo payloads by default. Each tool normalizes the corresponding `yfinance` output into a compact structure.
- History-bearing tools now share an internal frame cache so exact repeats and overlapping explicit date ranges can reuse previously fetched data instead of redownloading full windows.
- Asset support is tool-specific:
  - `company_fundamentals` and `analyst_snapshot` are equity-only.
- `futures_snapshot` is future-only and `resolve_symbol` uses `yfinance.Lookup(...).get_future(...)` when `asset_type="future"`.
- `fund_snapshot` is for ETFs and mutual funds.
- `options_expirations` is the required discovery step when the user asks what option dates exist or has not yet chosen an expiration.
- `options_chain` is for one exact underlying symbol and one exact expiration at a time, and returns bounded, agent-usable contract rows instead of raw full chains. It now supports strike-range filtering without refetching the raw chain for every filter combination.
- `equity_screen` only exposes a curated set of predefined equity screens:
  - `aggressive_small_caps`
  - `day_gainers`
  - `day_losers`
  - `growth_technology_stocks`
  - `most_actives`
  - `most_shorted_stocks`
  - `small_cap_gainers`
  - `undervalued_growth_stocks`
  - `undervalued_large_caps`

## Related Files

- [mesh/tests/yahoo_finance_agent.py](/home/appuser/heurist-agent-framework/mesh/tests/yahoo_finance_agent.py)
- [mesh/tests/yahoo_finance_agent_example.yaml](/home/appuser/heurist-agent-framework/mesh/tests/yahoo_finance_agent_example.yaml)
