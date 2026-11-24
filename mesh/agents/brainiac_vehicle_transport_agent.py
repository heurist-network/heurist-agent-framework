"""Auto-generated BRAINIAC Heurist Mesh agent for group `vehicle-transport` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "vehicle-transport__vin-check-digit-validate",
      "description": "Validate a VIN check digit. Validate the structure and 9th-position check digit of a 17-character VIN and read model-year code candidates from 49 CFR Part 565. Pure computation; no network. Docs: https://www.brainiac.software/api/vehicle-transport/vin-check-digit-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "vin": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          }
        },
        "required": [
          "vin"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vehicle-transport__vin-decode",
      "description": "Decode a VIN via vendored vPIC. Decode a VIN to make, model, year, body, engine and plant fields from the vendored NHTSA vPIC standalone database. No live vPIC API call. Docs: https://www.brainiac.software/api/vehicle-transport/vin-decode",
      "parameters": {
        "type": "object",
        "properties": {
          "vin": {
            "type": "string",
            "minLength": 3,
            "maxLength": 17
          },
          "modelYear": {
            "type": "integer",
            "minimum": 1980,
            "maximum": 2039
          },
          "includeAll": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "vin"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vehicle-transport__nhtsa-recall-by-vin",
      "description": "Look up NHTSA recalls by VIN or make/model/year. List NHTSA safety recall campaigns filed since 2010 for a VIN (decoded locally) or make/model/year from the vendored ODI flat file. Docs: https://www.brainiac.software/api/vehicle-transport/nhtsa-recall-by-vin",
      "parameters": {
        "type": "object",
        "properties": {
          "vin": {
            "type": "string",
            "minLength": 17,
            "maxLength": 17
          },
          "make": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "model": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "modelYear": {
            "type": "integer",
            "minimum": 1900,
            "maximum": 2039
          },
          "recallType": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "V",
                "E",
                "T",
                "C"
              ]
            }
          },
          "limit": {
            "default": 50,
            "type": "integer",
            "minimum": 1,
            "maximum": 200
          },
          "includeUnknownYear": {
            "default": false,
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
      "name": "vehicle-transport__nhtsa-safety-ratings",
      "description": "Look up NHTSA 5-Star Safety Ratings. Return NHTSA Safercar 5-Star Safety Ratings and listed safety equipment for a make, model and model year from the vendored Safercar file. Docs: https://www.brainiac.software/api/vehicle-transport/nhtsa-safety-ratings",
      "parameters": {
        "type": "object",
        "properties": {
          "make": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "model": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "modelYear": {
            "type": "integer",
            "minimum": 1990,
            "maximum": 2027
          },
          "driveTrain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "bodyStyle": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "vin": {
            "type": "string",
            "minLength": 17,
            "maxLength": 17
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vehicle-transport__epa-fuel-economy-lookup",
      "description": "Look up EPA fuel economy. Return EPA fuel-economy, CO2 and annual fuel-cost figures (and EV range/consumption) from the vendored fueleconomy.gov vehicle file. Docs: https://www.brainiac.software/api/vehicle-transport/epa-fuel-economy-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "year": {
            "type": "integer",
            "minimum": 1984,
            "maximum": 2027
          },
          "make": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "model": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "baseModel": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "drive": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "limit": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": [
          "year",
          "make"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vehicle-transport__uk-ved-rate-lookup",
      "description": "Look up UK Vehicle Excise Duty. Compute UK Vehicle Excise Duty for cars, vans, motorcycles and tricycles for the rate year 1 April 2026 – 31 March 2027 from GOV.UK rate tables in code. Docs: https://www.brainiac.software/api/vehicle-transport/uk-ved-rate-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "enum": [
              "car",
              "light-goods",
              "motorcycle",
              "tricycle",
              "private-heavy-goods"
            ]
          },
          "firstRegistered": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "taxDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "payment": {
            "type": "string",
            "enum": [
              "first-registration",
              "renewal"
            ]
          },
          "fuel": {
            "type": "string",
            "enum": [
              "petrol",
              "diesel",
              "alternative",
              "electric"
            ]
          },
          "co2GPerKm": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "dieselMeetsRde2": {
            "type": "boolean"
          },
          "listPricePence": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "engineCc": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "euroStandard": {
            "type": "string",
            "enum": [
              "euro4",
              "euro5"
            ]
          }
        },
        "required": [
          "category",
          "firstRegistered",
          "payment"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vehicle-transport__bts-ontime-lookup",
      "description": "Look up BTS airline on-time performance. Return official on-time, cancellation and diversion counts for a US carrier, airport or route from vendored BTS Reporting Carrier On-Time Performance aggregates (Sep 2025 – Aug 2026). Docs: https://www.brainiac.software/api/vehicle-transport/bts-ontime-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "carrier": {
            "type": "string",
            "pattern": "^[A-Z0-9]{2}$"
          },
          "origin": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "dest": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "year": {
            "type": "integer",
            "minimum": 2025,
            "maximum": 2026
          },
          "month": {
            "type": "integer",
            "minimum": 1,
            "maximum": 12
          },
          "groupBy": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "month",
                "carrier",
                "route"
              ]
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "vehicle-transport__vin-check-digit-validate": "0.01",
  "vehicle-transport__vin-decode": "0.03",
  "vehicle-transport__nhtsa-recall-by-vin": "0.03",
  "vehicle-transport__nhtsa-safety-ratings": "0.02",
  "vehicle-transport__epa-fuel-economy-lookup": "0.02",
  "vehicle-transport__uk-ved-rate-lookup": "0.01",
  "vehicle-transport__bts-ontime-lookup": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "vehicle-transport__vin-check-digit-validate": "vehicle-transport/vin-check-digit-validate",
  "vehicle-transport__vin-decode": "vehicle-transport/vin-decode",
  "vehicle-transport__nhtsa-recall-by-vin": "vehicle-transport/nhtsa-recall-by-vin",
  "vehicle-transport__nhtsa-safety-ratings": "vehicle-transport/nhtsa-safety-ratings",
  "vehicle-transport__epa-fuel-economy-lookup": "vehicle-transport/epa-fuel-economy-lookup",
  "vehicle-transport__uk-ved-rate-lookup": "vehicle-transport/uk-ved-rate-lookup",
  "vehicle-transport__bts-ontime-lookup": "vehicle-transport/bts-ontime-lookup"
}


class BrainiacVehicleTransportAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — vehicle-transport",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the vehicle-transport catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "vehicle-transport", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate a VIN check digit"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the vehicle-transport group. "
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
