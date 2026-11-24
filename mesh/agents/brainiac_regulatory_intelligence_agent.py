"""Auto-generated BRAINIAC Heurist Mesh agent for group `regulatory-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "regulatory-intelligence__uk__search",
      "description": "Search UK legislation. Search UK legislation by keyword, document type, year, and jurisdiction. Note: legislation.gov.uk does not provide a public JSON search API. This endpoint has limited functionality. Docs: https://www.brainiac.software/api/regulatory-intelligence/uk-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "legislationType": {
            "type": "string",
            "maxLength": 50
          },
          "year": {
            "type": "integer",
            "minimum": 1000,
            "maximum": 3000
          },
          "jurisdiction": {
            "type": "string",
            "maxLength": 50
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
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
      "name": "regulatory-intelligence__uk__details",
      "description": "Get UK legislation details. Retrieve UK legislation details, publication dates, commencement information, and amendment metadata from legislation.gov.uk XML data. Docs: https://www.brainiac.software/api/regulatory-intelligence/uk-details",
      "parameters": {
        "type": "object",
        "properties": {
          "documentId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          }
        },
        "required": [
          "documentId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "regulatory-intelligence__us__search",
      "description": "Search US Federal Register. Search US Federal Register documents by keyword, agency, document type, and publication date using the official federalregister.gov API. Docs: https://www.brainiac.software/api/regulatory-intelligence/us-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "agencyId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "documentType": {
            "type": "string",
            "maxLength": 100
          },
          "publicationDateFrom": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "publicationDateTo": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "page": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
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
      "name": "regulatory-intelligence__us__details",
      "description": "Get US Federal Register document details. Retrieve US Federal Register document details and effective dates from the official federalregister.gov API. Docs: https://www.brainiac.software/api/regulatory-intelligence/us-details",
      "parameters": {
        "type": "object",
        "properties": {
          "documentNumber": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
          }
        },
        "required": [
          "documentNumber"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "regulatory-intelligence__us__agencies",
      "description": "Get US Federal Register agencies. Retrieve list of US Federal Register agencies with their IDs and metadata from the official federalregister.gov API. Docs: https://www.brainiac.software/api/regulatory-intelligence/us-agencies",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "maxLength": 200
          },
          "limit": {
            "default": 50,
            "type": "integer",
            "minimum": 1,
            "maximum": 200
          },
          "page": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "regulatory-intelligence__uk__search": "0.05",
  "regulatory-intelligence__uk__details": "0.05",
  "regulatory-intelligence__us__search": "0.05",
  "regulatory-intelligence__us__details": "0.03",
  "regulatory-intelligence__us__agencies": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "regulatory-intelligence__uk__search": "regulatory-intelligence/uk/search",
  "regulatory-intelligence__uk__details": "regulatory-intelligence/uk/details",
  "regulatory-intelligence__us__search": "regulatory-intelligence/us/search",
  "regulatory-intelligence__us__details": "regulatory-intelligence/us/details",
  "regulatory-intelligence__us__agencies": "regulatory-intelligence/us/agencies"
}


class BrainiacRegulatoryIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — regulatory-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the regulatory-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "regulatory-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search UK legislation"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the regulatory-intelligence group. "
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
