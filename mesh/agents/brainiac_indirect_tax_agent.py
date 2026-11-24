"""Auto-generated BRAINIAC Heurist Mesh agent for group `indirect-tax` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "indirect-tax__eu-oss-threshold-check",
      "description": "EU OSS €10,000 threshold place-of-supply check. Decide whether an EU-established supplier's B2C cross-border TBE services and distance sales stay taxed at home or switch to the customer's Member State under the EU-wide €10,000 threshold. Docs: https://www.brainiac.software/api/indirect-tax/eu-oss-threshold-check",
      "parameters": {
        "type": "object",
        "properties": {
          "supplierCountry": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
          },
          "establishedInOtherMemberStates": {
            "type": "boolean"
          },
          "previousYearTotalEurCents": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "sales": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "customerCountry": {
                  "type": "string",
                  "minLength": 2,
                  "maxLength": 2
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "tbe_service",
                    "distance_sale_goods"
                  ]
                },
                "netEurCents": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "date",
                "customerCountry",
                "kind",
                "netEurCents"
              ],
              "additionalProperties": false
            }
          },
          "optedForDestination": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "supplierCountry",
          "establishedInOtherMemberStates",
          "previousYearTotalEurCents",
          "sales"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "indirect-tax__canada-gst-hst-pst",
      "description": "Canada GST/HST and PST rate and tax amount. Look up GST/HST (and PST where the CRA table lists one) for a province and date, and compute tax on an amount in cents. Docs: https://www.brainiac.software/api/indirect-tax/canada-gst-hst-pst",
      "parameters": {
        "type": "object",
        "properties": {
          "province": {
            "type": "string",
            "enum": [
              "AB",
              "BC",
              "MB",
              "NB",
              "NL",
              "NT",
              "NS",
              "NU",
              "ON",
              "QC",
              "PE",
              "SK",
              "YT"
            ]
          },
          "date": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "amountCents": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "supply": {
            "default": "taxable",
            "type": "string",
            "enum": [
              "taxable",
              "zero_rated"
            ]
          }
        },
        "required": [
          "province",
          "date",
          "amountCents"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "indirect-tax__australia-nz-gst",
      "description": "Australia and New Zealand GST registration threshold. Test AU/NZ GST registration thresholds from monthly turnover and optionally extract GST from an inclusive or exclusive price. Docs: https://www.brainiac.software/api/indirect-tax/australia-nz-gst",
      "parameters": {
        "type": "object",
        "properties": {
          "country": {
            "type": "string",
            "enum": [
              "AU",
              "NZ"
            ]
          },
          "nonProfit": {
            "default": false,
            "type": "boolean"
          },
          "monthlyTurnoverCents": {
            "minItems": 12,
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "projectedNextMonthsCents": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "taxiOrRideSourcing": {
            "default": false,
            "type": "boolean"
          },
          "priceCents": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "priceIncludesGst": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "country",
          "monthlyTurnoverCents",
          "projectedNextMonthsCents"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "indirect-tax__uk-vat-flat-rate",
      "description": "UK VAT Flat Rate Scheme percentage and VAT due. Return the HMRC Flat Rate Scheme percentage for a business type and date (including limited-cost and first-year discount) and compute VAT due on VAT-inclusive turnover. Docs: https://www.brainiac.software/api/indirect-tax/uk-vat-flat-rate",
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
      "name": "indirect-tax__vat-invoice-requirements",
      "description": "UK VAT invoice content requirements check. Check a supplied invoice against HMRC Notice 700/21 full and simplified VAT invoice content rules and recompute arithmetic. Docs: https://www.brainiac.software/api/indirect-tax/vat-invoice-requirements",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "number": {
                "type": "string",
                "minLength": 1,
                "maxLength": 64
              },
              "timeOfSupply": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "issueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "supplier": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 500
                  },
                  "address": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 1000
                  },
                  "vatNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 32
                  }
                },
                "additionalProperties": false
              },
              "customer": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 500
                  },
                  "address": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 1000
                  },
                  "vatNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 32
                  }
                },
                "additionalProperties": false
              },
              "lines": {
                "default": [],
                "maxItems": 500,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 500
                    },
                    "quantity": {
                      "type": "number"
                    },
                    "unitPricePence": {
                      "type": "integer",
                      "minimum": -9007199254740991,
                      "maximum": 9007199254740991
                    },
                    "vatRate": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1
                    },
                    "netPence": {
                      "type": "integer",
                      "minimum": -9007199254740991,
                      "maximum": 9007199254740991
                    }
                  },
                  "additionalProperties": false
                }
              },
              "cashDiscountRate": {
                "anyOf": [
                  {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "totalNetPence": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "totalVatPence": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "totalGrossPence": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "currency": {
                "type": "string",
                "minLength": 1,
                "maxLength": 8
              }
            },
            "additionalProperties": false
          },
          "supplierIsRetailer": {
            "default": false,
            "type": "boolean"
          },
          "type": {
            "default": "auto",
            "type": "string",
            "enum": [
              "full",
              "simplified",
              "auto"
            ]
          }
        },
        "required": [
          "invoice"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "indirect-tax__uk-mtd-itsa-obligations",
      "description": "UK MTD for Income Tax mandate and quarterly deadlines. Tell a sole trader or landlord when Making Tax Digital for Income Tax applies from qualifying income, and list quarterly update deadlines. Docs: https://www.brainiac.software/api/indirect-tax/uk-mtd-itsa-obligations",
      "parameters": {
        "type": "object",
        "properties": {
          "entity": {
            "type": "string",
            "enum": [
              "sole_trader",
              "landlord",
              "partnership"
            ]
          },
          "qualifyingIncomePence": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}$"
            },
            "additionalProperties": {
              "anyOf": [
                {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "updatePeriods": {
            "default": "standard",
            "type": "string",
            "enum": [
              "standard",
              "calendar"
            ]
          },
          "taxYear": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}$"
          }
        },
        "required": [
          "entity",
          "qualifyingIncomePence",
          "taxYear"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "indirect-tax__us-use-tax-accrual",
      "description": "US use-tax accrual from caller rates. Compute use tax owed on purchases where the vendor charged less than the caller-supplied combined rate, with per-jurisdiction totals. Docs: https://www.brainiac.software/api/indirect-tax/us-use-tax-accrual",
      "parameters": {
        "type": "object",
        "properties": {
          "purchases": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "shipToJurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "taxableAmountCents": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "salesTaxChargedCents": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "exempt": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "shipToJurisdiction",
                "taxableAmountCents",
                "salesTaxChargedCents"
              ],
              "additionalProperties": false
            }
          },
          "rates": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            },
            "additionalProperties": {
              "type": "number",
              "minimum": 0,
              "maximum": 0.2
            }
          }
        },
        "required": [
          "purchases",
          "rates"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "indirect-tax__eu-oss-threshold-check": "0.03",
  "indirect-tax__canada-gst-hst-pst": "0.02",
  "indirect-tax__australia-nz-gst": "0.02",
  "indirect-tax__uk-vat-flat-rate": "0.02",
  "indirect-tax__vat-invoice-requirements": "0.03",
  "indirect-tax__uk-mtd-itsa-obligations": "0.02",
  "indirect-tax__us-use-tax-accrual": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "indirect-tax__eu-oss-threshold-check": "indirect-tax/eu-oss-threshold-check",
  "indirect-tax__canada-gst-hst-pst": "indirect-tax/canada-gst-hst-pst",
  "indirect-tax__australia-nz-gst": "indirect-tax/australia-nz-gst",
  "indirect-tax__uk-vat-flat-rate": "indirect-tax/uk-vat-flat-rate",
  "indirect-tax__vat-invoice-requirements": "indirect-tax/vat-invoice-requirements",
  "indirect-tax__uk-mtd-itsa-obligations": "indirect-tax/uk-mtd-itsa-obligations",
  "indirect-tax__us-use-tax-accrual": "indirect-tax/us-use-tax-accrual"
}


class BrainiacIndirectTaxAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — indirect-tax",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the indirect-tax catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "indirect-tax", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["EU OSS €10,000 threshold place-of-supply check"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the indirect-tax group. "
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
