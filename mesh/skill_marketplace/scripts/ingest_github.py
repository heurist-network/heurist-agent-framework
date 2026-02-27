"""Ingest skill(s) from a GitHub repository.

Supports two modes:
1. Single skill: point at a repo + path to ingest one SKILL.md
2. Scan mode: scan a repo for all SKILL.md files in subdirectories

Usage:
    python -m mesh.skill_marketplace.scripts.ingest_github \
        --repo heurist-network/heurist-mesh-skill \
        --slug heurist-mesh-skill --category infrastructure

    python -m mesh.skill_marketplace.scripts.ingest_github \
        --repo heurist-network/heurist-mesh-skill --path skills/defi/SKILL.md \
        --slug defi-skill --category defi

    python -m mesh.skill_marketplace.scripts.ingest_github \
        --repo heurist-network/heurist-mesh-skill --scan --category infrastructure
"""

import argparse
import asyncio
import hashlib
import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import get_pool, init_db
from mesh.skill_marketplace.parser import parse_skill_md
from mesh.skill_marketplace.storage import upload_file, upload_folder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IngestGitHub")

GITHUB_API = "https://api.github.com"


async def fetch_github_file(session: aiohttp.ClientSession, owner: str, repo: str, path: str, token: str | None) -> bytes | None:
    """Fetch raw file content from GitHub API."""
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            logger.error(f"GitHub API returned {resp.status} for {owner}/{repo}/{path}")
            return None
        return await resp.read()


async def scan_for_skill_files(session: aiohttp.ClientSession, owner: str, repo: str, token: str | None) -> list[str]:
    """Recursively scan a GitHub repo for SKILL.md files using the Git tree API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            logger.error(f"GitHub tree API returned {resp.status}")
            return []
        data = await resp.json()

    return [item["path"] for item in data.get("tree", []) if item["path"].endswith("SKILL.md")]


async def fetch_folder_files(session: aiohttp.ClientSession, owner: str, repo: str, folder_path: str, token: str | None) -> dict[str, bytes]:
    """Fetch all files in a GitHub folder, preserving hierarchy relative to folder_path.

    Returns dict mapping relative paths to file contents.
    """
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            logger.error(f"GitHub tree API returned {resp.status}")
            return {}
        data = await resp.json()

    prefix = folder_path.rstrip("/") + "/"
    file_paths = [
        item["path"] for item in data.get("tree", [])
        if item["type"] == "blob" and item["path"].startswith(prefix)
    ]

    if not file_paths:
        return {}

    files = {}
    for file_path in file_paths:
        content = await fetch_github_file(session, owner, repo, file_path, token)
        if content is not None:
            relative_path = file_path[len(prefix):]
            files[relative_path] = content

    return files


async def ingest_one(session: aiohttp.ClientSession, pool, owner: str, repo: str, path: str, slug: str, args, token: str | None):
    """Ingest a skill from GitHub. If the SKILL.md is inside a folder with other files, uploads the entire folder as a zip bundle."""
    raw = await fetch_github_file(session, owner, repo, path, token)
    if not raw:
        return False

    parsed = parse_skill_md(raw)
    logger.info(f"[{slug}] parsed: name={parsed['name']}, description={parsed['description'][:60]}...")

    folder_path = str(Path(path).parent)
    if folder_path != ".":
        folder_files = await fetch_folder_files(session, owner, repo, folder_path, token)
        if len(folder_files) > 1:
            logger.info(f"[{slug}] folder skill detected: {len(folder_files)} files in {folder_path}/")
            for fp in sorted(folder_files.keys()):
                logger.info(f"  {fp} ({len(folder_files[fp])} bytes)")
            result = await upload_folder(folder_files, slug)
            logger.info(f"[{slug}] uploaded folder bundle: {result['gateway_url']}")
        else:
            result = await upload_file(raw, f"{slug}-SKILL.md")
            logger.info(f"[{slug}] uploaded: {result['gateway_url']}")
    else:
        result = await upload_file(raw, f"{slug}-SKILL.md")
        logger.info(f"[{slug}] uploaded: {result['gateway_url']}")

    skill_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)
    source_url = f"https://github.com/{owner}/{repo}"
    source_path = path if path != "SKILL.md" else None

    author_json = json.dumps(json.loads(args.author)) if args.author else None

    async with pool.acquire() as conn:
        existing = await conn.fetchval("SELECT id FROM skills WHERE slug = $1", slug)
        if existing:
            logger.warning(f"[{slug}] already exists (id={existing}), skipping")
            return False

        await conn.execute(
            """INSERT INTO skills (
                id, slug, name, description, skill_md_frontmatter_json,
                category, risk_tier, verification_status,
                source_type, source_url, source_path, author_json,
                file_url, approved_sha256, approved_at, approved_by,
                requires_secrets, requires_private_keys, requires_exchange_api_keys,
                can_sign_transactions, uses_leverage, accesses_user_portfolio,
                created_at, updated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24)""",
            skill_id,
            slug,
            parsed["name"],
            parsed["description"],
            json.dumps(parsed["frontmatter"]),
            args.category,
            args.risk_tier,
            "draft",
            "github",
            source_url,
            source_path,
            author_json,
            result["gateway_url"],
            result["sha256"],
            now,
            "admin",
            args.requires_secrets,
            args.requires_private_keys,
            args.requires_exchange_api_keys,
            args.can_sign_transactions,
            args.uses_leverage,
            args.accesses_user_portfolio,
            now,
            now,
        )

    logger.info(f"[{slug}] ingested as draft (id={skill_id})")
    return True


async def run(args):
    import os
    token = os.getenv("GITHUB_TOKEN")

    parts = args.repo.strip("/").split("/")
    if len(parts) != 2:
        logger.error("--repo must be in owner/repo format (e.g. heurist-network/heurist-mesh-skill)")
        sys.exit(1)
    owner, repo = parts

    await init_db()
    pool = await get_pool()

    async with aiohttp.ClientSession() as session:
        if args.scan:
            logger.info(f"scanning {owner}/{repo} for SKILL.md files...")
            paths = await scan_for_skill_files(session, owner, repo, token)
            if not paths:
                logger.info("no SKILL.md files found")
                return

            logger.info(f"found {len(paths)} SKILL.md file(s): {paths}")
            ingested = 0
            for path in paths:
                folder = Path(path).parent.name if Path(path).parent.name != "." else repo
                slug = args.slug_prefix + "-" + folder if args.slug_prefix else folder
                ok = await ingest_one(session, pool, owner, repo, path, slug, args, token)
                if ok:
                    ingested += 1
            logger.info(f"scan complete: {ingested}/{len(paths)} skills ingested")
        else:
            path = args.path or "SKILL.md"
            if not args.slug:
                logger.error("--slug is required in single-skill mode")
                sys.exit(1)
            await ingest_one(session, pool, owner, repo, path, args.slug, args, token)


def main():
    parser = argparse.ArgumentParser(description="Ingest skill(s) from a GitHub repository")
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/repo format")
    parser.add_argument("--path", help="path to SKILL.md within the repo (default: SKILL.md)")
    parser.add_argument("--slug", help="unique slug for the skill (required in single mode)")
    parser.add_argument("--scan", action="store_true", default=False,
                        help="scan repo for all SKILL.md files and ingest each one")
    parser.add_argument("--slug-prefix", dest="slug_prefix", help="prefix for auto-generated slugs in scan mode")
    parser.add_argument("--category", help="category for ingested skills")
    parser.add_argument("--risk-tier", dest="risk_tier", help="risk tier (low, medium, high)")
    parser.add_argument("--author", help='author JSON string')

    parser.add_argument("--requires-secrets", dest="requires_secrets", action="store_true", default=False)
    parser.add_argument("--requires-private-keys", dest="requires_private_keys", action="store_true", default=False)
    parser.add_argument("--requires-exchange-api-keys", dest="requires_exchange_api_keys", action="store_true", default=False)
    parser.add_argument("--can-sign-transactions", dest="can_sign_transactions", action="store_true", default=False)
    parser.add_argument("--uses-leverage", dest="uses_leverage", action="store_true", default=False)
    parser.add_argument("--accesses-user-portfolio", dest="accesses_user_portfolio", action="store_true", default=False)
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
