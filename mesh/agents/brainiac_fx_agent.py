"""Auto-generated BRAINIAC Heurist Mesh agent for group `fx` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "fx__rates__latest",
      "description": "Get latest exchange rates. Retrieve latest ECB reference rates via Frankfurter. Accepts ISO codes or pairs such as EURUSD, EUR/USD, EUR-USD. Successful bodies include source, date, delayed, and a delayed-reference limitation. Docs: https://www.brainiac.software/api/fx/rates-latest",
      "parameters": {
        "type": "object",
        "properties": {
          "pair": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "base": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "symbols": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 3,
                "maxLength": 8
              },
              {
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                }
              }
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
      "name": "fx__rates__historical",
      "description": "Get historical exchange rates. Retrieve ECB reference rates for a specific date via Frankfurter. Accepts ISO codes or pairs such as EURUSD, EUR/USD, EUR-USD. Returns rates for the closest working day with source, date, and delayed fields. Docs: https://www.brainiac.software/api/fx/rates-historical",
      "parameters": {
        "type": "object",
        "properties": {
          "date": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "pair": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "base": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "symbols": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 3,
                "maxLength": 8
              },
              {
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                }
              }
            ]
          }
        },
        "required": [
          "date"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fx__rates__timeseries",
      "description": "Get timeseries exchange rates. Retrieve ECB reference rates over a date range via Frankfurter. Accepts ISO codes or pairs such as EURUSD, EUR/USD, EUR-USD for the currency side. Returns source, date, delayed, and a delayed-reference limitation. Docs: https://www.brainiac.software/api/fx/rates-timeseries",
      "parameters": {
        "type": "object",
        "properties": {
          "from": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "to": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "pair": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "base": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "symbols": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 3,
                "maxLength": 8
              },
              {
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                }
              }
            ]
          }
        },
        "required": [
          "from",
          "to"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fx__rates__convert",
      "description": "Convert currency amount. Convert an amount using delayed ECB reference rates via Frankfurter. Accepts from/to ISO codes or a pair such as EURUSD. Returns amount, from, to, rate, result, source, date, and delayed. Docs: https://www.brainiac.software/api/fx/rates-convert",
      "parameters": {
        "type": "object",
        "properties": {
          "amount": {
            "type": "number",
            "minimum": 0.01
          },
          "pair": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "from": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "to": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          },
          "date": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          }
        },
        "required": [
          "amount"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fx__currencies__list",
      "description": "List supported currencies. Retrieve the list of supported currencies from the Frankfurter API. All currencies are ISO 4217 codes. Docs: https://www.brainiac.software/api/fx/currencies-list",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fx__ptax",
      "description": "Brazil PTAX FX rate. Official Central Bank of Brazil PTAX buy and sell quotes for USD or another listed PTAX currency, by date or the latest published bulletin. Not an ECB reference rate and not a crypto BRL market. Docs: https://www.brainiac.software/api/fx/ptax",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "currencies": {
            "minItems": 1,
            "maxItems": 5,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 3,
              "maxLength": 3
            }
          },
          "quoteDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "fx__rates__latest": "0.004",
  "fx__rates__historical": "0.004",
  "fx__rates__timeseries": "0.004",
  "fx__rates__convert": "0.004",
  "fx__currencies__list": "0.004",
  "fx__ptax": "0.002"
}
TOOL_ROUTES: Dict[str, str] = {
  "fx__rates__latest": "fx/rates/latest",
  "fx__rates__historical": "fx/rates/historical",
  "fx__rates__timeseries": "fx/rates/timeseries",
  "fx__rates__convert": "fx/rates/convert",
  "fx__currencies__list": "fx/currencies/list",
  "fx__ptax": "fx/ptax"
}


class BrainiacFxAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — fx",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the fx catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "fx", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Get latest exchange rates"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.002",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the fx group. "
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
