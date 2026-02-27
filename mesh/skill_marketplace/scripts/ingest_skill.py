"""Ingest a skill from a URL or local file into the marketplace.

Usage:
    python -m mesh.skill_marketplace.scripts.ingest_skill \
        --url https://raw.githubusercontent.com/heurist-network/heurist-mesh-skill/main/SKILL.md \
        --slug heurist-mesh-skill --category infrastructure --source-type github \
        --source-url https://github.com/heurist-network/heurist-mesh-skill \
        --author '{"display_name": "Heurist Network", "github_username": "heurist-network"}'

    python -m mesh.skill_marketplace.scripts.ingest_skill \
        --file ./SKILL.md --slug heurist-mesh-skill --category infrastructure --source-type github \
        --source-url https://github.com/heurist-network/heurist-mesh-skill
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
from mesh.skill_marketplace.parser import parse_skill_md
from mesh.skill_marketplace.storage import upload_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IngestSkill")


async def fetch_url(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.read()


async def ingest(args):
    await init_db()

    if args.url:
        logger.info(f"fetching {args.url}")
        raw = await fetch_url(args.url)
        source_url = args.url
    elif args.file:
        logger.info(f"reading {args.file}")
        raw = Path(args.file).read_bytes()
        source_url = args.source_url
    else:
        logger.error("provide --url or --file")
        sys.exit(1)

    parsed = parse_skill_md(raw)
    logger.info(f"parsed skill: name={parsed['name']}, description={parsed['description'][:80]}...")

    logger.info("uploading to Autonomys...")
    result = await upload_file(raw, f"{args.slug}-SKILL.md")
    logger.info(f"file_url: {result['gateway_url']}")
    logger.info(f"SHA256: {result['sha256']}")

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
                requires_secrets, requires_private_keys, requires_exchange_api_keys,
                can_sign_transactions, uses_leverage, accesses_user_portfolio,
                created_at, updated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24)""",
            skill_id,
            args.slug,
            parsed["name"],
            parsed["description"],
            json.dumps(parsed["frontmatter"]),
            args.category,
            args.risk_tier,
            "draft",
            args.source_type,
            source_url,
            args.source_path,
            json.dumps(json.loads(args.author)) if args.author else None,
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

    logger.info(f"skill '{args.slug}' ingested as draft (id={skill_id})")
    logger.info(f"approve with: python -m mesh.skill_marketplace.scripts.approve_skill --slug {args.slug}")


def main():
    parser = argparse.ArgumentParser(description="Ingest a skill into the marketplace")
    parser.add_argument("--url", help="URL to a SKILL.md file")
    parser.add_argument("--file", help="local path to a SKILL.md file")
    parser.add_argument("--slug", required=True, help="unique slug for this skill")
    parser.add_argument("--category", help="category (defi, infrastructure, analytics, etc.)")
    parser.add_argument("--risk-tier", dest="risk_tier", help="risk tier (low, medium, high)")
    parser.add_argument("--source-type", dest="source_type", choices=["github", "web_url"])
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
