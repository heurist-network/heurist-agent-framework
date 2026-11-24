"""Auto-generated BRAINIAC Heurist Mesh agent for group `weather` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "weather__report",
      "description": "City weather report. Current conditions and a multi-day forecast for a city or coordinates via MET Norway Locationforecast 2.0, with city geocoding from a bundled GeoNames dump. If both city and coordinates are sent, coordinates win. Does not include air quality or sunrise/sunset. Docs: https://www.brainiac.software/api/weather/report",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "countryCode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
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
          "timezone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "temperatureUnit": {
            "type": "string",
            "enum": [
              "celsius",
              "fahrenheit"
            ]
          },
          "windSpeedUnit": {
            "type": "string",
            "enum": [
              "kmh",
              "ms",
              "mph",
              "kn"
            ]
          },
          "precipitationUnit": {
            "type": "string",
            "enum": [
              "mm",
              "inch"
            ]
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "weather__sunrise",
      "description": "Sunrise and sunset. Official MET Norway Sunrise 3.0 sunrise, sunset, and solar noon for a city or coordinates. Credit Data from MET Norway. Docs: https://www.brainiac.software/api/weather/sunrise",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "countryCode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
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
          "timezone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "temperatureUnit": {
            "type": "string",
            "enum": [
              "celsius",
              "fahrenheit"
            ]
          },
          "windSpeedUnit": {
            "type": "string",
            "enum": [
              "kmh",
              "ms",
              "mph",
              "kn"
            ]
          },
          "precipitationUnit": {
            "type": "string",
            "enum": [
              "mm",
              "inch"
            ]
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9
          },
          "date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "weather__us-alerts",
      "description": "US NWS weather alerts. Active US National Weather Service watches, warnings, and advisories for a US point or city from the official NWS API. Docs: https://www.brainiac.software/api/weather/us-alerts",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "countryCode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
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
          "timezone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "temperatureUnit": {
            "type": "string",
            "enum": [
              "celsius",
              "fahrenheit"
            ]
          },
          "windSpeedUnit": {
            "type": "string",
            "enum": [
              "kmh",
              "ms",
              "mph",
              "kn"
            ]
          },
          "precipitationUnit": {
            "type": "string",
            "enum": [
              "mm",
              "inch"
            ]
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "weather__report": "0.002",
  "weather__sunrise": "0.002",
  "weather__us-alerts": "0.002"
}
TOOL_ROUTES: Dict[str, str] = {
  "weather__report": "weather/report",
  "weather__sunrise": "weather/sunrise",
  "weather__us-alerts": "weather/us-alerts"
}


class BrainiacWeatherAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — weather",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the weather catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "weather", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["City weather report"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.002",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the weather group. "
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
