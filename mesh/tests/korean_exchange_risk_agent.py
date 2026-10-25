import asyncio
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.korean_exchange_risk_agent import KoreanExchangeRiskAgent  # noqa: E402


async def run_agent():
    agent = KoreanExchangeRiskAgent()
    try:
        results = {}
        results["recent_warnings_and_delistings"] = await agent.call_agent(
            {"tool": "get_korean_exchange_events", "tool_arguments": {"event_types": ["WARNING_SET", "DELISTING"], "limit": 5}}
        )
        results["bithumb_suspensions"] = await agent.call_agent(
            {
                "tool": "get_korean_exchange_events",
                "tool_arguments": {"exchange": "bithumb", "event_types": ["DEPOSIT_SUSPENDED", "WITHDRAWAL_SUSPENDED"], "limit": 5},
            }
        )
        results["coin_status_icx"] = await agent.call_agent(
            {"tool": "get_korean_exchange_coin_status", "tool_arguments": {"symbol": "ICX"}}
        )
        results["natural_language"] = await agent.call_agent(
            {"query": "Which coins did Upbit or Bithumb flag with a trading warning recently?"}
        )
        out = Path(__file__).with_name("korean_exchange_risk_agent_example.yaml")
        out.write_text(yaml.dump(results, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"Results saved to {out}")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
