"""SKILL.md frontmatter parser.

Extracts YAML frontmatter and markdown body from SKILL.md files.
Stores the full raw frontmatter for skill_md_frontmatter_json column.
"""

import yaml


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
