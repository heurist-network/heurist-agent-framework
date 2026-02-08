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
                "description": "Provides DeFi protocol and blockchain metrics including TVL, fees, volume, and trend analysis from DefiLlama.",
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
        return """You are a DeFi analytics assistant powered by DefiLlama data. You provide accurate metrics about DeFi protocols and blockchains including TVL (Total Value Locked), fees, trading volume, and trends.

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
                    "credits": 1,
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
        ]

    @with_cache(ttl_seconds=3600)
    async def _get_protocol_metrics(self, protocol: str) -> Dict[str, Any]:
        return await self.client.get_protocol_enriched_async(protocol.lower().strip())

    @with_cache(ttl_seconds=3600)
    async def _get_chain_metrics(self, chain: str) -> Dict[str, Any]:
        return await self.client.get_chain_enriched_async(chain.strip())

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "get_protocol_metrics":
            return await self._get_protocol_metrics(function_args["protocol"])
        elif tool_name == "get_chain_metrics":
            return await self._get_chain_metrics(function_args["chain"])
        return {"error": f"Unknown tool: {tool_name}"}

    async def cleanup(self):
        await self.client.close()
        await super().cleanup()
