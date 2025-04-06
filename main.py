import logging
import os
import threading

import dotenv

from agents.core_agent import CoreAgent
from interfaces.api import FlaskAgent
from interfaces.telegram import TelegramAgent
from interfaces.twitter_post import TwitterAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_flask(flask_agent):
    """Runs the (blocking) Flask API agent in a separate thread."""
    try:
        logger.info("Starting Flask API agent...")
        flask_agent.run(host="0.0.0.0", port=5005)
    except Exception as e:
        logger.error(f"Flask API agent error: {str(e)}")


def run_telegram(telegram_agent):
    """Run the Telegram agent"""
    try:
        logger.info("Starting Telegram agent...")
        telegram_agent.run()
    except Exception as e:
        logger.error(f"Telegram agent error: {str(e)}")


def run_twitter(twitter_agent):
    """Run the Twitter agent"""
    try:
        logger.info("Starting Twitter agent...")
        twitter_agent.run()
    except Exception as e:
        logger.error(f"Twitter agent error: {str(e)}")


def reload_environment():
    """Reload environment variables"""
    os.environ.clear()
    dotenv.load_dotenv(override=True)
    logger.info("Environment variables reloaded")


def main():
    """Main entry point"""
    try:
        # Initial load of environment variables
        reload_environment()

        # Create shared core agent and interfaces
        core_agent = CoreAgent()
        flask_agent = FlaskAgent(core_agent)
        telegram_agent = TelegramAgent(core_agent)
        twitter_agent = TwitterAgent(core_agent)
        # farcaster_agent = FarcasterAgent(core_agent)  # noqa: F841

        # Start Flask in a separate thread
        flask_thread = threading.Thread(target=run_flask, args=(flask_agent,), daemon=True)
        flask_thread.start()

        # Start Twitter in a separate thread
        twitter_thread = threading.Thread(target=run_twitter, args=(twitter_agent,), daemon=True)
        twitter_thread.start()

        # Run Telegram in the main thread
        run_telegram(telegram_agent)

        # Wait for other threads
        flask_thread.join()
        twitter_thread.join()

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
