import asyncio

import yaml

from mesh.agents.momus_prediction_market_agent import MomusPredictionMarketAgent


async def test_agent():
    agent = MomusPredictionMarketAgent()
    try:
        # Natural language
        print(yaml.dump(await agent.call_agent({"query": "What are the odds for Real Madrid vs Barcelona?"})))
        # Direct tool calls
        print(yaml.dump(await agent.call_agent({"tool": "football_quote", "tool_arguments": {"home_team": "Arsenal", "away_team": "Liverpool"}})))
        print(yaml.dump(await agent.call_agent({"tool": "midterms_odds", "tool_arguments": {}})))
        print(yaml.dump(await agent.call_agent({"tool": "tennis_read", "tool_arguments": {}})))
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(test_agent())
