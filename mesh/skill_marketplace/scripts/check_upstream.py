"""Detect upstream changes for ingested skills.

Polls GitHub repos and web URLs to check if source content has changed
since the last approved version. Alerts the team for manual review.

Usage:
    python -m mesh.skill_marketplace.scripts.check_upstream
    python -m mesh.skill_marketplace.scripts.check_upstream --slack-webhook https://hooks.slack.com/services/...
    python -m mesh.skill_marketplace.scripts.check_upstream --dry-run
"""

import argparse
import asyncio
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import aiohttp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from mesh.skill_marketplace.db import get_pool, init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CheckUpstream")

GITHUB_API = "https://api.github.com"


def _parse_github_url(source_url: str) -> tuple[str, str] | None:
    """Extract owner/repo from a GitHub URL. Returns (owner, repo) or None."""
    parsed = urlparse(source_url)
    if parsed.hostname not in ("github.com", "www.github.com"):
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        return None
    return parts[0], parts[1]


async def check_github_skill(session: aiohttp.ClientSession, skill: dict, github_token: str | None) -> dict | None:
    """Check if a GitHub-sourced skill has upstream changes.

    Fetches the SKILL.md content from the repo's default branch and compares
    its SHA256 against the approved_sha256 in our DB.
    """
    owner_repo = _parse_github_url(skill["source_url"])
    if not owner_repo:
        logger.warning(f"[{skill['slug']}] cannot parse GitHub URL: {skill['source_url']}")
        return None

    owner, repo = owner_repo
    path = skill["source_path"] or "SKILL.md"

    headers = {"Accept": "application/vnd.github.v3.raw"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"

    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 404:
                logger.warning(f"[{skill['slug']}] SKILL.md not found at {owner}/{repo}/{path}")
                return None
            resp.raise_for_status()
            content = await resp.read()
    except aiohttp.ClientError as e:
        logger.error(f"[{skill['slug']}] GitHub API error: {e}")
        return None

    upstream_sha256 = hashlib.sha256(content).hexdigest()
    if upstream_sha256 != skill["approved_sha256"]:
        return {
            "slug": skill["slug"],
            "source_type": "github",
            "source_url": skill["source_url"],
            "approved_sha256": skill["approved_sha256"],
            "upstream_sha256": upstream_sha256,
        }
    return None


async def check_web_url_skill(session: aiohttp.ClientSession, skill: dict) -> dict | None:
    """Check if a web-URL-sourced skill has upstream changes.

    Fetches the source URL and compares content SHA256 against approved_sha256.
    """
    try:
        async with session.get(skill["source_url"]) as resp:
            resp.raise_for_status()
            content = await resp.read()
    except aiohttp.ClientError as e:
        logger.error(f"[{skill['slug']}] fetch error: {e}")
        return None

    upstream_sha256 = hashlib.sha256(content).hexdigest()
    if upstream_sha256 != skill["approved_sha256"]:
        return {
            "slug": skill["slug"],
            "source_type": "web_url",
            "source_url": skill["source_url"],
            "approved_sha256": skill["approved_sha256"],
            "upstream_sha256": upstream_sha256,
        }
    return None


async def send_slack_alert(session: aiohttp.ClientSession, webhook_url: str, changes: list[dict]):
    """Send a Slack notification summarizing detected upstream changes."""
    lines = [f"*Skill Marketplace — {len(changes)} upstream change(s) detected*\n"]
    for c in changes:
        lines.append(f"• `{c['slug']}` ({c['source_type']}) — <{c['source_url']}|source>")
        lines.append(f"  approved: `{c['approved_sha256'][:12]}…` → upstream: `{c['upstream_sha256'][:12]}…`")

    payload = {"text": "\n".join(lines)}
    try:
        async with session.post(webhook_url, json=payload) as resp:
            if resp.status != 200:
                logger.error(f"Slack webhook returned {resp.status}")
            else:
                logger.info("Slack alert sent")
    except aiohttp.ClientError as e:
        logger.error(f"Slack webhook error: {e}")


async def run(args):
    await init_db()
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
        logger.info("no verified skills with source URLs found")
        return

    logger.info(f"checking {len(rows)} verified skill(s) for upstream changes")

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.warning("GITHUB_TOKEN not set — GitHub API rate limits will be restrictive")

    changes = []
    async with aiohttp.ClientSession() as session:
        for row in rows:
            skill = dict(row)
            result = None

            if skill["source_type"] == "github":
                result = await check_github_skill(session, skill, github_token)
            elif skill["source_type"] == "web_url":
                result = await check_web_url_skill(session, skill)
            else:
                logger.info(f"[{skill['slug']}] skipping unknown source_type: {skill['source_type']}")
                continue

            if result:
                changes.append(result)
                logger.warning(f"[{result['slug']}] CHANGED — approved: {result['approved_sha256'][:12]}… → upstream: {result['upstream_sha256'][:12]}…")
            else:
                logger.info(f"[{skill['slug']}] no changes")

        if changes:
            print(f"\n{'Slug':<30} {'Type':<10} {'Approved SHA256':<16} {'Upstream SHA256':<16}")
            print("-" * 75)
            for c in changes:
                print(f"{c['slug']:<30} {c['source_type']:<10} {c['approved_sha256'][:14]:<16} {c['upstream_sha256'][:14]:<16}")

            if args.slack_webhook and not args.dry_run:
                await send_slack_alert(session, args.slack_webhook, changes)
        else:
            print("\nAll skills are up to date with upstream sources.")

    if args.dry_run:
        logger.info("dry run — no notifications sent")


def main():
    parser = argparse.ArgumentParser(description="Check for upstream changes in skill sources")
    parser.add_argument("--slack-webhook", dest="slack_webhook", help="Slack webhook URL for alerts")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False,
                        help="detect changes but skip notifications")
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
