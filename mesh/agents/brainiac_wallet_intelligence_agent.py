"""Auto-generated BRAINIAC Heurist Mesh agent for group `wallet-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "wallet-intelligence__snapshot",
      "description": "Get wallet snapshot. Retrieve current wallet balance and supplied token balances on Base Mainnet with USD valuations from Chainlink Data Feeds on Base and the Coinbase Exchange public ticker (documented Base address map only). Token approvals/allowances are not included; use security/approvals before moving funds. Docs: https://www.brainiac.software/api/wallet-intelligence/snapshot",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "tokenAddresses": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^0x[a-fA-F0-9]{40}$"
            }
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__transfers",
      "description": "Get wallet transfers. Retrieve ERC-20 transfer activity within a requested block range on Base Mainnet using public JSON-RPC. Docs: https://www.brainiac.software/api/wallet-intelligence/transfers",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "tokenAddresses": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^0x[a-fA-F0-9]{40}$"
            }
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
          "limit": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__analyze",
      "description": "Analyze wallet. Consolidate wallet balances and observed transfer activity on Base Mainnet with block range coverage information. Docs: https://www.brainiac.software/api/wallet-intelligence/analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "tokenAddresses": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^0x[a-fA-F0-9]{40}$"
            }
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
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__transaction",
      "description": "Inspect transaction. Inspect a supplied transaction hash on Base Mainnet with gas analysis and USD cost estimation. Docs: https://www.brainiac.software/api/wallet-intelligence/transaction",
      "parameters": {
        "type": "object",
        "properties": {
          "txHash": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{64}$"
          }
        },
        "required": [
          "txHash"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__security__address",
      "description": "Check address security. Check wallet address for malicious activity indicators using GoPlus Labs threat intelligence on Base Mainnet. Docs: https://www.brainiac.software/api/wallet-intelligence/security-address",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__security__approvals",
      "description": "Check approval security. Check wallet address for risky token approvals and permissions using GoPlus Labs risk analysis on Base Mainnet. Docs: https://www.brainiac.software/api/wallet-intelligence/security-approvals",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wallet-intelligence__security__risk-report",
      "description": "Generate security report. Generate a combined security report using GoPlus Labs address security and approval checks on Base Mainnet. Docs: https://www.brainiac.software/api/wallet-intelligence/security-risk-report",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "includeAddressCheck": {
            "default": true,
            "type": "boolean"
          },
          "includeApprovalCheck": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "walletAddress"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "wallet-intelligence__snapshot": "0.02",
  "wallet-intelligence__transfers": "0.05",
  "wallet-intelligence__analyze": "0.10",
  "wallet-intelligence__transaction": "0.03",
  "wallet-intelligence__security__address": "0.05",
  "wallet-intelligence__security__approvals": "0.05",
  "wallet-intelligence__security__risk-report": "0.10"
}
TOOL_ROUTES: Dict[str, str] = {
  "wallet-intelligence__snapshot": "wallet-intelligence/snapshot",
  "wallet-intelligence__transfers": "wallet-intelligence/transfers",
  "wallet-intelligence__analyze": "wallet-intelligence/analyze",
  "wallet-intelligence__transaction": "wallet-intelligence/transaction",
  "wallet-intelligence__security__address": "wallet-intelligence/security/address",
  "wallet-intelligence__security__approvals": "wallet-intelligence/security/approvals",
  "wallet-intelligence__security__risk-report": "wallet-intelligence/security/risk-report"
}


class BrainiacWalletIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — wallet-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the wallet-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "wallet-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Get wallet snapshot"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the wallet-intelligence group. "
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
