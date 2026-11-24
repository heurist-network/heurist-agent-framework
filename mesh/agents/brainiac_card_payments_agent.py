"""Auto-generated BRAINIAC Heurist Mesh agent for group `card-payments` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "card-payments__pan-check",
      "description": "Validate a card PAN (Luhn). Check card number length and Luhn check digit. Never echoes the full PAN; returns masked form and last4 only. Docs: https://www.brainiac.software/api/card-payments/pan-check",
      "parameters": {
        "type": "object",
        "properties": {
          "pan": {
            "type": "string",
            "minLength": 12,
            "maxLength": 32
          }
        },
        "required": [
          "pan"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "card-payments__pan-mask",
      "description": "Mask a PAN or redact PANs in text. PCI DSS display masking for a single PAN, or find and redact Luhn-valid PANs in free text. Docs: https://www.brainiac.software/api/card-payments/pan-mask",
      "parameters": {
        "type": "object",
        "properties": {
          "pan": {
            "type": "string",
            "minLength": 12,
            "maxLength": 32
          },
          "text": {
            "type": "string",
            "maxLength": 1048576
          },
          "binLength": {
            "default": 6,
            "anyOf": [
              {
                "type": "number",
                "const": 6
              },
              {
                "type": "number",
                "const": 8
              }
            ]
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "card-payments__interchange-cap-check",
      "description": "Check EU/US interchange fee caps. Compute regulated maximum interchange under EU IFR consumer caps or US Reg II debit caps and flag fees above the cap. Docs: https://www.brainiac.software/api/card-payments/interchange-cap-check",
      "parameters": {
        "type": "object",
        "properties": {
          "regime": {
            "type": "string",
            "enum": [
              "EU_IFR",
              "US_REG_II"
            ]
          },
          "cardType": {
            "type": "string",
            "enum": [
              "consumer_debit",
              "consumer_credit",
              "debit",
              "commercial"
            ]
          },
          "amount": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
          },
          "actualFee": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "regulatedIssuer": {
            "type": "boolean"
          },
          "fraudAdjustmentEligible": {
            "default": false,
            "type": "boolean"
          },
          "domesticCapOverride": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "regime",
          "cardType",
          "amount",
          "currency"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "card-payments__sca-exemption-evaluate",
      "description": "Evaluate PSD2 SCA exemptions. Decide which PSD2 RTS SCA exemptions may apply to a remote or contactless payment from caller-supplied facts. Docs: https://www.brainiac.software/api/card-payments/sca-exemption-evaluate",
      "parameters": {
        "type": "object",
        "properties": {
          "channel": {
            "type": "string",
            "enum": [
              "remote",
              "contactless_pos"
            ]
          },
          "instrument": {
            "type": "string",
            "enum": [
              "card",
              "credit_transfer"
            ]
          },
          "amountEur": {
            "type": "number",
            "minimum": 0
          },
          "sinceLastSca": {
            "default": {
              "cumulativeEur": 0,
              "count": 0
            },
            "type": "object",
            "properties": {
              "cumulativeEur": {
                "type": "number",
                "minimum": 0
              },
              "count": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            },
            "required": [
              "cumulativeEur",
              "count"
            ],
            "additionalProperties": false
          },
          "trustedBeneficiary": {
            "default": false,
            "type": "boolean"
          },
          "trustedBeneficiaryListChanging": {
            "default": false,
            "type": "boolean"
          },
          "recurringSameAmountSamePayee": {
            "default": false,
            "type": "boolean"
          },
          "firstInSeries": {
            "default": false,
            "type": "boolean"
          },
          "sameOwnerSameAspsp": {
            "default": false,
            "type": "boolean"
          },
          "tra": {
            "type": "object",
            "properties": {
              "fraudRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              },
              "fraudValue": {
                "type": "number",
                "minimum": 0
              },
              "totalValue": {
                "type": "number",
                "minimum": 0
              },
              "riskSignalsClear": {
                "default": true,
                "type": "boolean"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "channel",
          "instrument",
          "amountEur"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "card-payments__app-scam-reimbursement",
      "description": "UK APP scam reimbursement split. Calculate the UK mandatory APP scam reimbursement amount and 50:50 receiving-PSP contributions under PSR rules. Docs: https://www.brainiac.software/api/card-payments/app-scam-reimbursement",
      "parameters": {
        "type": "object",
        "properties": {
          "scheme": {
            "type": "string",
            "enum": [
              "FPS",
              "CHAPS"
            ]
          },
          "payments": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "receivingPsp": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "date",
                "amount",
                "receivingPsp"
              ],
              "additionalProperties": false
            }
          },
          "claimDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "excessApplied": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 10000
          },
          "vulnerable": {
            "default": false,
            "type": "boolean"
          },
          "exceptionsAsserted": {
            "default": [],
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "first_party_fraud",
                "gross_negligence"
              ]
            }
          }
        },
        "required": [
          "scheme",
          "payments",
          "claimDate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "card-payments__psd2-certificate-roles",
      "description": "Parse PSD2 eIDAS certificate roles. Parse a TPP QWAC/QSealC certificate for PSD2 roles, NCA and authorisation number. Does not verify the chain. Docs: https://www.brainiac.software/api/card-payments/psd2-certificate-roles",
      "parameters": {
        "type": "object",
        "properties": {
          "certificatePem": {
            "type": "string",
            "minLength": 32,
            "maxLength": 65536
          }
        },
        "required": [
          "certificatePem"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "card-payments__pan-check": "0.01",
  "card-payments__pan-mask": "0.01",
  "card-payments__interchange-cap-check": "0.02",
  "card-payments__sca-exemption-evaluate": "0.03",
  "card-payments__app-scam-reimbursement": "0.03",
  "card-payments__psd2-certificate-roles": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "card-payments__pan-check": "card-payments/pan-check",
  "card-payments__pan-mask": "card-payments/pan-mask",
  "card-payments__interchange-cap-check": "card-payments/interchange-cap-check",
  "card-payments__sca-exemption-evaluate": "card-payments/sca-exemption-evaluate",
  "card-payments__app-scam-reimbursement": "card-payments/app-scam-reimbursement",
  "card-payments__psd2-certificate-roles": "card-payments/psd2-certificate-roles"
}


class BrainiacCardPaymentsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — card-payments",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the card-payments catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "card-payments", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate a card PAN (Luhn)"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the card-payments group. "
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
