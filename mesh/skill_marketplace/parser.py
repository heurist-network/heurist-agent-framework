"""SKILL.md frontmatter parser and URL utilities.

Extracts YAML frontmatter and markdown body from SKILL.md files.
Stores the full raw frontmatter for skill_md_frontmatter_json column.
"""

from urllib.parse import urlparse

import yaml

GITHUB_HOSTS = {"github.com", "www.github.com", "raw.githubusercontent.com"}


def derive_source_type(url: str) -> str:
    """Derive source_type from a URL. GitHub domains → 'github', everything else → 'web_url'."""
    hostname = urlparse(url).hostname or ""
    return "github" if hostname in GITHUB_HOSTS else "web_url"


def parse_github_owner_repo(url: str) -> tuple[str, str] | None:
    """Extract (owner, repo) from a GitHub or raw.githubusercontent.com URL."""
    parsed = urlparse(url)
    if parsed.hostname not in GITHUB_HOSTS:
        return None
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        return None
    return parts[0], parts[1]


def parse_skill_md(content: str | bytes) -> dict:
    """Parse a SKILL.md file into name, description, full frontmatter dict, and markdown body.

    Raises ValueError if name or description are missing from frontmatter.
    """
    if isinstance(content, bytes):
        content = content.decode("utf-8")

    content = content.strip()
    if not content.startswith("---"):
        raise ValueError("SKILL.md must start with YAML frontmatter (---)")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter not properly closed with ---")

    frontmatter = yaml.safe_load(parts[1].strip()) or {}
    body = parts[2].strip()

    if "name" not in frontmatter:
        raise ValueError("SKILL.md missing required 'name' field in frontmatter")
    if "description" not in frontmatter:
        raise ValueError("SKILL.md missing required 'description' field in frontmatter")

    return {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
        "frontmatter": frontmatter,
        "body": body,
    }
