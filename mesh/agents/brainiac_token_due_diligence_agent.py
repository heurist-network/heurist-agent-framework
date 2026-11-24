"""Auto-generated BRAINIAC Heurist Mesh agent for group `token-due-diligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "token-due-diligence__analyze",
      "description": "Analyze token contract. Analyze a token contract on Base Mainnet including bytecode, ERC-20 metadata, owner, proxy status, and privileges. Docs: https://www.brainiac.software/api/token-due-diligence/analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "token-due-diligence__liquidity",
      "description": "Inspect DEX liquidity. Inspect supported DEX liquidity pools on Base Mainnet using official Uniswap V2 and V3 factories. Docs: https://www.brainiac.software/api/token-due-diligence/liquidity",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "token-due-diligence__holders",
      "description": "Analyze holder concentration. Analyze holder concentration from transfer events when complete transfer history is available on Base Mainnet. Docs: https://www.brainiac.software/api/token-due-diligence/holders",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "deploymentBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "fromBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "toBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "token-due-diligence__permissions",
      "description": "Inspect contract permissions. Inspect contract ownership and privileged controls on Base Mainnet including owner, admin, and upgradeability. Docs: https://www.brainiac.software/api/token-due-diligence/permissions",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "token-due-diligence__honeypot",
      "description": "Check honeypot status. Check if a token is a honeypot using Honeypot.is simulation, including buy/sell tax, gas information, and contract verification. Docs: https://www.brainiac.software/api/token-due-diligence/honeypot",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "pairAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "token-due-diligence__security-report",
      "description": "Generate security report. Generate a combined security report using Honeypot checks. Docs: https://www.brainiac.software/api/token-due-diligence/security-report",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "pairAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "includeHoneypot": {
            "default": true,
            "type": "boolean"
          },
          "includeMarketActivity": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "token-due-diligence__analyze": "0.01",
  "token-due-diligence__liquidity": "0.01",
  "token-due-diligence__holders": "0.01",
  "token-due-diligence__permissions": "0.01",
  "token-due-diligence__honeypot": "0.01",
  "token-due-diligence__security-report": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "token-due-diligence__analyze": "token-due-diligence/analyze",
  "token-due-diligence__liquidity": "token-due-diligence/liquidity",
  "token-due-diligence__holders": "token-due-diligence/holders",
  "token-due-diligence__permissions": "token-due-diligence/permissions",
  "token-due-diligence__honeypot": "token-due-diligence/honeypot",
  "token-due-diligence__security-report": "token-due-diligence/security-report"
}


class BrainiacTokenDueDiligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — token-due-diligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the token-due-diligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "token-due-diligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze token contract"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the token-due-diligence group. "
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
