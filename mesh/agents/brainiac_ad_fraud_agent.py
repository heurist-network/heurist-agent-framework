"""Auto-generated BRAINIAC Heurist Mesh agent for group `ad-fraud` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "ad-fraud__bot-detect",
      "description": "Detect ad-click automation signals. Look for automation indicators in caller-supplied HTTP and browser signals. An IP address is ignored. A User-Agent token is a string match, not proof of a bot. Docs: https://www.brainiac.software/api/ad-fraud/bot-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "signals": {
            "type": "object",
            "properties": {
              "userAgent": {
                "type": "string",
                "maxLength": 400
              },
              "acceptLanguage": {
                "type": "string",
                "maxLength": 200
              },
              "webdriver": {
                "type": "boolean"
              },
              "headless": {
                "type": "boolean"
              },
              "automationFlags": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "pluginsCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 500
              },
              "languages": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "hardwareConcurrency": {
                "type": "integer",
                "minimum": 0,
                "maximum": 512
              },
              "deviceMemory": {
                "type": "number",
                "minimum": 0,
                "maximum": 1024
              },
              "maxTouchPoints": {
                "type": "integer",
                "minimum": 0,
                "maximum": 32
              },
              "screenWidth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "screenHeight": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "mouseMoves": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "keyCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "scrollCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "clickCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "timeOnPageMs": {
                "type": "integer",
                "minimum": 0,
                "maximum": 86400000
              },
              "ip": {
                "type": "string",
                "maxLength": 80
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "signals"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__browser-integrity-check",
      "description": "Check browser property consistency. Compare caller-supplied browser properties for contradictions. The User-Agent is not verified, and a timezone offset is not a location. Docs: https://www.brainiac.software/api/ad-fraud/browser-integrity-check",
      "parameters": {
        "type": "object",
        "properties": {
          "browser": {
            "type": "object",
            "properties": {
              "userAgent": {
                "type": "string",
                "maxLength": 400
              },
              "platform": {
                "type": "string",
                "maxLength": 80
              },
              "vendor": {
                "type": "string",
                "maxLength": 80
              },
              "language": {
                "type": "string",
                "maxLength": 40
              },
              "languages": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "timezone": {
                "type": "string",
                "maxLength": 80
              },
              "timezoneOffsetMinutes": {
                "type": "integer",
                "minimum": -840,
                "maximum": 840
              },
              "screenWidth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "screenHeight": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "colorDepth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 64
              },
              "devicePixelRatio": {
                "type": "number",
                "minimum": 0,
                "maximum": 10
              },
              "hardwareConcurrency": {
                "type": "integer",
                "minimum": 0,
                "maximum": 512
              },
              "deviceMemory": {
                "type": "number",
                "minimum": 0,
                "maximum": 1024
              },
              "maxTouchPoints": {
                "type": "integer",
                "minimum": 0,
                "maximum": 32
              },
              "brands": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "brand": {
                      "type": "string",
                      "maxLength": 40
                    },
                    "version": {
                      "type": "string",
                      "maxLength": 20
                    }
                  },
                  "required": [
                    "brand"
                  ],
                  "additionalProperties": false
                }
              },
              "uaPlatform": {
                "type": "string",
                "maxLength": 40
              },
              "webglVendor": {
                "type": "string",
                "maxLength": 120
              },
              "webglRenderer": {
                "type": "string",
                "maxLength": 160
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "browser"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__device-consistency-check",
      "description": "Check device characteristic consistency. Compare caller-supplied device type, OS, model, screen, and architecture. No device identity is looked up. Docs: https://www.brainiac.software/api/ad-fraud/device-consistency-check",
      "parameters": {
        "type": "object",
        "properties": {
          "device": {
            "type": "object",
            "properties": {
              "deviceType": {
                "type": "string",
                "enum": [
                  "phone",
                  "tablet",
                  "desktop",
                  "tv",
                  "other"
                ]
              },
              "os": {
                "type": "string",
                "maxLength": 40
              },
              "osVersion": {
                "type": "string",
                "maxLength": 40
              },
              "model": {
                "type": "string",
                "maxLength": 80
              },
              "architecture": {
                "type": "string",
                "maxLength": 40
              },
              "simulator": {
                "type": "boolean"
              },
              "screenWidth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "screenHeight": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "pixelRatio": {
                "type": "number",
                "minimum": 0,
                "maximum": 10
              },
              "touch": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "device"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__click-timing-analyze",
      "description": "Analyze click timing. Check caller-supplied click timestamps and dwell for impossible order or a fixed short gap. One fast click is a weak indicator, not a campaign pattern. Docs: https://www.brainiac.software/api/ad-fraud/click-timing-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "clicks": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "dwellMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "timeToClickMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "pageLoadAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "x": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "y": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fingerprintId": {
                  "type": "string",
                  "maxLength": 120
                },
                "referrer": {
                  "type": "string",
                  "maxLength": 500
                },
                "landingUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "clicks"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__duplicate-click-detect",
      "description": "Detect duplicate click identifiers. Find repeated click ids, gclids, and fbclids in the supplied batch and optional history. Nothing is stored between calls. Docs: https://www.brainiac.software/api/ad-fraud/duplicate-click-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "clicks": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "dwellMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "timeToClickMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "pageLoadAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "x": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "y": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fingerprintId": {
                  "type": "string",
                  "maxLength": 120
                },
                "referrer": {
                  "type": "string",
                  "maxLength": 500
                },
                "landingUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "history": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          }
        },
        "required": [
          "clicks"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__click-velocity-analyze",
      "description": "Analyze click velocity. Count timestamped clicks inside a supplied window. A burst is a frequency calculation, not proof of automation. Clicks are not grouped by IP. Docs: https://www.brainiac.software/api/ad-fraud/click-velocity-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "clicks": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "dwellMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "timeToClickMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "pageLoadAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "x": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "y": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fingerprintId": {
                  "type": "string",
                  "maxLength": 120
                },
                "referrer": {
                  "type": "string",
                  "maxLength": 500
                },
                "landingUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "windowSeconds": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3600
          },
          "threshold": {
            "type": "integer",
            "minimum": 3,
            "maximum": 500
          },
          "groupBy": {
            "type": "string",
            "enum": [
              "none",
              "campaign",
              "fingerprint"
            ]
          }
        },
        "required": [
          "clicks"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__referrer-integrity-check",
      "description": "Check referrer and campaign consistency. Compare a caller-supplied referrer, landing URL, and campaign source. URLs are not fetched. A family mismatch is a heuristic, not a verified referrer. Docs: https://www.brainiac.software/api/ad-fraud/referrer-integrity-check",
      "parameters": {
        "type": "object",
        "properties": {
          "referrer": {
            "type": "string",
            "maxLength": 500
          },
          "landingUrl": {
            "type": "string",
            "maxLength": 500
          },
          "campaign": {
            "type": "object",
            "properties": {
              "source": {
                "type": "string",
                "maxLength": 80
              },
              "medium": {
                "type": "string",
                "maxLength": 40
              },
              "name": {
                "type": "string",
                "maxLength": 80
              }
            },
            "additionalProperties": false
          },
          "expectedHosts": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "ad-fraud__click-fingerprint-analyze",
      "description": "Compare click fingerprints. Compare caller-supplied canvas, WebGL, audio, and font hashes. Hashes are not computed here, and a match is not a device identity. Docs: https://www.brainiac.software/api/ad-fraud/click-fingerprint-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "fingerprints": {
            "minItems": 1,
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "canvasHash": {
                  "type": "string",
                  "maxLength": 128
                },
                "webglHash": {
                  "type": "string",
                  "maxLength": 128
                },
                "audioHash": {
                  "type": "string",
                  "maxLength": 128
                },
                "fontHash": {
                  "type": "string",
                  "maxLength": 128
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 400
                },
                "screenWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "screenHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "timezone": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "fingerprints"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__conversion-fraud-detect",
      "description": "Detect click and conversion disagreements. Compare caller-supplied clicks and conversions for time order, campaign mismatch, and repeated ids. An unmatched conversion is a missing link, not proof the click never happened. Docs: https://www.brainiac.software/api/ad-fraud/conversion-fraud-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "clicks": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "dwellMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "timeToClickMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "pageLoadAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "x": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "y": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fingerprintId": {
                  "type": "string",
                  "maxLength": 120
                },
                "referrer": {
                  "type": "string",
                  "maxLength": 500
                },
                "landingUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "conversions": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "conversions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__campaign-anomaly-detect",
      "description": "Detect campaign metric anomalies. Find impossible ratios and, when at least eight rows have clicks and impressions, click-through-rate outliers. An outlier is a statistic, not a fraud verdict. Docs: https://www.brainiac.software/api/ad-fraud/campaign-anomaly-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "rows": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "day": {
                  "type": "string",
                  "maxLength": 20
                },
                "clicks": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "spend": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "rows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__click-pattern-detect",
      "description": "Detect repeated click patterns. Look for identical timestamps, a fixed gap, or identical coordinates across a supplied click collection. Fewer than five usable clicks is insufficient. Docs: https://www.brainiac.software/api/ad-fraud/click-pattern-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "clicks": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "dwellMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "timeToClickMs": {
                  "type": "integer",
                  "minimum": -1000000,
                  "maximum": 86400000
                },
                "pageLoadAt": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 40
                },
                "x": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "y": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 20000
                },
                "campaignId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fingerprintId": {
                  "type": "string",
                  "maxLength": 120
                },
                "referrer": {
                  "type": "string",
                  "maxLength": 500
                },
                "landingUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "clicks"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ad-fraud__click-risk-score",
      "description": "Score supplied click risk. Sum a documented weight for each supplied click attribute. Missing data adds no points. The score is not a probability of fraud. Docs: https://www.brainiac.software/api/ad-fraud/click-risk-score",
      "parameters": {
        "type": "object",
        "properties": {
          "click": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "at": {
                "type": "string",
                "minLength": 8,
                "maxLength": 40
              },
              "clickId": {
                "type": "string",
                "maxLength": 160
              },
              "gclid": {
                "type": "string",
                "maxLength": 200
              },
              "fbclid": {
                "type": "string",
                "maxLength": 200
              },
              "dwellMs": {
                "type": "integer",
                "minimum": -1000000,
                "maximum": 86400000
              },
              "timeToClickMs": {
                "type": "integer",
                "minimum": -1000000,
                "maximum": 86400000
              },
              "pageLoadAt": {
                "type": "string",
                "minLength": 8,
                "maxLength": 40
              },
              "x": {
                "type": "number",
                "minimum": 0,
                "maximum": 20000
              },
              "y": {
                "type": "number",
                "minimum": 0,
                "maximum": 20000
              },
              "campaignId": {
                "type": "string",
                "maxLength": 80
              },
              "fingerprintId": {
                "type": "string",
                "maxLength": 120
              },
              "referrer": {
                "type": "string",
                "maxLength": 500
              },
              "landingUrl": {
                "type": "string",
                "maxLength": 500
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "signals": {
            "type": "object",
            "properties": {
              "userAgent": {
                "type": "string",
                "maxLength": 400
              },
              "acceptLanguage": {
                "type": "string",
                "maxLength": 200
              },
              "webdriver": {
                "type": "boolean"
              },
              "headless": {
                "type": "boolean"
              },
              "automationFlags": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "pluginsCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 500
              },
              "languages": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "hardwareConcurrency": {
                "type": "integer",
                "minimum": 0,
                "maximum": 512
              },
              "deviceMemory": {
                "type": "number",
                "minimum": 0,
                "maximum": 1024
              },
              "maxTouchPoints": {
                "type": "integer",
                "minimum": 0,
                "maximum": 32
              },
              "screenWidth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "screenHeight": {
                "type": "integer",
                "minimum": 0,
                "maximum": 20000
              },
              "mouseMoves": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "keyCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "scrollCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "clickCount": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "timeOnPageMs": {
                "type": "integer",
                "minimum": 0,
                "maximum": 86400000
              },
              "ip": {
                "type": "string",
                "maxLength": 80
              }
            },
            "additionalProperties": false
          },
          "history": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "clickId": {
                  "type": "string",
                  "maxLength": 160
                },
                "gclid": {
                  "type": "string",
                  "maxLength": 200
                },
                "fbclid": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "conversion": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "at": {
                "type": "string",
                "minLength": 8,
                "maxLength": 40
              },
              "clickId": {
                "type": "string",
                "maxLength": 160
              },
              "campaignId": {
                "type": "string",
                "maxLength": 80
              },
              "value": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "referrer": {
            "type": "string",
            "maxLength": 500
          },
          "landingUrl": {
            "type": "string",
            "maxLength": 500
          },
          "campaign": {
            "type": "object",
            "properties": {
              "source": {
                "type": "string",
                "maxLength": 80
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "click"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "ad-fraud__bot-detect": "0.03",
  "ad-fraud__browser-integrity-check": "0.03",
  "ad-fraud__device-consistency-check": "0.03",
  "ad-fraud__click-timing-analyze": "0.03",
  "ad-fraud__duplicate-click-detect": "0.03",
  "ad-fraud__click-velocity-analyze": "0.04",
  "ad-fraud__referrer-integrity-check": "0.03",
  "ad-fraud__click-fingerprint-analyze": "0.04",
  "ad-fraud__conversion-fraud-detect": "0.04",
  "ad-fraud__campaign-anomaly-detect": "0.04",
  "ad-fraud__click-pattern-detect": "0.04",
  "ad-fraud__click-risk-score": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "ad-fraud__bot-detect": "ad-fraud/bot-detect",
  "ad-fraud__browser-integrity-check": "ad-fraud/browser-integrity-check",
  "ad-fraud__device-consistency-check": "ad-fraud/device-consistency-check",
  "ad-fraud__click-timing-analyze": "ad-fraud/click-timing-analyze",
  "ad-fraud__duplicate-click-detect": "ad-fraud/duplicate-click-detect",
  "ad-fraud__click-velocity-analyze": "ad-fraud/click-velocity-analyze",
  "ad-fraud__referrer-integrity-check": "ad-fraud/referrer-integrity-check",
  "ad-fraud__click-fingerprint-analyze": "ad-fraud/click-fingerprint-analyze",
  "ad-fraud__conversion-fraud-detect": "ad-fraud/conversion-fraud-detect",
  "ad-fraud__campaign-anomaly-detect": "ad-fraud/campaign-anomaly-detect",
  "ad-fraud__click-pattern-detect": "ad-fraud/click-pattern-detect",
  "ad-fraud__click-risk-score": "ad-fraud/click-risk-score"
}


class BrainiacAdFraudAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — ad-fraud",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the ad-fraud catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "ad-fraud", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect ad-click automation signals"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the ad-fraud group. "
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
