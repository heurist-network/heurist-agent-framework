"""Auto-generated BRAINIAC Heurist Mesh agent for group `accounting-schedules` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "accounting-schedules__depreciation-schedule",
      "description": "Book depreciation schedule. Straight-line, declining-balance, sum-of-years'-digits and units-of-production depreciation schedules with optional first-year convention and journal entries. Docs: https://www.brainiac.software/api/accounting-schedules/depreciation-schedule",
      "parameters": {
        "type": "object",
        "properties": {
          "cost": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "salvage": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "lifeYears": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 100
          },
          "method": {
            "type": "string",
            "enum": [
              "SL",
              "DDB",
              "DB150",
              "SYD",
              "UOP"
            ]
          },
          "inServiceDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "convention": {
            "default": "none",
            "type": "string",
            "enum": [
              "full_month",
              "half_year",
              "none"
            ]
          },
          "fiscalYearEndMonth": {
            "default": 12,
            "type": "integer",
            "minimum": 1,
            "maximum": 12
          },
          "unitsTotal": {
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
          "unitsByPeriod": {
            "anyOf": [
              {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "number",
                  "minimum": 0
                }
              },
              {
                "type": "null"
              }
            ]
          },
          "switchToSL": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "cost",
          "salvage",
          "lifeYears",
          "method",
          "inServiceDate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__macrs-depreciation",
      "description": "US MACRS GDS depreciation. Apply IRS Publication 946 Appendix A GDS percentage tables (half-year, mid-quarter, mid-month) after optional section 179 and caller-supplied bonus percentage. Docs: https://www.brainiac.software/api/accounting-schedules/macrs-depreciation",
      "parameters": {
        "type": "object",
        "properties": {
          "basis": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "recoveryPeriod": {
            "anyOf": [
              {
                "type": "number",
                "const": 3
              },
              {
                "type": "number",
                "const": 5
              },
              {
                "type": "number",
                "const": 7
              },
              {
                "type": "number",
                "const": 10
              },
              {
                "type": "number",
                "const": 15
              },
              {
                "type": "number",
                "const": 20
              },
              {
                "type": "number",
                "const": 27.5
              },
              {
                "type": "number",
                "const": 39
              }
            ]
          },
          "convention": {
            "type": "string",
            "enum": [
              "HY",
              "MQ",
              "MM"
            ]
          },
          "quarterPlaced": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 4
          },
          "monthPlaced": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 12
          },
          "placedInService": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "section179": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "bonusPct": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "q4BasisShare": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "basis",
          "recoveryPeriod",
          "convention"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__lease-schedule",
      "description": "Lessee lease liability and ROU schedule. Present-value a payment stream at the periodic discount rate and amortise the lease liability and right-of-use asset (IFRS 16 / ASC 842 finance-lease mechanics). Docs: https://www.brainiac.software/api/accounting-schedules/lease-schedule",
      "parameters": {
        "type": "object",
        "properties": {
          "payments": {
            "minItems": 1,
            "maxItems": 600,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "commencement": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "discountRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "timing": {
            "default": "arrears",
            "type": "string",
            "enum": [
              "arrears",
              "advance"
            ]
          },
          "initialDirectCosts": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "incentives": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "periodicity": {
            "default": "annual",
            "type": "string",
            "enum": [
              "annual",
              "monthly"
            ]
          }
        },
        "required": [
          "payments",
          "commencement",
          "discountRate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__revenue-recognition-schedule",
      "description": "Allocate contract price to performance obligations. Allocate transaction price by relative standalone selling price and schedule point-in-time, straight-line or milestone recognition by month. Docs: https://www.brainiac.software/api/accounting-schedules/revenue-recognition-schedule",
      "parameters": {
        "type": "object",
        "properties": {
          "transactionPrice": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "obligations": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "ssp": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "pattern": {
                  "type": "string",
                  "enum": [
                    "point_in_time",
                    "straight_line",
                    "milestone"
                  ]
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "start": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "end": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "milestones": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "date": {
                        "type": "string",
                        "format": "date",
                        "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                      },
                      "pct": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "date",
                      "pct"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "ssp",
                "pattern"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "transactionPrice",
          "obligations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__loan-amortization-journal",
      "description": "Fixed-rate loan amortisation journal. Compute a level-payment amortisation table and balancing journal entries for a fixed-rate loan. Docs: https://www.brainiac.software/api/accounting-schedules/loan-amortization-journal",
      "parameters": {
        "type": "object",
        "properties": {
          "principal": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "annualRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "termMonths": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 600
          },
          "firstPaymentDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "accounts": {
            "type": "object",
            "properties": {
              "loan": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "interest": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "cash": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              }
            },
            "required": [
              "loan",
              "interest",
              "cash"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "principal",
          "annualRate",
          "termMonths",
          "firstPaymentDate",
          "accounts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__bank-reconciliation-match",
      "description": "Match bank lines to ledger entries. Match bank statement lines to ledger entries by amount+reference, amount+date tolerance, and optional many-to-one subset sums. Docs: https://www.brainiac.software/api/accounting-schedules/bank-reconciliation-match",
      "parameters": {
        "type": "object",
        "properties": {
          "bank": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "text": {
                  "default": "",
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "ledger": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "ref": {
                  "default": "",
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "dateToleranceDays": {
            "default": 5,
            "type": "integer",
            "minimum": 0,
            "maximum": 90
          },
          "allowManyToOne": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "bank",
          "ledger"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__trial-balance-validate",
      "description": "Validate a trial balance. Check debit/credit equality, abnormal balances by account type, duplicate codes and lines with both debit and credit. Docs: https://www.brainiac.software/api/accounting-schedules/trial-balance-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "accounts": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "name": {
                  "default": "",
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "asset",
                    "liability",
                    "equity",
                    "income",
                    "expense"
                  ]
                },
                "debit": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "credit": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "statementLine": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                }
              },
              "required": [
                "code",
                "type"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "accounts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__financial-statements-build",
      "description": "Build income statement and balance sheet. Roll a mapped trial balance into income-statement and balance-sheet lines, add net income to equity, and check A = L + E. Docs: https://www.brainiac.software/api/accounting-schedules/financial-statements-build",
      "parameters": {
        "type": "object",
        "properties": {
          "accounts": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "name": {
                  "default": "",
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "asset",
                    "liability",
                    "equity",
                    "income",
                    "expense"
                  ]
                },
                "debit": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "credit": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "statementLine": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                }
              },
              "required": [
                "code",
                "type"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "accounts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__cash-flow-forecast-13w",
      "description": "13-week direct cash-flow forecast. Bucket receivables, payables and recurring cash items into Monday-start weeks and report closing cash versus a minimum. Docs: https://www.brainiac.software/api/accounting-schedules/cash-flow-forecast-13w",
      "parameters": {
        "type": "object",
        "properties": {
          "openingCash": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "weekStart": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "receivables": {
            "default": [],
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "due": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "collectionDelayDays": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 365
                }
              },
              "required": [
                "due",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "payables": {
            "default": [],
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "due": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "amount": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "paymentDelayDays": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 365
                }
              },
              "required": [
                "due",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "recurring": {
            "default": [],
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "every": {
                  "type": "string",
                  "enum": [
                    "1w",
                    "2w",
                    "4w",
                    "monthly"
                  ]
                },
                "start": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                }
              },
              "required": [
                "name",
                "amount",
                "every",
                "start"
              ],
              "additionalProperties": false
            }
          },
          "minimumCash": {
            "default": 0,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "openingCash",
          "weekStart"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__fx-revaluation",
      "description": "Unrealised FX revaluation. Revalue foreign-currency monetary balances at closing rates and propose unrealised gain/loss journal entries. Docs: https://www.brainiac.software/api/accounting-schedules/fx-revaluation",
      "parameters": {
        "type": "object",
        "properties": {
          "functionalCurrency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "balances": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "currency": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 3
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "carryingRate": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "asset",
                    "liability"
                  ]
                }
              },
              "required": [
                "account",
                "currency",
                "amount",
                "carryingRate",
                "type"
              ],
              "additionalProperties": false
            }
          },
          "closingRates": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 3,
              "maxLength": 3
            },
            "additionalProperties": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "rateQuote": {
            "type": "string",
            "enum": [
              "foreign_per_functional",
              "functional_per_foreign"
            ]
          },
          "accounts": {
            "default": {
              "gainLoss": "7900"
            },
            "type": "object",
            "properties": {
              "gainLoss": {
                "default": "7900",
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          }
        },
        "required": [
          "functionalCurrency",
          "balances",
          "closingRates",
          "rateQuote"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__inventory-costing",
      "description": "FIFO, weighted-average and specific-ID costing. Cost inventory issues under FIFO, perpetual weighted average or specific identification and report closing quantity and value. Docs: https://www.brainiac.software/api/accounting-schedules/inventory-costing",
      "parameters": {
        "type": "object",
        "properties": {
          "method": {
            "type": "string",
            "enum": [
              "FIFO",
              "WAVG",
              "SPECIFIC"
            ]
          },
          "movements": {
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
                "type": {
                  "type": "string",
                  "enum": [
                    "receipt",
                    "issue"
                  ]
                },
                "qty": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "unitCost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "lotId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              },
              "required": [
                "date",
                "type",
                "qty"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "method",
          "movements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__accrual-prepaid-schedule",
      "description": "Prepaid/accrual amortisation schedule. Spread a prepaid or accrual amount over months on a daily or equal-month basis with balancing journal entries. Docs: https://www.brainiac.software/api/accounting-schedules/accrual-prepaid-schedule",
      "parameters": {
        "type": "object",
        "properties": {
          "amount": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "start": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "end": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "basis": {
            "default": "daily",
            "type": "string",
            "enum": [
              "daily",
              "monthly_equal"
            ]
          },
          "accounts": {
            "type": "object",
            "properties": {
              "prepaid": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              },
              "expense": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
              }
            },
            "required": [
              "prepaid",
              "expense"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "amount",
          "start",
          "end",
          "accounts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__intercompany-eliminate",
      "description": "Intercompany balance elimination. Pair entity/counterparty intercompany balances, flag differences above tolerance, and propose elimination entries for matched amounts. Docs: https://www.brainiac.software/api/accounting-schedules/intercompany-eliminate",
      "parameters": {
        "type": "object",
        "properties": {
          "balances": {
            "minItems": 2,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "entity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "counterparty": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 3
                }
              },
              "required": [
                "entity",
                "counterparty",
                "account",
                "amount",
                "currency"
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
          "balances"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__journal-anomaly-detect",
      "description": "Rule-based journal anomaly flags. Flag round amounts, weekend/after-hours postings, amount z-scores, duplicates and Benford first-digit chi-square on journal lines. Docs: https://www.brainiac.software/api/accounting-schedules/journal-anomaly-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "entries": {
            "minItems": 1,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "postedAt": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
                },
                "user": {
                  "type": "string",
                  "maxLength": 64
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "description": {
                  "default": "",
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "date",
                "account",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "rules": {
            "default": {
              "weekendPosting": true,
              "zScore": 3
            },
            "type": "object",
            "properties": {
              "roundAmountMultiple": {
                "type": "integer",
                "exclusiveMinimum": 0,
                "maximum": 9007199254740991
              },
              "weekendPosting": {
                "default": true,
                "type": "boolean"
              },
              "afterHours": {
                "type": "array",
                "prefixItems": [
                  {
                    "type": "string",
                    "pattern": "^\\d{2}:\\d{2}$"
                  },
                  {
                    "type": "string",
                    "pattern": "^\\d{2}:\\d{2}$"
                  }
                ],
                "items": false,
                "minItems": 2,
                "maxItems": 2
              },
              "zScore": {
                "default": 3,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "entries"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounting-schedules__form-1099-threshold-check",
      "description": "Form 1099 threshold check. Sum payee payments by category for tax year 2026 and flag 1099-NEC / 1099-MISC boxes that meet IRS thresholds. Docs: https://www.brainiac.software/api/accounting-schedules/form-1099-threshold-check",
      "parameters": {
        "type": "object",
        "properties": {
          "taxYear": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "payments": {
            "minItems": 1,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "payeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "payeeType": {
                  "type": "string",
                  "enum": [
                    "individual",
                    "corporation",
                    "attorney"
                  ]
                },
                "category": {
                  "type": "string",
                  "enum": [
                    "services",
                    "rents",
                    "royalties",
                    "attorney_proceeds",
                    "prizes",
                    "other_income",
                    "medical"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "paidByCardOrThirdParty": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "payeeId",
                "payeeType",
                "category",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "taxYear",
          "payments"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "accounting-schedules__depreciation-schedule": "0.03",
  "accounting-schedules__macrs-depreciation": "0.03",
  "accounting-schedules__lease-schedule": "0.04",
  "accounting-schedules__revenue-recognition-schedule": "0.03",
  "accounting-schedules__loan-amortization-journal": "0.03",
  "accounting-schedules__bank-reconciliation-match": "0.04",
  "accounting-schedules__trial-balance-validate": "0.02",
  "accounting-schedules__financial-statements-build": "0.03",
  "accounting-schedules__cash-flow-forecast-13w": "0.04",
  "accounting-schedules__fx-revaluation": "0.03",
  "accounting-schedules__inventory-costing": "0.03",
  "accounting-schedules__accrual-prepaid-schedule": "0.02",
  "accounting-schedules__intercompany-eliminate": "0.03",
  "accounting-schedules__journal-anomaly-detect": "0.04",
  "accounting-schedules__form-1099-threshold-check": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "accounting-schedules__depreciation-schedule": "accounting-schedules/depreciation-schedule",
  "accounting-schedules__macrs-depreciation": "accounting-schedules/macrs-depreciation",
  "accounting-schedules__lease-schedule": "accounting-schedules/lease-schedule",
  "accounting-schedules__revenue-recognition-schedule": "accounting-schedules/revenue-recognition-schedule",
  "accounting-schedules__loan-amortization-journal": "accounting-schedules/loan-amortization-journal",
  "accounting-schedules__bank-reconciliation-match": "accounting-schedules/bank-reconciliation-match",
  "accounting-schedules__trial-balance-validate": "accounting-schedules/trial-balance-validate",
  "accounting-schedules__financial-statements-build": "accounting-schedules/financial-statements-build",
  "accounting-schedules__cash-flow-forecast-13w": "accounting-schedules/cash-flow-forecast-13w",
  "accounting-schedules__fx-revaluation": "accounting-schedules/fx-revaluation",
  "accounting-schedules__inventory-costing": "accounting-schedules/inventory-costing",
  "accounting-schedules__accrual-prepaid-schedule": "accounting-schedules/accrual-prepaid-schedule",
  "accounting-schedules__intercompany-eliminate": "accounting-schedules/intercompany-eliminate",
  "accounting-schedules__journal-anomaly-detect": "accounting-schedules/journal-anomaly-detect",
  "accounting-schedules__form-1099-threshold-check": "accounting-schedules/form-1099-threshold-check"
}


class BrainiacAccountingSchedulesAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — accounting-schedules",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the accounting-schedules catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "accounting-schedules", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Book depreciation schedule"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the accounting-schedules group. "
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
