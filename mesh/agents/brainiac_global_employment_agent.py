"""Auto-generated BRAINIAC Heurist Mesh agent for group `global-employment` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "global-employment__uk-statutory-notice-period",
      "description": "Calculate UK statutory notice period. Calculate the minimum statutory employer notice period in Great Britain from continuous employment dates, and compare it with caller-supplied contractual notice. Docs: https://www.brainiac.software/api/global-employment/uk-statutory-notice-period",
      "parameters": {
        "type": "object",
        "properties": {
          "startDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "noticeDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "contractualNoticeWeeks": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 260
          }
        },
        "required": [
          "startDate",
          "noticeDate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "global-employment__uk-statutory-redundancy-pay",
      "description": "Calculate UK statutory redundancy pay. Calculate Great Britain statutory redundancy pay from age, service, redundancy date, and weekly pay using the 2026 cap and 20-year service limit. Docs: https://www.brainiac.software/api/global-employment/uk-statutory-redundancy-pay",
      "parameters": {
        "type": "object",
        "properties": {
          "dateOfBirth": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "startDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "redundancyDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "weeklyPayPence": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100000000
          }
        },
        "required": [
          "dateOfBirth",
          "startDate",
          "redundancyDate",
          "weeklyPayPence"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "global-employment__uk-working-time-check",
      "description": "Check UK working-time limits. Check caller-supplied shifts against UK 48-hour average, under-18 limits, 20-minute breaks, daily rest, and weekly or fortnightly rest rules. Docs: https://www.brainiac.software/api/global-employment/uk-working-time-check",
      "parameters": {
        "type": "object",
        "properties": {
          "shifts": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "start": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}(?::\\d{2})?$"
                },
                "end": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}(?::\\d{2})?$"
                },
                "breakMinutes": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                }
              },
              "required": [
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          },
          "referenceWeeks": {
            "default": 17,
            "type": "integer",
            "minimum": 1,
            "maximum": 52
          },
          "optedOut": {
            "default": false,
            "type": "boolean"
          },
          "under18": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "shifts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "global-employment__us-overtime-calculate",
      "description": "Calculate US overtime pay. Calculate federal FLSA weekly overtime, or California daily, seventh-day, and weekly overtime, from one caller-supplied workweek. Docs: https://www.brainiac.software/api/global-employment/us-overtime-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "jurisdiction": {
            "type": "string",
            "enum": [
              "federal",
              "california"
            ]
          },
          "hourlyRateCents": {
            "type": "integer",
            "minimum": 0,
            "maximum": 1000000
          },
          "days": {
            "minItems": 1,
            "maxItems": 7,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 24
                }
              },
              "required": [
                "date",
                "hours"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "jurisdiction",
          "hourlyRateCents",
          "days"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "global-employment__gender-pay-gap-calc",
      "description": "Calculate UK gender pay gap figures. Compute UK gender pay gap mean, median, bonus, bonus proportion, quartile, headcount, and reporting-threshold figures from caller-supplied employee-level data. Docs: https://www.brainiac.software/api/global-employment/gender-pay-gap-calc",
      "parameters": {
        "type": "object",
        "properties": {
          "snapshotDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "employees": {
            "minItems": 1,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sex": {
                  "type": "string",
                  "enum": [
                    "male",
                    "female"
                  ]
                },
                "fullPayRelevant": {
                  "type": "boolean"
                },
                "hourlyPayPence": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "bonusPence": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "sex",
                "fullPayRelevant",
                "hourlyPayPence"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "snapshotDate",
          "employees"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "global-employment__uk-statutory-notice-period": "0.03",
  "global-employment__uk-statutory-redundancy-pay": "0.04",
  "global-employment__uk-working-time-check": "0.04",
  "global-employment__us-overtime-calculate": "0.04",
  "global-employment__gender-pay-gap-calc": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "global-employment__uk-statutory-notice-period": "global-employment/uk-statutory-notice-period",
  "global-employment__uk-statutory-redundancy-pay": "global-employment/uk-statutory-redundancy-pay",
  "global-employment__uk-working-time-check": "global-employment/uk-working-time-check",
  "global-employment__us-overtime-calculate": "global-employment/us-overtime-calculate",
  "global-employment__gender-pay-gap-calc": "global-employment/gender-pay-gap-calc"
}


class BrainiacGlobalEmploymentAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — global-employment",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the global-employment catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "global-employment", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Calculate UK statutory notice period"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the global-employment group. "
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
