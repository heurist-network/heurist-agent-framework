"""Autonomys Auto Drive (ai3.storage) client for skill file storage.

Upload protocol: create session → send chunks → complete → returns CID.
Download: tries public gateway first, falls back to authenticated API.
"""

import hashlib
import logging
import math
import os

import aiohttp

logger = logging.getLogger("SkillMarketplace")

AUTONOMYS_API_KEY = os.getenv("AI3_API_KEY", "")
AUTONOMYS_API_URL = os.getenv("AUTONOMYS_API_URL", "https://mainnet.auto-drive.autonomys.xyz")
AUTONOMYS_GATEWAY_URL = os.getenv("AUTONOMYS_GATEWAY_URL", "https://gateway.autonomys.xyz")

CHUNK_SIZE = 1024 * 1024


def _headers():
    return {
        "Authorization": f"Bearer {AUTONOMYS_API_KEY}",
        "X-Auth-Provider": "apikey",
    }


async def upload_file(content: bytes, filename: str) -> dict:
    """Upload a file to Autonomys DSN and return its CID, SHA256, and gateway URL."""
    sha256 = hashlib.sha256(content).hexdigest()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTONOMYS_API_URL}/api/uploads/file",
            headers={**_headers(), "Content-Type": "application/json"},
            json={"filename": filename, "mimeType": "text/markdown", "uploadOptions": None},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            upload_id = data["id"] if isinstance(data, dict) else data

        total_chunks = max(1, math.ceil(len(content) / CHUNK_SIZE))
        for i in range(total_chunks):
            chunk = content[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
            form = aiohttp.FormData()
            form.add_field("file", chunk, filename="chunk", content_type="application/octet-stream")
            form.add_field("index", str(i))
            async with session.post(
                f"{AUTONOMYS_API_URL}/api/uploads/file/{upload_id}/chunk",
                headers=_headers(),
                data=form,
            ) as resp:
                resp.raise_for_status()

        async with session.post(
            f"{AUTONOMYS_API_URL}/api/uploads/{upload_id}/complete",
            headers=_headers(),
        ) as resp:
            resp.raise_for_status()
            result = await resp.json()
            cid = result["cid"] if isinstance(result, dict) else result

    gateway_url = f"{AUTONOMYS_GATEWAY_URL}/file/{cid}"
    logger.info(f"uploaded {filename} -> CID {cid}")
    return {"cid": cid, "sha256": sha256, "gateway_url": gateway_url}


async def download_file(cid: str) -> bytes:
    """Download a file from Autonomys by CID. Tries public gateway first."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{AUTONOMYS_GATEWAY_URL}/file/{cid}") as resp:
            if resp.status == 200:
                return await resp.read()

        # gateway miss — fall back to authenticated API
        async with session.get(
            f"{AUTONOMYS_API_URL}/api/downloads/{cid}",
            headers=_headers(),
        ) as resp:
            resp.raise_for_status()
            return await resp.read()
