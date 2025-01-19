import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.zkignite_yield_agent import ZkIgniteYieldAgent
import asyncio

agent = ZkIgniteYieldAgent()

async def test_zkignite_yield_agent():
    result = await agent.handle_message({})
    print(result)

asyncio.run(test_zkignite_yield_agent())