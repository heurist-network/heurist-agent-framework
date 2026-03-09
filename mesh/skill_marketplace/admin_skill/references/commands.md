# Heurist Skill Marketplace — Full Command Reference

## Ingest: From GitHub URL (recommended)

```bash
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill \
  --category Crypto \
  --label defi \
  --risk-tier low \
  --source-url https://github.com/OWNER/REPO \
  --author '{"display_name": "Author Name", "github_username": "username"}' \
  --reference-url https://x.com/example/status/123 \
  --reference-url https://example.com
```

**Multi-skill repo (skill in subfolder):**
```bash
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/skills/my-skill/SKILL.md \
  --slug my-skill \
  --category Developer \
  --label tooling \
  --source-url https://github.com/OWNER/REPO \
  --source-path skills/my-skill \
  --reference-url https://x.com/example/status/123
```

## Ingest: From Local Directory or File

```bash
# From local directory
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --dir ./path/to/skill-folder \
  --slug my-skill \
  --category Stocks \
  --label analytics \
  --source-url https://github.com/OWNER/REPO \
  --reference-url https://example.com

# From local file
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --file ./SKILL.md \
  --slug my-skill \
  --category Social \
  --label news \
  --source-url https://github.com/OWNER/REPO \
  --reference-url https://example.com
```

## Ingest: From GitHub Repo (Alternative)

```bash
uv run python -m mesh.skill_marketplace.scripts.ingest_github \
  --repo OWNER/REPO \
  --slug my-skill \
  --category Crypto \
  --reference-url https://example.com

# Scan repo for all SKILL.md files
uv run python -m mesh.skill_marketplace.scripts.ingest_github \
  --repo OWNER/REPO \
  --scan \
  --slug-prefix prefix \
  --category Developer
```

## Taxonomy Update (Category + Labels)

Category is the single top-level browse bucket. Valid values are:
`Stocks`, `Macro`, `Crypto`, `Developer`, `Social`

Labels are overlapping secondary descriptors such as:
`analytics`, `signals`, `screening`, `portfolio`, `research`, `execution`, `mcp`, `options`, `defi`, `ethereum`, `news`, `twitter`

Use the admin taxonomy endpoint to fix or backfill both:

```bash
curl -X PATCH https://mesh.heurist.xyz/admin/skills/SKILL_ID/taxonomy \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Stocks",
    "labels": ["analytics", "options"]
  }'
```

Do not use labels for capabilities already covered by dedicated DB columns:
`requires_secrets`, `requires_private_keys`, `requires_exchange_api_keys`, `can_sign_transactions`, `uses_leverage`, `accesses_user_portfolio`

## Approve

```bash
uv run python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill
# Optional: --by admin-name
```

**Via Admin API:**
```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/SKILL_ID/approve \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"by": "admin", "notes": "Reviewed and approved"}'
```

## Reject

```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/SKILL_ID/reject \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"by": "admin", "notes": "Reason for rejection"}'
```
Sets `review_state=rejected`, `verification_status=draft`. Hidden from public API.

## Remove (DB)

No dedicated script — use direct DB:

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

## Update Name (DB)

Fix a generic parsed name before or after approval:

```python
import asyncio, asyncpg, ssl, os
from dotenv import load_dotenv
load_dotenv()

async def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = await asyncpg.connect(os.getenv('SKILLS_DATABASE_URL'), ssl=ctx)
    await conn.execute("UPDATE skills SET name = $1 WHERE slug = $2", "Ethereum Gas Tracker", "eth-gas")
    await conn.close()

asyncio.run(main())
```

## Update External API Dependencies

```bash
curl -X PATCH https://mesh.heurist.xyz/admin/skills/SKILL_ID/external-api-dependencies \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"external_api_dependencies": ["CoinGecko", "OKX"]}'
```

## Update Reference URLs

Admin-only recordkeeping links such as announcement posts, websites, or docs:

```bash
curl -X PATCH https://mesh.heurist.xyz/admin/skills/SKILL_ID/reference-urls \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"reference_urls": ["https://x.com/unusual_whales/status/2030312769489416403", "https://ethskills.com/"]}'
```

## Update Metrics (Stars / Downloads)

`download_count` increments automatically on `GET /skills/{slug}/download`. Use this endpoint for `star_count` updates or one-time backfills:

```bash
curl -X PATCH https://mesh.heurist.xyz/admin/skills/SKILL_ID/metrics \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"star_count": 12, "download_count": 340}'
```

## Update Skill Content (Preferred)

Use `--update` to update an existing skill in place. Preserves `id`, `download_count`, `star_count`, and `created_at`. Resets status to `draft`.

```bash
# 1. Update from source
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill --category Stocks --label analytics \
  --source-url https://github.com/OWNER/REPO --update

# 2. Re-approve
uv run python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill
```



## Check Upstream Changes

Detects if GitHub/web source has changed since last approval:

```bash
uv run python -m mesh.skill_marketplace.scripts.check_upstream
uv run python -m mesh.skill_marketplace.scripts.check_upstream --dry-run
uv run python -m mesh.skill_marketplace.scripts.check_upstream --slack-webhook https://hooks.slack.com/...
```

**Via Admin API:**
```bash
curl -X POST https://mesh.heurist.xyz/admin/skills/check-upstream \
  -H "X-API-Key: $INTERNAL_API_KEY"
```

## List Skills

```bash
uv run python -m mesh.skill_marketplace.scripts.list_skills
uv run python -m mesh.skill_marketplace.scripts.list_skills --status draft
uv run python -m mesh.skill_marketplace.scripts.list_skills --status verified
```

## Via Admin API: Import Skill

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
    "author_json": {"display_name": "Name", "github_username": "user"},
    "external_api_dependencies": ["CoinGecko", "OKX"],
    "reference_urls": ["https://x.com/example/status/123", "https://example.com"]
  }'
```

## Development: Run Standalone Server

```bash
uv run python -m mesh.skill_marketplace.scripts.run_standalone --port 8001 --reload
# API docs: http://localhost:8001/docs
```

## DB Schema Quick Reference

| Column | Type | Description |
|---|---|---|
| id | VARCHAR(8) | Auto-generated hex ID |
| slug | VARCHAR(128) | Unique skill identifier |
| name | VARCHAR(64) | Display name (from SKILL.md frontmatter) |
| description | VARCHAR(1024) | Description (from SKILL.md frontmatter) |
| category | VARCHAR(64) | Primary category: Stocks, Macro, Crypto, Developer, Social |
| labels | TEXT[] | Overlapping labels such as analytics, signals, options, defi, mcp |
| risk_tier | VARCHAR(32) | low, medium, high |
| verification_status | VARCHAR(16) | draft, verified |
| source_type | VARCHAR(16) | github, web_url (auto-derived) |
| source_url | VARCHAR(512) | GitHub repo or web URL |
| source_path | VARCHAR(512) | Subfolder path in multi-skill repos |
| is_folder | BOOLEAN | true if skill has multiple files |
| file_url | VARCHAR(512) | Autonomys gateway URL for SKILL.md |
| approved_sha256 | VARCHAR(64) | SHA256 of SKILL.md at approval time |
| author_json | JSONB | {display_name, github_username} |
| external_api_dependencies | TEXT[] | Admin-managed list of external API names |
| reference_urls | TEXT[] | Admin-only recordkeeping links such as announcement posts or websites |
| download_count | INTEGER | Auto-incremented on download |
| star_count | INTEGER | Admin-managed star count |
