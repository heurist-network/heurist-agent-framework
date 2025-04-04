import logging
import os

import discord
import dotenv
from discord.ext import commands

from agents.base_agent import BaseAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()


class DiscordAgent:
    def __init__(self, core_agent=None):
        # Type check if core_agent is provided
        if core_agent is not None and not isinstance(core_agent, BaseAgent):
            raise TypeError(f"core_agent must be an instance of BaseAgent, got {type(core_agent).__name__}")

        if core_agent:
            super().__setattr__("_parent", core_agent)
        else:
            # Need to set _parent = self first before super().__init__()
            super().__setattr__("_parent", self)  # Bypass normal __setattr__
            super().__init__()

        # Define intents to allow the bot to read message content
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.token = os.getenv("DISCORD_TOKEN")

        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.event
        async def on_ready():
            print(f"Logged in as {self.bot.user}")

        @self.bot.command()
        async def hello(ctx):
            await ctx.send("Hello! How can I help you?")

        @self.bot.event
        async def on_message(message):
            # Ignore bot's own messages
            if message.author == self.bot.user:
                return

            try:
                # Get user message
                user_message = message.content.lower()

                # Handle message using core agent functionality
                text_response, image_url, _ = await self.handle_message(user_message)

                if image_url:
                    embed = discord.Embed(title="Here you go!", color=discord.Color.blue())
                    embed.set_image(url=image_url)
                    await message.channel.send(embed=embed)
                elif text_response:
                    await message.channel.send(text_response)
                else:
                    await message.channel.send("Sorry, I couldn't process your message.")

            except Exception as e:
                logger.error(f"Message handling failed: {str(e)}")
                await message.channel.send("Sorry, I encountered an error processing your message.")

            # Ensure other commands still work
            await self.bot.process_commands(message)

        # Command: Simple echo function
        @self.bot.command()
        async def echo(ctx, *, message: str):
            await ctx.send(f"You said: {message}")

    def run(self):
        self.bot.run(self.token)
