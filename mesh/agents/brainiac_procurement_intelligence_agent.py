"""Auto-generated BRAINIAC Heurist Mesh agent for group `procurement-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "procurement-intelligence__search",
      "description": "Search procurement opportunities. Search UK procurement opportunities from Contracts Finder and Find a Tender with filtering by date, stage, keyword, CPV, location, and value. Docs: https://www.brainiac.software/api/procurement-intelligence/search",
      "parameters": {
        "type": "object",
        "properties": {
          "publishedFrom": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "publishedTo": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "stages": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "keyword": {
            "type": "string",
            "maxLength": 200
          },
          "cpvCode": {
            "type": "string",
            "maxLength": 20
          },
          "location": {
            "type": "string",
            "maxLength": 100
          },
          "minValue": {
            "type": "number",
            "minimum": 0
          },
          "maxValue": {
            "type": "number",
            "minimum": 0
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "cursor": {
            "type": "string",
            "maxLength": 200
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__opportunity",
      "description": "Get opportunity details. Retrieve full details of a procurement opportunity by OCID from UK Contracts Finder or Find a Tender. Docs: https://www.brainiac.software/api/procurement-intelligence/opportunity",
      "parameters": {
        "type": "object",
        "properties": {
          "ocid": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          }
        },
        "required": [
          "ocid"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__buyer",
      "description": "Get buyer procurement history. Retrieve procurement history for a buyer from UK Contracts Finder and Find a Tender. Docs: https://www.brainiac.software/api/procurement-intelligence/buyer",
      "parameters": {
        "type": "object",
        "properties": {
          "buyerId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": [
          "buyerId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__awards",
      "description": "Get awarded contracts. Retrieve awarded contracts and suppliers from UK Contracts Finder and Find a Tender by OCID or buyer ID. Docs: https://www.brainiac.software/api/procurement-intelligence/awards",
      "parameters": {
        "type": "object",
        "properties": {
          "ocid": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "buyerId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
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
      "name": "procurement-intelligence__match",
      "description": "Match company to opportunities. Match a company profile against available procurement opportunities from UK Contracts Finder and Find a Tender with transparent scoring. Docs: https://www.brainiac.software/api/procurement-intelligence/match",
      "parameters": {
        "type": "object",
        "properties": {
          "companyProfile": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "industries": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "keywords": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "cpvCodes": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "locations": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "minValue": {
                "type": "number",
                "minimum": 0
              },
              "maxValue": {
                "type": "number",
                "minimum": 0
              },
              "capabilities": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            },
            "required": [
              "name"
            ],
            "additionalProperties": false
          },
          "publishedFrom": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "publishedTo": {
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
        "required": [
          "companyProfile"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__eu__notices__search",
      "description": "Search EU notices. Search published EU procurement notices from TED with filtering by keyword, CPV code, NUTS code, and date range. Docs: https://www.brainiac.software/api/procurement-intelligence/eu-notices-search",
      "parameters": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string"
          },
          "cpvCode": {
            "type": "string"
          },
          "nutsCode": {
            "type": "string"
          },
          "startDate": {
            "type": "string"
          },
          "endDate": {
            "type": "string"
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
      "name": "procurement-intelligence__eu__notices__resolve",
      "description": "Resolve EU notice. Retrieve full details of an EU procurement notice from TED by notice ID. Docs: https://www.brainiac.software/api/procurement-intelligence/eu-notices-resolve",
      "parameters": {
        "type": "object",
        "properties": {
          "noticeId": {
            "type": "string"
          }
        },
        "required": [
          "noticeId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__us__awards__search",
      "description": "Search US awards. Search federal contract awards from USAspending with filtering by keyword, recipient, agency, and fiscal year. Docs: https://www.brainiac.software/api/procurement-intelligence/us-awards-search",
      "parameters": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string"
          },
          "recipientId": {
            "type": "string"
          },
          "agencyId": {
            "type": "string"
          },
          "fiscalYear": {
            "type": "integer",
            "minimum": 2000,
            "maximum": 2099
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
      "name": "procurement-intelligence__us__recipients__profile",
      "description": "Get US recipient profile. Retrieve recipient details from USAspending by recipient ID. Docs: https://www.brainiac.software/api/procurement-intelligence/us-recipients-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "recipientId": {
            "type": "string"
          }
        },
        "required": [
          "recipientId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__us__recipients__awards",
      "description": "Get US recipient awards. Retrieve award history for a US recipient from USAspending by recipient ID. Docs: https://www.brainiac.software/api/procurement-intelligence/us-recipients-awards",
      "parameters": {
        "type": "object",
        "properties": {
          "recipientId": {
            "type": "string"
          },
          "limit": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": [
          "recipientId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "procurement-intelligence__us__agency-spend",
      "description": "Get US agency spend. Retrieve award spending data for a US federal agency from USAspending by agency ID. Docs: https://www.brainiac.software/api/procurement-intelligence/us-agency-spend",
      "parameters": {
        "type": "object",
        "properties": {
          "agencyId": {
            "type": "string"
          },
          "fiscalYear": {
            "type": "integer",
            "minimum": 2000,
            "maximum": 2099
          }
        },
        "required": [
          "agencyId"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "procurement-intelligence__search": "0.02",
  "procurement-intelligence__opportunity": "0.03",
  "procurement-intelligence__buyer": "0.05",
  "procurement-intelligence__awards": "0.05",
  "procurement-intelligence__match": "0.10",
  "procurement-intelligence__eu__notices__search": "0.05",
  "procurement-intelligence__eu__notices__resolve": "0.05",
  "procurement-intelligence__us__awards__search": "0.05",
  "procurement-intelligence__us__recipients__profile": "0.05",
  "procurement-intelligence__us__recipients__awards": "0.05",
  "procurement-intelligence__us__agency-spend": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "procurement-intelligence__search": "procurement-intelligence/search",
  "procurement-intelligence__opportunity": "procurement-intelligence/opportunity",
  "procurement-intelligence__buyer": "procurement-intelligence/buyer",
  "procurement-intelligence__awards": "procurement-intelligence/awards",
  "procurement-intelligence__match": "procurement-intelligence/match",
  "procurement-intelligence__eu__notices__search": "procurement-intelligence/eu/notices/search",
  "procurement-intelligence__eu__notices__resolve": "procurement-intelligence/eu/notices/resolve",
  "procurement-intelligence__us__awards__search": "procurement-intelligence/us/awards/search",
  "procurement-intelligence__us__recipients__profile": "procurement-intelligence/us/recipients/profile",
  "procurement-intelligence__us__recipients__awards": "procurement-intelligence/us/recipients/awards",
  "procurement-intelligence__us__agency-spend": "procurement-intelligence/us/agency-spend"
}


class BrainiacProcurementIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — procurement-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the procurement-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "procurement-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search procurement opportunities"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the procurement-intelligence group. "
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
