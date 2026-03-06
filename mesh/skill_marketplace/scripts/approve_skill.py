"""Approve a draft skill, setting verification_status to 'verified'.

Usage:
    python -m mesh.skill_marketplace.scripts.approve_skill --slug xapi
    python -m mesh.skill_marketplace.scripts.approve_skill --slug xapi --by "admin-name"
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import get_pool, init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ApproveSkill")


async def approve(args):
    await init_db()
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug, name, verification_status FROM skills WHERE slug = $1", args.slug)
        if not row:
            logger.error(f"skill '{args.slug}' not found")
            sys.exit(1)

        if row["verification_status"] == "verified":
            logger.info(f"skill '{args.slug}' is already verified")
            return

        now = datetime.now(timezone.utc)
        await conn.execute(
            """UPDATE skills
               SET verification_status = 'verified', approved_by = $1, approved_at = $2, updated_at = $3
               WHERE slug = $4""",
            args.by, now, now, args.slug,
        )

    logger.info(f"skill '{args.slug}' ({row['name']}) -> verified by {args.by}")


def main():
    parser = argparse.ArgumentParser(description="Approve a draft skill")
    parser.add_argument("--slug", required=True, help="skill slug to approve")
    parser.add_argument("--by", default="admin", help="approver name (default: admin)")
    args = parser.parse_args()
    asyncio.run(approve(args))


if __name__ == "__main__":
    main()
