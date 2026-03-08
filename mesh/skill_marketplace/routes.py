"""Skill marketplace read-only API routes, mounted by mesh_api.py.

Endpoints for frontend UI and the forked skills CLI tool.
"""

import io
import json
import logging
import os
import zipfile
from enum import Enum
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field

from mesh.skill_marketplace.db import get_pool
from mesh.skill_marketplace.storage import cid_from_gateway_url, download_file, download_files
from mesh.skill_marketplace.taxonomy import normalize_category, normalize_labels

logger = logging.getLogger("SkillMarketplace")

router = APIRouter(tags=["Skill Marketplace"])


class VerificationStatus(str, Enum):
    draft = "draft"
    verified = "verified"
    archived = "archived"


class SkillOrderBy(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"
    download_count = "download_count"
    star_count = "star_count"
    name_asc = "name_asc"
    name_desc = "name_desc"


class SkillCapabilities(BaseModel):
    requires_secrets: bool = False
    requires_private_keys: bool = False
    requires_exchange_api_keys: bool = False
    can_sign_transactions: bool = False
    uses_leverage: bool = False
    accesses_user_portfolio: bool = False


class SkillAuthor(BaseModel):
    display_name: Optional[str] = None
    author_type: Optional[str] = None
    github_username: Optional[str] = None
    github_profile_url: Optional[str] = None
    website_url: Optional[str] = None


class SkillSummary(BaseModel):
    id: str
    slug: str
    name: str
    description: str
    category: Optional[str] = None
    labels: list[str] = Field(default_factory=list)
    risk_tier: Optional[str] = None
    verification_status: VerificationStatus
    author: SkillAuthor = SkillAuthor()
    file_url: Optional[str] = None
    external_api_dependencies: list[str] = Field(default_factory=list)
    download_count: int = 0
    star_count: int = 0
    capabilities: SkillCapabilities = SkillCapabilities()


class SkillDetail(SkillSummary):
    skill_md_frontmatter_json: Optional[dict] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None
    source_path: Optional[str] = None
    approved_sha256: Optional[str] = None
    approved_at: Optional[str] = None
    approved_by: Optional[str] = None
    is_folder: bool = False
    folder_manifest: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SkillListResponse(BaseModel):
    skills: list[SkillSummary]
    total: int


class CheckUpdatesRequest(BaseModel):
    installed: list[dict]


class CheckUpdatesResponse(BaseModel):
    updates: list[dict]


SKILL_ORDER_SQL = {
    SkillOrderBy.created_at: "created_at DESC, name ASC",
    SkillOrderBy.updated_at: "updated_at DESC, name ASC",
    SkillOrderBy.download_count: "download_count DESC, name ASC",
    SkillOrderBy.star_count: "star_count DESC, name ASC",
    SkillOrderBy.name_asc: "name ASC",
    SkillOrderBy.name_desc: "name DESC",
}


def _row_to_summary(row) -> dict:
    return {
        "id": row["id"],
        "slug": row["slug"],
        "name": row["name"],
        "description": row["description"],
        "category": row["category"],
        "labels": row["labels"] or [],
        "risk_tier": row["risk_tier"],
        "verification_status": row["verification_status"],
        "author": json.loads(row["author_json"]) if row["author_json"] else {},
        "file_url": row["file_url"],
        "external_api_dependencies": row["external_api_dependencies"] or [],
        "download_count": row["download_count"] or 0,
        "star_count": row["star_count"] or 0,
        "capabilities": {
            "requires_secrets": row["requires_secrets"],
            "requires_private_keys": row["requires_private_keys"],
            "requires_exchange_api_keys": row["requires_exchange_api_keys"],
            "can_sign_transactions": row["can_sign_transactions"],
            "uses_leverage": row["uses_leverage"],
            "accesses_user_portfolio": row["accesses_user_portfolio"],
        },
    }


def _row_to_detail(row) -> dict:
    d = _row_to_summary(row)
    d.update({
        "skill_md_frontmatter_json": json.loads(row["skill_md_frontmatter_json"]) if row["skill_md_frontmatter_json"] else None,
        "source_type": row["source_type"],
        "source_url": row["source_url"],
        "source_path": row["source_path"],
        "approved_sha256": row["approved_sha256"],
        "approved_at": row["approved_at"].isoformat() if row["approved_at"] else None,
        "approved_by": row["approved_by"],
        "is_folder": row["is_folder"] if "is_folder" in row.keys() else False,
        "folder_manifest": json.loads(row["folder_manifest_json"]) if row.get("folder_manifest_json") else None,
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
    })
    return d


@router.get("/skills", response_model=SkillListResponse, summary="List skills",
             description="Browse and search the skill catalog. Returns only verified skills by default. Supports filtering by category, search by slug/name/description, sorting, and pagination.")
async def list_skills(
    category: Optional[str] = Query(None, description="Filter by category"),
    labels: Optional[list[str]] = Query(None, description="Filter by one or more labels (matches any label)"),
    verification_status: Optional[VerificationStatus] = Query(None, description="Filter by status: draft | verified | archived"),
    search: Optional[str] = Query(None, description="Search by skill slug, name, or description"),
    order_by: SkillOrderBy = Query(
        SkillOrderBy.created_at,
        description="Sort order: created_at | updated_at | download_count | star_count | name_asc | name_desc",
    ),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(20, ge=1, le=100, description="Results per page (max 100)"),
):
    pool = await get_pool()

    conditions = []
    params = []
    idx = 1

    if verification_status:
        conditions.append(f"verification_status = ${idx}")
        params.append(verification_status)
        idx += 1
    else:
        conditions.append(f"verification_status = ${idx}")
        params.append("verified")
        idx += 1

    normalized_category = normalize_category(category)
    if normalized_category:
        conditions.append(f"category = ${idx}")
        params.append(normalized_category)
        idx += 1

    normalized_labels = normalize_labels(labels)
    if normalized_labels:
        conditions.append(f"labels && ${idx}::text[]")
        params.append(normalized_labels)
        idx += 1

    if search:
        conditions.append(f"(slug ILIKE ${idx} OR name ILIKE ${idx} OR description ILIKE ${idx})")
        params.append(f"%{search}%")
        idx += 1

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    order_clause = SKILL_ORDER_SQL[order_by]

    async with pool.acquire() as conn:
        total = await conn.fetchval(f"SELECT COUNT(*) FROM skills {where}", *params)

        rows = await conn.fetch(
            f"SELECT * FROM skills {where} ORDER BY {order_clause} LIMIT ${idx} OFFSET ${idx + 1}",
            *params, limit, offset,
        )

    return SkillListResponse(
        skills=[SkillSummary(**_row_to_summary(r)) for r in rows],
        total=total,
    )


@router.get("/skills/categories/list", summary="List skill categories",
             description="Returns all categories with their verified skill counts. Useful for building category filters in the UI.")
async def list_categories():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT category, COUNT(*) as count FROM skills
               WHERE category IS NOT NULL AND verification_status = 'verified'
               GROUP BY category ORDER BY count DESC"""
        )
    return [{"category": r["category"], "count": r["count"]} for r in rows]


@router.get("/skills/labels/list", summary="List skill labels",
             description="Returns all labels with their verified skill counts. Useful for building secondary filters in the UI.")
async def list_labels():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT label, COUNT(*) as count
               FROM skills, unnest(labels) AS label
               WHERE verification_status = 'verified'
               GROUP BY label ORDER BY count DESC, label ASC"""
        )
    return [{"label": r["label"], "count": r["count"]} for r in rows]


@router.get("/skills/{slug}", response_model=SkillDetail, summary="Get skill detail",
             description="Returns full skill metadata including frontmatter, capabilities, source attribution, and audit fields.")
async def get_skill(slug: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM skills WHERE slug = $1", slug)

    if not row:
        raise HTTPException(status_code=404, detail="Skill not found")

    return SkillDetail(**_row_to_detail(row))


@router.get("/skills/{slug}/download", summary="Download skill",
             description="For single-file skills: returns SKILL.md as text/markdown. For folder skills: returns a zip bundle of all files assembled on-the-fly from per-file CIDs. Includes X-Skill-SHA256 header.")
async def download_skill(slug: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT id, slug, file_url, approved_sha256, is_folder, folder_manifest_json FROM skills
               WHERE slug = $1 AND verification_status = 'verified'""",
            slug,
        )

    if not row:
        raise HTTPException(status_code=404, detail="Skill not found or not verified")

    if row["is_folder"] and row["folder_manifest_json"]:
        manifest = json.loads(row["folder_manifest_json"])
        contents_by_path = await download_files(
            {rel_path: cid for rel_path, cid in sorted(manifest.items())}
        )
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel_path, cid in sorted(manifest.items()):
                zf.writestr(rel_path, contents_by_path[rel_path])
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE skills SET download_count = download_count + 1 WHERE id = $1",
                row["id"],
            )
        return Response(
            content=buf.getvalue(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{slug}.zip"',
                "X-Skill-SHA256": row["approved_sha256"] or "",
                "X-Skill-Slug": slug,
            },
        )

    cid = cid_from_gateway_url(row["file_url"])
    if not cid:
        raise HTTPException(status_code=500, detail="No file CID available")

    content = await download_file(cid)
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE skills SET download_count = download_count + 1 WHERE id = $1",
            row["id"],
        )
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="{slug}-SKILL.md"',
            "X-Skill-SHA256": row["approved_sha256"] or "",
            "X-Skill-Slug": slug,
        },
    )


@router.get("/skills/{slug}/files", summary="List files in a folder skill",
             description="Returns the file manifest for folder skills (path → CID mapping). For single-file skills, returns just the SKILL.md entry.")
async def list_skill_files(slug: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT slug, file_url, approved_sha256, is_folder, folder_manifest_json FROM skills
               WHERE slug = $1 AND verification_status = 'verified'""",
            slug,
        )

    if not row:
        raise HTTPException(status_code=404, detail="Skill not found or not verified")

    if row["is_folder"] and row["folder_manifest_json"]:
        manifest = json.loads(row["folder_manifest_json"])
        file_list = [
            {"path": path, "cid": cid, "gateway_url": f"https://gateway.autonomys.xyz/file/{cid}"}
            for path, cid in sorted(manifest.items())
        ]
    else:
        cid = cid_from_gateway_url(row["file_url"])
        file_list = [{"path": "SKILL.md", "cid": cid, "gateway_url": row["file_url"]}]

    return {"slug": slug, "is_folder": row["is_folder"], "file_count": len(file_list), "files": file_list}


@router.get("/skills/{slug}/files/{file_path:path}", summary="Download individual file from folder skill",
             description="Download a specific file from a folder skill by its relative path (e.g. SKILL.md, tools/helper.py).")
async def download_skill_file(slug: str, file_path: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT slug, file_url, is_folder, folder_manifest_json FROM skills
               WHERE slug = $1 AND verification_status = 'verified'""",
            slug,
        )

    if not row:
        raise HTTPException(status_code=404, detail="Skill not found or not verified")

    if row["is_folder"] and row["folder_manifest_json"]:
        manifest = json.loads(row["folder_manifest_json"])
        cid = manifest.get(file_path)
        if not cid:
            raise HTTPException(status_code=404, detail=f"File '{file_path}' not found in skill")
    elif file_path == "SKILL.md":
        cid = cid_from_gateway_url(row["file_url"])
    else:
        raise HTTPException(status_code=404, detail=f"File '{file_path}' not found in skill")

    content = await download_file(cid)
    media_type = "text/markdown" if file_path.endswith(".md") else "application/octet-stream"
    filename = file_path.split("/")[-1]

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/check-updates", response_model=CheckUpdatesResponse, summary="Check for skill updates",
              description="CLI sends a list of installed skill slugs with their SHA256 hashes. Returns any skills that have a newer approved version available.")
async def check_updates(body: CheckUpdatesRequest):
    pool = await get_pool()
    updates = []

    async with pool.acquire() as conn:
        for installed in body.installed:
            slug = installed.get("slug")
            sha256 = installed.get("sha256")
            if not slug or not sha256:
                continue

            # TODO: for folder skills, approved_sha256 tracks only SKILL.md, not auxiliary files.
            # If a secondary file changes without a SKILL.md change, this check will miss it.
            # Fix: compute a composite hash over all files in folder_manifest_json at approve time.
            row = await conn.fetchrow(
                """SELECT slug, approved_sha256, file_url FROM skills
                   WHERE slug = $1 AND verification_status = 'verified'
                   AND approved_sha256 IS NOT NULL AND approved_sha256 != $2""",
                slug, sha256,
            )
            if row:
                updates.append({
                    "slug": row["slug"],
                    "approved_sha256": row["approved_sha256"],
                    "file_url": row["file_url"],
                })

    return CheckUpdatesResponse(updates=updates)
