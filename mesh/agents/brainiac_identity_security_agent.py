"""Auto-generated BRAINIAC Heurist Mesh agent for group `identity-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "identity-security__authentication-pattern-analyze",
      "description": "Analyze authentication patterns. Identify abnormal authentication patterns from caller-supplied logs using local time-window correlation. VPN/proxy/shared-network labels reduce confidence. Never proof of compromise from a single login. Docs: https://www.brainiac.software/api/identity-security/authentication-pattern-analyze",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__impossible-travel-detect",
      "description": "Detect impossible travel. Detect geographically inconsistent logins from supplied timestamps and locations. Accounts for VPN/proxy/shared networks and legitimate-travel labels; a single unusual pair is not proof of compromise. Docs: https://www.brainiac.software/api/identity-security/impossible-travel-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__session-hijacking-signal-detect",
      "description": "Detect session-hijacking signals. Identify suspicious session changes and reuse patterns from caller-supplied session, device, IP, and user-agent fields. Indicators only—not confirmed hijacking. Docs: https://www.brainiac.software/api/identity-security/session-hijacking-signal-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__mfa-fatigue-detect",
      "description": "Detect MFA fatigue. Detect repeated MFA push/challenge patterns from caller-supplied MFA events that may indicate an MFA fatigue attack. Not confirmation of account takeover. Docs: https://www.brainiac.software/api/identity-security/mfa-fatigue-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__account-sharing-detect",
      "description": "Detect account sharing. Identify suspicious account-sharing patterns from multi-device, multi-location, and near-simultaneous authentications. Shared-network context is treated as a mitigating factor. Docs: https://www.brainiac.software/api/identity-security/account-sharing-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__access-policy-conflict-detect",
      "description": "Detect access-policy conflicts. Detect conflicting allow/deny access rules from caller-supplied policy exports for the same principal, resource, and action. Docs: https://www.brainiac.software/api/identity-security/access-policy-conflict-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__dormant-account-risk-detect",
      "description": "Detect dormant-account risk. Identify risks from inactive but enabled accounts using caller-supplied account inventory and optional recent auth events. Hygiene signal only—not confirmed compromise. Docs: https://www.brainiac.software/api/identity-security/dormant-account-risk-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "identity-security__service-account-anomaly-detect",
      "description": "Detect service-account anomalies. Analyze unusual service-account activity such as interactive logins, off-hours use, and high application/IP diversity from caller-supplied events. Docs: https://www.brainiac.software/api/identity-security/service-account-anomaly-detect",
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
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 120
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "success",
                    "failure",
                    "challenge",
                    "unknown"
                  ]
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "geoCity": {
                  "type": "string",
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "asn": {
                  "type": "string",
                  "maxLength": 80
                },
                "isVpn": {
                  "type": "boolean"
                },
                "isProxy": {
                  "type": "boolean"
                },
                "isSharedNetwork": {
                  "type": "boolean"
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "previousDeviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "sessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "previousSessionId": {
                  "type": "string",
                  "maxLength": 160
                },
                "userAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "previousUserAgent": {
                  "type": "string",
                  "maxLength": 500
                },
                "mfaMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "mfaResult": {
                  "type": "string",
                  "enum": [
                    "approved",
                    "denied",
                    "timeout",
                    "push_sent",
                    "unknown"
                  ]
                },
                "application": {
                  "type": "string",
                  "maxLength": 160
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "labels": {
                  "maxItems": 40,
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
          "accounts": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "username": {
                  "type": "string",
                  "maxLength": 120
                },
                "accountType": {
                  "type": "string",
                  "enum": [
                    "user",
                    "service",
                    "unknown"
                  ]
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastLoginAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastActivityAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "isPrivileged": {
                  "type": "boolean"
                },
                "isDisabled": {
                  "type": "boolean"
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                },
                "labels": {
                  "maxItems": 40,
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
          "policies": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "principal": {
                  "type": "string",
                  "maxLength": 200
                },
                "resource": {
                  "type": "string",
                  "maxLength": 300
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "effect": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                },
                "priority": {
                  "type": "number",
                  "minimum": -1000000,
                  "maximum": 1000000
                },
                "conditions": {
                  "type": "string",
                  "maxLength": 2000
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
          "authWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "mfaWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "mfaPushThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 1000
          },
          "sharingWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 720
          },
          "dormantDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "maxTravelKmh": {
            "type": "number",
            "minimum": 50,
            "maximum": 2000
          },
          "serviceBaselineWindowHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "identity-security__authentication-pattern-analyze": "0.04",
  "identity-security__impossible-travel-detect": "0.05",
  "identity-security__session-hijacking-signal-detect": "0.04",
  "identity-security__mfa-fatigue-detect": "0.04",
  "identity-security__account-sharing-detect": "0.04",
  "identity-security__access-policy-conflict-detect": "0.03",
  "identity-security__dormant-account-risk-detect": "0.03",
  "identity-security__service-account-anomaly-detect": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "identity-security__authentication-pattern-analyze": "identity-security/authentication-pattern-analyze",
  "identity-security__impossible-travel-detect": "identity-security/impossible-travel-detect",
  "identity-security__session-hijacking-signal-detect": "identity-security/session-hijacking-signal-detect",
  "identity-security__mfa-fatigue-detect": "identity-security/mfa-fatigue-detect",
  "identity-security__account-sharing-detect": "identity-security/account-sharing-detect",
  "identity-security__access-policy-conflict-detect": "identity-security/access-policy-conflict-detect",
  "identity-security__dormant-account-risk-detect": "identity-security/dormant-account-risk-detect",
  "identity-security__service-account-anomaly-detect": "identity-security/service-account-anomaly-detect"
}


class BrainiacIdentitySecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — identity-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the identity-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "identity-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze authentication patterns"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the identity-security group. "
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
