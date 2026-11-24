"""Auto-generated BRAINIAC Heurist Mesh agent for group `identifiers` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "identifiers__phone-e164-validate",
      "description": "Validate a phone number to E.164. Normalise and validate a phone number with bundled libphonenumber metadata. Returns validity, E.164, region, calling code, and number type when known. Not a live carrier lookup. Docs: https://www.brainiac.software/api/identifiers/phone-e164-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "phone": {
            "type": "string",
            "minLength": 3,
            "maxLength": 32
          },
          "defaultRegion": {
            "type": "string",
            "pattern": "^[A-Za-z]{2}$"
          }
        },
        "required": [
          "phone"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__gtin-checksum-validate",
      "description": "Validate a GTIN check digit. Validate GTIN-8, GTIN-12, GTIN-13, or GTIN-14 check digits with the published GS1 algorithm. Company prefix ownership is not looked up. Docs: https://www.brainiac.software/api/identifiers/gtin-checksum-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "gtin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 18
          }
        },
        "required": [
          "gtin"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__isbn-issn-validate",
      "description": "Validate ISBN or ISSN check digits. Validate ISBN-10, ISBN-13, or ISSN check characters after stripping spaces and hyphens. Bibliographic metadata is not looked up. Docs: https://www.brainiac.software/api/identifiers/isbn-issn-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "value": {
            "type": "string",
            "minLength": 8,
            "maxLength": 24
          },
          "kind": {
            "default": "auto",
            "type": "string",
            "enum": [
              "auto",
              "isbn",
              "issn"
            ]
          }
        },
        "required": [
          "value"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__eori-format-validate",
      "description": "Validate EORI number format. Validate Economic Operators Registration and Identification (EORI) shape: ISO country prefix plus up to 15 alphanumeric characters. Does not confirm the number is issued. Docs: https://www.brainiac.software/api/identifiers/eori-format-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "eori": {
            "type": "string",
            "minLength": 3,
            "maxLength": 24
          }
        },
        "required": [
          "eori"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__address-parse-normalize",
      "description": "Parse and normalise a postal address. Heuristically split a free-text address into street, locality, region, postal code, and country hints. No postal directory is used. Docs: https://www.brainiac.software/api/identifiers/address-parse-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "minLength": 3,
            "maxLength": 500
          },
          "countryHint": {
            "type": "string",
            "pattern": "^[A-Za-z]{2}$"
          }
        },
        "required": [
          "address"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__unit-ucum-convert",
      "description": "Convert UCUM units. Convert a numeric value between a small bundled UCUM / alias unit subset (length, mass, volume, time, temperature). Incommensurable units return converted=null. Docs: https://www.brainiac.software/api/identifiers/unit-ucum-convert",
      "parameters": {
        "type": "object",
        "properties": {
          "value": {
            "type": "number"
          },
          "from": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          },
          "to": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          }
        },
        "required": [
          "value",
          "from",
          "to"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identifiers__us-zcta-geocode",
      "description": "Geocode a US ZIP to Census ZCTA. Resolve a US 5-digit ZIP to its Census ZIP Code Tabulation Area (ZCTA) internal point and land/water area from the vendored 2026 Gazetteer. Optional toZip returns great-circle distance. Not a street-address geocoder. Docs: https://www.brainiac.software/api/identifiers/us-zcta-geocode",
      "parameters": {
        "type": "object",
        "properties": {
          "zip": {
            "type": "string",
            "pattern": "^\\d{5}(-\\d{4})?$"
          },
          "toZip": {
            "type": "string",
            "pattern": "^\\d{5}(-\\d{4})?$"
          }
        },
        "required": [
          "zip"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "identifiers__phone-e164-validate": "0.02",
  "identifiers__gtin-checksum-validate": "0.01",
  "identifiers__isbn-issn-validate": "0.01",
  "identifiers__eori-format-validate": "0.01",
  "identifiers__address-parse-normalize": "0.02",
  "identifiers__unit-ucum-convert": "0.02",
  "identifiers__us-zcta-geocode": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "identifiers__phone-e164-validate": "identifiers/phone-e164-validate",
  "identifiers__gtin-checksum-validate": "identifiers/gtin-checksum-validate",
  "identifiers__isbn-issn-validate": "identifiers/isbn-issn-validate",
  "identifiers__eori-format-validate": "identifiers/eori-format-validate",
  "identifiers__address-parse-normalize": "identifiers/address-parse-normalize",
  "identifiers__unit-ucum-convert": "identifiers/unit-ucum-convert",
  "identifiers__us-zcta-geocode": "identifiers/us-zcta-geocode"
}


class BrainiacIdentifiersAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — identifiers",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the identifiers catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "identifiers", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate a phone number to E.164"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the identifiers group. "
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
