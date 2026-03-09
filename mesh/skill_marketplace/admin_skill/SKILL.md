---
name: heurist-skill-marketplace-admin
description: "Admin operations for the Heurist Skill Marketplace. Use this skill when the user asks to add, ingest, approve, reject, remove, update, or list skills in the Heurist marketplace. Also triggers for checking upstream changes, updating external API dependencies, updating metrics (stars/downloads), re-ingesting skills, or any marketplace database management task. Working directory is heurist-agent-framework. Always use uv run python to run scripts."
---

# Heurist Skill Marketplace Admin

Full command reference and DB/API operations: see `references/commands.md`.

## Required env vars (`.env`)
- `SKILLS_DATABASE_URL` — PostgreSQL connection string
- `INTERNAL_API_KEY` — Admin HTTP endpoint key
- `AI3_API_KEY` — Autonomys Auto Drive storage key
- `GITHUB_TOKEN` — (optional) GitHub API rate limits

## Standard Workflow: Add a Skill End-to-End

```bash
# 1. Ingest from GitHub URL
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill \
  --category Stocks \
  --label analytics \
  --risk-tier low \
  --source-url https://github.com/OWNER/REPO \
  --author '{"display_name": "Name", "github_username": "username"}'

# 2. Check it's in DB as draft
uv run python -m mesh.skill_marketplace.scripts.list_skills --status draft

# 3. Approve
uv run python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill

# 4. Confirm live
uv run python -m mesh.skill_marketplace.scripts.list_skills --status verified
```

## Key Ingest Flags

| Flag | Purpose |
|---|---|
| `--label analytics` | Repeatable secondary label; use for overlapping capability/domain metadata |
| `--source-path skills/my-skill` | Subfolder in multi-skill repos |
| `--external-api-dependency Name` | Repeat for each external API (e.g. `CoinGecko`) |
| `--requires-secrets` | Skill needs API tokens/env vars |
| `--requires-private-keys` | Skill accesses private keys |
| `--requires-exchange-api-keys` | Needs exchange credentials |
| `--can-sign-transactions` | Skill signs on-chain txs |
| `--uses-leverage` | Leveraged trading |
| `--accesses-user-portfolio` | Reads user portfolio data |
| `--update` | Update existing skill in place (preserves id, download_count, star_count, created_at) |

## Name Check After Ingest

The `name` field is parsed from SKILL.md frontmatter and may be generic (e.g., `tools`, `gas`). Always check the ingest log output. Fix ambiguous names before approving — use the DB update snippet in `references/commands.md`.

Good naming: `gas` → `Ethereum Gas Tracker`, `tools` → `Ethereum Developer Tools`, `opensea` → `OpenSea NFT API`

## Primary Categories
`Stocks`, `Macro`, `Crypto`, `Developer`, `Social`

Use `category` only for the single top-level browse bucket.

Use `labels` for overlapping metadata such as:
`analytics`, `signals`, `screening`, `portfolio`, `research`, `execution`, `mcp`, `options`, `defi`, `ethereum`, `news`, `twitter`

Do not duplicate built-in capability fields with labels. These are already first-class DB columns:
`requires_secrets`, `requires_private_keys`, `requires_exchange_api_keys`, `can_sign_transactions`, `uses_leverage`, `accesses_user_portfolio`

## Risk Tiers
`low` (read-only/analysis), `medium` (writes, no keys), `high` (keys, signing, leverage)

## Common Quick Commands

```bash
# List skills
uv run python -m mesh.skill_marketplace.scripts.list_skills
uv run python -m mesh.skill_marketplace.scripts.list_skills --status draft
uv run python -m mesh.skill_marketplace.scripts.list_skills --status verified

# Update category + labels
curl -X PATCH https://mesh.heurist.xyz/admin/skills/SKILL_ID/taxonomy \
  -H "X-API-Key: $INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "Crypto", "labels": ["defi", "analytics"]}'

# Approve
uv run python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill

# Check upstream changes
uv run python -m mesh.skill_marketplace.scripts.check_upstream
```

## Update Skill Content (Preferred)

Use `--update` to update an existing skill in place — no need to delete first. Preserves `id`, `download_count`, `star_count`, and `created_at`. Resets status to `draft` so you must re-approve.

```bash
# 1. Update from source
uv run python -m mesh.skill_marketplace.scripts.ingest_skill \
  --url https://raw.githubusercontent.com/OWNER/REPO/main/SKILL.md \
  --slug my-skill \
  --category Crypto \
  --label defi \
  --source-url https://github.com/OWNER/REPO \
  --update

# 2. Re-approve
uv run python -m mesh.skill_marketplace.scripts.approve_skill --slug my-skill
```

## Other Operations

For reject, remove, update metrics, update external API dependencies, local file/dir ingest, and Admin HTTP API calls — see `references/commands.md`.
