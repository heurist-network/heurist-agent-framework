import asyncio
import logging
import os
import random
import re
import string
import threading
import time
from decimal import Decimal
from typing import Any

import aiohttp
import boto3
import botocore.exceptions
from boto3.dynamodb.types import TypeSerializer
from fastapi import HTTPException

logger = logging.getLogger("TweetClaim")

VERIFICATION_TTL = 600  # 10 minutes
FREE_CREDITS = Decimal("100")
PENDING_ITEM_TYPE = "PENDING_VERIFICATION"
CLAIMED_ITEM_TYPE = "CLAIMED_HANDLE"
CLAIM_KEY_ATTR = "claim_key"
CLAIMS_TABLE_NAME = "tweet-credits-claims"


class ClaimStoreError(Exception):
    pass


class ClaimStoreUnavailableError(ClaimStoreError):
    pass


class InvalidOrExpiredVerificationCodeError(ClaimStoreError):
    pass


class AlreadyClaimedError(ClaimStoreError):
    pass


class ClaimStore:
    """Storage abstraction for pending verification codes and claimed handles."""

    def __init__(self):
        self.users_table_name = os.getenv("DYNAMODB_TABLE_NAME")
        self.claims_table_name = CLAIMS_TABLE_NAME
        self.aws_region = os.getenv("AWS_REGION")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self._resource = None
        self._client = None
        self._users_table = None
        self._claims_table = None
        self._serializer = TypeSerializer()
        self._ready = False
        self._ready_lock = threading.Lock()

    def _build_boto_kwargs(self) -> dict[str, str]:
        kwargs: dict[str, str] = {}
        if self.aws_region:
            kwargs["region_name"] = self.aws_region
        if self.aws_access_key_id and self.aws_secret_access_key:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key
        return kwargs

    def _get_resource(self):
        if self._resource is None:
            self._resource = boto3.resource("dynamodb", **self._build_boto_kwargs())
        return self._resource

    def _get_client(self):
        if self._client is None:
            self._client = boto3.client("dynamodb", **self._build_boto_kwargs())
        return self._client

    def _get_users_table(self):
        if not self.users_table_name:
            raise ClaimStoreUnavailableError("DYNAMODB_TABLE_NAME is not configured")
        if self._users_table is None:
            self._users_table = self._get_resource().Table(self.users_table_name)
        return self._users_table

    def _get_claims_table(self):
        if not self.claims_table_name:
            raise ClaimStoreUnavailableError("Claims table name is not configured")
        if self._claims_table is None:
            self._claims_table = self._get_resource().Table(self.claims_table_name)
        return self._claims_table

    def _serialize_item(self, item: dict[str, Any]) -> dict[str, Any]:
        return {key: self._serializer.serialize(value) for key, value in item.items()}

    def _code_key(self, code: str) -> str:
        return f"CODE#{code}"

    def _handle_key(self, twitter_handle: str) -> str:
        return f"HANDLE#{twitter_handle}"

    def ensure_ready(self):
        with self._ready_lock:
            if self._ready:
                return
            try:
                self._get_users_table().load()
                self._get_claims_table().load()
            except botocore.exceptions.ClientError as exc:
                raise ClaimStoreUnavailableError(f"Unable to access DynamoDB tables: {exc}") from exc
            self._ready = True

    def create_pending_verification(self, code: str, created_at: int):
        self.ensure_ready()
        expires_at = created_at + VERIFICATION_TTL
        self._get_claims_table().put_item(
            Item={
                CLAIM_KEY_ATTR: self._code_key(code),
                "item_type": PENDING_ITEM_TYPE,
                "verification_code": code,
                "created_at": created_at,
                "expires_at": expires_at,
            }
        )

    def is_verification_code_active(self, code: str, now_ts: int) -> bool:
        self.ensure_ready()
        response = self._get_claims_table().get_item(
            Key={CLAIM_KEY_ATTR: self._code_key(code)},
            ConsistentRead=True,
        )
        item = response.get("Item")
        if not item:
            return False
        return item.get("item_type") == PENDING_ITEM_TYPE and int(item.get("expires_at", 0)) > now_ts

    def _is_handle_claimed(self, twitter_handle: str) -> bool:
        response = self._get_claims_table().get_item(
            Key={CLAIM_KEY_ATTR: self._handle_key(twitter_handle)},
            ConsistentRead=True,
        )
        return "Item" in response

    def create_claim_and_user(
        self,
        twitter_handle: str,
        api_key_part: str,
        verification_code: str,
        tweet_id: str,
        now_ts: int,
    ):
        self.ensure_ready()

        if self._is_handle_claimed(twitter_handle):
            raise AlreadyClaimedError("Twitter handle already claimed")

        client = self._get_client()
        full_api_key_item = {"user_id": twitter_handle, "api_key": api_key_part}
        user_data_item = {"user_id": twitter_handle, "api_key": "USER_DATA", "remaining_credits": FREE_CREDITS}
        claimed_item = {
            CLAIM_KEY_ATTR: self._handle_key(twitter_handle),
            "item_type": CLAIMED_ITEM_TYPE,
            "twitter_handle": twitter_handle,
            "tweet_id": tweet_id,
            "verification_code": verification_code,
            "claimed_at": now_ts,
        }

        try:
            client.transact_write_items(
                TransactItems=[
                    {
                        "Delete": {
                            "TableName": self.claims_table_name,
                            "Key": self._serialize_item({CLAIM_KEY_ATTR: self._code_key(verification_code)}),
                            "ConditionExpression": "attribute_exists(claim_key) AND item_type = :pending_type AND expires_at > :now",
                            "ExpressionAttributeValues": self._serialize_item(
                                {
                                    ":pending_type": PENDING_ITEM_TYPE,
                                    ":now": now_ts,
                                }
                            ),
                        }
                    },
                    {
                        "Put": {
                            "TableName": self.claims_table_name,
                            "Item": self._serialize_item(claimed_item),
                            "ConditionExpression": "attribute_not_exists(claim_key)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": self.users_table_name,
                            "Item": self._serialize_item(full_api_key_item),
                            "ConditionExpression": "attribute_not_exists(user_id) AND attribute_not_exists(api_key)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": self.users_table_name,
                            "Item": self._serialize_item(user_data_item),
                            "ConditionExpression": "attribute_not_exists(user_id) AND attribute_not_exists(api_key)",
                        }
                    },
                ]
            )
        except botocore.exceptions.ClientError as exc:
            err_code = exc.response.get("Error", {}).get("Code")
            if err_code == "TransactionCanceledException":
                if self._is_handle_claimed(twitter_handle):
                    raise AlreadyClaimedError("Twitter handle already claimed") from exc
                if not self.is_verification_code_active(verification_code, now_ts):
                    raise InvalidOrExpiredVerificationCodeError("Invalid or expired verification code") from exc
            raise ClaimStoreError(f"Failed to persist claim transaction: {exc}") from exc


claim_store = ClaimStore()


def generate_verification_code() -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=5))


def parse_tweet_url(url: str) -> tuple[str, str]:
    match = re.match(r"https?://(?:www\.)?(?:twitter\.com|x\.com)/(\w+)/status/(\d+)", url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid tweet URL format")
    return match.group(1), match.group(2)


def validate_claim_tweet(tweet_text: str, code: str):
    tweet_text_lower = tweet_text.lower()
    if "@heurist_ai" not in tweet_text_lower:
        raise HTTPException(status_code=400, detail="Tweet does not contain the required claim text")
    if not re.search(rf"\bverification:\s*{re.escape(code)}\b", tweet_text_lower):
        raise HTTPException(status_code=400, detail="Tweet does not contain the verification code")


async def _fetch_tweet_from_fxtwitter(username: str, tweet_id: str) -> tuple[tuple[str, str] | None, bool]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.fxtwitter.com/{username}/status/{tweet_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("code") == 200 and data.get("tweet"):
                        tweet = data["tweet"]
                        screen_name = tweet.get("author", {}).get("screen_name", username)
                        text = tweet.get("text", "")
                        return (screen_name, text), False
                if resp.status == 404:
                    return None, True
                logger.warning(f"FXTwitter unexpected status {resp.status} for tweet {tweet_id}")
    except Exception as exc:
        logger.warning(f"FXTwitter failed: {exc}")
    return None, False


async def _fetch_tweet_from_apidance(
    username: str, tweet_id: str, apidance_key: str
) -> tuple[tuple[str, str] | None, bool]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.apidance.pro/sapi/TweetDetail?tweet_id={tweet_id}",
                headers={"apikey": apidance_key},
            ) as resp:
                if resp.status == 404:
                    return None, True
                if resp.status != 200:
                    logger.warning(f"APIDance unexpected status {resp.status} for tweet {tweet_id}")
                    return None, False
                data = await resp.json()
                root = data.get("data") or data
                tweets = root.get("tweets") or []
                for tweet in tweets:
                    tid = str(tweet.get("tweet_id") or tweet.get("id_str") or tweet.get("id") or "")
                    if tid == tweet_id:
                        screen_name = (tweet.get("user") or {}).get("screen_name", username)
                        text = tweet.get("text", "")
                        return (screen_name, text), False
                return None, True
    except Exception as exc:
        logger.warning(f"APIDance failed: {exc}")
        return None, False


async def fetch_tweet(username: str, tweet_id: str) -> tuple[str, str]:
    attempts = 0
    not_found_signals = 0

    result, not_found = await _fetch_tweet_from_fxtwitter(username, tweet_id)
    attempts += 1
    if result:
        return result
    if not_found:
        not_found_signals += 1

    apidance_key = os.getenv("APIDANCE_API_KEY")
    if apidance_key:
        result, not_found = await _fetch_tweet_from_apidance(username, tweet_id, apidance_key)
        attempts += 1
        if result:
            return result
        if not_found:
            not_found_signals += 1

    if attempts > 0 and not_found_signals == attempts:
        raise HTTPException(status_code=404, detail="Tweet not found")
    raise HTTPException(status_code=502, detail="Tweet verification service unavailable")


def ensure_claim_store_ready_sync():
    claim_store.ensure_ready()


async def initiate_claim() -> dict:
    try:
        await asyncio.to_thread(claim_store.ensure_ready)
    except ClaimStoreUnavailableError as exc:
        logger.error(f"Claim store unavailable during initiate: {exc}")
        raise HTTPException(status_code=503, detail="Tweet claim service unavailable")

    code = generate_verification_code()
    created_at = int(time.time())
    try:
        await asyncio.to_thread(claim_store.create_pending_verification, code, created_at)
    except ClaimStoreError as exc:
        logger.error(f"Failed to create pending verification: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to initiate claim")

    tweet_text = (
        f"I'm claiming my free API credits on @heurist_ai Mesh\n\nverification: {code}"
    )

    return {
        "verification_code": code,
        "tweet_text": tweet_text,
        "instructions": "Post the tweet text above on X (Twitter), then call /claim_credits/verify with the tweet URL and verification code.",
    }


async def verify_claim(tweet_url: str, verification_code: str) -> dict:
    code = verification_code.lower().strip()
    now_ts = int(time.time())

    try:
        await asyncio.to_thread(claim_store.ensure_ready)
    except ClaimStoreUnavailableError as exc:
        logger.error(f"Claim store unavailable during verify: {exc}")
        raise HTTPException(status_code=503, detail="Tweet claim service unavailable")

    code_active = await asyncio.to_thread(claim_store.is_verification_code_active, code, now_ts)
    if not code_active:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    username, tweet_id = parse_tweet_url(tweet_url)
    screen_name, tweet_text = await fetch_tweet(username, tweet_id)
    validate_claim_tweet(tweet_text, code)

    twitter_handle = screen_name.lower()
    api_key_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))
    try:
        await asyncio.to_thread(
            claim_store.create_claim_and_user, twitter_handle, api_key_part, code, tweet_id, now_ts
        )
    except AlreadyClaimedError:
        raise HTTPException(status_code=409, detail="This Twitter account has already claimed credits")
    except InvalidOrExpiredVerificationCodeError:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    except ClaimStoreUnavailableError as exc:
        logger.error(f"Claim store unavailable during transaction: {exc}")
        raise HTTPException(status_code=503, detail="Tweet claim service unavailable")
    except ClaimStoreError as exc:
        logger.error(f"Claim transaction failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Unable to complete claim")

    full_api_key = f"{twitter_handle}-{api_key_part}"
    logger.info(f"Credits claimed for @{screen_name} -> {twitter_handle}")

    return {
        "api_key": full_api_key,
        "credits": 100,
        "twitter_handle": twitter_handle,
    }
