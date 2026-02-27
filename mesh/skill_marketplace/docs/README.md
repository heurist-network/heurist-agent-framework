# Skill Marketplace

Backend module for the Heurist Mesh Skill Marketplace. Makes Web3 agent skills discoverable, verifiable, and installable.

## Directory structure

```
mesh/skill_marketplace/
├── db.py              # PostgreSQL schema + asyncpg connection pool
├── parser.py          # SKILL.md YAML frontmatter parser
├── storage.py         # Autonomys Auto Drive upload/download
├── routes.py          # Read-only FastAPI routes (mounted by mesh_api.py)
├── admin_routes.py    # Admin API routes (import, approve, reject, check-upstream)
├── docs/
│   ├── README.md      # This file
│   └── scope.md       # Full project scope and checkpoint tracker
└── scripts/
    ├── ingest_skill.py    # Ingest a skill from URL or local file
    ├── ingest_github.py   # Ingest skill(s) from a GitHub repo (single or scan mode)
    ├── approve_skill.py   # Approve a draft skill
    ├── list_skills.py     # List all skills
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
- `GET /skills` — list skills (verified only by default, supports category/search/pagination)
- `GET /skills/{slug}` — skill detail with frontmatter, capabilities, source attribution
- `GET /skills/categories/list` — categories with counts
- `POST /check-updates` — CLI sends installed skill hashes, receives approved updates

**Admin:**
- `POST /admin/skills/import` — import a skill from URL (fetch, parse, upload to Autonomys, insert as draft)
- `POST /admin/skills/{id}/approve` — approve a draft skill
- `POST /admin/skills/{id}/reject` — reject a skill
- `POST /admin/skills/check-upstream` — poll all verified skills for upstream source changes

## Environment variables

Set in `.env` at the repo root:

| Variable | Required | Description |
|----------|----------|-------------|
| `SKILLS_DATABASE_URL` | Yes | PostgreSQL connection string |
| `AI3_API_KEY` | Yes | Autonomys Auto Drive API key |
| `GITHUB_TOKEN` | No | GitHub personal access token (raises API rate limits for upstream checks) |

## CLI Scripts

### Ingest a skill from URL/file

```bash
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_skill \
    --url https://raw.githubusercontent.com/heurist-network/heurist-mesh-skill/main/SKILL.md \
    --slug heurist-mesh-skill \
    --category infrastructure \
    --risk-tier low \
    --source-type github \
    --source-url https://github.com/heurist-network/heurist-mesh-skill \
    --author '{"display_name": "Heurist Network", "github_username": "heurist-network"}' \
    --requires-secrets \
    --requires-private-keys
```

Options:
- `--url` or `--file` — source of the SKILL.md file
- `--slug` — unique identifier (required)
- `--category` — defi, infrastructure, analytics, etc.
- `--risk-tier` — low, medium, high
- `--source-type` — github or web_url
- `--source-url` — source repository URL
- `--author` — JSON string with author metadata (display_name, github_username, github_profile_url, website_url)
- Capability flags: `--requires-secrets`, `--requires-private-keys`, `--requires-exchange-api-keys`, `--can-sign-transactions`, `--uses-leverage`, `--accesses-user-portfolio`

### Ingest from GitHub repo

```bash
# Single skill
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_github \
    --repo heurist-network/heurist-mesh-skill \
    --slug heurist-mesh-skill \
    --category infrastructure

# Single skill from a subfolder
.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_github \
    --repo heurist-network/heurist-mesh-skill \
    --path skills/defi/SKILL.md \
    --slug defi-skill \
    --category defi

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

### List all skills

```bash
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills --status draft
```

### Check for upstream changes

```bash
# Dry run (detect only, no notifications)
.venv/bin/python -m mesh.skill_marketplace.scripts.check_upstream --dry-run

# With Slack alerting
.venv/bin/python -m mesh.skill_marketplace.scripts.check_upstream \
    --slack-webhook https://hooks.slack.com/services/...
```
