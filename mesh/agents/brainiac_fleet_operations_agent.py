"""Auto-generated BRAINIAC Heurist Mesh agent for group `fleet-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "fleet-operations__fuel-card-abuse-detect",
      "description": "Detect fuel card abuse. Flag fuel card transactions that exceed tank capacity, mismatch fuel type, duplicate within a time window, share one card across vehicles, overflow the tank without mileage burn evidence, or appear too far from the vehicle for the supplied max speed. Volumes are millilitres. Every flag includes deterministic evidence. No telematics or merchant network is queried. Docs: https://www.brainiac.software/api/fleet-operations/fuel-card-abuse-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "vehicles": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "registration": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fuel_type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "tank_capacity_ml": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "expected_consumption_ml_per_km": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "max_speed_meters_per_hour": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "fuel_type",
                "tank_capacity_ml"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "card_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "vehicle_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "purchased_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "volume_ml": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "fuel_type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "station_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
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
                }
              },
              "required": [
                "id",
                "card_id",
                "vehicle_id",
                "purchased_at",
                "volume_ml",
                "amount",
                "currency",
                "fuel_type"
              ],
              "additionalProperties": false
            }
          },
          "odometer_readings": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "vehicle_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "reading_km": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "recorded_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                }
              },
              "required": [
                "id",
                "vehicle_id",
                "reading_km",
                "recorded_at"
              ],
              "additionalProperties": false
            }
          },
          "locations": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "vehicle_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
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
                "recorded_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                }
              },
              "required": [
                "id",
                "vehicle_id",
                "latitude",
                "longitude",
                "recorded_at"
              ],
              "additionalProperties": false
            }
          },
          "duplicate_window_minutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": [
          "vehicles",
          "transactions"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "fleet-operations__fuel-card-abuse-detect": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "fleet-operations__fuel-card-abuse-detect": "fleet-operations/fuel-card-abuse-detect"
}


class BrainiacFleetOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — fleet-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the fleet-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "fleet-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect fuel card abuse"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the fleet-operations group. "
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
