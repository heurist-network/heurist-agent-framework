"""
Usage Tracker - Records API usage to centralized GCP PostgreSQL server.
"""

import os
import logging
import aiohttp
from typing import Optional

logger = logging.getLogger(__name__)

USAGE_API_URL = os.getenv("USAGE_API_URL", "")
USAGE_API_KEY = os.getenv("USAGE_API_KEY", "")


async def record_usage(
    user_id: str,
    agent_name: str,
    credits: float,
) -> bool:
    """
    Record API usage to the centralized usage tracking server.
    Non-blocking - failures are logged but don't affect the main flow.
    """
    if not USAGE_API_URL or not USAGE_API_KEY:
        return True

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{USAGE_API_URL.rstrip('/')}/record",
                json={
                    "user_id": user_id,
                    "agent_name": agent_name,
                    "credits": credits,
                },
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": USAGE_API_KEY,
                },
                timeout=aiohttp.ClientTimeout(total=5),
            ) as response:
                if response.status == 200:
                    logger.debug(f"Usage recorded: {user_id[:16]}... | {agent_name} | {credits}")
                    return True
                else:
                    text = await response.text()
                    logger.warning(f"Usage tracking failed: {response.status} - {text}")
                    return False
    except Exception as e:
        logger.warning(f"Usage tracking error: {e}")
        return False
