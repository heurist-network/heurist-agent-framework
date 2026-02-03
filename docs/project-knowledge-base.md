# Project Knowledge Agent Documentation

## Overview

The **Project Knowledge Agent** is a specialized Mesh Agent designed to provide comprehensive access to a cryptocurrency project information database. It enables queries about projects through multiple search strategies and returns detailed project information including funding, team details, events, and social metrics.

### Agent Metadata
| Field | Value |
|-------|-------|
| Name | Project Knowledge Agent |
| Version | 1.0.0 |
| Author | Heurist team |
| Author Address | 0x7d9d1821d15B9e0b8Ab98A058361233E255E405D |
| External APIs | PostgreSQL |
| Tags | Projects, Research |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ProjectKnowledgeAgent                         │
│                  (mesh/agents/project_knowledge_agent.py)        │
├─────────────────────────────────────────────────────────────────┤
│  Handles: Query Routing, Result Formatting                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ ProjectKnowledgeClient     │
        │  (clients/)                │
        ├────────────────────────────┤
        │ • get_project()            │
        │ • get_project_by_*()       │
        │ • search_by_investor()      │
        │ • search_by_keyword()       │
        │ • Advanced matching         │
        │ • Suffix stripping          │
        └──────────┬──────────────────┘
                   │
        ┌──────────▼──────────┐
        │  asyncpg Pool        │
        │  (PostgreSQL)        │
        └──────────┬──────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
    ┌──────────┐       ┌──────────┐
    │ Projects │       │ search   │
    │  Table   │       │  _index  │
    │          │       │  Table   │
    └──────────┘       └──────────┘
```

---

## Key Files

| File | Purpose |
|------|---------|
| `mesh/agents/project_knowledge_agent.py` | Main agent implementation with tool routing |
| `clients/project_knowledge_client.py` | Client with advanced cascading match strategy |
| `mesh/mesh_agent.py` | Base class for all mesh agents |

---

## Database Schema

### Projects Table

The agent queries a PostgreSQL database containing crypto project information.

**Core Identity Fields:**
- `id` (UUID) - Internal database ID
- `rootdata_id` (INTEGER) - RootData unique identifier
- `name` (VARCHAR) - Project name
- `name_lower` (VARCHAR) - Lowercase name (generated, for search)
- `token_symbol` (VARCHAR) - Token ticker symbol (e.g., "ETH", "BTC")
- `symbol_lower` (VARCHAR) - Lowercase symbol (generated, for search)

**Description & Classification:**
- `one_liner` (TEXT) - One-line project description
- `description` (TEXT) - Full project description
- `tags` (JSONB) - Project category tags array
- `active` (BOOLEAN) - Project status

**Timeline:**
- `establishment_date` (VARCHAR) - Project founding date
- `launch_date` (VARCHAR) - Token/product launch date

**Financial Data:**
- `total_funding` (BIGINT) - Total fundraising amount
- `total_supply` (BIGINT) - Token total supply

**Blockchain & Contract:**
- `contract_address` (VARCHAR) - Token contract address (normalized: 0x addresses stored lowercase)

**Team & Governance:**
- `team` (JSONB) - Team members array
- `investors` (JSONB) - Investor list array
- `fundraising` (JSONB) - Fundraising rounds detail array
- `events` (JSONB) - Project events/milestones array

**External Links:**
- `website` (TEXT) - Official website URL
- `twitter_handle` (TEXT) - Normalized Twitter handle (without @, x.com, twitter.com)
- `rootdata_url` (TEXT) - RootData project profile URL
- `coingecko_slug` (VARCHAR) - CoinGecko identifier for API integration
- `logo_url` (TEXT) - Project logo image URL

**DeFiLlama Integration:**
- `defillama_chain_name` (VARCHAR) - DeFiLlama chain name (for exact matches)
- `defillama_slugs` (JSONB) - List of DeFiLlama protocol slugs

**Metadata:**
- `similar_projects` (JSONB) - Related projects array
- `exchanges` (JSONB) - List of trading venues
- `data_source` (VARCHAR) - Data origin attribution
- `created_at` (TIMESTAMPTZ) - Record creation timestamp
- `updated_at` (TIMESTAMPTZ) - Last update timestamp

### Search Index Table

Aliases and alternative names for fuzzy matching:
- `project_id` (UUID) - Foreign key to projects table
- `term` (VARCHAR) - Search term/alias
- `term_lower` (VARCHAR) - Lowercase term (generated)
- `term_type` (VARCHAR) - Type of term (e.g., "alias", "tag")

### Project Investors Table

Normalized investor relationships:
- `project_id` (UUID) - Foreign key to projects table
- `investor_name` (VARCHAR) - Investor name
- `investor_name_lower` (VARCHAR) - Lowercase name (generated)
- `investor_id` (INTEGER) - Investor ID if available
- `lead_investor` (BOOLEAN) - Whether lead investor
- `round_name` (VARCHAR) - Funding round name

---

## Tool Schema

### `get_project` Tool

The agent exposes one unified tool with multiple query modes:

```json
{
  "type": "function",
  "function": {
    "name": "get_project",
    "description": "Get project information. Can search by name, symbol, x_handle, investor, or keyword query",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Project name for exact match lookup"
        },
        "symbol": {
          "type": "string",
          "description": "Token symbol for exact match lookup"
        },
        "x_handle": {
          "type": "string",
          "description": "Twitter/X handle (with or without @)"
        },
        "contract_address": {
          "type": "string",
          "description": "Contract address for exact match lookup (normalized: 0x addresses are case-insensitive)"
        },
        "investor": {
          "type": "string",
          "description": "Investor name to find their portfolio"
        },
        "query": {
          "type": "string",
          "description": "Keyword for fuzzy/full-text search"
        },
        "limit": {
          "type": "integer",
          "description": "Max results (default: 10, max: 50)"
        }
      }
    }
  }
}
```

---

## Search and Ranking Algorithms

### Search Priority Order

The `lexical_search_projects` SQL function implements this ranking:

| Priority | Match Type | Score |
|----------|------------|-------|
| 1 | Contract address exact match | 1.0 |
| 1.5 | Exact name match | 1.0 |
| 2 | Name match after suffix removal | 1.0 |
| 3 | Symbol exact match | 0.95 |
| 4 | Name prefix match | 0.85 |
| 5 | Symbol prefix match | 0.80 |
| 6 | Name trigram fuzzy match | 0.7 × similarity |
| 7 | Symbol trigram fuzzy match | 0.65 × similarity |
| 8 | Search index exact match | 0.75 |
| 9 | Search index trigram match | 0.6 × similarity |
| 10 | Contract address prefix match | 0.5 |

**Note:** Results are deduplicated by project ID, keeping the highest-scoring match for each project. Final ranking is by score (descending), then by project ID.

### Suffix Stripping

The `strip_crypto_suffix()` function removes common crypto project suffixes to improve matching:

```
finance, labs, protocol, network, dao, token, coin,
ai, chain, swap, dex, defi, exchange, capital, ventures
```

**Example:** Query "Uniswap Labs" → stripped to "uniswap" → matches "Uniswap"

### Client Cascading Match Strategy

For name-based queries, the client implements cascading matching:

1. **Exact Match** - Case-insensitive exact string match
2. **Prefix Match** - Names starting with query (min 3 chars)
3. **Suffix Stripping & Retry** - Strips common suffixes, retries exact → prefix matching
4. **Trigram Fuzzy Match** - Similarity-based (min 4 chars, 30% threshold)

**Return Fields:**
- Single match (`get_project_by_name`): Returns project dict with `match_type` field ("exact", "prefix", or "trigram")
- Trigram matches also include `similarity_score` field (0.0-1.0)
- Multiple matches (`search_projects_by_name`): Returns list of projects, each with `match_type` and optional `similarity_score`

**Query Priority (for `get_project` method):**
When multiple parameters are provided, priority order is: `contract_address` > `symbol` > `x_handle` > `name`

### Twitter Handle Normalization

The agent normalizes various Twitter input formats:
- `@handle` → `handle`
- `https://x.com/handle` → `handle`
- `https://twitter.com/handle` → `handle`
- `x.com/handle` → `handle`

---

## Filtering Rules

### Content Quality Filter
Projects are excluded if:
- `events` array is empty AND
- (`investors` array is empty OR `fundraising` array is empty)

In other words, a project must have either events OR investor/fundraising data to be included. This ensures only well-documented projects are returned.

---

## External Dependencies

### PostgreSQL Database
- **Driver:** asyncpg (async PostgreSQL)
- **Pool:** min_size=1, max_size=10 connections

---

## Configuration

### Environment Variables

```bash
# Database (required)
POSTGRESQL_URL=postgresql://user:password@host:port/database
```

### Default Values

| Setting | Value |
|---------|-------|
| Query limit default | 10 |
| Query limit max | 50 |
| Name prefix min length | 3 characters |
| Name trigram min length | 4 characters |
| Trigram similarity threshold | 0.3 (30%) |

---

## Performance Features

### Connection Pooling
- Lazy initialization on first use
- Async locks for thread safety
- Graceful shutdown with explicit `close()`

---

## Usage Examples

### 1. Exact Name Lookup
```
User: "Get information about Ethereum"
Agent: get_project(name="Ethereum")
→ SQL: get_project_details('Ethereum')
→ Returns: Full project details
```

### 2. Symbol Search
```
User: "What is ETH?"
Agent: get_project(symbol="ETH")
→ SQL: get_project_details('ETH')
→ Returns: Ethereum project details
```

### 3. Twitter Handle Search
```
User: "Find project @uniswap"
Agent: get_project(x_handle="@uniswap")
→ Normalized: "uniswap"
→ SQL: get_project_by_twitter('uniswap')
→ Returns: Uniswap project details
```

### 4. Investor Portfolio Search
```
User: "What did Paradigm invest in?"
Agent: get_project(investor="Paradigm", limit=10)
→ SQL: search_projects_by_investor('Paradigm', 10)
→ Returns: List of Paradigm portfolio projects
```

### 5. Keyword/Fuzzy Search
```
User: "Find oracle projects"
Agent: get_project(query="oracle", limit=10)
→ SQL: lexical_search_projects('oracle', false)
→ Returns: List of project summaries (not full details) with relevance scores
→ Fields included: id, name, token_symbol, one_liner, rootdata_url, twitter_handle, 
  coingecko_slug, defillama_chain_name, defillama_slugs, score, investors, 
  fundraising, events
→ Results sorted by score (descending), where score ranges from 0.0 to 1.0
```

### 6. Suffix-Stripped Match
```
User: "Tell me about Uniswap Labs"
Agent: get_project(name="Uniswap Labs")
→ No exact match found
→ Strips "Labs" suffix
→ Retries exact match with "Uniswap"
→ Matches "Uniswap"
→ Returns: Uniswap project details with match_type="exact"
```

### 7. Contract Address Search
```
User: "Find project with address 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
Agent: get_project(contract_address="0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
→ Normalized to lowercase for 0x addresses
→ SQL: get_project_by_contract('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984')
→ Returns: Full project details (Uniswap in this case)
```

---

## System Prompt

The agent receives the following system prompt to guide its behavior:

```
You are a helpful assistant that provides information about crypto projects
from a comprehensive database.

You can search for projects by:
- Project name (e.g., "Ethereum", "Uniswap") - exact match with cascading fallback
- Token symbol (e.g., "ETH", "UNI") - exact match
- X (Twitter) handle (e.g., "@ethereum", "ethereum") - exact match
- Contract address (e.g., "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984") - exact match
- Investor name (e.g., "Paradigm", "a16z") - returns list of projects invested by that investor
- Keyword query (e.g., "oracle", "DeFi", "layer 2", "top oracle projects") - fuzzy search across names, descriptions, and tags, returns summaries with relevance scores

When providing project information, be clear and concise. Include key details:
- Project name and token symbol
- One-liner description
- Key investors and funding rounds
- Recent events
- Links to official websites and social media

Format your response in clean text. Be objective and informative.
```

---

## SQL Functions Reference

### `lexical_search_projects(query TEXT, return_details BOOLEAN)`
Multi-tier ranked search across projects table and search_index. Returns results with relevance scores (0.0-1.0). When `return_details=false`, returns summary fields; when `true`, returns all project fields.

### `get_project_details(query TEXT)`
Single project lookup by name, symbol, or Twitter handle.

### `search_projects_by_investor(investor_name TEXT, limit_count INTEGER)`
Find projects by investor name with content quality filtering.

### `strip_crypto_suffix(input_text TEXT)`
Remove common crypto suffixes for improved matching.

### `get_project_by_symbol(p_symbol TEXT)`
Exact symbol match lookup.

### `get_project_by_twitter(p_handle TEXT)`
Exact Twitter handle match lookup.

### `get_project_by_contract(p_address TEXT)`
Contract address lookup with normalization.

### `get_project_by_name_exact(p_name TEXT)`
Exact name match lookup.

### `get_project_by_name_prefix(p_name TEXT, p_limit INT)`
Name prefix match with configurable limit.

### `get_project_by_name_trigram(p_name TEXT, p_threshold REAL)`
Trigram fuzzy match with similarity threshold.

---

## Key Features Summary

- **Multiple Search Methods:** Name, symbol, X-handle, contract address, investor, keyword
- **Advanced Matching:** Exact, prefix, suffix-stripping, trigram fuzzy with relevance scoring
- **Rich Project Data:** 30+ fields including team, investors, events, funding, DeFiLlama integration
- **Result Formatting:** Full details for single lookups, summaries with scores for search results
- **Performance:** Connection pooling, async/await
- **Data Quality:** Filters low-quality projects (must have events OR investor/fundraising data)
- **Production Ready:** Type hints, async/await, proper resource cleanup
- **DeFiLlama Integration:** Chain names and protocol slugs for enhanced project matching