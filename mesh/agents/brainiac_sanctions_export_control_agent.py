"""Auto-generated BRAINIAC Heurist Mesh agent for group `sanctions-export-control` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "sanctions-export-control__itar-usml-lookup",
      "description": "Look up USML category headings. Search 22 CFR 121 USML category headings and keywords. Returns category matches only — not an export classification determination. Docs: https://www.brainiac.software/api/sanctions-export-control/itar-usml-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "category": {
            "type": "string",
            "minLength": 1,
            "maxLength": 8
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 21
          }
        },
        "required": [
          "query"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "sanctions-export-control__eu-sanctions-screen",
      "description": "Screen a name against the EU consolidated sanctions list. Compare a name with the vendored EU consolidated list of persons, groups and entities subject to EU financial sanctions (every name and alias, all languages). Candidate matches carry the EU reference number, programmes and regulations and need human review. Docs: https://www.brainiac.software/api/sanctions-export-control/eu-sanctions-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "type": {
            "default": "any",
            "type": "string",
            "enum": [
              "individual",
              "entity",
              "any"
            ]
          },
          "programme": {
            "type": "string",
            "pattern": "^[A-Z]{2,6}$"
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
      "name": "sanctions-export-control__ca-sema-screen",
      "description": "Screen a name against the Canadian SEMA sanctions list. Compare a name with the vendored Canada consolidated Special Economic Measures Act (SEMA) sanctions list, including aliases. Candidate matches need human review. Docs: https://www.brainiac.software/api/sanctions-export-control/ca-sema-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "type": {
            "default": "any",
            "type": "string",
            "enum": [
              "individual",
              "entity",
              "vessel",
              "any"
            ]
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
      "name": "sanctions-export-control__au-dfat-screen",
      "description": "Screen a name or vessel IMO against the Australian sanctions list. Compare a name, or a vessel IMO number, with the vendored DFAT Australian Sanctions Consolidated List. Candidate matches carry the reference, alias strength and measures and need human review. Docs: https://www.brainiac.software/api/sanctions-export-control/au-dfat-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "imoNumber": {
            "type": "string",
            "pattern": "^\\d{7}$"
          },
          "type": {
            "default": "any",
            "type": "string",
            "enum": [
              "individual",
              "entity",
              "vessel",
              "any"
            ]
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "sanctions-export-control__ofac-non-sdn-screen",
      "description": "Screen a name against OFAC non-SDN lists. Compare a name with the vendored OFAC Consolidated (non-SDN) list: SSI, NS-MBS, CMIC, NS-PLC and CAPTA. SDN screening stays in exclusion.screen. Candidate matches need human review. Docs: https://www.brainiac.software/api/sanctions-export-control/ofac-non-sdn-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "lists": {
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "SSI",
                "NS-MBS",
                "CMIC",
                "NS-PLC",
                "CAPTA"
              ]
            }
          },
          "type": {
            "default": "any",
            "type": "string",
            "enum": [
              "individual",
              "entity",
              "vessel",
              "any"
            ]
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
      "name": "sanctions-export-control__bis-denied-party-screen",
      "description": "Screen a party against the BIS Entity, Denied Persons, Unverified and MEU lists. Compare a party name with the vendored BIS rows of the Consolidated Screening List: Entity List, Denied Persons List, Unverified List and Military End-User List. Candidate matches carry addresses, licence requirement and policy and need human review. Docs: https://www.brainiac.software/api/sanctions-export-control/bis-denied-party-screen",
      "parameters": {
        "type": "object",
        "properties": {
          "legalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "country": {
            "type": "string",
            "pattern": "^[A-Z]{2}$"
          },
          "lists": {
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "EL",
                "DPL",
                "UVL",
                "MEU"
              ]
            }
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
      "name": "sanctions-export-control__ccl-eccn-lookup",
      "description": "Look up a Commerce Control List ECCN. Return the Commerce Control List entry text for an ECCN, or ECCN headings matching keywords, from the vendored eCFR 15 CFR part 774 snapshot. Text lookup only, not an export classification. Docs: https://www.brainiac.software/api/sanctions-export-control/ccl-eccn-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "eccn": {
            "type": "string",
            "pattern": "^([0-9][A-E][0-9]{3}|EAR99)(\\.[a-z0-9.]+)?$"
          },
          "query": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "sanctions-export-control__usml-category-lookup",
      "description": "Look up United States Munitions List text. Return the USML (22 CFR 121.1) text for a category or paragraph, or paragraphs matching keywords, from the vendored eCFR snapshot. Not a jurisdiction or classification determination. Docs: https://www.brainiac.software/api/sanctions-export-control/usml-category-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "pattern": "^(XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I|XXI)(\\([a-z]\\)(\\([0-9]+\\))?)?$"
          },
          "query": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "sanctions-export-control__itar-usml-lookup": "0.04",
  "sanctions-export-control__eu-sanctions-screen": "0.05",
  "sanctions-export-control__ca-sema-screen": "0.05",
  "sanctions-export-control__au-dfat-screen": "0.05",
  "sanctions-export-control__ofac-non-sdn-screen": "0.05",
  "sanctions-export-control__bis-denied-party-screen": "0.05",
  "sanctions-export-control__ccl-eccn-lookup": "0.04",
  "sanctions-export-control__usml-category-lookup": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "sanctions-export-control__itar-usml-lookup": "sanctions-export-control/itar-usml-lookup",
  "sanctions-export-control__eu-sanctions-screen": "sanctions-export-control/eu-sanctions-screen",
  "sanctions-export-control__ca-sema-screen": "sanctions-export-control/ca-sema-screen",
  "sanctions-export-control__au-dfat-screen": "sanctions-export-control/au-dfat-screen",
  "sanctions-export-control__ofac-non-sdn-screen": "sanctions-export-control/ofac-non-sdn-screen",
  "sanctions-export-control__bis-denied-party-screen": "sanctions-export-control/bis-denied-party-screen",
  "sanctions-export-control__ccl-eccn-lookup": "sanctions-export-control/ccl-eccn-lookup",
  "sanctions-export-control__usml-category-lookup": "sanctions-export-control/usml-category-lookup"
}


class BrainiacSanctionsExportControlAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — sanctions-export-control",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the sanctions-export-control catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "sanctions-export-control", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Look up USML category headings"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the sanctions-export-control group. "
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
