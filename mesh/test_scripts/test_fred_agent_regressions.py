import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.fred_macro_agent import FredMacroAgent


def test_headline_cpi_yoy_calendar_alignment() -> None:
    """April CPI YoY must compare to April of the prior year, not March."""
    agent = FredMacroAgent()
    spec = agent.series_by_key["headline_cpi"]
    observations = [
        {"date": "2025-03-01", "value": 319.785},
        {"date": "2025-04-01", "value": 320.302},
        {"date": "2025-09-01", "value": 324.245},
        {"date": "2025-11-01", "value": 325.063},
        {"date": "2026-04-01", "value": 332.407},
    ]
    point = agent._metric_point(spec, observations, len(observations) - 1, "yoy")
    assert point is not None
    assert point["comparison_date"] == "2025-04-01"
    assert abs(point["value"] - 3.78) < 0.05


async def main():
    agent = FredMacroAgent()
    try:
        vintage = await agent.macro_vintage_history(
            series_key="real_gdp",
            realtime_date="2020-07-01",
            period="10y",
            limit=8,
        )
        assert vintage["status"] == "success", vintage
        vintage_data = vintage["data"]
        assert vintage_data["point_in_time_safe"] is True, vintage_data
        assert "observation_end" not in vintage_data["series"], vintage_data["series"]
        assert "last_updated" not in vintage_data["series"], vintage_data["series"]

        explicit_window = await agent.macro_series_history(
            series_key="headline_cpi",
            start_date="2024-01-01",
            end_date="2025-01-31",
            view="level",
            limit=6,
        )
        assert explicit_window["status"] == "success", explicit_window
        resolved_window = explicit_window["data"]["resolved_window"]
        assert resolved_window["window_source"] == "explicit_dates", resolved_window
        assert "period" not in resolved_window, resolved_window

        wide_calendar = await agent.macro_release_calendar(
            from_date="2025-01-01",
            to_date="2026-03-31",
            release_keys=["weekly_claims"],
        )
        assert wide_calendar["status"] == "success", wide_calendar
        releases = wide_calendar["data"]["releases"]
        assert len(releases) == 1, releases
        assert len(releases[0]["release_dates"]) > 18, releases[0]

        invalid_view = await agent.macro_series_history(
            series_key="ust_10y",
            period="1y",
            view="yoy",
        )
        assert invalid_view["status"] == "error", invalid_view

        print("FRED agent regressions passed")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
