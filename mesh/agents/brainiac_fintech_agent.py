"""Auto-generated BRAINIAC Heurist Mesh agent for group `fintech` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "fintech__schedule-risk-audit",
      "description": "Audit financial schedule stress. Stress-test a caller-supplied loan schedule, cashflow stream, and payout list. Inflows move 7, 14, and 30 days later, outflows stay on their dates, and financing cost uses the supplied annual rate. The math stays in memory. This is not a credit decision. Docs: https://www.brainiac.software/api/fintech/schedule-risk-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "opening_balance": {
            "type": "number",
            "minimum": -1000000000000,
            "maximum": 1000000000000
          },
          "minimum_balance": {
            "type": "number",
            "minimum": -1000000000000,
            "maximum": 1000000000000
          },
          "annual_rate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "payments": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "label": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "cashflows": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "label": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "milestones": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "label": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fintech__repayment-waterfall-simulate",
      "description": "Simulate repayment waterfall. Allocate available cash across caller-supplied debt facilities by contractual priority and bucket order (fees, arrears, interest, principal). Returns step-by-step intermediate calculations. No bank account is accessed. Docs: https://www.brainiac.software/api/fintech/repayment-waterfall-simulate",
      "parameters": {
        "type": "object",
        "properties": {
          "available_cash": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "facilities": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "priority": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 10000
                },
                "principal": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "accrued_interest": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "fees": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "arrears": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "interest_rate_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "payment_order": {
                  "minItems": 1,
                  "maxItems": 4,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "fees",
                      "arrears",
                      "interest",
                      "principal"
                    ]
                  }
                }
              },
              "required": [
                "id",
                "currency",
                "priority",
                "principal"
              ],
              "additionalProperties": false
            }
          },
          "default_payment_order": {
            "minItems": 1,
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "fees",
                "arrears",
                "interest",
                "principal"
              ]
            }
          }
        },
        "required": [
          "available_cash",
          "currency",
          "facilities"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fintech__covenant-headroom-calculate",
      "description": "Calculate covenant headroom. Compute headroom for caller-supplied financial covenants against metric values and thresholds. Returns the exact threshold, headroom formula, and breach status. No credit bureau is contacted. Docs: https://www.brainiac.software/api/fintech/covenant-headroom-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "metrics": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "value": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "covenants": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "metric_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "enum": [
                    "gte",
                    "lte",
                    "gt",
                    "lt"
                  ]
                },
                "threshold": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "metric_id",
                "operator",
                "threshold"
              ],
              "additionalProperties": false
            }
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          }
        },
        "required": [
          "metrics",
          "covenants"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fintech__receivables-dilution-analyze",
      "description": "Analyze receivables dilution. Quantify how credit notes, disputes, returns, rebates, and write-offs reduce face value in a caller-supplied receivables portfolio. Dilution is capped at face value per receivable and reported by currency without FX conversion. Docs: https://www.brainiac.software/api/fintech/receivables-dilution-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "receivables": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "face_value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                }
              },
              "required": [
                "id",
                "face_value",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "dilutions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "receivable_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "credit_note",
                    "dispute",
                    "return",
                    "rebate",
                    "write_off",
                    "other"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                }
              },
              "required": [
                "id",
                "receivable_id",
                "kind",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "receivables",
          "dilutions"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "fintech__schedule-risk-audit": "0.04",
  "fintech__repayment-waterfall-simulate": "0.04",
  "fintech__covenant-headroom-calculate": "0.04",
  "fintech__receivables-dilution-analyze": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "fintech__schedule-risk-audit": "fintech/schedule-risk-audit",
  "fintech__repayment-waterfall-simulate": "fintech/repayment-waterfall-simulate",
  "fintech__covenant-headroom-calculate": "fintech/covenant-headroom-calculate",
  "fintech__receivables-dilution-analyze": "fintech/receivables-dilution-analyze"
}


class BrainiacFintechAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — fintech",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the fintech catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "fintech", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit financial schedule stress"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the fintech group. "
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
