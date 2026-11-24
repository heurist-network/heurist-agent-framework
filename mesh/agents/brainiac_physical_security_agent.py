"""Auto-generated BRAINIAC Heurist Mesh agent for group `physical-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "physical-security__sensor-event-anomaly-detect",
      "description": "Detect sensor-event anomalies. Detect anomalies in caller-supplied sensor telemetry using thresholds, baselines, and local standard-deviation rules. Anomalies are not confirmed physical incidents. Docs: https://www.brainiac.software/api/physical-security/sensor-event-anomaly-detect",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__door-access-pattern-detect",
      "description": "Detect unusual door-access patterns. Identify unusual access patterns from caller-supplied door-entry logs (denials, forced doors, held-open, after-hours). Not a confirmed intrusion. Docs: https://www.brainiac.software/api/physical-security/door-access-pattern-detect",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__access-tailgating-signal-detect",
      "description": "Detect tailgating signals. Identify possible tailgating using caller-supplied access grants correlated with nearby motion/occupancy or unbadged second passages. Not visually confirmed. Docs: https://www.brainiac.software/api/physical-security/access-tailgating-signal-detect",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__perimeter-breach-signal-detect",
      "description": "Detect perimeter-breach signals. Analyze caller-supplied perimeter sensor events for possible breaches. Multi-sensor alarms raise confidence; still not a confirmed physical breach. Docs: https://www.brainiac.software/api/physical-security/perimeter-breach-signal-detect",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__camera-tampering-signal-detect",
      "description": "Detect camera-tampering signals. Identify camera tampering indicators from caller-supplied telemetry (covered/moved/signal-loss). Scene content is not visually verified. Docs: https://www.brainiac.software/api/physical-security/camera-tampering-signal-detect",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__alarm-correlation-analyze",
      "description": "Correlate multi-sensor alarms. Correlate alarms from multiple caller-supplied sensors into possible incident groups using time windows. Correlation is not confirmation of a physical incident. Docs: https://www.brainiac.software/api/physical-security/alarm-correlation-analyze",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__iot-device-behavior-analyze",
      "description": "Analyze IoT device behaviour. Identify unusual IoT device behaviour from caller-supplied telemetry (reporting gaps, outliers, unexpected reboot/config events). Devices are never contacted or controlled. Docs: https://www.brainiac.software/api/physical-security/iot-device-behavior-analyze",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "physical-security__building-security-timeline",
      "description": "Build building-security timeline. Generate a chronological security timeline from caller-supplied building events. Timeline entries are observed events, not confirmed incidents. Docs: https://www.brainiac.software/api/physical-security/building-security-timeline",
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
                  "enum": [
                    "sensor",
                    "door",
                    "perimeter",
                    "camera",
                    "alarm",
                    "iot",
                    "access",
                    "other"
                  ]
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "deviceType": {
                  "type": "string",
                  "maxLength": 80
                },
                "zone": {
                  "type": "string",
                  "maxLength": 120
                },
                "building": {
                  "type": "string",
                  "maxLength": 120
                },
                "doorId": {
                  "type": "string",
                  "maxLength": 120
                },
                "cameraId": {
                  "type": "string",
                  "maxLength": 120
                },
                "userId": {
                  "type": "string",
                  "maxLength": 120
                },
                "badgeId": {
                  "type": "string",
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out",
                    "unknown"
                  ]
                },
                "outcome": {
                  "type": "string",
                  "enum": [
                    "granted",
                    "denied",
                    "forced",
                    "held",
                    "alarm",
                    "clear",
                    "unknown"
                  ]
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "baseline": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "threshold": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
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
          "anomalyStdev": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "doorWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "tailgateSeconds": {
            "type": "number",
            "minimum": 1,
            "maximum": 600
          },
          "correlationWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 1440
          },
          "offlineMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "physical-security__sensor-event-anomaly-detect": "0.04",
  "physical-security__door-access-pattern-detect": "0.04",
  "physical-security__access-tailgating-signal-detect": "0.05",
  "physical-security__perimeter-breach-signal-detect": "0.04",
  "physical-security__camera-tampering-signal-detect": "0.04",
  "physical-security__alarm-correlation-analyze": "0.05",
  "physical-security__iot-device-behavior-analyze": "0.04",
  "physical-security__building-security-timeline": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "physical-security__sensor-event-anomaly-detect": "physical-security/sensor-event-anomaly-detect",
  "physical-security__door-access-pattern-detect": "physical-security/door-access-pattern-detect",
  "physical-security__access-tailgating-signal-detect": "physical-security/access-tailgating-signal-detect",
  "physical-security__perimeter-breach-signal-detect": "physical-security/perimeter-breach-signal-detect",
  "physical-security__camera-tampering-signal-detect": "physical-security/camera-tampering-signal-detect",
  "physical-security__alarm-correlation-analyze": "physical-security/alarm-correlation-analyze",
  "physical-security__iot-device-behavior-analyze": "physical-security/iot-device-behavior-analyze",
  "physical-security__building-security-timeline": "physical-security/building-security-timeline"
}


class BrainiacPhysicalSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — physical-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the physical-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "physical-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect sensor-event anomalies"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the physical-security group. "
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
