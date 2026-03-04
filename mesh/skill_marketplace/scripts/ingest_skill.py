"""Ingest a skill from a URL, local file, or local directory into the marketplace.

source_type is auto-derived from the URL: github.com and raw.githubusercontent.com
URLs are treated as 'github', everything else as 'web_url'.

Supports folder skills: use --dir to ingest a directory containing SKILL.md and
other files. All files are bundled into a zip and uploaded preserving hierarchy.

Usage:
    python -m mesh.skill_marketplace.scripts.ingest_skill \
        --url https://raw.githubusercontent.com/heurist-network/heurist-mesh-skill/main/SKILL.md \
        --slug heurist-mesh-skill --category infrastructure \
        --source-url https://github.com/heurist-network/heurist-mesh-skill \
        --author '{"display_name": "Heurist Network", "github_username": "heurist-network"}'

    python -m mesh.skill_marketplace.scripts.ingest_skill \
        --dir ./my-skill-folder --slug my-skill --category defi \
        --source-url https://github.com/org/repo
"""

import argparse
import asyncio
import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import get_pool, init_db
from mesh.skill_marketplace.parser import derive_source_type, parse_skill_md
from mesh.skill_marketplace.storage import upload_file, upload_files_individually

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IngestSkill")


async def fetch_url(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.read()


async def ingest(args):
    await init_db()

    is_folder = False
    if args.url:
        logger.info(f"fetching {args.url}")
        raw = await fetch_url(args.url)
        source_url = args.url
    elif args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            logger.error(f"not a directory: {args.dir}")
            sys.exit(1)
        skill_md = dir_path / "SKILL.md"
        if not skill_md.exists():
            logger.error(f"no SKILL.md found in {args.dir}")
            sys.exit(1)
        raw = skill_md.read_bytes()
        source_url = args.source_url
        is_folder = True
    elif args.file:
        logger.info(f"reading {args.file}")
        raw = Path(args.file).read_bytes()
        source_url = args.source_url
    else:
        logger.error("provide --url, --file, or --dir")
        sys.exit(1)

    parsed = parse_skill_md(raw)
    logger.info(f"parsed skill: name={parsed['name']}, description={parsed['description'][:80]}...")

    logger.info("uploading to Autonomys...")
    folder_manifest = None
    if is_folder:
        dir_path = Path(args.dir)
        files = {}
        for file_path in sorted(dir_path.rglob("*")):
            if file_path.is_file():
                relative = file_path.relative_to(dir_path).as_posix()
                files[relative] = file_path.read_bytes()
        logger.info(f"folder skill: {len(files)} files")
        for fp in sorted(files.keys()):
            logger.info(f"  {fp} ({len(files[fp])} bytes)")
        manifest = await upload_files_individually(files, args.slug)
        folder_manifest = {path: info["cid"] for path, info in manifest.items()}
        skill_md_info = manifest.get("SKILL.md", next(iter(manifest.values())))
        file_url = skill_md_info["gateway_url"]
        # TODO: sha256 tracks only SKILL.md for folder skills. Changes to auxiliary files
        # will not be detected by check-updates. Fix: store a composite hash of all files.
        sha256 = skill_md_info["sha256"]
    else:
        result = await upload_file(raw, f"{args.slug}-SKILL.md")
        file_url = result["gateway_url"]
        sha256 = result["sha256"]
    logger.info(f"file_url: {file_url}")
    logger.info(f"SHA256: {sha256}")

    resolved_source_url = args.source_url or source_url
    source_type = args.source_type or derive_source_type(resolved_source_url)
    logger.info(f"source_type: {source_type} (derived from URL)")

    skill_id = uuid.uuid4().hex[:8]

    pool = await get_pool()
    now = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        existing = await conn.fetchval("SELECT id FROM skills WHERE slug = $1", args.slug)
        if existing:
            logger.error(f"slug '{args.slug}' already exists (id={existing})")
            sys.exit(1)

        await conn.execute(
            """INSERT INTO skills (
                id, slug, name, description, skill_md_frontmatter_json,
                category, risk_tier, verification_status,
                source_type, source_url, source_path,
                author_json,
                file_url, approved_sha256, approved_at, approved_by,
                is_folder, folder_manifest_json,
                requires_secrets, requires_private_keys, requires_exchange_api_keys,
                can_sign_transactions, uses_leverage, accesses_user_portfolio,
                created_at, updated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26)""",
            skill_id,
            args.slug,
            parsed["name"],
            parsed["description"],
            json.dumps(parsed["frontmatter"]),
            args.category,
            args.risk_tier,
            "draft",
            source_type,
            resolved_source_url,
            args.source_path,
            json.dumps(json.loads(args.author)) if args.author else None,
            file_url,
            sha256,
            now,
            "admin",
            is_folder,
            json.dumps(folder_manifest) if folder_manifest else None,
            args.requires_secrets,
            args.requires_private_keys,
            args.requires_exchange_api_keys,
            args.can_sign_transactions,
            args.uses_leverage,
            args.accesses_user_portfolio,
            now,
            now,
        )

    logger.info(f"skill '{args.slug}' ingested as draft (id={skill_id})")
    logger.info(f"approve with: python -m mesh.skill_marketplace.scripts.approve_skill --slug {args.slug}")


def main():
    parser = argparse.ArgumentParser(description="Ingest a skill into the marketplace")
    parser.add_argument("--url", help="URL to a SKILL.md file")
    parser.add_argument("--file", help="local path to a SKILL.md file")
    parser.add_argument("--dir", help="local directory containing SKILL.md and other files (folder skill)")
    parser.add_argument("--slug", required=True, help="unique slug for this skill")
    parser.add_argument("--category", help="category (defi, infrastructure, analytics, etc.)")
    parser.add_argument("--risk-tier", dest="risk_tier", help="risk tier (low, medium, high)")
    parser.add_argument("--source-type", dest="source_type", choices=["github", "web_url"],
                        help="override auto-derived source type (auto: github.com/raw.githubusercontent.com → github, else web_url)")
    parser.add_argument("--source-url", dest="source_url", help="source repo URL or file URL")
    parser.add_argument("--source-path", dest="source_path", help="path within repo for multi-skill repos")
    parser.add_argument("--author", help='author JSON string, e.g. \'{"display_name": "x", "github_username": "y"}\'')

    parser.add_argument("--requires-secrets", dest="requires_secrets", action="store_true", default=False)
    parser.add_argument("--requires-private-keys", dest="requires_private_keys", action="store_true", default=False)
    parser.add_argument("--requires-exchange-api-keys", dest="requires_exchange_api_keys", action="store_true", default=False)
    parser.add_argument("--can-sign-transactions", dest="can_sign_transactions", action="store_true", default=False)
    parser.add_argument("--uses-leverage", dest="uses_leverage", action="store_true", default=False)
    parser.add_argument("--accesses-user-portfolio", dest="accesses_user_portfolio", action="store_true", default=False)
    args = parser.parse_args()
    asyncio.run(ingest(args))


if __name__ == "__main__":
    main()
