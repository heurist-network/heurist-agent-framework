"""Auto-generated BRAINIAC Heurist Mesh agent for group `ecommerce-profitability` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "ecommerce-profitability__unit-economics",
      "description": "Per-unit contribution margin and break-even. Compute landed cost, total cost per unit, contribution margin, ROI, break-even price and break-even ACoS from caller-supplied product costs and marketplace fees or fee rates. Docs: https://www.brainiac.software/api/ecommerce-profitability/unit-economics",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "pricePerUnit": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "costs": {
            "type": "object",
            "properties": {
              "product": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "inboundFreight": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "duty": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "packaging": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "marketplaceFees": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "fulfilmentFees": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "storage": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              },
              "other": {
                "default": 0,
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            },
            "required": [
              "product",
              "inboundFreight",
              "duty",
              "packaging",
              "fulfilmentFees",
              "storage"
            ],
            "additionalProperties": false
          },
          "marketplaceFeeRate": {
            "type": "number",
            "minimum": 0,
            "exclusiveMaximum": 1
          },
          "returnRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "returnLossPerUnit": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "salesTaxIncluded": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "currency",
          "pricePerUnit",
          "costs",
          "returnRate",
          "returnLossPerUnit"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__ppc-report-analyze",
      "description": "Analyse a sponsored-ads search-term report. Aggregate ACoS, ROAS, TACoS, CTR and CVR for a search-term report and flag negate, promote and insufficient-data candidates from caller rules. Docs: https://www.brainiac.software/api/ecommerce-profitability/ppc-report-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "rows": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "campaign": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "adGroup": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "searchTerm": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "matchType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "clicks": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "spend": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "orders": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sales": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "campaign",
                "adGroup",
                "searchTerm",
                "matchType",
                "impressions",
                "clicks",
                "spend",
                "orders",
                "sales"
              ],
              "additionalProperties": false
            }
          },
          "totalSales": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "rules": {
            "type": "object",
            "properties": {
              "targetAcos": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              },
              "minClicksNegate": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "minOrdersPromote": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              }
            },
            "required": [
              "targetAcos",
              "minClicksNegate",
              "minOrdersPromote"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "currency",
          "rows",
          "totalSales",
          "rules"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__listing-keyword-coverage",
      "description": "Check listing keyword coverage and length limits. Token-match caller keywords against title, bullets, description and backend terms, including simple plurals, and check caller-supplied title and backend length limits. Docs: https://www.brainiac.software/api/ecommerce-profitability/listing-keyword-coverage",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "maxLength": 2000
          },
          "bullets": {
            "default": [],
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "description": {
            "default": "",
            "type": "string",
            "maxLength": 20000
          },
          "backendTerms": {
            "default": "",
            "type": "string",
            "maxLength": 2000
          },
          "keywords": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "limits": {
            "type": "object",
            "properties": {
              "titleChars": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 10000
              },
              "backendBytes": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 10000
              }
            },
            "required": [
              "titleChars",
              "backendBytes"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "title",
          "keywords",
          "limits"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__landed-cost-import",
      "description": "Allocate import costs to SKU landed cost. Allocate shipment freight and insurance by value, weight or volume, compute CIF or FOB customs value, duty and import VAT from caller rates, and return per-unit landed cost. Docs: https://www.brainiac.software/api/ecommerce-profitability/landed-cost-import",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "lines": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "units": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 10000000
                },
                "unitCost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "weightKg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "volumeM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "dutyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "sku",
                "units",
                "unitCost",
                "weightKg",
                "volumeM3",
                "dutyRate"
              ],
              "additionalProperties": false
            }
          },
          "freight": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "insurance": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "allocation": {
            "type": "string",
            "enum": [
              "value",
              "weight",
              "volume"
            ]
          },
          "dutyBasis": {
            "type": "string",
            "enum": [
              "CIF",
              "FOB"
            ]
          },
          "importVatRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "vatRecoverable": {
            "type": "boolean"
          }
        },
        "required": [
          "currency",
          "lines",
          "freight",
          "insurance",
          "allocation",
          "dutyBasis",
          "importVatRate",
          "vatRecoverable"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__price-elasticity-estimate",
      "description": "Estimate own-price elasticity from history. OLS of ln(units) on ln(price) with optional week or month seasonal dummies, classical standard errors and a 95% t interval from caller price/quantity history. Docs: https://www.brainiac.software/api/ecommerce-profitability/price-elasticity-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "observations": {
            "minItems": 12,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "price": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "units": {
                  "type": "number",
                  "minimum": 0
                },
                "promo": {
                  "type": "boolean"
                }
              },
              "required": [
                "date",
                "price",
                "units"
              ],
              "additionalProperties": false
            }
          },
          "seasonality": {
            "default": "none",
            "type": "string",
            "enum": [
              "none",
              "week_of_year",
              "month"
            ]
          },
          "promoFlagField": {
            "anyOf": [
              {
                "type": "string",
                "const": "promo"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "observations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__competitive-price-index",
      "description": "Price index and rank vs competitors. Compare our landed price (price + shipping) with in-stock competitor landed prices to return median index, min and rank. Docs: https://www.brainiac.software/api/ecommerce-profitability/competitive-price-index",
      "parameters": {
        "type": "object",
        "properties": {
          "ourPrice": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "ourShipping": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "competitors": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "price": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "shipping": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "inStock": {
                  "type": "boolean"
                }
              },
              "required": [
                "name",
                "price",
                "inStock"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "ourPrice",
          "competitors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__bundle-pricing",
      "description": "Compare bundle margin with separate sales. Compute separate and bundle margins, discount depth, margin delta and the break-even bundle price from caller component and bundle fees. Docs: https://www.brainiac.software/api/ecommerce-profitability/bundle-pricing",
      "parameters": {
        "type": "object",
        "properties": {
          "components": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "price": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "unitCost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "fulfilmentFee": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "sku",
                "price",
                "unitCost",
                "feeRate",
                "fulfilmentFee"
              ],
              "additionalProperties": false
            }
          },
          "bundle": {
            "type": "object",
            "properties": {
              "price": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 9007199254740991
              },
              "feeRate": {
                "type": "number",
                "minimum": 0,
                "exclusiveMaximum": 1
              },
              "fulfilmentFee": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            },
            "required": [
              "price",
              "feeRate",
              "fulfilmentFee"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "components",
          "bundle"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__packaging-optimize",
      "description": "Pick the box that minimises billable weight. Try caller boxes and orientations with padding, compute dimensional and billable weight from a caller divisor, and pick the best by billable weight or box cost. Docs: https://www.brainiac.software/api/ecommerce-profitability/packaging-optimize",
      "parameters": {
        "type": "object",
        "properties": {
          "items": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "l": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "w": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "h": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "weightG": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "qty": {
                  "default": 1,
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 1000
                }
              },
              "required": [
                "l",
                "w",
                "h",
                "weightG"
              ],
              "additionalProperties": false
            }
          },
          "boxes": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "l": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "w": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "h": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "tareG": {
                  "type": "number",
                  "minimum": 0
                },
                "cost": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "l",
                "w",
                "h",
                "tareG"
              ],
              "additionalProperties": false
            }
          },
          "paddingCm": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "dimDivisor": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "objective": {
            "default": "billable_weight",
            "type": "string",
            "enum": [
              "billable_weight",
              "box_cost"
            ]
          }
        },
        "required": [
          "items",
          "boxes",
          "dimDivisor"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-profitability__settlement-tax-reconcile",
      "description": "Reconcile marketplace settlement tax lines. Match order tax charged to settlement tax, marketplace-facilitator tax and refund lines within a tolerance and total seller vs marketplace collected tax. Docs: https://www.brainiac.software/api/ecommerce-profitability/settlement-tax-reconcile",
      "parameters": {
        "type": "object",
        "properties": {
          "orders": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "taxCharged": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "orderId",
                "taxCharged"
              ],
              "additionalProperties": false
            }
          },
          "settlementLines": {
            "default": [],
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "tax",
                    "marketplace_facilitator_tax",
                    "refund_tax"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "orderId",
                "type",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "tolerance": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "orders"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "ecommerce-profitability__unit-economics": "0.03",
  "ecommerce-profitability__ppc-report-analyze": "0.04",
  "ecommerce-profitability__listing-keyword-coverage": "0.02",
  "ecommerce-profitability__landed-cost-import": "0.04",
  "ecommerce-profitability__price-elasticity-estimate": "0.04",
  "ecommerce-profitability__competitive-price-index": "0.02",
  "ecommerce-profitability__bundle-pricing": "0.02",
  "ecommerce-profitability__packaging-optimize": "0.03",
  "ecommerce-profitability__settlement-tax-reconcile": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "ecommerce-profitability__unit-economics": "ecommerce-profitability/unit-economics",
  "ecommerce-profitability__ppc-report-analyze": "ecommerce-profitability/ppc-report-analyze",
  "ecommerce-profitability__listing-keyword-coverage": "ecommerce-profitability/listing-keyword-coverage",
  "ecommerce-profitability__landed-cost-import": "ecommerce-profitability/landed-cost-import",
  "ecommerce-profitability__price-elasticity-estimate": "ecommerce-profitability/price-elasticity-estimate",
  "ecommerce-profitability__competitive-price-index": "ecommerce-profitability/competitive-price-index",
  "ecommerce-profitability__bundle-pricing": "ecommerce-profitability/bundle-pricing",
  "ecommerce-profitability__packaging-optimize": "ecommerce-profitability/packaging-optimize",
  "ecommerce-profitability__settlement-tax-reconcile": "ecommerce-profitability/settlement-tax-reconcile"
}


class BrainiacEcommerceProfitabilityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — ecommerce-profitability",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the ecommerce-profitability catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "ecommerce-profitability", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Per-unit contribution margin and break-even"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the ecommerce-profitability group. "
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
