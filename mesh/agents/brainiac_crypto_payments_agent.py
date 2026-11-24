"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-payments` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-payments__stablecoin-payment-reconcile",
      "description": "Reconcile stablecoin payment. Reconcile caller-supplied stablecoin payment records against invoices. Compares amounts, token, recipient, and chain ID, and reports underpayments, overpayments, duplicate transaction hashes, and payments that are not linked to an invoice. reconciliation_status is matched, underpaid, overpaid, duplicate, mismatched, or incomplete. Amounts are integers in smallest units. No chain is queried, and a transaction hash is not treated as confirmation that funds arrived. Docs: https://www.brainiac.software/api/crypto-payments/stablecoin-payment-reconcile",
      "parameters": {
        "type": "object",
        "properties": {
          "invoices": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
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
                },
                "chainId": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 2147483647
                },
                "recipient": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "tolerance": {
                  "type": "string"
                }
              },
              "required": [
                "id",
                "amount",
                "decimals",
                "token",
                "chainId",
                "recipient"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
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
                },
                "chainId": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 2147483647
                },
                "recipient": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "transactionHash": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{64}$"
                },
                "timestamp": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                }
              },
              "required": [
                "amount",
                "decimals",
                "token",
                "chainId",
                "recipient"
              ],
              "additionalProperties": false
            }
          },
          "rules": {
            "type": "object",
            "properties": {
              "allowPartial": {
                "type": "boolean"
              },
              "tolerance": {
                "type": "string"
              },
              "associateUnlabeledPayments": {
                "type": "string",
                "enum": [
                  "none",
                  "single_invoice"
                ]
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "invoices",
          "payments"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-payments__invoice-match-score",
      "description": "Score invoice payment match. Match caller-supplied payments to invoice amounts, due dates, and fee rates in basis points. Accuracy gives 60 points to the amount, 20 to paying on time, and 20 to the fee. The discrepancy is the invoice total minus the linked payments. No chain is queried. Docs: https://www.brainiac.software/api/crypto-payments/invoice-match-score",
      "parameters": {
        "type": "object",
        "properties": {
          "invoices": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "due_on": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "fee_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "required": [
                "id",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "invoice_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "paid_on": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "fee": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "invoice_id",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "invoices",
          "payments"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-payments__stablecoin-payment-reconcile": "0.05",
  "crypto-payments__invoice-match-score": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-payments__stablecoin-payment-reconcile": "crypto-payments/stablecoin-payment-reconcile",
  "crypto-payments__invoice-match-score": "crypto-payments/invoice-match-score"
}


class BrainiacCryptoPaymentsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-payments",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-payments catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-payments", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Reconcile stablecoin payment"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-payments group. "
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
