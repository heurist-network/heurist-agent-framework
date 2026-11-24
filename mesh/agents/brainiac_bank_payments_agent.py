"""Auto-generated BRAINIAC Heurist Mesh agent for group `bank-payments` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "bank-payments__uk-modulus-check",
      "description": "UK sort code + account modulus check. Check whether a UK sort code and account number pair can be valid using Vocalink modulus weights (valacdos/scsubtab) and exceptions 1–14. Docs: https://www.brainiac.software/api/bank-payments/uk-modulus-check",
      "parameters": {
        "type": "object",
        "properties": {
          "sortCode": {
            "type": "string",
            "minLength": 6,
            "maxLength": 12
          },
          "accountNumber": {
            "type": "string",
            "minLength": 6,
            "maxLength": 14
          }
        },
        "required": [
          "sortCode",
          "accountNumber"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__sepa-creditor-id-validate",
      "description": "Validate a SEPA Creditor Identifier. Parse a SEPA Direct Debit Creditor Identifier and recompute ISO 7064 Mod 97-10 check digits (business code excluded). Docs: https://www.brainiac.software/api/bank-payments/sepa-creditor-id-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "creditorId": {
            "type": "string",
            "minLength": 8,
            "maxLength": 40
          }
        },
        "required": [
          "creditorId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__iban-from-bban",
      "description": "Build an IBAN from a BBAN. Compute ISO 13616 check digits for a country code and domestic BBAN, then validate the resulting IBAN structure. Docs: https://www.brainiac.software/api/bank-payments/iban-from-bban",
      "parameters": {
        "type": "object",
        "properties": {
          "country": {
            "type": "string",
            "pattern": "^[A-Za-z]{2}$"
          },
          "bban": {
            "type": "string",
            "minLength": 1,
            "maxLength": 34
          }
        },
        "required": [
          "country",
          "bban"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__uetr-validate",
      "description": "Validate or generate a UETR. Validate an ISO 20022 UETR as a UUID version 4, or generate one or more UETRs with crypto.randomUUID(). Docs: https://www.brainiac.software/api/bank-payments/uetr-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "uetr": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "generate": {
            "type": "boolean"
          },
          "count": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__postal-address-check",
      "description": "CBPR+ postal address format check. Classify an ISO 20022 PostalAddress as structured, hybrid or unstructured and check Swift CBPR+ town/country/AdrLine rules. Docs: https://www.brainiac.software/api/bank-payments/postal-address-check",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "object",
            "properties": {
              "Dept": {
                "type": "string",
                "maxLength": 70
              },
              "SubDept": {
                "type": "string",
                "maxLength": 70
              },
              "StrtNm": {
                "type": "string",
                "maxLength": 70
              },
              "BldgNb": {
                "type": "string",
                "maxLength": 16
              },
              "BldgNm": {
                "type": "string",
                "maxLength": 35
              },
              "Flr": {
                "type": "string",
                "maxLength": 70
              },
              "PstBx": {
                "type": "string",
                "maxLength": 16
              },
              "Room": {
                "type": "string",
                "maxLength": 70
              },
              "PstCd": {
                "type": "string",
                "maxLength": 16
              },
              "TwnNm": {
                "type": "string",
                "maxLength": 35
              },
              "TwnLctnNm": {
                "type": "string",
                "maxLength": 35
              },
              "DstrctNm": {
                "type": "string",
                "maxLength": 35
              },
              "CtrySubDvsn": {
                "type": "string",
                "maxLength": 35
              },
              "Ctry": {
                "type": "string",
                "pattern": "^[A-Za-z]{2}$"
              },
              "AdrLine": {
                "maxItems": 7,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 70
                }
              }
            },
            "additionalProperties": false
          },
          "role": {
            "default": "party",
            "type": "string",
            "enum": [
              "party",
              "agent"
            ]
          },
          "agentHasBic": {
            "type": "boolean"
          },
          "messageType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          }
        },
        "required": [
          "address"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__nacha-file-build",
      "description": "Build a NACHA ACH file. Generate a 94-character NACHA ACH file (PPD/CCD/WEB/TEL) with batch hashes, totals and blocking-factor padding from JSON entries. Docs: https://www.brainiac.software/api/bank-payments/nacha-file-build",
      "parameters": {
        "type": "object",
        "properties": {
          "immediateDestination": {
            "type": "string",
            "minLength": 9,
            "maxLength": 10
          },
          "immediateOrigin": {
            "type": "string",
            "minLength": 9,
            "maxLength": 10
          },
          "destinationName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 23
          },
          "originName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 23
          },
          "fileCreationDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "fileCreationTime": {
            "type": "string",
            "pattern": "^\\d{2}:\\d{2}$"
          },
          "fileIdModifier": {
            "default": "A",
            "type": "string",
            "pattern": "^[A-Z0-9]$"
          },
          "batches": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "companyName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 16
                },
                "companyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 10
                },
                "secCode": {
                  "type": "string",
                  "enum": [
                    "PPD",
                    "CCD",
                    "WEB",
                    "TEL"
                  ]
                },
                "entryDescription": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 10
                },
                "effectiveEntryDate": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "odfiRouting": {
                  "type": "string",
                  "pattern": "^\\d{8}$"
                },
                "companyDiscretionaryData": {
                  "type": "string",
                  "maxLength": 20
                },
                "descriptiveDate": {
                  "type": "string",
                  "maxLength": 6
                },
                "entries": {
                  "minItems": 1,
                  "maxItems": 100000,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "transactionCode": {
                        "type": "string",
                        "enum": [
                          "22",
                          "23",
                          "27",
                          "28",
                          "32",
                          "33",
                          "37",
                          "38"
                        ]
                      },
                      "rdfiRouting": {
                        "type": "string",
                        "minLength": 8,
                        "maxLength": 12
                      },
                      "accountNumber": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 17
                      },
                      "amount": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9999999999
                      },
                      "individualId": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 15
                      },
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 22
                      },
                      "paymentTypeCode": {
                        "type": "string",
                        "enum": [
                          "R",
                          "S"
                        ]
                      },
                      "addenda": {
                        "type": "string",
                        "maxLength": 80
                      }
                    },
                    "required": [
                      "transactionCode",
                      "rdfiRouting",
                      "accountNumber",
                      "amount",
                      "individualId",
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "companyName",
                "companyId",
                "secCode",
                "entryDescription",
                "effectiveEntryDate",
                "odfiRouting",
                "entries"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "immediateDestination",
          "immediateOrigin",
          "destinationName",
          "originName",
          "fileCreationDate",
          "fileCreationTime",
          "batches"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__nacha-file-validate",
      "description": "Validate a NACHA ACH file. Validate NACHA record order, lengths, ABA checksums, batch/file hashes and totals, reporting every structural error by line. Docs: https://www.brainiac.software/api/bank-payments/nacha-file-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "file": {
            "type": "string",
            "minLength": 94,
            "maxLength": 5000000
          },
          "maxErrors": {
            "default": 200,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          }
        },
        "required": [
          "file"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "bank-payments__camt053-parse",
      "description": "Parse camt.052/053/054 statements. Parse an ISO 20022 bank-to-customer statement or report into normalised JSON with balance reconciliation checks. Docs: https://www.brainiac.software/api/bank-payments/camt053-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "xml": {
            "type": "string",
            "minLength": 20,
            "maxLength": 10000000
          },
          "includeRaw": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "xml"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "bank-payments__uk-modulus-check": "0.02",
  "bank-payments__sepa-creditor-id-validate": "0.01",
  "bank-payments__iban-from-bban": "0.01",
  "bank-payments__uetr-validate": "0.01",
  "bank-payments__postal-address-check": "0.02",
  "bank-payments__nacha-file-build": "0.04",
  "bank-payments__nacha-file-validate": "0.03",
  "bank-payments__camt053-parse": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "bank-payments__uk-modulus-check": "bank-payments/uk-modulus-check",
  "bank-payments__sepa-creditor-id-validate": "bank-payments/sepa-creditor-id-validate",
  "bank-payments__iban-from-bban": "bank-payments/iban-from-bban",
  "bank-payments__uetr-validate": "bank-payments/uetr-validate",
  "bank-payments__postal-address-check": "bank-payments/postal-address-check",
  "bank-payments__nacha-file-build": "bank-payments/nacha-file-build",
  "bank-payments__nacha-file-validate": "bank-payments/nacha-file-validate",
  "bank-payments__camt053-parse": "bank-payments/camt053-parse"
}


class BrainiacBankPaymentsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — bank-payments",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the bank-payments catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "bank-payments", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["UK sort code + account modulus check"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the bank-payments group. "
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
