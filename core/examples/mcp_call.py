import asyncio

from heurist_core.components import LLMProvider
from heurist_core.tools.tools_mcp import Tools

tools = Tools()
llm_provider = LLMProvider(tool_manager=tools)
server_url = "https://localhost:8000/sse"


async def main():
    await tools.initialize(server_url=server_url)
    result = await llm_provider.call(system_prompt="You are a helpful assistant.", user_prompt="Hello, how are you?")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
