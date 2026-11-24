"""Auto-generated BRAINIAC Heurist Mesh agent for group `token-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "token-security__risk-verdict",
      "description": "Token risk verdict. Read a Base token contract and return an evidence-based verdict. Facts, signals, and unavailable checks are separate. No risk score is produced, and absence of a signal is not a safety approval. Docs: https://www.brainiac.software/api/token-security/risk-verdict",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__honeypot-risk-check",
      "description": "Honeypot risk check. Look for observable pause and blacklist indicators in bytecode and standard calls. Optional chain/chainId (default Base; also ethereum, arbitrum, optimism, polygon, bsc). This does not simulate a buy or sell. Docs: https://www.brainiac.software/api/token-security/honeypot-risk-check",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__ownership-risk-check",
      "description": "Ownership risk check. Read owner(), EIP-1967 proxy slots, and bytecode selectors for mint, pause, and blacklist privileges. Optional chain/chainId (default Base; also ethereum, arbitrum, optimism, polygon, bsc). Selector presence is not proof the owner can call them. Docs: https://www.brainiac.software/api/token-security/ownership-risk-check",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__liquidity-risk-assessment",
      "description": "Liquidity risk assessment. Assess pool liquidity reported by the public DEX Screener API, including concentration across returned pools. Optional chain/chainId (default Base). LP lock is not verified. Docs: https://www.brainiac.software/api/token-security/liquidity-risk-assessment",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__manipulation-signals",
      "description": "Token manipulation signals. Report buy, sell, price-change, and volume signals from public DEX Screener data for the largest pool on the selected chain. Optional chain/chainId (default Base). These are feed observations, not proof of manipulation. Docs: https://www.brainiac.software/api/token-security/manipulation-signals",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__due-diligence-report",
      "description": "Token due diligence report. Combine contract checks, DEX Screener observations, and a Honeypot.is sell-simulation into one report. Optional chain/chainId (default Base; also ethereum, arbitrum, optimism, polygon, bsc). The report never approves interaction and does not turn missing evidence into a safety claim. Docs: https://www.brainiac.software/api/token-security/due-diligence-report",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__sell-simulation",
      "description": "Token sell simulation. Simulate buy then sell for a token via Honeypot.is (optional chain/chainId, default Base; also ethereum, arbitrum, optimism, polygon, bsc) and return sellable as pass, fail, or not_checked with buy/sell tax when reported. Absence of a honeypot flag is never recorded as pass without a successful simulation. Docs: https://www.brainiac.software/api/token-security/sell-simulation",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "amountUsd": {
            "default": 100,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 10000
          },
          "pairAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__deployer-funding-trace",
      "description": "Deployer funding and holder clusters. Identify the token deployer via Blockscout when configured for the chain, walk early inbound funding hops, and report holder concentration clusters. Optional chain/chainId (default Base). Unknown funding origin is identified=false with origin_label=unknown — not a neutral skip. Docs: https://www.brainiac.software/api/token-security/deployer-funding-trace",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "maxHops": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 5
          },
          "topHolders": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
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
      "name": "token-security__price-two-source",
      "description": "Two-source token price check. Compare an on-pool DEX Screener USD price with Chainlink Data Feeds on Base and/or the Coinbase Exchange public ticker for a documented Base address→symbol map. Optional chain/chainId (default Base). agree is pass, fail, or not_checked against the second-side midpoint (or single usable source); a single side never yields agree=pass. Docs: https://www.brainiac.software/api/token-security/price-two-source",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "tolerancePct": {
            "default": 2,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 50
          },
          "chain": {
            "type": "string",
            "minLength": 2,
            "maxLength": 32
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
      "name": "token-security__lp-lock-status",
      "description": "LP lock status. Check whether a Base token's DEX LP is locked in a documented locker contract (UNCX V2/V3/Aerodrome) via public Base RPC balanceOf reads. Returns locked, unlocked, or unknown per pool. Unknown is not a safety approval. Docs: https://www.brainiac.software/api/token-security/lp-lock-status",
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
      "name": "token-security__sniper-bundler-scan",
      "description": "Sniper bundler scan. Bounded first-window scan after liquidity is added on Base: early buyers, same-block multi-buys, and simple shared-funding flags from public Base RPC. Not a full holder history. Docs: https://www.brainiac.software/api/token-security/sniper-bundler-scan",
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
          "maxBlocks": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "maxBuyers": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
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
      "name": "token-security__source-verification",
      "description": "Sourcify source verification. Official Sourcify v2 lookup for a Base (or other chainId) token: match type, contract name, compiler, proxy flag, and whether an ABI is present. No Etherscan key. Docs: https://www.brainiac.software/api/token-security/source-verification",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "chainId": {
            "default": 8453,
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
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
  "token-security__risk-verdict": "0.01",
  "token-security__honeypot-risk-check": "0.01",
  "token-security__ownership-risk-check": "0.01",
  "token-security__liquidity-risk-assessment": "0.01",
  "token-security__manipulation-signals": "0.01",
  "token-security__due-diligence-report": "0.01",
  "token-security__sell-simulation": "0.01",
  "token-security__deployer-funding-trace": "0.01",
  "token-security__price-two-source": "0.001",
  "token-security__lp-lock-status": "0.01",
  "token-security__sniper-bundler-scan": "0.01",
  "token-security__source-verification": "0.002"
}
TOOL_ROUTES: Dict[str, str] = {
  "token-security__risk-verdict": "token-security/risk-verdict",
  "token-security__honeypot-risk-check": "token-security/honeypot-risk-check",
  "token-security__ownership-risk-check": "token-security/ownership-risk-check",
  "token-security__liquidity-risk-assessment": "token-security/liquidity-risk-assessment",
  "token-security__manipulation-signals": "token-security/manipulation-signals",
  "token-security__due-diligence-report": "token-security/due-diligence-report",
  "token-security__sell-simulation": "token-security/sell-simulation",
  "token-security__deployer-funding-trace": "token-security/deployer-funding-trace",
  "token-security__price-two-source": "token-security/price-two-source",
  "token-security__lp-lock-status": "token-security/lp-lock-status",
  "token-security__sniper-bundler-scan": "token-security/sniper-bundler-scan",
  "token-security__source-verification": "token-security/source-verification"
}


class BrainiacTokenSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — token-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the token-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "token-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Token risk verdict"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the token-security group. "
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
