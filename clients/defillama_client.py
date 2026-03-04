import asyncio
import logging
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from .base_client import BaseAPIClient

logger = logging.getLogger(__name__)

YIELDS_MIN_TVL_USD = 500_000
YIELDS_DEFAULT_LIMIT = 10
YIELDS_MAX_LIMIT = 50
YIELDS_CHART_CONCURRENCY = 4


def _format_usd(value: float) -> str:
    """Format USD value with appropriate suffix (K, M, B, T)."""
    if value is None or value == 0:
        return "0 USD"

    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T USD"
    elif abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B USD"
    elif abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M USD"
    elif abs_value >= 1_000:
        return f"{value / 1_000:.2f}K USD"
    else:
        return f"{value:,.0f} USD"


def _calculate_period_average(data_points: list, days: int) -> float:
    """Calculate average from the last N days of data points.

    Args:
        data_points: List of [timestamp, value] or {date, totalLiquidityUSD}
        days: Number of days to average

    Returns:
        Average value for the period, or 0 if insufficient data
    """
    if not data_points or len(data_points) < days:
        return 0

    recent = data_points[-days:]

    values = []
    for point in recent:
        if isinstance(point, list):
            values.append(point[1])
        elif isinstance(point, dict):
            values.append(point.get("totalLiquidityUSD", 0))

    return sum(values) / len(values) if values else 0


def _calculate_trend_percentage(current_avg: float, previous_avg: float) -> float:
    """Calculate percentage change between two averages."""
    if previous_avg == 0:
        return 0 if current_avg == 0 else 100.0
    return ((current_avg - previous_avg) / previous_avg) * 100


def _format_trend_description(wow_pct: float, mom_pct: float) -> str:
    """Generate natural language trend description."""

    def format_change(pct: float) -> str:
        if abs(pct) < 1:
            return f"stable ({pct:+.1f}%)"
        elif pct > 0:
            return f"up {abs(pct):.1f}%"
        else:
            return f"down {abs(pct):.1f}%"

    wow_desc = format_change(wow_pct)
    mom_desc = format_change(mom_pct)

    return f"{wow_desc.capitalize()} WoW, {mom_desc} MoM"


class DefiLlamaClient(BaseAPIClient):
    """DefiLlama API implementation"""

    def __init__(self):
        super().__init__("https://api.llama.fi")
        self.yields_client = BaseAPIClient("https://yields.llama.fi")

    # sync methods
    def get_protocol_tvl(self, protocol: str) -> Dict:
        return self._sync_request("get", f"/protocol/{protocol}")

    def get_protocols(self) -> List[Dict]:
        return self._sync_request("get", "/protocols")

    def get_chain_tvl(self, chain: str) -> Dict:
        return self._sync_request("get", f"/v2/historicalChainTvl/{chain}")

    def get_current_tvl_all_chains(self) -> float:
        return self._sync_request("get", "/v2/chains")

    # async methods
    async def get_protocol_tvl_async(self, protocol: str) -> Dict:
        """
        Get TVL data for a specific protocol

        Args:
            protocol: Protocol identifier (e.g. 'aave', 'uniswap') in lowercase

        Returns:
            Dictionary containing detailed TVL data for the protocol, including:
            - tvl: Current total locked value
            - chainTvls: TVL distribution across chains
            - tokens: Details of locked tokens
            - name: Protocol name
            - symbol: Protocol token symbol (if any)
            - gecko_id: CoinGecko API ID (if any)
        """
        return await self._async_request("get", f"/protocol/{protocol}")

    async def get_protocols_async(self) -> List[Dict]:
        """
        Get list of all protocols and their TVL data

        Returns:
            List of protocols, each containing:
            - name: Protocol name
            - symbol: Protocol token symbol
            - chain: Main chain
            - tvl: Current TVL
            - change_1h: 1 hour TVL change percentage
            - change_1d: 24 hour TVL change percentage
            - change_7d: 7 day TVL change percentage
        """
        return await self._async_request("get", "/protocols")

    async def get_chain_tvl_async(self, chain: str) -> Dict:
        """
        Get historical TVL data for a specific blockchain

        Args:
            chain: Blockchain identifier (e.g. 'ethereum', 'bsc') in lowercase

        Returns:
            Historical TVL data for the chain, containing timestamps and corresponding TVL values:
            [
                {
                    "date": unix timestamp,
                    "tvl": float
                },
                ...
            ]
        """
        return await self._async_request("get", f"/v2/historicalChainTvl/{chain}")

    async def get_current_tvl_all_chains_async(self) -> List[Dict]:
        """
        Get current TVL data for all chains

        Returns:
            List containing current TVL data for all chains:
            [
                {
                    "gecko_id": str,
                    "tvl": float,
                    "tokenSymbol": str,
                    "cmcId": str,
                    "name": str,
                    "chainId": str
                },
                ...
            ]
        """
        return await self._async_request("get", "/v2/chains")

    async def get_chains_async(self) -> List[Dict]:
        """Fetch all chains from DeFiLlama /v2/chains endpoint."""
        return await self._async_request("get", "/v2/chains")

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2, delay=0.5)
    async def get_yield_pools_async(self) -> List[Dict[str, Any]]:
        payload = await self.yields_client._async_request("get", "/pools")
        return payload["data"]

    @with_cache(ttl_seconds=300)
    async def get_yield_chart_async(self, pool_id: str) -> List[Dict[str, Any]]:
        payload = await self.yields_client._async_request("get", f"/chart/{pool_id}")
        return payload["data"]

    def _avg_last(self, values: List[float], window: int) -> Optional[float]:
        if len(values) < window:
            return None
        return sum(values[-window:]) / window

    def _avg_prev(self, values: List[float], window: int) -> Optional[float]:
        if len(values) < window * 2:
            return None
        return sum(values[-window * 2 : -window]) / window

    def _pct(self, current: Optional[float], previous: Optional[float]) -> Optional[float]:
        if current is None or previous is None or previous == 0:
            return None
        return ((current - previous) / abs(previous)) * 100

    def _round(self, value: Optional[float], digits: int = 4) -> Optional[float]:
        if value is None:
            return None
        return round(value, digits)

    def _drop_null_fields(self, value: Any) -> tuple[Any, int]:
        if value is None:
            return None, 1
        if type(value) is dict:
            cleaned = {}
            removed = 0
            for key, item in value.items():
                if item is None:
                    removed += 1
                    continue
                nested, nested_removed = self._drop_null_fields(item)
                removed += nested_removed
                if nested is None:
                    removed += 1
                    continue
                cleaned[key] = nested
            return cleaned, removed
        if type(value) is list:
            cleaned = []
            removed = 0
            for item in value:
                if item is None:
                    removed += 1
                    continue
                nested, nested_removed = self._drop_null_fields(item)
                removed += nested_removed
                if nested is None:
                    removed += 1
                    continue
                cleaned.append(nested)
            return cleaned, removed
        return value, 0

    def _build_history_metrics(self, history: List[Dict[str, Any]], fallback_apy: Optional[float]) -> Dict[str, Any]:
        if not history:
            return {
                "apy_latest": self._round(fallback_apy),
                "apy_avg_7d": None,
                "apy_avg_30d": None,
                "apy_change_7d_pct": None,
                "apy_change_30d_pct": None,
                "tvl_trend_7d_pct": None,
                "tvl_trend_30d_pct": None,
            }

        latest_point = history[-1]
        apy_latest = latest_point.get("apy")
        if apy_latest is None:
            apy_latest = fallback_apy

        apy_series = [point["apy"] for point in history if point.get("apy") is not None]
        tvl_series = [point["tvlUsd"] for point in history if point.get("tvlUsd") is not None]

        apy_avg_7d = self._avg_last(apy_series, 7)
        apy_avg_30d = self._avg_last(apy_series, 30)

        tvl_avg_7d = self._avg_last(tvl_series, 7)
        tvl_prev_7d = self._avg_prev(tvl_series, 7)
        tvl_avg_30d = self._avg_last(tvl_series, 30)
        tvl_prev_30d = self._avg_prev(tvl_series, 30)

        return {
            "apy_latest": self._round(apy_latest),
            "apy_avg_7d": self._round(apy_avg_7d),
            "apy_avg_30d": self._round(apy_avg_30d),
            "apy_change_7d_pct": self._round(self._pct(apy_latest, apy_avg_7d), 2),
            "apy_change_30d_pct": self._round(self._pct(apy_latest, apy_avg_30d), 2),
            "tvl_trend_7d_pct": self._round(self._pct(tvl_avg_7d, tvl_prev_7d), 2),
            "tvl_trend_30d_pct": self._round(self._pct(tvl_avg_30d, tvl_prev_30d), 2),
        }

    def _build_base_yield_row(self, pool_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "project": pool_data["project"],
            "chain": pool_data["chain"],
            "symbol": pool_data["symbol"],
            "stablecoin": pool_data["stablecoin"],
            "tvl_usd": int(pool_data["tvlUsd"]),
            "apy": self._round(pool_data.get("apy")),
            "apy_base": self._round(pool_data.get("apyBase")),
            "apy_reward": self._round(pool_data.get("apyReward")),
        }

    async def _attach_history_metrics(
        self, pool_data: Dict[str, Any], row: Dict[str, Any], semaphore: asyncio.Semaphore
    ) -> Dict[str, Any]:
        history = []
        try:
            async with semaphore:
                history = await self.get_yield_chart_async(pool_data["pool"])
        except Exception as error:
            logger.warning(f"Yield chart fetch failed for {pool_data['pool']}: {error}")

        result = dict(row)
        result["history"] = self._build_history_metrics(history, row["apy"])
        return result

    async def search_yield_pools_async(
        self,
        projects: Optional[List[str]] = None,
        chains: Optional[List[str]] = None,
        symbols: Optional[List[str]] = None,
        stablecoin: Optional[bool] = None,
        sort_by: str = "apy",
        limit: int = YIELDS_DEFAULT_LIMIT,
    ) -> Dict[str, Any]:
        if sort_by not in {"apy", "tvl"}:
            raise ValueError("sort_by must be either 'apy' or 'tvl'")

        if limit < 1:
            limit = 1
        elif limit > YIELDS_MAX_LIMIT:
            limit = YIELDS_MAX_LIMIT

        project_set = {project.lower().strip() for project in projects} if projects else set()
        chain_set = {chain.lower().strip() for chain in chains} if chains else set()
        symbol_set = {symbol.upper().strip() for symbol in symbols} if symbols else set()

        pools = await self.get_yield_pools_async()
        filtered = []
        skipped_tvl_lt_min = 0
        for pool in pools:
            if pool["tvlUsd"] < YIELDS_MIN_TVL_USD:
                skipped_tvl_lt_min += 1
                continue
            if project_set and pool["project"].lower() not in project_set:
                continue
            if chain_set and pool["chain"].lower() not in chain_set:
                continue
            if symbol_set and pool["symbol"].upper() not in symbol_set:
                continue
            if stablecoin is not None and pool["stablecoin"] != stablecoin:
                continue
            filtered.append(pool)

        sort_key = "apy" if sort_by == "apy" else "tvlUsd"
        ranked = sorted(filtered, key=lambda pool: pool[sort_key] if pool[sort_key] is not None else -1, reverse=True)
        selected_pools = ranked[:limit]
        selected_rows = [self._build_base_yield_row(pool) for pool in selected_pools]

        semaphore = asyncio.Semaphore(YIELDS_CHART_CONCURRENCY)
        enriched_rows = await asyncio.gather(
            *[
                self._attach_history_metrics(pool_data=pool, row=row, semaphore=semaphore)
                for pool, row in zip(selected_pools, selected_rows)
            ]
        )

        rows = []
        null_fields_removed = 0
        for row in enriched_rows:
            cleaned_row, removed = self._drop_null_fields(row)
            null_fields_removed += removed
            rows.append(cleaned_row)

        applied_filters = {"min_tvl_usd": YIELDS_MIN_TVL_USD}
        if projects:
            applied_filters["projects"] = projects
        if chains:
            applied_filters["chains"] = chains
        if symbols:
            applied_filters["symbols"] = symbols
        if stablecoin is not None:
            applied_filters["stablecoin"] = stablecoin

        return {
            "sort_by": sort_by,
            "limit": limit,
            "matched": len(filtered),
            "returned": len(rows),
            "filters": applied_filters,
            "skipped": {
                "tvl_lt_min": skipped_tvl_lt_min,
                "null_fields_removed": null_fields_removed,
            },
            "note": f"Pools with tvlUsd < {YIELDS_MIN_TVL_USD} are skipped.",
            "results": rows,
        }

    def _calculate_tvl_trends(self, tvl_data: list) -> dict:
        """Calculate WoW and MoM trends from TVL time series."""
        if not tvl_data or len(tvl_data) < 7:
            current = tvl_data[-1].get("totalLiquidityUSD", 0) if tvl_data else 0
            return {"current": _format_usd(current), "trend": "Insufficient data for trend analysis"}

        current = tvl_data[-1].get("totalLiquidityUSD", 0)

        last_7d_avg = _calculate_period_average(tvl_data, 7)
        prev_7d_avg = _calculate_period_average(tvl_data[:-7], 7) if len(tvl_data) >= 14 else last_7d_avg
        wow_pct = _calculate_trend_percentage(last_7d_avg, prev_7d_avg)

        last_30d_avg = _calculate_period_average(tvl_data, 30) if len(tvl_data) >= 30 else last_7d_avg
        prev_30d_avg = _calculate_period_average(tvl_data[:-30], 30) if len(tvl_data) >= 60 else last_30d_avg
        mom_pct = _calculate_trend_percentage(last_30d_avg, prev_30d_avg)

        return {"current": _format_usd(current), "trend": _format_trend_description(wow_pct, mom_pct)}

    def _calculate_fees_trends(self, fee_chart_data: list) -> str:
        """Calculate WoW and MoM trends from fee time series (totalDataChart)."""
        if not fee_chart_data or len(fee_chart_data) < 7:
            return "Insufficient data for trend analysis"

        last_7d_avg = _calculate_period_average(fee_chart_data, 7)
        prev_7d_avg = _calculate_period_average(fee_chart_data[:-7], 7) if len(fee_chart_data) >= 14 else last_7d_avg
        wow_pct = _calculate_trend_percentage(last_7d_avg, prev_7d_avg)

        last_30d_avg = _calculate_period_average(fee_chart_data, 30) if len(fee_chart_data) >= 30 else last_7d_avg
        prev_30d_avg = _calculate_period_average(fee_chart_data[:-30], 30) if len(fee_chart_data) >= 60 else last_30d_avg
        mom_pct = _calculate_trend_percentage(last_30d_avg, prev_30d_avg)

        return _format_trend_description(wow_pct, mom_pct)

    def _build_tvl_data(self, protocol_data: dict) -> dict:
        """Build TVL data with trend from protocol response."""
        tvl_history = protocol_data.get("tvl", [])

        if isinstance(tvl_history, list) and tvl_history:
            return self._calculate_tvl_trends(tvl_history)

        current_tvls = protocol_data.get("currentChainTvls", {})
        total = sum(v for k, v in current_tvls.items() if isinstance(v, (int, float)) and "-borrowed" not in k and k != "borrowed")
        return {"current": _format_usd(total), "trend": "Historical data not available"}

    def _build_top_chains(self, protocol_data: dict) -> list:
        """Build top 3 chains by TVL with trend analysis."""
        current_tvls = protocol_data.get("currentChainTvls", {})
        chain_tvls_history = protocol_data.get("chainTvls", {})

        chain_values = []
        for chain, value in current_tvls.items():
            if "-borrowed" in chain or chain == "borrowed":
                continue
            if isinstance(value, (int, float)):
                chain_values.append((chain, value))

        chain_values.sort(key=lambda x: x[1], reverse=True)
        top_3 = chain_values[:3]

        result = []
        for chain, tvl in top_3:
            chain_entry = {"chain": chain, "tvl": _format_usd(tvl), "trend": "Historical data not available"}

            chain_history = chain_tvls_history.get(chain, {})
            if isinstance(chain_history, dict):
                tvl_list = chain_history.get("tvl", [])
                if tvl_list:
                    trends = self._calculate_tvl_trends(tvl_list)
                    chain_entry["trend"] = trends["trend"]

            result.append(chain_entry)

        return result

    def _build_volume_data(self, dexs_data: dict) -> dict:
        """Build DEX volume data with trends."""
        return {
            "past24h": _format_usd(dexs_data.get("total24h", 0)),
            "past7d": _format_usd(dexs_data.get("total7d", 0)),
            "past30d": _format_usd(dexs_data.get("total30d", 0)),
            "trend": self._calculate_fees_trends(dexs_data.get("totalDataChart", [])),
        }

    def _build_breakdown_top_chains(self, data: dict, value_field: str) -> list:
        """Build top 3 chains from totalDataChartBreakdown.

        Args:
            data: API response containing totalDataChartBreakdown
            value_field: Field name for the value (e.g., "24h_volume", "24h_fees")
        """
        breakdown = data.get("totalDataChartBreakdown", [])
        if not breakdown:
            return []

        # Each entry is [timestamp, {chain: {protocol: value}}]
        chain_totals = {}
        chain_history = {}

        for entry in breakdown:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            timestamp, chain_data = entry[0], entry[1]
            if not isinstance(chain_data, dict):
                continue

            for chain, protocol_values in chain_data.items():
                if not isinstance(protocol_values, dict):
                    continue
                value = sum(v for v in protocol_values.values() if isinstance(v, (int, float)))
                if chain not in chain_history:
                    chain_history[chain] = []
                chain_history[chain].append([timestamp, value])

        for chain, history in chain_history.items():
            if history:
                chain_totals[chain] = history[-1][1]

        sorted_chains = sorted(chain_totals.items(), key=lambda x: x[1], reverse=True)[:3]

        result = []
        for chain, value in sorted_chains:
            history = chain_history.get(chain, [])
            trend = self._calculate_fees_trends(history) if len(history) >= 7 else "Insufficient data"
            result.append({"chain": chain, value_field: _format_usd(value), "trend": trend})

        return result

    def get_protocol_enriched(self, protocol: str) -> Dict:
        """
        Get enriched protocol data combining TVL and fee information (sync version).

        Args:
            protocol: Protocol identifier (e.g. 'aave-v3', 'uniswap-v3')

        Returns:
            Dictionary containing:
            - description, chain, gecko_id, category, chains
            - revenue_methodology: Fee/revenue breakdown explanation
            - fees: Past 24h, 7d, 30d with trend analysis
            - tvl: Current value with trend analysis
            - top_chains: Top 3 chains by TVL with trends
            - volume (DEX only): Past 24h, 7d, 30d volume with trend
            - volume_top_chains (DEX only): Top 3 chains by volume with trends
        """
        protocol_data = self._sync_request("get", f"/protocol/{protocol}")
        category = protocol_data.get("category", "")

        fees_data = None
        try:
            fees_data = self._sync_request("get", f"/summary/fees/{protocol}")
        except Exception:
            pass

        dexs_data = None
        if category == "Dexes" or category == "Dexs":
            try:
                dexs_data = self._sync_request("get", f"/summary/dexs/{protocol}")
            except Exception:
                pass

        result = {
            "description": protocol_data.get("description", ""),
            "chain": protocol_data.get("chain", ""),
            "gecko_id": protocol_data.get("gecko_id"),
            "category": category,
            "chains": protocol_data.get("chains", []),
            "revenue_methodology": {},
            "fees": {"past24h": "N/A", "past7d": "N/A", "past30d": "N/A", "trend": "No fee data available"},
            "tvl": self._build_tvl_data(protocol_data),
            "top_chains": self._build_top_chains(protocol_data),
        }

        tvl_methodology = protocol_data.get("methodology")
        if tvl_methodology and isinstance(tvl_methodology, str):
            result["tvl_methodology"] = tvl_methodology

        if fees_data:
            result["revenue_methodology"] = fees_data.get("methodology", {})
            result["fees"] = {
                "past24h": _format_usd(fees_data.get("total24h", 0)),
                "past7d": _format_usd(fees_data.get("total7d", 0)),
                "past30d": _format_usd(fees_data.get("total30d", 0)),
                "trend": self._calculate_fees_trends(fees_data.get("totalDataChart", [])),
            }
            fees_top_chains = self._build_breakdown_top_chains(fees_data, "24h_fees")
            if fees_top_chains:
                result["fees_top_chains"] = fees_top_chains

        if dexs_data:
            result["volume"] = self._build_volume_data(dexs_data)
            result["volume_top_chains"] = self._build_breakdown_top_chains(dexs_data, "24h_volume")

        return result

    async def get_protocol_enriched_async(self, protocol: str) -> Dict:
        """
        Get enriched protocol data combining TVL and fee information (async version).

        Args:
            protocol: Protocol identifier (e.g. 'aave-v3', 'uniswap-v3')

        Returns:
            Dictionary containing:
            - description, chain, gecko_id, category, chains
            - revenue_methodology: Fee/revenue breakdown explanation
            - fees: Past 24h, 7d, 30d with trend analysis
            - tvl: Current value with trend analysis
            - top_chains: Top 3 chains by TVL with trends
            - volume (DEX only): Past 24h, 7d, 30d volume with trend
            - volume_top_chains (DEX only): Top 3 chains by volume with trends
        """
        protocol_data = await self._async_request("get", f"/protocol/{protocol}")
        category = protocol_data.get("category", "")

        tasks = [self._async_request("get", f"/summary/fees/{protocol}")]
        if category == "Dexes" or category == "Dexs":
            tasks.append(self._async_request("get", f"/summary/dexs/{protocol}"))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        fees_data = results[0]
        dexs_data = results[1] if len(results) > 1 else None

        result = {
            "description": protocol_data.get("description", ""),
            "chain": protocol_data.get("chain", ""),
            "gecko_id": protocol_data.get("gecko_id"),
            "category": category,
            "chains": protocol_data.get("chains", []),
            "revenue_methodology": {},
            "fees": {"past24h": "N/A", "past7d": "N/A", "past30d": "N/A", "trend": "No fee data available"},
            "tvl": self._build_tvl_data(protocol_data),
            "top_chains": self._build_top_chains(protocol_data),
        }

        tvl_methodology = protocol_data.get("methodology")
        if tvl_methodology and isinstance(tvl_methodology, str):
            result["tvl_methodology"] = tvl_methodology

        if not isinstance(fees_data, Exception) and fees_data:
            result["revenue_methodology"] = fees_data.get("methodology", {})
            result["fees"] = {
                "past24h": _format_usd(fees_data.get("total24h", 0)),
                "past7d": _format_usd(fees_data.get("total7d", 0)),
                "past30d": _format_usd(fees_data.get("total30d", 0)),
                "trend": self._calculate_fees_trends(fees_data.get("totalDataChart", [])),
            }
            fees_top_chains = self._build_breakdown_top_chains(fees_data, "24h_fees")
            if fees_top_chains:
                result["fees_top_chains"] = fees_top_chains

        if dexs_data and not isinstance(dexs_data, Exception):
            result["volume"] = self._build_volume_data(dexs_data)
            result["volume_top_chains"] = self._build_breakdown_top_chains(dexs_data, "24h_volume")

        return result

    def get_chain_enriched(self, chain: str) -> Dict:
        """
        Get enriched chain data combining TVL and fee information (sync version).

        Args:
            chain: Chain name (e.g. 'Ethereum', 'Solana', 'Base')

        Returns:
            Dictionary containing chain TVL and fee metrics with trends
        """
        tvl_data = self._sync_request("get", f"/v2/historicalChainTvl/{chain}")
        fees_data = self._sync_request("get", f"/overview/fees/{chain}")
        return self._build_chain_enriched_result(chain, tvl_data, fees_data)

    async def get_chain_enriched_async(self, chain: str) -> Dict:
        """
        Get enriched chain data combining TVL and fee information (async version).

        Args:
            chain: Chain name (e.g. 'Ethereum', 'Solana', 'Base')

        Returns:
            Dictionary containing chain TVL and fee metrics with trends
        """
        tvl_result, fees_result = await asyncio.gather(
            self._async_request("get", f"/v2/historicalChainTvl/{chain}"),
            self._async_request("get", f"/overview/fees/{chain}"),
            return_exceptions=True,
        )
        tvl_data = tvl_result if not isinstance(tvl_result, Exception) else []
        fees_data = fees_result if not isinstance(fees_result, Exception) else {}
        if not tvl_data and not fees_data:
            raise ValueError(f"No data available for chain '{chain}'")
        return self._build_chain_enriched_result(chain, tvl_data, fees_data)

    def _build_chain_enriched_result(self, chain: str, tvl_data: list, fees_data: dict) -> Dict:
        """Build enriched chain result from TVL and fees data."""
        # Calculate TVL trends from historical data
        tvl_result = {"current": "0 USD", "trend": "No data available"}
        if tvl_data:
            current_tvl = tvl_data[-1].get("tvl", 0)
            week_ago_tvl = tvl_data[-7].get("tvl", current_tvl) if len(tvl_data) >= 7 else current_tvl
            month_ago_tvl = tvl_data[-30].get("tvl", current_tvl) if len(tvl_data) >= 30 else current_tvl

            wow_pct = _calculate_trend_percentage(current_tvl, week_ago_tvl)
            mom_pct = _calculate_trend_percentage(current_tvl, month_ago_tvl)

            tvl_result = {
                "current": _format_usd(current_tvl),
                "trend": _format_trend_description(wow_pct, mom_pct),
            }

        # Build fees result - use pre-calculated changes from API
        fees_result = {"past24h": "N/A", "past7d": "N/A", "past30d": "N/A", "trend": "No fee data available"}
        if fees_data:
            # API provides change_7dover7d (WoW) and change_30dover30d (MoM)
            wow_pct = fees_data.get("change_7dover7d", 0)
            mom_pct = fees_data.get("change_30dover30d", 0)

            fees_result = {
                "past24h": _format_usd(fees_data.get("total24h", 0)),
                "past7d": _format_usd(fees_data.get("total7d", 0)),
                "past30d": _format_usd(fees_data.get("total30d", 0)),
                "all_time": _format_usd(fees_data.get("totalAllTime", 0)),
                "trend": _format_trend_description(wow_pct, mom_pct),
            }

        # Get top protocols on this chain
        top_protocols = []
        protocols = fees_data.get("protocols", []) if fees_data else []
        sorted_protocols = sorted(protocols, key=lambda x: x.get("total24h") or 0, reverse=True)[:5]
        for p in sorted_protocols:
            top_protocols.append({
                "name": p.get("displayName", p.get("name", "")),
                "category": p.get("category", ""),
                "24h_fees": _format_usd(p.get("total24h", 0)),
            })

        return {
            "chain": chain,
            "tvl": tvl_result,
            "fees": fees_result,
            "top_protocols_by_fees": top_protocols,
            "protocol_count": len(protocols),
        }

    async def close(self):
        await super().close()
        await self.yields_client.close()
