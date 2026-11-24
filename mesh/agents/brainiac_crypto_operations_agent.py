"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-operations__bridge-partial-failure-audit",
      "description": "Audit bridge partial failure. Compare caller-supplied source and destination records for a cross-chain bridge. Operations are matched only by message identifier, or by the log field named in fieldMapping. Amounts are scaled with the supplied decimals, fee, and optional conversion rate. consistency_status is consistent, inconsistent, incomplete, or indeterminate. risk_level is low, medium, high, or critical. A missing record is incomplete evidence, not proof that the bridge failed. No chain is queried, and no transaction is treated as final. Docs: https://www.brainiac.software/api/crypto-operations/bridge-partial-failure-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "source": {
            "type": "object",
            "properties": {
              "chainId": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 2147483647
              },
              "transactions": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "hash": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{64}$"
                    },
                    "from": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "to": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "nonce": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 2147483647
                    },
                    "receipt": {
                      "type": "object",
                      "properties": {
                        "status": {
                          "type": "string",
                          "enum": [
                            "success",
                            "reverted"
                          ]
                        },
                        "logs": {
                          "maxItems": 40,
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "logIndex": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 1000000
                              },
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
                                "maxLength": 8194,
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
                                  "maxLength": 200
                                }
                              }
                            },
                            "additionalProperties": false
                          }
                        }
                      },
                      "required": [
                        "status"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "required": [
                    "hash"
                  ],
                  "additionalProperties": false
                }
              },
              "operations": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "messageId": {
                      "type": "string",
                      "maxLength": 200,
                      "pattern": "^\\S(?:.*\\S)?$"
                    },
                    "nonce": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,77})$"
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
                    "decimals": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 36
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "pending",
                        "sent",
                        "completed",
                        "failed",
                        "reverted"
                      ]
                    },
                    "transactionHash": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{64}$"
                    }
                  },
                  "required": [
                    "messageId"
                  ],
                  "additionalProperties": false
                }
              },
              "token": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              },
              "amount": {
                "type": "string"
              },
              "decimals": {
                "type": "integer",
                "minimum": 0,
                "maximum": 36
              }
            },
            "required": [
              "chainId"
            ],
            "additionalProperties": false
          },
          "destination": {
            "type": "object",
            "properties": {
              "chainId": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 2147483647
              },
              "transactions": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "hash": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{64}$"
                    },
                    "from": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "to": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{40}$"
                    },
                    "nonce": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 2147483647
                    },
                    "receipt": {
                      "type": "object",
                      "properties": {
                        "status": {
                          "type": "string",
                          "enum": [
                            "success",
                            "reverted"
                          ]
                        },
                        "logs": {
                          "maxItems": 40,
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "logIndex": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 1000000
                              },
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
                                "maxLength": 8194,
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
                                  "maxLength": 200
                                }
                              }
                            },
                            "additionalProperties": false
                          }
                        }
                      },
                      "required": [
                        "status"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "required": [
                    "hash"
                  ],
                  "additionalProperties": false
                }
              },
              "operations": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "messageId": {
                      "type": "string",
                      "maxLength": 200,
                      "pattern": "^\\S(?:.*\\S)?$"
                    },
                    "nonce": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,77})$"
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
                    "decimals": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 36
                    },
                    "status": {
                      "type": "string",
                      "enum": [
                        "pending",
                        "sent",
                        "completed",
                        "failed",
                        "reverted"
                      ]
                    },
                    "transactionHash": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{64}$"
                    }
                  },
                  "required": [
                    "messageId"
                  ],
                  "additionalProperties": false
                }
              },
              "token": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              },
              "amount": {
                "type": "string"
              },
              "decimals": {
                "type": "integer",
                "minimum": 0,
                "maximum": 36
              }
            },
            "required": [
              "chainId"
            ],
            "additionalProperties": false
          },
          "fieldMapping": {
            "type": "object",
            "properties": {
              "messageId": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "nonce": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "recipient": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "token": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "amount": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "decimals": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "status": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              }
            },
            "required": [
              "messageId"
            ],
            "additionalProperties": false
          },
          "fee": {
            "type": "object",
            "properties": {
              "amount": {
                "type": "string"
              },
              "decimals": {
                "type": "integer",
                "minimum": 0,
                "maximum": 36
              },
              "token": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              }
            },
            "required": [
              "amount"
            ],
            "additionalProperties": false
          },
          "conversion": {
            "type": "object",
            "properties": {
              "numerator": {
                "type": "string",
                "pattern": "^[1-9][0-9]{0,77}$"
              },
              "denominator": {
                "type": "string",
                "pattern": "^[1-9][0-9]{0,77}$"
              }
            },
            "required": [
              "numerator",
              "denominator"
            ],
            "additionalProperties": false
          },
          "expectedStatus": {
            "type": "string",
            "enum": [
              "settled",
              "pending",
              "failed"
            ]
          }
        },
        "required": [
          "source",
          "destination"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-operations__bridge-leg-consistency",
      "description": "Score bridge leg consistency. Group caller-supplied source and destination legs by message id. A message is consistent when both legs succeeded for the same amount. The recovery index is the hardest leg: a pending destination after a successful source scores lower than two matching successes. No chain is queried. Docs: https://www.brainiac.software/api/crypto-operations/bridge-leg-consistency",
      "parameters": {
        "type": "object",
        "properties": {
          "legs": {
            "minItems": 2,
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "message_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "source",
                    "destination"
                  ]
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failed",
                    "pending"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "message_id",
                "role",
                "status",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "legs"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-operations__bridge-partial-failure-audit": "0.05",
  "crypto-operations__bridge-leg-consistency": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-operations__bridge-partial-failure-audit": "crypto-operations/bridge-partial-failure-audit",
  "crypto-operations__bridge-leg-consistency": "crypto-operations/bridge-leg-consistency"
}


class BrainiacCryptoOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit bridge partial failure"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-operations group. "
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
