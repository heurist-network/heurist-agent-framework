"""Admin API routes for skill marketplace.

Endpoints: import (URL/GitHub), approve, reject, check-upstream.
These mirror the CLI scripts but are callable via HTTP for admin UI integration.
"""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from mesh.skill_marketplace.db import get_pool
from mesh.skill_marketplace.parser import derive_source_type, parse_github_owner_repo, parse_skill_md
from mesh.skill_marketplace.storage import upload_file, upload_folder

logger = logging.getLogger("SkillMarketplace")

admin_router = APIRouter(prefix="/admin/skills", tags=["Skill Marketplace Admin"])


class ImportSkillRequest(BaseModel):
    url: Optional[str] = None
    slug: str
    category: Optional[str] = None
    risk_tier: Optional[str] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None
    source_path: Optional[str] = None
    author_json: Optional[dict] = None
    requires_secrets: bool = False
    requires_private_keys: bool = False
    requires_exchange_api_keys: bool = False
    can_sign_transactions: bool = False
    uses_leverage: bool = False
    accesses_user_portfolio: bool = False


class ApproveRejectRequest(BaseModel):
    by: str = "admin"
    notes: Optional[str] = None


@admin_router.post("/import", summary="Import a skill from URL",
                   description="Fetch a SKILL.md from a URL, parse frontmatter, upload to Autonomys, and insert as draft.")
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

    folder_files = None
    owner_repo = parse_github_owner_repo(body.url)
    if owner_repo and body.source_path:
        github_token = os.getenv("GITHUB_TOKEN")
        gh_headers = {"Accept": "application/vnd.github.v3+json"}
        if github_token:
            gh_headers["Authorization"] = f"token {github_token}"
        owner, repo = owner_repo
        folder_prefix = body.source_path.rstrip("/") + "/"
        async with aiohttp.ClientSession() as gh_session:
            async with gh_session.get(
                f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1",
                headers=gh_headers,
            ) as tree_resp:
                if tree_resp.status == 200:
                    tree_data = await tree_resp.json()
                    file_paths = [
                        item["path"] for item in tree_data.get("tree", [])
                        if item["type"] == "blob" and item["path"].startswith(folder_prefix)
                    ]
                    if len(file_paths) > 1:
                        folder_files = {}
                        raw_headers = {"Accept": "application/vnd.github.v3.raw"}
                        if github_token:
                            raw_headers["Authorization"] = f"token {github_token}"
                        for fp in file_paths:
                            async with gh_session.get(
                                f"https://api.github.com/repos/{owner}/{repo}/contents/{fp}",
                                headers=raw_headers,
                            ) as file_resp:
                                if file_resp.status == 200:
                                    folder_files[fp[len(folder_prefix):]] = await file_resp.read()

    if folder_files and len(folder_files) > 1:
        result = await upload_folder(folder_files, body.slug)
    else:
        result = await upload_file(raw, f"{body.slug}-SKILL.md")

    skill_id = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)

    resolved_source_url = body.source_url or body.url
    source_type = body.source_type or derive_source_type(resolved_source_url)

    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO skills (
                id, slug, name, description, skill_md_frontmatter_json,
                category, risk_tier, verification_status,
                source_type, source_url, source_path, author_json,
                file_url, approved_sha256, approved_at, approved_by,
                requires_secrets, requires_private_keys, requires_exchange_api_keys,
                can_sign_transactions, uses_leverage, accesses_user_portfolio,
                created_at, updated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24)""",
            skill_id,
            body.slug,
            parsed["name"],
            parsed["description"],
            json.dumps(parsed["frontmatter"]),
            body.category,
            body.risk_tier,
            "draft",
            source_type,
            resolved_source_url,
            body.source_path,
            json.dumps(body.author_json) if body.author_json else None,
            result["gateway_url"],
            result["sha256"],
            now,
            "admin",
            body.requires_secrets,
            body.requires_private_keys,
            body.requires_exchange_api_keys,
            body.can_sign_transactions,
            body.uses_leverage,
            body.accesses_user_portfolio,
            now,
            now,
        )

    return {"id": skill_id, "slug": body.slug, "status": "draft", "file_url": result["gateway_url"]}


@admin_router.post("/{skill_id}/approve", summary="Approve a skill",
                   description="Set verification_status to verified with audit fields.")
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
                   description="Set review_state to rejected. Skill stays as draft but is flagged.")
async def reject_skill(skill_id: str, body: ApproveRejectRequest):
    pool = await get_pool()
    now = datetime.now(timezone.utc)

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, slug FROM skills WHERE id = $1", skill_id)
        if not row:
            raise HTTPException(status_code=404, detail="Skill not found")

        await conn.execute(
            """UPDATE skills SET review_state = 'rejected',
               review_notes = $1, reviewed_at = $2, updated_at = $2
               WHERE id = $3""",
            body.notes, now, skill_id,
        )

    return {"id": skill_id, "slug": row["slug"], "review_state": "rejected"}


@admin_router.post("/check-upstream", summary="Check for upstream changes",
                   description="Poll GitHub repos and web URLs for all verified skills. Returns list of skills whose source content has changed since last approval.")
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
                    async with session.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", headers=headers) as resp:
                        if resp.status != 200:
                            continue
                        content = await resp.read()
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
