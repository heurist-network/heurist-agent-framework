"""Auto-generated BRAINIAC Heurist Mesh agent for group `property-official` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "property-official__uk-hpi-lookup",
      "description": "Look up UK House Price Index figures. Return official UK HPI average price, index and change figures for a geography and month from the vendored HM Land Registry full file. Docs: https://www.brainiac.software/api/property-official/uk-hpi-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "area": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "month": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}$"
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}$"
          },
          "to": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}$"
          }
        },
        "required": [
          "area"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-official__epa-radon-zone-lookup",
      "description": "Look up EPA radon zone by US county. Return the EPA Map of Radon Zones zone (1–3) for a US county from the vendored EPA spreadsheet. Docs: https://www.brainiac.software/api/property-official/epa-radon-zone-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "state": {
            "type": "string",
            "minLength": 2,
            "maxLength": 40
          },
          "county": {
            "type": "string",
            "minLength": 2,
            "maxLength": 80
          }
        },
        "required": [
          "state",
          "county"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-official__hud-fmr-lookup",
      "description": "Look up HUD Fair Market Rents (FY2027). Return HUD FY2027 Fair Market Rents for a county/town FIPS or HUD area, or Small Area FMRs for a ZIP, from vendored HUD files. Docs: https://www.brainiac.software/api/property-official/hud-fmr-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "fips": {
            "type": "string",
            "pattern": "^\\d{5}(\\d{5})?$"
          },
          "hudAreaCode": {
            "type": "string",
            "minLength": 3,
            "maxLength": 40
          },
          "zip": {
            "type": "string",
            "pattern": "^\\d{5}$"
          },
          "bedrooms": {
            "anyOf": [
              {
                "type": "number",
                "const": 0
              },
              {
                "type": "number",
                "const": 1
              },
              {
                "type": "number",
                "const": 2
              },
              {
                "type": "number",
                "const": 3
              },
              {
                "type": "number",
                "const": 4
              }
            ]
          },
          "year": {
            "default": 2027,
            "type": "number",
            "const": 2027
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-official__ofgem-price-cap-lookup",
      "description": "Look up the Ofgem default tariff cap. Return the Ofgem GB domestic energy price cap for a region, fuel, meter and payment method for the vendored charge restriction period. Docs: https://www.brainiac.software/api/property-official/ofgem-price-cap-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "region": {
            "type": "string",
            "minLength": 2,
            "maxLength": 80
          },
          "fuel": {
            "type": "string",
            "enum": [
              "electricity",
              "gas"
            ]
          },
          "meter": {
            "type": "string",
            "enum": [
              "single-rate",
              "multi-register"
            ]
          },
          "paymentMethod": {
            "default": "direct-debit",
            "type": "string",
            "enum": [
              "direct-debit",
              "standard-credit",
              "prepayment"
            ]
          },
          "date": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "annualKwh": {
            "type": "number",
            "minimum": 0,
            "maximum": 100000
          }
        },
        "required": [
          "region",
          "fuel"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "property-official__uk-hpi-lookup": "0.03",
  "property-official__epa-radon-zone-lookup": "0.02",
  "property-official__hud-fmr-lookup": "0.03",
  "property-official__ofgem-price-cap-lookup": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "property-official__uk-hpi-lookup": "property-official/uk-hpi-lookup",
  "property-official__epa-radon-zone-lookup": "property-official/epa-radon-zone-lookup",
  "property-official__hud-fmr-lookup": "property-official/hud-fmr-lookup",
  "property-official__ofgem-price-cap-lookup": "property-official/ofgem-price-cap-lookup"
}


class BrainiacPropertyOfficialAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — property-official",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the property-official catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "property-official", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Look up UK House Price Index figures"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the property-official group. "
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
