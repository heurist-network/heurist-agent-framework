"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-prices` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-prices__spot",
      "description": "Crypto spot price. Return a USD spot price for a crypto ticker by comparing Chainlink Data Feeds on Base and the Coinbase Exchange public ticker. agree is pass only when both sources return a usable quote within 1%. 24h change comes from Coinbase stats only. Not a Base token-address DEX price. Docs: https://www.brainiac.software/api/crypto-prices/spot",
      "parameters": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string",
            "minLength": 1,
            "maxLength": 24
          },
          "quote": {
            "type": "string",
            "minLength": 2,
            "maxLength": 12
          }
        },
        "required": [
          "symbol"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-prices__history",
      "description": "Crypto price history. Historical USD prices for a crypto ticker such as BTC, ETH, or SOL from Chainlink Data Feeds on Base. Returns official aggregator rounds plus first, last, high, low and change over a window of up to 365 days. On-chain series, not exchange candles or volume. Docs: https://www.brainiac.software/api/crypto-prices/history",
      "parameters": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string",
            "minLength": 1,
            "maxLength": 24
          },
          "quote": {
            "type": "string",
            "minLength": 2,
            "maxLength": 12
          },
          "days": {
            "default": 30,
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": [
          "symbol"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-prices__spot": "0.001",
  "crypto-prices__history": "0.002"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-prices__spot": "crypto-prices/spot",
  "crypto-prices__history": "crypto-prices/history"
}


class BrainiacCryptoPricesAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-prices",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-prices catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-prices", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Crypto spot price"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-prices group. "
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
