import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from decorators import with_cache
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

PUMPFUN_NOTE = (
    "graduation of pump.fun means that a newly launched token hits a certain market cap threshold, and that it has "
    "gained traction and liquidity."
)
GMGN_NOTE = "gmgn is a memecoin trading platform."

TRENDING_CHAIN_DATA_BASE_URL = "https://mesh-data.heurist.xyz/"
TELEGRAM_CHANNELS = ("overheardonct", "groupdigest")
TELEGRAM_CHANNELS_API_BASE_URL = "https://ask-backend.heurist.xyz/api/v1/public/telegram-channel"


class TrendingTokenAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Trending Token Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Aggregates trending tokens from GMGN, CoinGecko, Pump.fun, Dexscreener, and Twitter discussions.",
                "external_apis": ["GMGN", "CoinGecko", "Dexscreener", "Elfa", "AIXBT", "Telegram"],
                "tags": ["Token Trends", "Market Data"],
                "verified": True,
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/trending-token-agent.png",
                "examples": [
                    "Show me trending tokens",
                    "Get trending tokens including memecoins",
                    "What are the hottest tokens right now across all platforms?",
                    "Show me trending tokens from CoinGecko and Twitter only",
                    "What tokens have recently graduated from pump.fun?",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
                "erc8004": {
                    "enabled": True,
                    "supported_trust": ["reputation"],
                    "wallet_chain_id": 1,
                },
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
                    "description": "Get trending tokens that are most talked about and traded on CEXs and DEXs. Optionally get trending tokens on a specific chain.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Chain to get trending tokens for. Your default action is to keep it empty to get trending tokens across CEXs and chains. Include this field if specific chain is requested in the context.",
                                "enum": ["base", "ethereum", "solana", "bsc"],
                            },
                            "include_memes": {
                                "type": "boolean",
                                "description": "Include GMGN trending memecoins and Pump.fun recent graduated tokens. Keep it false by default. Include only if memecoins are specifically requested in the context.",
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_summary",
                    "description": "Get a summary of recent market-wide news including macroeconomics, major updates of well-known crypto projects and tokens, and most discussed topics on crypto Twitter and Telegram groups. This tool returns 10~20 bite-sized items about various topics like market trends, opportunities, catalysts and risks. Useful for knowing what's going on in crypto now.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "get_trending_tokens":
            include_memes = function_args.get("include_memes", False)
            chain = function_args.get("chain", "")
            return await self.get_trending_tokens(include_memes=include_memes, chain=chain)
        if tool_name == "get_market_summary":
            return await self.get_market_summary()
        return {"status": "error", "error": f"Unsupported tool '{tool_name}'"}

    def _normalize_tool_result(self, result: Any, context: str) -> Dict[str, Any]:
        if isinstance(result, Exception):
            logger.warning(f"{context} raised exception: {result}")
            return {"status": "error", "error": str(result)}
        if isinstance(result, dict):
            return result
        logger.warning(f"{context} returned unexpected payload type {type(result).__name__}")
        return {"status": "error", "error": "unexpected payload"}

    def _check_data_freshness(self, last_updated_str: str) -> Optional[str]:
        # Check if data is outdated (>1 day old).
        # last_updated_str: ISO format timestamp string
        try:
            last_updated = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
            if last_updated.tzinfo is None:
                last_updated = last_updated.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)
            age = now - last_updated

            if age > timedelta(days=1):
                return f"warning: data is outdated (last updated {age.days} day(s) ago)"
            return None
        except Exception as e:
            logger.warning(f"Failed to parse last_updated timestamp: {e}")
            return None

    def _is_date_stale(self, date_str: str, max_age_days: int = 3) -> bool:
        """Check if a date string is older than max_age_days."""
        try:
            parsed_date = datetime.fromisoformat(date_str.replace(" UTC", "+00:00"))
            age_days = (datetime.now(timezone.utc) - parsed_date).days
            return age_days > max_age_days
        except Exception as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            return True

    async def _fetch_aixbt_market_summary(self) -> Dict[str, Any]:
        result = await self._call_agent_tool_safe(
            "mesh.agents.aixbt_project_info_agent",
            "AIXBTProjectInfoAgent",
            "get_market_summary",
            {"lookback_days": 1},
            log_instance=logger,
            context="AIXBTProjectInfoAgent.get_market_summary",
        )
        normalized = self._normalize_tool_result(result, "AIXBTProjectInfoAgent.get_market_summary")
        if normalized.get("status") == "error" or "error" in normalized:
            return {
                "status": "error",
                "error": normalized.get("error", "AIXBT summary unavailable"),
            }

        data = normalized.get("data") if isinstance(normalized, dict) else None
        if not isinstance(data, dict):
            data = normalized if isinstance(normalized, dict) else {}

        summaries = data.get("summaries")
        if not summaries:
            return {"status": "error", "error": "No recent AIXBT market summary available"}

        return {"status": "success", "summary": summaries[0]}

    async def _fetch_telegram_channel(self, channel: str) -> Dict[str, Any]:
        url = f"{TELEGRAM_CHANNELS_API_BASE_URL}/{channel}"
        payload = await self._api_request(url=url, method="GET", params={"max_num": 10}, timeout=2)
        if not isinstance(payload, dict):
            return {"status": "error", "error": "unexpected response"}
        if "error" in payload:
            return {"status": "error", "error": payload["error"]}

        items = payload.get("items")
        if not items:
            return {"status": "error", "error": "empty response"}

        item = items[0] if items else None
        if not isinstance(item, dict):
            return {"status": "error", "error": "invalid item"}

        message_time = item.get("message_time")
        message = item.get("message", "")
        if not message_time or not message:
            return {"status": "error", "error": "missing fields"}
        if self._is_date_stale(message_time, max_age_days=3):
            return {"status": "error", "error": "stale item"}

        return {
            "status": "success",
            "item": {
                "channel": channel,
                "message": message,
                "message_time": message_time,
            },
        }

    async def _fetch_telegram_topics(self) -> Dict[str, Any]:
        task_map = {channel: self._fetch_telegram_channel(channel) for channel in TELEGRAM_CHANNELS}
        results = await asyncio.gather(*task_map.values(), return_exceptions=True)
        result_map = dict(zip(task_map.keys(), results))

        topics = []
        for channel, result in result_map.items():
            normalized = self._normalize_tool_result(result, f"telegram_channel[{channel}]")
            if normalized.get("status") == "error":
                continue
            item = normalized.get("item")
            if item:
                topics.append(item)

        status = "success" if topics else "error"
        return {"status": status, "topics": topics}

    @with_cache(ttl_seconds=3600)
    async def get_market_summary(self) -> Dict[str, Any]:
        aixbt_task = self._fetch_aixbt_market_summary()
        telegram_task = self._fetch_telegram_topics()
        funding_rate_task = self._call_agent_tool_safe(
            "mesh.agents.funding_rate_agent",
            "FundingRateAgent",
            "get_all_funding_rates",
            {},
            log_instance=logger,
            context="FundingRateAgent.get_all_funding_rates",
        )
        aixbt_result, telegram_result, funding_rate_result = await asyncio.gather(
            aixbt_task, telegram_task, funding_rate_task, return_exceptions=True
        )

        aixbt_result = self._normalize_tool_result(aixbt_result, "AIXBT market summary")
        telegram_result = self._normalize_tool_result(telegram_result, "Telegram topics")
        funding_rate_result = self._normalize_tool_result(funding_rate_result, "Funding rates")

        sections = []
        if aixbt_result.get("status") == "success":
            summary = aixbt_result.get("summary", {})
            news = summary.get("news", [])
            if news:
                date = summary.get("date", "unknown date")
                news_lines = "\n".join(f"- {item}" for item in news)
                sections.append(f"## AIXBT market summary ({date})\n{news_lines}")

        if telegram_result.get("status") == "success":
            topics = telegram_result.get("topics", [])
            if topics:
                topic_lines = "\n".join(f"- [{item.get('channel')}] {item.get('message')}" for item in topics)
                sections.append(f"## Most discussed topics in crypto Telegram groups\n{topic_lines}")

        summary_text = "\n\n".join(sections)
        has_success = bool(sections)

        funding_rates = None
        if "rates" in funding_rate_result:
            funding_rates = funding_rate_result

        payload = {
            "status": "success" if has_success else "error",
            "data": {
                "summary": summary_text,
                "funding_rates": funding_rates,
            },
        }
        if not has_success:
            payload["error"] = "Failed to fetch AIXBT market summary and telegram topics"
        return payload

    async def _fetch_chain_data(self, chain: str) -> Dict[str, Any]:
        """Fetch trending tokens from chain-specific API endpoint."""
        url = f"{TRENDING_CHAIN_DATA_BASE_URL}trending_tokens_{chain}.json"
        return await self._api_request(url, method="GET")

    async def get_trending_tokens(self, include_memes: bool = False, chain: str = "") -> Dict[str, Any]:
        # If chain is specified and it's not "base", only fetch chain-specific data
        if chain and chain != "base":
            chain_result = await self._fetch_chain_data(chain)
            if "error" in chain_result:
                return {"status": "error", "error": chain_result["error"]}

            notes = "The ranking is based on multiple factors including DEX volume and social discussions."
            if "last_updated" in chain_result:
                warning = self._check_data_freshness(chain_result["last_updated"])
                if warning:
                    notes = f"{warning}. {notes}"

            return {"status": "success", "data": {f"{chain}_trending": chain_result, "notes": notes}}

        # For chain="base" or no chain specified, continue with full aggregation
        task_map = {
            "coingecko": self._call_agent_tool_safe(
                "mesh.agents.coingecko_token_info_agent",
                "CoinGeckoTokenInfoAgent",
                "get_trending_coins",
                {},
                log_instance=logger,
                context="CoinGeckoTokenInfoAgent.get_trending_coins",
            ),
            "twitter": self._call_agent_tool_safe(
                "mesh.agents.elfa_twitter_intelligence_agent",
                "ElfaTwitterIntelligenceAgent",
                "get_trending_tokens",
                {"time_window": "24h"},
                log_instance=logger,
                context="ElfaTwitterIntelligenceAgent.get_trending_tokens",
            ),
        }

        if chain == "base":
            task_map["base_chain"] = self._fetch_chain_data(chain)

        if include_memes:
            task_map["gmgn"] = self._call_agent_tool_safe(
                "mesh.agents.unifai_token_analysis_agent",
                "UnifaiTokenAnalysisAgent",
                "get_gmgn_trend",
                {"time_window": "24h", "limit": 10},
                log_instance=logger,
                context="UnifaiTokenAnalysisAgent.get_gmgn_trend",
            )
            task_map["pumpfun"] = self._call_agent_tool_safe(
                "mesh.agents.pumpfun_token_agent",
                "PumpFunTokenAgent",
                "query_latest_graduated_tokens",
                {"timeframe": 12},
                log_instance=logger,
                context="PumpFunTokenAgent.query_latest_graduated_tokens",
            )

        results = await asyncio.gather(*task_map.values(), return_exceptions=True)
        result_map = dict(zip(task_map.keys(), results))

        coingecko_result = self._normalize_tool_result(
            result_map["coingecko"], "CoinGeckoTokenInfoAgent.get_trending_coins"
        )
        twitter_result = self._normalize_tool_result(
            result_map["twitter"], "ElfaTwitterIntelligenceAgent.get_trending_tokens"
        )

        aggregated = {
            "coingecko_trending": coingecko_result,
            "twitter_trending": twitter_result,
        }

        notes_parts = [
            "Trending tokens on coingecko and twitter include CEX and DEX tokens, and Twitter trends may include stock tickers."
        ]

        # Process Base chain data if fetched
        if "base_chain" in result_map:
            base_chain_result = self._normalize_tool_result(result_map["base_chain"], "_fetch_chain_data[base]")
            aggregated["base_trending"] = base_chain_result

            if "last_updated" in base_chain_result:
                warning = self._check_data_freshness(base_chain_result["last_updated"])
                if warning:
                    notes_parts.append(f"Base chain data: {warning}.")

        if include_memes:
            gmgn_result = self._normalize_tool_result(result_map["gmgn"], "UnifaiTokenAnalysisAgent.get_gmgn_trend")
            pumpfun_result = self._normalize_tool_result(
                result_map["pumpfun"], "PumpFunTokenAgent.query_latest_graduated_tokens"
            )

            aggregated["gmgn_trending"] = gmgn_result
            aggregated["pumpfun_recent_graduated"] = pumpfun_result

            if self._has_useful_data(pumpfun_result, data_key="graduated_tokens"):
                notes_parts.append(PUMPFUN_NOTE)
            if self._has_useful_data(gmgn_result):
                notes_parts.append(GMGN_NOTE)

        aggregated["notes"] = " ".join(notes_parts)

        return {"status": "success", "data": aggregated}
