# Skill Marketplace Admin Commands

Reference for operating admin commands via Claude Code or terminal.

## Setup

**Working directory:** `D:/Github/heurist-agent-framework`

**Required env vars** (in `.env`):
- `SKILLS_DATABASE_URL` — PostgreSQL connection string
- `INTERNAL_API_KEY` — API key for admin HTTP endpoints
- `AI3_API_KEY` — Autonomys Auto Drive storage key
- `GITHUB_TOKEN` — (optional) for GitHub API rate limits

---

## 1. Add a Skill (Ingest)

### From GitHub URL (recommended)

```bash
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill \
  --category defi \
  --risk-tier low \
  --source-url https://github.com/OWNER/REPO \
  --author '{"display_name": "Author Name", "github_username": "username"}'
```

**For multi-skill repos** (skill in a subfolder):
```bash
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/skills/my-skill/SKILL.md \
  --slug my-skill \
  --source-url https://github.com/OWNER/REPO \
  --source-path skills/my-skill
```

### From GitHub repo (alternative)

```bash
python -m mesh.skill_marketplace.scripts.ingest_github \
  --repo OWNER/REPO \
  --slug my-skill \
  --category defi
```

**Scan a repo for all SKILL.md files:**
```bash
python -m mesh.skill_marketplace.scripts.ingest_github \
  --repo OWNER/REPO \
  --scan \
  --slug-prefix prefix
```

### From local directory

```bash
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --dir ./path/to/skill-folder \
  --slug my-skill \
  --category defi \
  --source-url https://github.com/OWNER/REPO
```

### From local file

```bash
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --file ./SKILL.md \
  --slug my-skill \
  --source-url https://github.com/OWNER/REPO
```

### Via Admin API

```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/import \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md",
    "slug": "my-skill",
    "category": "defi",
    "risk_tier": "low",
    "source_url": "https://github.com/OWNER/REPO",
    "author_json": {"display_name": "Name", "github_username": "user"}
  }'
```

### Security flags (optional, all default to false)

Add any of these to ingest commands:
- `--requires-secrets`
- `--requires-private-keys`
- `--requires-exchange-api-keys`
- `--can-sign-transactions`
- `--uses-leverage`
- `--accesses-user-portfolio`

**Note:** Ingested skills start as `draft` status. They must be approved to appear in public listings.

---

## 2. Approve a Skill

### Via CLI script

```bash
python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill
```

Optional: `--by admin-name`

### Via Admin API

```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/SKILL_ID/approve \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"by": "admin", "notes": "Reviewed and approved"}'
```

---

## 3. Reject a Skill

### Via Admin API

```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/SKILL_ID/reject \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"by": "admin", "notes": "Reason for rejection"}'
```

Sets `review_state=rejected` and `verification_status=draft`. Skill is hidden from public API.

---

## 4. Remove a Skill

No dedicated script exists. Use direct DB:

```python
import asyncio, asyncpg, ssl, os
from dotenv import load_dotenv
load_dotenv()

async def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = await asyncpg.connect(os.getenv('SKILLS_DATABASE_URL'), ssl=ctx)
    result = await conn.execute("DELETE FROM skills WHERE slug = $1", "my-skill")
    print(result)
    await conn.close()

asyncio.run(main())
```

---

## 5. Update / Re-ingest a Skill

To update a skill with new content from upstream:

1. **Delete** the existing skill from DB (see Remove above)
2. **Re-ingest** using the same slug (see Add above)
3. **Re-approve** (see Approve above)

Alternatively, update specific fields directly:

```python
import asyncio, asyncpg, ssl, os, json
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

from mesh.skill_marketplace.parser import fetch_github_folder_files
from mesh.skill_marketplace.storage import prepare_skill_artifact

async def main():
    url = "https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md"
    folder_files = await fetch_github_folder_files(url)
    raw = folder_files.get("SKILL.md", b"") if folder_files else b""

    artifact = await prepare_skill_artifact(raw, "my-skill", folder_files)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = await asyncpg.connect(os.getenv("SKILLS_DATABASE_URL"), ssl=ctx)

    await conn.execute("""
        UPDATE skills SET
            file_url = $1, approved_sha256 = $2,
            is_folder = $3, folder_manifest_json = $4,
            updated_at = $5
        WHERE slug = $6
    """, artifact["file_url"], artifact["sha256"],
        artifact["is_folder"],
        json.dumps(artifact["folder_manifest"]) if artifact["folder_manifest"] else None,
        datetime.now(timezone.utc), "my-skill")

    await conn.close()
    print("Updated")

asyncio.run(main())
```

---

## 6. List Skills

### Via CLI script

```bash
python -m mesh.skill_marketplace.scripts.list_skills
python -m mesh.skill_marketplace.scripts.list_skills --status draft
python -m mesh.skill_marketplace.scripts.list_skills --status verified
```

### Via DB query

```python
rows = await conn.fetch(
    "SELECT id, slug, name, category, verification_status, is_folder FROM skills ORDER BY created_at DESC"
)
```

---

## 7. Check Upstream Changes

Detects if GitHub/web source has changed since last approval.

```bash
python -m mesh.skill_marketplace.scripts.check_upstream
python -m mesh.skill_marketplace.scripts.check_upstream --slack-webhook https://hooks.slack.com/...
python -m mesh.skill_marketplace.scripts.check_upstream --dry-run
```

### Via Admin API

```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/check-upstream \
  -H "X-API-Key: $INTERNAL_API_KEY"
```

---

## 8. Run Standalone Server (Development)

```bash
python -m mesh.skill_marketplace.scripts.run_standalone --port 8001 --reload
```

API docs: `http://localhost:8001/docs`

---

## Common Workflows

### Add a new skill end-to-end

```bash
# 1. Ingest
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill --category defi --risk-tier low \
  --source-url https://github.com/OWNER/REPO \
  --author '{"display_name": "Name", "github_username": "user"}'

# 2. Verify it's in the DB
python -m mesh.skill_marketplace.scripts.list_skills --status draft

# 3. Approve
python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill

# 4. Confirm it's live
python -m mesh.skill_marketplace.scripts.list_skills --status verified
```

### Re-ingest a skill (update content)

```bash
# 1. Delete existing
python -c "
import asyncio, asyncpg, ssl, os
from dotenv import load_dotenv; load_dotenv()
async def main():
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    conn = await asyncpg.connect(os.getenv('SKILLS_DATABASE_URL'), ssl=ctx)
    print(await conn.execute('DELETE FROM skills WHERE slug = \$1', 'my-skill'))
    await conn.close()
asyncio.run(main())
"

# 2. Re-ingest (same command as original ingest)
python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill --category defi --source-url https://github.com/OWNER/REPO

# 3. Re-approve
python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill
```

---

## DB Schema Quick Reference

| Column | Type | Description |
|---|---|---|
| id | VARCHAR(8) | Auto-generated hex ID |
| slug | VARCHAR(128) | Unique skill identifier |
| name | VARCHAR(64) | Display name (from SKILL.md frontmatter) |
| description | VARCHAR(1024) | Description (from SKILL.md frontmatter) |
| category | VARCHAR(64) | defi, infrastructure, analytics, etc. |
| risk_tier | VARCHAR(32) | low, medium, high |
| verification_status | VARCHAR(16) | draft, verified |
| source_type | VARCHAR(16) | github, web_url (auto-derived) |
| source_url | VARCHAR(512) | GitHub repo or web URL |
| source_path | VARCHAR(512) | Subfolder path in multi-skill repos |
| is_folder | BOOLEAN | true if skill has multiple files |
| folder_manifest_json | JSONB | {path: cid} mapping for folder skills |
| file_url | VARCHAR(512) | Autonomys gateway URL for SKILL.md |
| approved_sha256 | VARCHAR(64) | SHA256 of SKILL.md at approval time |
| author_json | JSONB | {display_name, github_username} |
