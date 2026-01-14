"""
R2 Client for ERC-8004 Registration Files

Handles uploading and reading agent registration JSON files from Cloudflare R2.
"""

import json
import os

import boto3
from botocore.exceptions import ClientError
from loguru import logger

from mesh.erc8004.config import R2_CONFIG


class ERC8004R2Client:
    def __init__(self):
        self.endpoint = os.getenv("R2_ENDPOINT")
        self.access_key = os.getenv("R2_ACCESS_KEY")
        self.secret_key = os.getenv("R2_SECRET_KEY")
        self.bucket = R2_CONFIG["bucket"]
        self.base_url = R2_CONFIG["base_url"]
        self.folder = R2_CONFIG["folder"]

        if not all([self.endpoint, self.access_key, self.secret_key]):
            raise ValueError("R2_ENDPOINT, R2_ACCESS_KEY, and R2_SECRET_KEY must be set")

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="auto",
        )

    def _get_key(self, agent_name: str) -> str:
        return f"{self.folder}/{agent_name}.json"

    def get_registration(self, agent_name: str) -> dict | None:
        """Read existing registration JSON from R2, return None if not found"""
        key = self._get_key(agent_name)
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
            content = response["Body"].read().decode("utf-8")
            return json.loads(content)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise

    def upload_registration(self, agent_name: str, registration_data: dict) -> str:
        """Upload registration JSON, return public URL"""
        key = self._get_key(agent_name)
        body = json.dumps(registration_data, indent=2)

        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )

        url = f"{self.base_url}/{key}"
        logger.info(f"Uploaded registration to {url}")
        return url

    def delete_registration(self, agent_name: str) -> bool:
        """Delete registration JSON from R2, return True if deleted"""
        key = self._get_key(agent_name)
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"Deleted registration {key}")
            return True
        except ClientError:
            return False

    def list_registrations(self) -> list[str]:
        """List all registration files in the erc8004 folder"""
        prefix = f"{self.folder}/"
        response = self.s3_client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)

        agent_names = []
        for obj in response.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".json"):
                name = key[len(prefix) : -5]  # Remove prefix and .json suffix
                agent_names.append(name)

        return agent_names
