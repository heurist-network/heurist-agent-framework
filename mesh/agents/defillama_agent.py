import logging
from typing import Any, Dict, List, Optional

from clients.defillama_client import DefiLlamaClient
from decorators import with_cache
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class DefiLlamaAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.client = DefiLlamaClient()

        self.metadata.update(
            {
                "name": "DefiLlama Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Provides DeFi protocol, chain, and yield metrics including TVL, fees, volume, and yield trend analysis from DefiLlama.",
                "external_apis": ["DefiLlama"],
                "tags": ["DeFi", "Analytics"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/DefiLlama.png",
                "examples": [
                    "What is the TVL of Aave?",
                    "Get metrics for Uniswap V3",
                    "How much fees does Ethereum generate?",
                    "What are the top protocols on Solana by fees?",
                    "Get chain metrics for Base",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """You are a DeFi analytics assistant powered by DefiLlama data. You provide accurate metrics about DeFi protocols, blockchains, and yield pools including TVL (Total Value Locked), fees, trading volume, APY, and trends.

When asked about protocols, use lowercase slugs with hyphens (e.g., 'aave-v3', 'uniswap-v3', 'curve-dex').
When asked about chains, use proper case names (e.g., 'Ethereum', 'Solana', 'Base').

Present data clearly with appropriate context. Explain trends (WoW = week-over-week, MoM = month-over-month) when relevant. Be concise and factual."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_protocol_metrics",
                    "description": "Get metrics for a DeFi protocol including TVL, fees, volume (for DEXes), revenue, deployed chains, and growth trend. Use this tool when you want to analyze a DeFi project. You must input the defillama slug obtained from project knowledge base.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "protocol": {
                                "type": "string",
                                "description": "Protocol slug (e.g., 'aave-v3', 'curve-dex')",
                            }
                        },
                        "required": ["protocol"],
                    },
                    "verified": True,
                    "recommended": True,
                    "credits": {"default": 1},
                    "x402_config": {
                        "enabled": True,
                        "default_price_usd": "0.01",
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_chain_metrics",
                    "description": "Get metrics for a blockchain including TVL, fees, top protocols by fees, and growth trends.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain name (e.g., 'Solana', 'Base')",
                            }
                        },
                        "required": ["chain"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_yield_pools",
                    "description": "Search DefiLlama yield pools with optional filters for projects, chains, symbols, and stablecoin flag. Returns compact results with APY and TVL trend metrics. List filters (projects/chains/symbols) use OR matching, while different filter types are combined with AND.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "projects": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional project slugs (e.g., ['aave-v3', 'curve-dex'])",
                            },
                            "chains": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional chain names (e.g., ['Ethereum', 'Arbitrum'])",
                            },
                            "symbols": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional token symbols (e.g., ['USDC', 'USDT'])",
                            },
                            "stablecoin": {
                                "type": "boolean",
                                "description": "Optional stablecoin-only filter",
                            },
                            "sort_by": {
                                "type": "string",
                                "description": "Sort field: APY or TVL",
                                "enum": ["apy", "tvl"],
                                "default": "apy",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of pools to return (1-50)",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50,
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

    @with_cache(ttl_seconds=3600)
    async def _get_protocol_metrics(self, protocol: str) -> Dict[str, Any]:
        return await self.client.get_protocol_enriched_async(protocol.lower().strip())

    @with_cache(ttl_seconds=3600)
    async def _get_chain_metrics(self, chain: str) -> Dict[str, Any]:
        return await self.client.get_chain_enriched_async(chain.strip())

    @with_cache(ttl_seconds=120)
    async def _search_yield_pools(
        self,
        projects: Optional[List[str]] = None,
        chains: Optional[List[str]] = None,
        symbols: Optional[List[str]] = None,
        stablecoin: Optional[bool] = None,
        sort_by: str = "apy",
        limit: int = 10,
    ) -> Dict[str, Any]:
        return await self.client.search_yield_pools_async(
            projects=projects,
            chains=chains,
            symbols=symbols,
            stablecoin=stablecoin,
            sort_by=sort_by,
            limit=limit,
        )

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "get_protocol_metrics":
            return await self._get_protocol_metrics(function_args["protocol"])
        elif tool_name == "get_chain_metrics":
            return await self._get_chain_metrics(function_args["chain"])
        elif tool_name == "search_yield_pools":
            return await self._search_yield_pools(
                projects=function_args.get("projects"),
                chains=function_args.get("chains"),
                symbols=function_args.get("symbols"),
                stablecoin=function_args.get("stablecoin"),
                sort_by=function_args.get("sort_by", "apy"),
                limit=function_args.get("limit", 10),
            )
        return {"error": f"Unknown tool: {tool_name}"}

    async def cleanup(self):
        await self.client.close()
        await super().cleanup()
