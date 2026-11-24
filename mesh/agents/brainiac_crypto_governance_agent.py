"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-governance` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-governance__governance-execution-diff",
      "description": "Diff governance execution. Compare the structured actions in a caller-supplied DAO proposal with the caller-supplied execution calls. Targets, selectors, decoded parameters, and native value are compared. execution_match is exact, partial, mismatch, or indeterminate. risk_level is low, medium, high, or critical. The proposal description is not treated as the approved action list. No chain is queried, and approval or execution is not inferred from chain state. Docs: https://www.brainiac.software/api/crypto-governance/governance-execution-diff",
      "parameters": {
        "type": "object",
        "properties": {
          "proposal": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "description": {
                "type": "string",
                "maxLength": 4000
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 2147483647
          },
          "orderSensitive": {
            "type": "boolean"
          },
          "approvedActions": {
            "minItems": 1,
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "target": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "signature": {
                  "type": "string",
                  "pattern": "^[A-Za-z_][A-Za-z0-9_]*\\((?:[A-Za-z0-9_[\\],() ]{0,400})\\)$"
                },
                "functionName": {
                  "type": "string",
                  "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,79}$"
                },
                "calldata": {
                  "type": "string",
                  "maxLength": 131074,
                  "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
                },
                "value": {
                  "type": "string"
                },
                "parameters": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "type": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "value": {
                        "type": "string",
                        "maxLength": 2000
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "recipient": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "token": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "amount": {
                  "type": "string"
                },
                "spender": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                }
              },
              "required": [
                "target"
              ],
              "additionalProperties": false
            }
          },
          "execution": {
            "type": "object",
            "properties": {
              "transactionHash": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{64}$"
              },
              "value": {
                "type": "string"
              },
              "calls": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "target": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "signature": {
                      "type": "string",
                      "pattern": "^[A-Za-z_][A-Za-z0-9_]*\\((?:[A-Za-z0-9_[\\],() ]{0,400})\\)$"
                    },
                    "functionName": {
                      "type": "string",
                      "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,79}$"
                    },
                    "calldata": {
                      "type": "string",
                      "maxLength": 131074,
                      "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
                    },
                    "value": {
                      "type": "string"
                    },
                    "parameters": {
                      "maxItems": 32,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 80
                          },
                          "type": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 200
                          },
                          "value": {
                            "type": "string",
                            "maxLength": 2000
                          }
                        },
                        "required": [
                          "name",
                          "value"
                        ],
                        "additionalProperties": false
                      }
                    },
                    "recipient": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "token": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "amount": {
                      "type": "string"
                    },
                    "spender": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    }
                  },
                  "required": [
                    "target"
                  ],
                  "additionalProperties": false
                }
              },
              "logs": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "address": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "topics": {
                      "maxItems": 4,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "pattern": "^0x[0-9a-fA-F]{64}$"
                      }
                    },
                    "data": {
                      "type": "string",
                      "maxLength": 131074,
                      "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
                    },
                    "fields": {
                      "type": "object",
                      "propertyNames": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "additionalProperties": {
                        "type": "string",
                        "maxLength": 2000
                      }
                    }
                  },
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "fieldMapping": {
            "type": "object",
            "properties": {
              "target": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "signature": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "functionName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "recipient": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "amount": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "spender": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "value": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              }
            },
            "additionalProperties": false
          },
          "abi": {
            "maxItems": 48,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "function",
                    "constructor",
                    "receive",
                    "fallback",
                    "event",
                    "error"
                  ]
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "stateMutability": {
                  "type": "string",
                  "enum": [
                    "pure",
                    "view",
                    "nonpayable",
                    "payable"
                  ]
                },
                "inputs": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {}
                },
                "outputs": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {}
                },
                "anonymous": {
                  "type": "boolean"
                }
              },
              "required": [
                "type"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "proposal",
          "approvedActions",
          "execution"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-governance__execution-risk-score",
      "description": "Score governance execution drift. Apply caller-supplied transfer and transferFrom calls to the supplied token balances. A transfer that is not in the expected list is unforeseen. The drift index is the share of balances that change. Amounts stay inside the local integer limit. This is not an EVM simulation and no chain is queried. Docs: https://www.brainiac.software/api/crypto-governance/execution-risk-score",
      "parameters": {
        "type": "object",
        "properties": {
          "sender": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "calls": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "target": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "data": {
                  "type": "string",
                  "maxLength": 20000,
                  "pattern": "^0x[0-9a-fA-F]*$"
                },
                "value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "target",
                "data"
              ],
              "additionalProperties": false
            }
          },
          "balances": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "token": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$|^native$"
                },
                "account": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "token",
                "account",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "token": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$|^native$"
                },
                "to": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "token",
                "to",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "sender",
          "calls",
          "balances"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-governance__governance-execution-diff": "0.05",
  "crypto-governance__execution-risk-score": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-governance__governance-execution-diff": "crypto-governance/governance-execution-diff",
  "crypto-governance__execution-risk-score": "crypto-governance/execution-risk-score"
}


class BrainiacCryptoGovernanceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-governance",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-governance catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-governance", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Diff governance execution"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-governance group. "
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
