"""Auto-generated BRAINIAC Heurist Mesh agent for group `equity-analytics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "equity-analytics__financial-ratios",
      "description": "Compute standard financial ratios. Profitability, liquidity, leverage, efficiency and valuation ratios from caller-supplied statements and an optional price. Missing fields yield null metrics; division by zero is reported. Docs: https://www.brainiac.software/api/equity-analytics/financial-ratios",
      "parameters": {
        "type": "object",
        "properties": {
          "statements": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "period": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "revenue": {
                  "type": "number"
                },
                "cogs": {
                  "type": "number"
                },
                "sga": {
                  "type": "number"
                },
                "depreciation": {
                  "type": "number"
                },
                "ebit": {
                  "type": "number"
                },
                "interestExpense": {
                  "type": "number"
                },
                "netIncome": {
                  "type": "number"
                },
                "cfo": {
                  "type": "number"
                },
                "capex": {
                  "type": "number"
                },
                "totalAssets": {
                  "type": "number"
                },
                "currentAssets": {
                  "type": "number"
                },
                "currentLiabilities": {
                  "type": "number"
                },
                "totalLiabilities": {
                  "type": "number"
                },
                "longTermDebt": {
                  "type": "number"
                },
                "receivables": {
                  "type": "number"
                },
                "inventory": {
                  "type": "number"
                },
                "ppeNet": {
                  "type": "number"
                },
                "retainedEarnings": {
                  "type": "number"
                },
                "sharesOutstanding": {
                  "type": "number"
                },
                "dividendsPaid": {
                  "type": "number"
                },
                "equity": {
                  "type": "number"
                },
                "cash": {
                  "type": "number"
                },
                "securities": {
                  "type": "number"
                },
                "priorTotalAssets": {
                  "type": "number"
                },
                "ebt": {
                  "type": "number"
                }
              },
              "required": [
                "period"
              ],
              "additionalProperties": false
            }
          },
          "price": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "unit": {
            "default": "USD thousands",
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          }
        },
        "required": [
          "statements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__dcf-valuation",
      "description": "Two-stage discounted cash flow. Discount explicit free cash flows and a Gordon or exit-multiple terminal value to enterprise and equity value per share, with a discount-rate and growth sensitivity grid. Docs: https://www.brainiac.software/api/equity-analytics/dcf-valuation",
      "parameters": {
        "type": "object",
        "properties": {
          "fcf": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "discountRate": {
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "terminal": {
            "type": "object",
            "properties": {
              "method": {
                "type": "string",
                "enum": [
                  "gordon",
                  "exit_multiple"
                ]
              },
              "growth": {
                "type": "number",
                "exclusiveMinimum": -1,
                "exclusiveMaximum": 1
              },
              "multiple": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "metric": {
                "type": "number"
              }
            },
            "required": [
              "method"
            ],
            "additionalProperties": false
          },
          "netDebt": {
            "default": 0,
            "type": "number"
          },
          "sharesOutstanding": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "midYear": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "fcf",
          "discountRate",
          "terminal",
          "sharesOutstanding"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__wacc-calculate",
      "description": "Weighted average cost of capital. CAPM cost of equity and after-tax cost of debt combined into WACC from supplied equity and debt values. Docs: https://www.brainiac.software/api/equity-analytics/wacc-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "equityValue": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "debtValue": {
            "type": "number",
            "minimum": 0
          },
          "riskFree": {
            "type": "number"
          },
          "beta": {
            "type": "number"
          },
          "equityRiskPremium": {
            "type": "number"
          },
          "costOfDebt": {
            "type": "number"
          },
          "taxRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "sizePremium": {
            "default": 0,
            "type": "number"
          }
        },
        "required": [
          "equityValue",
          "debtValue",
          "riskFree",
          "beta",
          "equityRiskPremium",
          "costOfDebt",
          "taxRate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__beta-regression",
      "description": "OLS equity beta vs a benchmark. Align asset and benchmark closes, compute simple returns at daily, weekly or monthly frequency, and return OLS beta, alpha, R², standard error and optional Blume-adjusted beta. Docs: https://www.brainiac.software/api/equity-analytics/beta-regression",
      "parameters": {
        "type": "object",
        "properties": {
          "assetPrices": {
            "minItems": 21,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "close": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "date",
                "close"
              ],
              "additionalProperties": false
            }
          },
          "benchmarkPrices": {
            "minItems": 21,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "close": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "date",
                "close"
              ],
              "additionalProperties": false
            }
          },
          "frequency": {
            "default": "daily",
            "type": "string",
            "enum": [
              "daily",
              "weekly",
              "monthly"
            ]
          },
          "blumeAdjust": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "assetPrices",
          "benchmarkPrices"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__corporate-action-adjust",
      "description": "Back-adjust prices for splits and dividends. Apply split and cash-dividend factors backwards through a price series (CRSP-style multiplicative dividends) and return adjusted closes, volumes and cumulative factors. Docs: https://www.brainiac.software/api/equity-analytics/corporate-action-adjust",
      "parameters": {
        "type": "object",
        "properties": {
          "prices": {
            "minItems": 1,
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
                "close": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "volume": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "date",
                "close"
              ],
              "additionalProperties": false
            }
          },
          "actions": {
            "default": [],
            "maxItems": 500,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "exDate": {
                      "type": "string",
                      "format": "date",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                    },
                    "type": {
                      "type": "string",
                      "const": "split"
                    },
                    "ratio": {
                      "type": "number",
                      "exclusiveMinimum": 0
                    }
                  },
                  "required": [
                    "exDate",
                    "type",
                    "ratio"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "exDate": {
                      "type": "string",
                      "format": "date",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                    },
                    "type": {
                      "type": "string",
                      "const": "dividend"
                    },
                    "amount": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "exDate",
                    "type",
                    "amount"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          }
        },
        "required": [
          "prices"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__total-return-series",
      "description": "Build a dividend-reinvested total-return index. Compound a total-return index from closes and cash dividends with optional withholding tax, and report price return, total return and CAGR. Docs: https://www.brainiac.software/api/equity-analytics/total-return-series",
      "parameters": {
        "type": "object",
        "properties": {
          "prices": {
            "minItems": 2,
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
                "close": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "date",
                "close"
              ],
              "additionalProperties": false
            }
          },
          "dividends": {
            "default": [],
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "exDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "number"
                }
              },
              "required": [
                "exDate",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "base": {
            "default": 100,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "withholdingTax": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "prices"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__altman-z-score",
      "description": "Altman Z, Z′ and Z″ scores. Compute the public manufacturing Z-score, private Z′ or non-manufacturing Z″ with published safe/grey/distress zones from caller-supplied balance-sheet and income items. Docs: https://www.brainiac.software/api/equity-analytics/altman-z-score",
      "parameters": {
        "type": "object",
        "properties": {
          "variant": {
            "type": "string",
            "enum": [
              "Z",
              "Z_prime",
              "Z_double_prime"
            ]
          },
          "workingCapital": {
            "type": "number"
          },
          "retainedEarnings": {
            "type": "number"
          },
          "ebit": {
            "type": "number"
          },
          "marketValueEquity": {
            "type": "number"
          },
          "bookEquity": {
            "type": "number"
          },
          "sales": {
            "type": "number"
          },
          "totalAssets": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "totalLiabilities": {
            "type": "number"
          }
        },
        "required": [
          "variant",
          "workingCapital",
          "retainedEarnings",
          "ebit",
          "totalAssets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__piotroski-f-score",
      "description": "Piotroski F-score (0–9). Nine binary profitability, leverage, liquidity and operating-efficiency tests from two years of statements. Docs: https://www.brainiac.software/api/equity-analytics/piotroski-f-score",
      "parameters": {
        "type": "object",
        "properties": {
          "current": {
            "type": "object",
            "properties": {
              "period": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "revenue": {
                "type": "number"
              },
              "cogs": {
                "type": "number"
              },
              "sga": {
                "type": "number"
              },
              "depreciation": {
                "type": "number"
              },
              "ebit": {
                "type": "number"
              },
              "interestExpense": {
                "type": "number"
              },
              "netIncome": {
                "type": "number"
              },
              "cfo": {
                "type": "number"
              },
              "capex": {
                "type": "number"
              },
              "totalAssets": {
                "type": "number"
              },
              "currentAssets": {
                "type": "number"
              },
              "currentLiabilities": {
                "type": "number"
              },
              "totalLiabilities": {
                "type": "number"
              },
              "longTermDebt": {
                "type": "number"
              },
              "receivables": {
                "type": "number"
              },
              "inventory": {
                "type": "number"
              },
              "ppeNet": {
                "type": "number"
              },
              "retainedEarnings": {
                "type": "number"
              },
              "sharesOutstanding": {
                "type": "number"
              },
              "dividendsPaid": {
                "type": "number"
              },
              "equity": {
                "type": "number"
              },
              "cash": {
                "type": "number"
              },
              "securities": {
                "type": "number"
              },
              "priorTotalAssets": {
                "type": "number"
              },
              "ebt": {
                "type": "number"
              }
            },
            "additionalProperties": false
          },
          "prior": {
            "type": "object",
            "properties": {
              "period": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "revenue": {
                "type": "number"
              },
              "cogs": {
                "type": "number"
              },
              "sga": {
                "type": "number"
              },
              "depreciation": {
                "type": "number"
              },
              "ebit": {
                "type": "number"
              },
              "interestExpense": {
                "type": "number"
              },
              "netIncome": {
                "type": "number"
              },
              "cfo": {
                "type": "number"
              },
              "capex": {
                "type": "number"
              },
              "totalAssets": {
                "type": "number"
              },
              "currentAssets": {
                "type": "number"
              },
              "currentLiabilities": {
                "type": "number"
              },
              "totalLiabilities": {
                "type": "number"
              },
              "longTermDebt": {
                "type": "number"
              },
              "receivables": {
                "type": "number"
              },
              "inventory": {
                "type": "number"
              },
              "ppeNet": {
                "type": "number"
              },
              "retainedEarnings": {
                "type": "number"
              },
              "sharesOutstanding": {
                "type": "number"
              },
              "dividendsPaid": {
                "type": "number"
              },
              "equity": {
                "type": "number"
              },
              "cash": {
                "type": "number"
              },
              "securities": {
                "type": "number"
              },
              "priorTotalAssets": {
                "type": "number"
              },
              "ebt": {
                "type": "number"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "current",
          "prior"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__beneish-m-score",
      "description": "Beneish eight-variable M-score. Compute DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI and TATA and the Beneish (1999) M-score with the −1.78 flag threshold. Docs: https://www.brainiac.software/api/equity-analytics/beneish-m-score",
      "parameters": {
        "type": "object",
        "properties": {
          "current": {
            "type": "object",
            "properties": {
              "period": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "revenue": {
                "type": "number"
              },
              "cogs": {
                "type": "number"
              },
              "sga": {
                "type": "number"
              },
              "depreciation": {
                "type": "number"
              },
              "ebit": {
                "type": "number"
              },
              "interestExpense": {
                "type": "number"
              },
              "netIncome": {
                "type": "number"
              },
              "cfo": {
                "type": "number"
              },
              "capex": {
                "type": "number"
              },
              "totalAssets": {
                "type": "number"
              },
              "currentAssets": {
                "type": "number"
              },
              "currentLiabilities": {
                "type": "number"
              },
              "totalLiabilities": {
                "type": "number"
              },
              "longTermDebt": {
                "type": "number"
              },
              "receivables": {
                "type": "number"
              },
              "inventory": {
                "type": "number"
              },
              "ppeNet": {
                "type": "number"
              },
              "retainedEarnings": {
                "type": "number"
              },
              "sharesOutstanding": {
                "type": "number"
              },
              "dividendsPaid": {
                "type": "number"
              },
              "equity": {
                "type": "number"
              },
              "cash": {
                "type": "number"
              },
              "securities": {
                "type": "number"
              },
              "priorTotalAssets": {
                "type": "number"
              },
              "ebt": {
                "type": "number"
              }
            },
            "additionalProperties": false
          },
          "prior": {
            "type": "object",
            "properties": {
              "period": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "revenue": {
                "type": "number"
              },
              "cogs": {
                "type": "number"
              },
              "sga": {
                "type": "number"
              },
              "depreciation": {
                "type": "number"
              },
              "ebit": {
                "type": "number"
              },
              "interestExpense": {
                "type": "number"
              },
              "netIncome": {
                "type": "number"
              },
              "cfo": {
                "type": "number"
              },
              "capex": {
                "type": "number"
              },
              "totalAssets": {
                "type": "number"
              },
              "currentAssets": {
                "type": "number"
              },
              "currentLiabilities": {
                "type": "number"
              },
              "totalLiabilities": {
                "type": "number"
              },
              "longTermDebt": {
                "type": "number"
              },
              "receivables": {
                "type": "number"
              },
              "inventory": {
                "type": "number"
              },
              "ppeNet": {
                "type": "number"
              },
              "retainedEarnings": {
                "type": "number"
              },
              "sharesOutstanding": {
                "type": "number"
              },
              "dividendsPaid": {
                "type": "number"
              },
              "equity": {
                "type": "number"
              },
              "cash": {
                "type": "number"
              },
              "securities": {
                "type": "number"
              },
              "priorTotalAssets": {
                "type": "number"
              },
              "ebt": {
                "type": "number"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "current",
          "prior"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__dupont-analysis",
      "description": "Three- and five-step DuPont ROE. Decompose ROE into net margin, asset turnover and equity multiplier, and optionally the five-step tax, interest and EBIT-margin path. Docs: https://www.brainiac.software/api/equity-analytics/dupont-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "netIncome": {
            "type": "number"
          },
          "revenue": {
            "type": "number"
          },
          "totalAssets": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "equity": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "ebt": {
            "type": "number"
          },
          "ebit": {
            "type": "number"
          }
        },
        "required": [
          "netIncome",
          "revenue",
          "totalAssets",
          "equity"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__peer-multiples",
      "description": "Peer multiple stats and implied value. Summarise peer EV/EBITDA, P/E and related multiples with optional IQR trimming, and imply enterprise, equity and per-share values for a target. Docs: https://www.brainiac.software/api/equity-analytics/peer-multiples",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "object",
            "properties": {
              "ebitda": {
                "type": "number"
              },
              "netDebt": {
                "default": 0,
                "type": "number"
              },
              "shares": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "netIncome": {
                "type": "number"
              },
              "equity": {
                "type": "number"
              },
              "sales": {
                "type": "number"
              },
              "revenue": {
                "type": "number"
              }
            },
            "additionalProperties": false
          },
          "peers": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "evToEbitda": {
                  "type": "number"
                },
                "pe": {
                  "type": "number"
                },
                "pb": {
                  "type": "number"
                },
                "evToSales": {
                  "type": "number"
                },
                "ps": {
                  "type": "number"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "multiples": {
            "minItems": 1,
            "maxItems": 5,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "evToEbitda",
                "pe",
                "pb",
                "evToSales",
                "ps"
              ]
            }
          },
          "trimOutliersIqr": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "target",
          "peers",
          "multiples"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__dividend-metrics",
      "description": "Dividend yield, payout, coverage and CAGR. Compute trailing yield, payout ratio, FCF coverage and DPS CAGR from a price and a dividends-per-share series. Docs: https://www.brainiac.software/api/equity-analytics/dividend-metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "price": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "dividendsPerShare": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "year": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "dps": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "year",
                "dps"
              ],
              "additionalProperties": false
            }
          },
          "eps": {
            "type": "number"
          },
          "fcfPerShare": {
            "type": "number"
          }
        },
        "required": [
          "price",
          "dividendsPerShare"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__security-identifier-validate",
      "description": "Validate ISIN, CUSIP and SEDOL check digits. Detect identifier type by pattern, validate check digits, and optionally convert CUSIP or SEDOL to ISIN. Existence is not confirmed. Docs: https://www.brainiac.software/api/equity-analytics/security-identifier-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "identifiers": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 20
            }
          },
          "toIsin": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 2
              }
            },
            "required": [
              "country"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "identifiers"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "equity-analytics__lei-validate",
      "description": "Validate an LEI check digits. Check ISO 17442 structure and ISO/IEC 7064 MOD 97-10 check digits for a Legal Entity Identifier. Registration status is not looked up. Docs: https://www.brainiac.software/api/equity-analytics/lei-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "lei": {
            "type": "string",
            "minLength": 18,
            "maxLength": 24
          }
        },
        "required": [
          "lei"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "equity-analytics__financial-ratios": "0.03",
  "equity-analytics__dcf-valuation": "0.04",
  "equity-analytics__wacc-calculate": "0.02",
  "equity-analytics__beta-regression": "0.03",
  "equity-analytics__corporate-action-adjust": "0.03",
  "equity-analytics__total-return-series": "0.03",
  "equity-analytics__altman-z-score": "0.02",
  "equity-analytics__piotroski-f-score": "0.02",
  "equity-analytics__beneish-m-score": "0.03",
  "equity-analytics__dupont-analysis": "0.02",
  "equity-analytics__peer-multiples": "0.03",
  "equity-analytics__dividend-metrics": "0.02",
  "equity-analytics__security-identifier-validate": "0.02",
  "equity-analytics__lei-validate": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "equity-analytics__financial-ratios": "equity-analytics/financial-ratios",
  "equity-analytics__dcf-valuation": "equity-analytics/dcf-valuation",
  "equity-analytics__wacc-calculate": "equity-analytics/wacc-calculate",
  "equity-analytics__beta-regression": "equity-analytics/beta-regression",
  "equity-analytics__corporate-action-adjust": "equity-analytics/corporate-action-adjust",
  "equity-analytics__total-return-series": "equity-analytics/total-return-series",
  "equity-analytics__altman-z-score": "equity-analytics/altman-z-score",
  "equity-analytics__piotroski-f-score": "equity-analytics/piotroski-f-score",
  "equity-analytics__beneish-m-score": "equity-analytics/beneish-m-score",
  "equity-analytics__dupont-analysis": "equity-analytics/dupont-analysis",
  "equity-analytics__peer-multiples": "equity-analytics/peer-multiples",
  "equity-analytics__dividend-metrics": "equity-analytics/dividend-metrics",
  "equity-analytics__security-identifier-validate": "equity-analytics/security-identifier-validate",
  "equity-analytics__lei-validate": "equity-analytics/lei-validate"
}


class BrainiacEquityAnalyticsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — equity-analytics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the equity-analytics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "equity-analytics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Compute standard financial ratios"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the equity-analytics group. "
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
