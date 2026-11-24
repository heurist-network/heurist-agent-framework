"""Auto-generated BRAINIAC Heurist Mesh agent for group `trade-tariff` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "trade-tariff__container-iso6346-validate",
      "description": "Validate ISO 6346 container number. Validate freight container owner code, category identifier, serial, and ISO 6346 check digit. Does not confirm registration. Docs: https://www.brainiac.software/api/trade-tariff/container-iso6346-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "containerNumber": {
            "type": "string",
            "minLength": 10,
            "maxLength": 15
          }
        },
        "required": [
          "containerNumber"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-tariff__customs-bond-type-explain",
      "description": "Explain a US customs bond type. Return a short structured explanation of common CBP customs bond forms and activity codes from public CBP bond concepts. Docs: https://www.brainiac.software/api/trade-tariff/customs-bond-type-explain",
      "parameters": {
        "type": "object",
        "properties": {
          "bondType": {
            "default": "unknown",
            "type": "string",
            "enum": [
              "continuous",
              "single_transaction",
              "activity_1",
              "activity_2",
              "activity_3",
              "activity_4",
              "unknown"
            ]
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-tariff__us-hts-duty-rate-lookup",
      "description": "Look up US HTS duty rates. Return the published HTSUS General, Special and Column 2 rate columns, units and Chapter 99 cross-references for an HTS code from the vendored USITC release. Not a classification or additional-duty calculation. Docs: https://www.brainiac.software/api/trade-tariff/us-hts-duty-rate-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "hts": {
            "type": "string",
            "pattern": "^\\d{4}(\\.?\\d{2}){0,3}$"
          },
          "program": {
            "type": "string",
            "pattern": "^[A-Z]{1,2}\\*?\\+?$"
          }
        },
        "required": [
          "hts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-tariff__uk-global-tariff-lookup",
      "description": "Look up UK Global Tariff duty. Return the UK Global Tariff third-country (measure type 103) duty for a UK commodity code from a vendored DBT dataset subset. Preferential rates are not included. Docs: https://www.brainiac.software/api/trade-tariff/uk-global-tariff-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "commodityCode": {
            "type": "string",
            "pattern": "^(\\d{8}|\\d{10})$"
          },
          "date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          }
        },
        "required": [
          "commodityCode"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-tariff__us-schedule-b-lookup",
      "description": "Look up a US Schedule B export code. Look up a 10-digit US Schedule B export code or search Schedule B descriptions in the vendored Census concordance. Not an AES filing. Docs: https://www.brainiac.software/api/trade-tariff/us-schedule-b-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "code": {
            "type": "string",
            "pattern": "^\\d{10}$"
          },
          "query": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
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
      "name": "trade-tariff__us-airport-lookup",
      "description": "Look up a US airport or landing facility. Look up a US landing facility by FAA location identifier, ICAO id or name from the vendored FAA NASR 28-day APT_BASE data. Docs: https://www.brainiac.software/api/trade-tariff/us-airport-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "faaId": {
            "type": "string",
            "pattern": "^[A-Z0-9]{2,4}$"
          },
          "icao": {
            "type": "string",
            "pattern": "^[A-Z]{4}$"
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "trade-tariff__container-iso6346-validate": "0.01",
  "trade-tariff__customs-bond-type-explain": "0.02",
  "trade-tariff__us-hts-duty-rate-lookup": "0.02",
  "trade-tariff__uk-global-tariff-lookup": "0.02",
  "trade-tariff__us-schedule-b-lookup": "0.02",
  "trade-tariff__us-airport-lookup": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "trade-tariff__container-iso6346-validate": "trade-tariff/container-iso6346-validate",
  "trade-tariff__customs-bond-type-explain": "trade-tariff/customs-bond-type-explain",
  "trade-tariff__us-hts-duty-rate-lookup": "trade-tariff/us-hts-duty-rate-lookup",
  "trade-tariff__uk-global-tariff-lookup": "trade-tariff/uk-global-tariff-lookup",
  "trade-tariff__us-schedule-b-lookup": "trade-tariff/us-schedule-b-lookup",
  "trade-tariff__us-airport-lookup": "trade-tariff/us-airport-lookup"
}


class BrainiacTradeTariffAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — trade-tariff",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the trade-tariff catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "trade-tariff", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate ISO 6346 container number"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the trade-tariff group. "
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
