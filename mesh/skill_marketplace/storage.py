"""Autonomys Auto Drive (ai3.storage) client for skill file storage.

Supports single file and multi-file folder uploads.
Folder skills upload each file individually — no zipping.
Each file gets its own CID. A folder manifest (path -> CID) is stored in PostgreSQL.

Upload protocol: create session → send chunks → complete → returns CID.
Download: tries public gateway first, falls back to authenticated API.
"""

import asyncio
import hashlib
import logging
import math
import mimetypes
import os

import aiohttp

logger = logging.getLogger("SkillMarketplace")

AUTONOMYS_API_KEY = os.getenv("AI3_API_KEY", "")
AUTONOMYS_API_URL = os.getenv("AUTONOMYS_API_URL", "https://mainnet.auto-drive.autonomys.xyz")
AUTONOMYS_GATEWAY_URL = os.getenv("AUTONOMYS_GATEWAY_URL", "https://gateway.autonomys.xyz")

CHUNK_SIZE = 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 15
DOWNLOAD_CONCURRENCY = 8


def _headers():
    return {
        "Authorization": f"Bearer {AUTONOMYS_API_KEY}",
        "X-Auth-Provider": "apikey",
    }


def _mime_type(filename: str) -> str:
    if filename.endswith(".md"):
        return "text/markdown"
    guessed, _ = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"


async def _upload_single(session: aiohttp.ClientSession, content: bytes, filename: str) -> str:
    """Upload one file via the 3-step Autonomys protocol. Returns CID."""
    async with session.post(
        f"{AUTONOMYS_API_URL}/api/uploads/file",
        headers={**_headers(), "Content-Type": "application/json"},
        json={"filename": filename, "mimeType": _mime_type(filename), "uploadOptions": None},
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
        return result["cid"] if isinstance(result, dict) else result


async def upload_file(content: bytes, filename: str) -> dict:
    """Upload a single file to Autonomys DSN. Returns cid, sha256, gateway_url."""
    sha256 = hashlib.sha256(content).hexdigest()
    async with aiohttp.ClientSession() as session:
        cid = await _upload_single(session, content, filename)
    gateway_url = f"{AUTONOMYS_GATEWAY_URL}/file/{cid}"
    logger.info(f"uploaded {filename} -> CID {cid}")
    return {"cid": cid, "sha256": sha256, "gateway_url": gateway_url}


async def upload_files_individually(files: dict[str, bytes], folder_name: str) -> dict[str, dict]:
    """Upload each file in a folder skill individually to Autonomys.

    Each file gets its own CID. No zipping.
    The returned manifest is stored in folder_manifest_json in PostgreSQL.

    Args:
        files: dict mapping relative paths to file contents
               e.g. {"SKILL.md": b"...", "tools/helper.py": b"..."}
        folder_name: used for logging only

    Returns:
        dict mapping relative paths to {cid, sha256, gateway_url}
        e.g. {"SKILL.md": {"cid": "bafk...", "sha256": "...", "gateway_url": "..."}}
    """
    manifest = {}
    async with aiohttp.ClientSession() as session:
        for rel_path, content in sorted(files.items()):
            filename = rel_path.split("/")[-1]
            sha256 = hashlib.sha256(content).hexdigest()
            cid = await _upload_single(session, content, filename)
            gateway_url = f"{AUTONOMYS_GATEWAY_URL}/file/{cid}"
            manifest[rel_path] = {"cid": cid, "sha256": sha256, "gateway_url": gateway_url}
            logger.info(f"uploaded {folder_name}/{rel_path} -> CID {cid}")
    logger.info(f"folder {folder_name}: {len(manifest)} files uploaded individually")
    return manifest


async def prepare_skill_artifact(raw: bytes, slug: str, folder_files: dict[str, bytes] | None = None) -> dict:
    """Upload skill files to Autonomys and return a normalized artifact record.

    For folder skills (folder_files with >1 file): uploads each file individually,
    each gets its own CID.
    For single-file skills: uploads raw as SKILL.md.

    Returns:
        {file_url, sha256, is_folder, folder_manifest}
        folder_manifest is {path: cid} for folder skills, None otherwise.
    """
    if folder_files and len(folder_files) > 1:
        manifest = await upload_files_individually(folder_files, slug)
        skill_md_info = manifest.get("SKILL.md", next(iter(manifest.values())))
        return {
            "file_url": skill_md_info["gateway_url"],
            # TODO: sha256 tracks only SKILL.md for folder skills. Changes to auxiliary files
            # will not be detected by check-updates. Fix: store a composite hash of all files.
            "sha256": skill_md_info["sha256"],
            "is_folder": True,
            "folder_manifest": {path: info["cid"] for path, info in manifest.items()},
        }
    else:
        result = await upload_file(raw, f"{slug}-SKILL.md")
        return {
            "file_url": result["gateway_url"],
            "sha256": result["sha256"],
            "is_folder": False,
            "folder_manifest": None,
        }


async def _download_file_with_session(session: aiohttp.ClientSession, cid: str) -> bytes:
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


async def download_file(cid: str) -> bytes:
    """Download a file from Autonomys by CID. Tries public gateway first."""
    timeout = aiohttp.ClientTimeout(total=DOWNLOAD_TIMEOUT_SECONDS)
    connector = aiohttp.TCPConnector(limit=DOWNLOAD_CONCURRENCY)
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        return await _download_file_with_session(session, cid)


async def download_files(cids_by_path: dict[str, str]) -> dict[str, bytes]:
    """Download multiple files concurrently from Autonomys.

    Uses a shared session plus bounded concurrency so folder skill downloads do
    not serialize dozens of network round trips.
    """
    timeout = aiohttp.ClientTimeout(total=DOWNLOAD_TIMEOUT_SECONDS)
    connector = aiohttp.TCPConnector(limit=DOWNLOAD_CONCURRENCY)
    semaphore = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)

    async def fetch_one(path: str, cid: str) -> tuple[str, bytes]:
        async with semaphore:
            return path, await _download_file_with_session(session, cid)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        results = await asyncio.gather(
            *(fetch_one(path, cid) for path, cid in cids_by_path.items())
        )
    return dict(results)


def cid_from_gateway_url(gateway_url: str) -> str | None:
    """Extract CID from a gateway URL like https://gateway.autonomys.xyz/file/<cid>."""
    if not gateway_url:
        return None
    parts = gateway_url.rstrip("/").split("/")
    return parts[-1] if parts else None
