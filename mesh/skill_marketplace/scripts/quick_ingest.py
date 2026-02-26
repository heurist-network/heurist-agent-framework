"""Quick one-shot ingest script that uses direct connection instead of pool."""

import asyncio
import json
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

from mesh.skill_marketplace.parser import parse_skill_md
from mesh.skill_marketplace.storage import upload_file

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
    result = await upload_file(raw, "heurist-mesh-skill-SKILL.md")
    print(f"file_url: {result['gateway_url']}")
    print(f"sha256: {result['sha256']}")

    # Direct connection (no pool)
    print("connecting to DB...")
    conn = await asyncpg.connect(DB_URL, timeout=60)

    # Clean slate
    await conn.execute("DELETE FROM skills WHERE slug = $1", "heurist-mesh-skill")

    skill_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)

    await conn.execute(
        """INSERT INTO skills (
            id, slug, name, description, skill_md_frontmatter_json,
            category, risk_tier, verification_status,
            source_type, source_url, source_path,
            author_display_name, author_github_url,
            file_url, approved_sha256, approved_at, approved_by,
            requires_secrets, requires_private_keys, requires_exchange_api_keys,
            can_sign_transactions, uses_leverage, accesses_user_portfolio,
            created_at, updated_at
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25)""",
        skill_id,
        "heurist-mesh-skill",
        parsed["name"],
        parsed["description"],
        json.dumps(parsed["frontmatter"]),
        "infrastructure",
        "low",
        "draft",
        "github",
        "https://github.com/heurist-network/heurist-mesh-skill",
        None,
        "Heurist Network",
        "https://github.com/heurist-network",
        result["gateway_url"],
        result["sha256"],
        now,
        "admin",
        True,   # requires_secrets
        True,   # requires_private_keys
        False,  # requires_exchange_api_keys
        False,  # can_sign_transactions
        False,  # uses_leverage
        True,   # accesses_user_portfolio
        now,
        now,
    )
    print(f"ingested as draft (id={skill_id})")

    # Approve
    await conn.execute(
        "UPDATE skills SET verification_status = 'verified', approved_by = 'admin', approved_at = $1, updated_at = $1 WHERE slug = $2",
        now,
        "heurist-mesh-skill",
    )
    print("approved -> verified")

    # Verify
    row = await conn.fetchrow(
        "SELECT id, slug, name, verification_status, file_url, requires_secrets, accesses_user_portfolio FROM skills WHERE slug = $1",
        "heurist-mesh-skill",
    )
    print(f"done: id={row['id']}, status={row['verification_status']}")
    print(f"  file_url={row['file_url']}")
    print(f"  requires_secrets={row['requires_secrets']}, accesses_user_portfolio={row['accesses_user_portfolio']}")

    await conn.close()


asyncio.run(main())
