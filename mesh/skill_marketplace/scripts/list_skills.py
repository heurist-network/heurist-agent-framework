"""
Admin script: List all skills in the database.

Usage:
    python -m mesh.skill_marketplace.scripts.list_skills
    python -m mesh.skill_marketplace.scripts.list_skills --status draft
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import get_pool, init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ListSkills")


async def list_skills(args):
    await init_db()
    pool = await get_pool()

    query = "SELECT id, slug, name, category, risk_tier, verification_status, author_display_name FROM skills"
    params = []

    if args.status:
        query += " WHERE verification_status = $1"
        params.append(args.status)

    query += " ORDER BY created_at DESC"

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    if not rows:
        print("No skills found.")
        return

    print(f"\n{'ID':<10} {'Slug':<25} {'Name':<25} {'Category':<15} {'Risk':<10} {'Status':<12} {'Author'}")
    print("-" * 120)
    for r in rows:
        author = r["author_display_name"] or "—"
        print(f"{r['id']:<10} {r['slug']:<25} {r['name']:<25} {r['category'] or '—':<15} {r['risk_tier'] or '—':<10} {r['verification_status']:<12} {author}")

    print(f"\nTotal: {len(rows)} skills")


def main():
    parser = argparse.ArgumentParser(description="List skills in the marketplace DB")
    parser.add_argument("--status", choices=["draft", "verified", "archived"], help="filter by status")
    args = parser.parse_args()
    asyncio.run(list_skills(args))


if __name__ == "__main__":
    main()
