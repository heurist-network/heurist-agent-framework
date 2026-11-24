"""Auto-generated BRAINIAC Heurist Mesh agent for group `telecom-billing` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "telecom-billing__roaming-charge-audit",
      "description": "Audit roaming charges. Recalculate international roaming charges from caller-supplied usage, tariff rules, packages, country zones, and billed charges. A usage row is priced only when exactly one tariff matches. Missing or ambiguous tariffs are reported and never assumed. Daily-pass packages zero incremental usage. Positive actual-minus-expected deltas form estimated overbilling by currency. No FX conversion is applied. Docs: https://www.brainiac.software/api/telecom-billing/roaming-charge-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "usage": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "sms",
                    "data"
                  ]
                },
                "country": {
                  "type": "string",
                  "pattern": "^[A-Z]{2}$"
                },
                "started_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "ended_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "units": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "unit_kind": {
                  "type": "string",
                  "enum": [
                    "seconds",
                    "messages",
                    "bytes"
                  ]
                }
              },
              "required": [
                "id",
                "type",
                "country",
                "started_at",
                "units",
                "unit_kind"
              ],
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "sms",
                    "data",
                    "daily_pass"
                  ]
                },
                "country": {
                  "type": "string",
                  "pattern": "^[A-Z]{2}$"
                },
                "zone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "rate_per_unit": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "unit_kind": {
                  "type": "string",
                  "enum": [
                    "seconds",
                    "messages",
                    "bytes",
                    "day"
                  ]
                },
                "effective_from": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "effective_to": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "daily_cap": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "type",
                "currency",
                "rate_per_unit",
                "effective_from"
              ],
              "additionalProperties": false
            }
          },
          "packages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "sms",
                    "data",
                    "daily_pass"
                  ]
                },
                "country": {
                  "type": "string",
                  "pattern": "^[A-Z]{2}$"
                },
                "zone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "allowance_units": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "unit_kind": {
                  "type": "string",
                  "enum": [
                    "seconds",
                    "messages",
                    "bytes",
                    "day"
                  ]
                },
                "price": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "effective_from": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "effective_to": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "type",
                "currency",
                "price",
                "effective_from"
              ],
              "additionalProperties": false
            }
          },
          "zones": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "zone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "pattern": "^[A-Z]{2}$"
                }
              },
              "required": [
                "zone",
                "country"
              ],
              "additionalProperties": false
            }
          },
          "billed_charges": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "usage_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "package_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "sms",
                    "data",
                    "daily_pass",
                    "other"
                  ]
                },
                "country": {
                  "type": "string",
                  "pattern": "^[A-Z]{2}$"
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "billed_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                }
              },
              "required": [
                "id",
                "type",
                "currency",
                "amount",
                "billed_at"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "usage",
          "billed_charges"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "telecom-billing__roaming-charge-audit": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "telecom-billing__roaming-charge-audit": "telecom-billing/roaming-charge-audit"
}


class BrainiacTelecomBillingAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — telecom-billing",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the telecom-billing catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "telecom-billing", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit roaming charges"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the telecom-billing group. "
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
