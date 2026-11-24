"""Auto-generated BRAINIAC Heurist Mesh agent for group `energy-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "energy-intelligence__current",
      "description": "Get current carbon intensity. Retrieve current GB electricity carbon intensity from the Carbon Intensity API. Supports optional regional filtering. Docs: https://www.brainiac.software/api/energy-intelligence/current",
      "parameters": {
        "type": "object",
        "properties": {
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "energy-intelligence__historical",
      "description": "Get historical carbon intensity. Retrieve historical or forecast carbon intensity data for a specific time period from the Carbon Intensity API. Supports regional filtering. Docs: https://www.brainiac.software/api/energy-intelligence/historical",
      "parameters": {
        "type": "object",
        "properties": {
          "from": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "to": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "energy-intelligence__regional",
      "description": "Get regional carbon intensity. Retrieve carbon intensity data for all GB regions or a specific region from the Carbon Intensity API. Includes generation mix information. Docs: https://www.brainiac.software/api/energy-intelligence/regional",
      "parameters": {
        "type": "object",
        "properties": {
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "energy-intelligence__generation-mix",
      "description": "Get generation mix. Retrieve electricity generation mix data showing fuel type proportions from the Carbon Intensity API. Supports regional and time-based filtering. Docs: https://www.brainiac.software/api/energy-intelligence/generation-mix",
      "parameters": {
        "type": "object",
        "properties": {
          "from": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "to": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "energy-intelligence__forecast",
      "description": "Get carbon intensity forecast. Retrieve forecast carbon intensity data from the Carbon Intensity API. Supports regional filtering. Docs: https://www.brainiac.software/api/energy-intelligence/forecast",
      "parameters": {
        "type": "object",
        "properties": {
          "from": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "to": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          },
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "energy-intelligence__regions",
      "description": "Get all regions. Retrieve metadata for all GB regions supported by the Carbon Intensity API including region IDs and names. Docs: https://www.brainiac.software/api/energy-intelligence/regions",
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
      "name": "energy-intelligence__report",
      "description": "Get energy intelligence report. Generate a comprehensive energy intelligence report combining current intensity, regional data, and generation mix from the Carbon Intensity API. Docs: https://www.brainiac.software/api/energy-intelligence/report",
      "parameters": {
        "type": "object",
        "properties": {
          "regionId": {
            "type": "integer",
            "minimum": 1,
            "maximum": 18
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "energy-intelligence__current": "0.02",
  "energy-intelligence__historical": "0.05",
  "energy-intelligence__regional": "0.05",
  "energy-intelligence__generation-mix": "0.03",
  "energy-intelligence__forecast": "0.03",
  "energy-intelligence__regions": "0.01",
  "energy-intelligence__report": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "energy-intelligence__current": "energy-intelligence/current",
  "energy-intelligence__historical": "energy-intelligence/historical",
  "energy-intelligence__regional": "energy-intelligence/regional",
  "energy-intelligence__generation-mix": "energy-intelligence/generation-mix",
  "energy-intelligence__forecast": "energy-intelligence/forecast",
  "energy-intelligence__regions": "energy-intelligence/regions",
  "energy-intelligence__report": "energy-intelligence/report"
}


class BrainiacEnergyIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — energy-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the energy-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "energy-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Get current carbon intensity"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the energy-intelligence group. "
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
