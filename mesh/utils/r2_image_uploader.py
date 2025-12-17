import logging
import os
from typing import Optional
from pathlib import Path

import aiohttp
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class R2ImageUploader:
    def __init__(self):
        self.endpoint = os.getenv("R2_ENDPOINT")
        self.access_key = os.getenv("R2_ACCESS_KEY")
        self.secret_key = os.getenv("R2_SECRET_KEY")
        self.bucket_name = "ask-heurist"

        if not all([self.endpoint, self.access_key, self.secret_key]):
            raise ValueError("R2_ENDPOINT, R2_ACCESS_KEY, and R2_SECRET_KEY must be set in environment")

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="auto",
        )

    def _file_exists(self, key: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    async def _download_image(self, url: str) -> Optional[bytes]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    logger.error(f"Failed to download image from {url}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            return None

    def _upload_to_r2(self, key: str, data: bytes, content_type: str = "image/png") -> bool:
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=data, ContentType=content_type)
            logger.info(f"Successfully uploaded {key} to R2")
            return True
        except Exception as e:
            logger.error(f"Error uploading {key} to R2: {e}")
            return False

    async def upload_token_images(self, coingecko_id: str, image_urls: dict) -> dict:
        results = {}

        for size in ["thumb", "small"]:
            if size not in image_urls:
                continue

            url = image_urls[size]
            extension = Path(url).suffix.split("?")[0] or ".png"
            size_suffix = "thumbnail" if size == "thumb" else "small"
            r2_key = f"token-icon/{coingecko_id}-{size_suffix}{extension}"

            if self._file_exists(r2_key):
                logger.info(f"Image already exists at {r2_key}, skipping upload")
                results[size] = {"skipped": True, "r2_key": r2_key}
                continue

            image_data = await self._download_image(url)
            if not image_data:
                results[size] = {"success": False, "error": "Failed to download image"}
                continue

            content_type = "image/png" if extension == ".png" else f"image/{extension.lstrip('.')}"
            success = self._upload_to_r2(r2_key, image_data, content_type)

            results[size] = {"success": success, "r2_key": r2_key if success else None}

        return results
