"""Auto-generated BRAINIAC Heurist Mesh agent for group `license` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "license__requirements",
      "description": "Read verified licence renewal requirements. Return source-linked rules only for supported Texas electrician and UK SIA licence types; unsupported jurisdictions remain explicitly unsupported. Docs: https://www.brainiac.software/api/license/requirements",
      "parameters": {
        "type": "object",
        "properties": {
          "jurisdiction": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "licenseType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          }
        },
        "required": [
          "jurisdiction",
          "licenseType"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "license__renewal-plan",
      "description": "Build a sourced renewal plan. Calculate a renewal checklist and PDF from verified rules and caller-supplied expiry/CE data. Unsupported combinations remain unsupported. Docs: https://www.brainiac.software/api/license/renewal-plan",
      "parameters": {
        "type": "object",
        "properties": {
          "jurisdiction": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "licenseType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "expiresOn": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "completedCeHours": {
            "default": 0,
            "type": "number",
            "minimum": 0
          }
        },
        "required": [
          "jurisdiction",
          "licenseType"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "license__deadline-watch",
      "description": "Calculate licence reminder dates. Return reminder dates from a caller-supplied expiry date. This is data only; BRAINIAC.software does not send notifications. Docs: https://www.brainiac.software/api/license/deadline-watch",
      "parameters": {
        "type": "object",
        "properties": {
          "expiresOn": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "remindDays": {
            "default": [
              90,
              30,
              7
            ],
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 730
            }
          }
        },
        "required": [
          "expiresOn"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "license__requirements": "0.01",
  "license__renewal-plan": "0.05",
  "license__deadline-watch": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "license__requirements": "license/requirements",
  "license__renewal-plan": "license/renewal-plan",
  "license__deadline-watch": "license/deadline-watch"
}


class BrainiacLicenseAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — license",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the license catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "license", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Read verified licence renewal requirements"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the license group. "
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
