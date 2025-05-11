# Heurist Mesh

![mesh-2](https://github.com/user-attachments/assets/ae8987db-f009-4cbb-9e8d-1ebc828f1810)

🧩 **Heurist Mesh** is an open network of modular and purpose-built AI agents. Each agent is a specialized unit that can process data, generate reports, or engage in conversations, while collectively forming an intelligent swarm to tackle complex tasks. Built on decentralized compute and powered by diverse open-source AI models, Mesh agents can be combined into powerful workflows for cost-efficient and highly flexible solutions. Once a Mesh agent is added to this Github main branch, it's automatically deployed and instantly available via REST API and MCP.

## Using Mesh Agents

> [!NOTE]
> For detailed API documentation including examples of both synchronous and asynchronous usage, please refer to the [official Heurist Mesh documentation](https://docs.heurist.ai/dev-guide/heurist-mesh/).

Mesh agents hosted by Heurist can be accessed via two interfaces:

- **Synchronous API** - Direct, immediate responses for quick queries and actions
- **Asynchronous API** - For longer-running tasks or when you want to track the reasoning process

To use any Mesh agent, you'll need a Heurist API key, get one at [https://heurist.ai/credits](https://www.heurist.ai/credits).

## MCP (Model Context Protocol)

Model Context Protocol allows AI assistants like Claude to directly interact with Heurist Mesh agents as tools.

**[Heurist Mesh MCP Portal](https://mcp.heurist.ai)** - The fastest way to get started with our MCP integration with no setup required!

For self-hosting with complete control, check out our [heurist-mesh-mcp-server](https://github.com/heurist-network/heurist-mesh-mcp-server/blob/main/README.md).

## How It Works

- **Mesh Agents** can process information from external APIs, or access other mesh agents.
- Agents run on a decentralized compute layer, and each agent can optionally use external APIs, Large Language Models, or other tools provided by Heurist and 3rd parties.
- **Agent Developers** can contribute by adding specialized agents to the network. Each invocation of an agent can generate pay-per-use revenue for the agent's author.
- **Users or Developers** get access to a rich library of pre-built, purpose-driven AI agents they can seamlessly integrate into their products or workflows via REST APIs or frontend interface usage.

## Building a New Mesh Agent

### Setup & Development

1. **Create virtual environment**:

```bash
cd mesh
uv sync
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. **Create your agent**:

```python
from mesh.mesh_agent import MeshAgent
from typing import Dict, Any, List

class MySpecialAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update({
            'name': 'My Special Agent',
            'version': '1.0.0',
            'author': 'Your Name',
            'author_address': '0xYourEthereumAddress',
            'description': 'This agent can do...',
            'external_apis': ['API_Name'],
            'tags': ['Category1', 'Category2'],
            'image_url': 'https://example.com/image.png',
            'examples': ['Example query 1', 'Example query 2'],
        })

    def get_system_prompt(self) -> str:
        """Return the system prompt for the agent"""
        return """
        You are a helpful assistant that can [describe agent's purpose].
        [Include any specific instructions for the LLM here]
        """

    def get_tool_schemas(self) -> List[Dict]:
        """Define the tools that your agent exposes"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "my_tool_name",
                    "description": "Description of what this tool does",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "param1": {"type": "string", "description": "Description of parameter 1"},
                            "param2": {"type": "number", "description": "Description of parameter 2"},
                        },
                        "required": ["param1"]
                    }
                }
            }
        ]

    async def _handle_tool_logic(self, tool_name: str, function_args: dict) -> Dict[str, Any]:
        """Handle the execution of your agent's tools"""
        if tool_name == "my_tool_name":
            # Implement your tool logic here
            param1 = function_args.get("param1")
            param2 = function_args.get("param2", 0)  # Default value if not provided

            # Call your API or process data here
            result = await self._api_request(
                url="https://api.example.com/endpoint",
                method="GET",
                headers={"Authorization": "Bearer your_api_key"},
                params={"query": param1}
            )

            # Check for errors
            if errors := self._handle_error(result):
                return errors

            # Return processed data
            return {
                "status": "success",
                "data": {"result": result}
            }

        return {"error": f"Unsupported tool: {tool_name}"}
```

3. **Test your agent**:

   - Create `mesh/tests/my_special_agent.py` with a basic test:

   ```python
   import asyncio
   import yaml
   from mesh.agents.my_special_agent import MySpecialAgent

   async def test_agent():
       agent = MySpecialAgent()
       # Test natural language query
       response = await agent.call_agent({"query": "Run a test query"})
       print(yaml.dump(response))

       # Test direct tool call
       response = await agent.call_agent({
           "tool": "my_tool_name",
           "tool_arguments": {"param1": "test value", "param2": 123}
       })
       print(yaml.dump(response))

   if __name__ == "__main__":
       asyncio.run(test_agent())
   ```

   - Run: `python mesh/tests/my_special_agent.py`

4. **Start local server**:

```bash
uvicorn mesh.mesh_api:app --reload
```

## Contributor Guidelines

1. **Fork & branch** the repository
2. **Add your agent** under `mesh/`
3. **Test** locally and with external dependencies
4. **Submit PR** with clear description of agent functionality
5. **Deployment** happens automatically after merge

### Coding Style and Best Practices

- Use Python **type hints** and **docstrings** for clarity
- Design for **modularity** with each agent focused on a single domain
- Use [decorators](https://github.com/heurist-network/heurist-agent-framework/blob/main/decorators.py) for API caching and retry
- Support natural language in `query` parameter (e.g., both "tell me about Ethereum" and "analyze ETH" should be accepted)

### Metadata Requirements

Each agent's `metadata` dictionary should at least contain:

- `name`: Human-readable name of the agent.
- `version`: Agent version (e.g., `1.0.0`).
- `author`: Name or handle of the contributor.
- `author_address`: Ethereum address (or any relevant address) for potential revenue share.
- `description`: Short, clear summary of your agent's purpose.
- `external_apis`: Any external service your agent accesses (e.g., `['DefiLlama']`).
- `tags`: Keywords or categories to help users discover your agent.

## Examples

We have included example agents in this folder:

1. **Allora Price Prediction Agent** ([allora_price_prediction_agent.py](./agents/allora_price_prediction_agent.py))

   - Fetches and predicts short-term crypto prices using Allora's API.
   - Demonstrates how to integrate external APIs, handle asynchronous calls, and structure multi-step logic.

2. **DuckDuckGo Search Agent** ([duckduckgo_search_agent.py](./agents/duckduckgo_search_agent.py))
   - Fetches and analyzes web search results using DuckDuckGo's API.
   - Shows how to process user queries, connect to external search services, and return structured results.

Each example agent has a corresponding test script in `mesh/tests/` that demonstrates how to run the agent and produce an example output file (in YAML).

## Contact & Support

- **Issues**: If you find bugs or have questions, open an issue on the [GitHub repository](https://github.com/heurist-network/heurist-agent-framework/issues).
- **Community Chat**: Join our [Discord](https://discord.com/invite/heuristai) or [Telegram Builder Group](https://t.me/heuristsupport) for real-time support or to showcase your new agents.

> **Happy Hacking & Welcome to the Mesh!**

---

## Appendix: All Available Mesh Agents

| Agent ID | Description | Available Tools | Source Code | External APIs |
|----------|-------------|-----------------|-------------|---------------|
| AIXBTProjectInfoAgent | This agent can retrieve trending project information including fundamental analysis, social activity, and recent developments using the aixbt API | • search_projects | [Source](./agents/aixbt_project_info_agent.py) | aixbt |
| AaveAgent | This agent can report the status of Aave v3 protocols deployed on Ethereum, Polygon, Avalanche, and Arbitrum with details on liquidity, borrowing rates, and more | • get_aave_reserves | [Source](./agents/aave_agent.py) | Aave |
| AlloraPricePredictionAgent | This agent can predict the price of ETH/BTC with confidence intervals using Allora price prediction API | • get_allora_prediction | [Source](./agents/allora_price_prediction_agent.py) | Allora |
| BitquerySolanaTokenInfoAgent | This agent provides comprehensive analysis of Solana tokens using Bitquery API. It can analyze token metrics (volume, price, liquidity), track holders and buyers, monitor trading activity, and identify trending tokens. The agent supports both specific token analysis and market-wide trend discovery. | • query_token_metrics<br>• query_token_holders<br>• query_token_buyers<br>• query_top_traders<br>• query_holder_status<br>• get_top_trending_tokens | [Source](./agents/bitquery_solana_token_info_agent.py) | Bitquery |
| CarvOnchainDataAgent | This agent can query blockchain metrics of Ethereum, Base, Bitcoin, or Solana using natural language through the CARV API. | • query_onchain_data | [Source](./agents/carv_onchain_data_agent.py) | CARV |
| CoinGeckoTokenInfoAgent | This agent can fetch token information, market data, trending coins, and category data from CoinGecko. | • get_token_info<br>• get_trending_coins<br>• get_token_price_multi<br>• get_categories_list<br>• get_category_data<br>• get_tokens_by_category | [Source](./agents/coingecko_token_info_agent.py) | Coingecko |
| CookieProjectInfoAgent | This agent provides information about crypto projects using Cookie API, including project details by Twitter username and contract address. | • get_project_by_twitter_username<br>• get_project_by_contract_address | [Source](./agents/cookie_project_info_agent.py) | Cookie API |
| DeepResearchAgent | Advanced research agent that performs multi-level web searches with recursive exploration, analyzes content across sources, and produces comprehensive research reports with key insights | • deep_research | [Source](./agents/deep_research_agent.py) | Firecrawl |
| DexScreenerTokenInfoAgent | This agent fetches real-time DEX trading data and token information across multiple chains using DexScreener API | • search_pairs<br>• get_specific_pair_info<br>• get_token_pairs | [Source](./agents/dexscreener_token_info_agent.py) | DexScreener |
| DuckDuckGoSearchAgent | This agent can fetch and analyze web search results using DuckDuckGo API and provide intelligent summaries. | • search_web | [Source](./agents/duckduckgo_search_agent.py) | DuckDuckGo |
| ElfaTwitterIntelligenceAgent | This agent analyzes a token or a topic or a Twitter account using Twitter data and Elfa API. It highlights smart influencers. | • search_mentions<br>• search_account<br>• get_trending_tokens | [Source](./agents/elfa_twitter_intelligence_agent.py) | Elfa |
| ExaSearchAgent | This agent can search the web using Exa's API and provide direct answers to questions. | • exa_web_search<br>• exa_answer_question | [Source](./agents/exa_search_agent.py) | Exa |
| FirecrawlSearchAgent | Advanced search agent that uses Firecrawl to perform research with intelligent query generation and content analysis. | • firecrawl_web_search<br>• firecrawl_extract_web_data | [Source](./agents/firecrawl_search_agent.py) | Firecrawl |
| FundingRateAgent | This agent can fetch funding rate data and identify arbitrage opportunities across cryptocurrency exchanges. | • get_all_funding_rates<br>• get_symbol_funding_rates<br>• find_cross_exchange_opportunities<br>• find_spot_futures_opportunities | [Source](./agents/funding_rate_agent.py) | Coinsider |
| GoplusAnalysisAgent | This agent can fetch and analyze security details of blockchain token contracts using GoPlus API. | • fetch_security_details | [Source](./agents/goplus_analysis_agent.py) | GoPlus |
| MasaTwitterSearchAgent | This agent can search on Twitter through Masa API and analyze the results by identifying trending topics and sentiment related to a topic. | • search_twitter | [Source](./agents/masa_twitter_search_agent.py) | Masa |
| MetaSleuthSolTokenWalletClusterAgent | This agent can analyze the wallet clusters holding a specific Solana token, and identify top holder behavior, concentration, and potential market manipulation. | • fetch_token_clusters<br>• fetch_cluster_details | [Source](./agents/metasleuth_sol_token_wallet_cluster_agent.py) | MetaSleuth |
| MindAiKolAgent | This agent analyzes Key Opinion Leaders (KOLs) and token performance in the crypto space using Mind AI API. | • get_best_initial_calls<br>• get_kol_statistics<br>• get_token_statistics<br>• get_top_gainers | [Source](./agents/mindai_kol_agent.py) | Mind AI |
| MoniTwitterInsightAgent | This agent analyzes Twitter accounts providing insights on smart followers, mentions, and account activity. | • get_smart_followers_history<br>• get_smart_followers_categories<br>• get_smart_mentions_feed | [Source](./agents/moni_twitter_insight_agent.py) | Moni |
| PondWalletAnalysisAgent | This agent analyzes cryptocurrency wallet activities across Ethereum, Solana, and Base networks using the Cryptopond API. | • analyze_ethereum_wallet<br>• analyze_solana_wallet<br>• analyze_base_wallet | [Source](./agents/pond_wallet_analysis_agent.py) | Cryptopond |
| PumpFunTokenAgent | This agent analyzes Pump.fun token on Solana using Bitquery API. It tracks token creation and graduation events on Pump.fun. | • query_recent_token_creation<br>• query_latest_graduated_tokens | [Source](./agents/pumpfun_token_agent.py) | Bitquery |
| SolWalletAgent | This agent can query Solana wallet assets and recent swap transactions using Helius API. | • get_wallet_assets<br>• analyze_common_holdings_of_top_holders<br>• get_tx_history | [Source](./agents/sol_wallet_agent.py) | Helius |
| SpaceTimeAgent | This agent can analyze blockchain data by executing SQL queries from natural language using Space and Time, a database with ZK proofs. | • generate_and_execute_sql | [Source](./agents/space_and_time_agent.py) | Space and Time |
| TokenMetricsAgent | This agent provides market insights, sentiment analysis, and resistance/support data for cryptocurrencies using TokenMetrics API. | • get_sentiments<br>• get_resistance_support_levels<br>• get_token_info | [Source](./agents/tokenmetrics_agent.py) | TokenMetrics |
| TruthSocialAgent | This agent can retrieve and analyze posts from Donald Trump on Truth Social. | • get_trump_posts | [Source](./agents/truth_social_agent.py) | Apify |
| TwitterInfoAgent | This agent fetches a Twitter user's profile information and recent tweets. It's useful for getting project updates or tracking key opinion leaders (KOLs) in the space. | • get_user_tweets<br>• get_twitter_detail<br>• get_general_search | [Source](./agents/twitter_info_agent.py) | Twitter API |
| UnifaiTokenAnalysisAgent | This agent provides token analysis using UnifAI's API, including GMGN trend analysis (GMGN is a memecoin trading platform) and comprehensive token analysis for various cryptocurrencies | • get_gmgn_trend<br>• get_gmgn_token_info<br>• analyze_token | [Source](./agents/unifai_token_analysis_agent.py) | UnifAI |
| UnifaiWeb3NewsAgent | This agent fetches the latest Web3 and cryptocurrency news using UnifAI's API | • get_web3_news | [Source](./agents/unifai_web3_news_agent.py) | UnifAI |
| ZerionWalletAnalysisAgent | This agent can fetch and analyze the token and NFT holdings of a crypto wallet (must be EVM chain) | • fetch_wallet_tokens<br>• fetch_wallet_nfts | [Source](./agents/zerion_wallet_analysis_agent.py) | Zerion |
---  

_This document is a work-in-progress. Please feel free to update and improve it as the system evolves._
