# Mesh Agent System Technical Documentation

## Overview

Heurist Mesh is an open network of modular and purpose-built AI agents. Each agent is a collection of tools for AI that can be accessed via REST API and MCP (Model Context Protocol). Once a Mesh agent is added to the main branch, it's automatically deployed and instantly available.

## Architecture

### Core Components

- **`mesh/mesh_agent.py`**: Base class that all mesh agents inherit from
- **`mesh/mesh_api.py`**: API layer that handles agent pool and task management
- **`mesh/agents/`**: Directory containing all agent implementations
- **`.github/scripts/update_mesh_metadata.py`**: Metadata extraction and publishing script

### Agent Lifecycle

1. **Development**: Agent is created by inheriting from `MeshAgent`
2. **Metadata Extraction**: AST-based parsing extracts metadata without importing
3. **Deployment**: Metadata published to S3 (`mesh.heurist.ai/metadata.json`)
4. **Discovery**: Agents are discoverable via metadata.json
5. **Execution**: Agents invoked via REST API or MCP

## Agent Metadata Structure

### Type Definitions

All metadata is strongly typed using Python `TypedDict`:

```python
class AgentMetadataRequired(TypedDict):
    name: str                      # Agent display name
    version: str                   # Semantic versioning (e.g., "1.0.0")
    author: str                    # Author name
    author_address: str            # Ethereum address (0x-prefixed, 42 chars)
    description: str               # Agent description
    tags: List[str]               # Classification tags
    inputs: List[InputField]       # Input parameter schemas
    outputs: List[OutputField]     # Output schemas
    image_url: str                 # Agent icon URL

class AgentMetadata(AgentMetadataRequired, total=False):
    external_apis: List[str]       # External API names (optional)
    examples: List[str]            # Usage example prompts (optional)
    verified: bool                 # Verified/trusted flag (default: False)
    recommended: bool              # Recommended agent flag (default: False)
    hidden: bool                   # Hide from UI (default: False)
    credits: float                 # Cost in credits (optional)
    x402_config: X402Config        # Payment configuration (optional)
```

### Required Fields (9 fields)

Every agent **must** define these fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Agent display name (e.g., "CoinGecko Agent") |
| `version` | `str` | Semantic version (e.g., "1.0.0") |
| `author` | `str` | Author name (usually "Heurist team") |
| `author_address` | `str` | Ethereum address (42 chars, 0x-prefixed) |
| `description` | `str` | Brief description of agent capabilities |
| `tags` | `List[str]` | Classification tags (e.g., ["Trading", "DeFi"]) |
| `inputs` | `List[InputField]` | Input parameter definitions |
| `outputs` | `List[OutputField]` | Output field definitions |
| `image_url` | `str` | URL to agent icon (GitHub raw content URL) |

### Optional Fields

| Field | Type | Usage | Default |
|-------|------|-------|---------|
| `external_apis` | `List[str]` | External API dependencies | `[]` |
| `examples` | `List[str]` | Usage example prompts | `[]` |
| `verified` | `bool` | Agent is verified/trusted | `False` |
| `recommended` | `bool` | Featured/recommended agent | `False` |
| `hidden` | `bool` | Hide from UI listings | `False` |
| `credits` | `float` | Cost in credits | - |
| `x402_config` | `X402Config` | Payment integration config | - |

### Input/Output Field Structure

```python
class InputField(TypedDict, total=False):
    name: str          # Parameter name
    description: str   # Parameter description
    type: str         # Type: "str", "int", "bool", "dict", etc.
    required: bool    # Whether parameter is required
    default: Any      # Default value (for optional parameters)

class OutputField(TypedDict):
    name: str          # Output field name
    description: str   # Field description
    type: str         # Field type
```

### Payment Configuration (x402)

```python
class X402Config(TypedDict, total=False):
    enabled: bool                      # Enable x402 payments
    default_price_usd: str            # Default price per call (USD string)
    tool_prices: Dict[str, str]       # Per-tool pricing override
```

**Example:**
```python
"x402_config": {
    "enabled": True,
    "default_price_usd": "0.01",
    "tool_prices": {
        "advanced_search": "0.05",
        "basic_query": "0.01"
    }
}
```

## Tool Schema Structure

Tools use OpenAI-compatible function calling format:

```python
class ToolParameterPropertyRequired(TypedDict):
    type: str          # Parameter type (required)
    description: str   # Parameter description (required)

class ToolParameterProperty(ToolParameterPropertyRequired, total=False):
    enum: List[str]    # Allowed values (optional)
    default: Any       # Default value (optional)

class ToolSchema(TypedDict):
    type: str          # Always "function"
    function: {
        "name": str,
        "description": str,
        "parameters": {
            "type": "object",
            "properties": Dict[str, ToolParameterProperty],
            "required": List[str]
        }
    }
```

## Creating a New Agent

### 1. Basic Structure

```python
from mesh.mesh_agent import MeshAgent
from typing import Any, Dict, List

class YourAgent(MeshAgent):
    def __init__(self):
        super().__init__()

        # Update metadata
        self.metadata.update({
            "name": "Your Agent",
            "version": "1.0.0",
            "author": "Your Name",
            "author_address": "0x...",
            "description": "Brief description",
            "tags": ["Category"],
            "image_url": "https://raw.githubusercontent.com/.../YourAgent.png",
            "examples": [
                "Example query 1",
                "Example query 2"
            ]
        })

    def get_system_prompt(self) -> str:
        return "Your agent's system prompt"

    def get_tool_schemas(self) -> List[Dict]:
        return [{
            "type": "function",
            "function": {
                "name": "your_tool",
                "description": "Tool description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param": {
                            "type": "string",
                            "description": "Parameter description"
                        }
                    },
                    "required": ["param"]
                }
            }
        }]

    async def _handle_tool_logic(
        self,
        tool_name: str,
        function_args: dict,
        session_context: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        if tool_name == "your_tool":
            # Implement tool logic
            return {"result": "data"}

        return {"error": f"Unknown tool: {tool_name}"}
```

### 2. Agent Naming Convention

- Use `PascalCase` with "Agent" suffix (e.g., `CoinGeckoTokenInfoAgent`)
- File name: `snake_case` with `_agent.py` suffix (e.g., `coingecko_token_info_agent.py`)

### 3. Metadata Best Practices

**Standard Ethereum Address:**
Most agents use: `0x7d9d1821d15B9e0b8Ab98A058361233E255E405D`

**Image URL Pattern:**
```
https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/{AgentName}.png
```

**Tags:**
Common tags: `Trading`, `DeFi`, `Research`, `Twitter`, `Search`, `x402`, `Solana`, `EVM`, `Intelligence`, `Security`

**Examples:**
Provide 3-7 realistic usage examples showing different capabilities.

### 4. Tool Implementation

Tools are called via two modes:

**1. Direct Tool Call (no LLM):**
```python
params = {
    "tool": "tool_name",
    "tool_arguments": {"arg": "value"},
    "raw_data_only": True
}
```

**2. Natural Language Query (LLM decides tool):**
```python
params = {
    "query": "What's the price of ETH?",
    "raw_data_only": False  # LLM generates explanation
}
```

### 5. Error Handling

Return structured errors:
```python
{
    "status": "error",
    "error": "Error message"
}
```

### 6. Caching and Retry

Use decorators for external API calls:
```python
from decorators import with_cache, with_retry

@with_cache(ttl_seconds=300)
@with_retry(max_attempts=3)
async def fetch_data(self, url: str):
    # API call logic
```

## Metadata Generation

### Manual Update

```bash
# Dev mode (writes to local file)
uv run python .github/scripts/update_mesh_metadata.py --dev

# Production mode (uploads to S3)
uv run python .github/scripts/update_mesh_metadata.py
```

### How It Works

1. **AST Parsing**: Extracts metadata from source files without importing
2. **Base Metadata Merge**: Merges agent-specific metadata with base defaults
3. **Tool Schema Extraction**: Extracts tool definitions from `get_tool_schemas()`
4. **Dynamic Input Injection**: Adds `tool` and `tool_arguments` inputs
5. **Preservation**: Preserves runtime fields (`total_calls`, `greeting_message`)
6. **Output**: Generates `metadata.json` with structure:

```json
{
  "last_updated": "2026-01-14T12:34:56.789123+00:00",
  "commit_sha": "abc123...",
  "agents": {
    "AgentName": {
      "metadata": { /* AgentMetadata */ },
      "module": "module_name",
      "tools": [ /* ToolSchema[] */ ]
    }
  }
}
```

## Testing Agents

### Test Script Location

Create test scripts in `mesh/test_scripts/`:

```python
# mesh/test_scripts/test_your_agent.py
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mesh.agents.your_agent import YourAgent

async def test():
    agent = YourAgent()

    # Test direct tool call
    result = await agent.handle_message({
        "tool": "your_tool",
        "tool_arguments": {"param": "value"},
        "raw_data_only": True
    })

    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
```

### Running Tests

```bash
uv run python mesh/test_scripts/test_your_agent.py
```

## Payment Integration (x402)

### Enabling Payments

1. Add `x402_config` to metadata
2. Add "x402" tag
3. Set pricing:

```python
"x402_config": {
    "enabled": True,
    "default_price_usd": "0.01",  # $0.01 per call
}
```

### Per-Tool Pricing

```python
"x402_config": {
    "enabled": True,
    "default_price_usd": "0.01",
    "tool_prices": {
        "expensive_tool": "0.10",
        "cheap_tool": "0.01"
    }
}
```

## ERC-8004 On-Chain Registration

### Overview

ERC-8004 is an on-chain identity protocol for AI agents on Ethereum. Agents can be registered on Sepolia (testnet) or Mainnet.

### Configuration

Add `erc8004_config` to enable registration:

```python
"erc8004_config": {
    "enabled": True,
    "supported_trust": ["reputation"]  # Trust models
}
```

**Supported trust models:**
- `"reputation"` - Reputation-based trust
- `"crypto-economic"` - Economic stake-based trust
- `"tee-attestation"` - TEE attestation-based trust

### Registration Flow

**1. Register agent on-chain:**
```bash
# List eligible agents
uv run python -m mesh.erc8004.cli list --chain sepolia

# Register single agent
uv run python -m mesh.erc8004.cli register "Token Resolver Agent" --chain sepolia

# Sync all eligible agents
uv run python -m mesh.erc8004.cli sync --chain sepolia
```

**2. Auto-update registry:**
When registered, agent ID is automatically saved to `mesh/erc8004/registered_agents.json`:
```json
{
  "sepolia": {
    "Token Resolver Agent": "11155111:42"
  },
  "mainnet": {}
}
```

**3. Metadata publish flow:**
When `update_mesh_metadata.py` runs, it merges agent IDs from the registry:
```json
{
  "erc8004_config": {
    "enabled": true,
    "supported_trust": ["reputation"],
    "agent_ids": {
      "sepolia": "11155111:42",
      "mainnet": "1:123"
    }
  }
}
```

### Agent ID Format

Agent IDs follow the format: `"chainId:tokenId"` (e.g., `"11155111:42"` for Sepolia)

### Key Points

- Agent IDs are stored in `mesh/erc8004/registered_agents.json`, not in agent source code
- Registry file is auto-updated on successful registration
- Metadata publish script merges agent IDs into `metadata.json`
- Supports both Sepolia (11155111) and Mainnet (1)

## Advanced Features

### Timeout Configuration

```python
def get_default_timeout_seconds(self) -> Optional[int]:
    return 30  # 30 second timeout

def get_tool_timeout_seconds(self) -> Dict[str, int]:
    return {
        "slow_tool": 60,
        "fast_tool": 10
    }
```

### Fallback Agents

```python
async def get_fallback_for_tool(
    self,
    tool_name: Optional[str],
    function_args: Dict[str, Any],
    original_params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    if tool_name == "search":
        return {
            "module": "mesh.agents.exa_search_agent",
            "class": "ExaSearchAgent",
            "input": {
                "tool": "search",
                "tool_arguments": function_args
            }
        }
    return None
```

### Calling Other Agents

```python
# Call another agent's tool
result = await self._call_agent_tool(
    module="mesh.agents.coingecko_token_info_agent",
    class_name="CoinGeckoTokenInfoAgent",
    tool_name="get_token_info",
    tool_args={"symbol": "ETH"}
)
```


## Best Practices

### DO ✅

- Inherit from `MeshAgent`
- Use `@with_retry` for external API calls
- Use `@with_cache` for expensive operations
- Return structured data in `_handle_tool_logic`
- Provide 3-7 realistic examples
- Use clear, descriptive tool names
- Test with `mesh/test_scripts/`

### DON'T ❌

- Don't hardcode API keys (use environment variables)
- Don't create agents without metadata
- Don't use generic error messages
- Don't create duplicate functionality
- Don't modify `MeshAgent` base class without discussion
