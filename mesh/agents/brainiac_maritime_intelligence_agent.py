"""Auto-generated BRAINIAC Heurist Mesh agent for group `maritime-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "maritime-intelligence__vessel-identity-normalize",
      "description": "Normalize vessel identity. Normalize caller-supplied vessel name, IMO, MMSI, call sign, flag, owner, and operator fields. Validates IMO checksum when an IMO is supplied. Paid AIS coverage is not used. Docs: https://www.brainiac.software/api/maritime-intelligence/vessel-identity-normalize",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__ais-track-gap-detect",
      "description": "Detect AIS track gaps. Detect time gaps and implied speeds between caller-supplied AIS points. Global real-time AIS coverage is not claimed. Docs: https://www.brainiac.software/api/maritime-intelligence/ais-track-gap-detect",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__vessel-route-deviation-detect",
      "description": "Detect vessel route deviations. Compare caller-supplied AIS points to planned waypoints and flag points beyond a distance threshold. Docs: https://www.brainiac.software/api/maritime-intelligence/vessel-route-deviation-detect",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__port-congestion-analyze",
      "description": "Analyze port congestion. Analyze caller-supplied port wait, queue, and berth-occupancy samples. Live terminal systems are not queried. Docs: https://www.brainiac.software/api/maritime-intelligence/port-congestion-analyze",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__vessel-eta-estimate",
      "description": "Estimate vessel ETA. Estimate ETA from the latest caller-supplied AIS point to a destination using geodesic distance and SOG or assumed speed. Docs: https://www.brainiac.software/api/maritime-intelligence/vessel-eta-estimate",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__demurrage-cost-calculate",
      "description": "Calculate demurrage cost. Calculate demurrage from caller-supplied allowed/used laytime and daily rate. Results are not legal invoices. Docs: https://www.brainiac.software/api/maritime-intelligence/demurrage-cost-calculate",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__vessel-sanctions-signal-check",
      "description": "Check vessel sanctions signals. Screen caller-supplied vessel/owner/operator names and IMOs against caller sanctions entries or optional key-free OFAC SDN names. Not a legal determination. Docs: https://www.brainiac.software/api/maritime-intelligence/vessel-sanctions-signal-check",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__cargo-shipment-event-reconcile",
      "description": "Reconcile cargo shipment events. Reconcile document-side and ops-side caller-supplied cargo shipment events by shipment/BL, event type, time, location, and quantity. Docs: https://www.brainiac.software/api/maritime-intelligence/cargo-shipment-event-reconcile",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__vessel-ownership-history-normalize",
      "description": "Normalize vessel ownership history. Normalize caller-supplied vessel ownership timeline rows and flag overlapping intervals. Registry filings are not invented. Docs: https://www.brainiac.software/api/maritime-intelligence/vessel-ownership-history-normalize",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "maritime-intelligence__voyage-risk-report",
      "description": "Build maritime voyage risk report. Aggregate identity, AIS gaps, route deviation, port congestion, ETA, demurrage, sanctions signals, cargo reconciliation, and ownership history from caller-supplied records only. Docs: https://www.brainiac.software/api/maritime-intelligence/voyage-risk-report",
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
          "vessels": {
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "callSign": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselType": {
                  "type": "string",
                  "maxLength": 80
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "operator": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "aisPoints": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "mmsi": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
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
                "sogKn": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cogDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "headingDeg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "navStatus": {
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
          "waypoints": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 120
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
                "sequence": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 10000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "portSamples": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "portCode": {
                  "type": "string",
                  "maxLength": 20
                },
                "portName": {
                  "type": "string",
                  "maxLength": 160
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "vesselsWaiting": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "averageWaitHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                },
                "berthOccupancyPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "arrivals24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "departures24h": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "demurrageCases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "voyageId": {
                  "type": "string",
                  "maxLength": 80
                },
                "laytimeAllowedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "laytimeUsedHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "demurrageRatePerDay": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
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
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "program": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "cargoEvents": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "shipmentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "billOfLading": {
                  "type": "string",
                  "maxLength": 80
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 160
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "document",
                    "ops",
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
          "ownershipRecords": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "vesselId": {
                  "type": "string",
                  "maxLength": 80
                },
                "imo": {
                  "type": "string",
                  "maxLength": 20
                },
                "owner": {
                  "type": "string",
                  "maxLength": 200
                },
                "ownerType": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 40
                },
                "to": {
                  "type": "string",
                  "maxLength": 40
                },
                "flag": {
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
          "fetchOfac": {
            "type": "boolean"
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "gapThresholdHours": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 720
          },
          "deviationThresholdKm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 5000
          },
          "destinationLat": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "destinationLon": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "assumedSpeedKn": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "maritime-intelligence__vessel-identity-normalize": "0.03",
  "maritime-intelligence__ais-track-gap-detect": "0.04",
  "maritime-intelligence__vessel-route-deviation-detect": "0.04",
  "maritime-intelligence__port-congestion-analyze": "0.04",
  "maritime-intelligence__vessel-eta-estimate": "0.04",
  "maritime-intelligence__demurrage-cost-calculate": "0.03",
  "maritime-intelligence__vessel-sanctions-signal-check": "0.05",
  "maritime-intelligence__cargo-shipment-event-reconcile": "0.04",
  "maritime-intelligence__vessel-ownership-history-normalize": "0.03",
  "maritime-intelligence__voyage-risk-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "maritime-intelligence__vessel-identity-normalize": "maritime-intelligence/vessel-identity-normalize",
  "maritime-intelligence__ais-track-gap-detect": "maritime-intelligence/ais-track-gap-detect",
  "maritime-intelligence__vessel-route-deviation-detect": "maritime-intelligence/vessel-route-deviation-detect",
  "maritime-intelligence__port-congestion-analyze": "maritime-intelligence/port-congestion-analyze",
  "maritime-intelligence__vessel-eta-estimate": "maritime-intelligence/vessel-eta-estimate",
  "maritime-intelligence__demurrage-cost-calculate": "maritime-intelligence/demurrage-cost-calculate",
  "maritime-intelligence__vessel-sanctions-signal-check": "maritime-intelligence/vessel-sanctions-signal-check",
  "maritime-intelligence__cargo-shipment-event-reconcile": "maritime-intelligence/cargo-shipment-event-reconcile",
  "maritime-intelligence__vessel-ownership-history-normalize": "maritime-intelligence/vessel-ownership-history-normalize",
  "maritime-intelligence__voyage-risk-report": "maritime-intelligence/voyage-risk-report"
}


class BrainiacMaritimeIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — maritime-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the maritime-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "maritime-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize vessel identity"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the maritime-intelligence group. "
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
