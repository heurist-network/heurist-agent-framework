"""Auto-generated BRAINIAC Heurist Mesh agent for group `staking-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "staking-operations__staking-reward-allocation-audit",
      "description": "Audit staking reward allocation. Calculate staking reward allocations from the supplied commission percent, share percents, penalties, and rounding rule. Share percents must sum to 100%. Commission is that percent of gross rewards or of rewards after penalties. audit_status is balanced, mismatched, invalid, or incomplete. Expected amounts are calculated. Actual amounts come only from distribution records in the request. No staking reward is fetched, and this is not an invoice or stablecoin reconciliation. Docs: https://www.brainiac.software/api/staking-operations/staking-reward-allocation-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "periods": {
            "minItems": 1,
            "maxItems": 24,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "validator": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "totalRewards": {
                  "type": "string",
                  "pattern": "^(0|[1-9][0-9]{0,77})$"
                },
                "start": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "end": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "deductions": {
                  "maxItems": 16,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "amount": {
                        "type": "string",
                        "pattern": "^(0|[1-9][0-9]{0,77})$"
                      },
                      "beneficiary": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      }
                    },
                    "required": [
                      "id",
                      "amount"
                    ],
                    "additionalProperties": false
                  }
                },
                "commission": {
                  "type": "object",
                  "properties": {
                    "beneficiary": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "percent": {
                      "type": "string",
                      "pattern": "^(100(?:\\.0{1,4})?|(?:0|[1-9]\\d?)(?:\\.\\d{1,4})?)$"
                    },
                    "basis": {
                      "type": "string",
                      "enum": [
                        "gross",
                        "net_after_deductions"
                      ]
                    }
                  },
                  "required": [
                    "beneficiary",
                    "percent",
                    "basis"
                  ],
                  "additionalProperties": false
                },
                "statedCommission": {
                  "type": "string",
                  "pattern": "^(0|[1-9][0-9]{0,77})$"
                },
                "shares": {
                  "maxItems": 64,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "beneficiary": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "role": {
                        "type": "string",
                        "enum": [
                          "operator",
                          "validator",
                          "delegator",
                          "other"
                        ]
                      },
                      "percent": {
                        "type": "string",
                        "pattern": "^(100(?:\\.0{1,4})?|(?:0|[1-9]\\d?)(?:\\.\\d{1,4})?)$"
                      }
                    },
                    "required": [
                      "beneficiary",
                      "role",
                      "percent"
                    ],
                    "additionalProperties": false
                  }
                },
                "rounding": {
                  "type": "string",
                  "enum": [
                    "floor",
                    "ceil",
                    "half_up"
                  ]
                },
                "remainder": {
                  "type": "string",
                  "enum": [
                    "operator",
                    "undistributed",
                    "largest_share"
                  ]
                }
              },
              "required": [
                "id",
                "validator",
                "totalRewards",
                "commission",
                "shares",
                "rounding",
                "remainder"
              ],
              "additionalProperties": false
            }
          },
          "distributions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "periodId": {
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
                  "type": "string",
                  "pattern": "^(0|[1-9][0-9]{0,77})$"
                },
                "at": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                }
              },
              "required": [
                "periodId",
                "beneficiary",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "periods"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "staking-operations__reward-fairness",
      "description": "Score staking reward fairness. Compare each supplied allocation with the share of the reward pool its weight implies. The rounding error is the total absolute gap, divided by the reward. Equal weights with uneven payouts lower the fairness score. No reward balance is fetched. Docs: https://www.brainiac.software/api/staking-operations/reward-fairness",
      "parameters": {
        "type": "object",
        "properties": {
          "reward": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "shares": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "weight": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "allocated": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "weight",
                "allocated"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "reward",
          "shares"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "staking-operations__staking-reward-allocation-audit": "0.05",
  "staking-operations__reward-fairness": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "staking-operations__staking-reward-allocation-audit": "staking-operations/staking-reward-allocation-audit",
  "staking-operations__reward-fairness": "staking-operations/reward-fairness"
}


class BrainiacStakingOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — staking-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the staking-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "staking-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit staking reward allocation"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the staking-operations group. "
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
