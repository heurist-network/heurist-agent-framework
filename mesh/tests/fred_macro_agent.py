import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.fred_macro_agent import FredMacroAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "macro_series_snapshot_headline_cpi": {
        "input": {
            "tool": "macro_series_snapshot",
            "tool_arguments": {"series_key": "headline_cpi"},
            "raw_data_only": True,
        },
        "description": "Compact latest snapshot for headline CPI.",
        "expected_status": "success",
    },
    "macro_series_snapshot_invalid_series": {
        "input": {
            "tool": "macro_series_snapshot",
            "tool_arguments": {"series_key": "totally_fake_series"},
            "raw_data_only": True,
        },
        "description": "Unsupported series keys fail directly instead of falling back to search.",
        "expected_status": "error",
    },
    "macro_series_history_core_pce_yoy": {
        "input": {
            "tool": "macro_series_history",
            "tool_arguments": {"series_key": "core_pce", "period": "5y", "view": "yoy", "limit": 12},
            "raw_data_only": True,
        },
        "description": "Bounded YoY history for core PCE.",
        "expected_status": "success",
    },
    "macro_series_history_invalid_view": {
        "input": {
            "tool": "macro_series_history",
            "tool_arguments": {"series_key": "ust_10y", "period": "1y", "view": "yoy"},
            "raw_data_only": True,
        },
        "description": "Unsupported transforms fail directly for series that do not advertise them.",
        "expected_status": "error",
    },
    "macro_series_history_explicit_start_date": {
        "input": {
            "tool": "macro_series_history",
            "tool_arguments": {
                "series_key": "headline_cpi",
                "start_date": "2024-01-01",
                "end_date": "2025-01-31",
                "view": "level",
                "limit": 6,
            },
            "raw_data_only": True,
        },
        "description": "Explicit date windows should work without pretending a rolling period was used.",
        "expected_status": "success",
    },
    "macro_regime_context_all_pillars": {
        "input": {
            "tool": "macro_regime_context",
            "tool_arguments": {},
            "raw_data_only": True,
        },
        "description": "Curated multi-pillar regime summary across the default macro set.",
        "expected_status": "success",
    },
    "macro_regime_context_invalid_pillar": {
        "input": {
            "tool": "macro_regime_context",
            "tool_arguments": {"pillars": ["inflation", "housing"]},
            "raw_data_only": True,
        },
        "description": "Invalid pillar filters fail directly.",
        "expected_status": "error",
    },
    "macro_release_calendar_curated_window": {
        "input": {
            "tool": "macro_release_calendar",
            "tool_arguments": {"from_date": "2026-03-01", "to_date": "2026-04-30", "release_keys": ["cpi", "gdp"]},
            "raw_data_only": True,
        },
        "description": "Curated release calendar restricted to selected release keys and date window.",
        "expected_status": "success",
    },
    "macro_release_calendar_invalid_release_key": {
        "input": {
            "tool": "macro_release_calendar",
            "tool_arguments": {"from_date": "2026-03-01", "to_date": "2026-04-30", "release_keys": ["cpi", "rates"]},
            "raw_data_only": True,
        },
        "description": "Unsupported release allowlist entries fail directly.",
        "expected_status": "error",
    },
    "macro_release_calendar_weekly_claims_wide_window": {
        "input": {
            "tool": "macro_release_calendar",
            "tool_arguments": {
                "from_date": "2025-01-01",
                "to_date": "2026-03-31",
                "release_keys": ["weekly_claims"],
            },
            "raw_data_only": True,
        },
        "description": "Wide release windows should not truncate weekly releases to a small fixed fetch size.",
        "expected_status": "success",
    },
    "macro_release_context_cpi": {
        "input": {
            "tool": "macro_release_context",
            "tool_arguments": {"release_key": "cpi", "lookback_releases": 4},
            "raw_data_only": True,
        },
        "description": "CPI release context with recent release dates and linked series.",
        "expected_status": "success",
    },
    "macro_release_context_invalid_release_key": {
        "input": {
            "tool": "macro_release_context",
            "tool_arguments": {"release_key": "h15"},
            "raw_data_only": True,
        },
        "description": "Unsupported release keys fail directly for release context requests.",
        "expected_status": "error",
    },
    "macro_vintage_history_real_gdp": {
        "input": {
            "tool": "macro_vintage_history",
            "tool_arguments": {"series_key": "real_gdp", "realtime_date": "2020-07-01", "period": "10y", "limit": 8},
            "raw_data_only": True,
        },
        "description": "Point-in-time-safe GDP history using ALFRED realtime filters.",
        "expected_status": "success",
    },
    "macro_vintage_history_bad_date": {
        "input": {
            "tool": "macro_vintage_history",
            "tool_arguments": {"series_key": "real_gdp", "realtime_date": "2020/07/01"},
            "raw_data_only": True,
        },
        "description": "Invalid realtime dates fail directly.",
        "expected_status": "error",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(FredMacroAgent, TEST_CASES, delay_seconds=0.4))
