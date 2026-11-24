"""Auto-generated BRAINIAC Heurist Mesh agent for group `robotics-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "robotics-intelligence__rosbag-telemetry-parse",
      "description": "Parse ROS bag telemetry exports. Parse caller-supplied ROS bag topic CSV/JSON exports into labeled telemetry samples. Binary .bag/.mcap files are not fully decoded and live robots are not contacted. Docs: https://www.brainiac.software/api/robotics-intelligence/rosbag-telemetry-parse",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__ros-topic-schema-diff",
      "description": "Diff ROS topic schemas. Compare caller-supplied left/right ROS topic message types and fields. Missing schemas are not invented. Docs: https://www.brainiac.software/api/robotics-intelligence/ros-topic-schema-diff",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__telemetry-anomaly-detect",
      "description": "Detect robot telemetry anomalies. Flag caller-supplied telemetry samples whose z-score is outside ±3 of the supplied series mean. Live equipment is not contacted. Docs: https://www.brainiac.software/api/robotics-intelligence/telemetry-anomaly-detect",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__cycle-time-analyze",
      "description": "Analyze robot cycle time. Summarize caller-supplied robot cycle durations by robot, workcell, and program. Missing durations are not invented when start/end times are absent. Docs: https://www.brainiac.software/api/robotics-intelligence/cycle-time-analyze",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__downtime-root-cause",
      "description": "Cluster robot downtime root causes. Cluster caller-supplied downtime events by code/message category signals. Live PLCs and robots are not contacted. Docs: https://www.brainiac.software/api/robotics-intelligence/downtime-root-cause",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__opcua-tag-map-normalize",
      "description": "Normalize OPC UA tag maps. Normalize caller-supplied OPC UA node exports into a consistent tag map. Live OPC UA servers are not contacted. Docs: https://www.brainiac.software/api/robotics-intelligence/opcua-tag-map-normalize",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__plc-alarm-cluster",
      "description": "Cluster PLC alarms. Cluster caller-supplied PLC alarm log events by controller, code, and area. Live PLCs are not contacted. Docs: https://www.brainiac.software/api/robotics-intelligence/plc-alarm-cluster",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__maintenance-interval-estimate",
      "description": "Estimate robot maintenance intervals. Estimate remaining hours/cycles to caller-supplied maintenance intervals. OEM schedules are not invented. Docs: https://www.brainiac.software/api/robotics-intelligence/maintenance-interval-estimate",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__protocol-compatibility-check",
      "description": "Check industrial protocol compatibility. Compare caller-supplied required versus available industrial protocol names, versions, and features. Protocol specifications are not invented. Docs: https://www.brainiac.software/api/robotics-intelligence/protocol-compatibility-check",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
      "name": "robotics-intelligence__workcell-performance-report",
      "description": "Build robot workcell performance report. Aggregate rosbag parse, schema diff, anomalies, cycle time, downtime, OPC UA tags, PLC alarms, maintenance, and protocol compatibility from caller-supplied records only. Docs: https://www.brainiac.software/api/robotics-intelligence/workcell-performance-report",
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
          "samples": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "field": {
                  "type": "string",
                  "maxLength": 120
                },
                "value": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
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
          "schemas": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "topic": {
                  "type": "string",
                  "maxLength": 200
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
                "messageType": {
                  "type": "string",
                  "maxLength": 160
                },
                "fields": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "type": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "optional": {
                        "type": "boolean"
                      }
                    },
                    "additionalProperties": false
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
          "cycles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "downtime": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "workcellId": {
                  "type": "string",
                  "maxLength": 80
                },
                "startedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "endedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "durationSec": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "category": {
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
          "opcuaTags": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "nodeId": {
                  "type": "string",
                  "maxLength": 200
                },
                "browseName": {
                  "type": "string",
                  "maxLength": 160
                },
                "displayName": {
                  "type": "string",
                  "maxLength": 160
                },
                "dataType": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 300
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
          "plcAlarms": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "controllerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 400
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
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
          "maintenance": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "robotId": {
                  "type": "string",
                  "maxLength": 80
                },
                "component": {
                  "type": "string",
                  "maxLength": 160
                },
                "runtimeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "intervalCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lastServiceAt": {
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
          "protocols": {
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
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "required",
                    "available",
                    "controller",
                    "device"
                  ]
                },
                "features": {
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
  "robotics-intelligence__rosbag-telemetry-parse": "0.04",
  "robotics-intelligence__ros-topic-schema-diff": "0.03",
  "robotics-intelligence__telemetry-anomaly-detect": "0.04",
  "robotics-intelligence__cycle-time-analyze": "0.04",
  "robotics-intelligence__downtime-root-cause": "0.04",
  "robotics-intelligence__opcua-tag-map-normalize": "0.03",
  "robotics-intelligence__plc-alarm-cluster": "0.04",
  "robotics-intelligence__maintenance-interval-estimate": "0.04",
  "robotics-intelligence__protocol-compatibility-check": "0.03",
  "robotics-intelligence__workcell-performance-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "robotics-intelligence__rosbag-telemetry-parse": "robotics-intelligence/rosbag-telemetry-parse",
  "robotics-intelligence__ros-topic-schema-diff": "robotics-intelligence/ros-topic-schema-diff",
  "robotics-intelligence__telemetry-anomaly-detect": "robotics-intelligence/telemetry-anomaly-detect",
  "robotics-intelligence__cycle-time-analyze": "robotics-intelligence/cycle-time-analyze",
  "robotics-intelligence__downtime-root-cause": "robotics-intelligence/downtime-root-cause",
  "robotics-intelligence__opcua-tag-map-normalize": "robotics-intelligence/opcua-tag-map-normalize",
  "robotics-intelligence__plc-alarm-cluster": "robotics-intelligence/plc-alarm-cluster",
  "robotics-intelligence__maintenance-interval-estimate": "robotics-intelligence/maintenance-interval-estimate",
  "robotics-intelligence__protocol-compatibility-check": "robotics-intelligence/protocol-compatibility-check",
  "robotics-intelligence__workcell-performance-report": "robotics-intelligence/workcell-performance-report"
}


class BrainiacRoboticsIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — robotics-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the robotics-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "robotics-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Parse ROS bag telemetry exports"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the robotics-intelligence group. "
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
