"""Auto-generated BRAINIAC Heurist Mesh agent for group `contract-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "contract-security__contract-bytecode-compare",
      "description": "Compare contract bytecode. Compare two caller-supplied EVM bytecodes. mode exact compares every byte. An omitted mode is exact. mode normalized masks only the supplied immutable ranges and a trailing Solidity CBOR metadata suffix when bytecodeKind is not creation and that suffix is present on both bytecodes. comparison_status is identical, different, partially_comparable, or invalid. Hashes are keccak256 of the supplied bytes. Similarity is the share of equal compared bytes, truncated to 4 decimal places. A difference is not a judgment that either bytecode is malicious, and similar bytecode is not equivalent behavior. No source code is verified and no chain is queried. Docs: https://www.brainiac.software/api/contract-security/contract-bytecode-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "reference": {
            "type": "string",
            "maxLength": 262146,
            "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
          },
          "candidate": {
            "type": "string",
            "maxLength": 262146,
            "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
          },
          "bytecodeKind": {
            "type": "string",
            "enum": [
              "runtime",
              "creation"
            ]
          },
          "mode": {
            "type": "string",
            "enum": [
              "exact",
              "normalized"
            ]
          },
          "compilerMetadata": {
            "type": "object",
            "properties": {
              "compiler": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "version": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              }
            },
            "additionalProperties": false
          },
          "constructorArguments": {
            "type": "string",
            "maxLength": 262146,
            "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
          },
          "immutableRanges": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "start": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 131072
                },
                "end": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 131072
                }
              },
              "required": [
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          },
          "expectedDifferences": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "start": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 131072
                },
                "end": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 131072
                }
              },
              "required": [
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "reference",
          "candidate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "contract-security__bytecode-structure-diff",
      "description": "Diff bytecode structure. Decode two caller-supplied EVM bytecodes, or two instruction lists, into opcodes and compare the instruction sequence. Similarity ignores PUSH immediates. The risk delta counts CALL, SSTORE, CREATE, DELEGATECALL, CALLCODE, and SELFDESTRUCT. A high similarity is not proof that the contracts behave the same. No chain is queried. Docs: https://www.brainiac.software/api/contract-security/bytecode-structure-diff",
      "parameters": {
        "type": "object",
        "properties": {
          "left": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200000,
                "pattern": "^(0x)?[0-9a-fA-F]*$"
              },
              {
                "type": "object",
                "properties": {
                  "ops": {
                    "minItems": 1,
                    "maxItems": 1500,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "op": {
                          "type": "string",
                          "pattern": "^[A-Za-z][A-Za-z0-9]{0,31}$"
                        },
                        "arg": {
                          "type": "string",
                          "pattern": "^(0x)?[0-9a-fA-F]{0,64}$"
                        }
                      },
                      "required": [
                        "op"
                      ],
                      "additionalProperties": false
                    }
                  }
                },
                "required": [
                  "ops"
                ],
                "additionalProperties": false
              }
            ]
          },
          "right": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200000,
                "pattern": "^(0x)?[0-9a-fA-F]*$"
              },
              {
                "type": "object",
                "properties": {
                  "ops": {
                    "minItems": 1,
                    "maxItems": 1500,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "op": {
                          "type": "string",
                          "pattern": "^[A-Za-z][A-Za-z0-9]{0,31}$"
                        },
                        "arg": {
                          "type": "string",
                          "pattern": "^(0x)?[0-9a-fA-F]{0,64}$"
                        }
                      },
                      "required": [
                        "op"
                      ],
                      "additionalProperties": false
                    }
                  }
                },
                "required": [
                  "ops"
                ],
                "additionalProperties": false
              }
            ]
          }
        },
        "required": [
          "left",
          "right"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "contract-security__contract-bytecode-compare": "0.05",
  "contract-security__bytecode-structure-diff": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "contract-security__contract-bytecode-compare": "contract-security/contract-bytecode-compare",
  "contract-security__bytecode-structure-diff": "contract-security/bytecode-structure-diff"
}


class BrainiacContractSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — contract-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the contract-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "contract-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Compare contract bytecode"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the contract-security group. "
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
