import asyncio
import os
import logging
from typing import Any, Dict, List, Optional, Tuple

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


def _pct(x: float) -> float:
    return x * 100.0


def _fmt_pct(x: float, places: int = 4) -> str:
    return f"{_pct(x):.{places}f}%"


class FundingRateAgent(MeshAgent):
    """
    Use Binance USDⓈ-M Futures public endpoints.

    Endpoints used (public, no key):
      - Exchange Info:          GET /fapi/v1/exchangeInfo
      - Mark Price (all/one):   GET /fapi/v1/premiumIndex
      - Funding Info:           GET /fapi/v1/fundingInfo
      - Funding Rate History:   GET /fapi/v1/fundingRate
      - Open Interest (point):  GET /fapi/v1/openInterest     [not required, but handy]
      - OI Statistics (4h):     GET /futures/data/openInterestHist

    Strategy:
      - Verify symbol exists on Binance perp via exchangeInfo
      - OI: fetch 7d of 4h bars, summarize trend + snapshot
      - Funding: use premiumIndex.lastFundingRate as "current"; derive fundingIntervalHours
                 from fundingInfo when present; otherwise infer from fundingRate timestamps;
                 otherwise default to 8h. Compute APR.
    """

    def __init__(self, base_url: Optional[str] = None):
        super().__init__()

        # Allow proxy override.
        # If env BINANCE_FAPI_BASE_URL is set, it wins. Otherwise use argument, then official host.
        self.base_url = os.getenv("BINANCE_FAPI_BASE_URL") or "https://fapi.binance.com"

        self.metadata.update(
            {
                "name": "Funding Rate Agent",
                "version": "2.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Fetches Binance USDⓈ‑M funding & open interest, summarizes OI trends, and computes APR from funding intervals.",
                "external_apis": ["Binance USDⓈ‑M Futures"],
                "tags": ["Arbitrage", "Funding", "Open Interest"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/FundingRate.png",
                "examples": [
                    "Get OI trend and funding APR for BTC",
                    "What is the current funding rate APR for SOL on Binance?",
                    "List current Binance funding rates (interval-aware)",
                    "Spot-perp carry candidates on Binance with funding > 0.02% per interval",
                ],
            }
        )

    # ---------------------------------------------------------------------
    # Identity / Prompt
    # ---------------------------------------------------------------------
    def get_system_prompt(self) -> str:
        return """
IDENTITY:
You specialize in Binance USDⓈ-M funding rates and open interest.

CAPABILITIES:
- Get latest funding rates and convert to APR based on each symbol's funding interval
- Fetch and summarize 7-day 4h Open Interest trends per symbol
- Identify spot-perp carry candidates on Binance (positive funding)

RESPONSE GUIDELINES:
- Format funding rates as percentages with 4 decimal places (e.g., "0.0123%")
- Include the funding interval in hours when presenting APR
- Summarize OI trends into clear statements (up/down/sideways), include latest OI and 24h change
"""

    # ---------------------------------------------------------------------
    # MCP Tools
    # ---------------------------------------------------------------------
    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_all_funding_rates",
                    "description": "Get current funding rates for major Binance perpetual symbols: BTC, ETH, SOL, BNB, XRP. Useful to identify overall perp market situation.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_symbol_funding_rates",
                    "description": "Get the latest funding rate and APR for a specific Binance perp symbol",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Asset ticker or full symbol (e.g., BTC or BTCUSDT)"},
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_symbol_oi_and_funding",
                    "description": "Get 7d 4h Open Interest trend summary + latest funding rate and APR for a symbol on Binance perp.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "Asset ticker or full symbol (e.g., BTC or BTCUSDT)"},
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "find_spot_futures_opportunities",
                    "description": "On Binance: list symbols with positive funding rates above a threshold (carry candidates).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min_funding_rate": {"type": "number", "description": "Per-interval threshold, default 0.0003"},
                        },
                        "required": [],
                    },
                },
            }
        ]

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None, use_data_host: bool = False) -> Any:
        base = self.base_url
        url = f"{base}{path}"
        return await self._api_request(url=url, method="GET", params=params or {})

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=2)
    async def _premium_index(self, symbol: Optional[str] = None) -> Any:
        params = {"symbol": symbol} if symbol else None
        return await self._get("/fapi/v1/premiumIndex", params=params)

    @with_cache(ttl_seconds=14400)
    @with_retry(max_retries=2)
    async def _funding_info_all(self) -> List[Dict[str, Any]]:
        # fundingInfo returns only symbols that had adjustments; we’ll filter locally.
        res = await self._get("/fapi/v1/fundingInfo")
        return res if isinstance(res, list) else []

    @with_cache(ttl_seconds=14400)
    @with_retry(max_retries=2)
    async def _funding_rate_history(self, symbol: str, limit: int = 2) -> List[Dict[str, Any]]:
        params = {"symbol": symbol, "limit": limit}
        res = await self._get("/fapi/v1/fundingRate", params=params)
        return res if isinstance(res, list) else []

    async def _infer_interval_hours(self, symbol: str) -> int:
        """
        1) Try fundingInfo.fundingIntervalHours
        2) Else infer from last 2 fundingRate timestamps
        3) Else default 8h
        """
        # 1) fundingInfo, when exists
        info_list = await self._funding_info_all()
        for row in info_list:
            if row.get("symbol") == symbol and "fundingIntervalHours" in row:
                return int(row["fundingIntervalHours"])

        # 2) infer from history
        hist = await self._funding_rate_history(symbol, limit=3)
        if len(hist) >= 2:
            t2 = int(hist[-1].get("fundingTime", 0))
            t1 = int(hist[-2].get("fundingTime", 0))
            if t1 and t2:
                hours = max(1, round((t2 - t1) / 3_600_000))
                # Clamp to common values
                if hours in (1, 2, 4, 6, 8, 12):
                    return hours
                # nearest typical
                for cand in (1, 2, 4, 6, 8, 12):
                    if abs(hours - cand) <= 1:
                        return cand

        # 3) default
        return 8

    def _apr_from_rate(self, per_interval_rate: float, interval_hours: int) -> Tuple[float, int]:
        """
        per_interval_rate is a decimal (e.g., 0.0005 = 0.05%).
        Returns (apr, intervals_per_year)
        """
        intervals_per_day = 24.0 / float(interval_hours)
        intervals_per_year = intervals_per_day * 365.0
        apr = per_interval_rate * intervals_per_year
        return apr, int(round(intervals_per_year))

    @with_retry(max_retries=2)
    async def _oi_hist_4h_7d(self, symbol: str) -> List[Dict[str, Any]]:
        # 7 days * 24h / 4h = 42 bars
        params = {"symbol": symbol, "period": "4h", "limit": 42}
        res = await self._get("/futures/data/openInterestHist", params=params, use_data_host=True)
        return res if isinstance(res, list) else []

    def _summarize_oi(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Transform 4h OI series into compact features/trend for LLM consumption.
        Uses sumOpenInterestValue (USDⓈ notionals).
        """
        if not rows:
            return {"status": "no_data", "message": "No OI data available for the past 7 days."}

        # Keep chronological order; Binance returns ascending for /futures/data/*
        def f(x): return float(x) if x is not None else 0.0

        vals = [f(r.get("sumOpenInterestValue")) for r in rows if "sumOpenInterestValue" in r]
        times = [int(r.get("timestamp", 0)) for r in rows]
        n = len(vals)
        first, last = vals[0], vals[-1]
        change_abs = last - first
        change_pct = (change_abs / first) if first else 0.0
        high, low = max(vals), min(vals)
        hi_ix, lo_ix = vals.index(high), vals.index(low)

        # Simple slope via last-first over span (per day)
        span_days = max(1.0, (times[-1] - times[0]) / (1000.0 * 60 * 60 * 24))
        daily_slope = change_abs / span_days

        # 24h change (last 6 bars ~ 24h)
        if n >= 7:
            day_ago = vals[-7]
            change_24h_abs = last - day_ago
            change_24h_pct = (change_24h_abs / day_ago) if day_ago else 0.0
        else:
            change_24h_abs = 0.0
            change_24h_pct = 0.0

        # Trend label
        if abs(change_pct) >= 0.10:
            trend = "uptrend" if change_pct > 0 else "downtrend"
        elif abs(change_pct) >= 0.04:
            trend = "mild " + ("uptrend" if change_pct > 0 else "downtrend")
        else:
            trend = "sideways"

        return {
            "status": "success",
            "trend_label": trend,
            "latest_oi": last,
            "change_7d_abs": change_abs,
            "change_7d_pct": change_pct,
            "change_24h_abs": change_24h_abs,
            "change_24h_pct": change_24h_pct,
            "high": {"value": high, "time": times[hi_ix]},
            "low": {"value": low, "time": times[lo_ix]},
            "daily_slope_abs": daily_slope,
            "points": n,
        }

    # ---------------------------------------------------------------------
    # Public Tool Methods
    # ---------------------------------------------------------------------
    @with_cache(ttl_seconds=90)
    @with_retry(max_retries=2)
    async def get_all_funding_rates(self) -> Dict[str, Any]:
        """
        Return funding rates for top 5 Binance USDⓈ-M tokens (BTC, ETH, SOL, BNB, XRP).
        Fetches in parallel with individual error handling.
        Format: ["symbol", rate_decimal, "intervalH"]
        """
        # Top 5 tokens to track
        top_tokens = ["BTC", "ETH", "SOL", "BNB", "XRP"]

        async def fetch_token_funding(token: str) -> Optional[List]:
            """Fetch funding rate for a single token with error handling."""
            try:
                result = await self.get_symbol_funding_rates(token)
                if result.get("status") == "success":
                    data = result.get("data", {})
                    symbol = data.get("symbol")
                    funding = data.get("funding", {})
                    rate = funding.get("latest_rate", 0.0)
                    interval = funding.get("interval_hours", 8)
                    logger.info(f"Successfully fetched funding rate for {token}: {rate * 100:.6f}%")
                    return [symbol, rate, f"{interval}h"]
                else:
                    logger.warning(f"Could not resolve symbol for {token}: {result.get('message', 'Unknown error')}")
                    return None
            except Exception as e:
                logger.warning(f"Error fetching funding rate for {token}: {str(e)}")
                return None

        try:
            logger.info("Fetching funding rates for top 5 tokens in parallel")
            # Fetch all tokens in parallel
            tasks = [fetch_token_funding(token) for token in top_tokens]
            results = await asyncio.gather(*tasks)

            # Filter out None results (failed fetches) and build formatted list
            formatted = [result for result in results if result is not None]

            # Sort by absolute rate descending
            formatted.sort(key=lambda x: abs(x[1]), reverse=True)

            return {"rates": formatted, "format": ["symbol", "rate", "interval"]}

        except Exception as e:
            logger.exception("get_all_funding_rates failed")
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=90)
    @with_retry(max_retries=2)
    async def get_symbol_funding_rates(self, symbol: str) -> Dict[str, Any]:
        """
        Latest funding rate and APR for a single symbol.
        Accepts 'BTC' or 'BTCUSDT'. Directly fetches data and returns friendly error if market doesn't exist.
        Always uses USDT as quote asset.
        """
        try:
            # Normalize symbol to standard format
            s = (symbol or "").upper().replace("PERP", "").replace("-PERP", "").strip()

            # If not already a full symbol, construct it with USDT
            if not s.endswith("USDT") and not s.endswith("USDC"):
                resolved = f"{s}USDT"
            else:
                resolved = s

            # Try to fetch data directly - if market doesn't exist, API will return error
            prem = await self._premium_index(resolved)

            # Check if API returned valid data
            if not isinstance(prem, dict):
                return {
                    "status": "no_data",
                    "message": f"Unable to fetch funding rate for '{symbol}'. "
                               f"Binance may not have a perpetual market for this token."
                }

            if prem.get("symbol") != resolved:
                return {
                    "status": "no_data",
                    "message": f"Symbol '{symbol}' (resolved as '{resolved}') not found. "
                               f"Binance may not have a perpetual market for this token."
                }

            last_rate = float(prem.get("lastFundingRate", 0.0) or 0.0)
            interval_h = await self._infer_interval_hours(resolved)
            apr, intervals_year = self._apr_from_rate(last_rate, interval_h)

            result = {
                "status": "success",
                "data": {
                    "symbol": resolved,
                    "funding": {
                        "latest_rate": last_rate,
                        "latest_rate_pct": _fmt_pct(last_rate, 4),
                        "interval_hours": interval_h,
                        "apr": apr,
                        "apr_pct": _fmt_pct(apr, 2),
                        "intervals_per_year": intervals_year,
                    },
                },
            }
            return result

        except Exception as e:
            logger.exception("get_symbol_funding_rates failed")
            return {
                "status": "error",
                "message": f"Failed to fetch funding rate for '{symbol}'. "
                          f"Binance may not have a perpetual market for this token, or there was an API error.",
                "error": str(e)
            }

    @with_cache(ttl_seconds=180)
    @with_retry(max_retries=2)
    async def get_symbol_oi_and_funding(self, symbol: str) -> Dict[str, Any]:
        """
        Combined view for a symbol:
          - OI trend summary (7d, 4h bars)
          - Funding snapshot + APR
        Always uses USDT as quote asset.

        If symbol is not available on Binance perp, returns the error from get_symbol_funding_rates.
        If OI data is not available, returns funding data with a friendly OI message.
        """
        try:
            funding = await self.get_symbol_funding_rates(symbol)
            if funding.get("status") != "success":
                # Reuse the friendly error message from get_symbol_funding_rates
                return funding

            # Get the resolved symbol from funding result
            resolved = funding["data"]["symbol"]

            # OI 4h × 7d
            oi_rows = await self._oi_hist_4h_7d(resolved)
            oi_summary = self._summarize_oi(oi_rows)

            # Friendly textual summary for OI
            oi_text = f"Open Interest data is not available for {resolved} on Binance perp."
            if oi_summary.get("status") == "success":
                latest = oi_summary["latest_oi"]
                c7 = oi_summary["change_7d_pct"]
                c24 = oi_summary["change_24h_pct"]
                high = oi_summary["high"]["value"]
                low = oi_summary["low"]["value"]
                label = oi_summary["trend_label"]
                oi_text = (
                    f"Open interest trend is {label}: latest ≈ {latest:,.0f} USD. "
                    f"7d change: {_fmt_pct(c7, 2)}, 24h: {_fmt_pct(c24, 2)}. "
                    f"Range over 7d: low {low:,.0f} – high {high:,.0f}. "
                )

            out = {
                "status": "success",
                "data": {
                    "symbol": resolved,
                    "funding": funding["data"]["funding"],
                    "open_interest": {
                        "summary": oi_summary,
                        "text": oi_text,
                        "period": "7d",
                        "interval": "4h",
                    },
                },
            }
            return out

        except Exception as e:
            logger.exception("get_symbol_oi_and_funding failed")
            return {"status": "error", "error": str(e)}

    @with_cache(ttl_seconds=90)
    @with_retry(max_retries=2)
    async def find_spot_futures_opportunities(self, min_funding_rate: float = 0.0003) -> Dict[str, Any]:
        """
        On Binance only: list symbols whose latest per-interval funding >= threshold.
        """
        try:
            all_rates = await self.get_all_funding_rates()
            if "rates" not in all_rates:
                return all_rates

            positives = [
                {
                    "symbol": sym,
                    "funding_rate": rate,
                    "funding_rate_pct": _fmt_pct(rate, 4),
                    "funding_interval": interval,
                }
                for sym, rate, interval in all_rates["rates"]
                if rate >= min_funding_rate
            ]
            return {"status": "success", "data": {"spot_futures_opportunities": positives}}

        except Exception as e:
            logger.exception("find_spot_futures_opportunities failed")
            return {"status": "error", "error": str(e)}

    # ---------------------------------------------------------------------
    # Tool dispatcher
    # ---------------------------------------------------------------------
    async def _handle_tool_logic(self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "get_all_funding_rates":
            return await self.get_all_funding_rates()

        if tool_name == "get_symbol_funding_rates":
            symbol = function_args.get("symbol")
            if not symbol:
                return {"error": "Missing 'symbol' parameter"}
            return await self.get_symbol_funding_rates(symbol)

        if tool_name == "get_symbol_oi_and_funding":
            symbol = function_args.get("symbol")
            if not symbol:
                return {"error": "Missing 'symbol' parameter"}
            return await self.get_symbol_oi_and_funding(symbol)

        if tool_name == "find_spot_futures_opportunities":
            min_rate = function_args.get("min_funding_rate", 0.0003)
            return await self.find_spot_futures_opportunities(min_rate)

        return {"error": f"Unsupported tool: {tool_name}"}
