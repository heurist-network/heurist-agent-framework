# Skill Review Checklist

Steps an admin must follow before approving a skill via `approve_skill.py` or `POST /admin/skills/{id}/approve`.

---

## 1. Frontmatter Validation

- [ ] SKILL.md has valid YAML frontmatter (name, description present)
- [ ] Name is descriptive and not misleading
- [ ] Description accurately reflects what the skill does
- [ ] Category is assigned and correct (defi, infrastructure, analytics, etc.)
- [ ] Risk tier is assigned (low, medium, high)

## 2. Capabilities Declaration

- [ ] `requires_secrets` set correctly (does it need API keys at runtime?)
- [ ] `external_api_dependencies` set correctly (e.g. `["OKX", "CoinGecko"]`), even if upstream `SKILL.md` does not declare them
- [ ] `requires_private_keys` set correctly (does it access wallet private keys?)
- [ ] `requires_exchange_api_keys` set correctly (does it use CEX API keys?)
- [ ] `can_sign_transactions` set correctly (does it sign on-chain transactions?)
- [ ] `uses_leverage` set correctly (does it involve leveraged positions?)
- [ ] `accesses_user_portfolio` set correctly (does it read user holdings?)
- [ ] Capabilities are not under-declared (skill doesn't do more than declared)

## 3. Security Screening

- [ ] No hardcoded secrets, private keys, or credentials in source
- [ ] No suspicious outbound URLs or domains
- [ ] No obfuscated code or encoded payloads
- [ ] No withdrawal or fund-transfer logic (no-withdrawals policy)
- [ ] No shell execution or arbitrary code eval patterns
- [ ] Dependencies (if any) are from known, trusted sources

## 4. Source Attribution

- [ ] `source_url` points to a valid, accessible repository or URL
- [ ] `source_path` is correct for multi-skill repos
- [ ] Author information is accurate (GitHub username matches repo owner/contributor)
- [ ] Source type (github/web_url) is correct

## 5. Folder Skills (multi-file bundles)

- [ ] All files in the bundle are necessary and relevant
- [ ] No unexpected file types (.exe, .bin, compiled artifacts)
- [ ] Folder hierarchy is logical and clean
- [ ] SKILL.md is present at the root of the folder

## 6. Content Quality

- [ ] Skill description is clear enough for end-users
- [ ] Frontmatter fields are complete (not just name/description)
- [ ] No placeholder or template content left in

## 7. Final Approval

- [ ] SHA256 hash recorded matches the uploaded artifact
- [ ] Approve with: `python -m mesh.skill_marketplace.scripts.approve_skill --slug <slug>`
- [ ] Verify the skill appears in `GET /skills` after approval
