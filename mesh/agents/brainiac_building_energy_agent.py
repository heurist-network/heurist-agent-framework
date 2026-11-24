"""Auto-generated BRAINIAC Heurist Mesh agent for group `building-energy` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "building-energy__consumption-analyze",
      "description": "Analyze building energy consumption. Calculate interval consumption and tariff-based cost from supplied meter readings and rates. Missing tariffs are not invented. Docs: https://www.brainiac.software/api/building-energy/consumption-analyze",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__meter-reading-anomaly-detect",
      "description": "Detect meter reading anomalies. Flag unusual daily usage against a baseline calculated from supplied intervals and explain the comparison method. Docs: https://www.brainiac.software/api/building-energy/meter-reading-anomaly-detect",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__hvac-performance-analyze",
      "description": "Analyze HVAC performance. Compare supplied HVAC efficiency and temperature readings with rated values. Equipment is never controlled and performance is not invented. Docs: https://www.brainiac.software/api/building-energy/hvac-performance-analyze",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__baseline-calculate",
      "description": "Calculate building energy baseline. Calculate a mean daily-interval baseline and standard deviation from supplied meter readings for each meter. Docs: https://www.brainiac.software/api/building-energy/baseline-calculate",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__cost-variance-detect",
      "description": "Detect energy cost variance. Compare billed costs with expected cost from supplied tariffs and quantities. Tariffs are never invented. Docs: https://www.brainiac.software/api/building-energy/cost-variance-detect",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__equipment-maintenance-priority",
      "description": "Prioritize equipment maintenance. Rank equipment using supplied service due dates, fault counts, efficiency, and runtime. Connected equipment is never controlled. Docs: https://www.brainiac.software/api/building-energy/equipment-maintenance-priority",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__occupancy-compare",
      "description": "Compare occupancy and energy. Compare buildings only when supplied measurement periods and energy units are compatible, optionally normalizing by occupants. Docs: https://www.brainiac.software/api/building-energy/occupancy-compare",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "building-energy__efficiency-report",
      "description": "Report building energy efficiency. Combine consumption, anomalies, HVAC flags, baselines, cost variance, maintenance priorities, and occupancy comparisons from supplied facility records. Docs: https://www.brainiac.software/api/building-energy/efficiency-report",
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
          "buildings": {
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
                  "maxLength": 200
                },
                "area": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "areaUnit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "meters": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "readings": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "meterId": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cumulative": {
                  "type": "boolean"
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
                "utility": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "fixedCharge": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
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
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "utility": {
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
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "equipment": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "ratedCapacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "capacityUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastServiceAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nextServiceDue": {
                  "type": "string",
                  "maxLength": 40
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "faultCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "efficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "ratedEfficiency": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "supplyTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "returnTemp": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                },
                "setpoint": {
                  "type": "number",
                  "minimum": -100,
                  "maximum": 200
                }
              },
              "additionalProperties": false
            }
          },
          "occupancy": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "buildingId": {
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
                "occupants": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "hoursOccupied": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
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
  "building-energy__consumption-analyze": "0.04",
  "building-energy__meter-reading-anomaly-detect": "0.05",
  "building-energy__hvac-performance-analyze": "0.05",
  "building-energy__baseline-calculate": "0.04",
  "building-energy__cost-variance-detect": "0.04",
  "building-energy__equipment-maintenance-priority": "0.04",
  "building-energy__occupancy-compare": "0.05",
  "building-energy__efficiency-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "building-energy__consumption-analyze": "building-energy/consumption-analyze",
  "building-energy__meter-reading-anomaly-detect": "building-energy/meter-reading-anomaly-detect",
  "building-energy__hvac-performance-analyze": "building-energy/hvac-performance-analyze",
  "building-energy__baseline-calculate": "building-energy/baseline-calculate",
  "building-energy__cost-variance-detect": "building-energy/cost-variance-detect",
  "building-energy__equipment-maintenance-priority": "building-energy/equipment-maintenance-priority",
  "building-energy__occupancy-compare": "building-energy/occupancy-compare",
  "building-energy__efficiency-report": "building-energy/efficiency-report"
}


class BrainiacBuildingEnergyAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — building-energy",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the building-energy catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "building-energy", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze building energy consumption"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the building-energy group. "
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
