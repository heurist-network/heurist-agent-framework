import asyncio
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.yahoo_finance_agent import YahooFinanceAgent


def _preview(payload, limit=600):
    return json.dumps(payload, ensure_ascii=True)[:limit]


async def main():
    agent = YahooFinanceAgent()
    failures = []

    try:
        futures_batch = await agent.futures_snapshot(symbols=["CL=F", "GC=F"], include_history=False)
        print("futures_snapshot list batch:", _preview(futures_batch))
        batch_results = (futures_batch.get("data") or {}).get("results") or []
        if futures_batch.get("status") != "success" or [item.get("symbol") for item in batch_results] != ["CL=F", "GC=F"]:
            failures.append("futures_snapshot should continue to support true list batching")

        futures_csv = await agent.futures_snapshot(symbols="CL=F,GC=F", include_history=False)
        print("futures_snapshot csv string:", _preview(futures_csv))
        csv_results = (futures_csv.get("data") or {}).get("results") or []
        if futures_csv.get("status") != "success" or [item.get("symbol") for item in csv_results] != ["CL=F", "GC=F"]:
            failures.append("futures_snapshot should coerce comma-separated symbols into a list")

        quote_csv = await agent.quote_snapshot("AAPL,MSFT")
        print("quote_snapshot csv string:", _preview(quote_csv))
        quote_results = (quote_csv.get("data") or {}).get("results") or []
        if quote_csv.get("status") != "success" or [item.get("symbol") for item in quote_results] != ["AAPL", "MSFT"]:
            failures.append("quote_snapshot should coerce comma-separated symbols into a list")

        expirations = await agent.options_expirations(symbol="AAPL", limit="3", min_days_to_expiration="0")
        print("options_expirations string limit:", _preview(expirations))
        expiration_data = expirations.get("data") or {}
        expiration_items = expiration_data.get("expirations") or []
        if expirations.get("status") != "success" or expiration_data.get("filters", {}).get("limit") != 3:
            failures.append("options_expirations should coerce string limit values")
        if len(expiration_items) > 3:
            failures.append("options_expirations should honor the coerced string limit")
        if not expiration_items:
            failures.append("options_expirations should return at least one expiration for AAPL")

        selected_expiration = expiration_items[0]["expiration"]
        chain = await agent.options_chain(symbol="AAPL", expiration=selected_expiration, limit_contracts="3")
        print("options_chain string limit_contracts:", _preview(chain))
        chain_data = chain.get("data") or {}
        calls = chain_data.get("calls") or []
        puts = chain_data.get("puts") or []
        if chain.get("status") != "success" or chain_data.get("filters", {}).get("limit_contracts") != 3:
            failures.append("options_chain should coerce string limit_contracts values")
        if len(calls) > 3 or len(puts) > 3:
            failures.append("options_chain should honor the coerced string limit_contracts")

        news = await agent.news_search(query="US Iran war defense energy oil stocks 2026", limit="3")
        print("news_search string limit:", _preview(news))
        if news.get("status") == "error" and "'<' not supported" in str(news.get("error")):
            failures.append("news_search should coerce string limit values before range clamping")

        simple_news = await agent.news_search(query="TSLA", limit="3")
        print("news_search simple string limit:", _preview(simple_news))
        simple_news_data = simple_news.get("data") or {}
        simple_news_items = simple_news_data.get("items") or []
        if simple_news.get("status") != "success":
            failures.append("news_search should still return success for a normal query with string limit values")
        if len(simple_news_items) > 3:
            failures.append("news_search should honor the coerced string limit")
    finally:
        await agent.cleanup()

    if failures:
        raise SystemExit("\n".join(failures))

    print("\nAll Yahoo options/futures regressions passed.")


if __name__ == "__main__":
    asyncio.run(main())
