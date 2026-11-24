"""Auto-generated BRAINIAC Heurist Mesh agent for group `electrical-engineering` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "electrical-engineering__load-schedule-calculate",
      "description": "Calculate electrical load schedules. Calculate kW, kVA, and current for caller-supplied loads using supplied voltage and power factor. Missing values are not invented. Docs: https://www.brainiac.software/api/electrical-engineering/load-schedule-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__three-phase-load-balance-check",
      "description": "Check three-phase load balance. Compare phase-leg currents from supplied loads and report imbalance percentage. Optional caller rule thresholds are compared when provided. Docs: https://www.brainiac.software/api/electrical-engineering/three-phase-load-balance-check",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__voltage-drop-calculate",
      "description": "Calculate voltage drop. Calculate voltage drop from supplied cable resistance/reactance, length, and load current. Cable tables are not invented. Docs: https://www.brainiac.software/api/electrical-engineering/voltage-drop-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__cable-sizing-calculate",
      "description": "Check cable sizing. Compare calculated design current to caller-supplied cable ampacity. Ampacity tables are not invented. Docs: https://www.brainiac.software/api/electrical-engineering/cable-sizing-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__breaker-rating-check",
      "description": "Check breaker ratings. Compare calculated design current to caller-supplied breaker ratings and continuous factors. Code rules are not invented. Docs: https://www.brainiac.software/api/electrical-engineering/breaker-rating-check",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__transformer-capacity-calculate",
      "description": "Calculate transformer capacity. Compare transformer rated kVA to supplied or schedule load kVA and report loading percentage. Docs: https://www.brainiac.software/api/electrical-engineering/transformer-capacity-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__power-factor-correction-calculate",
      "description": "Calculate power factor correction. Calculate required kVAR (and optional capacitance) to move from a supplied power factor to a supplied target. Docs: https://www.brainiac.software/api/electrical-engineering/power-factor-correction-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__generator-sizing-calculate",
      "description": "Calculate generator sizing. Size required generator kVA from supplied load and caller diversity, reserve, and derate factors. Docs: https://www.brainiac.software/api/electrical-engineering/generator-sizing-calculate",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__ev-charger-load-capacity-check",
      "description": "Check EV charger load capacity. Check EV charger design current against caller-supplied panel capacity and existing load. Continuous factors are used only when supplied. Docs: https://www.brainiac.software/api/electrical-engineering/ev-charger-load-capacity-check",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
      "name": "electrical-engineering__design-document-audit",
      "description": "Audit electrical design documents. Audit completeness of supplied electrical design inputs and aggregate load, balance, drop, cable, breaker, transformer, PF, generator, and EV checks. Does not invent code compliance. Docs: https://www.brainiac.software/api/electrical-engineering/design-document-audit",
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
          "loads": {
            "maxItems": 500,
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
                "phase": {
                  "type": "string",
                  "enum": [
                    "1",
                    "3",
                    "A",
                    "B",
                    "C",
                    "AB",
                    "BC",
                    "CA",
                    "ABC"
                  ]
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "kva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "continuous": {
                  "type": "boolean"
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "notes": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "cables": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "designation": {
                  "type": "string",
                  "maxLength": 120
                },
                "ampacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resistanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "reactanceOhmPerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "lengthM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "conductors": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100
                },
                "material": {
                  "type": "string",
                  "maxLength": 40
                },
                "sizeLabel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "breakers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "loadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratingA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "poles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 4
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transformers": {
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
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "primaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "secondaryV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "impedancePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "powerFactorCases": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "targetPowerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "frequencyHz": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                }
              },
              "additionalProperties": false
            }
          },
          "generators": {
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
                "loadKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "powerFactor": {
                  "type": "number",
                  "minimum": 0.01,
                  "maximum": 1
                },
                "diversityFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "reserveFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "altitudeDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "temperatureDerate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "ratedKva": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "chargers": {
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
                  "maxLength": 160
                },
                "voltageV": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currentA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "kw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "continuous": {
                  "type": "boolean"
                },
                "continuousFactor": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 2
                },
                "panelCapacityA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "existingLoadA": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "phases": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "subject": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "system": {
            "type": "object",
            "properties": {
              "voltageV": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "phases": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3
              },
              "frequencyHz": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000
              },
              "powerFactor": {
                "type": "number",
                "minimum": 0.01,
                "maximum": 1
              },
              "continuousFactor": {
                "type": "number",
                "minimum": 0,
                "maximum": 2
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
  "electrical-engineering__load-schedule-calculate": "0.04",
  "electrical-engineering__three-phase-load-balance-check": "0.03",
  "electrical-engineering__voltage-drop-calculate": "0.04",
  "electrical-engineering__cable-sizing-calculate": "0.04",
  "electrical-engineering__breaker-rating-check": "0.03",
  "electrical-engineering__transformer-capacity-calculate": "0.04",
  "electrical-engineering__power-factor-correction-calculate": "0.03",
  "electrical-engineering__generator-sizing-calculate": "0.04",
  "electrical-engineering__ev-charger-load-capacity-check": "0.04",
  "electrical-engineering__design-document-audit": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "electrical-engineering__load-schedule-calculate": "electrical-engineering/load-schedule-calculate",
  "electrical-engineering__three-phase-load-balance-check": "electrical-engineering/three-phase-load-balance-check",
  "electrical-engineering__voltage-drop-calculate": "electrical-engineering/voltage-drop-calculate",
  "electrical-engineering__cable-sizing-calculate": "electrical-engineering/cable-sizing-calculate",
  "electrical-engineering__breaker-rating-check": "electrical-engineering/breaker-rating-check",
  "electrical-engineering__transformer-capacity-calculate": "electrical-engineering/transformer-capacity-calculate",
  "electrical-engineering__power-factor-correction-calculate": "electrical-engineering/power-factor-correction-calculate",
  "electrical-engineering__generator-sizing-calculate": "electrical-engineering/generator-sizing-calculate",
  "electrical-engineering__ev-charger-load-capacity-check": "electrical-engineering/ev-charger-load-capacity-check",
  "electrical-engineering__design-document-audit": "electrical-engineering/design-document-audit"
}


class BrainiacElectricalEngineeringAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — electrical-engineering",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the electrical-engineering catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "electrical-engineering", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Calculate electrical load schedules"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the electrical-engineering group. "
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
