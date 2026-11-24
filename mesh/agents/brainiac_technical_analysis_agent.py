"""Auto-generated BRAINIAC Heurist Mesh agent for group `technical-analysis` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "technical-analysis__moving-averages",
      "description": "Compute moving averages (SMA, EMA, WMA, DEMA, TEMA, HMA). Compute SMA, EMA (SMA-seeded), WMA, DEMA, TEMA and Hull moving averages on caller-supplied OHLCV bars, on close or another price source, with warm-up length per series. Docs: https://www.brainiac.software/api/technical-analysis/moving-averages",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "types": {
            "default": [
              "sma",
              "ema"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "sma",
                "ema",
                "wma",
                "dema",
                "tema",
                "hma"
              ]
            }
          },
          "period": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "source": {
            "default": "c",
            "type": "string",
            "enum": [
              "o",
              "h",
              "l",
              "c",
              "hl2",
              "hlc3",
              "ohlc4"
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
      "name": "technical-analysis__momentum-oscillators",
      "description": "Compute momentum oscillators (RSI, Stochastic, CCI, MFI). Compute Wilder RSI, Stochastic %K/%D, Williams %R, CCI, ROC and MFI on caller-supplied OHLCV bars, with warm-up length per series. Docs: https://www.brainiac.software/api/technical-analysis/momentum-oscillators",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "default": [
              "rsi",
              "stoch",
              "williams",
              "cci",
              "roc",
              "mfi"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "rsi",
                "stoch",
                "williams",
                "cci",
                "roc",
                "mfi"
              ]
            }
          },
          "rsiPeriod": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "stochK": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "stochD": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "williamsPeriod": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "cciPeriod": {
            "default": 20,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "rocPeriod": {
            "default": 12,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "mfiPeriod": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
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
      "name": "technical-analysis__macd",
      "description": "Compute MACD with signal line and crossovers. Compute the MACD line, signal line and histogram on caller-supplied closes and list the bars where the histogram changes sign. Docs: https://www.brainiac.software/api/technical-analysis/macd",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "fast": {
            "default": 12,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "slow": {
            "default": 26,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "signal": {
            "default": 9,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
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
      "name": "technical-analysis__bands-channels",
      "description": "Compute Bollinger, Keltner and Donchian bands. Compute Bollinger Bands with %B and bandwidth, Keltner Channels and Donchian Channels on caller-supplied OHLCV bars. Docs: https://www.brainiac.software/api/technical-analysis/bands-channels",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "bollinger": {
            "default": {
              "period": 20,
              "k": 2
            },
            "type": "object",
            "properties": {
              "period": {
                "default": 20,
                "type": "integer",
                "minimum": 1,
                "maximum": 20000
              },
              "k": {
                "default": 2,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          },
          "keltner": {
            "default": {
              "period": 20,
              "atrPeriod": 10,
              "mult": 2
            },
            "type": "object",
            "properties": {
              "period": {
                "default": 20,
                "type": "integer",
                "minimum": 1,
                "maximum": 20000
              },
              "atrPeriod": {
                "default": 10,
                "type": "integer",
                "minimum": 1,
                "maximum": 20000
              },
              "mult": {
                "default": 2,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          },
          "donchian": {
            "default": {
              "period": 20
            },
            "type": "object",
            "properties": {
              "period": {
                "default": 20,
                "type": "integer",
                "minimum": 1,
                "maximum": 20000
              }
            },
            "additionalProperties": false
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
      "name": "technical-analysis__volatility-measures",
      "description": "Compute true range, ATR, NATR and historical volatility. Compute true range, Wilder ATR, NATR and annualised close-to-close historical volatility on caller-supplied OHLCV bars. Docs: https://www.brainiac.software/api/technical-analysis/volatility-measures",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "atrPeriod": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "hvPeriod": {
            "default": 20,
            "type": "integer",
            "minimum": 2,
            "maximum": 20000
          },
          "annualization": {
            "default": 252,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 100000
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
      "name": "technical-analysis__ichimoku",
      "description": "Compute Ichimoku Kinko Hyo lines and future cloud. Compute Tenkan, Kijun, displaced Senkou A/B and Chikou on caller-supplied OHLCV bars, plus the cloud projected beyond the last bar. Docs: https://www.brainiac.software/api/technical-analysis/ichimoku",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "tenkan": {
            "default": 9,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "kijun": {
            "default": 26,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "senkouB": {
            "default": 52,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "displacement": {
            "default": 26,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
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
      "name": "technical-analysis__trend-indicators",
      "description": "Compute ADX/DMI, Parabolic SAR, Aroon and SuperTrend. Compute Wilder ADX with +DI/-DI, Parabolic SAR with trend, Aroon Up/Down and SuperTrend with direction on caller-supplied OHLCV bars. Docs: https://www.brainiac.software/api/technical-analysis/trend-indicators",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "adxPeriod": {
            "default": 14,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "sar": {
            "default": {
              "step": 0.02,
              "max": 0.2
            },
            "type": "object",
            "properties": {
              "step": {
                "default": 0.02,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "max": {
                "default": 0.2,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          },
          "aroonPeriod": {
            "default": 25,
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "supertrend": {
            "default": {
              "atrPeriod": 10,
              "mult": 3
            },
            "type": "object",
            "properties": {
              "atrPeriod": {
                "default": 10,
                "type": "integer",
                "minimum": 1,
                "maximum": 20000
              },
              "mult": {
                "default": 3,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
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
      "name": "technical-analysis__volume-indicators",
      "description": "Compute OBV, A/D line, CMF, VWAP and volume SMA. Compute on-balance volume, the accumulation/distribution line, Chaikin Money Flow, session-anchored or cumulative VWAP and a volume SMA on caller-supplied OHLCV bars. Docs: https://www.brainiac.software/api/technical-analysis/volume-indicators",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "cmfPeriod": {
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "volumeSmaPeriod": {
            "type": "integer",
            "minimum": 1,
            "maximum": 20000
          },
          "vwapAnchor": {
            "default": "session",
            "type": "string",
            "enum": [
              "session",
              "none"
            ]
          },
          "sessionTz": {
            "default": "America/New_York",
            "type": "string"
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
      "name": "technical-analysis__volume-profile",
      "description": "Build a volume profile with POC and value area. Spread caller-supplied bar volume across equal price bins and return the histogram, point of control, and value area high and low. Docs: https://www.brainiac.software/api/technical-analysis/volume-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "rows": {
            "type": "integer",
            "minimum": 2,
            "maximum": 500
          },
          "tickSize": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "valueAreaPct": {
            "default": 0.7,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
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
      "name": "technical-analysis__pivot-points",
      "description": "Compute classic, Fibonacci, Woodie and Camarilla pivots. Compute floor, Fibonacci, Woodie and Camarilla pivot levels from the prior period's high, low and close. Docs: https://www.brainiac.software/api/technical-analysis/pivot-points",
      "parameters": {
        "type": "object",
        "properties": {
          "high": {
            "type": "number"
          },
          "low": {
            "type": "number"
          },
          "close": {
            "type": "number"
          },
          "open": {
            "type": "number"
          },
          "methods": {
            "default": [
              "classic",
              "fibonacci",
              "woodie",
              "camarilla"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "classic",
                "fibonacci",
                "woodie",
                "camarilla"
              ]
            }
          }
        },
        "required": [
          "high",
          "low",
          "close"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "technical-analysis__fibonacci-levels",
      "description": "Compute Fibonacci retracement and extension levels. Compute retracement and extension prices between a supplied swing low and high, or between the highest high and lowest low of caller-supplied bars. Docs: https://www.brainiac.software/api/technical-analysis/fibonacci-levels",
      "parameters": {
        "type": "object",
        "properties": {
          "swingLow": {
            "type": "number"
          },
          "swingHigh": {
            "type": "number"
          },
          "direction": {
            "default": "up",
            "type": "string",
            "enum": [
              "up",
              "down"
            ]
          },
          "levels": {
            "default": [
              0.236,
              0.382,
              0.5,
              0.618,
              0.786
            ],
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 10
            }
          },
          "extensions": {
            "default": [
              1.272,
              1.618
            ],
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 20
            }
          },
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "lookback": {
            "default": 100,
            "type": "integer",
            "minimum": 2,
            "maximum": 20000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "technical-analysis__candlestick-patterns",
      "description": "Detect candlestick patterns. Detect doji, hammer, shooting star, engulfing, harami, piercing line, dark cloud cover, morning/evening star, three white soldiers, three black crows and marubozu using explicit numeric thresholds you can override. Docs: https://www.brainiac.software/api/technical-analysis/candlestick-patterns",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "patterns": {
            "default": [
              "doji",
              "hammer",
              "shooting_star",
              "engulfing",
              "morning_star",
              "evening_star",
              "three_white_soldiers",
              "three_black_crows",
              "harami",
              "piercing_line",
              "dark_cloud_cover",
              "marubozu"
            ],
            "minItems": 1,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "doji",
                "hammer",
                "shooting_star",
                "engulfing",
                "bullish_engulfing",
                "bearish_engulfing",
                "morning_star",
                "evening_star",
                "three_white_soldiers",
                "three_black_crows",
                "harami",
                "bullish_harami",
                "bearish_harami",
                "piercing_line",
                "dark_cloud_cover",
                "marubozu"
              ]
            }
          },
          "trendLookback": {
            "default": 10,
            "type": "integer",
            "minimum": 2,
            "maximum": 1000
          },
          "thresholds": {
            "default": {
              "dojiBodyMax": 0.1,
              "hammerLowerShadowMin": 2,
              "hammerUpperShadowMax": 0.1,
              "starMiddleBodyMax": 0.3,
              "marubozuShadowMax": 0.05
            },
            "type": "object",
            "properties": {
              "dojiBodyMax": {
                "default": 0.1,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "hammerLowerShadowMin": {
                "default": 2,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "hammerUpperShadowMax": {
                "default": 0.1,
                "type": "number",
                "minimum": 0
              },
              "starMiddleBodyMax": {
                "default": 0.3,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "marubozuShadowMax": {
                "default": 0.05,
                "type": "number",
                "minimum": 0
              }
            },
            "additionalProperties": false
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
      "name": "technical-analysis__chart-patterns",
      "description": "Detect chart patterns from swing points. Find swing highs and lows, then detect double tops and bottoms, head and shoulders (and inverse), triangles and rectangles with necklines, targets and confirmation. Docs: https://www.brainiac.software/api/technical-analysis/chart-patterns",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "swingWindow": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          },
          "tolerance": {
            "default": 0.02,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "minBarsBetween": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 5000
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
      "name": "technical-analysis__support-resistance",
      "description": "Cluster support and resistance zones. Cluster swing highs and lows of caller-supplied bars into horizontal support and resistance zones with touch counts. Docs: https://www.brainiac.software/api/technical-analysis/support-resistance",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "swingWindow": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          },
          "zoneWidthPct": {
            "default": 0.005,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "minTouches": {
            "default": 2,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
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
      "name": "technical-analysis__strategy-backtest",
      "description": "Backtest a rule-based strategy. Backtest declarative entry and exit rules built from this product's indicators on caller-supplied bars, with next-open fills, fees, slippage, stops, trades, equity curve and metrics. Docs: https://www.brainiac.software/api/technical-analysis/strategy-backtest",
      "parameters": {
        "type": "object",
        "properties": {
          "bars": {
            "minItems": 2,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "t": {
                  "type": "string"
                },
                "o": {
                  "type": "number"
                },
                "h": {
                  "type": "number"
                },
                "l": {
                  "type": "number"
                },
                "c": {
                  "type": "number"
                },
                "v": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "t",
                "o",
                "h",
                "l",
                "c",
                "v"
              ],
              "additionalProperties": false
            }
          },
          "entry": {
            "type": "object",
            "properties": {
              "all": {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "indicator": {
                          "type": "string",
                          "enum": [
                            "close",
                            "open",
                            "high",
                            "low",
                            "volume",
                            "sma",
                            "ema",
                            "wma",
                            "dema",
                            "tema",
                            "hma",
                            "rsi",
                            "stochK",
                            "stochD",
                            "williamsR",
                            "cci",
                            "roc",
                            "mfi",
                            "macd",
                            "macdSignal",
                            "macdHistogram",
                            "bollingerUpper",
                            "bollingerMiddle",
                            "bollingerLower",
                            "percentB",
                            "bandwidth",
                            "keltnerUpper",
                            "keltnerMiddle",
                            "keltnerLower",
                            "donchianUpper",
                            "donchianMiddle",
                            "donchianLower",
                            "tr",
                            "atr",
                            "natr",
                            "hv",
                            "tenkan",
                            "kijun",
                            "senkouA",
                            "senkouB",
                            "adx",
                            "plusDI",
                            "minusDI",
                            "sar",
                            "aroonUp",
                            "aroonDown",
                            "supertrend",
                            "obv",
                            "adLine",
                            "cmf",
                            "vwap"
                          ]
                        },
                        "period": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "fast": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "slow": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "signal": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "atrPeriod": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "k": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "mult": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "op": {
                          "type": "string",
                          "enum": [
                            ">",
                            "<",
                            "crossAbove",
                            "crossBelow"
                          ]
                        },
                        "ref": {
                          "type": "object",
                          "properties": {
                            "indicator": {
                              "type": "string",
                              "enum": [
                                "close",
                                "open",
                                "high",
                                "low",
                                "volume",
                                "sma",
                                "ema",
                                "wma",
                                "dema",
                                "tema",
                                "hma",
                                "rsi",
                                "stochK",
                                "stochD",
                                "williamsR",
                                "cci",
                                "roc",
                                "mfi",
                                "macd",
                                "macdSignal",
                                "macdHistogram",
                                "bollingerUpper",
                                "bollingerMiddle",
                                "bollingerLower",
                                "percentB",
                                "bandwidth",
                                "keltnerUpper",
                                "keltnerMiddle",
                                "keltnerLower",
                                "donchianUpper",
                                "donchianMiddle",
                                "donchianLower",
                                "tr",
                                "atr",
                                "natr",
                                "hv",
                                "tenkan",
                                "kijun",
                                "senkouA",
                                "senkouB",
                                "adx",
                                "plusDI",
                                "minusDI",
                                "sar",
                                "aroonUp",
                                "aroonDown",
                                "supertrend",
                                "obv",
                                "adLine",
                                "cmf",
                                "vwap"
                              ]
                            },
                            "period": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "fast": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "slow": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "signal": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "atrPeriod": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "k": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            },
                            "mult": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            }
                          },
                          "required": [
                            "indicator"
                          ],
                          "additionalProperties": false
                        },
                        "value": {
                          "type": "number"
                        }
                      },
                      "required": [
                        "indicator",
                        "op"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "all": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        },
                        "any": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        }
                      },
                      "additionalProperties": false
                    }
                  ]
                }
              },
              "any": {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "indicator": {
                          "type": "string",
                          "enum": [
                            "close",
                            "open",
                            "high",
                            "low",
                            "volume",
                            "sma",
                            "ema",
                            "wma",
                            "dema",
                            "tema",
                            "hma",
                            "rsi",
                            "stochK",
                            "stochD",
                            "williamsR",
                            "cci",
                            "roc",
                            "mfi",
                            "macd",
                            "macdSignal",
                            "macdHistogram",
                            "bollingerUpper",
                            "bollingerMiddle",
                            "bollingerLower",
                            "percentB",
                            "bandwidth",
                            "keltnerUpper",
                            "keltnerMiddle",
                            "keltnerLower",
                            "donchianUpper",
                            "donchianMiddle",
                            "donchianLower",
                            "tr",
                            "atr",
                            "natr",
                            "hv",
                            "tenkan",
                            "kijun",
                            "senkouA",
                            "senkouB",
                            "adx",
                            "plusDI",
                            "minusDI",
                            "sar",
                            "aroonUp",
                            "aroonDown",
                            "supertrend",
                            "obv",
                            "adLine",
                            "cmf",
                            "vwap"
                          ]
                        },
                        "period": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "fast": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "slow": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "signal": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "atrPeriod": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "k": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "mult": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "op": {
                          "type": "string",
                          "enum": [
                            ">",
                            "<",
                            "crossAbove",
                            "crossBelow"
                          ]
                        },
                        "ref": {
                          "type": "object",
                          "properties": {
                            "indicator": {
                              "type": "string",
                              "enum": [
                                "close",
                                "open",
                                "high",
                                "low",
                                "volume",
                                "sma",
                                "ema",
                                "wma",
                                "dema",
                                "tema",
                                "hma",
                                "rsi",
                                "stochK",
                                "stochD",
                                "williamsR",
                                "cci",
                                "roc",
                                "mfi",
                                "macd",
                                "macdSignal",
                                "macdHistogram",
                                "bollingerUpper",
                                "bollingerMiddle",
                                "bollingerLower",
                                "percentB",
                                "bandwidth",
                                "keltnerUpper",
                                "keltnerMiddle",
                                "keltnerLower",
                                "donchianUpper",
                                "donchianMiddle",
                                "donchianLower",
                                "tr",
                                "atr",
                                "natr",
                                "hv",
                                "tenkan",
                                "kijun",
                                "senkouA",
                                "senkouB",
                                "adx",
                                "plusDI",
                                "minusDI",
                                "sar",
                                "aroonUp",
                                "aroonDown",
                                "supertrend",
                                "obv",
                                "adLine",
                                "cmf",
                                "vwap"
                              ]
                            },
                            "period": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "fast": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "slow": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "signal": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "atrPeriod": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "k": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            },
                            "mult": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            }
                          },
                          "required": [
                            "indicator"
                          ],
                          "additionalProperties": false
                        },
                        "value": {
                          "type": "number"
                        }
                      },
                      "required": [
                        "indicator",
                        "op"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "all": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        },
                        "any": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        }
                      },
                      "additionalProperties": false
                    }
                  ]
                }
              }
            },
            "additionalProperties": false
          },
          "exit": {
            "type": "object",
            "properties": {
              "all": {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "indicator": {
                          "type": "string",
                          "enum": [
                            "close",
                            "open",
                            "high",
                            "low",
                            "volume",
                            "sma",
                            "ema",
                            "wma",
                            "dema",
                            "tema",
                            "hma",
                            "rsi",
                            "stochK",
                            "stochD",
                            "williamsR",
                            "cci",
                            "roc",
                            "mfi",
                            "macd",
                            "macdSignal",
                            "macdHistogram",
                            "bollingerUpper",
                            "bollingerMiddle",
                            "bollingerLower",
                            "percentB",
                            "bandwidth",
                            "keltnerUpper",
                            "keltnerMiddle",
                            "keltnerLower",
                            "donchianUpper",
                            "donchianMiddle",
                            "donchianLower",
                            "tr",
                            "atr",
                            "natr",
                            "hv",
                            "tenkan",
                            "kijun",
                            "senkouA",
                            "senkouB",
                            "adx",
                            "plusDI",
                            "minusDI",
                            "sar",
                            "aroonUp",
                            "aroonDown",
                            "supertrend",
                            "obv",
                            "adLine",
                            "cmf",
                            "vwap"
                          ]
                        },
                        "period": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "fast": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "slow": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "signal": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "atrPeriod": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "k": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "mult": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "op": {
                          "type": "string",
                          "enum": [
                            ">",
                            "<",
                            "crossAbove",
                            "crossBelow"
                          ]
                        },
                        "ref": {
                          "type": "object",
                          "properties": {
                            "indicator": {
                              "type": "string",
                              "enum": [
                                "close",
                                "open",
                                "high",
                                "low",
                                "volume",
                                "sma",
                                "ema",
                                "wma",
                                "dema",
                                "tema",
                                "hma",
                                "rsi",
                                "stochK",
                                "stochD",
                                "williamsR",
                                "cci",
                                "roc",
                                "mfi",
                                "macd",
                                "macdSignal",
                                "macdHistogram",
                                "bollingerUpper",
                                "bollingerMiddle",
                                "bollingerLower",
                                "percentB",
                                "bandwidth",
                                "keltnerUpper",
                                "keltnerMiddle",
                                "keltnerLower",
                                "donchianUpper",
                                "donchianMiddle",
                                "donchianLower",
                                "tr",
                                "atr",
                                "natr",
                                "hv",
                                "tenkan",
                                "kijun",
                                "senkouA",
                                "senkouB",
                                "adx",
                                "plusDI",
                                "minusDI",
                                "sar",
                                "aroonUp",
                                "aroonDown",
                                "supertrend",
                                "obv",
                                "adLine",
                                "cmf",
                                "vwap"
                              ]
                            },
                            "period": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "fast": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "slow": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "signal": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "atrPeriod": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "k": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            },
                            "mult": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            }
                          },
                          "required": [
                            "indicator"
                          ],
                          "additionalProperties": false
                        },
                        "value": {
                          "type": "number"
                        }
                      },
                      "required": [
                        "indicator",
                        "op"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "all": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        },
                        "any": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        }
                      },
                      "additionalProperties": false
                    }
                  ]
                }
              },
              "any": {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "indicator": {
                          "type": "string",
                          "enum": [
                            "close",
                            "open",
                            "high",
                            "low",
                            "volume",
                            "sma",
                            "ema",
                            "wma",
                            "dema",
                            "tema",
                            "hma",
                            "rsi",
                            "stochK",
                            "stochD",
                            "williamsR",
                            "cci",
                            "roc",
                            "mfi",
                            "macd",
                            "macdSignal",
                            "macdHistogram",
                            "bollingerUpper",
                            "bollingerMiddle",
                            "bollingerLower",
                            "percentB",
                            "bandwidth",
                            "keltnerUpper",
                            "keltnerMiddle",
                            "keltnerLower",
                            "donchianUpper",
                            "donchianMiddle",
                            "donchianLower",
                            "tr",
                            "atr",
                            "natr",
                            "hv",
                            "tenkan",
                            "kijun",
                            "senkouA",
                            "senkouB",
                            "adx",
                            "plusDI",
                            "minusDI",
                            "sar",
                            "aroonUp",
                            "aroonDown",
                            "supertrend",
                            "obv",
                            "adLine",
                            "cmf",
                            "vwap"
                          ]
                        },
                        "period": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "fast": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "slow": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "signal": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "atrPeriod": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 20000
                        },
                        "k": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "mult": {
                          "type": "number",
                          "exclusiveMinimum": 0
                        },
                        "op": {
                          "type": "string",
                          "enum": [
                            ">",
                            "<",
                            "crossAbove",
                            "crossBelow"
                          ]
                        },
                        "ref": {
                          "type": "object",
                          "properties": {
                            "indicator": {
                              "type": "string",
                              "enum": [
                                "close",
                                "open",
                                "high",
                                "low",
                                "volume",
                                "sma",
                                "ema",
                                "wma",
                                "dema",
                                "tema",
                                "hma",
                                "rsi",
                                "stochK",
                                "stochD",
                                "williamsR",
                                "cci",
                                "roc",
                                "mfi",
                                "macd",
                                "macdSignal",
                                "macdHistogram",
                                "bollingerUpper",
                                "bollingerMiddle",
                                "bollingerLower",
                                "percentB",
                                "bandwidth",
                                "keltnerUpper",
                                "keltnerMiddle",
                                "keltnerLower",
                                "donchianUpper",
                                "donchianMiddle",
                                "donchianLower",
                                "tr",
                                "atr",
                                "natr",
                                "hv",
                                "tenkan",
                                "kijun",
                                "senkouA",
                                "senkouB",
                                "adx",
                                "plusDI",
                                "minusDI",
                                "sar",
                                "aroonUp",
                                "aroonDown",
                                "supertrend",
                                "obv",
                                "adLine",
                                "cmf",
                                "vwap"
                              ]
                            },
                            "period": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "fast": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "slow": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "signal": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "atrPeriod": {
                              "type": "integer",
                              "minimum": 1,
                              "maximum": 20000
                            },
                            "k": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            },
                            "mult": {
                              "type": "number",
                              "exclusiveMinimum": 0
                            }
                          },
                          "required": [
                            "indicator"
                          ],
                          "additionalProperties": false
                        },
                        "value": {
                          "type": "number"
                        }
                      },
                      "required": [
                        "indicator",
                        "op"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "all": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        },
                        "any": {
                          "minItems": 1,
                          "maxItems": 20,
                          "type": "array",
                          "items": {
                            "anyOf": [
                              {
                                "type": "object",
                                "properties": {
                                  "indicator": {
                                    "type": "string",
                                    "enum": [
                                      "close",
                                      "open",
                                      "high",
                                      "low",
                                      "volume",
                                      "sma",
                                      "ema",
                                      "wma",
                                      "dema",
                                      "tema",
                                      "hma",
                                      "rsi",
                                      "stochK",
                                      "stochD",
                                      "williamsR",
                                      "cci",
                                      "roc",
                                      "mfi",
                                      "macd",
                                      "macdSignal",
                                      "macdHistogram",
                                      "bollingerUpper",
                                      "bollingerMiddle",
                                      "bollingerLower",
                                      "percentB",
                                      "bandwidth",
                                      "keltnerUpper",
                                      "keltnerMiddle",
                                      "keltnerLower",
                                      "donchianUpper",
                                      "donchianMiddle",
                                      "donchianLower",
                                      "tr",
                                      "atr",
                                      "natr",
                                      "hv",
                                      "tenkan",
                                      "kijun",
                                      "senkouA",
                                      "senkouB",
                                      "adx",
                                      "plusDI",
                                      "minusDI",
                                      "sar",
                                      "aroonUp",
                                      "aroonDown",
                                      "supertrend",
                                      "obv",
                                      "adLine",
                                      "cmf",
                                      "vwap"
                                    ]
                                  },
                                  "period": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "fast": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "slow": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "signal": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "atrPeriod": {
                                    "type": "integer",
                                    "minimum": 1,
                                    "maximum": 20000
                                  },
                                  "k": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "mult": {
                                    "type": "number",
                                    "exclusiveMinimum": 0
                                  },
                                  "op": {
                                    "type": "string",
                                    "enum": [
                                      ">",
                                      "<",
                                      "crossAbove",
                                      "crossBelow"
                                    ]
                                  },
                                  "ref": {
                                    "type": "object",
                                    "properties": {
                                      "indicator": {
                                        "type": "string",
                                        "enum": [
                                          "close",
                                          "open",
                                          "high",
                                          "low",
                                          "volume",
                                          "sma",
                                          "ema",
                                          "wma",
                                          "dema",
                                          "tema",
                                          "hma",
                                          "rsi",
                                          "stochK",
                                          "stochD",
                                          "williamsR",
                                          "cci",
                                          "roc",
                                          "mfi",
                                          "macd",
                                          "macdSignal",
                                          "macdHistogram",
                                          "bollingerUpper",
                                          "bollingerMiddle",
                                          "bollingerLower",
                                          "percentB",
                                          "bandwidth",
                                          "keltnerUpper",
                                          "keltnerMiddle",
                                          "keltnerLower",
                                          "donchianUpper",
                                          "donchianMiddle",
                                          "donchianLower",
                                          "tr",
                                          "atr",
                                          "natr",
                                          "hv",
                                          "tenkan",
                                          "kijun",
                                          "senkouA",
                                          "senkouB",
                                          "adx",
                                          "plusDI",
                                          "minusDI",
                                          "sar",
                                          "aroonUp",
                                          "aroonDown",
                                          "supertrend",
                                          "obv",
                                          "adLine",
                                          "cmf",
                                          "vwap"
                                        ]
                                      },
                                      "period": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "fast": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "slow": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "signal": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "atrPeriod": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 20000
                                      },
                                      "k": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      },
                                      "mult": {
                                        "type": "number",
                                        "exclusiveMinimum": 0
                                      }
                                    },
                                    "required": [
                                      "indicator"
                                    ],
                                    "additionalProperties": false
                                  },
                                  "value": {
                                    "type": "number"
                                  }
                                },
                                "required": [
                                  "indicator",
                                  "op"
                                ],
                                "additionalProperties": false
                              },
                              {
                                "type": "object",
                                "properties": {
                                  "all": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  },
                                  "any": {
                                    "minItems": 1,
                                    "maxItems": 20,
                                    "type": "array",
                                    "items": {
                                      "type": "object",
                                      "properties": {
                                        "indicator": {
                                          "type": "string",
                                          "enum": [
                                            "close",
                                            "open",
                                            "high",
                                            "low",
                                            "volume",
                                            "sma",
                                            "ema",
                                            "wma",
                                            "dema",
                                            "tema",
                                            "hma",
                                            "rsi",
                                            "stochK",
                                            "stochD",
                                            "williamsR",
                                            "cci",
                                            "roc",
                                            "mfi",
                                            "macd",
                                            "macdSignal",
                                            "macdHistogram",
                                            "bollingerUpper",
                                            "bollingerMiddle",
                                            "bollingerLower",
                                            "percentB",
                                            "bandwidth",
                                            "keltnerUpper",
                                            "keltnerMiddle",
                                            "keltnerLower",
                                            "donchianUpper",
                                            "donchianMiddle",
                                            "donchianLower",
                                            "tr",
                                            "atr",
                                            "natr",
                                            "hv",
                                            "tenkan",
                                            "kijun",
                                            "senkouA",
                                            "senkouB",
                                            "adx",
                                            "plusDI",
                                            "minusDI",
                                            "sar",
                                            "aroonUp",
                                            "aroonDown",
                                            "supertrend",
                                            "obv",
                                            "adLine",
                                            "cmf",
                                            "vwap"
                                          ]
                                        },
                                        "period": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "fast": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "slow": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "signal": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "atrPeriod": {
                                          "type": "integer",
                                          "minimum": 1,
                                          "maximum": 20000
                                        },
                                        "k": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "mult": {
                                          "type": "number",
                                          "exclusiveMinimum": 0
                                        },
                                        "op": {
                                          "type": "string",
                                          "enum": [
                                            ">",
                                            "<",
                                            "crossAbove",
                                            "crossBelow"
                                          ]
                                        },
                                        "ref": {
                                          "type": "object",
                                          "properties": {
                                            "indicator": {
                                              "type": "string",
                                              "enum": [
                                                "close",
                                                "open",
                                                "high",
                                                "low",
                                                "volume",
                                                "sma",
                                                "ema",
                                                "wma",
                                                "dema",
                                                "tema",
                                                "hma",
                                                "rsi",
                                                "stochK",
                                                "stochD",
                                                "williamsR",
                                                "cci",
                                                "roc",
                                                "mfi",
                                                "macd",
                                                "macdSignal",
                                                "macdHistogram",
                                                "bollingerUpper",
                                                "bollingerMiddle",
                                                "bollingerLower",
                                                "percentB",
                                                "bandwidth",
                                                "keltnerUpper",
                                                "keltnerMiddle",
                                                "keltnerLower",
                                                "donchianUpper",
                                                "donchianMiddle",
                                                "donchianLower",
                                                "tr",
                                                "atr",
                                                "natr",
                                                "hv",
                                                "tenkan",
                                                "kijun",
                                                "senkouA",
                                                "senkouB",
                                                "adx",
                                                "plusDI",
                                                "minusDI",
                                                "sar",
                                                "aroonUp",
                                                "aroonDown",
                                                "supertrend",
                                                "obv",
                                                "adLine",
                                                "cmf",
                                                "vwap"
                                              ]
                                            },
                                            "period": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "fast": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "slow": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "signal": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "atrPeriod": {
                                              "type": "integer",
                                              "minimum": 1,
                                              "maximum": 20000
                                            },
                                            "k": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            },
                                            "mult": {
                                              "type": "number",
                                              "exclusiveMinimum": 0
                                            }
                                          },
                                          "required": [
                                            "indicator"
                                          ],
                                          "additionalProperties": false
                                        },
                                        "value": {
                                          "type": "number"
                                        }
                                      },
                                      "required": [
                                        "indicator",
                                        "op"
                                      ],
                                      "additionalProperties": false
                                    }
                                  }
                                },
                                "additionalProperties": false
                              }
                            ]
                          }
                        }
                      },
                      "additionalProperties": false
                    }
                  ]
                }
              }
            },
            "additionalProperties": false
          },
          "side": {
            "default": "long",
            "type": "string",
            "enum": [
              "long",
              "short"
            ]
          },
          "initialCapital": {
            "default": 10000,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "positionSize": {
            "default": {
              "type": "percentEquity",
              "value": 1
            },
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "enum": [
                  "percentEquity",
                  "fixedNotional",
                  "fixedQty"
                ]
              },
              "value": {
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "required": [
              "type",
              "value"
            ],
            "additionalProperties": false
          },
          "feePct": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 0.5
          },
          "slippagePct": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 0.5
          },
          "stopLossPct": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1
              },
              {
                "type": "null"
              }
            ]
          },
          "takeProfitPct": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "bars",
          "entry"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "technical-analysis__moving-averages": "0.02",
  "technical-analysis__momentum-oscillators": "0.03",
  "technical-analysis__macd": "0.02",
  "technical-analysis__bands-channels": "0.03",
  "technical-analysis__volatility-measures": "0.02",
  "technical-analysis__ichimoku": "0.03",
  "technical-analysis__trend-indicators": "0.04",
  "technical-analysis__volume-indicators": "0.03",
  "technical-analysis__volume-profile": "0.03",
  "technical-analysis__pivot-points": "0.02",
  "technical-analysis__fibonacci-levels": "0.02",
  "technical-analysis__candlestick-patterns": "0.04",
  "technical-analysis__chart-patterns": "0.05",
  "technical-analysis__support-resistance": "0.03",
  "technical-analysis__strategy-backtest": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "technical-analysis__moving-averages": "technical-analysis/moving-averages",
  "technical-analysis__momentum-oscillators": "technical-analysis/momentum-oscillators",
  "technical-analysis__macd": "technical-analysis/macd",
  "technical-analysis__bands-channels": "technical-analysis/bands-channels",
  "technical-analysis__volatility-measures": "technical-analysis/volatility-measures",
  "technical-analysis__ichimoku": "technical-analysis/ichimoku",
  "technical-analysis__trend-indicators": "technical-analysis/trend-indicators",
  "technical-analysis__volume-indicators": "technical-analysis/volume-indicators",
  "technical-analysis__volume-profile": "technical-analysis/volume-profile",
  "technical-analysis__pivot-points": "technical-analysis/pivot-points",
  "technical-analysis__fibonacci-levels": "technical-analysis/fibonacci-levels",
  "technical-analysis__candlestick-patterns": "technical-analysis/candlestick-patterns",
  "technical-analysis__chart-patterns": "technical-analysis/chart-patterns",
  "technical-analysis__support-resistance": "technical-analysis/support-resistance",
  "technical-analysis__strategy-backtest": "technical-analysis/strategy-backtest"
}


class BrainiacTechnicalAnalysisAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — technical-analysis",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the technical-analysis catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "technical-analysis", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Compute moving averages (SMA, EMA, WMA, DEMA, TEMA, HMA)"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the technical-analysis group. "
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
