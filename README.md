<div align="center">
    <img src="./docs/img/agent-framework-poster.jpg" alt="Heurist Agent Framework Banner" width="100%" />
</div>

# Heurist Agent Framework

A flexible multi-interface AI agent framework that can interact through various platforms including Telegram, Discord, Twitter, Farcaster, REST API, and MCP.

Grab a Heurist API Key instantly for free by using the code 'agent' while submitting the form on https://heurist.ai/dev-access

---

## Overview

The Heurist Agent Framework is built on a modular architecture that allows an AI agent to:
- Process text and voice messages
- Generate images and videos
- Interact across multiple platforms with consistent behavior
- Fetch and store information in a knowledge base (Postgres and SQLite supported)
- Access external APIs, tools, and a wide range of [Mesh Agents](./mesh/README.md) to compose complex workflows

## Table of Contents

- [Features](#features)
- [Heurist Mesh](#heurist-mesh)
  - [MCP Support](#mcp-support)
  - [Recommended Mesh Agents](#recommended-mesh-agents)
  - [Full List of Mesh Agents](#full-list-of-mesh-agents)
  - [Usage and Development Guide](#usage-and-development-guide)
- [Heurist Agent Framework Architecture](#heurist-agent-framework-architecture)
  - [Agent Structure](#agent-structure)
  - [Agent Interfaces](#agent-interfaces)
  - [Heurist Core](#heurist-core)
    - [Components](#components)
    - [Workflows](#workflows)
    - [Tool Management](#tool-management)
    - [External Clients](#external-clients)
  - [Agent Usage and Development Guide](#agent-usage-and-development-guide)
- [How to Use GitHub Issues](#how-to-use-github-issues)
- [License](#license)
- [Contributing](#contributing)
- [Support](#support)
- [Star History](#star-history)

## Features

- 🤖 **Core Agent** - Modular framework with advanced LLM integration
- 🧩 **Component Architecture** - Plug-and-play components for flexible agent or agentic application design
- 🔄 **Workflow System** - RAG, Chain of Thought, and Research workflows
- 🖼️ **Media Generation** - Image creation and processing capabilities
- 🎤 **Voice Processing** - Audio transcription and text-to-speech
- 💾 **Vector Storage** - Knowledge retrieval with PostgreSQL/SQLite support
- 🛠️ **Tool Integration** - Extensible tool framework with MCP support
- 🌐 **Mesh Agent Access** - Connect to community-contributed specialized agents via API or MCP
- 🔌 **Multi-platform Support**:
  - Telegram bot
  - Discord bot
  - Twitter automation
  - Farcaster integration
  - REST API
  - MCP integration

## Heurist Mesh
![mesh](https://github.com/user-attachments/assets/77a2ab3b-e35c-4313-8a5b-a0e751cac879)

**Heurist Mesh** is an open network where AI agents are contributed by the community and used modularly—similar to DeFi smart contracts. Each agent is a specialized unit that can process data, generate reports, or perform actions while collectively forming an intelligent swarm to tackle complex tasks. Each agent is accessible via a unified REST API interface, and can be used in conjunction with any agent framework or application.

Want to contribute your own agent? Check out the [Mesh README](./mesh/README.md) for detailed guidelines, examples, and best practices.

### MCP Support
**Just In:** All Heurist Mesh agents are accessible via MCP! This means you can access them from your favorite MCP client, including [Claude Desktop](https://claude.ai/download), [Cursor](https://www.cursor.com/), and [Windsurf](https://codeium.com/windsurf).

Head to [heurist-mesh-mcp-server](https://github.com/heurist-network/heurist-mesh-mcp-server) to set up a server and give your AI assistant a powerup.

### Recommended Mesh Agents

• [BitquerySolanaTokenInfoAgent](./mesh/agents/bitquery_solana_token_info_agent.py) - Provides comprehensive analysis of Solana tokens including metrics, holders, trading activity, and trending token discovery

• [CoinGeckoTokenInfoAgent](./mesh/agents/coingecko_token_info_agent.py) - Fetches token information, market data, trending coins, and category data from CoinGecko

• [DexScreenerTokenInfoAgent](./mesh/agents/dexscreener_token_info_agent.py) - Fetches real-time DEX trading data and token information across multiple chains

• [ElfaTwitterIntelligenceAgent](./mesh/agents/elfa_twitter_intelligence_agent.py) - Analyzes tokens, topics or Twitter accounts using Twitter data, highlighting smart influencers

• [ExaSearchAgent](./mesh/agents/exa_search_agent.py) - Searches the web and provides direct answers to questions

• [GoplusAnalysisAgent](./mesh/agents/goplus_analysis_agent.py) - Fetches and analyzes security details of blockchain token contracts

• [MetaSleuthSolTokenWalletClusterAgent](./mesh/agents/metasleuth_sol_token_wallet_cluster_agent.py) - Analyzes wallet clusters holding Solana tokens to identify holder behavior, concentration, and potential market manipulation

• [PumpFunTokenAgent](./mesh/agents/pumpfun_token_agent.py) - Analyzes Pump.fun tokens on Solana, tracking token creation and graduation events

• [SolWalletAgent](./mesh/agents/sol_wallet_agent.py) - Queries Solana wallet assets and recent swap transactions

### Full List of Mesh Agents

[View the full list](./mesh/README.md#appendix-all-available-mesh-agents)

### Usage and Development Guide

[Read the Mesh documentation](./mesh/README.md)


## Heurist Agent Framework Architecture

The framework follows a modular, component-based architecture:

<div align="center">
<img src="./docs/img/agent_hl.png" alt="Heurist Agent Framework" width="75%">
</div>

### Agent Structure

1. **BaseAgent** (Abstract Base Class)
   - Defines the interface and common functionality
   - Manages component initialization and lifecycle
   - Implements core messaging patterns

2. **CoreAgent** (Concrete Implementation)
   - Implements BaseAgent functionality
   - Orchestrates components and workflows
   - Handles decision-making for workflow selection

### Agent Interfaces

Each interface inherits from BaseAgent and implements platform-specific handling:

- **Telegram** (`interfaces/telegram_agent.py`)
- **Discord** (`interfaces/discord_agent.py`)
- **API** (`interfaces/flask_agent.py`)
- **Twitter** (`interfaces/twitter_agent.py`)
- **Farcaster** (`interfaces/farcaster_agent.py`)

### Heurist Core

Heurist Core provides a set of core components, tools, and workflows for building LLM-powered agents or agentic applications. It can be used as a standalone package or as part of the Heurist Agent Framework.

[Read the Heurist Core documentation](./core/README.md)

#### Components

The framework uses a modular component system:

- **PersonalityProvider**: Manages agent personality and system prompts
- **KnowledgeProvider**: Handles knowledge retrieval from vector database
- **ConversationManager**: Manages conversation history and context
- **ValidationManager**: Validates inputs and outputs
- **MediaHandler**: Processes images, audio, and other media
- **LLMProvider**: Interfaces with language models
- **MessageStore**: Stores and retrieves messages with vector search

#### Workflows

Workflows provide higher-level reasoning patterns:

- **AugmentedLLMCall**: Standard RAG + tools pattern for context-aware responses
- **ChainOfThoughtReasoning**: Multi-step reasoning with planning and execution phases
- **ResearchWorkflow**: Deep web search and analysis with hierarchical exploration

#### Tool Management

- **ToolBox**: Base framework for tool definition and registration
- **Tools**: Tool management and execution layer
- **ToolsMCP**: Integration with MCP Protocol for tool execution

#### External Clients

- **SearchClient**: Unified client for web search (Firecrawl/Exa)
- **MCPClient**: Client for MCP Protocol for local or remote servers.

### Agent Usage and Development Guide
Read the [Agent Usage and Development Guide](./agents/README.md)  


## How to Use GitHub Issues

We encourage the community to open **GitHub issues** whenever you have a new idea or find something that needs attention. When creating an issue, please use our [Issue Template](./.github/ISSUE_TEMPLATE/general_issue_template.md) and select one of the following categories:

1. **Integration Request**  
   - For requests to integrate with a new data source (e.g., CoinGecko, arXiv) or a new AI use case.  
   - **Most important** for the community, as these issues help drive the direction of our framework's evolution.  
   - If you have an idea but aren't sure how to implement it, open an issue under this label so others can pick it up or offer suggestions.

2. **Bug**  
   - For reporting errors or unexpected behavior in the framework.  
   - Provide as much detail as possible (logs, steps to reproduce, environment, etc.).

3. **Question**  
   - For inquiries about usage, best practices, or clarifications on existing features.

4. **Bounty**  
   - For tasks with a **reward** (e.g., tokens, NFTs, or other benefits).  
   - The bounty label indicates that Heurist team or another community member are offering a reward to whoever resolves the issue.  
   - **Bounty Rules**:
     - Make sure to read the issue description carefully for scope and acceptance criteria.  
     - Once your Pull Request addressing the bounty is merged, we'll follow up on fulfilling the reward.  
     - Additional instructions (e.g., contact method) may be included in the issue itself.

### Picking Up an Issue

- Look for **Integration Requests** or **Bounty** issues if you want to contribute new features or earn rewards.  
- Feel free to discuss approaches in the comments. If you're ready to tackle it, mention "I'm working on this!" so others know it's in progress.

This process helps us stay organized, encourages community involvement, and keeps development transparent.

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

For Heurist Mesh agents or to learn about contributing specialized community agents, please refer to the [Mesh README](./mesh/README.md)

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. Join the Heurist Ecosystem Builder telegram https://t.me/heuristsupport


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=heurist-network/heurist-agent-framework&type=Date)](https://star-history.com/#heurist-network/heurist-agent-framework&Date)
