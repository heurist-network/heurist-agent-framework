import asyncio

from agents.core_agent import CoreAgent

# from agents.core_agent import CoreAgent


async def main():
    # Initialize the core agent
    agent = CoreAgent()
    # UNCOMMENT TO INITIALIZE MCP TOOLS
    # server_url = "http://localhost:8000/sse"
    # await agent.initialize(server_url=server_url)

    print("Welcome to the Heurist Agent Console!")
    print("Type 'exit' to quit")
    print("-" * 50)

    while True:
        # Get user input
        user_message = input("\nYou: ").strip()

        if user_message.lower() == "exit":
            print("\nGoodbye!")
            break

        try:
            # Process the message using the core agent
            response = await agent.handle_message(
                message=user_message,
                source_interface="terminal",
                chat_id="console1",
                skip_conversation_context=False,
                skip_embedding=False,  # Skip embedding for simple console interaction
            )
            # response = await agent.deep_research(
            #     query=user_message,
            #     chat_id="console1",
            #     interactive=False,
            #     breadth=3,
            #     depth=2,
            #     concurrency=3,
            #     temperature=0.7,
            #     raw_data_only=False,
            # )
            # response = await agent.agent_cot(user_message, user="User", display_name="User 1", chat_id="console1")

            # Print the response
            print("\nAgent:", response)

        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
