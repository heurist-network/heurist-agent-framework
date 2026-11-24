"""Auto-generated BRAINIAC Heurist Mesh agent for group `health-codes` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "health-codes__fda-ndc-lookup",
      "description": "Look up an FDA NDC product or package. Resolve a 10-digit or 11-digit NDC, or search a proprietary/non-proprietary name, in the vendored FDA NDC Directory subset of human prescription and OTC drugs. Docs: https://www.brainiac.software/api/health-codes/fda-ndc-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "ndc": {
            "type": "string",
            "pattern": "^[0-9\\-]{9,13}$"
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 120
          },
          "labeler": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "limit": {
            "default": 20,
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
      "name": "health-codes__fda-orange-book-lookup",
      "description": "Look up FDA Orange Book products, patents and exclusivity. Return Orange Book product, therapeutic-equivalence, patent and exclusivity rows for an application number, trade name or ingredient from the vendored Orange Book data files. Docs: https://www.brainiac.software/api/health-codes/fda-orange-book-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "applNo": {
            "type": "string",
            "pattern": "^\\d{6}$"
          },
          "applType": {
            "type": "string",
            "enum": [
              "N",
              "A"
            ]
          },
          "tradeName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "ingredient": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "includeDiscontinued": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "health-codes__fda-510k-lookup",
      "description": "Look up an FDA 510(k) or De Novo decision. Find a 510(k) or De Novo decision by number, applicant, device name or product code in the vendored FDA 510(k) releasable database (1996–current). Docs: https://www.brainiac.software/api/health-codes/fda-510k-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "kNumber": {
            "type": "string",
            "pattern": "^(K|DEN)\\d{6}$"
          },
          "applicant": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "deviceName": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "productCode": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "limit": {
            "default": 20,
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
      "name": "health-codes__fda-drug-enforcement-search",
      "description": "Search FDA drug recall enforcement reports. Search vendored openFDA drug enforcement reports by recall number, firm, product text, classification or status. Docs: https://www.brainiac.software/api/health-codes/fda-drug-enforcement-search",
      "parameters": {
        "type": "object",
        "properties": {
          "recallNumber": {
            "type": "string",
            "pattern": "^D-\\d{4}-\\d{4}$"
          },
          "firm": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "product": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "classification": {
            "type": "string",
            "enum": [
              "Class I",
              "Class II",
              "Class III"
            ]
          },
          "status": {
            "type": "string",
            "enum": [
              "Ongoing",
              "Completed",
              "Terminated"
            ]
          },
          "reportDateFrom": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "reportDateTo": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "limit": {
            "default": 20,
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
      "name": "health-codes__fda-drug-shortage-lookup",
      "description": "Look up FDA drug shortage entries. Look up vendored openFDA drug-shortage entries by generic name, package NDC or company, with the snapshot date of the export. Docs: https://www.brainiac.software/api/health-codes/fda-drug-shortage-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "genericName": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "packageNdc": {
            "type": "string",
            "minLength": 5,
            "maxLength": 20
          },
          "company": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "status": {
            "type": "string",
            "enum": [
              "Current",
              "To Be Discontinued",
              "Resolved"
            ]
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
  },
  {
    "type": "function",
    "function": {
      "name": "health-codes__cqc-location-lookup",
      "description": "Look up a CQC-registered care location. Look up a CQC-registered care location in England from the vendored care directory and latest published Overall ratings by location id, name, postcode or provider id. Docs: https://www.brainiac.software/api/health-codes/cqc-location-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "locationId": {
            "type": "string",
            "pattern": "^1-\\d+$"
          },
          "name": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "postcode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 16
          },
          "providerId": {
            "type": "string",
            "minLength": 3,
            "maxLength": 32
          },
          "limit": {
            "default": 20,
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
  "health-codes__fda-ndc-lookup": "0.03",
  "health-codes__fda-orange-book-lookup": "0.03",
  "health-codes__fda-510k-lookup": "0.03",
  "health-codes__fda-drug-enforcement-search": "0.03",
  "health-codes__fda-drug-shortage-lookup": "0.03",
  "health-codes__cqc-location-lookup": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "health-codes__fda-ndc-lookup": "health-codes/fda-ndc-lookup",
  "health-codes__fda-orange-book-lookup": "health-codes/fda-orange-book-lookup",
  "health-codes__fda-510k-lookup": "health-codes/fda-510k-lookup",
  "health-codes__fda-drug-enforcement-search": "health-codes/fda-drug-enforcement-search",
  "health-codes__fda-drug-shortage-lookup": "health-codes/fda-drug-shortage-lookup",
  "health-codes__cqc-location-lookup": "health-codes/cqc-location-lookup"
}


class BrainiacHealthCodesAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — health-codes",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the health-codes catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "health-codes", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Look up an FDA NDC product or package"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the health-codes group. "
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
