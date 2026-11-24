"""Auto-generated BRAINIAC Heurist Mesh agent for group `exclusion` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "exclusion__normalize",
      "description": "Normalize a vendor identity. Normalize identifiers before source screening. This operation does not determine eligibility. Docs: https://www.brainiac.software/api/exclusion/normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "legalName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__screen",
      "description": "Screen a vendor against OFAC. Compare a vendor name with the official OFAC SDN list. Candidate matches require human review; source unavailability produces WARN. Docs: https://www.brainiac.software/api/exclusion/screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "legalName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__evidence-report",
      "description": "Build an exclusion screening evidence report. Screen a vendor name against the official OFAC SDN list and produce a PDF with source status, candidate records, timestamp, and snapshot hash. Matches are not identity confirmations. Docs: https://www.brainiac.software/api/exclusion/evidence-report",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "legalName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__uk__screen",
      "description": "Screen a vendor against UK Sanctions List. Compare a vendor name with the official UK Sanctions List XML. Candidate matches require human review; source unavailability produces WARN. Docs: https://www.brainiac.software/api/exclusion/uk-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "legalName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__uk__changes",
      "description": "Get UK Sanctions List changes. Retrieve changes to the UK Sanctions List since a given date, using the official Last Updated field and designation dates. Docs: https://www.brainiac.software/api/exclusion/uk-changes",
      "parameters": {
        "type": "object",
        "properties": {
          "since": {
            "type": "string"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__batch-screen",
      "description": "Batch screen vendors against OFAC. Screen multiple vendors against the official OFAC SDN list. Each vendor is screened independently. Docs: https://www.brainiac.software/api/exclusion/batch-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "vendors": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "legalName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 240
                }
              },
              "required": [
                "legalName"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "vendors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__multi-list__screen",
      "description": "Screen a vendor against multiple exclusion lists. Combine OFAC SDN and UK Sanctions List screening for a single vendor. Matches across lists require human identity review. Docs: https://www.brainiac.software/api/exclusion/multi-list-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "legalName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exclusion__crypto-address-screen",
      "description": "OFAC crypto address screen. Exact-match screen of one crypto address against digital currency addresses published on the official US Treasury OFAC SDN list. A miss is not a safety approval. Docs: https://www.brainiac.software/api/exclusion/crypto-address-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "minLength": 6,
            "maxLength": 200
          },
          "chainHint": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          }
        },
        "required": [
          "address"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "exclusion__normalize": "0.01",
  "exclusion__screen": "0.15",
  "exclusion__evidence-report": "0.15",
  "exclusion__uk__screen": "0.15",
  "exclusion__uk__changes": "0.05",
  "exclusion__batch-screen": "0.10",
  "exclusion__multi-list__screen": "0.20",
  "exclusion__crypto-address-screen": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "exclusion__normalize": "exclusion/normalize",
  "exclusion__screen": "exclusion/screen",
  "exclusion__evidence-report": "exclusion/evidence-report",
  "exclusion__uk__screen": "exclusion/uk/screen",
  "exclusion__uk__changes": "exclusion/uk/changes",
  "exclusion__batch-screen": "exclusion/batch-screen",
  "exclusion__multi-list__screen": "exclusion/multi-list/screen",
  "exclusion__crypto-address-screen": "exclusion/crypto-address-screen"
}


class BrainiacExclusionAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — exclusion",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the exclusion catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "exclusion", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize a vendor identity"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the exclusion group. "
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
