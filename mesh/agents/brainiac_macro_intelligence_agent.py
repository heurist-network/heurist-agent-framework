"""Auto-generated BRAINIAC Heurist Mesh agent for group `macro-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "macro-intelligence__central-bank-rate-compare",
      "description": "Compare central bank rates. Compare supplied policy rates across countries and banks. Missing previous rates leave change blank rather than inventing values. Docs: https://www.brainiac.software/api/macro-intelligence/central-bank-rate-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__yield-curve-analyze",
      "description": "Analyze yield curves. Analyze supplied sovereign yield tenors for slope, curvature, and curve shape without inventing missing points. Docs: https://www.brainiac.software/api/macro-intelligence/yield-curve-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__inflation-series-compare",
      "description": "Compare inflation series. Compare supplied CPI or inflation observations by country using the latest and previous points only. Docs: https://www.brainiac.software/api/macro-intelligence/inflation-series-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__economic-indicator-release-track",
      "description": "Track economic indicator releases. Track supplied indicator release dates with actual, consensus, and previous values when present. Docs: https://www.brainiac.software/api/macro-intelligence/economic-indicator-release-track",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__surprise-calculate",
      "description": "Calculate macro surprises. Calculate actual-minus-consensus surprises from supplied releases and optional z-scores against the sample stdev. Docs: https://www.brainiac.software/api/macro-intelligence/surprise-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__currency-purchasing-power-compare",
      "description": "Compare currency purchasing power. Compare supplied price indexes adjusted by FX-per-USD values. Missing FX or price indexes are not invented. Docs: https://www.brainiac.software/api/macro-intelligence/currency-purchasing-power-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__country-risk-profile",
      "description": "Profile country macro risk. Summarize supplied inflation, policy rates, and debt into a descriptive risk level. This is not a credit rating. Docs: https://www.brainiac.software/api/macro-intelligence/country-risk-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__sovereign-debt-maturity-analyze",
      "description": "Analyze sovereign debt maturity. Bucket supplied sovereign debt amounts by maturity window from the as-of date without inventing missing maturities. Docs: https://www.brainiac.software/api/macro-intelligence/sovereign-debt-maturity-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__commodity-price-transmission-analyze",
      "description": "Analyze commodity price transmission. Compare supplied commodity price changes with inflation observation changes. Causation is not claimed. Docs: https://www.brainiac.software/api/macro-intelligence/commodity-price-transmission-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__event-impact-timeline",
      "description": "Build macro event impact timeline. Place supplied macro events on a timeline and attach nearby observations within 45 days. Causation is not claimed. Docs: https://www.brainiac.software/api/macro-intelligence/event-impact-timeline",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "series": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "frequency": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "observations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "seriesId": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "bank": {
                  "type": "string",
                  "maxLength": 160
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "previousRate": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "tenors": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "tenor": {
                  "type": "string",
                  "maxLength": 40
                },
                "yieldPct": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "releases": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "indicator": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "releaseDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "actual": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "consensus": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "previous": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "priceLevels": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "priceIndex": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fxPerUsd": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "debt": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "instrument": {
                  "type": "string",
                  "maxLength": 160
                },
                "maturityDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "coupon": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "commodities": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 60
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__us-treasury-debt",
      "description": "US Treasury debt to the penny. Latest US public debt outstanding from the official Treasury Fiscal Data debt_to_penny series. Docs: https://www.brainiac.software/api/macro-intelligence/us-treasury-debt",
      "parameters": {
        "type": "object",
        "properties": {
          "recordDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__us-treasury-yield-curve",
      "description": "US Treasury yield curve. Latest official US Treasury daily par yield curve from the Treasury XML feed. Optional recordDate. Returns published tenors from 1 month to 30 years and optional derived 10Y-2Y / 10Y-3M spreads. Not a forecast. Docs: https://www.brainiac.software/api/macro-intelligence/us-treasury-yield-curve",
      "parameters": {
        "type": "object",
        "properties": {
          "recordDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__central-bank-policy-rates",
      "description": "Central bank policy rates. Fetch official BIS WS_CBPOL central-bank policy rates. Optional area and freq. Discontinued national euro-area series are not returned as current; use XM for the euro area. Docs: https://www.brainiac.software/api/macro-intelligence/central-bank-policy-rates",
      "parameters": {
        "type": "object",
        "properties": {
          "area": {
            "type": "string",
            "minLength": 2,
            "maxLength": 8
          },
          "freq": {
            "type": "string",
            "enum": [
              "D",
              "M"
            ]
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 10
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "macro-intelligence__ny-fed-reference-rates",
      "description": "NY Fed reference rates. Latest published New York Fed reference rates including SOFR and EFFR from the official Markets API. Docs: https://www.brainiac.software/api/macro-intelligence/ny-fed-reference-rates",
      "parameters": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "macro-intelligence__central-bank-rate-compare": "0.04",
  "macro-intelligence__yield-curve-analyze": "0.05",
  "macro-intelligence__inflation-series-compare": "0.04",
  "macro-intelligence__economic-indicator-release-track": "0.04",
  "macro-intelligence__surprise-calculate": "0.05",
  "macro-intelligence__currency-purchasing-power-compare": "0.05",
  "macro-intelligence__country-risk-profile": "0.05",
  "macro-intelligence__sovereign-debt-maturity-analyze": "0.04",
  "macro-intelligence__commodity-price-transmission-analyze": "0.05",
  "macro-intelligence__event-impact-timeline": "0.05",
  "macro-intelligence__us-treasury-debt": "0.001",
  "macro-intelligence__us-treasury-yield-curve": "0.0014",
  "macro-intelligence__central-bank-policy-rates": "0.012",
  "macro-intelligence__ny-fed-reference-rates": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "macro-intelligence__central-bank-rate-compare": "macro-intelligence/central-bank-rate-compare",
  "macro-intelligence__yield-curve-analyze": "macro-intelligence/yield-curve-analyze",
  "macro-intelligence__inflation-series-compare": "macro-intelligence/inflation-series-compare",
  "macro-intelligence__economic-indicator-release-track": "macro-intelligence/economic-indicator-release-track",
  "macro-intelligence__surprise-calculate": "macro-intelligence/surprise-calculate",
  "macro-intelligence__currency-purchasing-power-compare": "macro-intelligence/currency-purchasing-power-compare",
  "macro-intelligence__country-risk-profile": "macro-intelligence/country-risk-profile",
  "macro-intelligence__sovereign-debt-maturity-analyze": "macro-intelligence/sovereign-debt-maturity-analyze",
  "macro-intelligence__commodity-price-transmission-analyze": "macro-intelligence/commodity-price-transmission-analyze",
  "macro-intelligence__event-impact-timeline": "macro-intelligence/event-impact-timeline",
  "macro-intelligence__us-treasury-debt": "macro-intelligence/us-treasury-debt",
  "macro-intelligence__us-treasury-yield-curve": "macro-intelligence/us-treasury-yield-curve",
  "macro-intelligence__central-bank-policy-rates": "macro-intelligence/central-bank-policy-rates",
  "macro-intelligence__ny-fed-reference-rates": "macro-intelligence/ny-fed-reference-rates"
}


class BrainiacMacroIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — macro-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the macro-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "macro-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Compare central bank rates"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the macro-intelligence group. "
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
