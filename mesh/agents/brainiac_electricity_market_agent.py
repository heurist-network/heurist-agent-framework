"""Auto-generated BRAINIAC Heurist Mesh agent for group `electricity-market` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "electricity-market__price-series-normalize",
      "description": "Normalize electricity price series. Normalize caller-supplied electricity market prices with explicit units and timestamps. Missing prices are not invented. Docs: https://www.brainiac.software/api/electricity-market/price-series-normalize",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__price-compare",
      "description": "Compare electricity market prices. Compare average and latest electricity prices across supplied markets or regions. Missing values are not invented. Docs: https://www.brainiac.software/api/electricity-market/price-compare",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__demand-profile-analyze",
      "description": "Analyze electricity demand profiles. Analyze supplied demand observations for average, peak, minimum, and load factor by region. Missing megawatts are not invented. Docs: https://www.brainiac.software/api/electricity-market/demand-profile-analyze",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__carbon-intensity-track",
      "description": "Track grid carbon intensity. Track supplied carbon intensity points, optionally supplemented by the key-free Carbon Intensity API when requested. Docs: https://www.brainiac.software/api/electricity-market/carbon-intensity-track",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__bill-tariff-reconcile",
      "description": "Reconcile electricity bills to tariffs. Reconcile billed totals to tariff-implied energy, demand, and fixed charges using only supplied rates and quantities. Docs: https://www.brainiac.software/api/electricity-market/bill-tariff-reconcile",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__peak-demand-charge-calculate",
      "description": "Calculate peak demand charges. Calculate peak-demand charges from supplied peak kW and tariff peakDemandRate values. Missing inputs are not invented. Docs: https://www.brainiac.software/api/electricity-market/peak-demand-charge-calculate",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__energy-price-volatility-analyze",
      "description": "Analyze energy price volatility. Compute historical price and return standard deviations from supplied market price series. Thin samples are reported, not filled. Docs: https://www.brainiac.software/api/electricity-market/energy-price-volatility-analyze",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__renewable-generation-forecast",
      "description": "Report renewable generation forecasts. Report caller-supplied renewable historical and forecast megawatts, optionally enriched with World Bank renewable series. Future MW are never invented. Docs: https://www.brainiac.software/api/electricity-market/renewable-generation-forecast",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__grid-outage-public-data-analyze",
      "description": "Analyze grid outage public data. Analyze supplied outage notices and optional key-free public feeds by region and customers affected. Missing counts are not invented. Docs: https://www.brainiac.software/api/electricity-market/grid-outage-public-data-analyze",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
      "name": "electricity-market__exposure-report",
      "description": "Build electricity market exposure report. Aggregate price, demand, carbon, tariff, volatility, renewable, outage, and exposure findings from supplied records and optional key-free public datasets. Docs: https://www.brainiac.software/api/electricity-market/exposure-report",
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
          "prices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "price": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "product": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbon": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "intensity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "index": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "tariffs": {
            "maxItems": 100,
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
                  "maxLength": 160
                },
                "energyRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakDemandRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "demandUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bills": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "tariffId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "peakKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedEnergy": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedDemand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedFixed": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "billedTotal": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "generation": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "fuel": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "mw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "isForecast": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "customersAffected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "exposures": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "market": {
                  "type": "string",
                  "maxLength": 120
                },
                "volumeMwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "hedgeRatio": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 18
              },
              "forecast": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
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
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "electricity-market__price-series-normalize": "0.04",
  "electricity-market__price-compare": "0.04",
  "electricity-market__demand-profile-analyze": "0.04",
  "electricity-market__carbon-intensity-track": "0.04",
  "electricity-market__bill-tariff-reconcile": "0.05",
  "electricity-market__peak-demand-charge-calculate": "0.03",
  "electricity-market__energy-price-volatility-analyze": "0.04",
  "electricity-market__renewable-generation-forecast": "0.05",
  "electricity-market__grid-outage-public-data-analyze": "0.04",
  "electricity-market__exposure-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "electricity-market__price-series-normalize": "electricity-market/price-series-normalize",
  "electricity-market__price-compare": "electricity-market/price-compare",
  "electricity-market__demand-profile-analyze": "electricity-market/demand-profile-analyze",
  "electricity-market__carbon-intensity-track": "electricity-market/carbon-intensity-track",
  "electricity-market__bill-tariff-reconcile": "electricity-market/bill-tariff-reconcile",
  "electricity-market__peak-demand-charge-calculate": "electricity-market/peak-demand-charge-calculate",
  "electricity-market__energy-price-volatility-analyze": "electricity-market/energy-price-volatility-analyze",
  "electricity-market__renewable-generation-forecast": "electricity-market/renewable-generation-forecast",
  "electricity-market__grid-outage-public-data-analyze": "electricity-market/grid-outage-public-data-analyze",
  "electricity-market__exposure-report": "electricity-market/exposure-report"
}


class BrainiacElectricityMarketAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — electricity-market",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the electricity-market catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "electricity-market", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize electricity price series"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the electricity-market group. "
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
