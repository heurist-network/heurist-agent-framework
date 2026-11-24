"""Auto-generated BRAINIAC Heurist Mesh agent for group `product-safety` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "product-safety__cpsc-recall-search",
      "description": "Search CPSC product recalls. Search US CPSC recalls by keyword, firm, recall number, UPC or date range in the vendored snapshot. Docs: https://www.brainiac.software/api/product-safety/cpsc-recall-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 2,
            "maxLength": 120
          },
          "recallNumber": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "upc": {
            "type": "string",
            "minLength": 6,
            "maxLength": 14
          },
          "firm": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "to": {
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
  },
  {
    "type": "function",
    "function": {
      "name": "product-safety__eu-safety-gate-alert",
      "description": "Search EU Safety Gate alerts. Search EU Safety Gate (RAPEX) non-food product alerts from vendored English weekly reports since 2024. Docs: https://www.brainiac.software/api/product-safety/eu-safety-gate-alert",
      "parameters": {
        "type": "object",
        "properties": {
          "barcode": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "brand": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "category": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "riskType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "notifyingCountry": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "level": {
            "type": "string",
            "enum": [
              "Serious risk",
              "Other risk levels",
              "Other types of alerts"
            ]
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "to": {
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
  },
  {
    "type": "function",
    "function": {
      "name": "product-safety__fsa-allergy-alert-search",
      "description": "Search FSA allergy and food alerts. Search UK FSA allergy alerts, product recall information notices and food alerts for action. Docs: https://www.brainiac.software/api/product-safety/fsa-allergy-alert-search",
      "parameters": {
        "type": "object",
        "properties": {
          "allergen": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "business": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "alertType": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "AA",
                "PRIN",
                "FAFA"
              ]
            }
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "to": {
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
  },
  {
    "type": "function",
    "function": {
      "name": "product-safety__canada-health-recall-search",
      "description": "Search Canada recalls and safety alerts. Search Government of Canada Recalls and Safety Alerts open data in English or French. Docs: https://www.brainiac.software/api/product-safety/canada-health-recall-search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "organization": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "category": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "recallClass": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "includeArchived": {
            "default": false,
            "type": "boolean"
          },
          "language": {
            "default": "en",
            "type": "string",
            "enum": [
              "en",
              "fr"
            ]
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "to": {
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
  },
  {
    "type": "function",
    "function": {
      "name": "product-safety__usda-fooddata-nutrition",
      "description": "Look up USDA FoodData nutrition. Return nutrient values per 100 g from USDA FoodData Central Foundation Foods and SR Legacy. Docs: https://www.brainiac.software/api/product-safety/usda-fooddata-nutrition",
      "parameters": {
        "type": "object",
        "properties": {
          "fdcId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "query": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100
          },
          "dataType": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "Foundation",
                "SR Legacy"
              ]
            }
          },
          "nutrients": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
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
      "name": "product-safety__gs1-digital-link-parse",
      "description": "Parse a GS1 Digital Link URI. Parse an uncompressed GS1 Digital Link URI into primary key, qualifiers and attributes; return canonical URI and element string. Docs: https://www.brainiac.software/api/product-safety/gs1-digital-link-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "uri": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2048
          }
        },
        "required": [
          "uri"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "product-safety__cpsc-recall-search": "0.03",
  "product-safety__eu-safety-gate-alert": "0.03",
  "product-safety__fsa-allergy-alert-search": "0.03",
  "product-safety__canada-health-recall-search": "0.03",
  "product-safety__usda-fooddata-nutrition": "0.03",
  "product-safety__gs1-digital-link-parse": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "product-safety__cpsc-recall-search": "product-safety/cpsc-recall-search",
  "product-safety__eu-safety-gate-alert": "product-safety/eu-safety-gate-alert",
  "product-safety__fsa-allergy-alert-search": "product-safety/fsa-allergy-alert-search",
  "product-safety__canada-health-recall-search": "product-safety/canada-health-recall-search",
  "product-safety__usda-fooddata-nutrition": "product-safety/usda-fooddata-nutrition",
  "product-safety__gs1-digital-link-parse": "product-safety/gs1-digital-link-parse"
}


class BrainiacProductSafetyAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — product-safety",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the product-safety catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "product-safety", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search CPSC product recalls"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the product-safety group. "
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
