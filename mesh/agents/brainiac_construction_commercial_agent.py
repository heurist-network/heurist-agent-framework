"""Auto-generated BRAINIAC Heurist Mesh agent for group `construction-commercial` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "construction-commercial__contractor-payment-application-audit",
      "description": "Audit contractor payment applications. Independently check a contractor payment application against the schedule of values, measured work, approved variations, previous certificates, retention rules, and deductions. Unsupported claims, duplicated work, unapproved variations, retention errors, and certificate mismatches are adjusted with calculation evidence. The recommended payable amount is for review only. Docs: https://www.brainiac.software/api/construction-commercial/contractor-payment-application-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "contract": {
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
              "retention_bps": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10000
              },
              "retention_release_bps": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10000
              }
            },
            "required": [
              "id",
              "currency",
              "retention_bps"
            ],
            "additionalProperties": false
          },
          "schedule_of_values": {
            "minItems": 1,
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
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                },
                "contracted_amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "contracted_amount"
              ],
              "additionalProperties": false
            }
          },
          "payment_application": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "application_number": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10000
              },
              "submitted_on": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
              },
              "lines": {
                "minItems": 1,
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
                    "sov_item_id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "claimed_amount": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "variation_id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "previously_certified_amount": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    }
                  },
                  "required": [
                    "id",
                    "sov_item_id",
                    "claimed_amount"
                  ],
                  "additionalProperties": false
                }
              },
              "claimed_retention_release": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            },
            "required": [
              "id",
              "application_number",
              "submitted_on",
              "lines"
            ],
            "additionalProperties": false
          },
          "previous_certificates": {
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
                "certificate_number": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 10000
                },
                "certified_on": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "lines": {
                  "minItems": 1,
                  "maxItems": 2000,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "sov_item_id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "certified_amount": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9007199254740991
                      },
                      "variation_id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      }
                    },
                    "required": [
                      "sov_item_id",
                      "certified_amount"
                    ],
                    "additionalProperties": false
                  }
                },
                "retention_held": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "deductions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "certificate_number",
                "certified_on",
                "lines"
              ],
              "additionalProperties": false
            }
          },
          "measured_work": {
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
                "sov_item_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "measured_amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "measured_on": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "sov_item_id",
                "measured_amount"
              ],
              "additionalProperties": false
            }
          },
          "variations": {
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
                "sov_item_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "approved_amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "approved": {
                  "type": "boolean"
                },
                "approved_on": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                }
              },
              "required": [
                "id",
                "approved_amount",
                "approved"
              ],
              "additionalProperties": false
            }
          },
          "deductions": {
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
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "reason": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                }
              },
              "required": [
                "id",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "contract",
          "schedule_of_values",
          "payment_application"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "construction-commercial__contractor-payment-application-audit": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "construction-commercial__contractor-payment-application-audit": "construction-commercial/contractor-payment-application-audit"
}


class BrainiacConstructionCommercialAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — construction-commercial",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the construction-commercial catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "construction-commercial", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit contractor payment applications"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the construction-commercial group. "
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
