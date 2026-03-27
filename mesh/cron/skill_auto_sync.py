"""Auto-sync tracked skills from their GitHub repos to the Heurist Skill Marketplace.

Checks the latest commit SHA for each tracked repo. If it differs from the last
known SHA, calls the admin update endpoint to re-fetch and re-upload the skill.

State is persisted in /root/.cron/skill_sync_state.json.
Designed to run via cron every 30 minutes.
"""

import json
import logging
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SkillAutoSync")

# ---- Config ----

SKILLS = [
    {"id": "8264d2c1", "slug": "heurist-finance", "repo": "heurist-network/heurist-finance"},
    {"id": "09284204", "slug": "heurist-mesh", "repo": "heurist-network/heurist-mesh-skill"},
]

API_BASE = "https://mesh.heurist.xyz"
STATE_FILE = Path("/root/.cron/skill_sync_state.json")

# Load from heurist-agent-framework .env
ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


def load_env_var(name: str) -> str:
    val = os.getenv(name, "")
    if val:
        return val
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    return ""


INTERNAL_API_KEY = load_env_var("INTERNAL_API_KEY")
GITHUB_TOKEN = load_env_var("GITHUB_TOKEN")

# ---- State ----


def read_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def write_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


# ---- GitHub ----


def get_latest_commit_sha(repo: str) -> str | None:
    url = f"https://api.github.com/repos/{repo}/commits/HEAD"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("sha")
    except urllib.error.HTTPError as e:
        logger.error(f"GitHub API error for {repo}: {e.code} {e.reason}")
        return None
    except Exception as e:
        logger.error(f"Failed to fetch commit for {repo}: {e}")
        return None


# ---- Admin API ----


def trigger_update(skill_id: str, retries: int = 2) -> dict | None:
    url = f"{API_BASE}/admin/skills/{skill_id}/update"
    headers = {
        "X-API-Key": INTERNAL_API_KEY,
        "Content-Type": "application/json",
    }
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=b"{}", headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            logger.error(f"Admin update failed for {skill_id} (attempt {attempt}/{retries}): {e.code} {body}")
        except Exception as e:
            logger.error(f"Admin update request failed for {skill_id} (attempt {attempt}/{retries}): {e}")
        if attempt < retries:
            import time
            time.sleep(60)
    return None


# ---- Main ----


def main():
    if not INTERNAL_API_KEY:
        logger.error("INTERNAL_API_KEY not found. Cannot call admin API.")
        sys.exit(1)

    state = read_state()
    updated = 0
    skipped = 0

    for skill in SKILLS:
        slug = skill["slug"]
        repo = skill["repo"]
        skill_id = skill["id"]

        sha = get_latest_commit_sha(repo)
        if not sha:
            logger.warning(f"{slug}: could not fetch latest commit, skipping")
            continue

        last_sha = state.get(slug, {}).get("last_commit")

        if sha == last_sha:
            logger.info(f"{slug}: no changes (commit {sha[:12]})")
            skipped += 1
            continue

        logger.info(f"{slug}: change detected {(last_sha or 'none')[:12]} → {sha[:12]}, updating...")
        result = trigger_update(skill_id)

        if result:
            state[slug] = {
                "last_commit": sha,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "approved_sha256": result.get("approved_sha256", ""),
            }
            write_state(state)
            logger.info(f"{slug}: updated successfully (approved_sha256={result.get('approved_sha256', '')[:16]}...)")
            updated += 1
        else:
            logger.error(f"{slug}: update failed, will retry next cycle")

    logger.info(f"Done. Updated: {updated}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
