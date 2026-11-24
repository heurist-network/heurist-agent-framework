"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-security__transaction-intent-verify",
      "description": "Verify transaction intent. Compare an EVM transaction's calldata and native value with the action declared in the request. Decoding uses the ABI in the request, or the standard ERC-20 transfer, transferFrom, approve, and increaseAllowance encodings when that selector matches. intent_match is true, false, or the string indeterminate when a declared field cannot be checked. risk_level is low, medium, high, or critical. This is static analysis: it does not read chain state, simulate the call, or decide that a contract is malicious or that the transaction will succeed. Docs: https://www.brainiac.software/api/crypto-security/transaction-intent-verify",
      "parameters": {
        "type": "object",
        "properties": {
          "chainId": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 2147483647
          },
          "contractAddress": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "calldata": {
            "type": "string",
            "maxLength": 131074,
            "pattern": "^0x(?:[0-9a-fA-F]{2})*$"
          },
          "value": {
            "type": "string"
          },
          "expectedAction": {
            "type": "string",
            "enum": [
              "transfer",
              "token_approval",
              "swap",
              "contract_interaction"
            ]
          },
          "expected": {
            "type": "object",
            "properties": {
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
              },
              "contract": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              },
              "functionName": {
                "type": "string",
                "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,79}$"
              },
              "nativeValue": {
                "type": "string"
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
          "chainId",
          "contractAddress",
          "calldata",
          "value",
          "expectedAction"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-security__intent-safety",
      "description": "Score transaction intent safety. Read a caller-supplied EVM transaction or an EIP-712 typed-data message and describe the transfer, approval, permit, or outer call it encodes. Known selectors are transfer, transferFrom, approve, increaseAllowance, setApprovalForAll, permit, multicall, aggregate, and execute. The score is a local penalty count. It does not simulate the call or read a chain. Docs: https://www.brainiac.software/api/crypto-security/intent-safety",
      "parameters": {
        "type": "object",
        "properties": {
          "transaction": {
            "type": "object",
            "properties": {
              "to": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              },
              "value": {
                "type": "string",
                "pattern": "^(0x[0-9a-fA-F]+|\\d+)$"
              },
              "data": {
                "type": "string",
                "maxLength": 100000,
                "pattern": "^(0x)?[0-9a-fA-F]*$"
              }
            },
            "required": [
              "data"
            ],
            "additionalProperties": false
          },
          "typed_data": {
            "type": "object",
            "properties": {
              "primaryType": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "domain": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              },
              "types": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "maxItems": 40,
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
                        "maxLength": 80
                      }
                    },
                    "required": [
                      "name",
                      "type"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "message": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              }
            },
            "required": [
              "primaryType",
              "message"
            ],
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-security__proxy-upgrade-storage-audit",
      "description": "Audit proxy upgrade storage. Compare the Solidity storage layout of an upgradeable implementation with a proposed replacement. Variables are matched by slot and offset, not by name. The types map is used for structs, mappings, dynamic arrays, and byte sizes. compatibility_status is compatible, incompatible, warnings, or indeterminate. risk_level is low, medium, high, or critical. A compatible result is not a claim that the upgrade is safe. No chain is queried. Docs: https://www.brainiac.software/api/crypto-security/proxy-upgrade-storage-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "proxyPattern": {
            "type": "string",
            "enum": [
              "uups",
              "transparent",
              "beacon",
              "custom"
            ]
          },
          "current": {
            "type": "object",
            "properties": {
              "storage": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "astId": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "contract": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "label": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "offset": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 31
                    },
                    "slot": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,77})$"
                    },
                    "type": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "label",
                    "offset",
                    "slot",
                    "type"
                  ],
                  "additionalProperties": false
                }
              },
              "types": {
                "type": "object",
                "propertyNames": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "encoding": {
                      "type": "string",
                      "enum": [
                        "inplace",
                        "mapping",
                        "dynamic_array",
                        "bytes"
                      ]
                    },
                    "label": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "numberOfBytes": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,8})$"
                    },
                    "base": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "key": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "members": {
                      "maxItems": 64,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "astId": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 9007199254740991
                          },
                          "contract": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 200
                          },
                          "label": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 80
                          },
                          "offset": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 31
                          },
                          "slot": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,77})$"
                          },
                          "type": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 200
                          }
                        },
                        "required": [
                          "label",
                          "offset",
                          "slot",
                          "type"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "encoding",
                    "label"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "storage"
            ],
            "additionalProperties": false
          },
          "proposed": {
            "type": "object",
            "properties": {
              "storage": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "astId": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "contract": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "label": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "offset": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 31
                    },
                    "slot": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,77})$"
                    },
                    "type": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "label",
                    "offset",
                    "slot",
                    "type"
                  ],
                  "additionalProperties": false
                }
              },
              "types": {
                "type": "object",
                "propertyNames": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "additionalProperties": {
                  "type": "object",
                  "properties": {
                    "encoding": {
                      "type": "string",
                      "enum": [
                        "inplace",
                        "mapping",
                        "dynamic_array",
                        "bytes"
                      ]
                    },
                    "label": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "numberOfBytes": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,8})$"
                    },
                    "base": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "key": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "members": {
                      "maxItems": 64,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "astId": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 9007199254740991
                          },
                          "contract": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 200
                          },
                          "label": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 80
                          },
                          "offset": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 31
                          },
                          "slot": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,77})$"
                          },
                          "type": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 200
                          }
                        },
                        "required": [
                          "label",
                          "offset",
                          "slot",
                          "type"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "encoding",
                    "label"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "storage"
            ],
            "additionalProperties": false
          },
          "currentMetadata": {
            "type": "object",
            "properties": {
              "contractName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "compilerVersion": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "sourceName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "proposedMetadata": {
            "type": "object",
            "properties": {
              "contractName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "compilerVersion": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "sourceName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "current",
          "proposed"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-security__storage-slot-grade",
      "description": "Grade proxy storage slot changes. Compare two caller-supplied storage layouts by slot, offset, and size. A name that moves is a shift. Different names that occupy the same bytes are a collision. The grade and the collision score come from those counts. A variable is one slice of a single slot. No chain is queried. Docs: https://www.brainiac.software/api/crypto-security/storage-slot-grade",
      "parameters": {
        "type": "object",
        "properties": {
          "previous": {
            "minItems": 1,
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,79}$"
                },
                "slot": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "offset": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 31
                },
                "size": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 32
                }
              },
              "required": [
                "name",
                "slot"
              ],
              "additionalProperties": false
            }
          },
          "next": {
            "minItems": 1,
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z_][A-Za-z0-9_]{0,79}$"
                },
                "slot": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "offset": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 31
                },
                "size": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 32
                }
              },
              "required": [
                "name",
                "slot"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "previous",
          "next"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-security__transaction-intent-verify": "0.04",
  "crypto-security__intent-safety": "0.04",
  "crypto-security__proxy-upgrade-storage-audit": "0.05",
  "crypto-security__storage-slot-grade": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-security__transaction-intent-verify": "crypto-security/transaction-intent-verify",
  "crypto-security__intent-safety": "crypto-security/intent-safety",
  "crypto-security__proxy-upgrade-storage-audit": "crypto-security/proxy-upgrade-storage-audit",
  "crypto-security__storage-slot-grade": "crypto-security/storage-slot-grade"
}


class BrainiacCryptoSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Verify transaction intent"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-security group. "
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
