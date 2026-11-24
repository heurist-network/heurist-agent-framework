"""Auto-generated BRAINIAC Heurist Mesh agent for group `polymarket` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "polymarket__markets",
      "description": "Polymarket markets and odds. List Polymarket markets from the public Gamma API. query is filtered client-side on the returned page. Does not place orders. Docs: https://www.brainiac.software/api/polymarket/markets",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "slug": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "conditionId": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{64}$"
          },
          "closed": {
            "type": "boolean"
          },
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "offset": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "order": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "ascending": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "polymarket__events",
      "description": "Polymarket events. List Polymarket events and nested markets from the public Gamma Events API. query is filtered client-side on the returned page. Docs: https://www.brainiac.software/api/polymarket/events",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "slug": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "eventId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "closed": {
            "type": "boolean"
          },
          "active": {
            "type": "boolean"
          },
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "offset": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "polymarket__trades",
      "description": "Polymarket recent trades. Recent Polymarket trades from the public Data API v2 trade feed (not v1, not authenticated CLOB). Cursor pagination only. Docs: https://www.brainiac.software/api/polymarket/trades",
      "parameters": {
        "type": "object",
        "properties": {
          "conditionId": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{64}$"
          },
          "eventId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "user": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "polymarket__leaderboard",
      "description": "Polymarket leaderboard. Official Polymarket Data API v2 leaderboard of wallets by PnL and volume, with optional timeframe. Docs: https://www.brainiac.software/api/polymarket/leaderboard",
      "parameters": {
        "type": "object",
        "properties": {
          "timeframe": {
            "type": "string",
            "enum": [
              "day",
              "week",
              "month",
              "all"
            ]
          },
          "category": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "polymarket__price-history",
      "description": "Polymarket price history. Official Polymarket CLOB historical prices for a market token from the public prices-history API. Docs: https://www.brainiac.software/api/polymarket/price-history",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenId": {
            "type": "string",
            "minLength": 8,
            "maxLength": 120
          },
          "conditionId": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{64}$"
          },
          "outcome": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "interval": {
            "type": "string",
            "enum": [
              "1m",
              "1h",
              "6h",
              "1d",
              "1w",
              "max"
            ]
          },
          "fidelity": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "polymarket__order-book",
      "description": "Polymarket order book. Official Polymarket CLOB order book for a market token: bids and asks with price and size. Does not place orders. Docs: https://www.brainiac.software/api/polymarket/order-book",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenId": {
            "type": "string",
            "minLength": 8,
            "maxLength": 120
          },
          "conditionId": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{64}$"
          },
          "outcome": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "depth": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "polymarket__markets": "0.008",
  "polymarket__events": "0.008",
  "polymarket__trades": "0.008",
  "polymarket__leaderboard": "0.0085",
  "polymarket__price-history": "0.0085",
  "polymarket__order-book": "0.0085"
}
TOOL_ROUTES: Dict[str, str] = {
  "polymarket__markets": "polymarket/markets",
  "polymarket__events": "polymarket/events",
  "polymarket__trades": "polymarket/trades",
  "polymarket__leaderboard": "polymarket/leaderboard",
  "polymarket__price-history": "polymarket/price-history",
  "polymarket__order-book": "polymarket/order-book"
}


class BrainiacPolymarketAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — polymarket",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the polymarket catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "polymarket", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Polymarket markets and odds"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.008",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the polymarket group. "
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
