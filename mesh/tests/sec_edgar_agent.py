import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.sec_edgar_agent import SecEdgarAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    "resolve_company_apple": {
        "input": {
            "tool": "resolve_company",
            "tool_arguments": {"query": "AAPL", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Resolve a stock ticker into the canonical SEC issuer record.",
        "expected_status": "success",
    },
    "resolve_company_missing": {
        "input": {
            "tool": "resolve_company",
            "tool_arguments": {"query": "zxqwvut nonexistent corp 123456789", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Unknown issuer returns a direct SEC resolution error.",
        "expected_status": "error",
    },
    "filing_timeline_tesla": {
        "input": {
            "tool": "filing_timeline",
            "tool_arguments": {"query": "TSLA", "forms": ["8-K", "10-Q", "10-K"], "limit": 6},
            "raw_data_only": True,
        },
        "description": "Compact timeline of major Tesla filings.",
        "expected_status": "success",
    },
    "filing_diff_apple_10q": {
        "input": {
            "tool": "filing_diff",
            "tool_arguments": {"query": "AAPL", "form": "10-Q", "paragraph_limit": 3},
            "raw_data_only": True,
        },
        "description": "Paragraph-level comparison between Apple's latest and previous 10-Q.",
        "expected_status": "success",
    },
    "xbrl_fact_trends_apple_revenue": {
        "input": {
            "tool": "xbrl_fact_trends",
            "tool_arguments": {"query": "AAPL", "metric": "revenue", "frequency": "quarterly", "limit": 6},
            "raw_data_only": True,
        },
        "description": "Direct SEC-reported quarterly revenue trend for Apple.",
        "expected_status": "success",
    },
    "xbrl_fact_trends_plural_revenues_string_limit": {
        "input": {
            "tool": "xbrl_fact_trends",
            "tool_arguments": {"query": "AAPL", "metric": "Revenues", "frequency": "quarterly", "limit": "6"},
            "raw_data_only": True,
        },
        "description": "Plural revenue metric and stringified limit normalize cleanly and still return current SEC revenue facts.",
        "expected_status": "success",
    },
    "xbrl_fact_trends_legacy_concept_periods": {
        "input": {
            "tool": "xbrl_fact_trends",
            "tool_arguments": {"cik": "AAPL", "concept": "EarningsPerShareBasic", "periods": "6"},
            "raw_data_only": True,
        },
        "description": "Legacy concept and periods aliases normalize to the current XBRL fact trend contract.",
        "expected_status": "success",
    },
    "xbrl_fact_trends_invalid_metric": {
        "input": {
            "tool": "xbrl_fact_trends",
            "tool_arguments": {"query": "AAPL", "metric": "totally invented sec metric", "frequency": "quarterly"},
            "raw_data_only": True,
        },
        "description": "Invalid XBRL metric query fails directly instead of returning junk.",
        "expected_status": "error",
    },
    "insider_activity_tesla": {
        "input": {
            "tool": "insider_activity",
            "tool_arguments": {"query": "Tesla", "limit": 3},
            "raw_data_only": True,
        },
        "description": "Recent Tesla Forms 3/4/5 with parsed transaction rows.",
        "expected_status": "success",
    },
    "insider_activity_string_limit": {
        "input": {
            "tool": "insider_activity",
            "tool_arguments": {"query": "AAPL", "limit": "3"},
            "raw_data_only": True,
        },
        "description": "Stringified limit should normalize for insider activity.",
        "expected_status": "success",
    },
    "activist_watch_apple": {
        "input": {
            "tool": "activist_watch",
            "tool_arguments": {"query": "Apple", "limit": 2},
            "raw_data_only": True,
        },
        "description": "Recent Apple 13D/13G activity with filer and ownership fields.",
        "expected_status": "success",
    },
    "institutional_holders_apple": {
        "input": {
            "tool": "institutional_holders",
            "tool_arguments": {"query": "Apple", "limit": 5},
            "raw_data_only": True,
        },
        "description": "Issuer-level latest-quarter 13F holder snapshot for Apple.",
        "expected_status": "success",
    },
    "institutional_holders_legacy_top_n": {
        "input": {
            "tool": "institutional_holders",
            "tool_arguments": {"cik": "AAPL", "top_n": "5"},
            "raw_data_only": True,
        },
        "description": "Legacy issuer alias and stringified top_n should normalize for institutional holders.",
        "expected_status": "success",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(SecEdgarAgent, TEST_CASES, delay_seconds=0.4))
