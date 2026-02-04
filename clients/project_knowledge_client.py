"""
Client for interacting with the project knowledge database.
Uses simple SQL functions with cascading logic handled in Python.
"""

import asyncio
import logging
import os
import re
from typing import Any, Dict, List, Optional

import asyncpg
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("POSTGRESQL_URL")

# Common suffix words that can be stripped from queries
# Must match the suffixes in strip_crypto_suffix SQL function
SUFFIX_WORDS = {
    "finance",
    "labs",
    "protocol",
    "network",
    "dao",
    "token",
    "coin",
    "ai",
    "chain",
    "swap",
    "dex",
    "defi",
    "exchange",
    "capital",
    "ventures",
}


class ProjectKnowledgeClient:
    """Client for querying project knowledge database with deterministic functions."""

    _pool: Optional[asyncpg.Pool] = None
    _lock = asyncio.Lock()

    @classmethod
    async def _get_pool(cls) -> asyncpg.Pool:
        """Get or create connection pool (thread-safe, lazy initialization)."""
        if cls._pool is None:
            async with cls._lock:
                if cls._pool is None:
                    if not DATABASE_URL:
                        raise ValueError("POSTGRESQL_URL environment variable is required")
                    cls._pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
                    logger.info("Created database connection pool")
        return cls._pool

    @classmethod
    async def connect(cls):
        """Explicitly initialize connection pool."""
        await cls._get_pool()

    @classmethod
    async def close(cls):
        """Close connection pool."""
        if cls._pool:
            async with cls._lock:
                if cls._pool:
                    await cls._pool.close()
                    cls._pool = None
                    logger.info("Closed database connection pool")

    @staticmethod
    def _parse_twitter_handle(raw_input: str) -> str:
        """
        Parse Twitter handle from various input formats.

        Handles:
        - @handle -> handle
        - https://x.com/handle -> handle
        - https://twitter.com/handle -> handle
        - x.com/handle -> handle
        - handle -> handle
        """
        raw_input = raw_input.strip()

        # Remove @ prefix
        if raw_input.startswith("@"):
            return raw_input[1:].lower()

        # Extract from full URL
        match = re.match(r"^https?://(x\.com|twitter\.com)/([^/?]+)", raw_input, re.IGNORECASE)
        if match:
            return match.group(2).lower()

        # Extract from URL without https://
        match = re.match(r"^(x\.com|twitter\.com)/([^/?]+)", raw_input, re.IGNORECASE)
        if match:
            return match.group(2).lower()

        return raw_input.lower()

    @staticmethod
    def _strip_suffix_word(query: str) -> Optional[str]:
        """
        Strip common suffix words from query for fallback matching.

        Returns stripped query if applicable, None otherwise.

        Examples:
            "avalon finance" -> "avalon"
            "perle labs" -> "perle"
            "world liberty" -> "world"  (strips last word even if not in SUFFIX_WORDS)
            "ethereum" -> None (single word, nothing to strip)
        """
        query_lower = query.lower().strip()
        words = query_lower.split()

        if len(words) < 2:
            return None  # Single word, nothing to strip

        last_word = words[-1]

        # If last word is a known suffix, strip it
        if last_word in SUFFIX_WORDS:
            return " ".join(words[:-1])

        # Also strip last word for any multi-word query (fallback)
        return " ".join(words[:-1])

    async def get_project_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get project by exact symbol match.

        Args:
            symbol: Token symbol (case-insensitive)

        Returns:
            Project details dict or None if not found
        """
        if not symbol or not symbol.strip():
            return None

        pool = await self._get_pool()

        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM get_project_by_symbol($1)", symbol)

            if not row:
                return None

            project = dict(row)
            if self._should_exclude_project(project):
                return None

            return self._format_project(project)

    async def get_project_by_twitter(self, handle: str) -> Optional[Dict[str, Any]]:
        """
        Get project by Twitter/X handle (exact match).

        Args:
            handle: Twitter handle (with or without @, or full URL)

        Returns:
            Project details dict or None if not found
        """
        if not handle or not handle.strip():
            return None

        # Parse handle in Python
        clean_handle = self._parse_twitter_handle(handle)

        pool = await self._get_pool()

        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM get_project_by_twitter($1)", clean_handle)

            if not row:
                return None

            project = dict(row)
            if self._should_exclude_project(project):
                return None

            return self._format_project(project)

    async def get_project_by_contract(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Get project by contract address (exact match).

        Args:
            address: Contract address (case-insensitive)

        Returns:
            Project details dict or None if not found
        """
        if not address or not address.strip():
            return None

        pool = await self._get_pool()

        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM get_project_by_contract($1)", address)

            if not row:
                return None

            project = dict(row)
            if self._should_exclude_project(project):
                return None

            return self._format_project(project)

    async def get_project_by_name(
        self,
        name: str,
        min_prefix_len: int = 3,
        min_trigram_len: int = 4,
        trigram_threshold: float = 0.3,
    ) -> Optional[Dict[str, Any]]:
        """
        Get project by name using cascading match strategy:
        1. Exact match
        2. Prefix match (if query >= min_prefix_len chars)
        3. Trigram fuzzy match (if query >= min_trigram_len chars)

        Args:
            name: Project name (case-insensitive)
            min_prefix_len: Minimum query length for prefix matching (default: 3)
            min_trigram_len: Minimum query length for trigram matching (default: 4)
            trigram_threshold: Minimum similarity score for trigram match (default: 0.3)

        Returns:
            Project details dict with match_type field, or None if not found
        """
        if not name or not name.strip():
            return None

        query = name.strip()
        query_len = len(query)
        pool = await self._get_pool()

        async with pool.acquire() as conn:
            # 1. Exact match
            row = await conn.fetchrow("SELECT * FROM get_project_by_name_exact($1)", query)
            if row:
                project = dict(row)
                if not self._should_exclude_project(project):
                    result = self._format_project(project)
                    result["match_type"] = "exact"
                    return result

            # 2. Prefix match (only if query >= min_prefix_len chars)
            if query_len >= min_prefix_len:
                row = await conn.fetchrow("SELECT * FROM get_project_by_name_prefix($1)", query)
                if row:
                    project = dict(row)
                    if not self._should_exclude_project(project):
                        result = self._format_project(project)
                        result["match_type"] = "prefix"
                        return result

            # 3. Trigram fuzzy match (only if query >= min_trigram_len chars)
            if query_len >= min_trigram_len:
                row = await conn.fetchrow(
                    "SELECT (project).*, similarity_score FROM get_project_by_name_trigram($1, $2)",
                    query,
                    trigram_threshold,
                )
                if row:
                    project = dict(row)
                    if not self._should_exclude_project(project):
                        result = self._format_project(project)
                        result["match_type"] = "trigram"
                        result["similarity_score"] = float(project.get("similarity_score", 0))
                        return result

        return None

    async def search_projects_by_name(
        self,
        name: str,
        limit: int = 3,
        min_prefix_len: int = 3,
        min_trigram_len: int = 4,
        trigram_threshold: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """
        Search projects by name, returning multiple matches.

        Strategy:
        1. Collect exact match (if any)
        2. Collect prefix matches
        3. If no matches and query is multi-word, strip suffix and retry exact → prefix
        4. Fallback to trigram if still no matches

        Args:
            name: Project name (case-insensitive)
            limit: Maximum number of results (default: 3)
            min_prefix_len: Minimum query length for prefix matching (default: 3)
            min_trigram_len: Minimum query length for trigram matching (default: 4)
            trigram_threshold: Minimum similarity score for trigram match (default: 0.3)

        Returns:
            List of project dicts with match_type field, ordered by relevance
        """
        if not name or not name.strip():
            return []

        query = name.strip()
        query_len = len(query)
        pool = await self._get_pool()
        results: List[Dict[str, Any]] = []
        seen_ids: set = set()

        async with pool.acquire() as conn:
            # Helper to add results without duplicates
            def add_result(project: Dict, match_type: str, similarity: float = None):
                proj_id = project.get("id")
                if proj_id in seen_ids:
                    return
                if self._should_exclude_project(project):
                    return
                seen_ids.add(proj_id)
                formatted = self._format_project(project)
                formatted["match_type"] = match_type
                if similarity is not None:
                    formatted["similarity_score"] = similarity
                results.append(formatted)

            # 1. Exact match
            row = await conn.fetchrow("SELECT * FROM get_project_by_name_exact($1)", query)
            if row:
                add_result(dict(row), "exact")

            # 2. Prefix matches (get multiple)
            if query_len >= min_prefix_len and len(results) < limit:
                rows = await conn.fetch(
                    "SELECT * FROM get_project_by_name_prefix($1, $2)",
                    query,
                    limit,
                )
                for row in rows:
                    if len(results) >= limit:
                        break
                    add_result(dict(row), "prefix")

            # 3. If no matches yet and query is multi-word, try stripping suffix
            if not results:
                stripped_query = self._strip_suffix_word(query)
                if stripped_query and len(stripped_query) >= min_prefix_len:
                    # Try exact match with stripped query
                    row = await conn.fetchrow(
                        "SELECT * FROM get_project_by_name_exact($1)",
                        stripped_query,
                    )
                    if row:
                        add_result(dict(row), "exact_stripped")

                    # Try prefix matches with stripped query
                    if len(results) < limit:
                        rows = await conn.fetch(
                            "SELECT * FROM get_project_by_name_prefix($1, $2)",
                            stripped_query,
                            limit,
                        )
                        for row in rows:
                            if len(results) >= limit:
                                break
                            add_result(dict(row), "prefix_stripped")

            # 4. Trigram fallback (only if still no results)
            if not results and query_len >= min_trigram_len:
                row = await conn.fetchrow(
                    "SELECT (project).*, similarity_score FROM get_project_by_name_trigram($1, $2)",
                    query,
                    trigram_threshold,
                )
                if row:
                    project = dict(row)
                    add_result(project, "trigram", float(project.get("similarity_score", 0)))

        return results[:limit]

    async def get_project(
        self,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        x_handle: Optional[str] = None,
        contract_address: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Unified method to get project details.
        Calls appropriate specific method based on provided parameters.

        Priority: contract_address > symbol > x_handle > name

        Args:
            name: Project name
            symbol: Token symbol
            x_handle: X (Twitter) handle
            contract_address: Contract address

        Returns:
            Project details dict or None if not found
        """
        # Priority order: contract_address > x_handle > symbol > name
        if contract_address and contract_address.strip():
            result = await self.get_project_by_contract(contract_address)
            if result:
                return result

        if x_handle and x_handle.strip():
            result = await self.get_project_by_twitter(x_handle)
            if result:
                return result

        if symbol and symbol.strip():
            result = await self.get_project_by_symbol(symbol)
            if result:
                return result

        if name and name.strip():
            result = await self.get_project_by_name(name)
            if result:
                return result

        return None

    async def search_by_investor(
        self,
        investor_name: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search projects by investor name.

        Args:
            investor_name: Name of the investor
            limit: Maximum number of results

        Returns:
            List of project dicts
        """
        pool = await self._get_pool()

        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM search_projects_by_investor($1, $2)",
                investor_name,
                limit,
            )

            projects = []
            for row in rows:
                project = dict(row)
                projects.append(self._format_project_summary(project))

            return projects

    async def search_by_keyword(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search projects by keyword using lexical search.
        Searches in project name, token symbol, and search_index terms.

        Args:
            query: Keyword search query (e.g., "oracle", "DeFi", "layer 2")
            limit: Maximum number of results

        Returns:
            List of project dicts sorted by relevance score
        """
        if not query or not query.strip():
            return []

        pool = await self._get_pool()

        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                WITH search_results AS (
                    SELECT * FROM lexical_search_projects($1, false)
                )
                SELECT 
                    sr.id, sr.rootdata_id, sr.name, sr.token_symbol, sr.score,
                    p.one_liner, p.rootdata_url, p.twitter_handle, p.coingecko_slug,
                    p.defillama_chain_name, p.defillama_slugs,
                    p.investors, p.fundraising, p.events
                FROM search_results sr
                JOIN projects p ON sr.id = p.id
                ORDER BY sr.score DESC
                LIMIT $2
                """,
                query,
                limit,
            )

            projects = []
            for row in rows:
                project = dict(row)
                if not self._should_exclude_project(project):
                    projects.append(self._format_project_summary(project))

            return projects

    def _should_exclude_project(self, project: Dict[str, Any]) -> bool:
        """
        Check if project should be excluded based on filtering criteria.

        Excludes projects that have:
        - events = empty AND VC = empty

        Args:
            project: Project dict

        Returns:
            True if project should be excluded
        """
        events = project.get("events")
        investors = project.get("investors")
        fundraising = project.get("fundraising")

        has_events = events and len(events) > 0
        has_investors = investors and len(investors) > 0
        has_fundraising = fundraising and len(fundraising) > 0
        has_vc = has_investors or has_fundraising

        if not has_events and not has_vc:
            return True

        return False

    def _parse_json_field(self, value: Any) -> List[Dict]:
        """Parse JSON field that may be a string or already a list."""
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            import json

            return json.loads(value)
        return []

    def _format_team(self, team: Any) -> List[str]:
        """Format team list to simplified strings like 'Role: Name'."""
        items = self._parse_json_field(team)
        return [f"{m.get('role', 'Member')}: {m.get('name', '')}" for m in items if m.get("name")]

    def _format_investors(self, investors: Any, max_count: int = 10) -> List[str]:
        """Format investors list to names with lead indicator. Max 10 shown."""
        items = self._parse_json_field(investors)
        result = []
        for inv in items:
            name = inv.get("name", "")
            if not name:
                continue
            if inv.get("is_lead"):
                result.append(f"{name} (Lead)")
            else:
                result.append(name)
        total = len(result)
        if total > max_count:
            result = result[:max_count]
            result.append(f"{total - max_count} more")
        return result

    def _format_fundraising(self, fundraising: Any) -> List[str]:
        """Format fundraising list to 'date: round_name amount_display' strings."""
        items = self._parse_json_field(fundraising)
        result = []
        for fr in items:
            date = fr.get("date", "")
            round_name = fr.get("round_name", "")
            amount = fr.get("amount_display", "")
            if date and round_name:
                result.append(f"{date}: {round_name} {amount}".strip())
        return result

    def _format_events(self, events: Any, max_count: int = 6) -> List[str]:
        """Format events list to 'date: detail' strings. Only recent 6 shown."""
        items = self._parse_json_field(events)
        # Sort by date descending to get most recent first
        items.sort(key=lambda x: x.get("date", ""), reverse=True)
        result = []
        for ev in items[:max_count]:
            date = ev.get("date", "")
            detail = ev.get("event_detail", "")
            if date and detail:
                result.append(f"{date}: {detail}")
        return result

    def _format_similar_projects(self, similar_projects: Any) -> List[str]:
        """Format similar projects to 'Name: Description'."""
        items = self._parse_json_field(similar_projects)
        return [f"{p.get('name', '')}: {p.get('description', '')}" for p in items if p.get("name")]

    def _format_project(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Format project dict for API response."""
        token_symbol = project.get("token_symbol")
        coingecko_slug = project.get("coingecko_slug")
        defillama_slugs = self._parse_json_field(project.get("defillama_slugs"))
        tags = self._parse_json_field(project.get("tags"))

        return {
            "name": project.get("name"),
            "token_symbol": token_symbol if token_symbol else None,
            "one_liner": project.get("one_liner"),
            "description": project.get("description"),
            "active": project.get("active"),
            "establishment_date": project.get("establishment_date"),
            "launch_date": project.get("launch_date"),
            "total_funding": project.get("total_funding"),
            "total_supply": project.get("total_supply"),
            "contract_address": project.get("contract_address"),
            "logo_url": project.get("logo_url"),
            "website": project.get("website"),
            "twitter_handle": project.get("twitter_handle"),
            "coingecko_id": coingecko_slug if coingecko_slug else None,
            "defillama_chain_name": project.get("defillama_chain_name"),
            "defillama_slugs": defillama_slugs if defillama_slugs else None,
            "tags": tags if tags else None,
            # waiting for data fix
            "team": self._format_team(project.get("team")),
            "investors": self._format_investors(project.get("investors")),
            "fundraising": self._format_fundraising(project.get("fundraising")),
            "events": self._format_events(project.get("events")),
            "exchanges": self._parse_json_field(project.get("exchanges")) or None,
            # "similar_projects": self._format_similar_projects(project.get("similar_projects")),
            "updated_at": str(project.get("updated_at"))[:10] if project.get("updated_at") else None,
        }

    def _format_project_summary(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Format project summary for search results."""
        token_symbol = project.get("token_symbol")
        coingecko_slug = project.get("coingecko_slug")
        defillama_slugs = self._parse_json_field(project.get("defillama_slugs"))

        return {
            "name": project.get("name"),
            "token_symbol": token_symbol if token_symbol else None,
            "one_liner": project.get("one_liner"),
            "twitter_handle": project.get("twitter_handle"),
            "coingecko_id": coingecko_slug if coingecko_slug else None,
            "defillama_chain_name": project.get("defillama_chain_name"),
            "defillama_slugs": defillama_slugs if defillama_slugs else None,
            "investors": self._format_investors(project.get("investors")),
        }
