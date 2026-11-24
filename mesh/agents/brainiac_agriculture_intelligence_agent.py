"""Auto-generated BRAINIAC Heurist Mesh agent for group `agriculture-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "agriculture-intelligence__crop-weather-exposure-analyze",
      "description": "Analyze crop weather exposure. Analyze frost, drought, and excess-rain exposure from caller-supplied weather series or optional key-free Open-Meteo daily forecasts. No paid commodity feed. Docs: https://www.brainiac.software/api/agriculture-intelligence/crop-weather-exposure-analyze",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__crop-calendar-validate",
      "description": "Validate crop calendars. Validate planting/harvest/stage events against caller-supplied calendar windows. Not a regulatory planting determination. Docs: https://www.brainiac.software/api/agriculture-intelligence/crop-calendar-validate",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__crop-yield-estimate",
      "description": "Estimate crop yields. Estimate total yield from caller-supplied hectares and expected/historical yield-per-hectare rates, with optional weather stress factors. Docs: https://www.brainiac.software/api/agriculture-intelligence/crop-yield-estimate",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__commodity-price-series-normalize",
      "description": "Normalize commodity price series. Normalize caller-supplied commodity price points, or optional key-free World Bank Open Data indicator series when requested. No paid commodity feed. Docs: https://www.brainiac.software/api/agriculture-intelligence/commodity-price-series-normalize",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__commodity-price-spread-analyze",
      "description": "Analyze commodity price spreads. Analyze spot/futures or left/right price spreads from caller-supplied commodity price points. Docs: https://www.brainiac.software/api/agriculture-intelligence/commodity-price-spread-analyze",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__fertilizer-cost-per-hectare",
      "description": "Calculate fertilizer cost per hectare. Calculate fertilizer cost per hectare from caller-supplied application rates and unit prices. Docs: https://www.brainiac.software/api/agriculture-intelligence/fertilizer-cost-per-hectare",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__input-cost-compare",
      "description": "Compare agricultural input costs. Compare prior/current or left/right agricultural input costs per hectare from caller-supplied rate and price rows. Docs: https://www.brainiac.software/api/agriculture-intelligence/input-cost-compare",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__grain-quality-spec-validate",
      "description": "Validate grain quality specs. Validate caller-supplied grain lot moisture, protein, test weight, foreign material, damage, and grade against supplied specs. Docs: https://www.brainiac.software/api/agriculture-intelligence/grain-quality-spec-validate",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__crop-insurance-evidence-check",
      "description": "Check crop insurance evidence. Check caller-supplied crop insurance evidence items against a required checklist. Coverage is not confirmed. Docs: https://www.brainiac.software/api/agriculture-intelligence/crop-insurance-evidence-check",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agriculture-intelligence__market-risk-report",
      "description": "Build agricultural market risk report. Aggregate weather exposure, calendar, yield, price, spread, fertilizer, input-cost, grain-quality, and insurance-evidence sections from caller-supplied agricultural records. Docs: https://www.brainiac.software/api/agriculture-intelligence/market-risk-report",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "temperatureC": {
                  "type": "number",
                  "minimum": -80,
                  "maximum": 80
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2000
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "humidityPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "frost": {
                  "type": "boolean"
                },
                "droughtDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "variety": {
                  "type": "string",
                  "maxLength": 120
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitudeDeg": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitudeDeg": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "plantedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedHarvestAt": {
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
          "calendars": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "stage": {
                  "type": "string",
                  "maxLength": 80
                },
                "windowStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "eventAt": {
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
          "yields": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
                  "type": "string",
                  "maxLength": 80
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "historicalYieldPerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "weatherStressFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 5
                },
                "unit": {
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
          "prices": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "symbol": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "market": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "spot",
                    "futures",
                    "basis",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "inputCosts": {
            "maxItems": 5000,
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
                "category": {
                  "type": "string",
                  "enum": [
                    "fertilizer",
                    "seed",
                    "chemical",
                    "fuel",
                    "labor",
                    "other"
                  ]
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "nutrient": {
                  "type": "string",
                  "maxLength": 40
                },
                "ratePerHa": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "pricePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "hectares": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "current"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "grainLots": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "lotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "moisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "proteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "testWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "foreignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "damagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "grade": {
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
          "grainSpecs": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "commodity": {
                  "type": "string",
                  "maxLength": 80
                },
                "maxMoisturePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minProteinPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "minTestWeight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "maxForeignMaterialPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxDamagePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "requiredGrade": {
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
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "present": {
                  "type": "boolean"
                },
                "fieldId": {
                  "type": "string",
                  "maxLength": 80
                },
                "crop": {
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
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "openMeteo": {
            "type": "object",
            "properties": {
              "latitudeDeg": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "longitudeDeg": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "start": {
                "type": "string",
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 16
              },
              "fieldId": {
                "type": "string",
                "maxLength": 80
              },
              "crop": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
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
                "minLength": 2,
                "maxLength": 80
              },
              "perPage": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              },
              "commodity": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "country",
              "indicator"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "frostThresholdC": {
            "type": "number",
            "minimum": -40,
            "maximum": 10
          },
          "droughtThresholdDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "excessRainMm": {
            "type": "number",
            "minimum": 1,
            "maximum": 2000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "agriculture-intelligence__crop-weather-exposure-analyze": "0.04",
  "agriculture-intelligence__crop-calendar-validate": "0.03",
  "agriculture-intelligence__crop-yield-estimate": "0.04",
  "agriculture-intelligence__commodity-price-series-normalize": "0.03",
  "agriculture-intelligence__commodity-price-spread-analyze": "0.03",
  "agriculture-intelligence__fertilizer-cost-per-hectare": "0.03",
  "agriculture-intelligence__input-cost-compare": "0.03",
  "agriculture-intelligence__grain-quality-spec-validate": "0.03",
  "agriculture-intelligence__crop-insurance-evidence-check": "0.03",
  "agriculture-intelligence__market-risk-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "agriculture-intelligence__crop-weather-exposure-analyze": "agriculture-intelligence/crop-weather-exposure-analyze",
  "agriculture-intelligence__crop-calendar-validate": "agriculture-intelligence/crop-calendar-validate",
  "agriculture-intelligence__crop-yield-estimate": "agriculture-intelligence/crop-yield-estimate",
  "agriculture-intelligence__commodity-price-series-normalize": "agriculture-intelligence/commodity-price-series-normalize",
  "agriculture-intelligence__commodity-price-spread-analyze": "agriculture-intelligence/commodity-price-spread-analyze",
  "agriculture-intelligence__fertilizer-cost-per-hectare": "agriculture-intelligence/fertilizer-cost-per-hectare",
  "agriculture-intelligence__input-cost-compare": "agriculture-intelligence/input-cost-compare",
  "agriculture-intelligence__grain-quality-spec-validate": "agriculture-intelligence/grain-quality-spec-validate",
  "agriculture-intelligence__crop-insurance-evidence-check": "agriculture-intelligence/crop-insurance-evidence-check",
  "agriculture-intelligence__market-risk-report": "agriculture-intelligence/market-risk-report"
}


class BrainiacAgricultureIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — agriculture-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the agriculture-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "agriculture-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze crop weather exposure"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the agriculture-intelligence group. "
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
