"""Auto-generated BRAINIAC Heurist Mesh agent for group `food-safety` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "food-safety__search",
      "description": "Search food businesses. Search UK food businesses by name, location, postcode, or hygiene rating using the Food Standards Agency Food Hygiene Rating Scheme API. Docs: https://www.brainiac.software/api/food-safety/search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "ratingValue": {
            "type": "string",
            "maxLength": 50
          },
          "businessTypeId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10000
          },
          "localAuthorityId": {
            "type": "string",
            "maxLength": 10
          },
          "postcode": {
            "type": "string",
            "maxLength": 20
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "maxDistance": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "food-safety__business",
      "description": "Get food business details. Retrieve detailed information for a specific food business by its FSA FHRSID from the Food Standards Agency Food Hygiene Rating Scheme API. Docs: https://www.brainiac.software/api/food-safety/business",
      "parameters": {
        "type": "object",
        "properties": {
          "fsaId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "fsaId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "food-safety__batch",
      "description": "Batch lookup food businesses. Retrieve details for multiple food businesses in a single batch request using the Food Standards Agency Food Hygiene Rating Scheme API. Docs: https://www.brainiac.software/api/food-safety/batch",
      "parameters": {
        "type": "object",
        "properties": {
          "fsaIds": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 1,
              "maximum": 9007199254740991
            }
          }
        },
        "required": [
          "fsaIds"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "food-safety__ratings",
      "description": "Get food safety ratings. Retrieve the list of available hygiene rating values and their descriptions from the Food Standards Agency Food Hygiene Rating Scheme API. Docs: https://www.brainiac.software/api/food-safety/ratings",
      "parameters": {
        "type": "object",
        "properties": {
          "schemeType": {
            "type": "string",
            "maxLength": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "food-safety__authorities",
      "description": "Get food safety authorities. Retrieve the list of local authorities and their establishment counts from the Food Standards Agency Food Hygiene Rating Scheme API. Docs: https://www.brainiac.software/api/food-safety/authorities",
      "parameters": {
        "type": "object",
        "properties": {
          "regionName": {
            "type": "string",
            "maxLength": 100
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
  "food-safety__search": "0.05",
  "food-safety__business": "0.03",
  "food-safety__batch": "0.15",
  "food-safety__ratings": "0.01",
  "food-safety__authorities": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "food-safety__search": "food-safety/search",
  "food-safety__business": "food-safety/business",
  "food-safety__batch": "food-safety/batch",
  "food-safety__ratings": "food-safety/ratings",
  "food-safety__authorities": "food-safety/authorities"
}


class BrainiacFoodSafetyAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — food-safety",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the food-safety catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "food-safety", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search food businesses"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the food-safety group. "
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
