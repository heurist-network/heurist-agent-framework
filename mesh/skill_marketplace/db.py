"""Skill marketplace database setup and connection pool using asyncpg."""

import logging
import os

import ssl as _ssl

import asyncpg
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("SkillMarketplace")

DATABASE_URL = os.getenv(
    "SKILLS_DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/skills_marketplace",
)

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        ctx = _ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = _ssl.CERT_NONE
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10, ssl=ctx)
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


CREATE_SKILLS_TABLE = """
CREATE TABLE IF NOT EXISTS skills (
    id              VARCHAR(8) PRIMARY KEY,
    slug            VARCHAR(128) UNIQUE NOT NULL,
    name            VARCHAR(64) NOT NULL,
    description     VARCHAR(1024) NOT NULL,
    skill_md_frontmatter_json JSONB,
    category        VARCHAR(64),
    risk_tier       VARCHAR(32),
    verification_status VARCHAR(16) NOT NULL DEFAULT 'draft',
    source_type     VARCHAR(16),
    source_url      VARCHAR(512),
    source_path     VARCHAR(512),
    author_json     JSONB,
    file_url        VARCHAR(512),
    is_folder       BOOLEAN NOT NULL DEFAULT FALSE,
    folder_manifest_json JSONB,
    approved_sha256 VARCHAR(64),
    approved_at     TIMESTAMPTZ,
    approved_by     VARCHAR(128),
    submitted_by    VARCHAR(128),
    submitted_at    TIMESTAMPTZ,
    review_state    VARCHAR(32),
    review_notes    TEXT,
    reviewed_at     TIMESTAMPTZ,
    requires_secrets          BOOLEAN NOT NULL DEFAULT FALSE,
    requires_private_keys     BOOLEAN NOT NULL DEFAULT FALSE,
    requires_exchange_api_keys BOOLEAN NOT NULL DEFAULT FALSE,
    can_sign_transactions     BOOLEAN NOT NULL DEFAULT FALSE,
    uses_leverage             BOOLEAN NOT NULL DEFAULT FALSE,
    accesses_user_portfolio   BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_skills_slug ON skills (slug);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills (category);
CREATE INDEX IF NOT EXISTS idx_skills_verification ON skills (verification_status);
"""


MIGRATIONS = [
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS is_folder BOOLEAN NOT NULL DEFAULT FALSE",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS folder_manifest_json JSONB",
]


async def init_db():
    """Create the skills table and indexes if they don't exist. Run migrations."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_SKILLS_TABLE)
        for migration in MIGRATIONS:
            await conn.execute(migration)
    logger.info("skills table ready")
