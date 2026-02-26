# Skill Marketplace

Backend module for the Heurist Mesh Skill Marketplace. Makes Web3 agent skills discoverable, verifiable, and installable.

## Directory structure

```
mesh/skill_marketplace/
├── db.py              # PostgreSQL schema + asyncpg connection pool
├── parser.py          # SKILL.md YAML frontmatter parser
├── storage.py         # Autonomys Auto Drive upload/download
├── routes.py          # Read-only FastAPI routes (mounted by mesh_api.py)
├── docs/
│   ├── README.md      # This file
│   └── scope.md       # Full project scope and checkpoint tracker
└── scripts/
    ├── ingest_skill.py    # Ingest a skill from URL or local file
    ├── approve_skill.py   # Approve a draft skill
    ├── list_skills.py     # List all skills
    └── run_standalone.py  # Standalone dev server (no mesh_api dependency)
```

## Running

### Via mesh_api.py (production)

The skill marketplace routes are automatically mounted when mesh_api.py starts. No extra setup needed.

```bash
# From repo root: /root/heurist-agent-framework
cd /root/heurist-agent-framework
uv run uvicorn mesh.mesh_api:app --host 0.0.0.0 --port 8005
```

Endpoints available at `http://localhost:8005`:
- `GET /skills` — list skills (verified only by default)
- `GET /skills/{slug}` — skill detail
- `GET /skills/categories/list` — categories with counts
- `POST /check-updates` — check for skill updates

### Standalone dev server

Run the marketplace API independently without loading mesh agents:

```bash
cd /root/heurist-agent-framework
.venv/bin/python -m mesh.skill_marketplace.scripts.run_standalone
```

This starts a FastAPI server on port 8006 with only the skill marketplace routes.

## Environment variables

Set in `.env` at the repo root:

| Variable | Required | Description |
|----------|----------|-------------|
| `SKILLS_DATABASE_URL` | Yes | PostgreSQL connection string |
| `AI3_API_KEY` | Yes | Autonomys Auto Drive API key |

## Admin scripts

All admin operations are done via CLI scripts (no admin API endpoints).

### Ingest a skill

```bash
cd /root/heurist-agent-framework

.venv/bin/python -m mesh.skill_marketplace.scripts.ingest_skill \
    --url https://raw.githubusercontent.com/org/repo/main/SKILL.md \
    --slug my-skill \
    --category infrastructure \
    --risk-tier low \
    --source-type github \
    --source-url https://github.com/org/repo \
    --author-name "Author Name" \
    --author-github "https://github.com/author" \
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
- `--author-name` — author display name
- `--author-github` — author GitHub URL
- Capability flags: `--requires-secrets`, `--requires-private-keys`, `--requires-exchange-api-keys`, `--can-sign-transactions`, `--uses-leverage`, `--accesses-user-portfolio`

### Approve a skill

```bash
.venv/bin/python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill --by admin
```

### List all skills

```bash
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills
.venv/bin/python -m mesh.skill_marketplace.scripts.list_skills --status draft
```
