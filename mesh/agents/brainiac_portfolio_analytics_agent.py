"""Auto-generated BRAINIAC Heurist Mesh agent for group `portfolio-analytics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "portfolio-analytics__performance-twr-mwr",
      "description": "Time-weighted and money-weighted returns. Compute linked TWR, Modified Dietz and XIRR from valuations and external cash flows, with optional annualisation. Docs: https://www.brainiac.software/api/portfolio-analytics/performance-twr-mwr",
      "parameters": {
        "type": "object",
        "properties": {
          "valuations": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "value": {
                  "type": "number"
                },
                "beforeFlow": {
                  "type": "boolean"
                }
              },
              "required": [
                "date",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "flows": {
            "default": [],
            "maxItems": 100000,
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
                  "type": "number"
                }
              },
              "required": [
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "annualize": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "valuations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__risk-metrics",
      "description": "Volatility, Sharpe, Sortino and drawdown. Annualised volatility, Sharpe, Sortino, Calmar, max drawdown with peak/trough/recovery indices, skewness and excess kurtosis from a return series. Docs: https://www.brainiac.software/api/portfolio-analytics/risk-metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "returns": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "number",
                  "exclusiveMinimum": -1
                },
                {
                  "type": "object",
                  "properties": {
                    "date": {
                      "type": "string",
                      "format": "date",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                    },
                    "r": {
                      "type": "number",
                      "exclusiveMinimum": -1
                    }
                  },
                  "required": [
                    "date",
                    "r"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "periodsPerYear": {
            "default": 12,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "riskFreePerPeriod": {
            "default": 0,
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "array",
                "items": {
                  "type": "number"
                }
              }
            ]
          },
          "mar": {
            "type": [
              "number",
              "null"
            ]
          }
        },
        "required": [
          "returns"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__var-cvar",
      "description": "Value-at-Risk and Expected Shortfall. Historical, parametric normal and Monte Carlo VaR/ES at caller confidence levels from a return series. Docs: https://www.brainiac.software/api/portfolio-analytics/var-cvar",
      "parameters": {
        "type": "object",
        "properties": {
          "returns": {
            "minItems": 10,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": -1
            }
          },
          "confidence": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0.5,
              "exclusiveMaximum": 0.9999
            }
          },
          "methods": {
            "default": [
              "historical",
              "parametric",
              "monte_carlo"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "historical",
                "parametric",
                "monte_carlo"
              ]
            }
          },
          "portfolioValue": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "horizonPeriods": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "simulations": {
            "default": 10000,
            "type": "integer",
            "minimum": 1000,
            "maximum": 200000
          },
          "seed": {
            "default": 42,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "returns",
          "confidence"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__brinson-attribution",
      "description": "Brinson-Fachler attribution. Allocation, selection and interaction effects by segment for one or more periods, with optional Carino linking. Docs: https://www.brainiac.software/api/portfolio-analytics/brinson-attribution",
      "parameters": {
        "type": "object",
        "properties": {
          "periods": {
            "minItems": 1,
            "maxItems": 600,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "segments": {
                  "minItems": 1,
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
                      "wp": {
                        "type": "number"
                      },
                      "wb": {
                        "type": "number"
                      },
                      "rp": {
                        "type": "number"
                      },
                      "rb": {
                        "type": "number"
                      }
                    },
                    "required": [
                      "name",
                      "wp",
                      "wb",
                      "rp",
                      "rb"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "segments"
              ],
              "additionalProperties": false
            }
          },
          "linking": {
            "default": "carino",
            "type": "string",
            "enum": [
              "carino",
              "none"
            ]
          },
          "normalizeWeights": {
            "default": true,
            "type": "boolean"
          },
          "allowNegativeWeights": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "periods"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__factor-regression",
      "description": "Factor regression of excess returns. OLS of portfolio excess returns on caller-supplied factors with intercept, betas, alpha and optional Newey-West standard errors. Docs: https://www.brainiac.software/api/portfolio-analytics/factor-regression",
      "parameters": {
        "type": "object",
        "properties": {
          "returns": {
            "minItems": 4,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": -1
            }
          },
          "riskFree": {
            "default": 0,
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "array",
                "items": {
                  "type": "number"
                }
              }
            ]
          },
          "factors": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 32
            },
            "additionalProperties": {
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "periodsPerYear": {
            "default": 12,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "neweyWestLags": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": [
          "returns",
          "factors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__mean-variance-optimize",
      "description": "Markowitz mean-variance optimisation. Minimum variance, target return, max Sharpe or target volatility portfolios from expected returns and a covariance matrix, with bounds. Docs: https://www.brainiac.software/api/portfolio-analytics/mean-variance-optimize",
      "parameters": {
        "type": "object",
        "properties": {
          "assets": {
            "minItems": 2,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "expectedReturns": {
            "minItems": 2,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "covariance": {
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "returns": {
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "objective": {
            "type": "string",
            "enum": [
              "min_variance",
              "target_return",
              "max_sharpe",
              "target_volatility"
            ]
          },
          "targetReturn": {
            "type": "number"
          },
          "targetVolatility": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "riskFree": {
            "default": 0,
            "type": "number"
          },
          "bounds": {
            "default": {
              "min": 0,
              "max": 1
            },
            "type": "object",
            "properties": {
              "min": {
                "default": 0,
                "type": "number"
              },
              "max": {
                "default": 1,
                "type": "number"
              }
            },
            "additionalProperties": false
          },
          "groups": {
            "default": [],
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "assets": {
                  "minItems": 1,
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "min": {
                  "type": "number"
                },
                "max": {
                  "type": "number"
                }
              },
              "required": [
                "assets",
                "min",
                "max"
              ],
              "additionalProperties": false
            }
          },
          "frontierPoints": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "shrinkage": {
            "default": "none",
            "type": "string",
            "enum": [
              "none",
              "ledoit_wolf"
            ]
          }
        },
        "required": [
          "assets",
          "expectedReturns",
          "objective"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__risk-parity-weights",
      "description": "Equal-risk-contribution and inverse-volatility weights. Spinu ERC (or caller risk-budget) weights and inverse-volatility weights with risk-contribution breakdown. Docs: https://www.brainiac.software/api/portfolio-analytics/risk-parity-weights",
      "parameters": {
        "type": "object",
        "properties": {
          "assets": {
            "minItems": 2,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "covariance": {
            "minItems": 2,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "riskBudget": {
            "anyOf": [
              {
                "type": "array",
                "items": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              {
                "type": "null"
              }
            ]
          },
          "method": {
            "default": "erc",
            "type": "string",
            "enum": [
              "erc",
              "inverse_volatility"
            ]
          }
        },
        "required": [
          "assets",
          "covariance"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__rebalance-trades",
      "description": "Rebalance trades to target weights. Compute buys and sells that restore target weights with tolerance bands, a cash buffer, minimum trade size and whole-share rounding. Docs: https://www.brainiac.software/api/portfolio-analytics/rebalance-trades",
      "parameters": {
        "type": "object",
        "properties": {
          "holdings": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "symbol": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "quantity": {
                  "type": "number"
                },
                "price": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "symbol",
                "quantity",
                "price"
              ],
              "additionalProperties": false
            }
          },
          "cash": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "targets": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            },
            "additionalProperties": {
              "type": "number",
              "minimum": 0,
              "maximum": 1
            }
          },
          "band": {
            "default": {
              "type": "absolute",
              "value": 0
            },
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "enum": [
                  "absolute",
                  "relative"
                ]
              },
              "value": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              }
            },
            "required": [
              "type",
              "value"
            ],
            "additionalProperties": false
          },
          "cashBuffer": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 0.5
          },
          "minTradeValue": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "fractional": {
            "default": false,
            "type": "boolean"
          },
          "restricted": {
            "default": [],
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          }
        },
        "required": [
          "holdings",
          "targets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__correlation-matrix",
      "description": "Correlation and Ledoit-Wolf covariance. Pearson and Spearman correlation, optional covariance, rolling windows and Ledoit-Wolf shrinkage covariance from caller series. Docs: https://www.brainiac.software/api/portfolio-analytics/correlation-matrix",
      "parameters": {
        "type": "object",
        "properties": {
          "series": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            },
            "additionalProperties": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "methods": {
            "default": [
              "pearson",
              "spearman",
              "ledoit_wolf"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "pearson",
                "spearman",
                "ledoit_wolf",
                "covariance"
              ]
            }
          },
          "missing": {
            "default": "pairwise",
            "type": "string",
            "enum": [
              "pairwise",
              "listwise"
            ]
          },
          "rollingWindow": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 3,
                "maximum": 9007199254740991
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "series"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__stress-test",
      "description": "Scenario stress test on holdings. Apply caller-defined asset-class, factor and rate shocks to holdings and report P/L by holding and in total. Docs: https://www.brainiac.software/api/portfolio-analytics/stress-test",
      "parameters": {
        "type": "object",
        "properties": {
          "holdings": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "value": {
                  "type": "number"
                },
                "mapping": {
                  "type": "object",
                  "properties": {
                    "assetClass": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    }
                  },
                  "additionalProperties": false
                },
                "betas": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string"
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                },
                "duration": {
                  "type": "number"
                },
                "convexity": {
                  "type": "number"
                }
              },
              "required": [
                "id",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "scenarios": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "assetClassShocks": {
                  "default": {},
                  "type": "object",
                  "propertyNames": {
                    "type": "string"
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                },
                "factorShocks": {
                  "default": {},
                  "type": "object",
                  "propertyNames": {
                    "type": "string"
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                },
                "rateShockBp": {
                  "type": "number"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "holdings",
          "scenarios"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__monte-carlo-goal",
      "description": "Monte Carlo retirement or savings goal. Project a contribution/withdrawal plan with mulberry32 Monte Carlo paths and report success probability and terminal wealth percentiles. Docs: https://www.brainiac.software/api/portfolio-analytics/monte-carlo-goal",
      "parameters": {
        "type": "object",
        "properties": {
          "startValue": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "years": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "annualContribution": {
            "default": 0,
            "type": "number"
          },
          "annualWithdrawal": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "timing": {
            "default": "start",
            "type": "string",
            "enum": [
              "start",
              "end"
            ]
          },
          "meanReturn": {
            "type": "number"
          },
          "volatility": {
            "type": "number",
            "minimum": 0
          },
          "inflation": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "paths": {
            "default": 2000,
            "type": "integer",
            "minimum": 100,
            "maximum": 100000
          },
          "seed": {
            "default": 42,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "percentiles": {
            "default": [
              10,
              50,
              90
            ],
            "minItems": 1,
            "maxItems": 21,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 100
            }
          }
        },
        "required": [
          "startValue",
          "years",
          "meanReturn",
          "volatility"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__wash-sale-detect",
      "description": "Detect potential US wash sales. Flag IRC §1091 wash sales in caller transactions with FIFO lots, disallowed losses and replacement basis adjustments per IRS Publication 550. Docs: https://www.brainiac.software/api/portfolio-analytics/wash-sale-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "transactions": {
            "minItems": 1,
            "maxItems": 100000,
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
                "symbol": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell"
                  ]
                },
                "quantity": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "amount": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "id",
                "date",
                "symbol",
                "side",
                "quantity",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "identicalGroups": {
            "default": [],
            "type": "array",
            "items": {
              "minItems": 2,
              "type": "array",
              "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 64
              }
            }
          },
          "lotMethod": {
            "default": "fifo",
            "type": "string",
            "enum": [
              "fifo"
            ]
          }
        },
        "required": [
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__fee-drag-project",
      "description": "Project long-run fee drag. Compare terminal wealth with and without expense ratios, advisory fees and loads under multiplicative or subtractive fee methods. Docs: https://www.brainiac.software/api/portfolio-analytics/fee-drag-project",
      "parameters": {
        "type": "object",
        "properties": {
          "initial": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "annualContribution": {
            "default": 0,
            "type": "number"
          },
          "years": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "grossReturn": {
            "type": "number"
          },
          "fees": {
            "default": [],
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 0.2
                }
              },
              "required": [
                "name",
                "rate"
              ],
              "additionalProperties": false
            }
          },
          "frontLoad": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "feeMethod": {
            "default": "multiplicative",
            "type": "string",
            "enum": [
              "multiplicative",
              "subtractive"
            ]
          },
          "includeByYear": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "initial",
          "years",
          "grossReturn"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__tracking-error-capture",
      "description": "Tracking error and capture ratios. Tracking error, information ratio, up/down capture, batting average and optional active share versus a benchmark. Docs: https://www.brainiac.software/api/portfolio-analytics/tracking-error-capture",
      "parameters": {
        "type": "object",
        "properties": {
          "portfolio": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": -1
            }
          },
          "benchmark": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": -1
            }
          },
          "periodsPerYear": {
            "default": 12,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "holdings": {
            "type": "object",
            "properties": {
              "portfolio": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "number"
                }
              },
              "benchmark": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "number"
                }
              }
            },
            "required": [
              "portfolio",
              "benchmark"
            ],
            "additionalProperties": false
          },
          "captureMethod": {
            "default": "arithmetic",
            "type": "string",
            "enum": [
              "arithmetic",
              "geometric"
            ]
          }
        },
        "required": [
          "portfolio",
          "benchmark"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "portfolio-analytics__allocation-xray",
      "description": "Look-through allocation x-ray. Aggregate caller-supplied fund look-through holdings by asset class, sector, region and top underlying positions. Docs: https://www.brainiac.software/api/portfolio-analytics/allocation-xray",
      "parameters": {
        "type": "object",
        "properties": {
          "positions": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "value": {
                  "type": "number"
                },
                "lookThrough": {
                  "maxItems": 100000,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "security": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64
                      },
                      "weight": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      },
                      "assetClass": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64
                      },
                      "sector": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64
                      },
                      "region": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64
                      }
                    },
                    "required": [
                      "security",
                      "weight"
                    ],
                    "additionalProperties": false
                  }
                },
                "otherWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "otherClass": {
                  "type": "object",
                  "properties": {
                    "assetClass": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    },
                    "sector": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    },
                    "region": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    }
                  },
                  "additionalProperties": false
                },
                "assetClass": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "sector": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              },
              "required": [
                "id",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "top": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": [
          "positions"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "portfolio-analytics__performance-twr-mwr": "0.04",
  "portfolio-analytics__risk-metrics": "0.03",
  "portfolio-analytics__var-cvar": "0.04",
  "portfolio-analytics__brinson-attribution": "0.04",
  "portfolio-analytics__factor-regression": "0.04",
  "portfolio-analytics__mean-variance-optimize": "0.05",
  "portfolio-analytics__risk-parity-weights": "0.04",
  "portfolio-analytics__rebalance-trades": "0.03",
  "portfolio-analytics__correlation-matrix": "0.03",
  "portfolio-analytics__stress-test": "0.03",
  "portfolio-analytics__monte-carlo-goal": "0.05",
  "portfolio-analytics__wash-sale-detect": "0.04",
  "portfolio-analytics__fee-drag-project": "0.02",
  "portfolio-analytics__tracking-error-capture": "0.03",
  "portfolio-analytics__allocation-xray": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "portfolio-analytics__performance-twr-mwr": "portfolio-analytics/performance-twr-mwr",
  "portfolio-analytics__risk-metrics": "portfolio-analytics/risk-metrics",
  "portfolio-analytics__var-cvar": "portfolio-analytics/var-cvar",
  "portfolio-analytics__brinson-attribution": "portfolio-analytics/brinson-attribution",
  "portfolio-analytics__factor-regression": "portfolio-analytics/factor-regression",
  "portfolio-analytics__mean-variance-optimize": "portfolio-analytics/mean-variance-optimize",
  "portfolio-analytics__risk-parity-weights": "portfolio-analytics/risk-parity-weights",
  "portfolio-analytics__rebalance-trades": "portfolio-analytics/rebalance-trades",
  "portfolio-analytics__correlation-matrix": "portfolio-analytics/correlation-matrix",
  "portfolio-analytics__stress-test": "portfolio-analytics/stress-test",
  "portfolio-analytics__monte-carlo-goal": "portfolio-analytics/monte-carlo-goal",
  "portfolio-analytics__wash-sale-detect": "portfolio-analytics/wash-sale-detect",
  "portfolio-analytics__fee-drag-project": "portfolio-analytics/fee-drag-project",
  "portfolio-analytics__tracking-error-capture": "portfolio-analytics/tracking-error-capture",
  "portfolio-analytics__allocation-xray": "portfolio-analytics/allocation-xray"
}


class BrainiacPortfolioAnalyticsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — portfolio-analytics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the portfolio-analytics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "portfolio-analytics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Time-weighted and money-weighted returns"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the portfolio-analytics group. "
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
