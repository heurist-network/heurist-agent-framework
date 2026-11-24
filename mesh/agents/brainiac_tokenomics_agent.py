"""Auto-generated BRAINIAC Heurist Mesh agent for group `tokenomics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "tokenomics__token-vesting-schedule-audit",
      "description": "Audit token vesting schedule. Audit caller-supplied token vesting allocations against a declared supply. Checks totals, cliff and vesting dates, duplicate beneficiaries, overlapping schedules, and distribution records. audit_status is valid, warnings, invalid, or incomplete. Supported models are linear and custom. A linear schedule needs a start, cliffMode (included or before_vesting), a cliff duration or cliff date, a vesting duration, an unlock frequency, and an initial unlock percent or amount. initialUnlockPercent is a decimal string from 0 to 100 with at most 4 decimal places. Timestamps are UTC and must end in Z. No chain is queried, and wallet balances are not verified. Docs: https://www.brainiac.software/api/tokenomics/token-vesting-schedule-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "supply": {
            "type": "string"
          },
          "evaluationDates": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$"
            }
          },
          "allocations": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "beneficiary": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "string"
                },
                "model": {
                  "type": "string",
                  "enum": [
                    "linear",
                    "custom"
                  ]
                },
                "start": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$"
                },
                "cliffDurationSeconds": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 3153600000
                },
                "cliffDate": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$"
                },
                "cliffMode": {
                  "type": "string",
                  "enum": [
                    "included",
                    "before_vesting"
                  ]
                },
                "vestingDurationSeconds": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3153600000
                },
                "unlockFrequencySeconds": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3153600000
                },
                "initialUnlockPercent": {
                  "type": "string",
                  "pattern": "^(100(?:\\.0{1,4})?|(?:0|[1-9]\\d?)(?:\\.\\d{1,4})?)$"
                },
                "initialUnlockAmount": {
                  "type": "string"
                },
                "unlocks": {
                  "maxItems": 64,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "at": {
                        "type": "string",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$"
                      },
                      "amount": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "at",
                      "amount"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "beneficiary",
                "amount",
                "model"
              ],
              "additionalProperties": false
            }
          },
          "distributions": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "allocationId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "beneficiary": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "string"
                },
                "at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$"
                }
              },
              "required": [
                "allocationId",
                "amount",
                "at"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "supply",
          "allocations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "tokenomics__vesting-dilution",
      "description": "Score vesting dilution. Project a caller-supplied circulating supply and price across vesting cliffs. Each schedule unlocks one period at its cliff month, then monthly until it is fully unlocked. The FDV curve holds the price constant. The dilution score mixes the locked share with the largest single-month unlock. No price feed is queried. Docs: https://www.brainiac.software/api/tokenomics/vesting-dilution",
      "parameters": {
        "type": "object",
        "properties": {
          "circulating": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "price": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000000
          },
          "months": {
            "type": "integer",
            "minimum": 1,
            "maximum": 36
          },
          "schedules": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "cliff_months": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 120
                },
                "vesting_months": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 120
                }
              },
              "required": [
                "name",
                "amount",
                "cliff_months",
                "vesting_months"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "circulating",
          "price",
          "months",
          "schedules"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "tokenomics__token-vesting-schedule-audit": "0.05",
  "tokenomics__vesting-dilution": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "tokenomics__token-vesting-schedule-audit": "tokenomics/token-vesting-schedule-audit",
  "tokenomics__vesting-dilution": "tokenomics/vesting-dilution"
}


class BrainiacTokenomicsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — tokenomics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the tokenomics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "tokenomics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit token vesting schedule"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the tokenomics group. "
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
