import logging
import os
from typing import Any, Dict, List, Optional

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

MOMUS_BASE_URL = "https://momusai.io/api/agent"


class MomusPredictionMarketAgent(MeshAgent):
    """
    Momus — Prediction Market Intelligence.

    Momus is an autonomous AI betting agent that stakes its own capital on prediction markets in public, with every
    bet, pass and loss on the record (momusai.io). This agent exposes its models: football match probabilities from a
    self-fitted Dixon-Coles model, MLB win probabilities from a pitcher-aware Elo, US midterms 2026 control odds
    priced against Polymarket and Kalshi, and tennis reads priced on Meridian (Robinhood Chain).
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("MOMUS_API_KEY")
        if not self.api_key:
            raise ValueError("MOMUS_API_KEY environment variable is required")
        self.headers = {"x-momus-agent-key": self.api_key, "x-momus-venue": "heurist", "Content-Type": "application/json"}

        self.metadata.update(
            {
                "name": "Momus Prediction Market Agent",
                "version": "1.0.0",
                "author": "Momus (momusai.io)",
                "author_address": "0x370e246f9a0f7969a59469D5A3beBDE5F6A73c68",
                "description": "Prediction-market and sports intelligence from Momus, an AI agent that bets its own capital in public: football 1X2 probabilities with fair odds and likely scores, MLB win probabilities, US midterms Senate/House odds vs Polymarket and Kalshi, and tennis reads priced on-chain.",
                "external_apis": ["Momus"],
                "tags": ["Prediction Markets", "Sports", "Betting", "Politics"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Momus.png",
                "examples": [
                    "What are the odds for Real Madrid vs Barcelona?",
                    "Give me Momus's fair price for Arsenal vs Liverpool",
                    "Who wins Padres at Brewers tonight?",
                    "What are the chances Republicans keep the Senate?",
                    "What is Momus's latest tennis read?",
                ],
                "credits": {"default": 1},
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.05",
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You are Momus's prediction-market analyst. You answer with Momus's own model numbers.

Pick the tool by the question:
- `football_quote` for a football (soccer) match: two teams, home team first
- `mlb_quote` for a baseball game: one or two MLB teams
- `midterms_odds` for the 2026 US midterms (Senate / House control)
- `tennis_read` for a tennis match, player or tournament

Report probabilities as percentages and fair odds as decimals. If a team or game is not covered, say so plainly —
never invent numbers. These are model probabilities, not betting advice."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "football_quote",
                    "description": "Momus's football model for one match: home/draw/away probabilities, fair decimal odds, over/under, both-teams-to-score and the most likely scorelines (self-fitted Dixon-Coles across the major leagues). Teams Momus doesn't rate return an error.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "home_team": {"type": "string", "description": "Home team, e.g. 'Real Madrid'"},
                            "away_team": {"type": "string", "description": "Away team, e.g. 'Barcelona'"},
                        },
                        "required": ["home_team", "away_team"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "mlb_quote",
                    "description": "Momus's MLB model for one game: win probabilities from a pitcher-aware Elo, the de-vigged market, the blend Momus bets on, fair odds and probable starters. One team is enough for its next game within 72 hours.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "home_team": {"type": "string", "description": "Home team, e.g. 'Milwaukee Brewers'"},
                            "away_team": {"type": "string", "description": "Away team, e.g. 'San Diego Padres'"},
                        },
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "midterms_odds",
                    "description": "Momus's US midterms 2026 model: Senate and House control probabilities and seat distributions from a correlated Monte Carlo, priced against live Polymarket and Kalshi contracts with Momus's edge per market.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tennis_read",
                    "description": "A tennis match priced on Meridian (Robinhood Chain): Momus's win probability, the on-chain price, the edge, his call (position / would-bet / pass) and a short written read. Empty query returns his latest read.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Player, match or tournament, e.g. 'Sinner' or 'Shanghai Masters'"},
                        },
                    },
                },
            },
        ]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def football_quote(self, home_team: str, away_team: str) -> Dict[str, Any]:
        result = await self._api_request(
            url=f"{MOMUS_BASE_URL}/football/quote-internal",
            method="POST",
            headers=self.headers,
            json_data={"homeTeam": home_team, "awayTeam": away_team},
        )
        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def mlb_quote(self, home_team: str = "", away_team: str = "") -> Dict[str, Any]:
        result = await self._api_request(
            url=f"{MOMUS_BASE_URL}/mlb/quote-internal",
            method="POST",
            headers=self.headers,
            json_data={"homeTeam": home_team, "awayTeam": away_team},
        )
        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}

    @with_cache(ttl_seconds=1800)
    @with_retry(max_retries=2)
    async def midterms_odds(self) -> Dict[str, Any]:
        result = await self._api_request(url=f"{MOMUS_BASE_URL}/midterms/quote-internal", method="GET", headers=self.headers)
        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def tennis_read(self, query: str = "") -> Dict[str, Any]:
        result = await self._api_request(
            url=f"{MOMUS_BASE_URL}/meridian/read-internal",
            method="GET",
            headers=self.headers,
            params={"q": query} if query else None,
        )
        if errors := self._handle_error(result):
            return errors
        return {"status": "success", "data": result}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        if tool_name == "football_quote":
            home, away = function_args.get("home_team"), function_args.get("away_team")
            if not home or not away:
                return {"error": "Both 'home_team' and 'away_team' are required"}
            return await self.football_quote(home, away)
        if tool_name == "mlb_quote":
            home, away = function_args.get("home_team", ""), function_args.get("away_team", "")
            if not home and not away:
                return {"error": "Give at least one MLB team"}
            return await self.mlb_quote(home, away)
        if tool_name == "midterms_odds":
            return await self.midterms_odds()
        if tool_name == "tennis_read":
            return await self.tennis_read(function_args.get("query", ""))
        return {"error": f"Unsupported tool: {tool_name}"}
