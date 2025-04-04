"""
Agent flow:
1. Monitor finds tweets
2. Tweets go into JSON file
3. Workers pull from queue
4. CoreAgent processes messages
5. Results automatically route back through send_message
6. Queue tracks completion
"""

import asyncio
import json
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import dotenv
import requests

import clients.twitter_api as twitter_api
from agents.base_agent import BaseAgent
from core.config import PromptConfig
from utils.llm_utils import should_ignore_message
from utils.text_utils import strip_tweet_text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dotenv.load_dotenv()

# Constants
HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")
SELF_TWITTER_NAME = os.getenv("SELF_TWITTER_NAME")
DRYRUN = os.getenv("DRYRUN")

RATE_LIMIT_SLEEP = 120
TAGGING_CHECK_INTERVAL = 1800

if DRYRUN:
    print("DRYRUN MODE: Not posting real tweets")
else:
    print("LIVE MODE: Will post real tweets")

prompt_config = PromptConfig()


class QueueManager:
    def __init__(self, file_path="reply_history.json"):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create file with initial structure if it doesn't exist"""
        if not self.file_path.exists():
            self.write_data({"processed_replies": [], "pending_replies": [], "processing_replies": {}})

    def read_data(self) -> Dict:
        """Read current data from file"""
        try:
            with self.file_path.open("r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading reply history: {str(e)}")
            return {"processed_replies": [], "pending_replies": []}

    def write_data(self, data: Dict):
        """Write data to file"""
        try:
            with self.file_path.open("w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing reply history: {str(e)}")

    def add_reply(self, reply_data: dict):
        """Add new reply to queue"""
        logger.debug(f"Adding new reply to queue: {reply_data['tweet_id']}")
        data = self.read_data()
        # Use tweet_id from the API response
        reply_data["message_id"] = reply_data["tweet_id"]  # Store tweet_id as message_id
        data["pending_replies"].append(reply_data)  # Append to maintain order
        self.write_data(data)

    def pop_pending_reply(self):
        """Get next pending reply and mark as processing"""
        data = self.read_data()

        # Find first pending reply that's not being processed
        for reply in data["pending_replies"]:
            tweet_id = reply["tweet_id"]
            if tweet_id not in data.get("processing_replies", {}):
                logger.debug(f"Found unprocessed reply {tweet_id}, marking as processing")
                data["processing_replies"][tweet_id] = {"data": reply, "started_at": datetime.now().isoformat()}
                self.write_data(data)

                return {"message_id": tweet_id, "data": json.dumps(reply)}

        logger.debug("No pending replies found")
        return None

    def mark_as_done(self, message_id, response_data: dict):
        """Move from processing to processed"""
        logger.debug(f"Marking reply {message_id} as done")
        data = self.read_data()

        # Remove from pending and processing
        data["pending_replies"] = [r for r in data["pending_replies"] if r["tweet_id"] != message_id]
        data["processing_replies"].pop(message_id, None)

        # Add to processed
        data["processed_replies"].append(response_data)
        self.write_data(data)

    def get_all_tweet_ids(self) -> set:
        """Get set of all tweet IDs from both pending and processed replies"""
        data = self.read_data()
        processed_ids = {reply["tweet_id"] for reply in data["processed_replies"]}
        pending_ids = {reply["tweet_id"] for reply in data["pending_replies"]}
        return processed_ids | pending_ids

    def get_pending_tweet_ids(self) -> set:
        """Get set of all tweet IDs from pending replies"""
        data = self.read_data()
        pending_ids = {reply["tweet_id"] for reply in data["pending_replies"]}
        return pending_ids

    def get_processed_tweet_ids(self) -> set:
        """Get set of all tweet IDs from processed replies"""
        data = self.read_data()
        processed_ids = {reply["tweet_id"] for reply in data["processed_replies"]}
        return processed_ids


class TwitterSearchMonitor:
    def __init__(self, api_key: str, queue_manager: QueueManager):
        self.api_key = api_key
        self.queue_manager = queue_manager
        self.base_url = "https://api.apidance.pro/sapi/Search"
        self.search_terms = []  # Initialize empty list

    def set_search_terms(self, terms: list):
        """Set the search terms to monitor"""
        self.search_terms = terms

    def fetch_tweets(self, cursor: str = "") -> Dict:
        """Fetch tweets matching configured search terms"""
        # Join terms with OR for the search query
        query = " OR ".join(self.search_terms)
        params = {"q": query, "cursor": cursor}
        headers = {"apikey": self.api_key}

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"tweets": [], "next_cursor_str": None}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {"tweets": [], "next_cursor_str": None}

    def filter_tweets(self, tweets: List[Dict]) -> List[Dict]:
        """Filter tweets based on criteria. Return the tweets that are selected for processing"""
        # Get all processed tweet IDs from queues
        processed_tweets = self.queue_manager.get_all_tweet_ids()

        filtered_tweets = []
        for tweet in tweets:
            if SELF_TWITTER_NAME == tweet["user"]["name"]:
                continue

            # Skip if tweet is from the author itself
            if tweet.get("is_self_send"):
                continue

            # Skip if we've already processed this tweet
            if tweet["tweet_id"] in processed_tweets:
                continue

            # Check if tweet contains any of the search terms
            if not any(term.lower() in tweet["text"].lower() for term in self.search_terms):
                continue

            # filter out nested replies that >= 3 replies deep
            # tweet['text'] looks like "@user1 @user2 @user3 contents..." we should count the number of @userX at the beginning of the string
            words = tweet["text"].split()
            at_count = 0
            for word in words:
                if word.startswith("@"):
                    at_count += 1
                else:
                    break
            if at_count >= 3:
                continue

            # strip the tweet text of URLs and @ mentions
            cleaned_text = strip_tweet_text(tweet["text"])
            if len(cleaned_text) < 10:
                continue

            # check if the tweet should be ignored
            if should_ignore_message(
                base_url=HEURIST_BASE_URL,
                api_key=HEURIST_API_KEY,
                model_id=SMALL_MODEL_ID,
                criteria=prompt_config.get_social_reply_filter(),
                message=cleaned_text,
                temperature=0.0,
            ):
                logger.info(f"Ignoring tweet {cleaned_text} because it matches the ignore criteria")
                continue

            filtered_tweets.append(tweet)

        return filtered_tweets

    def process_mentions(self) -> List[Dict]:
        """Main function to process mentions and queue new tweets"""
        logger.info("Fetching tweets...")

        cursor = ""
        api_calls = 0
        all_candidates = []

        while api_calls < 5:
            api_calls += 1
            response_data = self.fetch_tweets(cursor)

            if not response_data.get("tweets"):
                logger.info("No tweets found in response")
                break

            logger.debug(f"Fetched {len(response_data['tweets'])} tweets")
            logger.debug(f"Response data: {response_data}")

            candidate_tweets = self.filter_tweets(response_data["tweets"])

            # Queue new candidates
            for tweet in candidate_tweets:
                related_tweet_id = tweet.get("related_tweet_id", None)
                related_tweet = None
                if related_tweet_id:
                    related_tweet = twitter_api.get_tweet_text(related_tweet_id)
                self.queue_manager.add_reply(
                    {
                        "tweet_id": tweet["tweet_id"],
                        "content": tweet["text"],
                        "author_name": tweet["user"]["name"],
                        "related_tweet_id": related_tweet_id,
                        "related_tweet_text": related_tweet,
                    }
                )

            all_candidates.extend(candidate_tweets)

            # Stop if we found at least one candidate
            if candidate_tweets:
                break

            # Get next cursor for pagination
            cursor = response_data.get("next_cursor_str")
            if not cursor:
                logger.info("No more pages to fetch")
                break

            # sleep for 5 seconds to avoid rate limiting
            time.sleep(5)

        return all_candidates


class TwitterReplyAgent:
    def __init__(self, core_agent=None):
        # Type check if core_agent is provided
        if core_agent is not None and not isinstance(core_agent, BaseAgent):
            raise TypeError(f"core_agent must be an instance of BaseAgent, got {type(core_agent).__name__}")

        if core_agent:
            super().__setattr__("_parent", core_agent)
        else:
            super().__setattr__("_parent", self)
            super().__init__()

        self.queue_manager = QueueManager()
        self.monitor = TwitterSearchMonitor(
            api_key=os.getenv("TWITTER_SEARCH_API_KEY"), queue_manager=self.queue_manager
        )
        self.register_interface("twitter_reply", self)
        self.set_search_terms(["@heurist_ai"])  # Set default search term

    async def send_message(self, chat_id: str, message: str, image_url: str = None):
        """Interface method called by CoreAgent's send_to_interface. chat_id is the tweet_id"""
        logger.debug(f"send_message {chat_id} {message} {image_url}")
        if not DRYRUN:
            if image_url:
                twitter_api.reply_with_image(message, image_url, chat_id)
            else:
                twitter_api.reply(message, chat_id)
        else:
            print(f"DRYRUN MODE: Would have replied to {chat_id} with {message} and image {image_url}")
            return

    async def process_reply(self, message_data):
        """Process single reply using CoreAgent's handle_message"""
        logger.debug(f"Processing reply for tweet {message_data['tweet_id']}")
        try:
            social_reply_template = prompt_config.get_social_reply_template()
            context = None
            if message_data["related_tweet_text"]:
                context = "Related tweet: " + message_data["related_tweet_text"]
            message = social_reply_template.format(
                user_name=message_data["author_name"],
                social_platform="Twitter",
                user_message=message_data["content"],
                context=context,
            )
            response, image_url, _ = await self.handle_message(
                message=message,
                source_interface="twitter_reply",
                chat_id=message_data["tweet_id"],
                skip_embedding=True,
                skip_tools=True,
            )

            # send the response to the original tweet
            await self.send_message(message_data["tweet_id"], response, image_url)

            # CoreAgent will automatically call send_to_interface to other registered interfaces
            return response, image_url

        except Exception as e:
            logger.error(f"Error processing reply: {str(e)}")
            return None, None

    async def run_workers(self, num_workers: int = 3):
        """Run multiple reply workers"""

        async def worker():
            while True:
                try:
                    message = self.queue_manager.pop_pending_reply()
                    if not message:
                        await asyncio.sleep(RATE_LIMIT_SLEEP)
                        continue

                    reply_data = json.loads(message["data"])
                    response, image_url = await self.process_reply(reply_data)

                    response_data = reply_data.copy()
                    response_data["response"] = response
                    if image_url:
                        response_data["image_url"] = image_url

                    self.queue_manager.mark_as_done(message["message_id"], response_data)
                    await asyncio.sleep(RATE_LIMIT_SLEEP)

                except Exception as e:
                    logger.error(f"Worker error: {str(e)}")
                    await asyncio.sleep(RATE_LIMIT_SLEEP)

        workers = [worker() for _ in range(num_workers)]
        await asyncio.gather(*workers)

    def start_monitoring(self):
        """Start tag monitoring in background thread"""

        def process_new_tags():
            while True:
                self.monitor.process_mentions()  # this handles queueing
                time.sleep(TAGGING_CHECK_INTERVAL)

        monitor_thread = threading.Thread(target=process_new_tags, daemon=True)
        monitor_thread.start()
        return monitor_thread

    async def start(self):
        """Main entry point to start the agent"""
        self.start_monitoring()

        try:
            await self.run_workers()
        except KeyboardInterrupt:
            logger.info("Shutting down...")

    def set_search_terms(self, terms: list):
        """Configure which terms to monitor for"""
        self.monitor.set_search_terms(terms)
