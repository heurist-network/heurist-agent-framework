import asyncio
import os

from heurist_core.clients.search_client import SearchClient
from heurist_core.components import ConversationManager, KnowledgeProvider, LLMProvider
from heurist_core.embedding import MessageStore, SQLiteConfig, SQLiteVectorStorage
from heurist_core.tools.tools_mcp import Tools
from heurist_core.workflows import AugmentedLLMCall, ChainOfThoughtReasoning, ResearchWorkflow

print("Successfully imported heurist_core modules!")
search_client = SearchClient(client_type="firecrawl", api_key=os.getenv("FIRECRAWL_KEY"), rate_limit=1)
# SETUP STORAGE FOR AUGMENTED LLM
config = SQLiteConfig()
storage = SQLiteVectorStorage(config)
message_store = MessageStore(storage)

# Initialize managers
tools = Tools()
knowledge_provider = KnowledgeProvider(message_store)
conversation_manager = ConversationManager(message_store)

llm_provider = LLMProvider(tool_manager=tools)

# Initialize reasoning patterns
augmented_llm = AugmentedLLMCall(knowledge_provider, conversation_manager, tools, llm_provider)
chain_of_thought = ChainOfThoughtReasoning(llm_provider, tools, augmented_llm)
research_workflow = ResearchWorkflow(llm_provider, tools, search_client)

server_url = "https://localhost:8000/sse"


async def main():
    # Initialize tools if using MCP
    await tools.initialize(server_url=server_url)

    result = await llm_provider.call(system_prompt="You are a helpful assistant.", user_prompt="Hello, how are you?")
    print(result)
    # result = await augmented_llm.process(system_prompt="You are a helpful assistant.", message="what are the trending tokens?")
    # print(result)
    # result = await chain_of_thought.process(system_prompt="You are a helpful assistant.", message="what are the trending tokens?")
    # print(result)
    result = await research_workflow.process(message="latest bitcoin news?")
    print(result)


# Run the async main function
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    finally:
        # Explicitly clean up tools before closing the loop
        if hasattr(tools, "cleanup") and callable(tools.cleanup):
            loop.run_until_complete(tools.cleanup())

        # Close all pending tasks
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()

        # Run the event loop once more to ensure all tasks are properly canceled
        if pending:
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))

        loop.close()
