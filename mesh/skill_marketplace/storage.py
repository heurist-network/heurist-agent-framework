"""Autonomys Auto Drive (ai3.storage) client for skill file storage.

Supports single file and multi-file folder uploads.
Upload protocol: create session → send chunks → complete → returns CID.
Download: tries public gateway first, falls back to authenticated API.
"""

import hashlib
import io
import logging
import math
import os
import zipfile

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


def bundle_files_to_zip(files: dict[str, bytes]) -> tuple[bytes, str]:
    """Bundle multiple files into a zip archive preserving folder hierarchy.

    Args:
        files: dict mapping relative paths to file contents, e.g.
               {"SKILL.md": b"...", "tools/helper.py": b"..."}

    Returns:
        (zip_bytes, sha256) tuple
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, content in sorted(files.items()):
            zf.writestr(path, content)
    zip_bytes = buf.getvalue()
    sha256 = hashlib.sha256(zip_bytes).hexdigest()
    return zip_bytes, sha256


async def upload_folder(files: dict[str, bytes], folder_name: str) -> dict:
    """Bundle files into a zip and upload to Autonomys.

    Args:
        files: dict mapping relative paths to file contents
        folder_name: name for the uploaded bundle

    Returns:
        dict with cid, sha256, gateway_url, and file_count
    """
    zip_bytes, sha256 = bundle_files_to_zip(files)
    filename = f"{folder_name}.zip"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{AUTONOMYS_API_URL}/api/uploads/file",
            headers={**_headers(), "Content-Type": "application/json"},
            json={"filename": filename, "mimeType": "application/zip", "uploadOptions": None},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
            upload_id = data["id"] if isinstance(data, dict) else data

        total_chunks = max(1, math.ceil(len(zip_bytes) / CHUNK_SIZE))
        for i in range(total_chunks):
            chunk = zip_bytes[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
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
    logger.info(f"uploaded folder {folder_name} ({len(files)} files) -> CID {cid}")
    return {"cid": cid, "sha256": sha256, "gateway_url": gateway_url, "file_count": len(files)}


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


def extract_zip(zip_bytes: bytes) -> dict[str, bytes]:
    """Extract a zip archive into a dict mapping relative paths to file contents.

    Args:
        zip_bytes: raw bytes of the zip file

    Returns:
        dict mapping paths to contents, e.g. {"SKILL.md": b"...", "tools/helper.py": b"..."}
    """
    files = {}
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            files[info.filename] = zf.read(info.filename)
    return files


async def download_folder(cid: str) -> dict[str, bytes]:
    """Download a folder bundle from Autonomys and extract it.

    Returns:
        dict mapping relative paths to file contents
    """
    zip_bytes = await download_file(cid)
    return extract_zip(zip_bytes)


def cid_from_gateway_url(gateway_url: str) -> str | None:
    """Extract CID from a gateway URL like https://gateway.autonomys.xyz/file/<cid>."""
    if not gateway_url:
        return None
    parts = gateway_url.rstrip("/").split("/")
    return parts[-1] if parts else None
