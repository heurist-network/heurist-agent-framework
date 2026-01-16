import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional

import asyncpg
from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)
load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


class ProjectKnowledgeClient:
    """PostgreSQL client for project knowledge database."""

    def __init__(self):
        self.database_url = os.getenv("POSTGRESQL_URL")
        if not self.database_url:
            raise ValueError("POSTGRESQL_URL environment variable is required")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self._openai_client = OpenAI(api_key=self.openai_api_key)
        self._pool: Optional[asyncpg.Pool] = None
        self._pool_lock = asyncio.Lock()

    async def connect(self):
        """Create connection pool."""
        if self._pool is not None:
            return
        async with self._pool_lock:
            if self._pool is not None:
                return
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=30,
            )
            logger.info("Connected to project knowledge database")

    async def close(self):
        """Close connection pool."""
        if not self._pool:
            return
        async with self._pool_lock:
            if not self._pool:
                return
            pool = self._pool
            self._pool = None
        await pool.close()
        logger.info("Closed project knowledge database connection")

    async def lexical_search(
        self, query: str, return_details: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Lexical search for projects by name, token symbol, or contract address.
        Returns best match + 3 fuzzy matches if return_details=False, or full details if return_details=True.
        """
        if not self._pool:
            await self.connect()

        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM lexical_search_projects($1, $2)", query, return_details
            )

        results = []
        for row in rows:
            result = dict(row)
            for key, value in result.items():
                if isinstance(value, (dict, list)):
                    result[key] = json.loads(json.dumps(value, default=str))
            results.append(result)

        return results

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a user query."""
        try:
            response = self._openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=query,
                dimensions=EMBEDDING_DIMENSIONS,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

    async def semantic_search(
        self, query: str, limit: int = 10, similarity_threshold: Optional[float] = None, query_specificity: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Semantic search using vector embeddings with two-tier ranking.
        
        Args:
            query: Natural language query
            limit: Maximum number of results
            similarity_threshold: Optional fixed threshold (if None, uses adaptive threshold based on query_specificity)
            query_specificity: 0.0-1.0, higher = more specific query (default 0.7)
                              - 0.9-1.0: Very specific (name/symbol) -> threshold ~0.80
                              - 0.7-0.9: Specific (category) -> threshold ~0.70-0.75
                              - 0.5-0.7: Exploratory -> threshold ~0.65-0.70
        """
        if not query:
            raise ValueError("query parameter is required")

        query_embedding = self.generate_query_embedding(query)
        if not self._pool:
            await self.connect()

        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM semantic_search_projects($1::vector, $2, $3, $4)",
                query_embedding,
                limit,
                similarity_threshold,
                query_specificity,
            )

        results = []
        for row in rows:
            result = dict(row)
            results.append(result)

        return results

    async def get_project_details(self, canonical_name: str) -> Optional[Dict[str, Any]]:
        """
        Get full project details by canonical name (exact match).
        """
        if not self._pool:
            await self.connect()

        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM get_project_details($1)", canonical_name
            )

        if not row:
            return None

        result = dict(row)
        for key, value in result.items():
            if isinstance(value, (dict, list)):
                result[key] = json.loads(json.dumps(value, default=str))

        return result


