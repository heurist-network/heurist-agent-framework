"""Auto-generated BRAINIAC Heurist Mesh agent for group `coi` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "coi__analyze",
      "description": "Extract and check a certificate of insurance. Extract PDF/image fields with confidence, then compare them with contract requirements. Uncertain OCR is WARN and is never treated as verified. Docs: https://www.brainiac.software/api/coi/analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "fileBase64": {
            "type": "string",
            "minLength": 1,
            "maxLength": 16777216
          },
          "mediaType": {
            "type": "string",
            "enum": [
              "application/pdf",
              "image/png",
              "image/jpeg"
            ]
          },
          "requirements": {
            "type": "object",
            "properties": {
              "namedInsured": {
                "type": "string"
              },
              "effectiveOn": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "expiresAfter": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "generalLiability": {
                "type": "object",
                "properties": {
                  "eachOccurrence": {
                    "type": "number",
                    "minimum": 0
                  },
                  "aggregate": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "additionalProperties": false
              },
              "workersCompensation": {
                "type": "object",
                "properties": {
                  "statutory": {
                    "type": "boolean"
                  },
                  "employerLiability": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "additionalProperties": false
              },
              "automobileLiability": {
                "type": "object",
                "properties": {
                  "combinedSingleLimit": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "additionalProperties": false
              },
              "umbrellaLiability": {
                "type": "object",
                "properties": {
                  "eachOccurrence": {
                    "type": "number",
                    "minimum": 0
                  },
                  "aggregate": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "additionalProperties": false
              },
              "additionalInsured": {
                "type": "boolean"
              },
              "waiverOfSubrogation": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "vendorName": {
            "type": "string",
            "maxLength": 200
          },
          "projectName": {
            "type": "string",
            "maxLength": 200
          }
        },
        "required": [
          "fileBase64",
          "mediaType",
          "requirements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "coi__coverage-grade",
      "description": "Grade certificate coverage gaps. Compare a caller-supplied certificate of insurance, as text or JSON, with the minimum limits, endorsements, and expiry date in the request. The grade is the share of each minimum that is missing. The text is not a PDF and the result is not a coverage opinion. Docs: https://www.brainiac.software/api/coi/coverage-grade",
      "parameters": {
        "type": "object",
        "properties": {
          "certificate": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 1,
                "maxLength": 100000
              },
              {
                "type": "object",
                "properties": {
                  "insured": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "insurer": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "policy_number": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "effective_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "expires_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "general_liability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "auto_liability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "workers_compensation": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "umbrella": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "additional_insured": {
                    "type": "boolean"
                  },
                  "waiver_of_subrogation": {
                    "type": "boolean"
                  }
                },
                "additionalProperties": false
              }
            ]
          },
          "requirements": {
            "type": "object",
            "properties": {
              "general_liability": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "auto_liability": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "workers_compensation": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "umbrella": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "additional_insured": {
                "type": "boolean"
              },
              "waiver_of_subrogation": {
                "type": "boolean"
              },
              "expires_after": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "certificate",
          "requirements"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "coi__analyze": "0.10",
  "coi__coverage-grade": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "coi__analyze": "coi/analyze",
  "coi__coverage-grade": "coi/coverage-grade"
}


class BrainiacCoiAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — coi",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the coi catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "coi", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract and check a certificate of insurance"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the coi group. "
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
