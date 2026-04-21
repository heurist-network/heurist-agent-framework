# Yahoo Finance Agent Feature Summary

This document maps the integrated Yahoo Finance agent tools to the underlying `yfinance` API surface they use.

The current agent entrypoint is [mesh/agents/yahoo_finance_agent.py](/home/appuser/heurist-agent-framework/mesh/agents/yahoo_finance_agent.py).

## Integrated Features

| Agent tool | What it returns | Original `yfinance` API |
| --- | --- | --- |
| `resolve_symbol` | Candidate tickers for a company name, fragment, or market term | `yfinance.Search(query, max_results=..., news_count=0, lists_count=0, include_cb=False).quotes` |
| `quote_snapshot` | Compact latest quote view for one or more symbols, with optional recent-bar history and window summary | `yfinance.Ticker(symbol).history(...)`, `Ticker.fast_info`, `Ticker.info` |
| `price_history` | Normalized OHLCV history with metadata and latest completed bars | `yfinance.Ticker(symbol).history(...)`, `Ticker.get_history_metadata()` |
| `technical_snapshot` | Technical indicators and signal summary | `yfinance.Ticker(symbol).history(...)` plus `stockstats.wrap(...)` over the returned OHLCV frame |
| `options_chain` | Two-mode options tool: discovery without `expiration`, or compact chain snapshot for one exact expiration with filtered contracts and open-interest or volume summary | `yfinance.Ticker(symbol).options`, `Ticker.option_chain(date)` |
| `news_search` | Recent news items for a symbol, company, or topic | `yfinance.Search(query, max_results=..., news_count=...).news` |
| `market_overview` | Market status and benchmark summary | `yfinance.Market(market).status`, `yfinance.Market(market).summary` |
| `equity_overview` | Compact equity overview combining fundamentals and analyst data, with optional section filtering | `Ticker.info`, `Ticker.calendar`, `Ticker.sec_filings`, `Ticker.income_stmt`, `Ticker.quarterly_income_stmt`, `Ticker.balance_sheet`, `Ticker.quarterly_balance_sheet`, `Ticker.cashflow`, `Ticker.quarterly_cashflow`, `Ticker.recommendations_summary`, `Ticker.analyst_price_targets`, `Ticker.earnings_estimate`, `Ticker.revenue_estimate`, `Ticker.eps_trend`, `Ticker.eps_revisions` |
| `fund_snapshot` | ETF or mutual fund overview and holdings | `Ticker.funds_data` and its properties: `description`, `fund_overview`, `fund_operations`, `asset_classes`, `top_holdings`, `equity_holdings`, `bond_holdings`, `sector_weightings` |
| `equity_screen` | Curated predefined equity screen results | `yfinance.screen(screen_name, count=...)` |

## Notes

- `fetch_price_history` is a legacy alias for `price_history`.
- `indicator_snapshot` is a legacy alias for `technical_snapshot`.
- The agent intentionally avoids exposing raw Yahoo payloads by default. Each tool normalizes the corresponding `yfinance` output into a compact structure.
- History-bearing tools now share an internal frame cache so exact repeats and overlapping explicit date ranges can reuse previously fetched data instead of redownloading full windows.
- Asset support is tool-specific:
  - `equity_overview` is equity-only.
- `fund_snapshot` is for ETFs and mutual funds.
- For futures symbols, use `quote_snapshot` with `include_history=true`.
- `options_chain` is now the discovery step as well: call it without `expiration` to list valid expirations, then call it again with an exact expiration. In chain mode it returns bounded, agent-usable contract rows instead of raw full chains.
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
