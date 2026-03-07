"""Admin API routes for skill marketplace.

Endpoints: import (URL/GitHub), approve, reject, check-upstream.
All endpoints require X-API-Key header matching INTERNAL_API_KEY env var.
"""

import hashlib
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from mesh.skill_marketplace.db import get_pool, insert_skill_draft
from mesh.skill_marketplace.parser import derive_source_type, fetch_github_folder_files, parse_github_owner_repo, parse_skill_md
from mesh.skill_marketplace.storage import prepare_skill_artifact

logger = logging.getLogger("SkillMarketplace")

admin_router = APIRouter(prefix="/admin/skills", tags=["Skill Marketplace Admin"])

# ---- Auth ----

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _require_api_key(api_key: str = Security(_api_key_header)):
    expected = os.getenv("INTERNAL_API_KEY", "")
    if not expected or api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


# ---- Request models ----

class ImportSkillRequest(BaseModel):
    url: Optional[str] = None
    slug: str
    category: Optional[str] = None
    risk_tier: Optional[str] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None
    source_path: Optional[str] = None
    author_json: Optional[dict] = None
    external_api_dependencies: list[str] = Field(default_factory=list)
    requires_secrets: bool = False
    requires_private_keys: bool = False
    requires_exchange_api_keys: bool = False
    can_sign_transactions: bool = False
    uses_leverage: bool = False
    accesses_user_portfolio: bool = False


class ApproveRejectRequest(BaseModel):
    by: str = "admin"
    notes: Optional[str] = None


class UpdateExternalApiDependenciesRequest(BaseModel):
    external_api_dependencies: list[str] = Field(default_factory=list)


class UpdateSkillMetricsRequest(BaseModel):
    download_count: Optional[int] = Field(default=None, ge=0)
    star_count: Optional[int] = Field(default=None, ge=0)


def _normalize_external_api_dependencies(values: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for value in values:
        cleaned = value.strip()
        if not cleaned:
            continue
        dedupe_key = cleaned.casefold()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        normalized.append(cleaned)

    return normalized


# ---- Endpoints ----

@admin_router.post("/import", summary="Import a skill from URL",
                   description="Fetch a SKILL.md from a URL, parse frontmatter, upload each file individually to Autonomys, and insert as draft.",
                   dependencies=[Depends(_require_api_key)])
async def import_skill(body: ImportSkillRequest):
    if not body.url:
        raise HTTPException(status_code=400, detail="url is required")

    pool = await get_pool()

    async with pool.acquire() as conn:
        existing = await conn.fetchval("SELECT id FROM skills WHERE slug = $1", body.slug)
        if existing:
            raise HTTPException(status_code=409, detail=f"slug '{body.slug}' already exists")

    async with aiohttp.ClientSession() as session:
        async with session.get(body.url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=400, detail=f"failed to fetch URL: {resp.status}")
            raw = await resp.read()

    parsed = parse_skill_md(raw)

    # Try to fetch full folder if it's a GitHub folder skill
    folder_files = await fetch_github_folder_files(body.url, body.source_path)

    skill_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)
    resolved_source_url = body.source_url or body.url
    source_type = body.source_type or derive_source_type(resolved_source_url)

    artifact = await prepare_skill_artifact(raw, body.slug, folder_files if folder_files and len(folder_files) > 1 else None)

    async with pool.acquire() as conn:
        await insert_skill_draft(conn, {
            "id": skill_id,
            "slug": body.slug,
            "name": parsed["name"],
            "description": parsed["description"],
            "skill_md_frontmatter_json": parsed["frontmatter"],
            "category": body.category,
            "risk_tier": body.risk_tier,
            "source_type": source_type,
            "source_url": resolved_source_url,
            "source_path": body.source_path,
            "author_json": body.author_json,
            "external_api_dependencies": _normalize_external_api_dependencies(body.external_api_dependencies),
            **artifact,
            "approved_by": "admin",
            "requires_secrets": body.requires_secrets,
            "requires_private_keys": body.requires_private_keys,
            "requires_exchange_api_keys": body.requires_exchange_api_keys,
            "can_sign_transactions": body.can_sign_transactions,
            "uses_leverage": body.uses_leverage,
            "accesses_user_portfolio": body.accesses_user_portfolio,
            "created_at": now,
        })

    return {"id": skill_id, "slug": body.slug, "status": "draft", "file_url": artifact["file_url"], "is_folder": artifact["is_folder"]}


@admin_router.patch("/{skill_id}/external-api-dependencies", summary="Update external API dependencies",
                    description="Set the admin-managed list of external API dependencies for a skill.",
                    dependencies=[Depends(_require_api_key)])
async def update_external_api_dependencies(skill_id: str, body: UpdateExternalApiDependenciesRequest):
    pool = await get_pool()
    now = datetime.now(timezone.utc)
    dependencies = _normalize_external_api_dependencies(body.external_api_dependencies)

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug FROM skills WHERE id = $1", skill_id)
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        await conn.execute(
            """UPDATE skills
               SET external_api_dependencies = $1, updated_at = $2
               WHERE id = $3""",
            dependencies, now, skill_id,
        )

    return {
        "id": skill_id,
        "slug": row["slug"],
        "external_api_dependencies": dependencies,
        "updated_at": now.isoformat(),
    }


@admin_router.patch("/{skill_id}/metrics", summary="Update skill metrics",
                    description="Set admin-managed metric counters for a skill, such as star_count or a backfilled download_count.",
                    dependencies=[Depends(_require_api_key)])
async def update_skill_metrics(skill_id: str, body: UpdateSkillMetricsRequest):
    if body.download_count is None and body.star_count is None:
        raise HTTPException(status_code=400, detail="At least one metric must be provided")

    pool = await get_pool()
    now = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, slug, download_count, star_count FROM skills WHERE id = $1",
            skill_id,
        )
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        await conn.execute(
            """UPDATE skills
               SET download_count = COALESCE($1, download_count),
                   star_count = COALESCE($2, star_count),
                   updated_at = $3
               WHERE id = $4""",
            body.download_count,
            body.star_count,
            now,
            skill_id,
        )

    return {
        "id": skill_id,
        "slug": row["slug"],
        "download_count": body.download_count if body.download_count is not None else row["download_count"],
        "star_count": body.star_count if body.star_count is not None else row["star_count"],
        "updated_at": now.isoformat(),
    }


@admin_router.post("/{skill_id}/approve", summary="Approve a skill",
                   description="Set verification_status to verified with audit fields.",
                   dependencies=[Depends(_require_api_key)])
async def approve_skill(skill_id: str, body: ApproveRejectRequest):
    pool = await get_pool()
    now = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug, verification_status FROM skills WHERE id = $1", skill_id)
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        if row["verification_status"] == "verified":
            return {"id": skill_id, "slug": row["slug"], "status": "already verified"}

        await conn.execute(
            """UPDATE skills SET verification_status = 'verified',
               approved_by = $1, approved_at = $2, review_notes = $3,
               review_state = 'approved', reviewed_at = $2, updated_at = $2
               WHERE id = $4""",
            body.by, now, body.notes, skill_id,
        )

    return {"id": skill_id, "slug": row["slug"], "status": "verified", "approved_by": body.by}


@admin_router.post("/{skill_id}/reject", summary="Reject a skill",
                   description="Set review_state=rejected and verification_status=draft. Skill is hidden from public API.",
                   dependencies=[Depends(_require_api_key)])
async def reject_skill(skill_id: str, body: ApproveRejectRequest):
    pool = await get_pool()
    now = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug FROM skills WHERE id = $1", skill_id)
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        await conn.execute(
            """UPDATE skills SET review_state = 'rejected',
               verification_status = 'draft',
               review_notes = $1, reviewed_at = $2, updated_at = $2
               WHERE id = $3""",
            body.notes, now, skill_id,
        )

    return {"id": skill_id, "slug": row["slug"], "review_state": "rejected", "verification_status": "draft"}


@admin_router.post("/check-upstream", summary="Check for upstream changes",
                   description="Poll GitHub repos and web URLs for all verified skills. Returns skills whose source content has changed since last approval.",
                   dependencies=[Depends(_require_api_key)])
async def check_upstream():
    pool = await get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT slug, source_type, source_url, source_path, approved_sha256
               FROM skills
               WHERE verification_status = 'verified'
               AND source_url IS NOT NULL
               AND approved_sha256 IS NOT NULL"""
        )

    if not rows:
        return {"changes": [], "checked": 0}

    github_token = os.getenv("GITHUB_TOKEN")
    changes = []

    async with aiohttp.ClientSession() as session:
        for row in rows:
            skill = dict(row)
            upstream_sha256 = None

            if skill["source_type"] == "github":
                owner_repo = parse_github_owner_repo(skill["source_url"])
                if not owner_repo:
                    continue
                owner, repo = owner_repo
                path = skill["source_path"] or "SKILL.md"
                headers = {"Accept": "application/vnd.github.v3.raw"}
                if github_token:
                    headers["Authorization"] = f"token {github_token}"
                try:
                    async with session.get(
                        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
                        headers=headers,
                    ) as resp:
                        if resp.status != 200:
                            continue
                        content = await resp.read()
                        # TODO: for folder skills, this only hashes SKILL.md. Changes to auxiliary
                        # files in the folder will not be detected. Fix: fetch and hash all files
                        # in the folder, then compare against a composite hash stored at approve time.
                        upstream_sha256 = hashlib.sha256(content).hexdigest()
                except aiohttp.ClientError:
                    continue

            elif skill["source_type"] == "web_url":
                try:
                    async with session.get(skill["source_url"]) as resp:
                        if resp.status != 200:
                            continue
                        content = await resp.read()
                        upstream_sha256 = hashlib.sha256(content).hexdigest()
                except aiohttp.ClientError:
                    continue

            if upstream_sha256 and upstream_sha256 != skill["approved_sha256"]:
                changes.append({
                    "slug": skill["slug"],
                    "source_type": skill["source_type"],
                    "source_url": skill["source_url"],
                    "approved_sha256": skill["approved_sha256"],
                    "upstream_sha256": upstream_sha256,
                })

    return {"changes": changes, "checked": len(rows)}
