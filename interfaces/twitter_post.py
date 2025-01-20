import json
import logging
import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any
import dotenv
import yaml
from agents.core_agent import CoreAgent
from platforms.twitter_api import tweet_with_image, tweet_text_only
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.clear()
dotenv.load_dotenv(override=True)
logger.info("Environment variables reloaded")

# Constants
TWEET_WORD_LIMITS = [30, 50, 100, 200]
IMAGE_GENERATION_PROBABILITY = 0.75
TWEET_HISTORY_FILE = "tweet_history.json"

DRYRUN = False if os.getenv("DRYRUN") == "False" else True

if DRYRUN:
    print(DRYRUN)
    print("DRYRUN MODE: Not posting real tweets")
else:
    print("LIVE MODE: Will post real tweets")

class TweetHistoryManager:
    def __init__(self, history_file=TWEET_HISTORY_FILE):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Error reading {self.history_file}, starting fresh")
                return []
        return []

    def add_tweet(self, tweet, metadata=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'tweet': tweet
        }
        if metadata:
            entry.update(metadata)
        
        entry = json.loads(json.dumps(entry, ensure_ascii=False))
        self.history.append(entry)
        self.save_history()

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def get_recent_tweets(self, n=6):
        return [entry['tweet']['tweet'] for entry in self.history[-n:]]

class TwitterAgent(CoreAgent):
    def __init__(self, core_agent=None):
        if core_agent:
            super().__setattr__('_parent', core_agent)
        else:
            super().__setattr__('_parent', self)
            super().__init__()
        
        # Initialize twitter specific stuff
        self.history_manager = TweetHistoryManager()
        self.register_interface('twitter', self)

    def __getattr__(self, name):
        return getattr(self._parent, name)
        
    def __setattr__(self, name, value):
        if not hasattr(self, '_parent'):
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
            style_option_2=style_options[1]
        )

    def format_tweet_instruction(self, basic_options, style_options, ideas=None):
        decoration_ideas = f"Ideas: {ideas}" if ideas else "\n"
        num_words = random.choice(TWEET_WORD_LIMITS)
        
        return self.prompt_config.get_tweet_instruction_template().format(
            basic_option_1=basic_options[0],
            basic_option_2=basic_options[1],
            style_option_1=style_options[0],
            style_option_2=style_options[1],
            decoration_ideas=decoration_ideas,
            num_words=num_words,
            rules=self.prompt_config.get_twitter_rules()
        )

    def format_context(self, tweets):
        if tweets is None:
            tweets = []
        return self.prompt_config.get_context_twitter_template().format(tweets=tweets)
    
    async def generate_tweet(self) -> tuple[str | None, str | None, dict | None]:
        """Generate a tweet with improved error handling"""
        tweet_data: Dict[str, Any] = {'metadata': {}}
        
        try:
            # Get recent tweets for context
            past_tweets = self.history_manager.get_recent_tweets()
            generate_image = random.random() < IMAGE_GENERATION_PROBABILITY
            image_instructions = ""
            if generate_image:
                image_instructions = "Generate an image for the post, create a prompt for the image generation model."
            # Generate randomized prompt
            basic_options = random.sample(self.prompt_config.get_basic_settings(), 2)
            style_options = random.sample(self.prompt_config.get_interaction_styles(), 2)
            instruction_tweet_idea = random.choice(self.prompt_config.get_tweet_ideas())
            tweet_instruction = (self.format_tweet_instruction(basic_options, style_options, "<Your Ideas from previoues steps>"))

            tweet_prompt = F"""
                You are going to generate a tweet post for a social media platform.
                Think of the following and generate new ideas:
                {instruction_tweet_idea}
                Then use the ideas from from the previous steps to generate a tweet, considering the following rules:
                {tweet_instruction}
                Once you have a final tweet, making sure you check the rules and make sure it is not too long or too short.
                {image_instructions}
                Then generate the image and final tweet.
                MAKE SURE THE FINAL TWEET IS LESS THAN 250 CHARACTERS.
                IMPORTANT: ADD A FINAL STEP TO MAKE SURE THE TWEET IS LESS THAN 250 CHARACTERS.
            """
            tweet_system_prompt = F"""
                Consider the following rules:
                {self.prompt_config.get_twitter_rules()}
                Consider the following style and basic options:
                {self.fill_basic_prompt(basic_options, style_options)}
                Consider your previous tweets:
                {past_tweets}
            """

            tweet, image_url, _ = await self.agent_cot(
                tweet_prompt, 
                user="agent", 
                display_name="agent", 
                chat_id="twitter_post", 
                source_interface="twitter", 
                final_format_prompt=tweet_system_prompt,
            )
            
            print("Tweet: ", tweet)
            tweet = tweet.replace('"', '')
            tweet_data['tweet'] = tweet
            tweet_data['metadata'].update({
                'basic_options': basic_options,
                'style_options': style_options
            })
            tweet_data['metadata']['ideas_instruction'] = instruction_tweet_idea
            tweet_data['metadata']['ideas'] = instruction_tweet_idea
            if image_url:
                tweet_data['metadata']['image_prompt'] = ""
                tweet_data['metadata']['image_url'] = image_url

            if tweet == "Sorry, I encountered an error processing your message.":
                raise Exception("Error generating tweet")
            
            return tweet, image_url, tweet_data

        except Exception as e:
            logger.error(f"Unexpected error in tweet generation: {str(e)}")
            return None, None, None

    def run(self):
        """Start the Twitter bot"""
        logger.info("Starting Twitter bot...")
        asyncio.run(self._run())

    async def _run(self):
        while True:
            try:
                # Generate tweet returns (tweet, image_url, tweet_data)
                tweet_result = await self.generate_tweet()
                logger.info("Tweet result: %s", tweet_result)
                
                # Unpack all three values
                tweet, image_url, tweet_data = tweet_result
                
                if tweet:
                    if not DRYRUN:
                        token_id = None
                        if image_url:
                            tweet_id, username = tweet_with_image(tweet, image_url)
                            logger.info("Successfully posted tweet with image: %s", tweet)
                            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
                        else:
                            tweet_id, username = tweet_text_only(tweet)
                            logger.info("Successfully posted tweet: %s", tweet)
                        
                        tweet_data['metadata']['tweet_id'] = tweet_id
                        tweet_data['metadata']['tweet_url'] = f"https://x.com/{username}/status/{tweet_id}"
                        self.last_tweet_id = tweet_id
                        
                        # Notify Telegram channel if configured
                        for interface_name, interface in self.interfaces.items():
                            if interface_name == 'telegram':
                                telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", None) 
                                if telegram_chat_id:
                                    await self.send_to_interface(interface_name, {
                                        'type': 'message',
                                        'content': "Just posted a tweet: " + tweet_data['metadata']['tweet_url'],
                                        'image_url': None,
                                        'source': 'twitter',
                                        'chat_id': telegram_chat_id
                                    })
                    else:
                        logger.info("Generated tweet: %s", tweet)
                    
                    self.history_manager.add_tweet(tweet_data)
                    wait_time = random_interval()
                else:
                    logger.error("Failed to generate tweet")
                    wait_time = 10
                
                next_time = datetime.now() + timedelta(seconds=wait_time)
                logger.info("Next tweet will be posted at: %s", next_time.strftime('%H:%M:%S'))
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                logger.error("Error occurred: %s", str(e))
                await asyncio.sleep(10)
                continue

def random_interval():
    """Generate a random interval between 1 and 2 hours in seconds"""
    return random.uniform(60*60*0.5, 60*60*1.5)

def main():
    agent = TwitterAgent()
    agent.run()

if __name__ == "__main__":
    try:
        logger.info("Starting Twitter agent...")
        main()
    except KeyboardInterrupt:
        logger.info("\nTwitter agent stopped by user")
    except Exception as e:
        logger.error("Fatal error: %s", str(e))