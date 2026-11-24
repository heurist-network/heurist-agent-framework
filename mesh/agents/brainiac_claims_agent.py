"""Auto-generated BRAINIAC Heurist Mesh agent for group `claims` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "claims__analyze",
      "description": "Analyze a policy and prepare claim evidence. Extract policy clauses, run a preliminary text-match screen, and build a general evidence checklist. This is not legal advice or confirmation of coverage. Docs: https://www.brainiac.software/api/claims/analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "filename": {
            "default": "policy.pdf",
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          },
          "fileBase64": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20971520
          },
          "incidentDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "incidentType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 12000
          },
          "knownDocuments": {
            "default": [],
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 240
            }
          }
        },
        "required": [
          "fileBase64",
          "incidentType",
          "description"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "claims__validity",
      "description": "Score claim validity against exclusions. Match a caller-supplied incident to policy exclusions, dates, and the limit. The validity score falls when an exclusion's distinctive words appear in the incident, and the denial risk rises with those matches. This is a text screen, not a claim decision. Docs: https://www.brainiac.software/api/claims/validity",
      "parameters": {
        "type": "object",
        "properties": {
          "incident": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 20,
                "maxLength": 20000
              },
              {
                "type": "object",
                "properties": {
                  "description": {
                    "type": "string",
                    "minLength": 20,
                    "maxLength": 20000
                  },
                  "occurred_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "notice_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "loss_type": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "amount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  }
                },
                "required": [
                  "description"
                ],
                "additionalProperties": false
              }
            ]
          },
          "policy": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 20,
                "maxLength": 50000
              },
              {
                "type": "object",
                "properties": {
                  "text": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50000
                  },
                  "effective_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "expires_on": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "limit": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "perils": {
                    "maxItems": 40,
                    "type": "array",
                    "items": {
                      "type": "string",
                      "minLength": 2,
                      "maxLength": 80
                    }
                  },
                  "exclusions": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "string",
                      "minLength": 3,
                      "maxLength": 400
                    }
                  }
                },
                "additionalProperties": false
              }
            ]
          }
        },
        "required": [
          "incident",
          "policy"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "claims__letter-draft",
      "description": "Draft insurer correspondence. Prepare a human-reviewed FNOL, follow-up, or complaint letter. BRAINIAC.software does not send the message or make legal conclusions. Docs: https://www.brainiac.software/api/claims/letter-draft",
      "parameters": {
        "type": "object",
        "properties": {
          "kind": {
            "type": "string",
            "enum": [
              "fnol",
              "chase",
              "complaint"
            ]
          },
          "insurer": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "policyNumber": {
            "type": "string",
            "maxLength": 120
          },
          "claimNumber": {
            "type": "string",
            "maxLength": 120
          },
          "incidentDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "summary": {
            "type": "string",
            "minLength": 1,
            "maxLength": 6000
          },
          "requestedAction": {
            "type": "string",
            "maxLength": 2000
          }
        },
        "required": [
          "kind",
          "insurer",
          "summary"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "claims__dispute-draft",
      "description": "Draft a claim or dispute letter. Fill a fixed claim or dispute letter from the caller-supplied facts and the scores from a validity screen. The same fields always produce the same letter. The draft is not sent and it is not a legal filing. Docs: https://www.brainiac.software/api/claims/dispute-draft",
      "parameters": {
        "type": "object",
        "properties": {
          "purpose": {
            "type": "string",
            "enum": [
              "claim",
              "dispute"
            ]
          },
          "claimant": {
            "type": "string",
            "minLength": 2,
            "maxLength": 160
          },
          "insurer": {
            "type": "string",
            "minLength": 2,
            "maxLength": 160
          },
          "policy_number": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "claim_number": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "incident_date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "amount": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "facts": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          },
          "claim_validity_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "risk_of_denial_percentage": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "matched_exclusions": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "clause": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 400
                },
                "basis": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 240
                }
              },
              "required": [
                "clause",
                "basis"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "purpose",
          "claimant",
          "insurer"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "claims__analyze": "0.10",
  "claims__validity": "0.04",
  "claims__letter-draft": "0.02",
  "claims__dispute-draft": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "claims__analyze": "claims/analyze",
  "claims__validity": "claims/validity",
  "claims__letter-draft": "claims/letter-draft",
  "claims__dispute-draft": "claims/dispute-draft"
}


class BrainiacClaimsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — claims",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the claims catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "claims", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze a policy and prepare claim evidence"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the claims group. "
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
