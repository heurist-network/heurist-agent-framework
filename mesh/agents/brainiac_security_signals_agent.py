"""Auto-generated BRAINIAC Heurist Mesh agent for group `security-signals` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "security-signals__event-correlate",
      "description": "Correlate security events. Correlate caller-supplied security events into related incident groups using time windows and shared actor/host/IP links. Observed grouping only—not a confirmed attack. Docs: https://www.brainiac.software/api/security-signals/event-correlate",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__weak-signal-detect",
      "description": "Detect weak security signals. Identify early suspicious-activity indicators from caller-supplied events. Weak signals are hypotheses with explicit confidence—not confirmed attacks. Docs: https://www.brainiac.software/api/security-signals/weak-signal-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__attack-sequence-detect",
      "description": "Detect attack sequences. Detect caller-supplied event sequences that match local attack-pattern rules. Matches are inferred patterns, not confirmed compromises. Docs: https://www.brainiac.software/api/security-signals/attack-sequence-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__insider-threat-signal-detect",
      "description": "Detect insider-threat signals. Identify unusual user activity in caller-supplied logs (off-hours, bulk/export wording, privilege changes). Not a confirmed insider attack. Docs: https://www.brainiac.software/api/security-signals/insider-threat-signal-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__privilege-escalation-detect",
      "description": "Detect privilege-escalation indicators. Detect privilege-escalation indicators from caller-supplied privilege fields and escalation keywords. Not confirmation of successful abuse. Docs: https://www.brainiac.software/api/security-signals/privilege-escalation-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__lateral-movement-detect",
      "description": "Detect lateral-movement indicators. Identify suspicious host-to-host movement from caller-supplied network/auth logs. Does not access the caller's network. Docs: https://www.brainiac.software/api/security-signals/lateral-movement-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__account-takeover-signal-detect",
      "description": "Detect account-takeover signals. Identify account-takeover indicators when multiple distinct signals appear for the same user (geo/device/MFA/recovery). Not a confirmed takeover. Docs: https://www.brainiac.software/api/security-signals/account-takeover-signal-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__credential-abuse-detect",
      "description": "Detect credential-abuse patterns. Detect suspicious credential usage such as repeated failures, fail-then-success, or reuse across many hosts from caller-supplied auth events. Docs: https://www.brainiac.software/api/security-signals/credential-abuse-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__brute-force-pattern-detect",
      "description": "Detect brute-force patterns. Identify burst, distributed, and low-and-slow brute-force patterns from caller-supplied authentication failures. Docs: https://www.brainiac.software/api/security-signals/brute-force-pattern-detect",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
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
      "name": "security-signals__event-severity-score",
      "description": "Score security-event severity. Calculate an explainable severity score for detections derived from caller-supplied events, with scoring breakdown and confirmedAttack=false. Docs: https://www.brainiac.software/api/security-signals/event-severity-score",
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
          "events": {
            "maxItems": 20000,
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
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "destinationHost": {
                  "type": "string",
                  "maxLength": 253
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "process": {
                  "type": "string",
                  "maxLength": 160
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "unknown"
                  ]
                },
                "privilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousPrivilege": {
                  "type": "string",
                  "maxLength": 80
                },
                "authMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaUsed": {
                  "type": "boolean"
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "previousGeoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "relatedEventIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "weakSignalWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "sequenceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "bruteForceFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "lowAndSlowFailureThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "security-signals__event-correlate": "0.05",
  "security-signals__weak-signal-detect": "0.04",
  "security-signals__attack-sequence-detect": "0.05",
  "security-signals__insider-threat-signal-detect": "0.05",
  "security-signals__privilege-escalation-detect": "0.04",
  "security-signals__lateral-movement-detect": "0.04",
  "security-signals__account-takeover-signal-detect": "0.05",
  "security-signals__credential-abuse-detect": "0.04",
  "security-signals__brute-force-pattern-detect": "0.04",
  "security-signals__event-severity-score": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "security-signals__event-correlate": "security-signals/event-correlate",
  "security-signals__weak-signal-detect": "security-signals/weak-signal-detect",
  "security-signals__attack-sequence-detect": "security-signals/attack-sequence-detect",
  "security-signals__insider-threat-signal-detect": "security-signals/insider-threat-signal-detect",
  "security-signals__privilege-escalation-detect": "security-signals/privilege-escalation-detect",
  "security-signals__lateral-movement-detect": "security-signals/lateral-movement-detect",
  "security-signals__account-takeover-signal-detect": "security-signals/account-takeover-signal-detect",
  "security-signals__credential-abuse-detect": "security-signals/credential-abuse-detect",
  "security-signals__brute-force-pattern-detect": "security-signals/brute-force-pattern-detect",
  "security-signals__event-severity-score": "security-signals/event-severity-score"
}


class BrainiacSecuritySignalsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — security-signals",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the security-signals catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "security-signals", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Correlate security events"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the security-signals group. "
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
