# Heurist Mesh Skills Marketplace — P0/P1 Requirements

## Summary of decisions (from team discussions)

* **Storage**: Use **ai3.storage** (Autonomys Auto Drive) for immutable file blobs (skill bundles). Use **PostgreSQL** for metadata.

  * ai3.storage: *instant finality*, bytes match after upload, and **gateway URL works out of the box** (UI can load files directly without client SDK).
* **Sources supported**:

  * **Single-file skill**: `SKILL.md` hosted on a URL (e.g., `https://.../skill.md`).
  * **GitHub repo**: repo may contain **multiple skill folders** (each folder = one skill). Extra non-skill files (README/LICENSE/etc.) that are out of scope.
* **Installer / UX**: Fork **vercel-labs/skills** CLI (MIT) and point it to our registry API.

  * Target install UX: `npx @heurist/skills add <skill-slug>`
  * Reuse CLI update-check mechanism (hash POST to `check-updates` endpoint) but **our backend controls versions**.
* **Version control policy**:

  * **No automatic updates** pulled from upstream sources (GitHub/web) to users.
  * Any upstream change triggers **manual approval** per version by Heurist team (P0).
  * Team learns about upstream changes via a **routine script** (polling).
* **Capabilities & Risk**: Must include (at minimum):

  * Requires secrets: yes/no
  * Requires private keys: yes/no
  * Can place orders: yes/no
  * (We will NOT use overly generic labels like “reads internet / writes files / writes code”.)

---

## Product goal

Create a **crypto-focused Skill Marketplace** that makes high-quality Web3 skills:

* discoverable (better than general directories)
* trustworthy (manual verification and controlled updates)
* easy to install (via a familiar CLI)

This marketplace complements existing Heurist Mesh MCP infra by providing a **distribution + trust + metadata layer** for curated and (later) community skills.

## Non-goals (for P0)

* Automatic update pulling from source repositories/websites.
* Full version history UI and rollback UX.
* Fully automated security screening pipeline (we start with manual verification).
* Overly broad capability labels (keep crypto-specific and actionable).

---

## Proposed high-level architecture

### Components

1. **Registry API** (Heurist)

   * List skills, fetch skill metadata
   * Provide metadata plus a canonical download endpoint for approved artifacts
   * Update-check endpoint for CLI
   * Admin endpoints for ingestion/review/publish

2. **Storage**

   * **ai3.storage**: canonical skill artifacts (single-file or folder bundle)
   * **PostgreSQL**: metadata (skill listing, inline author metadata, verification status, current approved artifact)

3. **Admin console / internal UI** (can be minimal P0)

   * Import from URL / GitHub
   * Preview + manual review checklist
   * Publish approved version
   * See “update available” signals from polling script

4. **Installer CLI** (do not add in heurist-agent-framework. to be forked from vercel-labs/skills)

   * Add a **Heurist provider**
   * `add` installs a skill into the user’s chosen agent skills directory
   * `check-updates` talks to our backend

---

## Data model (PostgreSQL)

> Constraint: **Do not use** `skill_sources` or `skill_snapshots` tables.

### Table: `skills`

Single table representing the marketplace listing and current approved artifact.
P0 keeps only publish-time fields, with author attribution inlined.

**Skill identity, display, and lifecycle**

* `id` (pk)
* `slug` (unique)
* `name` (from SKILL.md)
* `description` (from SKILL.md)
* `skill_md_frontmatter_json` (jsonb) — raw parsed YAML frontmatter (for future portability)
* `category` (frontend taxonomy)
* `risk_tier` (frontend taxonomy)
* `verification_status` enum: `draft` | `verified` | `archived`

**Source attribution**

* `source_type` enum: `github` | `web_url`
* `source_url` (repo URL or SKILL.md URL)
* `source_path` (nullable) — for GitHub multi-skill repos, the folder path for this skill
* `author_json` (jsonb) — inline author metadata, e.g. `display_name`, `author_type`, `github_username`, `github_profile_url`, `website_url`

**Approved artifact pointers**

* `file_url` (string) — gateway URL for the approved `SKILL.md` file
* `is_folder` (boolean) — whether this skill is a multi-file folder skill
* `folder_manifest_json` (jsonb, nullable) — for folder skills, maps relative file paths to ai3.storage CIDs
* `approved_sha256` (string) — content hash for integrity
* `approved_at` (timestamp)
* `approved_by` (string/user id)

> Canonical install/download artifact: `GET /skills/:slug/download`.
> For single-file skills it returns raw `SKILL.md`; for folder skills it returns a zip assembled server-side from `folder_manifest_json`.
> `file_url` is useful metadata and a direct gateway pointer for `SKILL.md`, but it is not the canonical install artifact for folder skills.

**P1 submission/review helpers (optional fields; same table)**

* `submitted_by` (string/user id, nullable)
* `submitted_at` (timestamp, nullable)
* `review_state` enum: `pending` | `changes_requested` | `rejected` | `approved` (nullable)
* `review_notes` (text, nullable)
* `reviewed_at` (timestamp, nullable)

**Timestamps**

* `created_at`, `updated_at`

> Note: Keeping `review_state` separate from `verification_status` lets us preserve a simple public lifecycle (`draft`/`verified`/`archived`) while still handling moderation workflows in P1.

---

## Capabilities & Risk taxonomy (for skill pages + CLI metadata)

We already have:

* **Requires secrets** (yes/no)
* **Requires private keys** (yes/no)
* **Requires exchange API keys** (yes/no)
* **Can sign transactions** (yes/no)
* **Uses leverage** (yes/no)
* **Accesses user portfolio** (yes/no)

---

# P0 Requirements (MVP)

> **P0 must be minimal**: curated verified skills + basic storage.

## P0.1 Marketplace catalog (curated-first)

* Launch with **<10 curated, verified skills**.
* Public catalog + detail pages:

  * Name, description, category
  * Verification status badge
  * Risk tier + capabilities
  * Author attribution (GitHub author or source website)
  * Install instructions via CLI and manual download
* Visibility policy:

  * `GET /skills` defaults to **verified** skills for the main catalog experience
  * `GET /skills` may also return `draft` or `archived` skills when a `verification_status` filter is explicitly requested
  * `GET /skills/:slug` may return a skill regardless of verification status
  * Frontend marketplace pages should treat **verified** as the default public browsing surface; unverified visibility is acceptable for internal tooling, direct-link previews, or future reviewer workflows

## P0.2 Ingestion supports two source types

* **Web URL single-file SKILL.md**

  * Fetch file
  * Normalize to a standard bundle (e.g., folder with `SKILL.md`)
* **GitHub multi-skill repo**

  * Admin selects skill folder path
  * Ingest only the folder content relevant to the skill
  * Ignore non-skill repo files unless inside the selected folder

## P0.3 Storage (ai3.storage + Postgres)

* On publish:

  * Upload approved skill files to **ai3.storage**
  * Store `file_url` + `approved_sha256` in Postgres
  * For folder skills, also store `folder_manifest_json` so the backend can assemble a zip on download
* UI/CLI should use `GET /skills/:slug/download` as the canonical install/download endpoint.
* Gateway URLs remain useful for direct file access and inspection (`file_url` and `/skills/:slug/files`), but should not be treated as the sole install contract across all skill types.

## P0.4 Manual verification workflow (required)

* Admin workflow:

  1. Import from source
  2. Manual review checklist
  3. Approve and publish `file_url` / folder manifest metadata + `approved_sha256` + audit fields (`approved_at`, `approved_by`)

## P0.5 Controlled updates (no automatic updates)

* Rules:

  * Never auto-update the approved artifact metadata when upstream changes.
  * CLI updates must only pull **approved** versions from our registry.

## P0.6 Routine script for upstream change detection

* A scheduled routine script (daily/weekly) that:

  * **GitHub**: checks the latest commit SHA for the relevant path/repo
  * **Web URL**: checks content hash (and optionally ETag/Last-Modified)
  * If changed: alert the team (Slack/email) for manual review

## P0.7 Installer CLI fork (Heurist provider)

* Fork vercel-labs/skills (TypeScript).
* Add provider: `HeuristProvider`

  * Query our registry API for metadata
  * Download installable artifact via `GET /skills/:slug/download`
  * Install into the user’s target skills directory
* CLI commands (P0):

  * `add <skill>`
  * `list`
  * `remove <skill>`
  * `check-updates` (points to our backend; no auto-apply without approved versions)

## P0.8 Registry API endpoints (minimum)

* `GET /skills` — list skills (defaults to verified; may include other statuses when explicitly filtered)
* `GET /skills/:slug` — skill detail incl. capabilities, risk tier, `file_url`, and folder metadata when applicable; may return unverified skills
* `GET /skills/:slug/download` — canonical approved artifact download endpoint (raw `SKILL.md` for single-file skills, zip bundle for folder skills)
* `POST /check-updates` — accept installed skill hashes; respond with available **approved** update(s)
* Admin-only:

  * `POST /admin/skills/import` (URL or GitHub)
  * `POST /admin/skills/:id/approve`
  * `POST /admin/skills/:id/reject`

---

# P1 Requirements (near-term)

## P1.1 Self-uploaded skills (draft submission lane)

* Allow community submissions (URL or GitHub) that enter **Draft**.
* Team review updates `review_state`; only **Verified** skills appear in the default catalog.
* Optional filter/toggle in UI for internal reviewers to view draft submissions.

## P1.2 Semi-automated security screening

* Add scanning support (still **approval-gated**):

  * Integrate GoPlus APIs for risk signals
  * Add basic static checks (suspicious patterns, known-bad domains)
  * Optional AI-assisted “diff review” summarizing changes between versions

## P1.3 Better update visibility + review tooling

* Admin UI shows:

  * “Update available” alerts from the routine polling workflow
  * Diff view between current approved artifact and latest fetched candidate
  * Reviewer notes and audit trail

## P1.4 Author reputation & provenance

* Store and surface reputation signals:

  * Verified publisher badge
  * GitHub org verification
  * Marketplace-level reputation score

## P1.5 Installer enhancements

* Support richer metadata display in CLI:

  * risk tier, verification status, author reputation
* Optional: “install bundles” (bootstrap pack) for first-time users.

## P1.6 (Optional) Version history as first-class feature

* Expose approved version history + rollback UI.
* If needed, introduce a dedicated versions table later (but not required for P1 if JSON history suffices).

---

## Operational notes & safeguards

* **No withdrawals** policy (recommended): execution skills must never request/enable withdrawals.
* **Auditability**: always store `approved_sha256`, `approved_at`, `approved_by`.
* **Emergency response**: ability to delist/disable a skill immediately (set `archived`), and CLI should respect registry state.

---

## Acceptance criteria (CTO checkpoint)

### P0 is complete when:

* We can publish a curated set of verified skills (<10) from both URL and GitHub sources.
* Each published skill is stored in ai3.storage and is installable through the registry download endpoint, with gateway-backed file access available for direct inspection.
* The CLI installs skills from our registry and can check for approved updates.
* Upstream changes do not affect users until Heurist team approves a new version.
* Routine script detects upstream changes and alerts the team.
