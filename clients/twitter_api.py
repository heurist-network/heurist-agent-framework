import os
from typing import Optional
from urllib.parse import urlparse

import requests
import tweepy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Create Client object
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

# We still need v1.1 API for media upload
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet_with_image(text, image_source):
    # Check if image_source is a URL
    if image_source.startswith(("http://", "https://")):
        # Download the image
        response = requests.get(image_source)
        if response.status_code != 200:
            raise Exception("Failed to download image")

        # Get the filename from the URL
        filename = os.path.basename(urlparse(image_source).path)
        if not filename:
            filename = "temp_image.jpg"

        # Save the image temporarily
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        # Assume image_source is a local file path
        filename = image_source

    # Upload the image using v1.1 API
    media = api.media_upload(filename)

    # Post the tweet with the uploaded media using v2 API
    response = client.create_tweet(text=text, media_ids=[media.media_id])

    # Get authenticated user info
    me = client.get_me()
    author_username = me.data.username

    # If the image was downloaded, delete the temporary file
    if image_source.startswith(("http://", "https://")):
        os.remove(filename)

    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    return response.data["id"], author_username


def tweet_text_only(text):
    # Post tweet with text only using v2 API
    print("Posting tweet with text only using v2 API")
    response = client.create_tweet(text=text)

    # Get authenticated user info
    me = client.get_me()
    author_username = me.data.username

    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    return response.data["id"], author_username


def reply(text, in_reply_to_tweet_id):
    print("Posting tweet in reply")
    response = client.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_tweet_id)
    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    return response.data["id"]


def reply_with_image(text, image_source, in_reply_to_tweet_id):
    if image_source.startswith(("http://", "https://")):
        response = requests.get(image_source)
        if response.status_code != 200:
            raise Exception("Failed to download image")

        # Get the filename from the URL
        filename = os.path.basename(urlparse(image_source).path)
        if not filename:
            filename = "temp_image.jpg"

        # Save the image temporarily
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        # Assume image_source is a local file path
        filename = image_source

    media = api.media_upload(filename)
    response = client.create_tweet(text=text, media_ids=[media.media_id], in_reply_to_tweet_id=in_reply_to_tweet_id)

    # If the image was downloaded, delete the temporary file
    if image_source.startswith(("http://", "https://")):
        os.remove(filename)

    print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
    return response.data["id"]


def get_user_id(username):
    """Get Twitter user ID from username"""
    try:
        # Remove @ if present
        username = username.lstrip("@")

        # Look up user
        user = client.get_user(username=username)

        if user.data:
            return str(user.data.id)
        return None

    except Exception as e:
        print(f"Error getting user ID for {username}: {str(e)}")
        return None


def get_tweet(tweet_id: str):
    """Get tweet content and metadata"""
    try:
        tweet = client.get_tweet(
            tweet_id,
            expansions=["author_id", "referenced_tweets.id"],
            tweet_fields=["created_at", "text", "referenced_tweets"],
        )

        if not tweet.data:
            return None

        # Extract basic tweet data
        tweet_data = {
            "id": tweet.data.id,
            "text": tweet.data.text,
            "author_id": tweet.data.author_id,
            "created_at": tweet.data.created_at,
        }

        # Add referenced tweet data if available
        if hasattr(tweet.data, "referenced_tweets") and tweet.data.referenced_tweets:
            tweet_data["referenced_tweets"] = [{"type": ref.type, "id": ref.id} for ref in tweet.data.referenced_tweets]

        return tweet_data

    except Exception as e:
        print(f"Error fetching tweet {tweet_id}: {str(e)}")
        return None


def get_tweet_text(tweet_id: str) -> Optional[str]:
    """Get just the text content of a tweet"""
    try:
        tweet = client.get_tweet(tweet_id, tweet_fields=["text"])
        if tweet.data:
            return tweet.data.text
        return None
    except Exception as e:
        print(f"Error fetching tweet text {tweet_id}: {str(e)}")
        return None


def get_referenced_tweet_id(tweet_id: str, ref_type: str = "replied_to") -> Optional[str]:
    """
    Get ID of referenced tweet (reply to, quote, etc)
    ref_type can be 'replied_to' or 'quoted'
    """
    try:
        tweet = client.get_tweet(tweet_id, expansions=["referenced_tweets"])

        if not tweet.data or not tweet.data.referenced_tweets:
            return None

        for ref in tweet.data.referenced_tweets:
            if (ref_type == "replied_to" and ref.type == "replied_to") or (
                ref_type == "quoted" and ref.type == "quoted"
            ):
                return ref.id

        return None

    except Exception as e:
        print(f"Error getting referenced tweet for {tweet_id}: {str(e)}")
        return None


# Example usage
# tweet_text = "Hello, Twitter! This is a test tweet with an image using API v2."
# image_url = "https://heurist-images.s3.us-east-1.amazonaws.com/sdk-image-dc55866be9-0x223759397ED62960222AF946aF833993220835d9-e14f4d.png?x-id=GetObject&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAWOPEZTMXKJKQSPG5%2F20241025%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241025T191541Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=9a4614d87a16d3fc69a397dfe2bc737ec7c06da0e18588640d576031e5083d85"

# tweet_with_image(tweet_text, image_url)

# Example usage of the text-only function
# text_only_tweet = "This is a text-only tweet using API v2!"
# tweet_text_only(text_only_tweet)

# print(get_user_id("heurist_ai"))
# print(get_tweet("1870107660260880471"))
