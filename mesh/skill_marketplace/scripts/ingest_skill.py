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

from mesh.skill_marketplace.db import get_pool, init_db, insert_skill_draft
from mesh.skill_marketplace.parser import (
    derive_source_type,
    fetch_github_folder_files,
    is_ignored_skill_path,
    parse_skill_md,
)
from mesh.skill_marketplace.storage import prepare_skill_artifact
from mesh.skill_marketplace.taxonomy import normalize_category, normalize_labels

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
    gh_folder = None
    if args.url:
        logger.info(f"fetching {args.url}")
        raw = await fetch_url(args.url)
        source_url = args.url
        gh_folder = await fetch_github_folder_files(args.url, args.source_path)
        if gh_folder:
            is_folder = True
            logger.info(f"detected GitHub folder skill: {len(gh_folder)} files")
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
    folder_files = None
    if is_folder and args.dir:
        dir_path = Path(args.dir)
        folder_files = {}
        for file_path in sorted(dir_path.rglob("*")):
            if file_path.is_file():
                relative = file_path.relative_to(dir_path).as_posix()
                if is_ignored_skill_path(relative):
                    continue
                folder_files[relative] = file_path.read_bytes()
        logger.info(f"folder skill: {len(folder_files)} files")
        for fp in sorted(folder_files.keys()):
            logger.info(f"  {fp} ({len(folder_files[fp])} bytes)")
    elif is_folder and gh_folder:
        folder_files = gh_folder
        logger.info(f"folder skill (GitHub): {len(folder_files)} files")
        for fp in sorted(folder_files.keys()):
            logger.info(f"  {fp} ({len(folder_files[fp])} bytes)")

    artifact = await prepare_skill_artifact(raw, args.slug, folder_files)
    logger.info(f"file_url: {artifact['file_url']}")
    logger.info(f"SHA256: {artifact['sha256']}, is_folder: {artifact['is_folder']}")

    resolved_source_url = args.source_url or source_url
    source_type = args.source_type or derive_source_type(resolved_source_url)
    logger.info(f"source_type: {source_type} (derived from URL)")

    skill_id = uuid.uuid4().hex[:8]
    pool = await get_pool()
    now = datetime.now(timezone.utc)

    folder_manifest = artifact.get("folder_manifest")
    folder_manifest_json = json.dumps(folder_manifest) if folder_manifest else None
    labels = normalize_labels(args.label)
    category = normalize_category(args.category)
    author_json = json.dumps(json.loads(args.author)) if args.author else None
    frontmatter = parsed["frontmatter"]
    if isinstance(frontmatter, dict):
        frontmatter = json.dumps(frontmatter)

    async with pool.acquire() as conn:
        existing = await conn.fetchval("SELECT id FROM skills WHERE slug = $1", args.slug)

        if existing and args.update:
            await conn.execute(
                """UPDATE skills SET
                    name = $1, description = $2, skill_md_frontmatter_json = $3,
                    category = $4, labels = $5, risk_tier = $6,
                    source_type = $7, source_url = $8, source_path = $9, author_json = $10,
                    file_url = $11, approved_sha256 = $12, is_folder = $13, folder_manifest_json = $14,
                    external_api_dependencies = $15,
                    requires_secrets = $16, requires_private_keys = $17, requires_exchange_api_keys = $18,
                    can_sign_transactions = $19, uses_leverage = $20, accesses_user_portfolio = $21,
                    verification_status = 'draft', updated_at = $22
                WHERE slug = $23""",
                parsed["name"], parsed["description"], frontmatter,
                category, labels, args.risk_tier,
                source_type, resolved_source_url, args.source_path, author_json,
                artifact["file_url"], artifact["sha256"], artifact.get("is_folder", False), folder_manifest_json,
                args.external_api_dependency or [],
                args.requires_secrets, args.requires_private_keys, args.requires_exchange_api_keys,
                args.can_sign_transactions, args.uses_leverage, args.accesses_user_portfolio,
                now, args.slug,
            )
            logger.info(f"skill '{args.slug}' updated in place (id={existing}), reset to draft")
            logger.info(f"approve with: python -m mesh.skill_marketplace.scripts.approve_skill --slug {args.slug}")
            return

        if existing:
            logger.error(f"slug '{args.slug}' already exists (id={existing}). Use --update to update in place.")
            sys.exit(1)

        await insert_skill_draft(conn, {
            "id": skill_id,
            "slug": args.slug,
            "name": parsed["name"],
            "description": parsed["description"],
            "skill_md_frontmatter_json": parsed["frontmatter"],
            "category": category,
            "labels": labels,
            "risk_tier": args.risk_tier,
            "source_type": source_type,
            "source_url": resolved_source_url,
            "source_path": args.source_path,
            "author_json": json.loads(args.author) if args.author else None,
            "external_api_dependencies": args.external_api_dependency,
            **artifact,
            "approved_by": "admin",
            "requires_secrets": args.requires_secrets,
            "requires_private_keys": args.requires_private_keys,
            "requires_exchange_api_keys": args.requires_exchange_api_keys,
            "can_sign_transactions": args.can_sign_transactions,
            "uses_leverage": args.uses_leverage,
            "accesses_user_portfolio": args.accesses_user_portfolio,
            "created_at": now,
        })

    logger.info(f"skill '{args.slug}' ingested as draft (id={skill_id})")
    logger.info(f"approve with: python -m mesh.skill_marketplace.scripts.approve_skill --slug {args.slug}")


def main():
    parser = argparse.ArgumentParser(description="Ingest a skill into the marketplace")
    parser.add_argument("--url", help="URL to a SKILL.md file")
    parser.add_argument("--file", help="local path to a SKILL.md file")
    parser.add_argument("--dir", help="local directory containing SKILL.md and other files (folder skill)")
    parser.add_argument("--slug", required=True, help="unique slug for this skill")
    parser.add_argument("--category", required=True,
                        help="category name, e.g. Stocks, Macro, Crypto, Developer, Social")
    parser.add_argument("--label", action="append", default=[],
                        help="repeatable secondary label, e.g. --label analytics --label options")
    parser.add_argument("--risk-tier", dest="risk_tier", help="risk tier (low, medium, high)")
    parser.add_argument("--source-type", dest="source_type", choices=["github", "web_url"],
                        help="override auto-derived source type (auto: github.com/raw.githubusercontent.com → github, else web_url)")
    parser.add_argument("--source-url", dest="source_url", help="source repo URL or file URL")
    parser.add_argument("--source-path", dest="source_path", help="path within repo for multi-skill repos")
    parser.add_argument("--author", help='author JSON string, e.g. \'{"display_name": "x", "github_username": "y"}\'')
    parser.add_argument("--external-api-dependency", dest="external_api_dependency", action="append", default=[],
                        help="repeatable external API dependency name, e.g. --external-api-dependency CoinGecko")

    parser.add_argument("--update", action="store_true", default=False,
                        help="update existing skill in place instead of failing on duplicate slug (preserves id, download_count, star_count, created_at)")
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
