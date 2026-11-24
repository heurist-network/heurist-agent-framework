"""Auto-generated BRAINIAC Heurist Mesh agent for group `company-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "company-intelligence__search",
      "description": "Search companies. Search companies by name and country using the GLEIF LEI database. Docs: https://www.brainiac.software/api/company-intelligence/search",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
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
      "name": "company-intelligence__profile",
      "description": "Get company profile. Retrieve a company profile using LEI from GLEIF. Docs: https://www.brainiac.software/api/company-intelligence/profile",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__ownership",
      "description": "Get company ownership. Retrieve parent and subsidiary relationships from GLEIF. Docs: https://www.brainiac.software/api/company-intelligence/ownership",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__financials",
      "description": "Get company financials. Retrieve and normalize financial metrics from SEC EDGAR using CIK or ticker. Docs: https://www.brainiac.software/api/company-intelligence/financials",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__filings",
      "description": "Get company filings. Retrieve recent SEC EDGAR filings by CIK or ticker. Optional formTypes filter (for example 10-K, 10-Q, 8-K). Each row includes primaryDocument, official documentUrl, and indexUrl when EDGAR publishes them. Docs: https://www.brainiac.software/api/company-intelligence/filings",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "formTypes": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 20
            }
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__insider-trades",
      "description": "SEC Form 4 insider trades. Official SEC Form 4 insider transactions for a US-listed issuer by ticker or CIK, parsed from EDGAR ownership XML. Docs: https://www.brainiac.software/api/company-intelligence/insider-trades",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          },
          "limit": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "transactionCodes": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4
            }
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__institutional-holdings",
      "description": "SEC 13F institutional holdings. Latest official SEC 13F-HR holdings for a filer by ticker or CIK, parsed from the EDGAR information table. Docs: https://www.brainiac.software/api/company-intelligence/institutional-holdings",
      "parameters": {
        "type": "object",
        "properties": {
          "identifier": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          },
          "limit": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": [
          "identifier"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "company-intelligence__vat-id-lookup",
      "description": "Look up VAT ID and registry numbers. Validate a supplied EU VAT ID with VIES and/or search GLEIF by company name for official registration numbers. Does not invent a VAT ID when VIES has none, and does not call UK Companies House. Docs: https://www.brainiac.software/api/company-intelligence/vat-id-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "vatId": {
            "type": "string",
            "minLength": 4,
            "maxLength": 32
          },
          "companyName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
          },
          "limit": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 20
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "company-intelligence__search": "0.01",
  "company-intelligence__profile": "0.02",
  "company-intelligence__ownership": "0.03",
  "company-intelligence__financials": "0.003",
  "company-intelligence__filings": "0.003",
  "company-intelligence__insider-trades": "0.001",
  "company-intelligence__institutional-holdings": "0.003",
  "company-intelligence__vat-id-lookup": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "company-intelligence__search": "company-intelligence/search",
  "company-intelligence__profile": "company-intelligence/profile",
  "company-intelligence__ownership": "company-intelligence/ownership",
  "company-intelligence__financials": "company-intelligence/financials",
  "company-intelligence__filings": "company-intelligence/filings",
  "company-intelligence__insider-trades": "company-intelligence/insider-trades",
  "company-intelligence__institutional-holdings": "company-intelligence/institutional-holdings",
  "company-intelligence__vat-id-lookup": "company-intelligence/vat-id-lookup"
}


class BrainiacCompanyIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — company-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the company-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "company-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search companies"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the company-intelligence group. "
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
