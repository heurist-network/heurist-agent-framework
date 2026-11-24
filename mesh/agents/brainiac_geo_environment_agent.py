"""Auto-generated BRAINIAC Heurist Mesh agent for group `geo-environment` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "geo-environment__fire-hotspots-nearby",
      "description": "List nearby NASA FIRMS fire hotspots. List MODIS C6.1 active-fire detections within a radius from the vendored 7-day FIRMS snapshot. Docs: https://www.brainiac.software/api/geo-environment/fire-hotspots-nearby",
      "parameters": {
        "type": "object",
        "properties": {
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
          "radiusKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 500
          },
          "from": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "to": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "minConfidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "limit": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          }
        },
        "required": [
          "latitude",
          "longitude",
          "radiusKm"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "geo-environment__earthquake-query",
      "description": "Query USGS earthquakes nearby. Find earthquakes within a radius and time window from the vendored USGS all_month feed. Docs: https://www.brainiac.software/api/geo-environment/earthquake-query",
      "parameters": {
        "type": "object",
        "properties": {
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
          "radiusKm": {
            "type": "number",
            "minimum": 1,
            "maximum": 20000
          },
          "minMagnitude": {
            "type": "number"
          },
          "from": {
            "type": "string",
            "minLength": 10,
            "maxLength": 40
          },
          "to": {
            "type": "string",
            "minLength": 10,
            "maxLength": 40
          },
          "eventType": {
            "default": "earthquake",
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "sort": {
            "default": "time",
            "type": "string",
            "enum": [
              "time",
              "magnitude"
            ]
          },
          "limit": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          }
        },
        "required": [
          "latitude",
          "longitude",
          "radiusKm"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "geo-environment__sun-times-position",
      "description": "Compute sunrise sunset and solar position. Compute sunrise, solar noon, sunset, day length and solar elevation/azimuth with NOAA Solar Calculator equations. Docs: https://www.brainiac.software/api/geo-environment/sun-times-position",
      "parameters": {
        "type": "object",
        "properties": {
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
          "date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "instant": {
            "type": "string",
            "minLength": 10,
            "maxLength": 40
          },
          "timeZone": {
            "default": "UTC",
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          }
        },
        "required": [
          "latitude",
          "longitude"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "geo-environment__us-acs-demographics",
      "description": "Look up US ACS demographics. Return selected ACS 2020–2024 5-year estimates and margins of error for a US state, county or ZCTA. Docs: https://www.brainiac.software/api/geo-environment/us-acs-demographics",
      "parameters": {
        "type": "object",
        "properties": {
          "geography": {
            "type": "string",
            "enum": [
              "state",
              "county",
              "zcta"
            ]
          },
          "code": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          }
        },
        "required": [
          "geography",
          "code"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "geo-environment__gtfs-next-arrivals",
      "description": "Compute next GTFS scheduled arrivals. Compute next scheduled arrivals at a stop from a caller-supplied static GTFS zip. No feeds are fetched. Docs: https://www.brainiac.software/api/geo-environment/gtfs-next-arrivals",
      "parameters": {
        "type": "object",
        "properties": {
          "gtfsZipBase64": {
            "type": "string",
            "minLength": 16,
            "maxLength": 14000000
          },
          "stopId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "at": {
            "type": "string",
            "minLength": 10,
            "maxLength": 40
          },
          "limit": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "includeChildStops": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "gtfsZipBase64",
          "stopId",
          "at"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "geo-environment__fire-hotspots-nearby": "0.03",
  "geo-environment__earthquake-query": "0.03",
  "geo-environment__sun-times-position": "0.01",
  "geo-environment__us-acs-demographics": "0.03",
  "geo-environment__gtfs-next-arrivals": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "geo-environment__fire-hotspots-nearby": "geo-environment/fire-hotspots-nearby",
  "geo-environment__earthquake-query": "geo-environment/earthquake-query",
  "geo-environment__sun-times-position": "geo-environment/sun-times-position",
  "geo-environment__us-acs-demographics": "geo-environment/us-acs-demographics",
  "geo-environment__gtfs-next-arrivals": "geo-environment/gtfs-next-arrivals"
}


class BrainiacGeoEnvironmentAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — geo-environment",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the geo-environment catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "geo-environment", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["List nearby NASA FIRMS fire hotspots"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the geo-environment group. "
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
