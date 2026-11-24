"""Auto-generated BRAINIAC Heurist Mesh agent for group `aml-monitoring` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "aml-monitoring__ctr-aggregate",
      "description": "CTR cash aggregation. Aggregate cash-in and cash-out per person per US business day and list totals that trigger a Currency Transaction Report. Docs: https://www.brainiac.software/api/aml-monitoring/ctr-aggregate",
      "parameters": {
        "type": "object",
        "properties": {
          "transactions": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "personIds": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "default": "USD",
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "postedDate": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "receivedAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 64
                }
              },
              "required": [
                "id",
                "personIds",
                "direction",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "businessDays": {
            "default": {
              "calendar": "US_FED"
            },
            "type": "object",
            "properties": {
              "calendar": {
                "default": "US_FED",
                "type": "string",
                "enum": [
                  "US_FED"
                ]
              }
            },
            "additionalProperties": false
          },
          "regime": {
            "default": "US_CTR",
            "type": "string",
            "enum": [
              "US_CTR",
              "custom"
            ]
          },
          "threshold": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "nearRatio": {
            "default": 0.8,
            "type": "number",
            "minimum": 0.1,
            "maximum": 1
          }
        },
        "required": [
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aml-monitoring__structuring-detect",
      "description": "Cash structuring heuristic. Flag repeated just-below-threshold cash deposits as a structuring heuristic for analyst review. Docs: https://www.brainiac.software/api/aml-monitoring/structuring-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "transactions": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "personIds": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "default": "USD",
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "postedDate": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "receivedAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 64
                }
              },
              "required": [
                "id",
                "personIds",
                "direction",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "params": {
            "default": {
              "windowDays": 7,
              "lowerRatio": 0.8,
              "minCount": 3,
              "minTotalRatio": 1
            },
            "type": "object",
            "properties": {
              "windowDays": {
                "default": 7,
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              },
              "lowerRatio": {
                "default": 0.8,
                "type": "number",
                "minimum": 0.5,
                "maximum": 0.99
              },
              "minCount": {
                "default": 3,
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "minTotalRatio": {
                "default": 1,
                "type": "number",
                "minimum": 0.1,
                "maximum": 10
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aml-monitoring__rapid-movement-detect",
      "description": "Rapid pass-through detection. Detect credits quickly followed by similar-sized debits as a money-mule pass-through indicator on caller data. Docs: https://www.brainiac.software/api/aml-monitoring/rapid-movement-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "accountId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "transactions": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 64
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "counterparty": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "required": [
                "id",
                "direction",
                "amount",
                "at"
              ],
              "additionalProperties": false
            }
          },
          "params": {
            "default": {
              "maxHours": 48,
              "minOutRatio": 0.9,
              "minAmount": 100000
            },
            "type": "object",
            "properties": {
              "maxHours": {
                "default": 48,
                "type": "number",
                "minimum": 1,
                "maximum": 720
              },
              "minOutRatio": {
                "default": 0.9,
                "type": "number",
                "minimum": 0.5,
                "maximum": 1
              },
              "minAmount": {
                "default": 100000,
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "accountId",
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aml-monitoring__sar-deadline",
      "description": "SAR / DAML deadline calendar. Compute US bank SAR filing deadlines or UK POCA s.335 notice and moratorium periods from vendored holiday calendars. Docs: https://www.brainiac.software/api/aml-monitoring/sar-deadline",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "aml-monitoring__ctr-aggregate": "0.03",
  "aml-monitoring__structuring-detect": "0.03",
  "aml-monitoring__rapid-movement-detect": "0.03",
  "aml-monitoring__sar-deadline": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "aml-monitoring__ctr-aggregate": "aml-monitoring/ctr-aggregate",
  "aml-monitoring__structuring-detect": "aml-monitoring/structuring-detect",
  "aml-monitoring__rapid-movement-detect": "aml-monitoring/rapid-movement-detect",
  "aml-monitoring__sar-deadline": "aml-monitoring/sar-deadline"
}


class BrainiacAmlMonitoringAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — aml-monitoring",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the aml-monitoring catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "aml-monitoring", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["CTR cash aggregation"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the aml-monitoring group. "
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
