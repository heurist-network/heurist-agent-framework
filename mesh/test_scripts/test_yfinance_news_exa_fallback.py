import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents import yahoo_finance_agent as yahoo_module
from mesh.agents.yahoo_finance_agent import YahooFinanceAgent


class StubYahooFinanceAgent(YahooFinanceAgent):
    def __init__(self):
        super().__init__()
        self.exa_calls = []

    async def _call_agent_tool_safe(
        self,
        module: str,
        class_name: str,
        tool_name: str,
        tool_args=None,
        *,
        raw_data_only: bool = True,
        session_context=None,
        log_instance=None,
        context=None,
        error_status: str = "error",
    ):
        self.exa_calls.append(
            {
                "module": module,
                "class_name": class_name,
                "tool_name": tool_name,
                "tool_args": tool_args or {},
            }
        )
        return {
            "status": "success",
            "data": {
                "processed_summary": "Stubbed Exa digest summary.",
            },
        }


class FakeSearch:
    def __init__(self, query, max_results, news_count, include_cb):
        self.query = query
        self.quotes = []
        self.news = [
            {
                "title": f"{query} headline 1",
                "publisher": "Example Publisher",
                "providerPublishTime": 1760000000,
                "link": "https://example.com/1",
                "type": "STORY",
                "relatedTickers": ["TSLA"],
            },
            {
                "title": f"{query} headline 2",
                "publisher": "Example Publisher",
                "providerPublishTime": 1760003600,
                "link": "https://example.com/2",
                "type": "STORY",
                "relatedTickers": ["TSLA"],
            },
        ][:news_count]


async def main():
    agent = StubYahooFinanceAgent()
    original_search = yahoo_module.yf.Search
    failures = []

    yahoo_module.yf.Search = FakeSearch
    try:
        fallback_result = await agent.news_search("oil prices outlook", limit="8")
        fallback_data = fallback_result.get("data") or {}
        if fallback_result.get("status") != "success":
            failures.append("3-word queries should redirect to Exa digest fallback")
        if fallback_data.get("processed_summary") != "Stubbed Exa digest summary.":
            failures.append("Exa digest fallback should return the nested processed summary")
        if not agent.exa_calls or agent.exa_calls[0]["tool_args"].get("search_term") != "oil prices outlook":
            failures.append("3-word queries should invoke ExaSearchDigestAgent.exa_web_search")
        if agent.exa_calls and agent.exa_calls[0]["tool_args"].get("limit") != 8:
            failures.append("Exa fallback should preserve numeric limits within Exa bounds")

        agent.exa_calls.clear()
        yahoo_result = await agent.news_search("Tesla news", limit="2")
        yahoo_data = yahoo_result.get("data") or {}
        yahoo_items = yahoo_data.get("items") or []
        if yahoo_result.get("status") != "success":
            failures.append("2-word queries should still use Yahoo news search")
        if len(yahoo_items) != 2:
            failures.append("Yahoo news search should still honor limit for short queries")
        if agent.exa_calls:
            failures.append("2-word queries should not redirect to Exa digest fallback")
    finally:
        yahoo_module.yf.Search = original_search
        await agent.cleanup()

    if failures:
        raise SystemExit("\n".join(failures))

    print("Yahoo news Exa fallback regression passed.")


if __name__ == "__main__":
    asyncio.run(main())
