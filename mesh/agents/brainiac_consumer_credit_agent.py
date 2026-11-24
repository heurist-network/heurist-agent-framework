"""Auto-generated BRAINIAC Heurist Mesh agent for group `consumer-credit` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "consumer-credit__reg-z-apr",
      "description": "Regulation Z APR (Appendix J). Compute the US closed-end credit APR with the Reg Z Appendix J actuarial method and optional disclosure tolerance check. Docs: https://www.brainiac.software/api/consumer-credit/reg-z-apr",
      "parameters": {
        "type": "object",
        "properties": {
          "amountFinanced": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "advanceDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "advances": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "amount": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "amount",
                "date"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "anyOf": [
              {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "amount": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    "count": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 1200
                    },
                    "firstDate": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "frequency": {
                      "type": "string",
                      "enum": [
                        "monthly",
                        "semimonthly",
                        "weekly",
                        "biweekly",
                        "quarterly",
                        "semiannual",
                        "annual"
                      ]
                    }
                  },
                  "required": [
                    "amount",
                    "count",
                    "firstDate",
                    "frequency"
                  ],
                  "additionalProperties": false
                }
              },
              {
                "minItems": 1,
                "maxItems": 1200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "amount": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    "date": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    }
                  },
                  "required": [
                    "amount",
                    "date"
                  ],
                  "additionalProperties": false
                }
              }
            ]
          },
          "disclosedApr": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
          }
        },
        "required": [
          "payments"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "consumer-credit__uk-early-settlement",
      "description": "UK early settlement rebate. Compute the statutory minimum early-settlement rebate and settlement figure under the Consumer Credit (Early Settlement) Regulations 2004. Docs: https://www.brainiac.software/api/consumer-credit/uk-early-settlement",
      "parameters": {
        "type": "object",
        "properties": {
          "advances": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "amount": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "amount",
                "date"
              ],
              "additionalProperties": false
            }
          },
          "repayments": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "amount": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  },
                  "count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1200
                  },
                  "firstDate": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  },
                  "frequency": {
                    "type": "string",
                    "enum": [
                      "monthly",
                      "semimonthly",
                      "weekly",
                      "biweekly",
                      "quarterly",
                      "semiannual",
                      "annual"
                    ]
                  }
                },
                "required": [
                  "amount",
                  "count",
                  "firstDate",
                  "frequency"
                ],
                "additionalProperties": false
              },
              {
                "minItems": 1,
                "maxItems": 1200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "amount": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    "date": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    }
                  },
                  "required": [
                    "amount",
                    "date"
                  ],
                  "additionalProperties": false
                }
              }
            ]
          },
          "apr": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 10
          },
          "noticeReceivedDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "settlementDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "lastPaidInstalment": {
            "type": "integer",
            "minimum": 0,
            "maximum": 1200
          },
          "deferral": {
            "default": "none",
            "type": "string",
            "enum": [
              "none",
              "one_month",
              "30_days"
            ]
          },
          "periodBasis": {
            "default": "month",
            "type": "string",
            "enum": [
              "month"
            ]
          },
          "treatLateAsOnTime": {
            "default": true,
            "type": "boolean"
          },
          "partialSettlement": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "advances",
          "repayments",
          "apr"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "consumer-credit__apy-calculate",
      "description": "Regulation DD APY. Compute annual percentage yield for US deposit disclosures under Reg DD Appendix A, including stepped and tiered rates. Docs: https://www.brainiac.software/api/consumer-credit/apy-calculate",
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
      "name": "consumer-credit__pmi-termination-dates",
      "description": "HPA PMI termination dates. Compute Homeowners Protection Act cancellation, automatic termination and final termination dates from the amortization schedule. Docs: https://www.brainiac.software/api/consumer-credit/pmi-termination-dates",
      "parameters": {
        "type": "object",
        "properties": {
          "loanAmount": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "annualRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "termMonths": {
            "type": "integer",
            "minimum": 12,
            "maximum": 600
          },
          "firstPaymentDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "salesPrice": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "appraisedValue": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "purpose": {
            "type": "string",
            "enum": [
              "purchase",
              "refinance"
            ]
          },
          "monthlyPayment": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ]
          },
          "currentSchedule": {
            "maxItems": 600,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "paymentNumber": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "balance": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "paymentNumber",
                "balance"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "loanAmount",
          "annualRate",
          "termMonths",
          "firstPaymentDate",
          "appraisedValue",
          "purpose"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "consumer-credit__reg-f-call-frequency",
      "description": "Regulation F call-frequency check. Check a debt-collector call log against the Reg F 7-in-7 presumption per debt. Docs: https://www.brainiac.software/api/consumer-credit/reg-f-call-frequency",
      "parameters": {
        "type": "object",
        "properties": {
          "debtId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "calls": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 64
                },
                "connected": {
                  "default": false,
                  "type": "boolean"
                },
                "excluded": {
                  "default": false,
                  "type": "boolean"
                },
                "consentGivenAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 64
                }
              },
              "required": [
                "at"
              ],
              "additionalProperties": false
            }
          },
          "timezone": {
            "default": "America/New_York",
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          }
        },
        "required": [
          "debtId",
          "calls"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "consumer-credit__reg-z-apr": "0.04",
  "consumer-credit__uk-early-settlement": "0.04",
  "consumer-credit__apy-calculate": "0.02",
  "consumer-credit__pmi-termination-dates": "0.03",
  "consumer-credit__reg-f-call-frequency": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "consumer-credit__reg-z-apr": "consumer-credit/reg-z-apr",
  "consumer-credit__uk-early-settlement": "consumer-credit/uk-early-settlement",
  "consumer-credit__apy-calculate": "consumer-credit/apy-calculate",
  "consumer-credit__pmi-termination-dates": "consumer-credit/pmi-termination-dates",
  "consumer-credit__reg-f-call-frequency": "consumer-credit/reg-f-call-frequency"
}


class BrainiacConsumerCreditAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — consumer-credit",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the consumer-credit catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "consumer-credit", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Regulation Z APR (Appendix J)"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the consumer-credit group. "
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
