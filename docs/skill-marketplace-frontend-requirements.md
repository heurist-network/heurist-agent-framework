# Skill Marketplace Frontend Requirements

## Goal

Build the P0 frontend for the Skill Marketplace with two primary user flows:

1. A **list page** that shows all marketplace skills in a responsive grid.
2. A **detail page** for a single skill where the user can:
   - view skill metadata
   - browse the skill's files
   - preview file contents
   - download the skill

This document is intentionally aligned with the current backend implementation in `mesh/skill_marketplace/routes.py`.

---

## Scope

### In scope

- Public marketplace list view
- Public skill detail view
- File navigation and file preview for verified skills
- Download action for verified skills

### Out of scope

- Admin review UI
- Skill submission UI
- Version history UI
- Diff view between versions
- Rich editing of skill files

---

## Page 1: Skill List View

### Purpose

Let users browse the marketplace and discover available skills.

### UX requirements

- Show skills in a **grid layout**.
- Each card should be clickable and route to the skill detail page.
- Default experience should show **verified** skills only.
- Support search and category filtering.
- Support pagination or incremental loading.

### Card content

Each skill card should display:

- `name`
- `description`
- `category`
- `risk_tier`
- `verification_status`
- author display name if available
- capability/risk badges when useful

### Recommended interactions

- Search box for name/description
- Category filter using category counts
- Optional status filter for internal/testing use only

### Backend endpoints

- `GET /skills`
- `GET /skills/categories/list`

### API notes

- `GET /skills` defaults to `verification_status=verified`.
- `GET /skills` may return `draft` or `archived` skills if `verification_status` is explicitly supplied.
- Marketplace FE should treat **verified** as the default browsing surface.

---

## Page 2: Skill Detail View

### Purpose

Let users inspect one skill in detail before downloading or installing it.

### Main sections

The detail page should include:

- skill header
- description and metadata
- source attribution
- capabilities and risk information
- file browser
- file preview panel
- download action

### Metadata to display

Display at minimum:

- `name`
- `slug`
- `description`
- `category`
- `risk_tier`
- `verification_status`
- author information
- `source_type`
- `source_url`
- `source_path`
- `approved_at`
- `approved_by`
- capability flags

### Download behavior

- Primary download action should call `GET /skills/{slug}/download`.
- For single-file skills, backend returns raw `SKILL.md`.
- For folder skills, backend returns a zip assembled server-side.
- Frontend should treat this endpoint as the **canonical download/install action**.

### File browser behavior

- Use `GET /skills/{slug}/files` to load the file list.
- Show files in a simple file tree or flat path list.
- Clicking a file should load `GET /skills/{slug}/files/{path}`.
- The file browser should support at least:
  - `SKILL.md`
  - `.py`
  - `.js`
  - `.ts`
  - `.json`
  - `.yaml` / `.yml`
  - `.txt`

### File preview behavior

- Markdown files can be rendered as formatted markdown or plain text.
- Code/text files can be rendered as plain text with syntax highlighting on the frontend.
- The backend currently returns `application/octet-stream` for non-Markdown files, so the frontend should not rely on response MIME type alone for preview decisions.
- Preview decisions should be based primarily on file extension.

### Verified-only caveat

- `GET /skills/{slug}` may return unverified skills.
- `GET /skills/{slug}/files`
- `GET /skills/{slug}/files/{path}`
- `GET /skills/{slug}/download`

These file and download endpoints currently require `verification_status = 'verified'`.

Frontend implication:

- For the public marketplace flow, the detail page should primarily be used for verified skills.
- If the frontend opens an unverified skill detail, file browsing and download may return `404` and should be handled gracefully.

### Backend endpoints

- `GET /skills/{slug}`
- `GET /skills/{slug}/files`
- `GET /skills/{slug}/files/{path}`
- `GET /skills/{slug}/download`

---

## Data Contract Summary

### List response

`GET /skills` returns:

- `skills`: array of skill summaries
- `total`: total number of matching skills

Each skill summary includes:

- `id`
- `slug`
- `name`
- `description`
- `category`
- `risk_tier`
- `verification_status`
- `author`
- `file_url`
- `capabilities`

### Detail response

`GET /skills/{slug}` returns:

- all summary fields
- `skill_md_frontmatter_json`
- `source_type`
- `source_url`
- `source_path`
- `approved_sha256`
- `approved_at`
- `approved_by`
- `is_folder`
- `folder_manifest`
- `created_at`
- `updated_at`

### File list response

`GET /skills/{slug}/files` returns:

- `slug`
- `is_folder`
- `file_count`
- `files`

Each file entry currently includes:

- `path`
- `cid`
- `gateway_url`

---

## Empty, Loading, and Error States

### List page

- Loading skeleton for grid cards
- Empty state when no skills match search/filter
- Error state when API request fails

### Detail page

- Loading state for metadata and file list
- Empty file state if no files are available
- File preview error state if a file request fails
- Download error state if download request fails

### Not found handling

- If `GET /skills/{slug}` returns `404`, show a not-found page.
- If the skill detail loads but file/download endpoints fail because the skill is unverified, show metadata but disable preview/download actions with a clear message.

---

## Responsive Requirements

- Grid should work on desktop and mobile.
- On desktop, detail page should prefer a two-panel layout:
  - left: file list
  - right: file preview
- On mobile, file list and preview can stack vertically.

---

## Suggested Frontend Routing

- `/skills` for the marketplace list page
- `/skills/:slug` for the skill detail page

---

## Implementation Notes

- Use `GET /skills` as the main source for the marketplace homepage.
- Use `GET /skills/categories/list` to populate category filters.
- Use `GET /skills/{slug}` first on the detail page, then load files separately.
- Treat `GET /skills/{slug}/download` as the only canonical download/install endpoint.
- Do not assume `file_url` is the correct direct download artifact for folder skills.
- Do not assume non-Markdown preview responses will have a text MIME type.

