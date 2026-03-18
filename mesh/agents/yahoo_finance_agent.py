import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from stockstats import wrap as stockstats_wrap
from yfinance.exceptions import (
    YFInvalidPeriodError,
    YFPricesMissingError,
    YFRateLimitError,
    YFTickerMissingError,
    YFTzMissingError,
)

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)

HISTORY_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
INTRADAY_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"}
MARKETS = ["US", "GB", "ASIA", "EUROPE", "RATES", "COMMODITIES", "CURRENCIES", "CRYPTOCURRENCIES"]
ASSET_TYPES = ["stock", "etf", "crypto", "currency", "index", "future", "fund"]
EQUITY_ONLY_ASSET_TYPES = {"stock"}
FUND_ONLY_ASSET_TYPES = {"etf", "fund"}
SUPPORTED_EQUITY_SCREENS = [
    "aggressive_small_caps",
    "day_gainers",
    "day_losers",
    "most_actives",
    "most_shorted_stocks",
    "small_cap_gainers",
    "growth_technology_stocks",
    "undervalued_growth_stocks",
    "undervalued_large_caps",
]
ASSET_TYPE_MAP = {
    "EQUITY": "stock",
    "ETF": "etf",
    "CRYPTOCURRENCY": "crypto",
    "CRYPTO": "crypto",
    "CURRENCY": "currency",
    "INDEX": "index",
    "FUTURE": "future",
    "MUTUALFUND": "fund",
    "MUTUAL FUND": "fund",
}
INTRADAY_DELTAS = {
    "1m": pd.Timedelta(minutes=1),
    "2m": pd.Timedelta(minutes=2),
    "5m": pd.Timedelta(minutes=5),
    "15m": pd.Timedelta(minutes=15),
    "30m": pd.Timedelta(minutes=30),
    "60m": pd.Timedelta(hours=1),
    "90m": pd.Timedelta(minutes=90),
    "1h": pd.Timedelta(hours=1),
    "1d": pd.Timedelta(days=1),
    "5d": pd.Timedelta(days=5),
}
INCOME_STATEMENT_FIELDS = {
    "total_revenue": ["Total Revenue"],
    "gross_profit": ["Gross Profit"],
    "operating_income": ["Operating Income"],
    "net_income": ["Net Income", "Net Income Common Stockholders"],
    "diluted_eps": ["Diluted EPS", "Basic EPS"],
    "ebitda": ["EBITDA", "Normalized EBITDA"],
}
BALANCE_SHEET_FIELDS = {
    "cash_and_equivalents": [
        "Cash And Cash Equivalents",
        "Cash Cash Equivalents And Short Term Investments",
        "Cash And Short Term Investments",
    ],
    "total_assets": ["Total Assets"],
    "total_liabilities": ["Total Liabilities Net Minority Interest", "Total Liabilities"],
    "total_debt": ["Total Debt", "Net Debt"],
    "shareholders_equity": [
        "Stockholders Equity",
        "Total Equity Gross Minority Interest",
        "Common Stock Equity",
    ],
    "working_capital": ["Working Capital"],
}
CASH_FLOW_FIELDS = {
    "operating_cash_flow": ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"],
    "capital_expenditure": ["Capital Expenditure"],
    "free_cash_flow": ["Free Cash Flow"],
    "investing_cash_flow": ["Investing Cash Flow", "Cash Flow From Continuing Investing Activities"],
    "financing_cash_flow": ["Financing Cash Flow", "Cash Flow From Continuing Financing Activities"],
    "dividends_paid": ["Cash Dividends Paid", "Common Stock Dividend Paid"],
}


class YahooFinanceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Yahoo Finance Agent",
                "version": "2.1.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Agent-friendly Yahoo Finance tools for symbol resolution, quote snapshots, normalized price history, technical analysis, news, market overview, company fundamentals, analyst views, fund snapshots, and curated equity screens.",
                "external_apis": ["Yahoo Finance"],
                "tags": ["Market Analysis"],
                "verified": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/YFinance.png",
                "examples": [
                    "Resolve the ticker for Apple",
                    "Give me a quote snapshot for BTC-USD",
                    "Get AAPL price history on 1h timeframe for 3 months",
                    "Show me a technical snapshot for TSLA",
                    "Find recent Nvidia news",
                    "What is the market overview for US equities?",
                    "Show company fundamentals for Microsoft",
                    "Give me an analyst snapshot for Amazon",
                    "Summarize the ETF SPY",
                    "Show me today's Yahoo day gainers",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 15

    def get_system_prompt(self) -> str:
        return """You are a Yahoo Finance assistant.

Use the tools with clear scope:
- `resolve_symbol` when the user gives a company name, ambiguous ticker, or asks what symbol to use
- `quote_snapshot` for the latest compact market snapshot of one symbol
- `price_history` for normalized OHLCV history
- `technical_snapshot` for technical analysis and signal summary
- `news_search` for recent news about a symbol, company, or market topic
- `market_overview` for high-level market status and benchmark summary
- `company_fundamentals` for compact equity fundamentals
- `analyst_snapshot` for compact equity analyst data
- `fund_snapshot` for normalized ETF or mutual fund data
- `equity_screen` for curated predefined equity screens

Rules:
- Use exact symbols when the user already provides them
- Prefer compact, structured outputs over raw dumps
- Be honest about unsupported asset/tool combinations
- Use the latest completed candle for technical analysis and price-history summaries
- Mention the exact symbol, interval, and resolved date window in your response
"""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "resolve_symbol",
                    "description": "Resolve a company name, ticker fragment, or market term into agent-usable Yahoo Finance symbols. Use this before other tools when the symbol is ambiguous.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Ticker, company name, or market term to resolve.",
                            },
                            "asset_type": {
                                "type": "string",
                                "enum": ASSET_TYPES,
                                "description": "Optional asset-type filter.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of matches to return.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "quote_snapshot",
                    "description": "Return a compact current snapshot for one Yahoo Finance symbol. Works best for stocks, ETFs, major crypto, indices, currencies, and futures.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Exact Yahoo Finance symbol such as AAPL, SPY, BTC-USD, EURUSD=X, or GC=F.",
                            }
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "price_history",
                    "description": "Return normalized OHLCV history with compact metadata, latest completed bar, and a limited number of bars. Use this instead of raw Yahoo Finance history dumps.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Exact Yahoo Finance symbol."},
                            "interval": {
                                "type": "string",
                                "enum": HISTORY_INTERVALS,
                                "description": "Bar interval.",
                                "default": "1d",
                            },
                            "period": {
                                "type": "string",
                                "description": "Rolling window like 5d,1mo,3mo,6mo,1y,2y,ytd,max. If start_date or end_date is provided, they take precedence.",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Inclusive start date in YYYY-MM-DD format.",
                            },
                            "end_date": {"type": "string", "description": "Exclusive end date in YYYY-MM-DD format."},
                            "include_prepost": {
                                "type": "boolean",
                                "description": "Include pre/post-market bars for eligible symbols.",
                                "default": False,
                            },
                            "repair": {
                                "type": "boolean",
                                "description": "Enable Yahoo Finance price-repair logic.",
                                "default": False,
                            },
                            "limit_bars": {
                                "type": "integer",
                                "description": "Maximum number of bars to return in the `bars` array.",
                                "default": 50,
                            },
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "technical_snapshot",
                    "description": "Return a quick technical analysis snapshot with trend, momentum, volatility, key levels, and a compact buy/sell/neutral signal.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Exact Yahoo Finance symbol."},
                            "interval": {
                                "type": "string",
                                "enum": HISTORY_INTERVALS,
                                "description": "Bar interval used for analysis.",
                                "default": "1d",
                            },
                            "period": {
                                "type": "string",
                                "description": "History window used to compute indicators. Defaults to 3mo for intraday and 1y for day-plus intervals.",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Inclusive start date in YYYY-MM-DD format.",
                            },
                            "end_date": {"type": "string", "description": "Exclusive end date in YYYY-MM-DD format."},
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "news_search",
                    "description": "Return compact recent news items for a symbol, company, asset, or market topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Symbol, company name, or news topic."},
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of news items to return.",
                                "default": 5,
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "market_overview",
                    "description": "Return market-open status and a compact benchmark summary for one supported Yahoo market region.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "market": {
                                "type": "string",
                                "enum": MARKETS,
                                "description": "Yahoo market region.",
                                "default": "US",
                            }
                        },
                        "required": ["market"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "company_fundamentals",
                    "description": "Return compact company fundamentals for one equity, including profile, earnings calendar, recent SEC filings, and summarized financial statements.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Exact Yahoo Finance equity symbol."}
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "analyst_snapshot",
                    "description": "Return a compact analyst view for one equity, including recommendations, price targets, estimates, EPS trend, and revisions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Exact Yahoo Finance equity symbol."}
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fund_snapshot",
                    "description": "Return a compact ETF or mutual-fund snapshot including description, expense ratio, asset allocation, top holdings, and exposures when available.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Exact Yahoo Finance ETF or mutual-fund symbol."}
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "equity_screen",
                    "description": "Run one curated predefined Yahoo Finance equity screen and return compact candidate rows.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "screen_name": {
                                "type": "string",
                                "enum": SUPPORTED_EQUITY_SCREENS,
                                "description": "Predefined Yahoo Finance equity screen name.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of screened candidates to return.",
                                "default": 10,
                            },
                        },
                        "required": ["screen_name"],
                    },
                },
            },
        ]

    def _normalize_symbol(self, symbol: str) -> Optional[str]:
        if not symbol or not isinstance(symbol, str):
            return None
        return symbol.strip().upper()

    def _normalize_asset_type(self, quote_type: Optional[str], type_disp: Optional[str] = None) -> Optional[str]:
        if quote_type and quote_type.upper() in ASSET_TYPE_MAP:
            return ASSET_TYPE_MAP[quote_type.upper()]
        if type_disp and type_disp.upper() in ASSET_TYPE_MAP:
            return ASSET_TYPE_MAP[type_disp.upper()]
        if type_disp:
            text = type_disp.lower()
            if "mutual" in text:
                return "fund"
            if "crypto" in text:
                return "crypto"
            if "future" in text:
                return "future"
            if "currency" in text:
                return "currency"
            if "index" in text:
                return "index"
            if "etf" in text:
                return "etf"
            if "equity" in text or "stock" in text:
                return "stock"
        return None

    def _default_period(self, interval: str) -> str:
        return "3mo" if interval in INTRADAY_INTERVALS else "1y"

    def _iso(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, (pd.Timestamp, datetime)):
            return value.isoformat()
        return str(value)

    def _safe_float(self, value: Any) -> Optional[float]:
        try:
            value = self._raw_value(value)
            if value is None or pd.isna(value):
                return None
            return float(value)
        except Exception:
            return None

    def _safe_int(self, value: Any) -> Optional[int]:
        try:
            value = self._raw_value(value)
            if value is None or pd.isna(value):
                return None
            return int(value)
        except Exception:
            return None

    def _trim_text(self, text: Optional[str], limit: int = 240) -> Optional[str]:
        if not text:
            return None
        clean = " ".join(str(text).split())
        if len(clean) <= limit:
            return clean
        return clean[: limit - 3] + "..."

    def _raw_value(self, value: Any) -> Any:
        if type(value) is dict and "raw" in value:
            return value["raw"]
        return value

    def _prune_empty(self, value: Any) -> Any:
        if type(value) is dict:
            out = {}
            for key, item in value.items():
                cleaned = self._prune_empty(item)
                if cleaned not in (None, "", [], {}):
                    out[key] = cleaned
            return out
        if type(value) is list:
            out = []
            for item in value:
                cleaned = self._prune_empty(item)
                if cleaned not in (None, "", [], {}):
                    out.append(cleaned)
            return out
        return value

    def _history_request(
        self, interval: str, period: Optional[str], start_date: Optional[str], end_date: Optional[str]
    ) -> Dict[str, Any]:
        return {
            "period": None if start_date or end_date else period or self._default_period(interval),
            "start_date": start_date,
            "end_date": end_date,
        }

    def _yfinance_error(self, exc: Exception, no_data_message: str) -> Dict[str, Any]:
        if isinstance(exc, YFRateLimitError):
            return {"status": "error", "error": "Yahoo Finance rate limited the request. Try again shortly."}
        if isinstance(exc, (YFPricesMissingError, YFTickerMissingError, YFTzMissingError)):
            return {"status": "no_data", "error": no_data_message}
        if isinstance(exc, YFInvalidPeriodError):
            return {"status": "error", "error": str(exc)}
        return {"status": "error", "error": f"Yahoo Finance request failed: {exc}"}

    def _drop_incomplete_bar(self, df: pd.DataFrame, interval: str) -> pd.DataFrame:
        if df is None or df.empty or len(df) < 2:
            return df

        last_ts = pd.Timestamp(df.index[-1])
        now = pd.Timestamp.now(tz=last_ts.tz) if last_ts.tz else pd.Timestamp.utcnow()

        if interval in INTRADAY_DELTAS:
            if now < last_ts + INTRADAY_DELTAS[interval]:
                return df.iloc[:-1]
            return df

        if interval == "1wk":
            if (last_ts.year, last_ts.isocalendar().week) == (now.year, now.isocalendar().week):
                return df.iloc[:-1]
            return df

        if interval == "1mo":
            if (last_ts.year, last_ts.month) == (now.year, now.month):
                return df.iloc[:-1]
            return df

        if interval == "3mo":
            last_quarter = (last_ts.month - 1) // 3
            now_quarter = (now.month - 1) // 3
            if (last_ts.year, last_quarter) == (now.year, now_quarter):
                return df.iloc[:-1]

        return df

    def _serialize_bars(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        out = []
        for timestamp, row in df.iterrows():
            item = {
                "timestamp": self._iso(timestamp),
                "open": self._safe_float(row.get("Open")),
                "high": self._safe_float(row.get("High")),
                "low": self._safe_float(row.get("Low")),
                "close": self._safe_float(row.get("Close")),
                "volume": self._safe_int(row.get("Volume")),
            }
            if "Repaired?" in df.columns:
                item["repaired"] = bool(row.get("Repaired?"))
            out.append(item)
        return out

    def _window_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        first_close = self._safe_float(df["Close"].iloc[0])
        last_close = self._safe_float(df["Close"].iloc[-1])
        change_abs = None
        change_pct = None
        if first_close is not None and last_close is not None and first_close != 0:
            change_abs = last_close - first_close
            change_pct = (change_abs / first_close) * 100
        volume_total = None
        if "Volume" in df.columns:
            volume_total = self._safe_int(df["Volume"].fillna(0).sum())
        repaired_count = None
        if "Repaired?" in df.columns:
            repaired_count = int(df["Repaired?"].fillna(False).astype(bool).sum())
        return {
            "open_close_change": self._safe_float(change_abs),
            "open_close_change_pct": self._safe_float(change_pct),
            "window_high": self._safe_float(df["High"].max()),
            "window_low": self._safe_float(df["Low"].min()),
            "volume_total": volume_total,
            "repaired_rows": repaired_count,
        }

    def _normalize_search_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        asset_type = self._normalize_asset_type(item.get("quoteType"), item.get("typeDisp"))
        if asset_type is None:
            return None
        name = item.get("longname") or item.get("shortname") or item.get("name")
        return {
            "symbol": item.get("symbol"),
            "name": name,
            "asset_type": asset_type,
            "exchange": item.get("exchange") or item.get("exchDisp"),
            "quote_type": item.get("quoteType"),
            "score": self._safe_float(item.get("score")),
        }

    def _normalize_news_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": item.get("uuid"),
            "title": item.get("title"),
            "publisher": item.get("publisher"),
            "published_at": self._iso(pd.to_datetime(item.get("providerPublishTime"), unit="s", utc=True))
            if item.get("providerPublishTime")
            else None,
            "url": item.get("link"),
            "content_type": item.get("type"),
            "related_tickers": item.get("relatedTickers") or [],
        }

    def _wrap_stockstats(self, ohlcv_df: pd.DataFrame) -> pd.DataFrame:
        cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in ohlcv_df.columns]
        df = ohlcv_df[cols].copy()
        df.columns = [c.lower() for c in df.columns]
        return stockstats_wrap(df)

    async def _fetch_history(
        self,
        symbol: str,
        interval: str,
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        include_prepost: bool = False,
        repair: bool = False,
    ) -> tuple[pd.DataFrame, Dict[str, Any]]:
        if interval not in HISTORY_INTERVALS:
            return pd.DataFrame(), {}

        def _do_history() -> tuple[pd.DataFrame, Dict[str, Any]]:
            ticker = yf.Ticker(symbol)
            kwargs = {
                "interval": interval,
                "auto_adjust": True,
                "prepost": include_prepost,
                "repair": repair,
                "actions": False,
                "timeout": 10,
                "raise_errors": True,
            }
            if start_date or end_date:
                kwargs["start"] = start_date
                kwargs["end"] = end_date
            else:
                kwargs["period"] = period or self._default_period(interval)

            df = ticker.history(**kwargs)
            metadata = ticker.get_history_metadata() or {}
            if df is None or df.empty:
                return pd.DataFrame(), metadata
            return df.dropna(how="all"), metadata

        return await asyncio.to_thread(_do_history)

    def _compact_profile(self, info: Dict[str, Any], asset_type: Optional[str]) -> Dict[str, Any]:
        keys = ["sector", "industry", "category", "fundFamily", "website", "country", "exchange", "market"]
        if asset_type == "crypto":
            keys = ["website", "algorithm", "name", "exchange"]

        profile = {}
        for key in keys:
            value = info.get(key)
            if value not in (None, "", [], {}):
                profile[key] = self._trim_text(value, 180) if isinstance(value, str) else value
        return profile

    def _compact_market_summary(self, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = []
        for key, value in summary.items():
            items.append(
                {
                    "key": key,
                    "symbol": value.get("symbol") or value.get("headSymbolAsString"),
                    "name": value.get("shortName"),
                    "quote_type": value.get("quoteType"),
                    "exchange": value.get("exchange"),
                    "price": self._safe_float(value.get("regularMarketPrice")),
                    "previous_close": self._safe_float(value.get("regularMarketPreviousClose")),
                    "change_pct": self._safe_float(value.get("regularMarketChangePercent")),
                }
            )
        return items[:8]

    def _asset_support_error(self, symbol: str, asset_type: Optional[str], supported_types: set[str], tool_name: str) -> Dict[str, Any]:
        supported = ", ".join(sorted(supported_types))
        actual = asset_type or "unknown"
        return {
            "status": "error",
            "error": f"{tool_name} supports only {supported}. {symbol} resolved to asset_type '{actual}'.",
        }

    def _company_card(self, symbol: str, info: Dict[str, Any]) -> Dict[str, Any]:
        quote_type = info.get("quoteType")
        return self._prune_empty(
            {
                "symbol": symbol,
                "name": info.get("shortName") or info.get("longName") or symbol,
                "asset_type": self._normalize_asset_type(quote_type, info.get("typeDisp")),
                "quote_type": quote_type,
                "exchange": info.get("exchange"),
                "currency": info.get("currency"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "market_cap": self._safe_float(info.get("marketCap")),
                "business_summary": self._trim_text(info.get("longBusinessSummary"), 320),
            }
        )

    def _compact_calendar(self, calendar: Dict[str, Any]) -> Dict[str, Any]:
        return self._prune_empty(
            {
                "earnings_date": [self._iso(value) for value in (calendar.get("Earnings Date") or [])],
                "earnings_estimate": {
                    "low": self._safe_float(calendar.get("Earnings Low")),
                    "average": self._safe_float(calendar.get("Earnings Average")),
                    "high": self._safe_float(calendar.get("Earnings High")),
                },
                "revenue_estimate": {
                    "low": self._safe_float(calendar.get("Revenue Low")),
                    "average": self._safe_float(calendar.get("Revenue Average")),
                    "high": self._safe_float(calendar.get("Revenue High")),
                },
                "dividend_date": self._iso(calendar.get("Dividend Date")),
                "ex_dividend_date": self._iso(calendar.get("Ex-Dividend Date")),
            }
        )

    def _compact_filings(self, filings: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        items = []
        for filing in filings[:limit]:
            items.append(
                self._prune_empty(
                    {
                        "date": self._iso(filing.get("date")),
                        "type": filing.get("type"),
                        "title": filing.get("title"),
                        "url": filing.get("edgarUrl"),
                        "exhibits": filing.get("exhibits"),
                    }
                )
            )
        return items

    def _statement_point_summary(self, df: pd.DataFrame, field_map: Dict[str, List[str]]) -> Dict[str, Any]:
        if df is None or df.empty or len(df.columns) == 0:
            return {}

        series = df.iloc[:, 0]
        summary = {"as_of": self._iso(df.columns[0])}
        for field_name, aliases in field_map.items():
            for alias in aliases:
                if alias in series.index:
                    summary[field_name] = self._safe_float(series[alias])
                    break
        return self._prune_empty(summary)

    def _statement_summary(
        self, annual_df: pd.DataFrame, quarterly_df: pd.DataFrame, field_map: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        return self._prune_empty(
            {
                "latest_annual": self._statement_point_summary(annual_df, field_map),
                "latest_quarterly": self._statement_point_summary(quarterly_df, field_map),
            }
        )

    def _records_from_frame(self, df: pd.DataFrame, limit: int = 4) -> List[Dict[str, Any]]:
        if df is None or df.empty:
            return []

        records = []
        for row in df.reset_index().head(limit).to_dict(orient="records"):
            item = {}
            for key, value in row.items():
                raw_value = self._raw_value(value)
                if raw_value is None or pd.isna(raw_value):
                    item[key] = None
                elif type(raw_value) in {pd.Timestamp, datetime}:
                    item[key] = self._iso(raw_value)
                elif type(raw_value) is str:
                    item[key] = raw_value
                else:
                    item[key] = self._safe_float(raw_value)
                    if item[key] is None:
                        item[key] = raw_value
            records.append(self._prune_empty(item))
        return records

    def _fund_operation_value(self, operations: pd.DataFrame, label: str) -> Optional[float]:
        if operations is None or operations.empty or label not in operations.index:
            return None
        return self._safe_float(operations.iloc[operations.index.get_loc(label), 0])

    def _normalize_top_holdings(self, holdings: pd.DataFrame, limit: int = 10) -> List[Dict[str, Any]]:
        if holdings is None or holdings.empty:
            return []

        items = []
        for row in holdings.reset_index().head(limit).to_dict(orient="records"):
            items.append(
                self._prune_empty(
                    {
                        "symbol": row.get("Symbol"),
                        "name": row.get("Name"),
                        "weight": self._safe_float(row.get("Holding Percent")),
                    }
                )
            )
        return items

    def _normalize_comparison_table(self, df: pd.DataFrame, metric_column: str, value_column: str, limit: int) -> List[Dict[str, Any]]:
        if df is None or df.empty:
            return []

        items = []
        for row in df.reset_index().head(limit).to_dict(orient="records"):
            items.append(
                self._prune_empty(
                    {
                        "metric": row.get(metric_column),
                        "fund": self._safe_float(row.get(value_column)),
                        "category_average": self._safe_float(row.get("Category Average")),
                    }
                )
            )
        return items

    def _normalize_weight_dict(self, values: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = []
        for key, value in values.items():
            items.append(self._prune_empty({"name": key, "weight": self._safe_float(value)}))
        return items

    def _normalize_screen_candidate(self, item: Dict[str, Any]) -> Dict[str, Any]:
        quote_type = item.get("quoteType")
        return self._prune_empty(
            {
                "symbol": item.get("symbol"),
                "name": item.get("shortName") or item.get("longName"),
                "asset_type": self._normalize_asset_type(quote_type, quote_type),
                "exchange": self._raw_value(item.get("exchange")),
                "price": self._safe_float(item.get("regularMarketPrice") or item.get("intradayprice")),
                "change_pct": self._safe_float(item.get("regularMarketChangePercent") or item.get("percentchange")),
                "volume": self._safe_int(item.get("regularMarketVolume") or item.get("dayvolume")),
                "market_cap": self._safe_float(item.get("marketCap") or item.get("intradaymarketcap")),
                "pe_ratio": self._safe_float(
                    item.get("trailingPE") or item.get("peRatio") or item.get("peratio.lasttwelvemonths")
                ),
                "sector": item.get("sector"),
                "industry": item.get("industry"),
            }
        )

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def resolve_symbol(self, query: str, asset_type: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        if not query or not isinstance(query, str):
            return {"status": "error", "error": "Query must be a non-empty string."}
        if asset_type is not None and asset_type not in ASSET_TYPES:
            return {"status": "error", "error": f"Unsupported asset_type '{asset_type}'."}

        def _do_search() -> List[Dict[str, Any]]:
            search = yf.Search(query, max_results=max(limit * 3, 10), news_count=0, lists_count=0, include_cb=False)
            candidates = []
            for item in search.quotes or []:
                normalized = self._normalize_search_result(item)
                if not normalized:
                    continue
                if asset_type and normalized["asset_type"] != asset_type:
                    continue
                candidates.append(normalized)
            return candidates[:limit]

        try:
            matches = await asyncio.to_thread(_do_search)
        except Exception as exc:
            return self._yfinance_error(exc, f"No symbol matches found for '{query}'.")
        if not matches:
            return {"status": "no_data", "error": f"No symbol matches found for '{query}'."}

        return {
            "status": "success",
            "data": {
                "query": query,
                "asset_type_filter": asset_type,
                "matches": matches,
            },
        }

    @with_cache(ttl_seconds=120)
    @with_retry(max_retries=1)
    async def quote_snapshot(self, symbol: str) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}

        def _do_quote() -> Dict[str, Any]:
            ticker = yf.Ticker(symbol)
            recent = ticker.history(period="5d", interval="1d", auto_adjust=True, actions=False, raise_errors=True)
            if recent is None or recent.empty:
                return {}
            fast_info = dict(ticker.fast_info)
            info = ticker.info or {}
            last_row = recent.iloc[-1]
            quote_type = info.get("quoteType") or fast_info.get("quoteType")
            asset_type = self._normalize_asset_type(quote_type, info.get("typeDisp"))
            name = info.get("shortName") or info.get("longName") or info.get("name") or symbol
            return {
                "symbol": symbol,
                "name": name,
                "asset_type": asset_type,
                "quote_type": quote_type,
                "currency": fast_info.get("currency") or info.get("currency"),
                "exchange": fast_info.get("exchange") or info.get("exchange"),
                "price": {
                    "last_price": self._safe_float(fast_info.get("lastPrice") or last_row.get("Close")),
                    "open": self._safe_float(fast_info.get("open") or last_row.get("Open")),
                    "previous_close": self._safe_float(
                        fast_info.get("previousClose") or fast_info.get("regularMarketPreviousClose")
                    ),
                    "day_high": self._safe_float(fast_info.get("dayHigh") or last_row.get("High")),
                    "day_low": self._safe_float(fast_info.get("dayLow") or last_row.get("Low")),
                    "volume": self._safe_int(fast_info.get("lastVolume") or last_row.get("Volume")),
                },
                "stats": {
                    "market_cap": self._safe_float(fast_info.get("marketCap") or info.get("marketCap")),
                    "fifty_day_average": self._safe_float(fast_info.get("fiftyDayAverage")),
                    "two_hundred_day_average": self._safe_float(fast_info.get("twoHundredDayAverage")),
                    "year_high": self._safe_float(fast_info.get("yearHigh")),
                    "year_low": self._safe_float(fast_info.get("yearLow")),
                    "year_change_pct": self._safe_float(fast_info.get("yearChange") * 100)
                    if fast_info.get("yearChange") is not None
                    else None,
                },
                "profile": self._compact_profile(info, asset_type),
                "as_of": self._iso(recent.index[-1]),
            }

        try:
            snapshot = await asyncio.to_thread(_do_quote)
        except Exception as exc:
            return self._yfinance_error(exc, f"No quote data returned for {symbol}.")
        if not snapshot:
            return {"status": "no_data", "error": f"No quote data returned for {symbol}."}
        return {"status": "success", "data": snapshot}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def price_history(
        self,
        symbol: str,
        interval: str = "1d",
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        include_prepost: bool = False,
        repair: bool = False,
        limit_bars: int = 50,
    ) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}
        if interval not in HISTORY_INTERVALS:
            return {"status": "error", "error": f"Unsupported interval '{interval}'."}

        limit_bars = max(1, min(limit_bars or 50, 250))
        try:
            df, metadata = await self._fetch_history(
                symbol=symbol,
                interval=interval,
                period=period,
                start_date=start_date,
                end_date=end_date,
                include_prepost=include_prepost,
                repair=repair,
            )
        except Exception as exc:
            return self._yfinance_error(exc, f"No historical data returned for {symbol} at {interval} interval.")

        if df.empty:
            return {"status": "no_data", "error": f"No historical data returned for {symbol} at {interval} interval."}

        completed = self._drop_incomplete_bar(df, interval)
        if completed.empty:
            completed = df

        bars = self._serialize_bars(completed.tail(limit_bars))
        latest_bar = bars[-1] if bars else None
        previous_bar = bars[-2] if len(bars) > 1 else None

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "interval": interval,
                "requested": {
                    **self._history_request(interval, period, start_date, end_date),
                    "include_prepost": include_prepost,
                    "repair": repair,
                    "limit_bars": limit_bars,
                },
                "resolved": {
                    "start": self._iso(completed.index.min()),
                    "end": self._iso(completed.index.max()),
                    "currency": metadata.get("currency"),
                    "exchange_timezone": metadata.get("exchangeTimezoneName"),
                    "instrument_type": metadata.get("instrumentType"),
                    "total_bars": len(completed),
                },
                "latest_completed_bar": latest_bar,
                "previous_completed_bar": previous_bar,
                "window_summary": self._window_summary(completed),
                "bars": bars,
            },
        }

    @with_cache(ttl_seconds=180)
    @with_retry(max_retries=1)
    async def technical_snapshot(
        self,
        symbol: str,
        interval: str = "1d",
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}
        if interval not in HISTORY_INTERVALS:
            return {"status": "error", "error": f"Unsupported interval '{interval}'."}

        try:
            df, metadata = await self._fetch_history(
                symbol=symbol,
                interval=interval,
                period=period,
                start_date=start_date,
                end_date=end_date,
                include_prepost=False,
                repair=False,
            )
        except Exception as exc:
            return self._yfinance_error(exc, f"No historical data returned for {symbol} at {interval} interval.")
        df = self._drop_incomplete_bar(df, interval)

        if df.empty or len(df) < 30:
            return {
                "status": "no_data",
                "error": f"Insufficient historical data for {symbol}. Need at least 30 completed bars.",
            }

        ss = self._wrap_stockstats(df)

        def _series(name: str) -> Optional[pd.Series]:
            try:
                return ss[name].astype(float)
            except Exception:
                return None

        close = df["Close"].astype(float)
        high = df["High"].astype(float)
        low = df["Low"].astype(float)
        rsi = _series("rsi")
        macd = _series("macd")
        macds = _series("macds")
        macdh = _series("macdh")
        boll = _series("boll")
        boll_ub = _series("boll_ub")
        boll_lb = _series("boll_lb")
        ema10 = _series("close_10_ema")
        sma50 = _series("close_50_sma")
        sma200 = _series("close_200_sma")

        last_close = self._safe_float(close.iloc[-1])
        last_rsi = self._safe_float(rsi.iloc[-1]) if rsi is not None else None
        last_macd = self._safe_float(macd.iloc[-1]) if macd is not None else None
        last_macds = self._safe_float(macds.iloc[-1]) if macds is not None else None
        last_macdh = self._safe_float(macdh.iloc[-1]) if macdh is not None else None
        last_ema10 = self._safe_float(ema10.iloc[-1]) if ema10 is not None else None
        last_sma50 = self._safe_float(sma50.iloc[-1]) if sma50 is not None else None
        last_sma200 = self._safe_float(sma200.iloc[-1]) if sma200 is not None else None
        last_boll = self._safe_float(boll.iloc[-1]) if boll is not None else None
        last_boll_ub = self._safe_float(boll_ub.iloc[-1]) if boll_ub is not None else None
        last_boll_lb = self._safe_float(boll_lb.iloc[-1]) if boll_lb is not None else None

        recent_window = df.tail(min(len(df), 20))
        support = self._safe_float(recent_window["Low"].min())
        resistance = self._safe_float(recent_window["High"].max())

        trend_score = 0
        reasons = []

        if last_close is not None and last_ema10 is not None:
            trend_score += 1 if last_close > last_ema10 else -1
            reasons.append("Price is above 10 EMA." if last_close > last_ema10 else "Price is below 10 EMA.")
        if last_close is not None and last_sma50 is not None:
            trend_score += 1 if last_close > last_sma50 else -1
            reasons.append("Price is above 50 SMA." if last_close > last_sma50 else "Price is below 50 SMA.")
        if last_close is not None and last_sma200 is not None:
            trend_score += 1 if last_close > last_sma200 else -1
            reasons.append("Price is above 200 SMA." if last_close > last_sma200 else "Price is below 200 SMA.")
        if last_macd is not None and last_macds is not None:
            trend_score += 1 if last_macd > last_macds else -1
            reasons.append("MACD is above signal." if last_macd > last_macds else "MACD is below signal.")
        if last_rsi is not None:
            if last_rsi >= 55:
                trend_score += 1
                reasons.append("RSI shows bullish momentum.")
            elif last_rsi <= 45:
                trend_score -= 1
                reasons.append("RSI shows bearish momentum.")

        if trend_score >= 3:
            action = "buy"
            trend = "bullish"
        elif trend_score <= -3:
            action = "sell"
            trend = "bearish"
        else:
            action = "neutral"
            trend = "mixed"

        confidence = min(0.9, 0.45 + (abs(trend_score) * 0.08))

        if last_rsi is None:
            momentum = "unknown"
        elif last_rsi >= 70:
            momentum = "overbought"
        elif last_rsi <= 30:
            momentum = "oversold"
        elif last_rsi >= 55:
            momentum = "bullish"
        elif last_rsi <= 45:
            momentum = "bearish"
        else:
            momentum = "neutral"

        volatility = "unknown"
        if last_boll_ub is not None and last_boll_lb is not None and last_close is not None and last_close != 0:
            band_width = (last_boll_ub - last_boll_lb) / last_close
            if band_width >= 0.12:
                volatility = "high"
            elif band_width >= 0.06:
                volatility = "medium"
            else:
                volatility = "low"

        macd_state = None
        if last_macd is not None and last_macds is not None:
            macd_state = "bullish" if last_macd > last_macds else "bearish"

        bollinger_position = None
        if last_close is not None and last_boll_ub is not None and last_boll_lb is not None:
            if last_close > last_boll_ub:
                bollinger_position = "above_upper_band"
            elif last_close < last_boll_lb:
                bollinger_position = "below_lower_band"
            else:
                bollinger_position = "within_bands"

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "interval": interval,
                "requested": self._history_request(interval, period, start_date, end_date),
                "resolved": {
                    "start": self._iso(df.index.min()),
                    "end": self._iso(df.index.max()),
                    "currency": metadata.get("currency"),
                    "instrument_type": metadata.get("instrumentType"),
                    "bar_count_used": len(df),
                },
                "as_of": self._iso(df.index[-1]),
                "price": {
                    "close": last_close,
                    "support": support,
                    "resistance": resistance,
                },
                "indicators": {
                    "rsi_14": last_rsi,
                    "macd": last_macd,
                    "macd_signal": last_macds,
                    "macd_histogram": last_macdh,
                    "ema_10": last_ema10,
                    "sma_50": last_sma50,
                    "sma_200": last_sma200,
                    "bollinger_middle": last_boll,
                    "bollinger_upper": last_boll_ub,
                    "bollinger_lower": last_boll_lb,
                },
                "states": {
                    "trend": trend,
                    "momentum": momentum,
                    "volatility": volatility,
                    "macd_state": macd_state,
                    "bollinger_position": bollinger_position,
                },
                "signal": {
                    "action": action,
                    "confidence": round(confidence, 2),
                    "rationale": reasons[:5],
                },
            },
        }

    @with_cache(ttl_seconds=180)
    @with_retry(max_retries=1)
    async def news_search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        if not query or not isinstance(query, str):
            return {"status": "error", "error": "Query must be a non-empty string."}

        limit = max(1, min(limit or 5, 10))

        def _do_search() -> List[Dict[str, Any]]:
            search = yf.Search(query, max_results=5, news_count=limit, include_cb=False)
            return [self._normalize_news_item(item) for item in (search.news or [])[:limit]]

        try:
            items = await asyncio.to_thread(_do_search)
        except Exception as exc:
            return self._yfinance_error(exc, f"No recent news found for '{query}'.")
        if not items:
            return {"status": "no_data", "error": f"No recent news found for '{query}'."}

        return {
            "status": "success",
            "data": {
                "query": query,
                "total_items": len(items),
                "items": items,
            },
        }

    @with_cache(ttl_seconds=120)
    @with_retry(max_retries=1)
    async def market_overview(self, market: str = "US") -> Dict[str, Any]:
        market = market.upper().strip()
        if market not in MARKETS:
            return {
                "status": "error",
                "error": f"Unsupported market '{market}'. Supported markets: {MARKETS}.",
            }

        def _do_market() -> Dict[str, Any]:
            yf_market = yf.Market(market)
            status = yf_market.status
            summary = yf_market.summary
            return {
                "market": market,
                "status": {
                    "name": status.get("name"),
                    "status": status.get("status"),
                    "message": status.get("message"),
                    "open": status.get("open"),
                    "close": status.get("close"),
                    "timezone": status.get("timezone", {}).get("$text")
                    if isinstance(status.get("timezone"), dict)
                    else None,
                },
                "benchmarks": self._compact_market_summary(summary),
            }

        try:
            overview = await asyncio.to_thread(_do_market)
        except Exception as exc:
            return self._yfinance_error(exc, f"No market overview returned for '{market}'.")
        return {"status": "success", "data": overview}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def company_fundamentals(self, symbol: str) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}

        def _do_company() -> Dict[str, Any]:
            ticker = yf.Ticker(symbol)
            info = ticker.info or {}
            asset_type = self._normalize_asset_type(info.get("quoteType"), info.get("typeDisp"))
            if not info and asset_type is None:
                return {}
            if asset_type not in EQUITY_ONLY_ASSET_TYPES:
                return {"asset_type": asset_type}

            return {
                "company": self._company_card(symbol, info),
                "calendar": self._compact_calendar(ticker.calendar or {}),
                "recent_filings": self._compact_filings(ticker.sec_filings or []),
                "financial_summary": self._prune_empty(
                    {
                        "currency": info.get("currency"),
                        "income_statement": self._statement_summary(
                            ticker.income_stmt, ticker.quarterly_income_stmt, INCOME_STATEMENT_FIELDS
                        ),
                        "balance_sheet": self._statement_summary(
                            ticker.balance_sheet, ticker.quarterly_balance_sheet, BALANCE_SHEET_FIELDS
                        ),
                        "cash_flow": self._statement_summary(
                            ticker.cashflow, ticker.quarterly_cashflow, CASH_FLOW_FIELDS
                        ),
                    }
                ),
            }

        try:
            fundamentals = await asyncio.to_thread(_do_company)
        except Exception as exc:
            return self._yfinance_error(exc, f"No company fundamentals returned for {symbol}.")

        if not fundamentals:
            return {"status": "no_data", "error": f"No company fundamentals returned for {symbol}."}
        if "asset_type" in fundamentals:
            return self._asset_support_error(symbol, fundamentals.get("asset_type"), EQUITY_ONLY_ASSET_TYPES, "company_fundamentals")
        return {"status": "success", "data": self._prune_empty(fundamentals)}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def analyst_snapshot(self, symbol: str) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}

        def _do_analyst() -> Dict[str, Any]:
            ticker = yf.Ticker(symbol)
            info = ticker.info or {}
            asset_type = self._normalize_asset_type(info.get("quoteType"), info.get("typeDisp"))
            if not info and asset_type is None:
                return {}
            if asset_type not in EQUITY_ONLY_ASSET_TYPES:
                return {"asset_type": asset_type}

            return {
                "company": self._company_card(symbol, info),
                "recommendations_summary": self._records_from_frame(ticker.recommendations_summary, limit=4),
                "price_targets": self._prune_empty(
                    {
                        "current": self._safe_float((ticker.analyst_price_targets or {}).get("current")),
                        "low": self._safe_float((ticker.analyst_price_targets or {}).get("low")),
                        "mean": self._safe_float((ticker.analyst_price_targets or {}).get("mean")),
                        "median": self._safe_float((ticker.analyst_price_targets or {}).get("median")),
                        "high": self._safe_float((ticker.analyst_price_targets or {}).get("high")),
                    }
                ),
                "earnings_estimate": self._records_from_frame(ticker.earnings_estimate, limit=4),
                "revenue_estimate": self._records_from_frame(ticker.revenue_estimate, limit=4),
                "eps_trend": self._records_from_frame(ticker.eps_trend, limit=4),
                "eps_revisions": self._records_from_frame(ticker.eps_revisions, limit=4),
            }

        try:
            snapshot = await asyncio.to_thread(_do_analyst)
        except Exception as exc:
            return self._yfinance_error(exc, f"No analyst data returned for {symbol}.")

        if not snapshot:
            return {"status": "no_data", "error": f"No analyst data returned for {symbol}."}
        if "asset_type" in snapshot:
            return self._asset_support_error(symbol, snapshot.get("asset_type"), EQUITY_ONLY_ASSET_TYPES, "analyst_snapshot")
        return {"status": "success", "data": self._prune_empty(snapshot)}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=1)
    async def fund_snapshot(self, symbol: str) -> Dict[str, Any]:
        symbol = self._normalize_symbol(symbol)
        if symbol is None:
            return {"status": "error", "error": "Symbol must be a non-empty string."}

        def _do_fund() -> Dict[str, Any]:
            ticker = yf.Ticker(symbol)
            info = ticker.info or {}
            funds = ticker.funds_data
            asset_type = self._normalize_asset_type(funds.quote_type(), info.get("typeDisp"))
            if not info and asset_type is None:
                return {}
            if asset_type not in FUND_ONLY_ASSET_TYPES:
                return {"asset_type": asset_type}

            operations = funds.fund_operations
            style_metrics = []
            if not funds.equity_holdings.empty:
                style_metrics = self._normalize_comparison_table(funds.equity_holdings, "Average", symbol, 6)
            elif not funds.bond_holdings.empty:
                style_metrics = self._normalize_comparison_table(funds.bond_holdings, "Average", symbol, 3)

            return {
                "fund": self._prune_empty(
                    {
                        "symbol": symbol,
                        "name": info.get("shortName") or info.get("longName") or symbol,
                        "asset_type": asset_type,
                        "quote_type": funds.quote_type(),
                        "exchange": info.get("exchange"),
                        "currency": info.get("currency"),
                        "category": (funds.fund_overview or {}).get("categoryName"),
                        "family": (funds.fund_overview or {}).get("family") or info.get("fundFamily"),
                        "legal_type": (funds.fund_overview or {}).get("legalType"),
                        "description": self._trim_text(funds.description, 320),
                        "expense_ratio": self._fund_operation_value(operations, "Annual Report Expense Ratio"),
                        "annual_holdings_turnover": self._fund_operation_value(operations, "Annual Holdings Turnover"),
                        "total_net_assets": self._fund_operation_value(operations, "Total Net Assets"),
                    }
                ),
                "asset_allocation": self._normalize_weight_dict(funds.asset_classes or {}),
                "top_holdings": self._normalize_top_holdings(funds.top_holdings),
                "sector_exposure": self._normalize_weight_dict(funds.sector_weightings or {}),
                "style_metrics": style_metrics,
            }

        try:
            snapshot = await asyncio.to_thread(_do_fund)
        except Exception as exc:
            return self._yfinance_error(exc, f"No fund data returned for {symbol}.")

        if not snapshot:
            return {"status": "no_data", "error": f"No fund data returned for {symbol}."}
        if "asset_type" in snapshot:
            return self._asset_support_error(symbol, snapshot.get("asset_type"), FUND_ONLY_ASSET_TYPES, "fund_snapshot")
        return {"status": "success", "data": self._prune_empty(snapshot)}

    @with_cache(ttl_seconds=180)
    @with_retry(max_retries=1)
    async def equity_screen(self, screen_name: str, limit: int = 10) -> Dict[str, Any]:
        if not screen_name or not isinstance(screen_name, str):
            return {"status": "error", "error": "screen_name must be a non-empty string."}
        if screen_name not in SUPPORTED_EQUITY_SCREENS:
            return {
                "status": "error",
                "error": f"Unsupported screen_name '{screen_name}'. Supported screens: {SUPPORTED_EQUITY_SCREENS}.",
            }

        limit = max(1, min(limit or 10, 25))

        def _do_screen() -> Dict[str, Any]:
            response = yf.screen(screen_name, count=limit)
            quotes = response.get("quotes") or []
            return {
                "screen": screen_name,
                "title": response.get("title"),
                "description": self._trim_text(response.get("description"), 220),
                "total_candidates": response.get("total"),
                "returned_candidates": len(quotes[:limit]),
                "candidates": [self._normalize_screen_candidate(item) for item in quotes[:limit]],
            }

        try:
            screen = await asyncio.to_thread(_do_screen)
        except Exception as exc:
            return self._yfinance_error(exc, f"No screen data returned for '{screen_name}'.")

        if not screen.get("candidates"):
            return {"status": "no_data", "error": f"No screen data returned for '{screen_name}'."}
        return {"status": "success", "data": self._prune_empty(screen)}

    async def fetch_price_history(
        self,
        symbol: str,
        interval: str = "1d",
        period: Optional[str] = "6mo",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self.price_history(
            symbol=symbol,
            interval=interval,
            period=period,
            start_date=start_date,
            end_date=end_date,
            include_prepost=False,
            repair=False,
            limit_bars=200,
        )

    async def indicator_snapshot(
        self,
        symbol: str,
        interval: str = "1d",
        period: str = "6mo",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self.technical_snapshot(
            symbol=symbol,
            interval=interval,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"[yahoo_finance] Handling tool call: {tool_name} args={function_args}")

        try:
            if tool_name == "resolve_symbol":
                result = await self.resolve_symbol(
                    query=function_args.get("query"),
                    asset_type=function_args.get("asset_type"),
                    limit=function_args.get("limit", 5),
                )
            elif tool_name == "quote_snapshot":
                result = await self.quote_snapshot(symbol=function_args.get("symbol"))
            elif tool_name in {"price_history", "fetch_price_history"}:
                result = await self.price_history(
                    symbol=function_args.get("symbol"),
                    interval=function_args.get("interval", "1d"),
                    period=function_args.get("period"),
                    start_date=function_args.get("start_date"),
                    end_date=function_args.get("end_date"),
                    include_prepost=function_args.get("include_prepost", False),
                    repair=function_args.get("repair", False),
                    limit_bars=function_args.get("limit_bars", 50),
                )
            elif tool_name in {"technical_snapshot", "indicator_snapshot"}:
                result = await self.technical_snapshot(
                    symbol=function_args.get("symbol"),
                    interval=function_args.get("interval", "1d"),
                    period=function_args.get("period"),
                    start_date=function_args.get("start_date"),
                    end_date=function_args.get("end_date"),
                )
            elif tool_name == "news_search":
                result = await self.news_search(
                    query=function_args.get("query"),
                    limit=function_args.get("limit", 5),
                )
            elif tool_name == "market_overview":
                result = await self.market_overview(market=function_args.get("market", "US"))
            elif tool_name == "company_fundamentals":
                result = await self.company_fundamentals(symbol=function_args.get("symbol"))
            elif tool_name == "analyst_snapshot":
                result = await self.analyst_snapshot(symbol=function_args.get("symbol"))
            elif tool_name == "fund_snapshot":
                result = await self.fund_snapshot(symbol=function_args.get("symbol"))
            elif tool_name == "equity_screen":
                result = await self.equity_screen(
                    screen_name=function_args.get("screen_name"),
                    limit=function_args.get("limit", 10),
                )
            else:
                return {"error": f"Unsupported tool: {tool_name}"}

            if errors := self._handle_error(result):
                return errors
            return result
        except Exception as e:
            logger.exception(f"[yahoo_finance] Tool execution failed: {e}")
            return {"status": "error", "error": f"Unhandled exception: {e}"}
