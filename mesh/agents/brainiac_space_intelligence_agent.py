"""Auto-generated BRAINIAC Heurist Mesh agent for group `space-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "space-intelligence__satellite-pass-predict",
      "description": "Predict satellite passes. Predict approximate satellite passes over caller-supplied observers from TLEs (or optional key-free CelesTrak GP). Uses simplified Keplerian propagation; communicate orbital uncertainty and TLE freshness. Docs: https://www.brainiac.software/api/space-intelligence/satellite-pass-predict",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-orbit-change-detect",
      "description": "Detect satellite orbit changes. Compare before/after TLE mean elements for inclination, RAAN, mean motion, and apogee/perigee deltas. Maneuver confirmation is not claimed. Docs: https://www.brainiac.software/api/space-intelligence/satellite-orbit-change-detect",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-conjunction-screen",
      "description": "Screen satellite conjunctions. Screen approximate miss distances between caller-supplied TLEs over a horizon. Not a covariance-based conjunction assessment. Docs: https://www.brainiac.software/api/space-intelligence/satellite-conjunction-screen",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__earth-observation-change-detect",
      "description": "Detect earth-observation changes. Compare before/after caller-supplied EO scene metadata (NDVI, brightness, cloud cover). Commercial imagery pixels are not downloaded. Docs: https://www.brainiac.software/api/space-intelligence/earth-observation-change-detect",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-imagery-cloud-assess",
      "description": "Assess satellite imagery cloud cover. Classify caller-supplied cloud-cover percentages for EO scenes. Commercial imagery archives are not queried. Docs: https://www.brainiac.software/api/space-intelligence/satellite-imagery-cloud-assess",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-image-quality-check",
      "description": "Check satellite image quality. Score caller-supplied sharpness, SNR, resolution, and cloud metrics for EO scenes. Missing metrics are not invented. Docs: https://www.brainiac.software/api/space-intelligence/satellite-image-quality-check",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-data-license-metadata",
      "description": "Extract satellite data license metadata. Extract and classify caller-supplied imagery license, attribution, and license URL fields. Legal advice is not provided. Docs: https://www.brainiac.software/api/space-intelligence/satellite-data-license-metadata",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__launch-window-weather-analyze",
      "description": "Analyze launch-window weather. Analyze caller-supplied weather samples or optional key-free Open-Meteo hourly forecasts against simple go/no-go thresholds. Docs: https://www.brainiac.software/api/space-intelligence/launch-window-weather-analyze",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__object-catalog-compare",
      "description": "Compare space-object catalogs. Compare left/right caller-supplied space-object catalog rows by NORAD ID/name and optional element fields. Docs: https://www.brainiac.software/api/space-intelligence/object-catalog-compare",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "space-intelligence__satellite-observation-evidence-report",
      "description": "Build satellite observation evidence report. Aggregate passes, orbit changes, conjunctions, EO change, cloud/quality/license checks, launch weather, and catalog comparison with orbital uncertainty and TLE freshness notes. Docs: https://www.brainiac.software/api/space-intelligence/satellite-observation-evidence-report",
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
          "tles": {
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
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "line1": {
                  "type": "string",
                  "maxLength": 120
                },
                "line2": {
                  "type": "string",
                  "maxLength": 120
                },
                "text": {
                  "type": "string",
                  "maxLength": 400
                },
                "epoch": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                }
              },
              "additionalProperties": false
            }
          },
          "observers": {
            "maxItems": 50,
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
                "altitudeKm": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 20
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "sceneId": {
                  "type": "string",
                  "maxLength": 120
                },
                "satellite": {
                  "type": "string",
                  "maxLength": 120
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "sharpness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "snr": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "resolutionM": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "license": {
                  "type": "string",
                  "maxLength": 200
                },
                "attribution": {
                  "type": "string",
                  "maxLength": 400
                },
                "licenseUrl": {
                  "type": "string",
                  "maxLength": 400
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "before",
                    "after",
                    "left",
                    "right",
                    "a",
                    "b"
                  ]
                },
                "ndvi": {
                  "type": "number",
                  "minimum": -1,
                  "maximum": 1
                },
                "brightness": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "weather": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "cloudCoverPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "windSpeedMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "precipitationMm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "visibilityKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 200
                },
                "thunderRisk": {
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
          "catalogObjects": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "noradId": {
                  "type": "string",
                  "maxLength": 20
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "objectType": {
                  "type": "string",
                  "maxLength": 80
                },
                "inclinationDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 180
                },
                "periodMin": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "eccentricity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "side": {
                  "type": "string",
                  "enum": [
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
          "celestrak": {
            "type": "object",
            "properties": {
              "catnr": {
                "type": "string",
                "maxLength": 20
              },
              "group": {
                "type": "string",
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "maxLength": 160
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50
              }
            },
            "additionalProperties": false
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
              "hours": {
                "type": "integer",
                "minimum": 1,
                "maximum": 168
              }
            },
            "required": [
              "latitudeDeg",
              "longitudeDeg"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "horizonHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 168
          },
          "minElevationDeg": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "stepMinutes": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 60
          },
          "conjunctionThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "space-intelligence__satellite-pass-predict": "0.05",
  "space-intelligence__satellite-orbit-change-detect": "0.04",
  "space-intelligence__satellite-conjunction-screen": "0.05",
  "space-intelligence__earth-observation-change-detect": "0.04",
  "space-intelligence__satellite-imagery-cloud-assess": "0.03",
  "space-intelligence__satellite-image-quality-check": "0.03",
  "space-intelligence__satellite-data-license-metadata": "0.03",
  "space-intelligence__launch-window-weather-analyze": "0.04",
  "space-intelligence__object-catalog-compare": "0.04",
  "space-intelligence__satellite-observation-evidence-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "space-intelligence__satellite-pass-predict": "space-intelligence/satellite-pass-predict",
  "space-intelligence__satellite-orbit-change-detect": "space-intelligence/satellite-orbit-change-detect",
  "space-intelligence__satellite-conjunction-screen": "space-intelligence/satellite-conjunction-screen",
  "space-intelligence__earth-observation-change-detect": "space-intelligence/earth-observation-change-detect",
  "space-intelligence__satellite-imagery-cloud-assess": "space-intelligence/satellite-imagery-cloud-assess",
  "space-intelligence__satellite-image-quality-check": "space-intelligence/satellite-image-quality-check",
  "space-intelligence__satellite-data-license-metadata": "space-intelligence/satellite-data-license-metadata",
  "space-intelligence__launch-window-weather-analyze": "space-intelligence/launch-window-weather-analyze",
  "space-intelligence__object-catalog-compare": "space-intelligence/object-catalog-compare",
  "space-intelligence__satellite-observation-evidence-report": "space-intelligence/satellite-observation-evidence-report"
}


class BrainiacSpaceIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — space-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the space-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "space-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Predict satellite passes"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the space-intelligence group. "
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
