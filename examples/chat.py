import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List

import aiohttp
from dotenv import load_dotenv
from openai import AsyncOpenAI
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

logging.getLogger("httpx").setLevel(logging.WARNING)

load_dotenv()

BANNER = """
╔══════════════════════════════════════════╗
║      CHAT WITH HEURIST MESH AGENTS       ║
╚══════════════════════════════════════════╝
"""

AGENT_NAME = "Bitquery Solana Token Info Agent"
AGENT_DESCRIPTION = "This agent fetches Solana token trading information and trending tokens from Bitquery"
ADDITIONAL_INSTRUCTIONS = "You are a crypto expert. You should give accurate, up-to-date information based on the context you have. Don't make up information. If you don't have the information, just say so. Don't sound like a robot. You should talk like a crypto native bro who is deep in the trenches."
# API_URL = "http://localhost:8000/mesh_request"
API_URL = f"{os.getenv('MESH_SERVER_URL', 'https://mesh.heurist.xyz')}/mesh_request"

console = Console()


class ChatSession:
    def __init__(self):
        self.messages: List[Dict] = []
        self.context_data: List[Dict] = []
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")
        self.greeted = False

    def get_system_prompt(self) -> str:
        prompt = f"You are {AGENT_NAME}. {AGENT_DESCRIPTION}."
        if self.context_data:
            prompt += "\n\nUse these data and context information if applicable:\n"
            for entry in self.context_data:
                prompt += f"\n[{entry['timestamp']}] {json.dumps(entry['data'], indent=2)}"
        return prompt

    async def call_agent(self, query: str) -> Dict:
        console.print("[dim]Calling agent API...[/dim]")
        payload = {
            "agent_id": "BitquerySolanaTokenInfoAgent",
            "input": {"query": query, "raw_data_only": True},
            "api_key": os.getenv("HEURIST_API_KEY"),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload) as response:
                result = await response.json()
                return result

    async def stream_llm_response(self, messages: List[Dict]) -> str:
        stream = await self.openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=True)

        collected_response = ""
        with Live(Text(""), refresh_per_second=10) as live:
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    collected_response += content
                    live.update(Text(collected_response))

        return collected_response

    async def greet_user(self):
        greeting_prompt = {
            "role": "system",
            "content": f"""You are {AGENT_NAME}. Create a short, fun, and engaging greeting message (2 sentences max).
            Be creative and talk like a crypto native bro who's deep in the trenches.
            Your skills: {AGENT_DESCRIPTION}
            Don't mention being an AI or assistant. Don't use emojis. Just jump right into the dialogue.""",
        }
        console.print("\n[bold green]AI:[/bold green]")
        greeting = await self.stream_llm_response([greeting_prompt])
        self.messages = [{"role": "system", "content": self.get_system_prompt()}]
        return greeting

    async def chat(self, user_input: str):
        # Send greeting if first message
        if not self.greeted:
            await self.greet_user()
            self.greeted = True

        # Initialize messages with system prompt if empty
        if not self.messages:
            self.messages = [{"role": "system", "content": self.get_system_prompt()}]

        # Add user message with styling
        console.print("\n[bold blue]You:[/bold blue]", user_input)
        self.messages.append({"role": "user", "content": user_input})

        # Call agent API
        agent_response = await self.call_agent(user_input)

        # If agent returned data, update context
        if agent_response.get("data"):
            console.print("[dim]Updating context with new data...[/dim]")
            self.context_data.append({"timestamp": datetime.now().isoformat(), "data": agent_response["data"]})
            # Update system message with new context
            self.messages[0] = {"role": "system", "content": self.get_system_prompt()}

        # Stream LLM response
        console.print("\n[bold green]AI:[/bold green]")
        llm_response = await self.stream_llm_response(self.messages)

        # Add assistant response to message history
        self.messages.append({"role": "assistant", "content": llm_response})


def print_welcome_message():
    console.print(Panel.fit(Text(BANNER, style="bold magenta"), title="Welcome", border_style="bright_blue"))
    console.print(
        Panel.fit(
            f"[bold]Agent:[/bold] {AGENT_NAME}\n[bold]Description:[/bold] {AGENT_DESCRIPTION}",
            title="Agent Info",
            border_style="green",
        )
    )
    console.print("\nType [bold red]'exit'[/bold red] to quit\n")


async def main():
    print_welcome_message()
    session = ChatSession()
    await session.greet_user()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                console.print("\n[bold yellow]Goodbye! Thanks for chatting![/bold yellow]")
                break

            if not user_input:
                continue

            await session.chat(user_input)

        except Exception as e:
            console.print(f"\n[bold red]ERROR:[/bold red] {str(e)}")
            console.print_exception()


if __name__ == "__main__":
    asyncio.run(main())
