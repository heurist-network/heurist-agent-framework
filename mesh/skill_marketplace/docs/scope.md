# Skill Marketplace — Project Scope & Progress

**Fully complete**: DB schema, Autonomys storage (single + folder), read-only API (6 endpoints), admin API, production wiring, upstream detection, GitHub ingestion, multi-file folder skills, auto source_type derivation, CLI tool (heurist-skills-cli), reject bug fix, verification_status enum validation
**Needs data/content**: Capabilities population for non-heurist skills, additional curated skills
**Phase 1**: Community submissions, security screening, author reputation

---

## Architecture

- **PostgreSQL** for queryable metadata (single `skills` table)
- **Autonomys Auto Drive (ai3.storage)** for immutable skill file blobs
- **Admin API** (import, approve, reject, check-upstream) + CLI scripts for ingestion, approval, listing
- **Read-only API** + **Admin API** mounted on mesh_api.py for frontend/CLI consumption
- **Forked CLI** (@heurist/skills) from vercel-labs/skills with HeuristProvider

---

## Phase 0 — MVP (Curated Verified Skills)

### P0.1 — Database schema & metadata storage

Set up PostgreSQL with a single `skills` table holding identity, source attribution, approved artifact pointers, review helpers, and timestamps. No separate skill_sources or skill_snapshots tables.

- [x] **Checkpoint 1**: `skills` table created with all spec columns (slug, name, description, skill_md_frontmatter_json, category, risk_tier, verification_status, source_type, source_url, source_path, author_json JSONB, file_url, approved_sha256, approved_at, approved_by, submitted_by, submitted_at, review_state, review_notes, reviewed_at, created_at, updated_at)
- [x] **Checkpoint 2**: Indexes on slug, category, verification_status
- [x] **Checkpoint 3**: Capabilities taxonomy columns — requires_secrets, requires_private_keys, requires_exchange_api_keys, can_sign_transactions, uses_leverage, accesses_user_portfolio (all boolean, default false)

### P0.2 — Ingestion scripts (two source types)

Support ingesting skills from web URLs (single SKILL.md) and GitHub repos (multi-skill folders). Parse YAML frontmatter, upload to Autonomys, insert as draft.

- [x] **Checkpoint 1**: Web URL ingestion — fetch SKILL.md from any URL, parse frontmatter, upload to Autonomys, insert into DB
- [x] **Checkpoint 2**: Local file ingestion — read SKILL.md from disk, same flow as URL
- [x] **Checkpoint 3**: GitHub multi-skill repo ingestion — `ingest_github.py` supports single path mode and `--scan` mode (auto-discovers all SKILL.md files via Git tree API)
- [x] **Checkpoint 4**: Auto-derive `source_type` from URL — github.com/raw.githubusercontent.com → github, else web_url. `--source-type` is now optional override
- [x] **Checkpoint 5**: Multi-file folder skill support — `--dir` flag for local folders, GitHub folder detection with hierarchy preservation, zip bundle upload to Autonomys

### P0.3 — Autonomys storage (ai3.storage)

Upload approved skill bundles to Autonomys and store CID + SHA256. Frontend/CLI fetches via public gateway URL.

- [x] **Checkpoint 1**: 3-step chunked upload working (create session → send chunks → complete)
- [x] **Checkpoint 2**: Download via public gateway with authenticated API fallback
- [x] **Checkpoint 3**: CID and SHA256 stored in DB, gateway URL returned in API responses
- [x] **Checkpoint 4**: Multi-file folder upload — `upload_folder()` bundles files into zip preserving hierarchy, uploads to Autonomys as single archive

### P0.4 — Manual verification workflow

Admin reviews imported skills and approves them. No automatic publishing.

- [x] **Checkpoint 1**: `approve_skill.py` script sets verification_status to verified with audit fields (approved_at, approved_by)
- [x] **Checkpoint 2**: `list_skills.py` script with status filter for admin overview
- [x] **Checkpoint 3**: Review checklist template — documented steps an admin follows before approving (frontmatter valid, no suspicious patterns, capabilities declared, risk tier assigned)

### P0.5 — Read-only API endpoints

Public API for frontend UI and CLI tool consumption.

- [x] **Checkpoint 1**: `GET /skills` — list with category, status, search, pagination (defaults to verified only)
- [x] **Checkpoint 2**: `GET /skills/{slug}` — full detail including frontmatter, source, audit fields
- [x] **Checkpoint 3**: `GET /skills/categories/list` — categories with counts (verified only)
- [x] **Checkpoint 4**: `POST /check-updates` — CLI sends installed skill hashes, receives approved updates
- [x] **Checkpoint 5**: `GET /skills/{slug}/download` — download skill file or folder bundle (zip), with SHA256 header
- [x] **Checkpoint 6**: `GET /skills/{slug}/files` — list files in a folder skill bundle with sizes

### P0.6 — Upstream change detection

Routine script that polls GitHub repos and web URLs to detect when source content changes, then alerts the team.

- [x] **Checkpoint 1**: GitHub detection — `check_upstream.py` + `POST /admin/skills/check-upstream` fetch SKILL.md via GitHub API, compare SHA256 against approved_sha256
- [x] **Checkpoint 2**: Web URL detection — same script/endpoint handles source_type=web_url, fetches and compares content hash
- [x] **Checkpoint 3**: Alert mechanism — Slack webhook support (`--slack-webhook`), structured log output, dry-run mode

### P0.7 — Installer CLI (heurist-skills-cli)

Built as a standalone TypeScript CLI (`@heurist/skills-cli`) pointing to our registry API. Not a fork — clean implementation tailored to our API with zero unnecessary dependencies.

- [x] **Checkpoint 1**: API client (`src/api.ts`) querying our `/skills` and `/skills/{slug}` endpoints
- [x] **Checkpoint 2**: `add <slug>` — download from `/skills/{slug}/download`, install SKILL.md or extract zip bundle to local scope (`~/.heurist/skills/` global or `.heurist/skills/` local)
- [x] **Checkpoint 3**: `list`, `list --remote`, `remove`, `info` commands — fully working
- [x] **Checkpoint 4**: `check-updates` — POSTs installed `{slug, sha256}` pairs to `/check-updates`, shows outdated skills
- [x] **Checkpoint 5**: Lock file (`~/.heurist/skills-lock.json`) tracks installed skills for update detection
- [x] **Checkpoint 6**: Capability warnings shown during `add` for risky skills (private-keys, sign-tx, leverage)
- [x] **Checkpoint 7**: Built with tsup (23.8KB bundle), dotenv support, MIT license. Repo: heurist-network/heurist-skills-cli

### P0.8 — Capabilities & risk taxonomy

Every skill declares what dangerous things it can do. Displayed on skill pages and in CLI metadata.

- [x] **Checkpoint 1**: Add boolean columns to skills table (requires_secrets, requires_private_keys, requires_exchange_api_keys, can_sign_transactions, uses_leverage, accesses_user_portfolio)
- [x] **Checkpoint 2**: Capabilities populated and verified for heurist-mesh-skill; other ingested skills (webapp-testing, mcp-builder, frontend-design, pdf-reader) are low-risk dev tools with no dangerous capabilities
- [x] **Checkpoint 3**: Return capabilities in API responses (both list and detail endpoints) — nested under `capabilities` object in SkillSummary and SkillDetail

### P0.9 — Curated skill catalog

Launch with <10 verified skills from both URL and GitHub sources.

- [x] **Checkpoint 1**: First skill ingested and verified (heurist-mesh-skill)
- [x] **Checkpoint 2**: 5 verified skills total — heurist-mesh-skill, webapp-testing, mcp-builder, frontend-design, pdf-reader (target was 5-10)
- [x] **Checkpoint 3**: All skills have category (infrastructure/dev-tools), risk_tier (low), capabilities set

### P0.10 — mesh_api.py wiring

Wire skill_marketplace into the production mesh API so endpoints are accessible at mesh.heurist.ai.

- [x] **Checkpoint 1**: Imports, lifespan hooks (init_db/close_pool), router include added to mesh_api.py
- [x] **Checkpoint 2**: Verify endpoints work on staging/production deployment — all 4 routes live on remote machine (34.122.195.244), PostgreSQL on remote, skill ingested and approved on production DB

---

## Phase 1 — Community & Tooling

### P1.1 — Self-uploaded skills (draft submission lane)

Allow community submissions via URL or GitHub that enter as draft. Team reviews and only verified skills appear in default catalog.

- [ ] **Checkpoint 1**: Public submission endpoint (POST /skills/submit) that creates draft entries
- [ ] **Checkpoint 2**: Reviewer UI/filter to view draft submissions
- [ ] **Checkpoint 3**: review_state workflow (pending → changes_requested / rejected / approved)

### P1.2 — Semi-automated security screening

Add scanning support (still approval-gated). Integrate GoPlus APIs, static checks, and optional AI-assisted diff review.

- [ ] **Checkpoint 1**: GoPlus API integration for risk signals
- [ ] **Checkpoint 2**: Static checks (suspicious patterns, known-bad domains)
- [ ] **Checkpoint 3**: AI-assisted diff review summarizing changes between versions

### P1.3 — Update visibility & review tooling

Admin UI showing update alerts, diff views, and audit trails.

- [ ] **Checkpoint 1**: "Update available" alerts from polling script displayed in admin view
- [ ] **Checkpoint 2**: Diff view between current approved artifact and latest fetched candidate
- [ ] **Checkpoint 3**: Reviewer notes and full audit trail

### P1.4 — Author reputation & provenance

Surface reputation signals: verified publisher badge, GitHub org verification, marketplace-level reputation.

- [ ] **Checkpoint 1**: Verified publisher badge logic
- [ ] **Checkpoint 2**: GitHub org verification
- [ ] **Checkpoint 3**: Reputation scoring system

### P1.5 — Installer CLI enhancements

Richer metadata display in CLI (risk tier, verification status, author reputation). Optional install bundles for first-time users.

- [ ] **Checkpoint 1**: Display risk tier and capabilities during `add`
- [ ] **Checkpoint 2**: Show verification status and author info
- [ ] **Checkpoint 3**: Bootstrap pack / install bundles

### P1.6 — Version history (optional)

Expose approved version history and rollback UI if needed.

- [ ] **Checkpoint 1**: Store version history (JSON or dedicated table)
- [ ] **Checkpoint 2**: Rollback mechanism

---

## Operational Safeguards

- No-withdrawals policy: execution skills must never request/enable withdrawals
- Auditability: always store approved_sha256, approved_at, approved_by
- Emergency response: ability to archive/delist a skill immediately, CLI respects registry state

---
