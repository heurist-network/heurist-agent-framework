# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands
Only apply these to production code, not testing scripts.
- **Lint**: `ruff check --fix --line-length=120 --select=I <path>`
- **Format**: `ruff format --line-length=120 <path>`
- **Install dependencies with uv**: `uv add <package_name>`
- Always use uv to run Python

## Heurist Mesh Overview
- **mesh/**: Heurist Mesh specialized agent implementations
**Heurist Mesh** is an open network of modular and purpose-built AI agents. Technically, you can think of each agent as a collection of tools for AI. Once a Mesh agent is added to the main branch, it's automatically deployed and instantly available via REST API and MCP (Model Context Protocol).

## Mesh Agent Development Guidelines
- **Base class**: Inherit from `mesh.mesh_agent.MeshAgent`
- **Agent naming**: Use descriptive PascalCase names ending with "Agent" (e.g., `AlloraPricePredictionAgent`)
- **Metadata**: Include complete metadata in `__init__` (name, version, author, description, inputs, outputs, etc.)
- **API access**: Store sensitive API keys in environment variables, never hardcode
- **Testing**: Create a test file in `mesh/tests/` with example input/output saved as YAML
- **Tools**: Define tools using `get_tool_schemas()` method
- **External APIs**: Use `@with_retry` and `@with_cache` decorators for network operations
- **Resource management**: Implement `__aenter__` and `__aexit__` for proper cleanup
- **Documentation**: Include examples and clear descriptions in metadata

## Testing Mesh Agents and Modules
When developing or testing individual Mesh agent modules to see outputs ad-hoc, create test scripts in `mesh/test_scripts/` folder:

- **Always use `uv run`**: Run scripts with `uv run python mesh/test_scripts/<script_name>.py`
- **Test script location**: Place all test scripts in `mesh/test_scripts/` directory
- **Import path fix**: Add project root to Python path in test scripts:
  ```python
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent.parent
  sys.path.insert(0, str(project_root))
  ```
- **Test specific functionality**: Test individual agent tools, API responses, or data transformations
- **Example tests**: See `mesh/test_scripts/test_trending_token.py` for aggregated data testing, or `test_token_resolver.py` for individual agent testing

Coding Style
- Prefer the most straightforward way of implementation.
- No defensive programming. Use try/except sparingly. Let most fatal errors propogate.
- No adding extra variables if there's not a clear reason to do so. Prefer simplicity
- Use comments sparingly. Function and variable names should be self-explaining and you don't need to comment most of the times
- If duplicate code is written, consider refactoring.
- DO NOT use `getattr` or `isinstance` or defensive programming patterns
- Do not create summary doc after completing a task, unless explicitly asked
- When you are asked to review git staged code changes, give feedback as if you are a senior tech lead ensuring high standards and rank the issues found with high/medium/low. Do not edit code or run git commands that manipulate the repo.
