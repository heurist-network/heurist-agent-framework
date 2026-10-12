import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()

BASE_URL = "https://events.pokt-agent.com"
EVENT_TYPES = [
    "WARNING_SET",
    "WARNING_CLEARED",
    "CAUTION_SET",
    "CAUTION_CLEARED",
    "DELISTING",
    "DEPOSIT_SUSPENDED",
    "DEPOSIT_RESUMED",
    "WITHDRAWAL_SUSPENDED",
    "WITHDRAWAL_RESUMED",
    "NETWORK_UPGRADE",
    "LISTING",
    "OTHER",
]


class KoreanExchangeRiskAgent(MeshAgent):
    """Upbit and Bithumb risk events (trading warnings, caution flags, delistings,
    deposit/withdrawal suspensions, new KRW listings) as structured English data.

    Korean exchange notices move prices but are published in Korean only. The data comes from
    POKT Agent's kr-crypto-events service, which polls both exchanges' official notice boards and
    market APIs every 10 minutes and normalises each notice into a typed event.
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("POKT_AGENT_API_KEY")
        self.metadata.update(
            {
                "name": "Korean Exchange Risk Agent",
                "version": "1.0.0",
                "author": "POKT Agent",
                "author_address": "0xC724e18704AC2AB701e7bb25692C289C449dDD71",
                "description": "Upbit and Bithumb risk events in English: trading warning and caution flags, delisting dates, deposit/withdrawal suspensions and new KRW listings, plus the current Korean exchange status of any coin.",
                "external_apis": ["POKT Agent kr-crypto-events (Upbit, Bithumb)"],
                "tags": ["Trading", "Market Data", "Korea"],
                "image_url": "",
                "examples": [
                    "Which coins did Upbit or Bithumb flag with a trading warning this week?",
                    "Is ICX being delisted from any Korean exchange?",
                    "Show deposit and withdrawal suspensions on Bithumb in the last 3 days",
                    "What new KRW listings were announced recently?",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You report risk events from the two largest Korean crypto exchanges, Upbit and Bithumb.

        CAPABILITIES:
        - List recent exchange events: trading warning (투자유의) and caution (투자주의) designations
          and releases, delisting announcements with effective dates, deposit/withdrawal suspensions
          and resumptions, network upgrades and new KRW listings.
        - Report the current Korean exchange status of one coin: listed markets, warning/caution
          flags, pending delisting and active suspensions on each exchange.

        RESPONSE GUIDELINES:
        - Lead with what matters for a trader: delistings and their effective dates, new warnings,
          suspensions that block transfers (these often drive the Korea premium).
        - Always name the exchange and give dates in UTC as returned.
        - Quote the event summary_en; mention the official notice URL when present.
        - If nothing matches, say so plainly.

        IMPORTANT:
        - NEVER make up data that is not returned from the tools.
        - This is exchange notice data, not investment advice.
        """

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_korean_exchange_events",
                    "description": "List recent Upbit/Bithumb risk events (warnings, cautions, delistings, deposit/withdrawal suspensions, network upgrades, new KRW listings), newest first. Use for questions like 'what did Upbit flag this week' or 'recent Bithumb suspensions'.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "exchange": {
                                "type": "string",
                                "enum": ["upbit", "bithumb"],
                                "description": "Only this exchange (omit for both).",
                            },
                            "event_types": {
                                "type": "array",
                                "items": {"type": "string", "enum": EVENT_TYPES},
                                "description": "Only these event types (omit for all).",
                            },
                            "ticker": {
                                "type": "string",
                                "description": "Only events for this coin symbol, e.g. ICX.",
                            },
                            "since": {
                                "type": "string",
                                "description": "Only events announced at or after this ISO 8601 time, e.g. 2026-10-01T00:00:00Z.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of events (1-100).",
                                "default": 20,
                            },
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_korean_exchange_coin_status",
                    "description": "Current Korean exchange status of one coin on Upbit and Bithumb: listed KRW/BTC/USDT markets, trading warning and caution flags, pending delisting with its effective date, and active deposit/withdrawal suspensions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Coin symbol, e.g. BTC, XRP, ICX.",
                            },
                        },
                        "required": ["symbol"],
                    },
                },
            },
        ]

    # ------------------------------------------------------------------------
    #                      API-SPECIFIC METHODS
    # ------------------------------------------------------------------------
    def _headers(self) -> Dict[str, str]:
        return {"x-api-key": self.api_key or "", "accept": "application/json"}

    @with_cache(ttl_seconds=120)
    @with_retry(max_retries=2)
    async def get_korean_exchange_events(
        self,
        exchange: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        ticker: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": max(1, min(int(limit or 20), 100))}
        if exchange:
            params["exchange"] = exchange.lower()
        if event_types:
            params["type"] = ",".join(t.upper() for t in event_types)
        if ticker:
            params["ticker"] = ticker.upper().strip()
        if since:
            params["since"] = since
        return await self._api_request(f"{BASE_URL}/v1/events", headers=self._headers(), params=params)

    @with_cache(ttl_seconds=120)
    @with_retry(max_retries=2)
    async def get_korean_exchange_coin_status(self, symbol: str) -> Dict[str, Any]:
        return await self._api_request(
            f"{BASE_URL}/v1/ticker", headers=self._headers(), params={"symbol": symbol.upper().strip()}
        )

    # ------------------------------------------------------------------------
    #                      TOOL HANDLING LOGIC
    # ------------------------------------------------------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "POKT_AGENT_API_KEY is not configured"}

        if tool_name == "get_korean_exchange_events":
            result = await self.get_korean_exchange_events(
                exchange=function_args.get("exchange"),
                event_types=function_args.get("event_types"),
                ticker=function_args.get("ticker"),
                since=function_args.get("since"),
                limit=function_args.get("limit", 20),
            )
        elif tool_name == "get_korean_exchange_coin_status":
            symbol = function_args.get("symbol")
            if not symbol:
                return {"error": "symbol is required"}
            result = await self.get_korean_exchange_coin_status(symbol)
        else:
            return {"error": f"Unsupported tool '{tool_name}'"}

        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}
