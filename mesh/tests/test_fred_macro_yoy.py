"""Unit tests for FRED macro YoY calendar alignment (no network)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mesh.agents.fred_macro_agent import FredMacroAgent  # noqa: E402


@pytest.fixture
def agent() -> FredMacroAgent:
    return FredMacroAgent()


@pytest.fixture
def headline_cpi_spec(agent: FredMacroAgent) -> dict:
    return agent.series_by_key["headline_cpi"]


def test_yoy_uses_same_calendar_month_despite_missing_rows(
    agent: FredMacroAgent, headline_cpi_spec: dict
) -> None:
    """Regression: a gap in monthly rows must not shift YoY to the prior month."""
    observations = [
        {"date": "2025-03-01", "value": 319.785},
        {"date": "2025-04-01", "value": 320.302},
        {"date": "2025-09-01", "value": 324.245},
        {"date": "2025-11-01", "value": 325.063},
        {"date": "2026-04-01", "value": 332.407},
    ]
    point = agent._metric_point(headline_cpi_spec, observations, len(observations) - 1, "yoy")
    assert point is not None
    assert point["comparison_date"] == "2025-04-01"
    assert point["value"] == pytest.approx(3.7794, rel=1e-3)


def test_yoy_returns_none_when_prior_year_month_missing(
    agent: FredMacroAgent, headline_cpi_spec: dict
) -> None:
    observations = [
        {"date": "2025-03-01", "value": 319.785},
        {"date": "2026-04-01", "value": 332.407},
    ]
    point = agent._metric_point(headline_cpi_spec, observations, 1, "yoy")
    assert point is None


def test_yoy_change_uses_calendar_year_ago(agent: FredMacroAgent) -> None:
    spec = agent.series_by_key["ust_10y"]
    observations = [
        {"date": "2024-05-15", "value": 4.36},
        {"date": "2025-03-15", "value": 4.10},
        {"date": "2025-05-15", "value": 4.50},
        {"date": "2026-05-15", "value": 4.59},
    ]
    point = agent._metric_point(spec, observations, 3, "yoy_change")
    assert point is not None
    assert point["comparison_date"] == "2025-05-15"
    assert point["value"] == pytest.approx(0.09, rel=1e-3)
