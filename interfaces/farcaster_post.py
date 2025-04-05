import asyncio
import json
import logging
import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import dotenv
import requests

from agents.base_agent import BaseAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.clear()
dotenv.load_dotenv(override=True)
logger.info("Environment variables reloaded")

# Constants
HEURIST_BASE_URL = "https://llm-gateway.heurist.xyz/v1"
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
FARCASTER_API_KEY = os.getenv("FARCASTER_API_KEY")
FARCASTER_SIGNER_UUID = os.getenv("FARCASTER_SIGNER_UUID")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")
CAST_WORD_LIMITS = [15, 20, 30, 35]
IMAGE_GENERATION_PROBABILITY = 1
CAST_HISTORY_FILE = "cast_history.json"

# DRYRUN = False if os.getenv("DRYRUN") == "False" else True
DRYRUN = False
if DRYRUN:
    print("DRYRUN MODE: Not posting real casts")
else:
    print("LIVE MODE: Will post real casts")


class FarcasterAPI:
    def __init__(self, api_key: str, signer_uuid: str):
        self.api_key = api_key
        self.signer_uuid = signer_uuid
        self.base_url = "https://api.neynar.com/v2/farcaster"
        self.headers = {"api_key": self.api_key, "Content-Type": "application/json"}

    def post_cast(self, message: str, image_url: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """Post a cast to Farcaster, optionally with an image"""
        try:
            endpoint = f"{self.base_url}/cast"

            data = {
                "signer_uuid": self.signer_uuid,
                "text": message,
            }

            if image_url:
                data["embeds"] = [{"url": image_url}]

            response = requests.post(endpoint, headers=self.headers, json=data)

            if response.status_code == 200:
                result = response.json()
                cast_hash = result.get("cast", {}).get("hash")
                username = result.get("cast", {}).get("author", {}).get("username")
                logger.info(f"Successfully posted cast with hash: {cast_hash}")
                return cast_hash, username
            else:
                logger.error(f"Failed to post cast. Status: {response.status_code}, Response: {response.text}")
                return None, None

        except Exception as e:
            logger.error(f"Error posting cast: {str(e)}")
            return None, None


class CastHistoryManager:
    def __init__(self, history_file: str = CAST_HISTORY_FILE):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self) -> list:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Error reading {self.history_file}, starting fresh")
                return []
        return []

    def add_cast(self, cast: str, metadata: Optional[Dict] = None) -> None:
        entry = {"timestamp": datetime.now().isoformat(), "cast": cast}
        if metadata:
            entry.update(metadata)

        entry = json.loads(json.dumps(entry, ensure_ascii=False))
        self.history.append(entry)
        self.save_history()

    def save_history(self) -> None:
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_recent_casts(self, n: int = 6) -> list:
        return [entry["cast"]["cast"] for entry in self.history[-n:]]


class FarcasterAgent:
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

        # Initialize Farcaster specific components
        self.history_manager = CastHistoryManager()
        self.farcaster_api = FarcasterAPI(FARCASTER_API_KEY, FARCASTER_SIGNER_UUID)
        self.register_interface("farcaster", self)
        self.last_cast_hash = None

    def __getattr__(self, name):
        return getattr(self._parent, name)

    def __setattr__(self, name, value):
        if not hasattr(self, "_parent"):
            super().__setattr__(name, value)
        elif name == "_parent" or self is self._parent or name in self.__dict__:
            super().__setattr__(name, value)
        else:
            setattr(self._parent, name, value)

    def fill_basic_prompt(self, basic_options, style_options):
        return self.prompt_config.get_basic_prompt_template().format(
            basic_option_1=basic_options[0],
            basic_option_2=basic_options[1],
            style_option_1=style_options[0],
            style_option_2=style_options[1],
        )

    def format_cast_instruction(self, basic_options, style_options, ideas=None):
        decoration_ideas = f"Ideas: {ideas}" if ideas else "\n"
        num_words = random.choice(CAST_WORD_LIMITS)

        return self.prompt_config.get_tweet_instruction_template().format(
            basic_option_1=basic_options[0],
            basic_option_2=basic_options[1],
            style_option_1=style_options[0],
            style_option_2=style_options[1],
            decoration_ideas=decoration_ideas,
            num_words=num_words,
            rules=self.prompt_config.get_farcaster_rules(),
        )

    def format_context(self, casts):
        """Format the context template with past casts.

        Args:
            casts: List of previous casts

        Returns:
            Formatted context string
        """
        if casts is None:
            casts = []

        # Convert list of casts to a formatted string
        cast_text = "\n".join([f"- {cast}" for cast in casts]) if casts else ""

        return self.prompt_config.get_context_farcaster_template().format(
            casts=cast_text
        )  # Changed 'tweets' to 'casts'

    async def generate_cast(self) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Generate a cast with improved error handling"""
        cast_data: Dict[str, Any] = {"metadata": {}}

        try:
            # Get recent casts for context
            past_casts = self.history_manager.get_recent_casts()

            # Generate randomized prompt
            basic_options = random.sample(self.prompt_config.get_basic_settings(), 2)
            style_options = random.sample(self.prompt_config.get_interaction_styles(), 2)
            cast_data["metadata"].update({"basic_options": basic_options, "style_options": style_options})

            prompt = self.fill_basic_prompt(basic_options, style_options)

            # Generate ideas using get_tweet_ideas() since cast-specific method doesn't exist yet
            instruction_cast_idea = random.choice(self.prompt_config.get_tweet_ideas())
            system_prompt = prompt + self.prompt_config.get_farcaster_rules() + self.format_context(past_casts)

            cast_data["metadata"]["ideas_instruction"] = instruction_cast_idea
            ideas_text, _, _ = await self.handle_message(
                instruction_cast_idea, system_prompt_fixed=system_prompt, source_interface="farcaster"
            )
            cast_data["metadata"]["ideas"] = ideas_text

            if not ideas_text:
                return None, None, None

            # Generate final cast
            system_prompt = (
                prompt
                + self.prompt_config.get_farcaster_rules()
                + self.format_context(past_casts)
                + self.format_cast_instruction(basic_options, style_options, ideas_text)
            )

            cast, _, _ = await self.handle_message(
                ideas_text, system_prompt_fixed=system_prompt, source_interface="farcaster"
            )

            if not cast:
                return None, None, None

            cast = cast.replace('"', "")
            cast_data["cast"] = cast

            # Image generation
            image_url = None
            if random.random() < IMAGE_GENERATION_PROBABILITY:
                try:
                    image_prompt = await self.generate_image_prompt(cast)
                    image_url = await self.handle_image_generation(image_prompt)
                    cast_data["metadata"]["image_prompt"] = image_prompt
                    cast_data["metadata"]["image_url"] = image_url
                except Exception as e:
                    logger.warning(f"Failed to generate image: {str(e)}")

            return cast, image_url, cast_data

        except Exception as e:
            logger.error(f"Unexpected error in cast generation: {str(e)}")
            return None, None, None

    async def _run(self):
        while True:
            try:
                cast_result = await self.generate_cast()
                logger.info("Cast result: %s", cast_result)

                cast, image_url, cast_data = cast_result

                if cast:
                    if not DRYRUN:
                        if image_url:
                            cast_hash, username = self.farcaster_api.post_cast(cast, image_url)
                            logger.info("Successfully posted cast with image: %s", cast)
                            cast_url = f"https://warpcast.com/{username}/0x{cast_hash}"
                        else:
                            cast_hash, username = self.farcaster_api.post_cast(cast)
                            logger.info("Successfully posted cast: %s", cast)
                            cast_url = f"https://warpcast.com/{username}/0x{cast_hash}"

                        if cast_hash:
                            cast_data["metadata"]["cast_hash"] = cast_hash
                            cast_data["metadata"]["cast_url"] = cast_url
                            self.last_cast_hash = cast_hash

                            # Notify other interfaces
                            for interface_name, interface in self.interfaces.items():
                                if interface_name == "telegram":
                                    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
                                    if telegram_chat_id:
                                        await self.send_to_interface(
                                            interface_name,
                                            {
                                                "type": "message",
                                                "content": f"Just posted a cast: {cast_url}",
                                                "image_url": None,
                                                "source": "farcaster",
                                                "chat_id": telegram_chat_id,
                                            },
                                        )
                    else:
                        logger.info("Generated cast: %s", cast)

                    self.history_manager.add_cast(cast_data)
                    wait_time = random_interval()
                else:
                    logger.error("Failed to generate cast")
                    wait_time = 10

                next_time = datetime.now() + timedelta(seconds=wait_time)
                logger.info("Next cast will be posted at: %s", next_time.strftime("%H:%M:%S"))
                await asyncio.sleep(wait_time)

            except Exception as e:
                logger.error("Error occurred: %s", str(e))
                await asyncio.sleep(10)
                continue

    def run(self):
        """Start the Farcaster bot"""
        logger.info("Starting Farcaster bot...")
        asyncio.run(self._run())


def random_interval():
    """Generate a random interval between 1 and 2 hours in seconds"""
    return random.uniform(3600, 7200)


def main():
    agent = FarcasterAgent()
    agent.run()


if __name__ == "__main__":
    try:
        logger.info("Starting Farcaster agent...")
        main()
    except KeyboardInterrupt:
        logger.info("\nFarcaster agent stopped by user")
    except Exception as e:
        logger.error("Fatal error: %s", str(e))
