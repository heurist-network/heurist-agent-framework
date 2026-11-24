"""Auto-generated BRAINIAC Heurist Mesh agent for group `registries` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "registries__fdic-bank-lookup",
      "description": "Look up an FDIC-insured bank. Find a US FDIC-insured or formerly insured institution by certificate number, RSSD id, or name in the vendored FDIC BankFind institutions file. Returns status, charter class, and end date; ambiguous names return candidates. Docs: https://www.brainiac.software/api/registries/fdic-bank-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "cert": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "rssd": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "state": {
            "type": "string",
            "pattern": "^[A-Z]{2}$"
          },
          "activeOnly": {
            "default": false,
            "type": "boolean"
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "registries__ncua-credit-union-lookup",
      "description": "Look up an NCUA credit union. Find a US credit union by NCUA charter number, RSSD id, name, or trade name from the vendored NCUA 5300 Call Report FOICU and TradeNames files. Only credit unions that filed in that cycle are listed. Docs: https://www.brainiac.software/api/registries/ncua-credit-union-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "charter": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "rssd": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "state": {
            "type": "string",
            "pattern": "^[A-Z]{2}$"
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "registries__uk-charity-lookup",
      "description": "Look up a charity in England and Wales. Find a charity on the Charity Commission register for England and Wales by registered number or name from a vendored charity-level subset of the register extract. Removed charities are reported, not missed. Docs: https://www.brainiac.software/api/registries/uk-charity-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "charityNumber": {
            "type": "integer",
            "minimum": 200000,
            "maximum": 9999999
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "includeLinked": {
            "default": false,
            "type": "boolean"
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "registries__fdic-bank-lookup": "0.03",
  "registries__ncua-credit-union-lookup": "0.03",
  "registries__uk-charity-lookup": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "registries__fdic-bank-lookup": "registries/fdic-bank-lookup",
  "registries__ncua-credit-union-lookup": "registries/ncua-credit-union-lookup",
  "registries__uk-charity-lookup": "registries/uk-charity-lookup"
}


class BrainiacRegistriesAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — registries",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the registries catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "registries", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Look up an FDIC-insured bank"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the registries group. "
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
