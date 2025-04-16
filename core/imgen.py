import json
import logging
import os
import random
import time

import dotenv
import requests
from requests.exceptions import Timeout

from .heurist_image.SmartGen import SmartGen
from .llm import call_llm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
os.environ.clear()
dotenv.load_dotenv(override=True)

# Constants
HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
SEQUENCER_API_ENDPOINT = "http://sequencer.heurist.xyz/submit_job"
PROMPT_MODEL_ID = "mistralai/mixtral-8x7b-instruct"

AVAILABLE_IMAGE_MODELS = ["AnimagineXL", "BrainDance", "ArthemyComics", "AAMXLAnimeMix"]

IMAGE_MODEL_ID = os.getenv("IMAGE_MODEL_ID") or random.choice(AVAILABLE_IMAGE_MODELS)

# Image generation settings
IMAGE_SETTINGS = {"width": 1024, "height": 1024, "num_iterations": 30, "guidance_scale": 3, "deadline": 60}

# Prompt templates
template_heuman_prompt = """
Important techniques to create high-quality prompts: Specify a realistic, cinematic, with a sense of mystery and tension image style. Describe the pose, activity, camera, lighting, and environment. Be creative and descriptive.

Follow these examples
1. A cinematic and realistic scene depicting a male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents. The scene is set in a futuristic urban landscape with towering structures, dim ambient lighting, and dramatic shadows, enhancing the epic mood. Fog rolls through the background, and faint neon lights reflect off the robot, creating a sense of mystery and tension. The mood is cinematic, evoking both awe and curiosity, and the power behind the Heuristai symbol.

2. In a gritty alleyway bathed in the soft glow of distant neon lights, an old man, wearing a weathered trench coat and a mechanical arm, stands beside a male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents. The man, with deep lines etched into his face and tired eyes, gently places his hand on the robot's back. The background is a dimly lit, rain-soaked urban landscape with flickering signs and towering buildings that disappear into the foggy night sky. Puddles reflect the faint neon light, adding to the cinematic mood. Despite the cold, dystopian setting, there is a sense of warmth between the man and the robot. the Heuristai logo on the robot's head casting a subtle glow.

Task: follow the same language style but add variation to the image contents and compisition. Always include the text description "male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents" without changing this description as the main character. Avoid using metaphors. Do not say "something is like something" but always be direct and straightforward. You should create an image to post on Twitter on behalf of the robot character, which is an AI agent created by Heurist - a decentralized AI compute protocol. The tweet content is: "{tweet}". You don't need to strictly follow the semantic meaning of the tweet but you should be imaginative. Be creative in describing the image to accompany the tweet. Important: "male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents" must be included without changing this sentence. Use less than 80 words. Write a prompt. Only include the prompt and nothing else.
"""

template_heuman_convo_prompt = """
Important techniques to create high-quality prompts: Specify a realistic, cinematic, with a sense of mystery and tension image style. Describe the pose, activity, camera, lighting, and environment. Be creative and descriptive.

Follow these examples
1. A cinematic and realistic scene depicting a male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents. The scene is set in a futuristic urban landscape with towering structures, dim ambient lighting, and dramatic shadows, enhancing the epic mood. Fog rolls through the background, and faint neon lights reflect off the robot, creating a sense of mystery and tension. The mood is cinematic, evoking both awe and curiosity, and the power behind the Heuristai symbol.

2. In a gritty alleyway bathed in the soft glow of distant neon lights, an old man, wearing a weathered trench coat and a mechanical arm, stands beside a male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents. The man, with deep lines etched into his face and tired eyes, gently places his hand on the robot's back. The background is a dimly lit, rain-soaked urban landscape with flickering signs and towering buildings that disappear into the foggy night sky. Puddles reflect the faint neon light, adding to the cinematic mood. Despite the cold, dystopian setting, there is a sense of warmth between the man and the robot. the Heuristai logo on the robot's head casting a subtle glow.

Task: follow the same language style but add variation to the image contents and compisition. Always include the text description "male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents" without changing this description as the main character. Avoid using metaphors. Do not say "something is like something" but always be direct and straightforward. You should create an image to accompany a Twitter reply on behalf of the robot character. The original tweet content is: "{original_tweet}". Robot reply is: "{reply}". You don't need to strictly follow the semantic meaning of the conversation but you should be imaginative and get inspired from the conversation. Be creative in describing the image to accompany the tweet. Important: "male humanoid robot with the heuristai logo as the head. The logo serves as the central design element, integrated seamlessly in the head. the robot body is matte white primary surface with polished chrome accents" must be included without changing this sentence. Use less than 80 words. Write a prompt. Only include the prompt and nothing else.
"""


def generate_job_id():
    """Generate a unique job ID for image generation"""
    import uuid

    return "sdk_image_" + str(uuid.uuid4())


def generate_image_prompt(tweet: str) -> str:
    """Generate an image prompt from a tweet"""
    user_prompt = template_heuman_prompt.format(tweet=tweet)
    system_prompt = "You are a helpful AI assistant. You are an expert in creating prompts for AI art. Your output only contains the prompt texts."
    return call_llm(
        HEURIST_BASE_URL,
        HEURIST_API_KEY,
        PROMPT_MODEL_ID,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.7,
    )


def generate_image_convo_prompt(original_tweet: str, reply: str) -> str:
    """Generate an image prompt from a conversation"""
    user_prompt = template_heuman_convo_prompt.format(original_tweet=original_tweet, reply=reply)
    system_prompt = "You are a helpful AI assistant. You are an expert in creating prompts for AI art. Your output only contains the prompt texts."
    return call_llm(
        HEURIST_BASE_URL,
        HEURIST_API_KEY,
        PROMPT_MODEL_ID,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.7,
    )


async def generate_image_smartgen(prompt: str) -> dict:
    """Generate an image using SmartGen with enhanced parameters."""
    try:
        async with SmartGen(api_key=HEURIST_API_KEY) as generator:
            response = await generator.generate_image(
                description=prompt,
                image_model=IMAGE_MODEL_ID,
                width=IMAGE_SETTINGS["width"],
                height=IMAGE_SETTINGS["height"],
                stylization_level=4,
                detail_level=5,
                color_level=5,
                lighting_level=4,
                quality="high",
            )
            print(response)
            return response["url"]
    except Exception as e:
        logger.error(f"SmartGen image generation failed: {str(e)}")
        return None


def generate_image(prompt: str) -> dict:
    """Generate an image from a prompt"""
    headers = {"Authorization": f"Bearer {HEURIST_API_KEY}", "Content-Type": "application/json"}
    print("Image model: ", IMAGE_MODEL_ID)
    payload = {
        "job_id": generate_job_id(),
        "model_input": {
            "SD": {
                "prompt": prompt,
                "neg_prompt": "",
                "num_iterations": IMAGE_SETTINGS["num_iterations"],
                "width": IMAGE_SETTINGS["width"],
                "height": IMAGE_SETTINGS["height"],
                "guidance_scale": IMAGE_SETTINGS["guidance_scale"],
                "seed": -1,
            }
        },
        "model_id": IMAGE_MODEL_ID,
        "deadline": IMAGE_SETTINGS["deadline"],
        "priority": 1,
    }

    try:
        response = requests.post(SEQUENCER_API_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=30)
    except Timeout:
        logger.error("Request timed out after 30 seconds")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Image generation failed: {response.status_code} - {response.text}")
        return None


def generate_image_with_retry(prompt: str, max_retries: int = 3, delay: int = 2) -> dict:
    """Generate an image with retry mechanism"""
    for attempt in range(max_retries):
        try:
            result = generate_image(prompt=prompt)
            if result:
                return result
        except Exception as e:
            logger.warning(f"Image generation attempt {attempt + 1} failed: {str(e)}")

        if attempt < max_retries - 1:
            time.sleep(delay)

    logger.error(f"Image generation failed after {max_retries} attempts")
    return None


async def generate_image_with_retry_smartgen(prompt: str, max_retries: int = 3, delay: int = 2) -> dict:
    """Generate an image with retry mechanism"""
    for attempt in range(max_retries):
        try:
            result = await generate_image_smartgen(prompt=prompt)
            if result:
                return result
        except Exception as e:
            logger.warning(f"Image generation attempt {attempt + 1} failed: {str(e)}")

        if attempt < max_retries - 1:
            time.sleep(delay)

    logger.error(f"Image generation failed after {max_retries} attempts")
    return None


if __name__ == "__main__":
    # Test image generation
    test_tweet = "test tweet"
    prompt = generate_image_prompt(test_tweet)
    result = generate_image_with_retry(prompt)
    if result:
        logger.info(f"Image generated successfully: {result}")
    else:
        logger.error("Failed to generate image")
