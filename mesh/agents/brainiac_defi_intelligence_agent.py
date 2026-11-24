"""Auto-generated BRAINIAC Heurist Mesh agent for group `defi-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "defi-intelligence__protocols__search",
      "description": "Search DeFi protocols. Search DeFi protocols by name, symbol, description, category, or chain using the DeFiLlama public API. Filtering is performed client-side. Docs: https://www.brainiac.software/api/defi-intelligence/protocols-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "category": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "chain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "limit": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "defi-intelligence__protocols__profile",
      "description": "Get protocol information. Retrieve detailed information for a specific DeFi protocol by ID or slug from DeFiLlama public API. Docs: https://www.brainiac.software/api/defi-intelligence/protocols-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          }
        },
        "required": [
          "id"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "defi-intelligence__protocols__tvl__current",
      "description": "Get current protocol TVL. Retrieve current protocol TVL from DefiLlama, plus chainTvls and change7d when DefiLlama publishes them. Delayed reference TVL, not a live on-chain read. Docs: https://www.brainiac.software/api/defi-intelligence/protocols-tvl-current",
      "parameters": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          }
        },
        "required": [
          "id"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "defi-intelligence__pools__yields",
      "description": "Rank DefiLlama yield pools. Highest-yield DeFi pools from the public DefiLlama yields API, filterable by chain, project, symbol, stablecoin flag, and min TVL. Returns official APY fields only — no invented risk score. Docs: https://www.brainiac.software/api/defi-intelligence/pools-yields",
      "parameters": {
        "type": "object",
        "properties": {
          "chain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "project": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "symbol": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "stablecoin": {
            "type": "boolean"
          },
          "minTvlUsd": {
            "default": 100000,
            "type": "number",
            "minimum": 0
          },
          "sortBy": {
            "default": "apy",
            "type": "string",
            "enum": [
              "apy",
              "tvl"
            ]
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "defi-intelligence__chains__tvl",
      "description": "Get TVL by blockchain. Retrieve Total Value Locked (TVL) across blockchains from DeFiLlama public API v2. TVL is a delayed reference value. Docs: https://www.brainiac.software/api/defi-intelligence/chains-tvl",
      "parameters": {
        "type": "object",
        "properties": {
          "chain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "defi-intelligence__protocols__search": "0.008",
  "defi-intelligence__protocols__profile": "0.008",
  "defi-intelligence__protocols__tvl__current": "0.008",
  "defi-intelligence__pools__yields": "0.008",
  "defi-intelligence__chains__tvl": "0.008"
}
TOOL_ROUTES: Dict[str, str] = {
  "defi-intelligence__protocols__search": "defi-intelligence/protocols/search",
  "defi-intelligence__protocols__profile": "defi-intelligence/protocols/profile",
  "defi-intelligence__protocols__tvl__current": "defi-intelligence/protocols/tvl/current",
  "defi-intelligence__pools__yields": "defi-intelligence/pools/yields",
  "defi-intelligence__chains__tvl": "defi-intelligence/chains/tvl"
}


class BrainiacDefiIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — defi-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the defi-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "defi-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search DeFi protocols"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.008",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the defi-intelligence group. "
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
