import logging

import dotenv

from agents.core_agent_refactor import CoreAgent
from interfaces.twitter_post import TwitterAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for the Heuman Agent Framework.
    Runs the Twitter agent for automated tweeting.
    """
    try:
        # Load environment variables
        dotenv.load_dotenv()

        # Initialize and run Twitter agent
        logger.info("Starting Twitter agent...")
        core_agent = CoreAgent()
        agent = TwitterAgent(core_agent)
        agent.run()

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
