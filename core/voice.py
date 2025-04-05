import hashlib
import logging
import os
import random
from pathlib import Path
from typing import Optional

from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy client initialization
_client = None


def _get_client():
    """Get or initialize the OpenAI client"""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OpenAI API key not found. Set the OPENAI_API_KEY environment variable to use voice functionality."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def transcribe_audio(file_path: str) -> str:
    """Transcribe audio to text using OpenAI's Whisper model"""
    try:
        client = _get_client()
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcription.text
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise


def speak_text(text: str) -> Optional[Path]:
    """Convert text to speech using OpenAI's TTS model"""
    try:
        client = _get_client()
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )

        project_root = Path(__file__).parent.parent
        audio_dir = project_root / "audio"
        audio_dir.mkdir(exist_ok=True)

        random_string = str(random.randint(1, 1000000))
        hash_object = hashlib.sha1(random_string.encode())
        filename = hash_object.hexdigest()[:8]
        file_path = audio_dir / f"{filename}.mp3"

        response.stream_to_file(file_path)
        logger.info(f"Audio content saved as '{file_path}'")
        return file_path
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        raise
