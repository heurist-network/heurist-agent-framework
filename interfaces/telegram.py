import logging
import os
from pathlib import Path

import dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from agents.base_agent import BaseAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ.clear()
dotenv.load_dotenv()

# Constants
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if not TELEGRAM_API_TOKEN:
    raise ValueError("TELEGRAM_API_TOKEN not found in environment variables")


class TelegramAgent:
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

        # Initialize telegram specific stuff
        self.app = Application.builder().token(TELEGRAM_API_TOKEN).build()
        self._setup_handlers()
        self.register_interface("telegram", self)

    def __getattr__(self, name):
        # Delegate to the parent instance for missing attributes/methods
        return getattr(self._parent, name)

    def __setattr__(self, name, value):
        if not hasattr(self, "_parent"):
            # During initialization, before _parent is set
            super().__setattr__(name, value)
        elif name == "_parent" or self is self._parent or name in self.__dict__:
            # Set local attributes (like _parent or already existing attributes)
            super().__setattr__(name, value)
        else:
            # Delegate attribute setting to the parent instance
            setattr(self._parent, name, value)

    def _setup_handlers(self):
        # Register the /start command handler
        self.app.add_handler(CommandHandler("start", self.start))
        # Register the /image command handler
        self.app.add_handler(CommandHandler("image", self.image))
        # Register a handler for voice messages
        self.app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        # Register a handler for echoing messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message))
        # Register a handler for getting the chat id
        self.app.add_handler(CommandHandler("get_id", self.get_id))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello World! I'm not a bot... I promise... ")

    async def get_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        await update.message.reply_text(f"Your Chat ID is: {chat_id}")

    async def image(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Get the text after the /image command
        prompt = " ".join(context.args) if context.args else None

        if not prompt:
            await update.message.reply_text("Please provide a prompt after /image command")
            return

        # Generate image using the prompt
        try:
            result = await self.handle_image_generation(prompt=prompt)
            if result:
                # Send the generated image as a photo using the URL
                await update.message.reply_photo(photo=result)
                await update.message.reply_text("Image generated successfully.")
            else:
                await update.message.reply_text("Failed to generate image")
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            await update.message.reply_text("Sorry, there was an error generating the image")

    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        COT = False
        user = update.effective_user
        username = user.username or "Unknown"
        display_name = user.full_name or username
        message_data = update.message.text
        chat_id = update.message.chat_id
        if not COT:
            text_response, image_url, _ = await self.handle_message(update.message.text, source_interface="telegram")
        else:
            text_response, image_url, _ = await self.agent_cot(
                message_data, user=username, display_name=display_name, chat_id=chat_id, source_interface="telegram"
            )
        logger.info(f"Telegram message: {update.message.text}")
        if self._parent != self:
            logger.info("Operating in shared mode with core agent")
        else:
            logger.info("Operating in standalone mode")

        if image_url:
            await update.message.reply_photo(photo=image_url)
        elif text_response:
            await update.message.reply_text(text_response)

    async def send_message(self, chat_id: int, message: str, image_url: str = None) -> None:
        """
        Send a message to a specific chat ID after validating the bot's membership.

        Args:
            chat_id (int): The Telegram chat ID to send the message to
            message (str): The message text to send

        Raises:
            TelegramError: If bot is not a member of the chat or other Telegram API errors
        """
        try:
            logger.info("Send message to telegram")
            logger.info(f"Sending message to chat {chat_id}")
            logger.info(f"Message: {message}")
            # Try to get chat member status of the bot in the target chat
            bot_member = await self.app.bot.get_chat_member(chat_id=chat_id, user_id=self.app.bot.id)

            # Check if bot is a member/admin in the chat
            if bot_member.status not in ["member", "administrator"]:
                logger.error(f"Bot is not a member of chat {chat_id}")
                return

            if image_url:
                await self.app.bot.send_photo(chat_id=chat_id, photo=image_url, caption="")
            else:
                message = message.replace('"', "")
                await self.app.bot.send_message(chat_id=chat_id, text=message)

        except Exception as e:
            logger.error(f"Failed to send message to chat {chat_id}: {str(e)}")
            raise

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.voice:
            # Get the file ID of the voice note
            file_id = update.message.voice.file_id

            # Get the file from Telegram's servers
            file = await context.bot.get_file(file_id)

            project_root = Path(__file__).parent.parent
            audio_dir = project_root / "audio"
            audio_dir.mkdir(exist_ok=True)

            # Define the file path where the audio will be saved
            file_path = audio_dir / f"{file_id}.ogg"

            # Download the file
            await file.download_to_drive(file_path)

            # Notify the user
            await update.message.reply_text("Voice note received. Processing...")
            user_message = await self.transcribe_audio(file_path)
            text_response, image_url, _ = await self.handle_message(user_message)

            if image_url:
                await update.message.reply_photo(photo=image_url)
            elif text_response:
                await update.message.reply_text(text_response.replace('"', ""))

    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram bot...")
        self.app.run_polling()


def main():
    agent = TelegramAgent()
    agent.run()


if __name__ == "__main__":
    try:
        logger.info("Starting Telegram agent...")
        main()
    except KeyboardInterrupt:
        logger.info("\nTelegram agent stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
