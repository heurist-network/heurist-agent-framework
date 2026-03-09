"""Skill marketplace database setup and connection pool using asyncpg."""

import json
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
    labels          TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    risk_tier       VARCHAR(32),
    verification_status VARCHAR(16) NOT NULL DEFAULT 'draft',
    source_type     VARCHAR(16),
    source_url      VARCHAR(512),
    source_path     VARCHAR(512),
    author_json     JSONB,
    file_url        VARCHAR(512),
    is_folder       BOOLEAN NOT NULL DEFAULT FALSE,
    folder_manifest_json JSONB,
    external_api_dependencies TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    reference_urls  TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    download_count  BIGINT NOT NULL DEFAULT 0,
    star_count      BIGINT NOT NULL DEFAULT 0,
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
CREATE INDEX IF NOT EXISTS idx_skills_created_at ON skills (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_skills_updated_at ON skills (updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_skills_download_count ON skills (download_count DESC);
CREATE INDEX IF NOT EXISTS idx_skills_star_count ON skills (star_count DESC);
CREATE INDEX IF NOT EXISTS idx_skills_name ON skills (name);
"""


MIGRATIONS = [
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS labels TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[]",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS is_folder BOOLEAN NOT NULL DEFAULT FALSE",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS folder_manifest_json JSONB",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS external_api_dependencies TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[]",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS reference_urls TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[]",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS download_count BIGINT NOT NULL DEFAULT 0",
    "ALTER TABLE skills ADD COLUMN IF NOT EXISTS star_count BIGINT NOT NULL DEFAULT 0",
    "CREATE INDEX IF NOT EXISTS idx_skills_labels ON skills USING GIN (labels)",
    "CREATE INDEX IF NOT EXISTS idx_skills_created_at ON skills (created_at DESC)",
    "CREATE INDEX IF NOT EXISTS idx_skills_updated_at ON skills (updated_at DESC)",
    "CREATE INDEX IF NOT EXISTS idx_skills_download_count ON skills (download_count DESC)",
    "CREATE INDEX IF NOT EXISTS idx_skills_star_count ON skills (star_count DESC)",
    "CREATE INDEX IF NOT EXISTS idx_skills_name ON skills (name)",
]


async def insert_skill_draft(conn, draft: dict) -> None:
    """Insert a new skill row as draft. Single source of truth for the INSERT schema.

    draft keys:
        id, slug, name, description, skill_md_frontmatter_json (JSON string or dict),
        category, labels, risk_tier, source_type, source_url, source_path, author_json (JSON string or dict),
        file_url, sha256, approved_by, is_folder, folder_manifest ({path:cid} dict or None),
        external_api_dependencies (list[str] or None),
        reference_urls (list[str] or None),
        requires_secrets, requires_private_keys, requires_exchange_api_keys,
        can_sign_transactions, uses_leverage, accesses_user_portfolio, created_at
    """
    frontmatter = draft["skill_md_frontmatter_json"]
    if isinstance(frontmatter, dict):
        frontmatter = json.dumps(frontmatter)

    author = draft.get("author_json")
    if isinstance(author, dict):
        author = json.dumps(author)

    folder_manifest = draft.get("folder_manifest")
    folder_manifest_json = json.dumps(folder_manifest) if folder_manifest else None
    labels = draft.get("labels") or []
    external_api_dependencies = draft.get("external_api_dependencies") or []
    reference_urls = draft.get("reference_urls") or []

    now = draft["created_at"]
    await conn.execute(
        """INSERT INTO skills (
            id, slug, name, description, skill_md_frontmatter_json,
            category, labels, risk_tier, verification_status,
            source_type, source_url, source_path, author_json,
            file_url, approved_sha256, approved_at, approved_by,
            is_folder, folder_manifest_json, external_api_dependencies,
            reference_urls,
            requires_secrets, requires_private_keys, requires_exchange_api_keys,
            can_sign_transactions, uses_leverage, accesses_user_portfolio,
            created_at, updated_at
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29)""",
        draft["id"], draft["slug"], draft["name"], draft["description"],
        frontmatter, draft.get("category"), labels, draft.get("risk_tier"), "draft",
        draft.get("source_type"), draft.get("source_url"), draft.get("source_path"),
        author,
        draft["file_url"], draft["sha256"], now, draft.get("approved_by", "admin"),
        draft.get("is_folder", False), folder_manifest_json, external_api_dependencies, reference_urls,
        draft.get("requires_secrets", False), draft.get("requires_private_keys", False),
        draft.get("requires_exchange_api_keys", False), draft.get("can_sign_transactions", False),
        draft.get("uses_leverage", False), draft.get("accesses_user_portfolio", False),
        now, now,
    )


async def init_db():
    """Create the skills table and indexes if they don't exist. Run migrations."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_SKILLS_TABLE)
        for migration in MIGRATIONS:
            await conn.execute(migration)
    logger.info("skills table ready")
