import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.sec_edgar_agent import SecEdgarAgent


async def run_case(name, args, coro):
    try:
        preview = await asyncio.wait_for(coro, timeout=150)
        return {
            "tool": name,
            "arguments": args,
            "status": "error" if "error" in preview else "success",
            "data_keys": list(preview.keys()),
            "preview": preview,
        }
    except Exception as exc:
        return {
            "tool": name,
            "arguments": args,
            "status": "error",
            "error": str(exc),
        }


async def run():
    agent = SecEdgarAgent()
    try:
        results = [
            await run_case("resolve_company", {"query": "AAPL", "limit": 3}, agent.resolve_company("AAPL", 3)),
            await run_case(
                "filing_timeline",
                {"query": "TSLA", "forms": ["8-K", "10-K", "10-Q"], "limit": 4},
                agent.filing_timeline("TSLA", ["8-K", "10-K", "10-Q"], 4),
            ),
            await run_case(
                "filing_diff",
                {"query": "AAPL", "form": "10-Q", "paragraph_limit": 2},
                agent.filing_diff("AAPL", "10-Q", 2),
            ),
            await run_case(
                "xbrl_fact_trends",
                {"query": "AAPL", "metric": "revenue", "frequency": "quarterly", "limit": 4},
                agent.xbrl_fact_trends("AAPL", "revenue", frequency="quarterly", limit=4),
            ),
            await run_case("insider_activity", {"query": "TSLA", "limit": 2}, agent.insider_activity("TSLA", 2)),
            await run_case("activist_watch", {"query": "Apple", "limit": 1}, agent.activist_watch("Apple", 1)),
            await run_case(
                "institutional_holders",
                {"query": "Apple", "limit": 3},
                agent.institutional_holders("Apple", 3),
            ),
        ]
        print(json.dumps(results, indent=2))
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run())
