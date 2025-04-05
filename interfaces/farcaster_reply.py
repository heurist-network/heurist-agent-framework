import asyncio
import base64
import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen

import dotenv
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from agents.base_agent import BaseAgent
from core.config import PromptConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

# Constants
HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")
FARCASTER_API_KEY = os.getenv("FARCASTER_API_KEY")
FARCASTER_SIGNER_UUID = os.getenv("FARCASTER_SIGNER_UUID")
FARCASTER_FID = int(os.getenv("FARCASTER_FID"))
DRYRUN = os.getenv("DRYRUN", False)

RATE_LIMIT_SLEEP = 5
REPLY_CHECK_INTERVAL = 10
IMAGE_GENERATION_PROBABILITY = 1

print(f"{'DRYRUN' if DRYRUN else 'LIVE'} MODE: {'Not posting' if DRYRUN else 'Will post'} real casts")


class QueueManager:
    def __init__(self, file_path="farcaster_reply_history.json"):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.write_data({"processed_replies": {}, "pending_replies": {}, "conversation_threads": {}})

    def read_data(self) -> Dict:
        try:
            with self.file_path.open("r") as f:
                data = json.load(f)
                data.setdefault("conversation_threads", {})
                return data
        except json.JSONDecodeError:
            return {"processed_replies": {}, "pending_replies": {}, "conversation_threads": {}}

    def write_data(self, data: Dict):
        try:
            with self.file_path.open("w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Database write error: {str(e)}")

    def add_to_conversation_thread(self, root_hash: str, cast_hash: str, cast_data: Dict):
        data = self.read_data()
        thread = data["conversation_threads"].setdefault(root_hash, [])

        cast = cast_data.get("cast", {})
        thread.append(
            {
                "cast_hash": cast_hash,
                "timestamp": cast.get("timestamp"),
                "text": cast.get("text", ""),
                "author": cast.get("author", {}).get("username", "anonymous"),
                "parent_hash": cast.get("parent_hash"),
            }
        )

        thread.sort(key=lambda x: parse_timestamp(x["timestamp"]) or datetime.min.replace(tzinfo=timezone.utc))
        self.write_data(data)

    def get_conversation_thread(self, root_hash: str) -> List[Dict]:
        return self.read_data()["conversation_threads"].get(root_hash, [])

    def mark_as_processed(self, cast_hash: str, response_data: Dict):
        data = self.read_data()
        if cast_hash in data["pending_replies"]:
            reply_data = data["pending_replies"].pop(cast_hash)
            reply_data.update(response_data)
            data["processed_replies"][cast_hash] = reply_data
            self.write_data(data)
            logger.info(f"Marked cast as processed: {cast_hash}")

    def add_pending_reply(self, cast_hash: str, cast_data: Dict):
        data = self.read_data()
        if cast_hash not in data["processed_replies"] and cast_hash not in data["pending_replies"]:
            data["pending_replies"][cast_hash] = cast_data
            self.write_data(data)
            logger.info(f"Added pending cast: {cast_hash}")

    def is_processed(self, cast_hash: str) -> bool:
        return cast_hash in self.read_data()["processed_replies"]

    def get_processed_cast_ids(self) -> set:
        return set(self.read_data()["processed_replies"].keys())

    def get_pending_cast_ids(self) -> set:
        return set(self.read_data()["pending_replies"].keys())


class FarcasterAPI:
    def __init__(self, api_key: str, signer_uuid: str):
        self.base_url = "https://api.neynar.com/v2/farcaster"
        self.headers = {"accept": "application/json", "api_key": api_key, "Content-Type": "application/json"}
        self.signer_uuid = signer_uuid

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        try:
            response = requests.request(method, f"{self.base_url}/{endpoint}", headers=self.headers, **kwargs)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"API request error: {str(e)}")
            return None

    def get_cast_with_context(self, cast_hash: str) -> Optional[Dict]:
        return self._make_request("GET", "cast", params={"identifier": cast_hash, "type": "hash"})

    def send_cast(
        self, message: str, parent_hash: Optional[str] = None, image_url: Optional[str] = None
    ) -> Optional[Dict]:
        data = {
            "signer_uuid": self.signer_uuid,
            "text": message,
            **({"parent": parent_hash} if parent_hash else {}),
            **({"embeds": [{"url": image_url}]} if image_url else {}),
        }

        logger.info(f"Sending cast: {message}")
        return self._make_request("POST", "cast", json=data)

    def get_mentions(self, fid: int, limit: int = 25) -> List[Dict]:
        return self._make_request(
            "GET", "notifications", params={"fid": fid, "type": "mentions", "priority_mode": "false"}
        ).get("notifications", [])


class FarcasterReplyMonitor:
    def __init__(self, api_key: str, signer_uuid: str, fid: int, queue_manager: QueueManager):
        self.api = FarcasterAPI(api_key, signer_uuid)
        self.fid = fid
        self.queue_manager = queue_manager

    def filter_mentions(self, mentions: List[Dict]) -> List[Dict]:
        processed_ids = self.queue_manager.get_processed_cast_ids()
        pending_ids = self.queue_manager.get_pending_cast_ids()

        filtered_mentions = []
        for mention in mentions:
            cast = mention.get("cast", {})
            cast_hash = cast.get("hash")

            if cast_hash in processed_ids or cast_hash in pending_ids:
                continue

            # Additional filtering logic can be added here

            filtered_mentions.append(mention)

        return filtered_mentions

    def process_mentions(self) -> List[Dict]:
        logger.info("Fetching mentions...")
        mentions = self.api.get_mentions(self.fid)

        if not mentions:
            logger.info("No mentions found")
            return []

        filtered_mentions = self.filter_mentions(mentions)

        for mention in filtered_mentions:
            cast = mention.get("cast", {})
            cast_hash = cast.get("hash")

            # Add to queue
            self.queue_manager.add_pending_reply(cast_hash, mention)

            # Process conversation thread if it exists
            parent_hash = cast.get("parent_hash")
            if parent_hash:
                conversation_tree = build_conversation_tree(mention, self.api)
                root_hash = conversation_tree[0]["hash"] if conversation_tree else parent_hash

                for cast_entry in conversation_tree:
                    self.queue_manager.add_to_conversation_thread(
                        root_hash,
                        cast_entry["hash"],
                        {
                            "cast": {
                                "hash": cast_entry["hash"],
                                "text": cast_entry["text"],
                                "author": {"username": cast_entry["author"]},
                                "timestamp": cast_entry["timestamp"],
                                "parent_hash": cast_entry["parent_hash"],
                            }
                        },
                    )

        return filtered_mentions


class FarcasterReplyAgent:
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
        self.monitor = FarcasterReplyMonitor(
            api_key=FARCASTER_API_KEY,
            signer_uuid=FARCASTER_SIGNER_UUID,
            fid=FARCASTER_FID,
            queue_manager=self.queue_manager,
        )
        self.register_interface("farcaster_reply", self)

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

    async def send_message(self, chat_id: str, message: str, image_url: str = None):
        """Interface method called by CoreAgent's send_to_interface"""
        logger.debug(f"send_message {chat_id} {message} {image_url}")
        if not DRYRUN:
            api = FarcasterAPI(FARCASTER_API_KEY, FARCASTER_SIGNER_UUID)
            api.send_cast(message, parent_hash=chat_id, image_url=image_url)
        else:
            print(f"DRYRUN MODE: Would have replied to {chat_id} with {message} and image {image_url}")

    async def process_reply(self, notification: Dict):
        cast = notification.get("cast", {})
        cast_hash = cast.get("hash")

        try:
            logger.debug(f"Processing reply for cast {cast_hash}")

            parent_hash = cast.get("parent_hash")
            conversation_context = None

            if parent_hash:
                logger.debug(f"Found parent hash {parent_hash}, retrieving conversation context")
                conversation_tree = build_conversation_tree(notification, self.monitor.api)
                if conversation_tree:
                    root_hash = conversation_tree[0]["hash"]
                    conversation_context = self.queue_manager.get_conversation_thread(root_hash)
                    logger.info(f"Retrieved conversation context with {len(conversation_context)} messages")

            prompt_config = PromptConfig()
            if conversation_context:
                context_str = "\n".join([f"@{msg['author']}: {msg['text']}" for msg in conversation_context])
                message = f"""This is a conversation thread:

{context_str}

The latest reply is from @{cast["author"]["username"]}: "{cast["text"]}"

Please generate a contextually relevant reply that takes into account the entire conversation history."""
            else:
                message = prompt_config.get_farcaster_reply_template().format(
                    author_name=cast["author"]["username"], message=cast["text"]
                )

            # Generate response using CoreAgent's handle_message
            response, image_url, _ = await self.handle_message(
                message=message,
                source_interface="farcaster_reply",
                chat_id=cast_hash,
                skip_embedding=True,
                skip_tools=True,
            )

            # Send the response
            await self.send_message(cast_hash, response, image_url)

            # Update queue with response data
            response_data = {"response": response, "processed_timestamp": datetime.now().isoformat()}
            if image_url:
                response_data["image_url"] = image_url

            self.queue_manager.mark_as_processed(cast_hash, response_data)
            logger.info(f"Successfully processed and responded to cast {cast_hash}")

            return response, image_url

        except Exception as e:
            logger.error(f"Error processing reply: {str(e)}")
            return None, None

    async def run_workers(self, num_workers: int = 3):
        """Run multiple reply workers"""

        async def worker():
            while True:
                try:
                    mentions = self.monitor.process_mentions()
                    for mention in mentions:
                        await self.process_reply(mention)
                        await asyncio.sleep(RATE_LIMIT_SLEEP)

                    await asyncio.sleep(REPLY_CHECK_INTERVAL)

                except Exception as e:
                    logger.error(f"Worker error: {str(e)}")
                    await asyncio.sleep(REPLY_CHECK_INTERVAL)

        workers = [worker() for _ in range(num_workers)]
        await asyncio.gather(*workers)

    def start_monitoring(self):
        """Start monitoring in background thread"""

        def monitor_mentions():
            while True:
                self.monitor.process_mentions()
                time.sleep(REPLY_CHECK_INTERVAL)

        monitor_thread = threading.Thread(target=monitor_mentions, daemon=True)
        monitor_thread.start()
        return monitor_thread

    async def start(self):
        """Main entry point to start the agent"""
        self.start_monitoring()

        try:
            await self.run_workers()
        except KeyboardInterrupt:
            logger.info("Shutting down...")


def build_conversation_tree(notification: Dict, farcaster_api: FarcasterAPI) -> List[Dict]:
    conversation = []
    current_cast = notification.get("cast", {})
    visited_hashes = set()

    while current_cast and current_cast.get("hash") not in visited_hashes:
        visited_hashes.add(current_cast.get("hash"))

        full_cast_data = farcaster_api.get_cast_with_context(current_cast.get("hash"))
        cast_details = full_cast_data.get("cast", current_cast) if full_cast_data else current_cast

        conversation.append(
            {
                "hash": cast_details.get("hash"),
                "text": cast_details.get("text", ""),
                "author": cast_details.get("author", {}).get("username", "anonymous"),
                "timestamp": cast_details.get("timestamp"),
                "parent_hash": cast_details.get("parent_hash"),
            }
        )

        if current_cast.get("parent_hash"):
            parent_cast = farcaster_api.get_cast_with_context(current_cast["parent_hash"])
            current_cast = parent_cast.get("cast") if parent_cast else None
        else:
            break

    return list(reversed(conversation))


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.000Z")
        return dt.replace(tzinfo=timezone.utc)
    except Exception as e:
        logger.error(f"Timestamp parsing error {timestamp_str}: {str(e)}")
        return None


@lru_cache(maxsize=100)
def upload_to_imgbb(image_url: str) -> Optional[str]:
    """Upload an image to IMGBB with caching for repeated uploads"""
    try:
        api_key = os.getenv("IMGBB_API_KEY")
        if not api_key:
            raise ValueError("IMGBB_API_KEY not found")

        image_data = urlopen(image_url).read()
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": api_key, "image": base64.b64encode(image_data).decode("utf-8")},
        )

        return response.json()["data"]["url"] if response.status_code == 200 else None

    except Exception as e:
        logger.error(f"IMGBB upload error: {str(e)}")
        return None


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_llm(
    url: str, api_key: str, model_id: str, system_prompt: str, user_prompt: str, temperature: float = 0.7
) -> str:
    """Call LLM with retry logic"""
    try:
        response = requests.post(
            f"{url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model_id,
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}")


async def main():
    """Main entry point"""
    agent = FarcasterReplyAgent()
    await agent.start()


if __name__ == "__main__":
    asyncio.run(main())
