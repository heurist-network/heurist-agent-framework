"""Auto-generated BRAINIAC Heurist Mesh agent for group `options-analytics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "options-analytics__black-scholes-greeks",
      "description": "Price a European option and its Greeks. Price a European option with Black-Scholes-Merton and return delta, gamma, vega, theta, rho, vanna and charm from caller-supplied spot, strike, time, rate, dividend yield and volatility. Pure computation with a high-accuracy normal CDF. Docs: https://www.brainiac.software/api/options-analytics/black-scholes-greeks",
      "parameters": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "call",
              "put"
            ]
          },
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "strike": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "timeYears": {
            "type": "number",
            "minimum": 0,
            "maximum": 50
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "sigma": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 5
          },
          "greeks": {
            "default": [
              "delta",
              "gamma",
              "vega",
              "theta",
              "rho",
              "vanna",
              "charm"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "delta",
                "gamma",
                "vega",
                "theta",
                "rho",
                "vanna",
                "charm"
              ]
            }
          },
          "dayCount": {
            "default": "ACT/365",
            "type": "string",
            "enum": [
              "ACT/365",
              "ACT/360",
              "TRADING/252"
            ]
          }
        },
        "required": [
          "type",
          "spot",
          "strike",
          "timeYears",
          "sigma"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__implied-volatility-solve",
      "description": "Solve implied volatility for option prices. Solve implied volatility for 1 to 500 option prices with Newton and Brent root-finding on Black-Scholes-Merton, or on a Cox-Ross-Rubinstein tree for American options. Prices outside the no-arbitrage bounds return a status instead of a number. Docs: https://www.brainiac.software/api/options-analytics/implied-volatility-solve",
      "parameters": {
        "type": "object",
        "properties": {
          "style": {
            "default": "european",
            "type": "string",
            "enum": [
              "european",
              "american"
            ]
          },
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "options": {
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
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "put"
                  ]
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "timeYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 50
                },
                "price": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "type",
                "strike",
                "timeYears",
                "price"
              ],
              "additionalProperties": false
            }
          },
          "treeSteps": {
            "default": 200,
            "type": "integer",
            "minimum": 50,
            "maximum": 2000
          }
        },
        "required": [
          "spot",
          "options"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__american-binomial-price",
      "description": "Price an American option on a binomial tree. Price an American or European option on a Cox-Ross-Rubinstein tree with optional discrete cash dividends (escrowed method), and return tree delta, gamma, theta, the early-exercise boundary and the Black-Scholes-Merton European value for comparison. Docs: https://www.brainiac.software/api/options-analytics/american-binomial-price",
      "parameters": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "call",
              "put"
            ]
          },
          "style": {
            "default": "american",
            "type": "string",
            "enum": [
              "american",
              "european"
            ]
          },
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "strike": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "timeYears": {
            "type": "number",
            "minimum": 0,
            "maximum": 50
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "sigma": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 5
          },
          "steps": {
            "default": 500,
            "type": "integer",
            "minimum": 1,
            "maximum": 5000
          },
          "dividends": {
            "default": [],
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "timeYears": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "amount": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "timeYears",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "type",
          "spot",
          "strike",
          "timeYears",
          "sigma"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__strategy-payoff",
      "description": "Compute multi-leg option strategy payoff. Compute payoff and profit or loss of a multi-leg option and stock position at expiry and at a valuation date, with exact breakevens, maximum profit and loss, and unlimited-risk flags. Docs: https://www.brainiac.software/api/options-analytics/strategy-payoff",
      "parameters": {
        "type": "object",
        "properties": {
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "multiplier": {
            "default": 100,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "valuationTimeYears": {
            "anyOf": [
              {
                "type": "number",
                "minimum": 0,
                "maximum": 50
              },
              {
                "type": "null"
              }
            ]
          },
          "legs": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "option",
                    "stock"
                  ]
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "put"
                  ]
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "timeYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 50
                },
                "qty": {
                  "type": "number"
                },
                "premium": {
                  "type": "number",
                  "minimum": 0
                },
                "sigma": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 5
                }
              },
              "required": [
                "kind",
                "qty",
                "premium"
              ],
              "additionalProperties": false
            }
          },
          "grid": {
            "type": "object",
            "properties": {
              "from": {
                "type": "number",
                "minimum": 0
              },
              "to": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "step": {
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "required": [
              "from",
              "to",
              "step"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "spot",
          "legs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__probability-of-profit",
      "description": "Compute lognormal option probabilities. Compute lognormal probabilities of finishing above or below levels, touching a level before expiry, and finishing in profit for a strategy given its breakevens, under risk-neutral or real-world drift. Docs: https://www.brainiac.software/api/options-analytics/probability-of-profit",
      "parameters": {
        "type": "object",
        "properties": {
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "sigma": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 5
          },
          "timeYears": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 50
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "measure": {
            "default": "risk_neutral",
            "type": "string",
            "enum": [
              "risk_neutral",
              "real_world"
            ]
          },
          "drift": {
            "anyOf": [
              {
                "type": "number",
                "minimum": -1,
                "maximum": 2
              },
              {
                "type": "null"
              }
            ]
          },
          "levels": {
            "default": [],
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "breakevens": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "profitAbove": {
            "type": "boolean"
          },
          "profitBetween": {
            "type": "array",
            "prefixItems": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "number",
                "exclusiveMinimum": 0
              }
            ],
            "items": false,
            "minItems": 2,
            "maxItems": 2
          }
        },
        "required": [
          "spot",
          "sigma",
          "timeYears"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__iv-rank-percentile",
      "description": "Compute IV rank and IV percentile. Compute IV rank and IV percentile of the current implied volatility against caller-supplied history over a trailing window of observations. Docs: https://www.brainiac.software/api/options-analytics/iv-rank-percentile",
      "parameters": {
        "type": "object",
        "properties": {
          "current": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "history": {
            "minItems": 2,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "iv": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "date",
                "iv"
              ],
              "additionalProperties": false
            }
          },
          "windowDays": {
            "default": 252,
            "type": "integer",
            "minimum": 5,
            "maximum": 2520
          }
        },
        "required": [
          "current",
          "history"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__historical-volatility",
      "description": "Compute realised volatility from OHLC bars. Compute close-to-close, Parkinson, Garman-Klass, Rogers-Satchell and Yang-Zhang realised volatility from OHLC bars, optionally excluding flagged days and returning a rolling series. Docs: https://www.brainiac.software/api/options-analytics/historical-volatility",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 3,
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
                "open": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "high": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "low": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "close": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "exclude": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "date",
                "open",
                "high",
                "low",
                "close"
              ],
              "additionalProperties": false
            }
          },
          "estimators": {
            "default": [
              "close_to_close",
              "parkinson",
              "garman_klass",
              "rogers_satchell",
              "yang_zhang"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "close_to_close",
                "parkinson",
                "garman_klass",
                "rogers_satchell",
                "yang_zhang"
              ]
            }
          },
          "annualization": {
            "default": 252,
            "type": "integer",
            "minimum": 1,
            "maximum": 366
          },
          "window": {
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
          "bars"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__volatility-surface-fit",
      "description": "Fit an SVI volatility surface. Fit a raw-SVI slice per expiry to strike implied volatilities with the Zeliade quasi-explicit method, interpolate the surface in total variance, and report butterfly and calendar static-arbitrage violations. Docs: https://www.brainiac.software/api/options-analytics/volatility-surface-fit",
      "parameters": {
        "type": "object",
        "properties": {
          "forwardByExpiry": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "points": {
            "minItems": 5,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "timeYears": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 50
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "iv": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 10
                }
              },
              "required": [
                "timeYears",
                "strike",
                "iv"
              ],
              "additionalProperties": false
            }
          },
          "query": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "timeYears": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "timeYears",
                "strike"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "forwardByExpiry",
          "points"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__put-call-parity-check",
      "description": "Check put-call parity and implied forward. Infer the implied forward and carry from call and put quote pairs, solve the rate by least squares when omitted, and flag pairs whose bid and ask break the European or American parity band. Docs: https://www.brainiac.software/api/options-analytics/put-call-parity-check",
      "parameters": {
        "type": "object",
        "properties": {
          "style": {
            "default": "european",
            "type": "string",
            "enum": [
              "european",
              "american"
            ]
          },
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "rate": {
            "anyOf": [
              {
                "type": "number",
                "minimum": -0.2,
                "maximum": 1
              },
              {
                "type": "null"
              }
            ]
          },
          "timeYears": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 50
          },
          "pairs": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "callBid": {
                  "type": "number",
                  "minimum": 0
                },
                "callAsk": {
                  "type": "number",
                  "minimum": 0
                },
                "putBid": {
                  "type": "number",
                  "minimum": 0
                },
                "putAsk": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "strike",
                "callBid",
                "callAsk",
                "putBid",
                "putAsk"
              ],
              "additionalProperties": false
            }
          },
          "toleranceAbs": {
            "default": 0.01,
            "type": "number",
            "minimum": 0
          }
        },
        "required": [
          "spot",
          "timeYears",
          "pairs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__expected-move",
      "description": "Compute market-implied expected move. Compute the one and two standard deviation expected move and price ranges from implied volatility or from the at-the-money straddle price. Docs: https://www.brainiac.software/api/options-analytics/expected-move",
      "parameters": {
        "type": "object",
        "properties": {
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "daysToExpiry": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 3650
          },
          "iv": {
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
          "straddlePrice": {
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
          "dayBasis": {
            "default": 365,
            "anyOf": [
              {
                "type": "number",
                "const": 365
              },
              {
                "type": "number",
                "const": 252
              }
            ]
          }
        },
        "required": [
          "spot",
          "daysToExpiry"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__skew-metrics",
      "description": "Compute 25-delta skew metrics. Compute 25-delta risk reversal, butterfly, skew slope and term-structure slope from strike and implied volatility quotes by expiry, with linear interpolation in log-moneyness and no extrapolation. Docs: https://www.brainiac.software/api/options-analytics/skew-metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "spot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "rate": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "dividendYield": {
            "default": 0,
            "type": "number",
            "minimum": -0.2,
            "maximum": 1
          },
          "deltaConvention": {
            "default": "spot",
            "type": "string",
            "enum": [
              "spot",
              "forward"
            ]
          },
          "expiries": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "timeYears": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 50
                },
                "points": {
                  "minItems": 3,
                  "maxItems": 500,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "strike": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      },
                      "iv": {
                        "type": "number",
                        "exclusiveMinimum": 0,
                        "maximum": 10
                      }
                    },
                    "required": [
                      "strike",
                      "iv"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "timeYears",
                "points"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "spot",
          "expiries"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__position-greeks-aggregate",
      "description": "Aggregate portfolio option Greeks. Aggregate share delta, dollar delta, gamma, vega, theta per day and beta-weighted delta across option and stock positions, computing Black-Scholes-Merton Greeks unless the caller supplies them. Docs: https://www.brainiac.software/api/options-analytics/position-greeks-aggregate",
      "parameters": {
        "type": "object",
        "properties": {
          "benchmarkSpot": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "positions": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "underlying": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "spot": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "beta": {
                  "default": 1,
                  "type": "number"
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "option",
                    "stock"
                  ]
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "put"
                  ]
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "timeYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 50
                },
                "rate": {
                  "default": 0,
                  "type": "number",
                  "minimum": -0.2,
                  "maximum": 1
                },
                "dividendYield": {
                  "default": 0,
                  "type": "number",
                  "minimum": -0.2,
                  "maximum": 1
                },
                "sigma": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 5
                },
                "qty": {
                  "type": "number"
                },
                "multiplier": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "delta": {
                  "type": "number"
                },
                "gamma": {
                  "type": "number"
                },
                "vega": {
                  "type": "number"
                },
                "theta": {
                  "type": "number"
                }
              },
              "required": [
                "underlying",
                "spot",
                "kind",
                "qty"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "benchmarkSpot",
          "positions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__covered-call-yield",
      "description": "Compute covered call and cash-secured put yield. Compute static and if-called returns, annualised returns, downside protection and breakeven for a covered call, or the return on collateral for a cash-secured put. Docs: https://www.brainiac.software/api/options-analytics/covered-call-yield",
      "parameters": {
        "type": "object",
        "properties": {
          "strategy": {
            "type": "string",
            "enum": [
              "covered_call",
              "cash_secured_put"
            ]
          },
          "stockPrice": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "strike": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "premium": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "daysToExpiry": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1095
          },
          "dividendsBeforeExpiry": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "commission": {
            "default": 0,
            "type": "number",
            "minimum": 0
          }
        },
        "required": [
          "strategy",
          "strike",
          "premium",
          "daysToExpiry"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__occ-symbol-parse",
      "description": "Parse or build OCC option symbols. Parse or build OCC Options Symbology Initiative 21-character option symbols, validating the calendar date and flagging roots that look adjusted. Docs: https://www.brainiac.software/api/options-analytics/occ-symbol-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "parse": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 40
            }
          },
          "build": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "root": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9]{1,6}$"
                },
                "expiry": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "call",
                    "put"
                  ]
                },
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "exclusiveMaximum": 100000
                }
              },
              "required": [
                "root",
                "expiry",
                "type",
                "strike"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "options-analytics__max-pain-oi",
      "description": "Compute max pain and open-interest walls. Compute the max-pain strike, per-strike payout, put/call open-interest ratio and the highest open-interest call and put walls for one expiry from a supplied option chain. Docs: https://www.brainiac.software/api/options-analytics/max-pain-oi",
      "parameters": {
        "type": "object",
        "properties": {
          "multiplier": {
            "default": 100,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "chain": {
            "minItems": 2,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "strike": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "callOi": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "putOi": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "strike",
                "callOi",
                "putOi"
              ],
              "additionalProperties": false
            }
          },
          "topWalls": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": [
          "chain"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "options-analytics__black-scholes-greeks": "0.02",
  "options-analytics__implied-volatility-solve": "0.04",
  "options-analytics__american-binomial-price": "0.04",
  "options-analytics__strategy-payoff": "0.03",
  "options-analytics__probability-of-profit": "0.02",
  "options-analytics__iv-rank-percentile": "0.02",
  "options-analytics__historical-volatility": "0.04",
  "options-analytics__volatility-surface-fit": "0.05",
  "options-analytics__put-call-parity-check": "0.03",
  "options-analytics__expected-move": "0.02",
  "options-analytics__skew-metrics": "0.03",
  "options-analytics__position-greeks-aggregate": "0.03",
  "options-analytics__covered-call-yield": "0.02",
  "options-analytics__occ-symbol-parse": "0.02",
  "options-analytics__max-pain-oi": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "options-analytics__black-scholes-greeks": "options-analytics/black-scholes-greeks",
  "options-analytics__implied-volatility-solve": "options-analytics/implied-volatility-solve",
  "options-analytics__american-binomial-price": "options-analytics/american-binomial-price",
  "options-analytics__strategy-payoff": "options-analytics/strategy-payoff",
  "options-analytics__probability-of-profit": "options-analytics/probability-of-profit",
  "options-analytics__iv-rank-percentile": "options-analytics/iv-rank-percentile",
  "options-analytics__historical-volatility": "options-analytics/historical-volatility",
  "options-analytics__volatility-surface-fit": "options-analytics/volatility-surface-fit",
  "options-analytics__put-call-parity-check": "options-analytics/put-call-parity-check",
  "options-analytics__expected-move": "options-analytics/expected-move",
  "options-analytics__skew-metrics": "options-analytics/skew-metrics",
  "options-analytics__position-greeks-aggregate": "options-analytics/position-greeks-aggregate",
  "options-analytics__covered-call-yield": "options-analytics/covered-call-yield",
  "options-analytics__occ-symbol-parse": "options-analytics/occ-symbol-parse",
  "options-analytics__max-pain-oi": "options-analytics/max-pain-oi"
}


class BrainiacOptionsAnalyticsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — options-analytics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the options-analytics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "options-analytics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Price a European option and its Greeks"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the options-analytics group. "
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
