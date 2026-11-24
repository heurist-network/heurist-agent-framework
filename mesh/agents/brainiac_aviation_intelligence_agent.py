"""Auto-generated BRAINIAC Heurist Mesh agent for group `aviation-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "aviation-intelligence__flight-schedule-normalize",
      "description": "Normalize flight schedules. Normalize caller-supplied flight schedule fields and compute delay/block times when actual times are present. Paid flight tracking is not used. Docs: https://www.brainiac.software/api/aviation-intelligence/flight-schedule-normalize",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__flight-delay-pattern-analyze",
      "description": "Analyze flight delay patterns. Aggregate delay statistics by flight number/route from caller-supplied scheduled and actual times. Docs: https://www.brainiac.software/api/aviation-intelligence/flight-delay-pattern-analyze",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__airport-connection-risk-calculate",
      "description": "Calculate airport connection risk. Calculate connection slack and risk from inbound/outbound caller-supplied flight times and minimum connect minutes. Docs: https://www.brainiac.software/api/aviation-intelligence/airport-connection-risk-calculate",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__flight-diversion-event-track",
      "description": "Track flight diversion events. Normalize caller-supplied diversion events and durations. Live paid tracking feeds are not queried. Docs: https://www.brainiac.software/api/aviation-intelligence/flight-diversion-event-track",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__aircraft-registration-lookup",
      "description": "Look up aircraft registrations. Normalize caller-supplied aircraft registration records, optionally enriched with key-free OpenSky aircraft metadata when openSky.icao24 is requested. Docs: https://www.brainiac.software/api/aviation-intelligence/aircraft-registration-lookup",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__aircraft-maintenance-log-parse",
      "description": "Parse aircraft maintenance logs. Parse caller-supplied maintenance log rows into normalized task entries and open-item flags. Docs: https://www.brainiac.software/api/aviation-intelligence/aircraft-maintenance-log-parse",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__document-expiry-check",
      "description": "Check aviation document expiry. Compare caller-supplied document expiry dates to asOf and flag expired or soon-expiring items. Regulatory compliance is not determined. Docs: https://www.brainiac.software/api/aviation-intelligence/document-expiry-check",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__flight-emissions-estimate",
      "description": "Estimate flight emissions. Estimate CO2 from caller-supplied fuel burn or distance with caller emission factors, falling back to a disclosed public-style factor table only when neither is supplied. Docs: https://www.brainiac.software/api/aviation-intelligence/flight-emissions-estimate",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__airport-ground-time-analyze",
      "description": "Analyze airport ground time. Analyze caller-supplied arrival/departure ground times against scheduled turn times. Docs: https://www.brainiac.software/api/aviation-intelligence/airport-ground-time-analyze",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__operations-report",
      "description": "Build aviation operations report. Aggregate schedule normalization, delay patterns, connection risk, diversions, registrations, maintenance, document expiry, emissions, and ground time from caller-supplied records only. Docs: https://www.brainiac.software/api/aviation-intelligence/operations-report",
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
          "flights": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "airline": {
                  "type": "string",
                  "maxLength": 120
                },
                "airlineIata": {
                  "type": "string",
                  "maxLength": 8
                },
                "origin": {
                  "type": "string",
                  "maxLength": 8
                },
                "destination": {
                  "type": "string",
                  "maxLength": 8
                },
                "scheduledDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualDepartureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualArrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "aircraftRegistration": {
                  "type": "string",
                  "maxLength": 20
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "distanceKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 40000
                },
                "seats": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "passengers": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "fuelBurnKg": {
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
          "diversions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "plannedDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "diversionAirport": {
                  "type": "string",
                  "maxLength": 8
                },
                "divertedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 200
                },
                "resumedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "finalDestination": {
                  "type": "string",
                  "maxLength": 8
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "icao24": {
                  "type": "string",
                  "maxLength": 12
                },
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "manufacturer": {
                  "type": "string",
                  "maxLength": 120
                },
                "model": {
                  "type": "string",
                  "maxLength": 120
                },
                "operator": {
                  "type": "string",
                  "maxLength": 160
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "serialNumber": {
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
          "maintenanceLogs": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "taskCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 400
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "cycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
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
          "documents": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "subject": {
                  "type": "string",
                  "maxLength": 160
                },
                "documentType": {
                  "type": "string",
                  "maxLength": 80
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
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
          "groundTimes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "flightNumber": {
                  "type": "string",
                  "maxLength": 20
                },
                "registration": {
                  "type": "string",
                  "maxLength": 20
                },
                "arrivalAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "departureAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "scheduledGroundMinutes": {
                  "type": "number",
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
          "emissionFactors": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "aircraftType": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2PerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "kgCo2PerPassengerKm": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "connections": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "outboundFlightId": {
                  "type": "string",
                  "maxLength": 80
                },
                "airport": {
                  "type": "string",
                  "maxLength": 8
                },
                "minimumConnectMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1440
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "openSky": {
            "type": "object",
            "properties": {
              "icao24": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12
              }
            },
            "required": [
              "icao24"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__us-airport-status",
      "description": "US airport NAS status. Official FAA NAS airport status: ground stops, ground delays, arrival/departure delays, and closures currently published. Optional airport IATA/ICAO filter. Docs: https://www.brainiac.software/api/aviation-intelligence/us-airport-status",
      "parameters": {
        "type": "object",
        "properties": {
          "airport": {
            "type": "string",
            "minLength": 3,
            "maxLength": 8
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "aviation-intelligence__metar-taf",
      "description": "METAR and TAF weather. Decoded METAR and optional TAF aviation weather from the official NOAA Aviation Weather API for up to 10 ICAO stations. Docs: https://www.brainiac.software/api/aviation-intelligence/metar-taf",
      "parameters": {
        "type": "object",
        "properties": {
          "icaoIds": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 3,
              "maxLength": 8
            }
          },
          "includeTaf": {
            "type": "boolean"
          }
        },
        "required": [
          "icaoIds"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "aviation-intelligence__flight-schedule-normalize": "0.03",
  "aviation-intelligence__flight-delay-pattern-analyze": "0.04",
  "aviation-intelligence__airport-connection-risk-calculate": "0.04",
  "aviation-intelligence__flight-diversion-event-track": "0.03",
  "aviation-intelligence__aircraft-registration-lookup": "0.03",
  "aviation-intelligence__aircraft-maintenance-log-parse": "0.04",
  "aviation-intelligence__document-expiry-check": "0.03",
  "aviation-intelligence__flight-emissions-estimate": "0.04",
  "aviation-intelligence__airport-ground-time-analyze": "0.03",
  "aviation-intelligence__operations-report": "0.08",
  "aviation-intelligence__us-airport-status": "0.005",
  "aviation-intelligence__metar-taf": "0.003"
}
TOOL_ROUTES: Dict[str, str] = {
  "aviation-intelligence__flight-schedule-normalize": "aviation-intelligence/flight-schedule-normalize",
  "aviation-intelligence__flight-delay-pattern-analyze": "aviation-intelligence/flight-delay-pattern-analyze",
  "aviation-intelligence__airport-connection-risk-calculate": "aviation-intelligence/airport-connection-risk-calculate",
  "aviation-intelligence__flight-diversion-event-track": "aviation-intelligence/flight-diversion-event-track",
  "aviation-intelligence__aircraft-registration-lookup": "aviation-intelligence/aircraft-registration-lookup",
  "aviation-intelligence__aircraft-maintenance-log-parse": "aviation-intelligence/aircraft-maintenance-log-parse",
  "aviation-intelligence__document-expiry-check": "aviation-intelligence/document-expiry-check",
  "aviation-intelligence__flight-emissions-estimate": "aviation-intelligence/flight-emissions-estimate",
  "aviation-intelligence__airport-ground-time-analyze": "aviation-intelligence/airport-ground-time-analyze",
  "aviation-intelligence__operations-report": "aviation-intelligence/operations-report",
  "aviation-intelligence__us-airport-status": "aviation-intelligence/us-airport-status",
  "aviation-intelligence__metar-taf": "aviation-intelligence/metar-taf"
}


class BrainiacAviationIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — aviation-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the aviation-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "aviation-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize flight schedules"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.003",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the aviation-intelligence group. "
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
