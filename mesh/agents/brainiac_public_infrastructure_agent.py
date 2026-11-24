"""Auto-generated BRAINIAC Heurist Mesh agent for group `public-infrastructure` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "public-infrastructure__ip-to-asn-lookup",
      "description": "Map IP or prefix to origin ASN. Longest-prefix match against a vendored RouteViews BGP snapshot, with IANA special-purpose flags. Docs: https://www.brainiac.software/api/public-infrastructure/ip-to-asn-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "ip": {
            "type": "string",
            "minLength": 3,
            "maxLength": 64
          },
          "prefix": {
            "type": "string",
            "minLength": 3,
            "maxLength": 64
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-infrastructure__iana-tld-rdap-bootstrap",
      "description": "IANA RDAP bootstrap lookup. Return IANA RDAP base URLs for a domain, IP or ASN from the vendored bootstrap registries. Docs: https://www.brainiac.software/api/public-infrastructure/iana-tld-rdap-bootstrap",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "ip": {
            "type": "string",
            "minLength": 3,
            "maxLength": 64
          },
          "asn": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              }
            ]
          },
          "full": {
            "type": "string",
            "enum": [
              "dns",
              "ipv4",
              "ipv6",
              "asn"
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
      "name": "public-infrastructure__travel-advisory-lookup",
      "description": "US and UK travel advisory lookup. Return State Department and FCDO travel advice for a country side by side. Docs: https://www.brainiac.software/api/public-infrastructure/travel-advisory-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "country": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100
          }
        },
        "required": [
          "country"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-infrastructure__visa-waiver-list-lookup",
      "description": "US VWP and UK visa-national list lookup. Check whether a nationality appears on the DHS Visa Waiver Program or UK VN 1.1(a) lists. Docs: https://www.brainiac.software/api/public-infrastructure/visa-waiver-list-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "nationality": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100
          },
          "list": {
            "default": "both",
            "type": "string",
            "enum": [
              "us-vwp",
              "uk-visa-national",
              "both"
            ]
          }
        },
        "required": [
          "nationality"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-infrastructure__ofsted-rating-lookup",
      "description": "Ofsted school rating lookup. Look up the latest Ofsted inspection outcomes for a state-funded school in England. Docs: https://www.brainiac.software/api/public-infrastructure/ofsted-rating-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "urn": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20
          },
          "laestab": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20
          },
          "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 200
          },
          "localAuthority": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100
          },
          "postcode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 12
          },
          "limit": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-infrastructure__college-scorecard-lookup",
      "description": "US College Scorecard lookup. Look up cost, admission, completion, earnings and debt fields from the College Scorecard. Docs: https://www.brainiac.software/api/public-infrastructure/college-scorecard-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "unitId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20
          },
          "opeId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20
          },
          "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 200
          },
          "state": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
          },
          "limit": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-infrastructure__grants-gov-opportunity-search",
      "description": "Search open Grants.gov opportunities. Search open US federal grant synopses and forecasts from the Grants.gov daily extract. Docs: https://www.brainiac.software/api/public-infrastructure/grants-gov-opportunity-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "opportunityNumber": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
          },
          "agencyCode": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "cfda": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20
          },
          "eligibleApplicants": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "kind": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "synopsis",
                "forecast"
              ]
            }
          },
          "closingBefore": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "public-infrastructure__ip-to-asn-lookup": "0.02",
  "public-infrastructure__iana-tld-rdap-bootstrap": "0.01",
  "public-infrastructure__travel-advisory-lookup": "0.02",
  "public-infrastructure__visa-waiver-list-lookup": "0.01",
  "public-infrastructure__ofsted-rating-lookup": "0.02",
  "public-infrastructure__college-scorecard-lookup": "0.02",
  "public-infrastructure__grants-gov-opportunity-search": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "public-infrastructure__ip-to-asn-lookup": "public-infrastructure/ip-to-asn-lookup",
  "public-infrastructure__iana-tld-rdap-bootstrap": "public-infrastructure/iana-tld-rdap-bootstrap",
  "public-infrastructure__travel-advisory-lookup": "public-infrastructure/travel-advisory-lookup",
  "public-infrastructure__visa-waiver-list-lookup": "public-infrastructure/visa-waiver-list-lookup",
  "public-infrastructure__ofsted-rating-lookup": "public-infrastructure/ofsted-rating-lookup",
  "public-infrastructure__college-scorecard-lookup": "public-infrastructure/college-scorecard-lookup",
  "public-infrastructure__grants-gov-opportunity-search": "public-infrastructure/grants-gov-opportunity-search"
}


class BrainiacPublicInfrastructureAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — public-infrastructure",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the public-infrastructure catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "public-infrastructure", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Map IP or prefix to origin ASN"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the public-infrastructure group. "
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
