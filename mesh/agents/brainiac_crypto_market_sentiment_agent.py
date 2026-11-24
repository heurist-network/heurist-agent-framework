"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-market-sentiment` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp

from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

TOOL_SCHEMAS: List[Dict[str, Any]] = [
  {
    "type": "function",
    "function": {
      "name": "crypto-market-sentiment__fear-greed",
      "description": "Crypto Fear and Greed index. Published crypto Fear and Greed index (0-100 and classification) from the public alternative.me API. Optional history days. Not trading advice. Docs: https://www.brainiac.software/api/crypto-market-sentiment/fear-greed",
      "parameters": {
        "type": "object",
        "properties": {
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 30
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-market-sentiment__global-snapshot",
      "description": "Crypto market global snapshot. Global crypto market snapshot from Coinlore: market cap, 24h volume, BTC/ETH dominance, market-cap change, and coin/market counts. Not a ticker price. Docs: https://www.brainiac.software/api/crypto-market-sentiment/global-snapshot",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-market-sentiment__fear-greed": "0.001",
  "crypto-market-sentiment__global-snapshot": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-market-sentiment__fear-greed": "crypto-market-sentiment/fear-greed",
  "crypto-market-sentiment__global-snapshot": "crypto-market-sentiment/global-snapshot"
}


class BrainiacCryptoMarketSentimentAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-market-sentiment",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-market-sentiment catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-market-sentiment", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Crypto Fear and Greed index"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-market-sentiment group. "
            "Prefer direct tool calls with JSON arguments matching each tool schema. "
            "If a tool returns status failed, report the failure and do not invent data."
        )

    def get_tool_schemas(self) -> List[Dict]:
        return TOOL_SCHEMAS

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 60

    async def _handle_tool_logic(
        self,
        tool_name: str,
        function_args: dict,
        session_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        route = TOOL_ROUTES.get(tool_name)
        if not route:
            return {"error": f"Unsupported tool: {tool_name}"}
        url = f"{self.base_url}/api/partner/v1/{route}"
        headers = {
            "content-type": "application/json",
            "x-partner-key": self.api_key,
            "x-brainiac-partner": "heurist",
        }
        if not self.api_key:
            return {"error": "HEURIST_PARTNER_KEY is not configured"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=function_args or {}, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    text = await response.text()
                    try:
                        data = await response.json(content_type=None)
                    except Exception:
                        data = {"raw": text[:2000]}
                    if response.status >= 400:
                        return {"error": f"HTTP {response.status}", "data": data}
                    if isinstance(data, dict) and data.get("status") == "failed":
                        return {"error": "operation failed", "data": data}
                    return {"data": data}
        except Exception as exc:
            logger.exception("brainiac partner call failed")
            return {"error": str(exc)}
