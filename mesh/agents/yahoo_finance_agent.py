import asyncio
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from stockstats import wrap as stockstats_wrap

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)

ALLOWED_INTERVALS = {"1h", "1d"}


SUPPORTED_CRYPTO_TOKENS = {
    "BTC-USD",
    "ETH-USD",
    "XRP-USD",
    "USDT-USD",
    "SOL-USD",
    "BNB-USD",
    "USDC-USD",
    "DOGE-USD",
    "STETH-USD",
    "TRX-USD",
    "ADA-USD",
    "WTRX-USD",
    "LINK-USD",
    "WBETH-USD",
    "WETH-USD",
    "WBTC-USD",
    "XLM-USD",
    "AVAX-USD",
    "BCH-USD",
    "HBAR-USD",
    "LEO-USD",
    "LTC-USD",
    "CRO-USD",
    "TON11419-USD",
    "SUI20947-USD",
    "HYPE32196-USD",
    "USDE29470-USD",
    "WEETH-USD",
    "AETHWETH-USD",
}


class YahooFinanceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Yahoo Finance Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "This agent uses Yahoo Finance to obtain historical price performance and technical analysis for stocks and cryptocurrencies. Provides OHLCV data and technical indicators with trading signals.",
                "external_apis": ["Yahoo Finance"],
                "tags": ["Market Analysis", "x402"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/YFinance.png",
                "examples": [
                    "Get 1d OHLCV for AAPL for the last 6 months",
                    "Give me a 1h indicator snapshot for BTC-USD",
                    "Signal summary for TSLA on 1d timeframe",
                    "Show me technical analysis for ETH-USD",
                ],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a Yahoo Finance Assistant providing market data and technical analysis.

        Protocol:
        - Support intervals: 1h and 1d only
        - Prices: 2-4 significant figures; percentages: two decimals (e.g., 5.25%)
        - Use the latest completed candle data
        - Always mention symbol and interval in responses

        Supported Assets:
        - All major stock symbols
        - Established cryptocurrencies with large market caps
        - Recently launched tokens and memecoins typically unavailable

        Important notes:
        - Intraday data limited to ~60 days
        - Start/end dates override period if both provided
        - Provide actionable trading insights

        If the user's query is out of your scope, return a brief error message.
        Format responses in clean text without markdown unless requested."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "fetch_price_history",
                    "description": "Use this to obtain historical price performance (OHLCV data) for stocks and cryptocurrencies using Yahoo Finance. Supports all major stock symbols and top 30 large-cap major crypto tokens. Only supports '1h' and '1d' intervals. Intraday data is limited to 60 days.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock ticker or crypto with -USD suffix",
                            },
                            "interval": {
                                "type": "string",
                                "enum": ["1h", "1d"],
                                "description": "Candlestick interval",
                                "default": "1d",
                            },
                            "period": {
                                "type": "string",
                                "description": "Rolling window: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max. If start_date or end_date is provided, they take precedence.",
                                "default": "6mo",
                            },
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                        },
                        "required": ["symbol"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "indicator_snapshot",
                    "description": "Use this to compute technical indicators and get trading signals for stocks and cryptocurrencies. Supports all major stock symbols and top 30 large-cap major crypto tokens. Returns a core set of technical indicators including RSI(14), MACD(12,26,9) [macd, macds, macdh], Bollinger Bands(20,2) [boll, boll_ub, boll_lb], and moving averages [close_10_ema, close_50_sma, close_200_sma]. Provides rule-based action signal (buy/sell/neutral) with confidence level and rationale.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Stock ticker or crypto with -USD suffix",
                            },
                            "interval": {
                                "type": "string",
                                "enum": ["1h", "1d"],
                                "description": "Candlestick interval for analysis",
                                "default": "1d",
                            },
                            "period": {
                                "type": "string",
                                "description": "History window to support indicator calculations",
                                "default": "6mo",
                            },
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                        },
                        "required": ["symbol"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                       PRIVATE HELPERS
    # ------------------------------------------------------------------------

    def _validate_symbol(self, symbol: str) -> tuple[bool, Optional[str]]:
        """Validate if a symbol is supported."""
        if not symbol or not isinstance(symbol, str):
            return False, "Symbol must be a non-empty string"

        symbol = symbol.upper().strip()

        if symbol.endswith("-USD"):
            if symbol not in SUPPORTED_CRYPTO_TOKENS:
                logger.info(f"Token {symbol} may be a newer or smaller cap token - attempting to fetch")
            return True, None

        if re.match(r"^[A-Z][A-Z0-9\.]{0,4}$", symbol):
            return True, None

        return (
            False,
            f"Invalid symbol: {symbol}. Use stock tickers or crypto pairs with -USD suffix.",
        )

    async def _download_history_df(
        self,
        symbol: str,
        interval: str,
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Download historical bars using yfinance."""
        if interval not in ALLOWED_INTERVALS:
            logger.error(f"Invalid interval: {interval}")
            return pd.DataFrame()

        def _do_download() -> pd.DataFrame:
            kwargs = dict(
                tickers=symbol,
                interval=interval,
                auto_adjust=True,
                prepost=False,
                progress=False,
                threads=False,
            )
            if start_date or end_date:
                kwargs["start"] = start_date
                kwargs["end"] = end_date
            else:
                kwargs["period"] = period or "6mo"

            df = yf.download(**kwargs)
            if df is None or df.empty:
                return pd.DataFrame()

            if isinstance(df.columns, pd.MultiIndex):
                try:
                    if symbol in df.columns.get_level_values(1):
                        df = df.xs(symbol, level=1, axis=1)
                    else:
                        df = df.droplevel(0, axis=1)
                except Exception:
                    df.columns = [" ".join([str(c) for c in col if c]).strip() for col in df.columns.values]

            wanted = ["Open", "High", "Low", "Close", "Volume"]
            keep = [c for c in wanted if c in df.columns]
            if not keep:
                return pd.DataFrame()
            out = df[keep].dropna(how="all")
            return out

        return await asyncio.to_thread(_do_download)

    @staticmethod
    def _wrap_stockstats(ohlcv_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare OHLCV for stockstats."""
        cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in ohlcv_df.columns]
        df = ohlcv_df[cols].copy()
        df.columns = [c.lower() for c in df.columns]
        return stockstats_wrap(df)

    @staticmethod
    def _safe_float(x) -> Optional[float]:
        try:
            if x is None or (isinstance(x, float) and np.isnan(x)):
                return None
            return float(x)
        except Exception:
            return None

    # ------------------------------------------------------------------------
    #                      API METHODS
    # ------------------------------------------------------------------------

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def fetch_price_history(
        self,
        symbol: str,
        interval: str = "1d",
        period: Optional[str] = "6mo",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch OHLCV bars and return JSON-friendly records."""
        logger.info(
            f"[yahoo_finance] fetch_price_history symbol={symbol} interval={interval} period={period} start={start_date} end={end_date}"
        )

        if interval not in ALLOWED_INTERVALS:
            return {
                "status": "error",
                "error": f"Unsupported interval '{interval}'. Only {sorted(ALLOWED_INTERVALS)} are supported.",
            }

        df = await self._download_history_df(
            symbol=symbol, interval=interval, period=period, start_date=start_date, end_date=end_date
        )

        if df is None or df.empty:
            return {"status": "no_data", "error": f"No historical data returned for {symbol} at {interval} interval."}

        out = df.copy()
        out.index.name = "timestamp"
        out = out.reset_index()

        def _to_iso(x):
            if isinstance(x, (pd.Timestamp, datetime)):
                try:
                    return x.isoformat()
                except Exception:
                    return str(x)
            return str(x)

        out["timestamp"] = out["timestamp"].apply(_to_iso)
        out = out.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
        rows = out[["timestamp", "open", "high", "low", "close", "volume"]].to_dict(orient="records")

        return {
            "status": "success",
            "data": {
                "symbol": symbol,
                "interval": interval,
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "total_rows": len(rows),
                "rows": rows,
            },
        }

    @with_cache(ttl_seconds=120)
    @with_retry(max_retries=3)
    async def indicator_snapshot(
        self,
        symbol: str,
        interval: str = "1d",
        period: str = "6mo",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Compute indicators and return trading signals."""
        logger.info(f"[yahoo_finance] indicator_snapshot symbol={symbol} interval={interval} period={period}")

        is_valid, error_msg = self._validate_symbol(symbol)
        if not is_valid:
            return {"status": "error", "error": error_msg}

        if interval not in ALLOWED_INTERVALS:
            return {
                "status": "error",
                "error": f"Unsupported interval '{interval}'. Only {sorted(ALLOWED_INTERVALS)} are supported.",
            }

        df = await self._download_history_df(
            symbol=symbol, interval=interval, period=period, start_date=start_date, end_date=end_date
        )

        if df is None or df.empty or len(df) < 50:
            return {
                "status": "no_data",
                "error": f"Insufficient historical data for {symbol}. Need at least 50 candles.",
            }

        ss = self._wrap_stockstats(df)

        def _get_series(name: str) -> Optional[pd.Series]:
            try:
                s = ss[name]
                return s.astype(float)
            except Exception as e:
                logger.warning(f"[yahoo_finance] indicator '{name}' unavailable: {e}")
                return None

        close = df["Close"].astype(float)
        rsi = _get_series("rsi")
        macd = _get_series("macd")
        macds = _get_series("macds")
        macdh = _get_series("macdh")
        boll = _get_series("boll")
        boll_ub = _get_series("boll_ub")
        boll_lb = _get_series("boll_lb")
        ema10 = _get_series("close_10_ema")
        sma50 = _get_series("close_50_sma")
        sma200 = _get_series("close_200_sma")

        if len(close) < 2:
            return {"status": "no_data", "error": "Not enough candles for analysis."}

        last = {
            "timestamp": close.index[-1].isoformat()
            if isinstance(close.index[-1], (pd.Timestamp, datetime))
            else str(close.index[-1]),
            "close": float(close.iloc[-1]),
            "rsi": float(rsi.iloc[-1]) if rsi is not None and not np.isnan(rsi.iloc[-1]) else None,
            "macd": float(macd.iloc[-1]) if macd is not None and not np.isnan(macd.iloc[-1]) else None,
            "macds": float(macds.iloc[-1]) if macds is not None and not np.isnan(macds.iloc[-1]) else None,
            "macdh": float(macdh.iloc[-1]) if macdh is not None and not np.isnan(macdh.iloc[-1]) else None,
            "boll": float(boll.iloc[-1]) if boll is not None and not np.isnan(boll.iloc[-1]) else None,
            "boll_ub": float(boll_ub.iloc[-1]) if boll_ub is not None and not np.isnan(boll_ub.iloc[-1]) else None,
            "boll_lb": float(boll_lb.iloc[-1]) if boll_lb is not None and not np.isnan(boll_lb.iloc[-1]) else None,
            "ema_10": float(ema10.iloc[-1]) if ema10 is not None and not np.isnan(ema10.iloc[-1]) else None,
            "sma_50": float(sma50.iloc[-1]) if sma50 is not None and not np.isnan(sma50.iloc[-1]) else None,
            "sma_200": float(sma200.iloc[-1]) if sma200 is not None and not np.isnan(sma200.iloc[-1]) else None,
        }

        prev = {
            "macd": float(macd.iloc[-2]) if macd is not None and not np.isnan(macd.iloc[-2]) else None,
            "macds": float(macds.iloc[-2]) if macds is not None and not np.isnan(macds.iloc[-2]) else None,
            "sma_50": float(sma50.iloc[-2]) if sma50 is not None and not np.isnan(sma50.iloc[-2]) else None,
            "sma_200": float(sma200.iloc[-2]) if sma200 is not None and not np.isnan(sma200.iloc[-2]) else None,
        }

        def cross_up(a, b, a_prev, b_prev) -> bool:
            if None in (a, b, a_prev, b_prev):
                return False
            return a > b and a_prev <= b_prev

        def cross_down(a, b, a_prev, b_prev) -> bool:
            if None in (a, b, a_prev, b_prev):
                return False
            return a < b and a_prev >= b_prev

        macd_bullish_cross = cross_up(last["macd"], last["macds"], prev["macd"], prev["macds"])
        macd_bearish_cross = cross_down(last["macd"], last["macds"], prev["macd"], prev["macds"])
        golden_cross = cross_up(last["sma_50"], last["sma_200"], prev["sma_50"], prev["sma_200"])
        death_cross = cross_down(last["sma_50"], last["sma_200"], prev["sma_50"], prev["sma_200"])

        regime = None
        if last["close"] is not None and last["sma_200"] is not None:
            regime = "bullish" if last["close"] >= last["sma_200"] else "bearish"

        rsi_state = None
        if last["rsi"] is not None:
            if last["rsi"] >= 70:
                rsi_state = "overbought"
            elif last["rsi"] <= 30:
                rsi_state = "oversold"
            elif last["rsi"] >= 50:
                rsi_state = "bullish_momentum"
            else:
                rsi_state = "bearish_momentum"

        boll_state = None
        if last["boll_ub"] is not None and last["boll_lb"] is not None:
            if last["close"] > last["boll_ub"]:
                boll_state = "above_upper_band"
            elif last["close"] < last["boll_lb"]:
                boll_state = "below_lower_band"
            else:
                boll_state = "within_bands"

        action = "neutral"
        confidence = 0.4
        rationale: List[str] = []

        if regime == "bullish":
            if macd_bullish_cross or (
                last["ema_10"] and last["close"] > last["ema_10"] and last["rsi"] and last["rsi"] > 50
            ):
                action = "buy"
                confidence = 0.65
                rationale.append("Bullish trend confirmed with momentum signals.")

            if golden_cross:
                confidence += 0.15
                rationale.append("Golden cross detected (50-SMA crossing above 200-SMA).")

            if boll_state == "above_upper_band":
                confidence += 0.05
                rationale.append("Price breaking above upper Bollinger Band suggests strong momentum.")

        elif regime == "bearish":
            if macd_bearish_cross or (
                last["ema_10"] and last["close"] < last["ema_10"] and last["rsi"] and last["rsi"] < 50
            ):
                action = "sell"
                confidence = 0.65
                rationale.append("Bearish trend confirmed with negative momentum signals.")

            if death_cross:
                confidence += 0.15
                rationale.append("Death cross detected (50-SMA crossing below 200-SMA).")

            if boll_state == "below_lower_band":
                confidence += 0.05
                rationale.append("Price breaking below lower Bollinger Band suggests strong selling pressure.")

        if rsi_state == "overbought" and action == "buy":
            confidence -= 0.1
            rationale.append("RSI overbought condition suggests caution.")
        elif rsi_state == "oversold" and action == "sell":
            confidence -= 0.1
            rationale.append("RSI oversold condition suggests potential bounce.")

        confidence = float(max(0.0, min(0.9, confidence)))

        snapshot = {
            "symbol": symbol,
            "interval": interval,
            "period": period if (start_date is None and end_date is None) else None,
            "start_date": start_date,
            "end_date": end_date,
            "timestamp": last["timestamp"],
            "close": last["close"],
            "rsi": last["rsi"],
            "macd": last["macd"],
            "macds": last["macds"],
            "macdh": last["macdh"],
            "boll_middle": last["boll"],
            "boll_upper": last["boll_ub"],
            "boll_lower": last["boll_lb"],
            "ema_10": last["ema_10"],
            "sma_50": last["sma_50"],
            "sma_200": last["sma_200"],
            "market_regime": regime,
            "rsi_state": rsi_state,
            "bollinger_position": boll_state,
            "macd_bullish_cross": macd_bullish_cross,
            "macd_bearish_cross": macd_bearish_cross,
            "golden_cross": golden_cross,
            "death_cross": death_cross,
        }

        return {
            "status": "success",
            "data": {
                "indicators": snapshot,
                "signal": {
                    "action": action,
                    "confidence": confidence,
                    "rationale": " ".join(rationale) if rationale else "Mixed or neutral signals detected.",
                },
            },
        }

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute tools and return data."""
        logger.info(f"[yahoo_finance] Handling tool call: {tool_name} args={function_args}")

        try:
            if tool_name == "fetch_price_history":
                symbol = function_args.get("symbol")
                if not symbol:
                    return {"error": "Missing 'symbol' parameter"}

                interval = function_args.get("interval", "1d")
                period = function_args.get("period", "6mo")
                start_date = function_args.get("start_date")
                end_date = function_args.get("end_date")

                result = await self.fetch_price_history(
                    symbol=symbol, interval=interval, period=period, start_date=start_date, end_date=end_date
                )

            elif tool_name == "indicator_snapshot":
                symbol = function_args.get("symbol")
                if not symbol:
                    return {"error": "Missing 'symbol' parameter"}

                interval = function_args.get("interval", "1d")
                period = function_args.get("period", "6mo")
                start_date = function_args.get("start_date")
                end_date = function_args.get("end_date")

                result = await self.indicator_snapshot(
                    symbol=symbol, interval=interval, period=period, start_date=start_date, end_date=end_date
                )

            else:
                return {"error": f"Unsupported tool: {tool_name}"}

            if errors := self._handle_error(result):
                return errors
            return result

        except Exception as e:
            logger.exception(f"[yahoo_finance] Tool execution failed: {e}")
            return {"status": "error", "error": f"Unhandled exception: {e}"}
