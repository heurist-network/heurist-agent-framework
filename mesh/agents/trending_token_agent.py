import asyncio
import logging
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

PUMPFUN_NOTE = (
    "graduation of pump.fun means that a newly launched token hits a certain market cap threshold, and that it has "
    "gained traction and liquidity."
)
GMGN_NOTE = "gmgn is a memecoin trading platform."


class TrendingTokenAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Trending Token Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Aggregates trending tokens from GMGN, CoinGecko, Pump.fun, and social media intelligence sources.",
                "external_apis": ["GMGN", "CoinGecko", "Bitquery", "ELFA"],
                "tags": ["Token Trends", "Market Data"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Heurist.png",
                "examples": [
                    "get_trending_tokens",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You aggregate trending token feeds across multiple data providers. Return concise structured data from each "
            "source without additional analysis. Highlight when a data source is unavailable."
        )

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_trending_tokens",
                    "description": "Aggregate trending tokens from CoinGecko, Crypto Twitter top mentions (24h), and optionally GMGN (24h, top 10) and Pump.fun graduations (12h).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "include_memes": {
                                "type": "boolean",
                                "description": "Include GMGN trending memecoins and Pump.fun recent graduated tokens. Default is false.",
                                "default": False,
                            }
                        },
                        "required": [],
                    },
                },
            }
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "get_trending_tokens":
            include_memes = function_args.get("include_memes", False)
            return await self.get_trending_tokens(include_memes=include_memes)
        return {"status": "error", "error": f"Unsupported tool '{tool_name}'"}

    def _normalize_tool_result(self, result: Any, context: str) -> Dict[str, Any]:
        if isinstance(result, Exception):
            logger.warning(f"{context} raised exception: {result}")
            return {"status": "error", "error": str(result)}
        if isinstance(result, dict):
            return result
        logger.warning(f"{context} returned unexpected payload type {type(result).__name__}")
        return {"status": "error", "error": "unexpected payload"}

    @with_cache(ttl_seconds=3600)
    @with_retry(max_retries=2)
    async def get_trending_tokens(self, include_memes: bool = False) -> Dict[str, Any]:
        # Always fetch CoinGecko and Twitter
        coingecko_task = self._call_agent_tool_safe(
            "mesh.agents.coingecko_token_info_agent",
            "CoinGeckoTokenInfoAgent",
            "get_trending_coins",
            {},
            log_instance=logger,
            context="CoinGeckoTokenInfoAgent.get_trending_coins",
        )
        twitter_task = self._call_agent_tool_safe(
            "mesh.agents.elfa_twitter_intelligence_agent",
            "ElfaTwitterIntelligenceAgent",
            "get_trending_tokens",
            {"time_window": "24h"},
            log_instance=logger,
            context="ElfaTwitterIntelligenceAgent.get_trending_tokens",
        )

        tasks = [coingecko_task, twitter_task]

        # Optionally fetch GMGN and Pump.fun if include_memes is True
        if include_memes:
            gmgn_task = self._call_agent_tool_safe(
                "mesh.agents.unifai_token_analysis_agent",
                "UnifaiTokenAnalysisAgent",
                "get_gmgn_trend",
                {"time_window": "24h", "limit": 10},
                log_instance=logger,
                context="UnifaiTokenAnalysisAgent.get_gmgn_trend",
            )
            pumpfun_task = self._call_agent_tool_safe(
                "mesh.agents.pumpfun_token_agent",
                "PumpFunTokenAgent",
                "query_latest_graduated_tokens",
                {"timeframe": 12},
                log_instance=logger,
                context="PumpFunTokenAgent.query_latest_graduated_tokens",
            )
            tasks.extend([gmgn_task, pumpfun_task])

        results = await asyncio.gather(*tasks, return_exceptions=True)

        coingecko_result = self._normalize_tool_result(results[0], "CoinGeckoTokenInfoAgent.get_trending_coins")
        twitter_result = self._normalize_tool_result(results[1], "ElfaTwitterIntelligenceAgent.get_trending_tokens")

        aggregated = {
            "coingecko_trending": coingecko_result,
            "twitter_trending": twitter_result,
        }

        notes_parts = []

        if include_memes:
            gmgn_result = self._normalize_tool_result(results[2], "UnifaiTokenAnalysisAgent.get_gmgn_trend")
            pumpfun_result = self._normalize_tool_result(results[3], "PumpFunTokenAgent.query_latest_graduated_tokens")

            aggregated["gmgn_trending"] = gmgn_result
            aggregated["pumpfun_recent_graduated"] = pumpfun_result

            if self._has_useful_data(pumpfun_result, data_key="graduated_tokens"):
                notes_parts.append(PUMPFUN_NOTE)
            if self._has_useful_data(gmgn_result):
                notes_parts.append(GMGN_NOTE)

        aggregated["notes"] = " ".join(notes_parts)

        return {"status": "success", "data": aggregated}
