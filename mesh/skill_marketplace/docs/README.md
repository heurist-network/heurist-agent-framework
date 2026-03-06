# Skill Marketplace

Backend module for the Heurist Mesh Skill Marketplace. Makes Web3 agent skills discoverable, verifiable, and installable.

## Directory structure

```
mesh/skill_marketplace/
├── db.py              # PostgreSQL schema + asyncpg connection pool
├── parser.py          # SKILL.md YAML frontmatter parser + shared URL utilities
├── storage.py         # Autonomys Auto Drive upload/download (single file + folder zip)
├── routes.py          # Read-only FastAPI routes (mounted by mesh_api.py)
├── admin_routes.py    # Admin API routes (import, approve, reject, check-upstream)
├── docs/
│   ├── README.md          # This file
│   ├── scope.md           # Full project scope and checkpoint tracker
│   └── review_checklist.md  # Admin review checklist before approving a skill
└── scripts/
    ├── ingest_skill.py    # Ingest a skill from URL, local file, or local folder
    ├── ingest_github.py   # Ingest skill(s) from a GitHub repo (single or scan mode)
    ├── approve_skill.py   # Approve a draft skill
    ├── list_skills.py     # List all skills (admin view)
    ├── check_upstream.py  # Detect upstream changes in skill sources
    └── run_standalone.py  # Standalone dev server (no mesh_api dependency)
```

## Running

### Via mesh_api.py (production)

The skill marketplace routes are automatically mounted when mesh_api.py starts. No extra setup needed.

```bash
cd /root/heurist-agent-framework
uv run uvicorn mesh.mesh_api:app --host 0.0.0.0 --port 8005
```

### Standalone dev server

Run the marketplace API independently without loading mesh agents:

```bash
cd /root/heurist-agent-framework

# Standard mode
.venv/bin/python -m mesh.skill_marketplace.scripts.run_standalone --port 8008

# Hot-reload mode (auto-restarts on file changes)
.venv/bin/python -m mesh.skill_marketplace.scripts.run_standalone --port 8008 --reload
```

### API endpoints

**Public (read-only):**
- `GET /skills` — list skills (verified only by default, supports `verification_status`, `category`, `search`, `limit`, `offset`)
- `GET /skills/{slug}` — full skill detail with frontmatter, capabilities, source attribution, audit fields
- `GET /skills/categories/list` — all categories with verified skill counts
- `GET /skills/{slug}/download` — download skill: returns `SKILL.md` (text/markdown) for single-file skills, or a `.zip` bundle assembled from per-file CIDs for folder skills; includes `X-Skill-SHA256` header
- `GET /skills/{slug}/files` — file manifest for folder skills: returns `{path, cid, gateway_url}` per file; single-file skills return a one-entry list with `SKILL.md`
- `GET /skills/{slug}/files/{path}` — download a specific file from a folder skill by relative path (e.g. `SKILL.md`, `tools/helper.py`)
- `POST /check-updates` — CLI sends list of `{slug, sha256}` pairs, receives slugs with newer approved versions

**Admin:**
- `POST /admin/skills/import` — import a skill from URL or GitHub (fetch, parse, upload to Autonomys, insert as draft)
- `POST /admin/skills/{id}/approve` — set `verification_status=verified` with audit fields
- `POST /admin/skills/{id}/reject` — set `review_state=rejected` and `verification_status=draft` (hides from public API)
- `POST /admin/skills/check-upstream` — poll all verified skills for upstream source changes (compares SHA256)

**Query parameters for `GET /skills`:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `verification_status` | `draft\|verified\|archived` | `verified` | Filter by status |
| `category` | string | — | Filter by category |
| `search` | string | — | Search slug, name, and description (case-insensitive) |
| `limit` | int (1–100) | 20 | Results per page |
| `offset` | int | 0 | Pagination offset |

## Environment variables

Set in `.env` at the repo root:

| Variable | Required | Description |
|----------|----------|-------------|
| `SKILLS_DATABASE_URL` | Yes | PostgreSQL connection string |
| `AI3_API_KEY` | Yes | Autonomys Auto Drive API key |
| `AUTONOMYS_API_URL` | No | Auto Drive API base URL (default: `https://mainnet.auto-drive.autonomys.xyz`) |
| `AUTONOMYS_GATEWAY_URL` | No | Auto Drive gateway URL (default: `https://gateway.autonomys.xyz`) |
| `GITHUB_TOKEN` | No | GitHub personal access token (raises API rate limits for upstream checks) |

## CLI Scripts

### Ingest a skill from URL/file/folder

```bash
# From a raw URL (source_type auto-derived from URL)
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_skill \
    --url https://raw.githubusercontent.com/heurist-network/heurist-mesh-skill/main/SKILL.md \
    --slug heurist-mesh-skill \
    --category infrastructure \
    --risk-tier low \
    --source-url https://github.com/heurist-network/heurist-mesh-skill \
    --author '{"display_name": "Heurist Network", "github_username": "heurist-network"}' \
    --requires-secrets

# From a local file
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_skill \
    --file ./SKILL.md \
    --slug my-skill \
    --category defi

# From a local folder (multi-file skill — uploads as zip bundle)
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_skill \
    --dir ./my-skill-folder \
    --slug my-folder-skill \
    --category defi
```

Options:
- `--url`, `--file`, or `--dir` — source of the skill (mutually exclusive)
- `--slug` — unique identifier (required)
- `--category` — defi, infrastructure, analytics, dev-tools, etc.
- `--risk-tier` — low, medium, high
- `--source-type` — github or web_url (optional, auto-derived from URL if omitted)
- `--source-url` — source repository URL
- `--author` — JSON string with author metadata (display_name, github_username, github_profile_url, website_url)
- Capability flags: `--requires-secrets`, `--requires-private-keys`, `--requires-exchange-api-keys`, `--can-sign-transactions`, `--uses-leverage`, `--accesses-user-portfolio`

### Ingest from GitHub repo

```bash
# Single skill (SKILL.md at repo root)
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_github \
    --repo heurist-network/heurist-mesh-skill \
    --slug heurist-mesh-skill \
    --category infrastructure

# Single skill from a subfolder
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_github \
    --repo anthropics/skills \
    --path skills/webapp-testing/SKILL.md \
    --slug webapp-testing \
    --category dev-tools

# Scan mode — auto-discover all SKILL.md files in a repo
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_github \
    --repo heurist-network/heurist-mesh-skill \
    --scan \
    --slug-prefix heurist \
    --category infrastructure
```

### Approve a skill

```bash
.venv/bin/python -m mesh.skill_marketplace.scripts.approve_skill --slug heurist-mesh-skill --by admin
```

### List all skills (admin view)

```bash
# All skills
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills

# Filter by status
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills --status draft
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills --status verified
```

### Check for upstream changes

```bash
# Dry run (detect only, no notifications)
.venv/bin/python -m mesh.skill_marketplace.scripts.check_upstream --dry-run

# With Slack alerting
.venv/bin/python -m mesh.skill_marketplace.scripts.check_upstream \
    --slack-webhook https://hooks.slack.com/services/...
```

## CLI Tool (heurist-skills-cli)

Users install and manage skills using the `@heurist/skills-cli` package:

```bash
# Browse available skills
heurist-skills list --remote

# Install a skill
heurist-skills add webapp-testing

# Show skill details
heurist-skills info heurist-mesh-skill

# Check for updates
heurist-skills check-updates

# Uninstall a skill
heurist-skills remove webapp-testing
```

Repo: [heurist-network/heurist-skills-cli](https://github.com/heurist-network/heurist-skills-cli)
