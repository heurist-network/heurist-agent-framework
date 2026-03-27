"""SKILL.md frontmatter parser and URL utilities.

Extracts YAML frontmatter and markdown body from SKILL.md files.
Stores the full raw frontmatter for skill_md_frontmatter_json column.
Provides shared GitHub folder detection used by admin_routes and ingest_skill.
"""

import io
import logging
import os
import tarfile
from pathlib import PurePosixPath
from urllib.parse import urlparse

import aiohttp
import yaml

logger = logging.getLogger("SkillMarketplace")

GITHUB_HOSTS = {"github.com", "www.github.com", "raw.githubusercontent.com"}
IGNORED_SKILL_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    ".git",
}
IGNORED_SKILL_FILE_NAMES = {
    ".DS_Store",
}
IGNORED_SKILL_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
}


def is_ignored_skill_path(path: str) -> bool:
    """Return True for generated files/directories that should not be ingested."""
    pure_path = PurePosixPath(path)
    if any(part in IGNORED_SKILL_DIR_NAMES for part in pure_path.parts):
        return True
    if pure_path.name in IGNORED_SKILL_FILE_NAMES:
        return True
    return pure_path.suffix in IGNORED_SKILL_SUFFIXES


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


def derive_github_folder_prefix(url: str, source_path: str | None = None) -> str | None:
    """Derive the folder prefix within a GitHub repo from a URL.

    If source_path is provided, use it directly. Otherwise, parse from the URL path.
    Returns the folder prefix (e.g. "skills/my-skill/") or "" for repo root.
    Returns None if the URL is not a GitHub URL.
    """
    parsed = urlparse(url)
    if parsed.hostname not in GITHUB_HOSTS:
        return None

    if source_path:
        normalized = source_path.rstrip("/")
        if normalized.endswith("/SKILL.md"):
            normalized = normalized[:-len("/SKILL.md")]
        elif normalized == "SKILL.md":
            normalized = ""
        return normalized + "/" if normalized else ""

    parts = parsed.path.strip("/").split("/")

    if parsed.hostname == "raw.githubusercontent.com":
        # Format: /owner/repo/branch/path/to/SKILL.md
        if len(parts) < 4:
            return None
        file_parts = parts[3:]  # everything after branch
    else:
        # Format: /owner/repo/blob/branch/path/to/SKILL.md
        if len(parts) < 5:
            return None
        file_parts = parts[4:]  # everything after branch

    # Remove the filename (SKILL.md) to get the directory
    if len(file_parts) <= 1:
        return ""  # file is at repo root
    return "/".join(file_parts[:-1]) + "/"


async def fetch_github_folder_files(
    url: str,
    source_path: str | None = None,
) -> dict[str, bytes] | None:
    """Fetch all files in a GitHub folder skill via the GitHub tree API.

    Works for both root-level repos (source_path=None) and subfolder skills.
    Returns dict of {relative_path: content} if folder has >1 file, None otherwise.
    """
    owner_repo = parse_github_owner_repo(url)
    if not owner_repo:
        return None

    folder_prefix = derive_github_folder_prefix(url, source_path)
    if folder_prefix is None:
        return None

    owner, repo = owner_repo
    github_token = os.getenv("GITHUB_TOKEN")
    gh_headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        gh_headers["Authorization"] = f"token {github_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1",
            headers=gh_headers,
        ) as tree_resp:
            if tree_resp.status != 200:
                logger.warning(f"GitHub tree API returned {tree_resp.status} for {owner}/{repo}")
                return None
            tree_data = await tree_resp.json()

        if folder_prefix == "":
            # Repo root — all blobs are candidates
            file_paths = [
                item["path"] for item in tree_data.get("tree", [])
                if item["type"] == "blob" and not is_ignored_skill_path(item["path"])
            ]
        else:
            file_paths = [
                item["path"] for item in tree_data.get("tree", [])
                if item["type"] == "blob"
                and item["path"].startswith(folder_prefix)
                and not is_ignored_skill_path(item["path"])
            ]

        if len(file_paths) <= 1:
            return None  # single file, not a folder skill

        logger.info(f"detected folder skill: {len(file_paths)} files in {owner}/{repo}/{folder_prefix or '(root)'}")

        # Download repo as tarball (1 request) instead of per-file fetching to avoid rate limits
        tarball_url = f"https://api.github.com/repos/{owner}/{repo}/tarball"
        async with session.get(tarball_url, headers=gh_headers) as tar_resp:
            if tar_resp.status != 200:
                logger.warning(f"tarball download failed for {owner}/{repo}: HTTP {tar_resp.status}")
                return None
            tarball_bytes = await tar_resp.read()

        folder_files = {}
        file_paths_set = set(file_paths)
        with tarfile.open(fileobj=io.BytesIO(tarball_bytes), mode="r:gz") as tar:
            for member in tar.getmembers():
                if not member.isfile():
                    continue
                # Tarball paths are prefixed with "{owner}-{repo}-{sha}/"
                parts = member.name.split("/", 1)
                if len(parts) < 2:
                    continue
                repo_path = parts[1]
                if repo_path not in file_paths_set:
                    continue
                f = tar.extractfile(member)
                if f:
                    rel_path = repo_path[len(folder_prefix):] if folder_prefix else repo_path
                    folder_files[rel_path] = f.read()

        logger.info(f"extracted {len(folder_files)} files from tarball for {owner}/{repo}")

    return folder_files if len(folder_files) > 1 else None


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
