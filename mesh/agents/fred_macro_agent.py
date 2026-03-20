import json
import logging
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)

FRED_BASE_URL = "https://api.stlouisfed.org/fred"
SUPPORTED_VIEWS = [
    "level",
    "change",
    "sign",
    "yoy",
    "mom_annualized",
    "mom_change",
    "yoy_change",
    "wow_change",
    "qoq_annualized",
]
PERIOD_TO_DAYS = {
    "1m": 31,
    "3m": 92,
    "6m": 183,
    "1y": 366,
    "2y": 731,
    "5y": 1827,
    "10y": 3653,
}


def _parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _iso_date(value: date) -> str:
    return value.isoformat()


def _safe_float(value: Optional[str]) -> Optional[float]:
    if value in (None, "", "."):
        return None
    return float(value)


def _round_value(value: Optional[float], digits: int = 4) -> Optional[float]:
    if value is None:
        return None
    return round(value, digits)


def _direction(current: Optional[float], previous: Optional[float], tolerance: float = 0.0001) -> Optional[str]:
    if current is None or previous is None:
        return None
    if current > previous + tolerance:
        return "rising"
    if current < previous - tolerance:
        return "falling"
    return "flat"


def _sign_label(value: float) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "flat"


class FredMacroAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.fred_api_key = os.getenv("FRED_API_KEY")
        self.registry_path = Path(__file__).resolve().parent.parent / "data" / "fred_macro_series.json"
        self.registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self.pillars = list(self.registry["pillars"].keys())
        self.series_by_key: Dict[str, Dict[str, Any]] = {}
        self.release_by_key = self.registry["release_keys"]
        self.release_key_by_id: Dict[int, str] = {}

        for pillar, items in self.registry["pillars"].items():
            for item in items:
                series = dict(item)
                series["pillar"] = pillar
                self.series_by_key[series["key"]] = series
        for release_key, item in self.release_by_key.items():
            self.release_key_by_id[item["release_id"]] = release_key

        self.metadata.update(
            {
                "name": "FRED Macro Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Registry-driven FRED and ALFRED macro agent for curated U.S. inflation, rates, labor, credit, growth, release, and vintage context.",
                "external_apis": ["FRED", "ALFRED"],
                "tags": ["Finance", "Macroeconomics"],
                "verified": True,
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Heurist.png",
                "examples": [
                    "Give me the latest headline CPI snapshot",
                    "Show core PCE YoY history for 2 years",
                    "Summarize the current macro regime",
                    "Show the upcoming CPI and payroll release calendar",
                    "Give me CPI release context",
                    "Show real GDP as known on 2020-07-01",
                ],
                "credits": {"default": 0.3},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.003",
                },
            }
        )

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 25

    def get_tool_timeout_seconds(self) -> Dict[str, int]:
        return {
            "macro_release_context": 30,
            "macro_regime_context": 35,
        }

    def get_system_prompt(self) -> str:
        return """You are a macroeconomic data assistant backed by a curated FRED and ALFRED registry.

Use tools by job:
- `macro_series_snapshot` for the latest compact read on one supported macro series
- `macro_series_history` for bounded historical series data with an explicit transformation
- `macro_vintage_history` for point-in-time-safe history using ALFRED realtime dates
- `macro_release_calendar` for curated CPI, PCE, payroll, GDP, and weekly claims release dates
- `macro_release_context` for one supported release and its linked series
- `macro_regime_context` for multi-pillar regime summaries

Rules:
- Only use supported `series_key` and `release_key` values from the tool schema
- Do not invent raw FRED series IDs when the registry key is available
- Be explicit when data is vintage-safe versus revised-history context
- Prefer the smallest tool that answers the request
"""

    def get_tool_schemas(self) -> List[Dict]:
        series_keys = list(self.series_by_key.keys())
        release_keys = list(self.release_by_key.keys())
        return [
            {
                "type": "function",
                "function": {
                    "name": "macro_series_snapshot",
                    "description": "Return a compact latest read for one curated macro series. Use this for the newest supported macro reading, previous reading, and derived change metrics.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "series_key": {
                                "type": "string",
                                "enum": series_keys,
                                "description": "Registry-backed macro series key such as headline_cpi, core_pce, fed_funds, unemployment_rate, or real_gdp.",
                            }
                        },
                        "required": ["series_key"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "macro_series_history",
                    "description": "Return bounded history for one curated macro series. Use this for overlays, trend summaries, or transformed views like YoY or qoq annualized.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "series_key": {
                                "type": "string",
                                "enum": series_keys,
                                "description": "Registry-backed macro series key.",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Inclusive start date in YYYY-MM-DD format. If omitted, `period` is used.",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "Inclusive end date in YYYY-MM-DD format. Defaults to today.",
                            },
                            "period": {
                                "type": "string",
                                "enum": list(PERIOD_TO_DAYS.keys()),
                                "description": "Rolling lookback window used when `start_date` is omitted.",
                                "default": "2y",
                            },
                            "view": {
                                "type": "string",
                                "enum": SUPPORTED_VIEWS,
                                "description": "Transformation view. Use `level` for raw values. The enum lists global candidates, but each `series_key` supports only its own subset. Common examples: `yoy` for inflation series, `qoq_annualized` for GDP, `change` for rates, and `wow_change` for weekly claims. Unsupported series and view combinations fail directly.",
                                "default": "level",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of observations to return after transformation.",
                                "default": 24,
                                "minimum": 1,
                                "maximum": 120,
                            },
                        },
                        "required": ["series_key"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "macro_regime_context",
                    "description": "Return a curated multi-pillar macro regime summary across inflation, rates, labor, credit conditions, and growth. Use this when the caller wants interpretation instead of one raw series.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pillars": {
                                "type": "array",
                                "items": {"type": "string", "enum": self.pillars},
                                "description": "Optional subset of macro pillars to include. Defaults to all supported pillars.",
                            },
                            "as_of_date": {
                                "type": "string",
                                "description": "Optional observation cutoff date in YYYY-MM-DD format. This uses revised history filtered through that date, not vintage-safe history.",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "macro_release_calendar",
                    "description": "Return curated upcoming or recent macro release dates for the supported release set only. Use this instead of raw FRED release calendar endpoints.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from_date": {
                                "type": "string",
                                "description": "Inclusive start date in YYYY-MM-DD format. Defaults to today.",
                            },
                            "to_date": {
                                "type": "string",
                                "description": "Inclusive end date in YYYY-MM-DD format. Defaults to 45 days after `from_date`.",
                            },
                            "release_keys": {
                                "type": "array",
                                "items": {"type": "string", "enum": release_keys},
                                "description": "Optional release allowlist. Defaults to all supported release keys.",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "macro_release_context",
                    "description": "Return compact release-aware context for one supported macro release, including recent release dates and linked curated series history.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "release_key": {
                                "type": "string",
                                "enum": release_keys,
                                "description": "Supported release key such as cpi, pce, employment_situation, gdp, or weekly_claims.",
                            },
                            "lookback_releases": {
                                "type": "integer",
                                "description": "Number of recent release dates to include.",
                                "default": 6,
                                "minimum": 2,
                                "maximum": 24,
                            },
                        },
                        "required": ["release_key"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "macro_vintage_history",
                    "description": "Return point-in-time-safe history for one curated series using ALFRED realtime dates. Use this for backtests or retrospective questions where revised history would be misleading.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "series_key": {
                                "type": "string",
                                "enum": series_keys,
                                "description": "Registry-backed macro series key.",
                            },
                            "realtime_date": {
                                "type": "string",
                                "description": "Point-in-time realtime date in YYYY-MM-DD format.",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Inclusive start date in YYYY-MM-DD format. If omitted, `period` is used.",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "Inclusive end date in YYYY-MM-DD format. Defaults to `realtime_date`.",
                            },
                            "period": {
                                "type": "string",
                                "enum": list(PERIOD_TO_DAYS.keys()),
                                "description": "Rolling lookback window used when `start_date` is omitted.",
                                "default": "5y",
                            },
                            "view": {
                                "type": "string",
                                "enum": SUPPORTED_VIEWS,
                                "description": "Transformation view. Use `level` for raw values. The enum lists global candidates, but each `series_key` supports only its own subset. Common examples: `yoy` for inflation series, `qoq_annualized` for GDP, `change` for rates, and `wow_change` for weekly claims. Unsupported series and view combinations fail directly.",
                                "default": "level",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of observations to return after transformation.",
                                "default": 24,
                                "minimum": 1,
                                "maximum": 120,
                            },
                        },
                        "required": ["series_key", "realtime_date"],
                    },
                },
            },
        ]

    def _error(self, message: str) -> Dict[str, Any]:
        return {"status": "error", "error": message}

    def _success(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "data": data}

    def _get_series_spec(self, series_key: str) -> Dict[str, Any]:
        if series_key not in self.series_by_key:
            raise ValueError(f"Unsupported series_key '{series_key}'.")
        return self.series_by_key[series_key]

    def _get_release_spec(self, release_key: str) -> Dict[str, Any]:
        if release_key not in self.release_by_key:
            raise ValueError(f"Unsupported release_key '{release_key}'.")
        return self.release_by_key[release_key]

    def _validate_limit(self, limit: int) -> int:
        if limit < 1 or limit > 120:
            raise ValueError("Limit must be between 1 and 120.")
        return limit

    def _validate_release_lookback(self, lookback_releases: int) -> int:
        if lookback_releases < 2 or lookback_releases > 24:
            raise ValueError("lookback_releases must be between 2 and 24.")
        return lookback_releases

    def _allowed_views(self, spec: Dict[str, Any]) -> List[str]:
        return list(dict.fromkeys(["level", *spec["default_views"]]))

    def _validate_view(self, spec: Dict[str, Any], view: str) -> str:
        if view not in self._allowed_views(spec):
            supported = ", ".join(self._allowed_views(spec))
            raise ValueError(f"View '{view}' is unsupported for {spec['key']}. Supported views: {supported}.")
        return view

    def _resolve_window(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        period: Optional[str],
        default_period: str,
        default_end_date: Optional[str] = None,
    ) -> Dict[str, str]:
        resolved_end = _parse_date(end_date or default_end_date) or date.today()
        window: Dict[str, str] = {"end_date": _iso_date(resolved_end)}
        if start_date:
            resolved_start = _parse_date(start_date)
            window["window_source"] = "explicit_dates"
        else:
            resolved_period = period or default_period
            if resolved_period not in PERIOD_TO_DAYS:
                raise ValueError(f"Unsupported period '{resolved_period}'.")
            resolved_start = resolved_end - timedelta(days=PERIOD_TO_DAYS[resolved_period])
            window["window_source"] = "period"
            window["period"] = resolved_period
        if resolved_start is None:
            raise ValueError("Unable to resolve start date.")
        if resolved_start > resolved_end:
            raise ValueError("start_date must be on or before end_date.")
        window["start_date"] = _iso_date(resolved_start)
        return window

    def _frequency_kind(self, frequency: str) -> str:
        normalized = frequency.lower()
        if "quarter" in normalized:
            return "quarterly"
        if "month" in normalized:
            return "monthly"
        if "week" in normalized:
            return "weekly"
        if "day" in normalized:
            return "daily"
        return "other"

    def _year_offset(self, spec: Dict[str, Any]) -> Optional[int]:
        kind = self._frequency_kind(spec["frequency"])
        if kind == "quarterly":
            return 4
        if kind == "monthly":
            return 12
        if kind == "weekly":
            return 52
        return None

    def _snapshot_history_limit(self, spec: Dict[str, Any]) -> int:
        kind = self._frequency_kind(spec["frequency"])
        if kind == "weekly":
            return 80
        if kind == "quarterly":
            return 20
        return 30

    def _view_unit(self, spec: Dict[str, Any], view: str) -> str:
        if view in {"yoy", "mom_annualized", "qoq_annualized"}:
            return "pct"
        if view == "sign":
            return "state"
        if "Percent" in spec["units"] and view in {"change", "mom_change", "yoy_change", "wow_change"}:
            return "percentage_points"
        return spec["units"]

    def _normalize_observation(self, raw: Dict[str, Any], include_realtime: bool = False) -> Optional[Dict[str, Any]]:
        value = _safe_float(raw.get("value"))
        if value is None:
            return None
        observation = {
            "date": raw["date"],
            "value": value,
        }
        if include_realtime:
            realtime_start = raw.get("realtime_start")
            realtime_end = raw.get("realtime_end")
            if realtime_start:
                observation["realtime_start"] = realtime_start
            if realtime_end:
                observation["realtime_end"] = realtime_end
        return observation

    def _series_card(self, spec: Dict[str, Any], live_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        release_key = self.release_key_by_id.get(spec["release_id"])
        card = {
            "key": spec["key"],
            "series_id": spec["series_id"],
            "title": spec["title"],
            "pillar": spec["pillar"],
            "frequency": spec["frequency"],
            "units": spec["units"],
            "default_views": spec["default_views"],
            "release": {
                "release_key": release_key,
                "release_id": spec["release_id"],
                "release_name": spec["release_name"],
            },
        }
        if live_meta:
            card["title"] = live_meta.get("title") or spec["title"]
            card["frequency"] = live_meta.get("frequency") or spec["frequency"]
            card["units"] = live_meta.get("units") or spec["units"]
            card["observation_start"] = live_meta.get("observation_start")
            card["observation_end"] = live_meta.get("observation_end")
            card["last_updated"] = live_meta.get("last_updated")
        return card

    def _metric_point(
        self, spec: Dict[str, Any], observations: List[Dict[str, Any]], idx: int, view: str
    ) -> Optional[Dict[str, Any]]:
        current = observations[idx]
        unit = self._view_unit(spec, view)

        if view == "level":
            return {
                "date": current["date"],
                "value": _round_value(current["value"]),
                "unit": unit,
            }

        if view == "sign":
            return {
                "date": current["date"],
                "value": _sign_label(current["value"]),
                "raw_value": _round_value(current["value"]),
                "unit": unit,
            }

        if view in {"change", "mom_change", "wow_change"}:
            if idx < 1:
                return None
            value = current["value"] - observations[idx - 1]["value"]
            point = {
                "date": current["date"],
                "value": _round_value(value),
                "unit": unit,
                "comparison_date": observations[idx - 1]["date"],
            }
            if "Percent" in spec["units"]:
                point["basis_points"] = _round_value(value * 100, 2)
            return point

        if view == "mom_annualized":
            if idx < 1 or observations[idx - 1]["value"] == 0:
                return None
            value = ((current["value"] / observations[idx - 1]["value"]) ** 12 - 1) * 100
            return {
                "date": current["date"],
                "value": _round_value(value),
                "unit": unit,
                "comparison_date": observations[idx - 1]["date"],
            }

        if view == "qoq_annualized":
            if idx < 1 or observations[idx - 1]["value"] == 0:
                return None
            value = ((current["value"] / observations[idx - 1]["value"]) ** 4 - 1) * 100
            return {
                "date": current["date"],
                "value": _round_value(value),
                "unit": unit,
                "comparison_date": observations[idx - 1]["date"],
            }

        offset = self._year_offset(spec)
        if offset is None:
            return None

        if view == "yoy":
            if idx < offset or observations[idx - offset]["value"] == 0:
                return None
            value = ((current["value"] / observations[idx - offset]["value"]) - 1) * 100
            return {
                "date": current["date"],
                "value": _round_value(value),
                "unit": unit,
                "comparison_date": observations[idx - offset]["date"],
            }

        if view == "yoy_change":
            if idx < offset:
                return None
            value = current["value"] - observations[idx - offset]["value"]
            point = {
                "date": current["date"],
                "value": _round_value(value),
                "unit": unit,
                "comparison_date": observations[idx - offset]["date"],
            }
            if "Percent" in spec["units"]:
                point["basis_points"] = _round_value(value * 100, 2)
            return point

        return None

    def _transform_observations(
        self, spec: Dict[str, Any], observations: List[Dict[str, Any]], view: str
    ) -> List[Dict[str, Any]]:
        transformed = []
        for idx in range(len(observations)):
            point = self._metric_point(spec, observations, idx, view)
            if point is None:
                continue
            if "realtime_start" in observations[idx]:
                point["realtime_start"] = observations[idx]["realtime_start"]
            if "realtime_end" in observations[idx]:
                point["realtime_end"] = observations[idx]["realtime_end"]
            transformed.append(point)
        return transformed

    def _latest_metric_summary(
        self, spec: Dict[str, Any], observations: List[Dict[str, Any]], view: str
    ) -> Optional[Dict[str, Any]]:
        transformed = self._transform_observations(spec, observations, view)
        if not transformed:
            return None
        latest = dict(transformed[-1])
        if view == "sign":
            return latest
        if len(transformed) > 1 and "value" in latest:
            previous = transformed[-2]
            latest["direction"] = _direction(latest["value"], previous["value"])
        return latest

    def _numeric_evidence(self, snapshot: Dict[str, Any], metric_key: str) -> Optional[float]:
        metric = snapshot["derived"].get(metric_key)
        if metric is None:
            return None
        return metric.get("value")

    def _pillar_release_key(self, spec: Dict[str, Any]) -> Optional[str]:
        return self.release_key_by_id.get(spec["release_id"]) or None

    def _summary_from_snapshots(self, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "series_key": snapshot["series"]["key"],
                "series_id": snapshot["series"]["series_id"],
                "title": snapshot["series"]["title"],
                "latest_observation": snapshot["latest_observation"],
                "derived": snapshot["derived"],
            }
            for snapshot in snapshots
        ]

    def _summarize_inflation(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        yoy_values = [
            value for value in [self._numeric_evidence(snapshot, "yoy") for snapshot in snapshots] if value is not None
        ]
        momentum_values = [
            value
            for value in [self._numeric_evidence(snapshot, "mom_annualized") for snapshot in snapshots]
            if value is not None
        ]
        avg_yoy = sum(yoy_values) / len(yoy_values) if yoy_values else None
        avg_momentum = sum(momentum_values) / len(momentum_values) if momentum_values else None

        state = "mixed"
        summary = "Inflation evidence is mixed across the curated registry."
        if avg_yoy is not None and avg_momentum is not None:
            if avg_yoy >= 3.0 and avg_momentum >= avg_yoy:
                state = "rising"
                summary = "Inflation remains elevated and recent momentum is re-accelerating."
            elif avg_yoy >= 3.0 and avg_momentum < avg_yoy:
                state = "easing"
                summary = "Inflation is still elevated, but near-term momentum is easing."
            elif avg_yoy <= 2.5 and avg_momentum <= 2.5:
                state = "contained"
                summary = "Inflation looks comparatively contained across headline and core gauges."
            else:
                state = "sticky"
                summary = "Inflation is off the peak but still sticky versus a clean target-consistent path."

        return {"state": state, "summary": summary}

    def _summarize_rates(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        by_key = {snapshot["series"]["key"]: snapshot for snapshot in snapshots}
        fed_funds = by_key.get("fed_funds", {}).get("latest_observation", {}).get("value")
        curve = by_key.get("curve_10y_minus_2y", {}).get("latest_observation", {}).get("value")
        two_year_change = self._numeric_evidence(by_key.get("ust_2y", {"derived": {}}), "change")

        state = "mixed"
        summary = "Rates are mixed."
        if fed_funds is not None and curve is not None:
            if fed_funds >= 4.0 and curve < 0:
                state = "tight"
                summary = "Policy and front-end rates still point to a restrictive rates backdrop."
            elif fed_funds >= 4.0:
                state = "restrictive"
                summary = "Rates remain high enough to read as restrictive even without inversion."
            elif two_year_change is not None and two_year_change < 0:
                state = "easing"
                summary = "Front-end rates are moving lower, consistent with an easing impulse."
            else:
                state = "normalizing"
                summary = "Rates look closer to normalization than outright tightening."

        return {"state": state, "summary": summary}

    def _summarize_labor(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        by_key = {snapshot["series"]["key"]: snapshot for snapshot in snapshots}
        unemployment = by_key.get("unemployment_rate", {}).get("latest_observation", {}).get("value")
        unemployment_change = self._numeric_evidence(by_key.get("unemployment_rate", {"derived": {}}), "change")
        payrolls_mom = self._numeric_evidence(by_key.get("nonfarm_payrolls", {"derived": {}}), "mom_change")
        claims_wow = self._numeric_evidence(by_key.get("initial_claims", {"derived": {}}), "wow_change")

        state = "mixed"
        summary = "Labor evidence is mixed."
        if unemployment is not None:
            if unemployment <= 4.2 and (claims_wow is None or claims_wow <= 0):
                state = "tight"
                summary = "Labor conditions still look tight with low unemployment and no obvious claims deterioration."
            elif (unemployment_change is not None and unemployment_change > 0.1) or (
                claims_wow is not None and claims_wow > 0
            ):
                state = "softening"
                summary = "Labor data is softening through unemployment or claims deterioration."
            elif payrolls_mom is not None and payrolls_mom > 0:
                state = "steady"
                summary = "Payroll growth remains positive and labor conditions look broadly steady."

        return {"state": state, "summary": summary}

    def _summarize_credit(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        by_key = {snapshot["series"]["key"]: snapshot for snapshot in snapshots}
        nfci = by_key.get("nfci", {}).get("latest_observation", {}).get("value")
        baa_spread = by_key.get("baa_treasury_spread", {}).get("latest_observation", {}).get("value")
        nfci_change = self._numeric_evidence(by_key.get("nfci", {"derived": {}}), "change")

        state = "mixed"
        summary = "Credit conditions are mixed."
        if nfci is not None and baa_spread is not None:
            if nfci > 0 or baa_spread >= 2.5:
                state = "tight"
                summary = "Credit conditions read as tight through NFCI or corporate spread stress."
            elif nfci < -0.5 and baa_spread < 2.0 and (nfci_change is None or nfci_change <= 0):
                state = "easy"
                summary = "Credit conditions look relatively easy by both NFCI and spread measures."
            else:
                state = "stable"
                summary = "Credit conditions are stable but not especially loose."

        return {"state": state, "summary": summary}

    def _summarize_growth(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        growth = snapshots[0]
        qoq = self._numeric_evidence(growth, "qoq_annualized")
        yoy = self._numeric_evidence(growth, "yoy")

        state = "mixed"
        summary = "Growth evidence is mixed."
        if qoq is not None:
            if qoq < 0:
                state = "contracting"
                summary = "Real GDP momentum is contracting on a qoq annualized basis."
            elif qoq < 1.5:
                state = "slowing"
                summary = "Real GDP is still positive but running at a slower pace."
            else:
                state = "expanding"
                summary = "Real GDP still points to an expanding growth backdrop."
        elif yoy is not None and yoy > 0:
            state = "expanding"
            summary = "Real GDP is still above year-ago levels."

        return {"state": state, "summary": summary}

    def _pillar_summary(self, pillar: str, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        if pillar == "inflation":
            summary = self._summarize_inflation(snapshots)
        elif pillar == "rates":
            summary = self._summarize_rates(snapshots)
        elif pillar == "labor":
            summary = self._summarize_labor(snapshots)
        elif pillar == "credit_conditions":
            summary = self._summarize_credit(snapshots)
        else:
            summary = self._summarize_growth(snapshots)

        summary["evidence"] = self._summary_from_snapshots(snapshots)
        return summary

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2, delay=1.0)
    async def _fred_get(self, endpoint: str, timeout: int = 20, **params) -> Dict[str, Any]:
        if not self.fred_api_key:
            return self._error("FRED_API_KEY is missing from the environment.")

        payload = await self._api_request(
            f"{FRED_BASE_URL}/{endpoint}",
            params={**params, "api_key": self.fred_api_key, "file_type": "json"},
            timeout=timeout,
        )
        if "error" in payload:
            raise RuntimeError(payload["error"])
        if payload.get("error_code"):
            return self._error(payload.get("error_message") or f"FRED error {payload['error_code']}.")
        return payload

    async def _series_metadata(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        payload = await self._fred_get("series", series_id=spec["series_id"])
        if payload.get("status") == "error":
            return payload
        if not payload["seriess"]:
            return self._error(f"No metadata returned for series '{spec['series_id']}'.")
        return payload["seriess"][0]

    async def _series_observations(
        self,
        spec: Dict[str, Any],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None,
        sort_order: str = "asc",
        realtime_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "series_id": spec["series_id"],
            "sort_order": sort_order,
        }
        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date
        if limit:
            params["limit"] = limit
        if realtime_date:
            params["realtime_start"] = realtime_date
            params["realtime_end"] = realtime_date

        payload = await self._fred_get("series/observations", **params)
        if payload.get("status") == "error":
            return payload

        observations = []
        for item in payload["observations"]:
            observation = self._normalize_observation(item, include_realtime=realtime_date is not None)
            if observation is None:
                continue
            observations.append(observation)

        if sort_order == "desc":
            observations.reverse()

        if not observations:
            return self._error(f"No observations returned for series '{spec['key']}'.")
        return {"status": "success", "data": observations}

    async def _release_metadata(self, release_spec: Dict[str, Any]) -> Dict[str, Any]:
        payload = await self._fred_get("release", release_id=release_spec["release_id"])
        if payload.get("status") == "error":
            return payload
        if not payload["releases"]:
            return self._error(f"No metadata returned for release '{release_spec['release_id']}'.")
        return payload["releases"][0]

    async def _release_dates(self, release_spec: Dict[str, Any], limit: int, offset: int = 0) -> Dict[str, Any]:
        payload = await self._fred_get(
            "release/dates",
            release_id=release_spec["release_id"],
            limit=limit,
            offset=offset,
            sort_order="desc",
            timeout=25,
        )
        if payload.get("status") == "error":
            return payload
        return {"status": "success", "data": [item["date"] for item in payload["release_dates"]]}

    async def _release_dates_in_window(self, release_spec: Dict[str, Any], start: date, end: date) -> Dict[str, Any]:
        offset = 0
        batch_size = 1000
        matched_dates: List[str] = []

        while True:
            dates_result = await self._release_dates(release_spec, limit=batch_size, offset=offset)
            if dates_result["status"] == "error":
                return dates_result

            batch = dates_result["data"]
            if not batch:
                break

            matched_dates.extend([value for value in batch if start <= _parse_date(value) <= end])
            oldest_date = _parse_date(batch[-1])
            if len(batch) < batch_size or oldest_date < start:
                break
            offset += batch_size

        return {"status": "success", "data": sorted(matched_dates)}

    async def _snapshot_payload(self, spec: Dict[str, Any], observation_end: Optional[str] = None) -> Dict[str, Any]:
        live_meta = await self._series_metadata(spec)
        if live_meta.get("status") == "error":
            return live_meta

        observations_result = await self._series_observations(
            spec,
            end_date=observation_end,
            limit=self._snapshot_history_limit(spec),
            sort_order="desc",
        )
        if observations_result["status"] == "error":
            return observations_result

        observations = observations_result["data"]
        derived = {}
        for view in spec["default_views"]:
            if view == "level":
                continue
            summary = self._latest_metric_summary(spec, observations, view)
            if summary:
                derived[view] = summary

        payload = {
            "series": self._series_card(spec, live_meta),
            "latest_observation": {
                "date": observations[-1]["date"],
                "value": _round_value(observations[-1]["value"]),
                "unit": spec["units"],
            },
            "previous_observation": None,
            "derived": derived,
        }
        if len(observations) > 1:
            payload["previous_observation"] = {
                "date": observations[-2]["date"],
                "value": _round_value(observations[-2]["value"]),
                "unit": spec["units"],
            }
        release_key = self._pillar_release_key(spec)
        if release_key:
            payload["release_context"] = {
                "release_key": release_key,
                "release_id": spec["release_id"],
                "release_name": spec["release_name"],
            }
        return payload

    async def _history_payload(
        self,
        spec: Dict[str, Any],
        start_date: Optional[str],
        end_date: Optional[str],
        period: Optional[str],
        view: str,
        limit: int,
        realtime_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        resolved_window = self._resolve_window(
            start_date,
            end_date,
            period,
            "2y" if realtime_date is None else "5y",
            default_end_date=realtime_date,
        )
        live_meta = None
        if realtime_date is None:
            live_meta = await self._series_metadata(spec)
            if live_meta.get("status") == "error":
                return live_meta

        observations_result = await self._series_observations(
            spec,
            start_date=resolved_window["start_date"],
            end_date=resolved_window["end_date"],
            sort_order="asc",
            realtime_date=realtime_date,
        )
        if observations_result["status"] == "error":
            return observations_result

        transformed = self._transform_observations(spec, observations_result["data"], view)
        if not transformed:
            return self._error(f"No transformed observations available for {spec['key']} with view '{view}'.")

        latest_summary = dict(transformed[-1])
        if view != "sign" and len(transformed) > 1 and "value" in latest_summary:
            latest_summary["direction"] = _direction(latest_summary["value"], transformed[-2]["value"])

        payload = {
            "series": self._series_card(spec, live_meta),
            "resolved_window": resolved_window,
            "view": view,
            "available_views": self._allowed_views(spec),
            "observations": transformed[-limit:],
            "latest_summary": latest_summary,
            "point_in_time_safe": realtime_date is not None,
        }
        if realtime_date:
            payload["realtime_date"] = realtime_date
            payload["note"] = "This history uses ALFRED realtime filters and is safe for point-in-time context."
        return payload

    async def macro_series_snapshot(self, series_key: str) -> Dict[str, Any]:
        try:
            spec = self._get_series_spec(series_key)
            payload = await self._snapshot_payload(spec)
            if payload.get("status") == "error":
                return payload
            return self._success(payload)
        except Exception as exc:
            return self._error(str(exc))

    async def macro_series_history(
        self,
        series_key: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = "2y",
        view: str = "level",
        limit: int = 24,
    ) -> Dict[str, Any]:
        try:
            spec = self._get_series_spec(series_key)
            self._validate_view(spec, view)
            limit = self._validate_limit(limit)
            payload = await self._history_payload(spec, start_date, end_date, period, view, limit)
            if payload.get("status") == "error":
                return payload
            return self._success(payload)
        except Exception as exc:
            return self._error(str(exc))

    async def macro_vintage_history(
        self,
        series_key: str,
        realtime_date: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = "5y",
        view: str = "level",
        limit: int = 24,
    ) -> Dict[str, Any]:
        try:
            _parse_date(realtime_date)
            spec = self._get_series_spec(series_key)
            self._validate_view(spec, view)
            limit = self._validate_limit(limit)
            payload = await self._history_payload(spec, start_date, end_date, period, view, limit, realtime_date)
            if payload.get("status") == "error":
                return payload
            return self._success(payload)
        except Exception as exc:
            return self._error(str(exc))

    async def macro_release_calendar(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        release_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        try:
            start = _parse_date(from_date) or date.today()
            end = _parse_date(to_date) or (start + timedelta(days=45))
            if start > end:
                raise ValueError("from_date must be on or before to_date.")

            selected_keys = release_keys or list(self.release_by_key.keys())
            for release_key in selected_keys:
                self._get_release_spec(release_key)

            releases = []
            for release_key in selected_keys:
                release_spec = self._get_release_spec(release_key)
                dates_result = await self._release_dates_in_window(release_spec, start, end)
                if dates_result["status"] == "error":
                    return dates_result

                if not dates_result["data"]:
                    continue

                releases.append(
                    {
                        "release_key": release_key,
                        "release_id": release_spec["release_id"],
                        "release_name": release_spec["release_name"],
                        "series_keys": release_spec["series_keys"],
                        "release_dates": dates_result["data"],
                    }
                )

            return self._success(
                {
                    "resolved_window": {
                        "from_date": _iso_date(start),
                        "to_date": _iso_date(end),
                    },
                    "releases": releases,
                }
            )
        except Exception as exc:
            return self._error(str(exc))

    async def macro_release_context(self, release_key: str, lookback_releases: int = 6) -> Dict[str, Any]:
        try:
            release_spec = self._get_release_spec(release_key)
            lookback_releases = self._validate_release_lookback(lookback_releases)

            metadata_result = await self._release_metadata(release_spec)
            if metadata_result.get("status") == "error":
                return metadata_result

            dates_result = await self._release_dates(release_spec, limit=lookback_releases)
            if dates_result["status"] == "error":
                return dates_result

            linked_series = []
            for series_key in release_spec["series_keys"]:
                spec = self._get_series_spec(series_key)
                snapshot = await self._snapshot_payload(spec)
                if snapshot.get("status") == "error":
                    return snapshot
                history = await self._history_payload(spec, None, None, "2y", "level", min(lookback_releases, 12))
                if history.get("status") == "error":
                    return history
                linked_series.append(
                    {
                        "series": snapshot["series"],
                        "latest_observation": snapshot["latest_observation"],
                        "derived": snapshot["derived"],
                        "recent_history": history["observations"],
                    }
                )

            release_dates = dates_result["data"]
            return self._success(
                {
                    "release": {
                        "release_key": release_key,
                        "release_id": release_spec["release_id"],
                        "release_name": metadata_result.get("name") or release_spec["release_name"],
                        "press_release": metadata_result.get("press_release"),
                        "link": metadata_result.get("link"),
                    },
                    "latest_release_date": release_dates[0] if release_dates else None,
                    "prior_release_dates": release_dates[1:],
                    "linked_series": linked_series,
                }
            )
        except Exception as exc:
            return self._error(str(exc))

    async def macro_regime_context(
        self, pillars: Optional[List[str]] = None, as_of_date: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            if as_of_date:
                _parse_date(as_of_date)
            selected_pillars = pillars or self.pillars
            for pillar in selected_pillars:
                if pillar not in self.pillars:
                    raise ValueError(f"Unsupported pillar '{pillar}'.")

            pillar_sections = []
            regime_states = []
            for pillar in selected_pillars:
                snapshots = []
                for series in self.registry["pillars"][pillar]:
                    spec = self._get_series_spec(series["key"])
                    snapshot = await self._snapshot_payload(spec, observation_end=as_of_date)
                    if snapshot.get("status") == "error":
                        return snapshot
                    snapshots.append(snapshot)

                pillar_summary = self._pillar_summary(pillar, snapshots)
                pillar_sections.append(
                    {
                        "pillar": pillar,
                        "state": pillar_summary["state"],
                        "summary": pillar_summary["summary"],
                        "evidence": pillar_summary["evidence"],
                    }
                )
                regime_states.append(f"{pillar}: {pillar_summary['state']}")

            note = "This regime view uses revised series history."
            if as_of_date:
                note = (
                    f"This regime view uses revised history filtered through {as_of_date}. "
                    "Use macro_vintage_history for point-in-time-safe context."
                )

            return self._success(
                {
                    "as_of_date": as_of_date,
                    "point_in_time_safe": False,
                    "overall_summary": "; ".join(regime_states),
                    "pillars": pillar_sections,
                    "note": note,
                }
            )
        except Exception as exc:
            return self._error(str(exc))

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            if tool_name == "macro_series_snapshot":
                return await self.macro_series_snapshot(function_args["series_key"])
            if tool_name == "macro_series_history":
                return await self.macro_series_history(
                    series_key=function_args["series_key"],
                    start_date=function_args.get("start_date"),
                    end_date=function_args.get("end_date"),
                    period=function_args.get("period", "2y"),
                    view=function_args.get("view", "level"),
                    limit=function_args.get("limit", 24),
                )
            if tool_name == "macro_regime_context":
                return await self.macro_regime_context(
                    pillars=function_args.get("pillars"),
                    as_of_date=function_args.get("as_of_date"),
                )
            if tool_name == "macro_release_calendar":
                return await self.macro_release_calendar(
                    from_date=function_args.get("from_date"),
                    to_date=function_args.get("to_date"),
                    release_keys=function_args.get("release_keys"),
                )
            if tool_name == "macro_release_context":
                return await self.macro_release_context(
                    release_key=function_args["release_key"],
                    lookback_releases=function_args.get("lookback_releases", 6),
                )
            if tool_name == "macro_vintage_history":
                return await self.macro_vintage_history(
                    series_key=function_args["series_key"],
                    realtime_date=function_args["realtime_date"],
                    start_date=function_args.get("start_date"),
                    end_date=function_args.get("end_date"),
                    period=function_args.get("period", "5y"),
                    view=function_args.get("view", "level"),
                    limit=function_args.get("limit", 24),
                )
            return self._error(f"Unsupported tool: {tool_name}")
        except Exception as exc:
            logger.error(f"FRED macro tool failure for {tool_name}: {exc}")
            return self._error(str(exc))
