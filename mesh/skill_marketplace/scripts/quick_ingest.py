"""Quick one-shot ingest script that uses direct connection instead of pool."""

import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiohttp
import asyncpg
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import insert_skill_draft
from mesh.skill_marketplace.parser import parse_skill_md
from mesh.skill_marketplace.storage import prepare_skill_artifact

DB_URL = os.getenv("SKILLS_DATABASE_URL")


async def main():
    # Fetch SKILL.md
    print("fetching SKILL.md...")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://raw.githubusercontent.com/heurist-network/heurist-mesh-skill/main/SKILL.md"
        ) as resp:
            raw = await resp.read()
    parsed = parse_skill_md(raw)
    print(f"parsed: {parsed['name']}")

    # Upload to Autonomys
    print("uploading to Autonomys...")
    artifact = await prepare_skill_artifact(raw, "heurist-mesh-skill")
    print(f"file_url: {artifact['file_url']}")
    print(f"sha256: {artifact['sha256']}")

    # Direct connection (no pool)
    print("connecting to DB...")
    conn = await asyncpg.connect(DB_URL, timeout=60)

    # Clean slate
    await conn.execute("DELETE FROM skills WHERE slug = $1", "heurist-mesh-skill")

    skill_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)

    await insert_skill_draft(conn, {
        "id": skill_id,
        "slug": "heurist-mesh-skill",
        "name": parsed["name"],
        "description": parsed["description"],
        "skill_md_frontmatter_json": parsed["frontmatter"],
        "category": "infrastructure",
        "risk_tier": "low",
        "source_type": "github",
        "source_url": "https://github.com/heurist-network/heurist-mesh-skill",
        "source_path": None,
        "author_json": {"display_name": "Heurist Network", "github_username": "heurist-network"},
        **artifact,
        "approved_by": "admin",
        "requires_secrets": True,
        "requires_private_keys": False,
        "requires_exchange_api_keys": False,
        "can_sign_transactions": False,
        "uses_leverage": False,
        "accesses_user_portfolio": False,
        "created_at": now,
    })
    print(f"ingested as draft (id={skill_id})")

    # Approve
    await conn.execute(
        "UPDATE skills SET verification_status = 'verified', approved_by = 'admin', approved_at = $1, updated_at = $1 WHERE slug = $2",
        now, "heurist-mesh-skill",
    )
    print("approved -> verified")

    # Verify
    row = await conn.fetchrow(
        "SELECT id, slug, name, verification_status, file_url, is_folder, requires_secrets FROM skills WHERE slug = $1",
        "heurist-mesh-skill",
    )
    print(f"done: id={row['id']}, status={row['verification_status']}, is_folder={row['is_folder']}")
    print(f"  file_url={row['file_url']}")
    print(f"  requires_secrets={row['requires_secrets']}")

    await conn.close()


asyncio.run(main())
