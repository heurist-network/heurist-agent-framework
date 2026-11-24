"""Auto-generated BRAINIAC Heurist Mesh agent for group `network-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "network-intelligence__log-normalize",
      "description": "Normalize network logs. Normalize caller-supplied network/syslog rows. Private addresses in caller data are retained but never contacted. Docs: https://www.brainiac.software/api/network-intelligence/log-normalize",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__latency-anomaly-detect",
      "description": "Detect network latency anomalies. Detect anomalous latency using z-scores on caller-supplied path samples. No active probing of private networks. Docs: https://www.brainiac.software/api/network-intelligence/latency-anomaly-detect",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__packet-loss-pattern-analyze",
      "description": "Analyze packet-loss patterns. Analyze caller-supplied packet-loss percent or sent/lost counts against a warning threshold. Docs: https://www.brainiac.software/api/network-intelligence/packet-loss-pattern-analyze",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__dns-resolution-diagnose",
      "description": "Diagnose DNS resolution. Diagnose caller-supplied DNS answers against expected values, or optionally query key-free public DNS for a public hostname. Docs: https://www.brainiac.software/api/network-intelligence/dns-resolution-diagnose",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__bgp-route-change-analyze",
      "description": "Analyze BGP route changes. Compare before/after BGP route rows for AS-path, next-hop, and origin changes from caller-supplied tables. Docs: https://www.brainiac.software/api/network-intelligence/bgp-route-change-analyze",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__certificate-expiry-inventory",
      "description": "Inventory TLS certificate expiry. Inventory caller-supplied TLS certificate expiry dates, or optionally inspect a public hostname on port 443 only. Docs: https://www.brainiac.software/api/network-intelligence/certificate-expiry-inventory",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__configuration-diff",
      "description": "Diff network configurations. Diff left/right or before/after network configuration key/value rows from caller-supplied exports. Docs: https://www.brainiac.software/api/network-intelligence/configuration-diff",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__ip-address-reputation-check",
      "description": "Check IP address reputation. Check caller-supplied IP reputation labels/scores only. No paid reputation API is used and private networks are not scanned. Docs: https://www.brainiac.software/api/network-intelligence/ip-address-reputation-check",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__incident-timeline-build",
      "description": "Build network incident timeline. Build a chronological timeline from caller-supplied incidents and severe log events. Docs: https://www.brainiac.software/api/network-intelligence/incident-timeline-build",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
      "name": "network-intelligence__infrastructure-health-report",
      "description": "Build network infrastructure health report. Aggregate log, latency, packet-loss, DNS, BGP, certificate, configuration, reputation, and incident sections from caller-supplied network records. Docs: https://www.brainiac.software/api/network-intelligence/infrastructure-health-report",
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
          "logs": {
            "maxItems": 10000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "facility": {
                  "type": "string",
                  "maxLength": 80
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "message": {
                  "type": "string",
                  "maxLength": 4000
                },
                "sourceIp": {
                  "type": "string",
                  "maxLength": 80
                },
                "destinationIp": {
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
          "latencySamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
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
          "packetLossSamples": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pathId": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "sent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lossPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "dnsRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "recordType": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "MX",
                    "TXT",
                    "NS",
                    "SOA"
                  ]
                },
                "answer": {
                  "type": "string",
                  "maxLength": 500
                },
                "resolver": {
                  "type": "string",
                  "maxLength": 80
                },
                "rcode": {
                  "type": "string",
                  "maxLength": 40
                },
                "latencyMs": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "expectedAnswer": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "bgpRoutes": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "prefix": {
                  "type": "string",
                  "maxLength": 80
                },
                "peer": {
                  "type": "string",
                  "maxLength": 80
                },
                "asPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "nextHop": {
                  "type": "string",
                  "maxLength": 80
                },
                "originAs": {
                  "type": "string",
                  "maxLength": 40
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "fingerprintSha256": {
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
          "configs": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 200
                },
                "key": {
                  "type": "string",
                  "maxLength": 200
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "before",
                    "after",
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
          "reputations": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "hostname": {
                  "type": "string",
                  "maxLength": 253
                },
                "listed": {
                  "type": "boolean"
                },
                "listName": {
                  "type": "string",
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "score": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "observedAt": {
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
          "incidents": {
            "maxItems": 5000,
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
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "detail": {
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
          "publicDns": {
            "type": "object",
            "properties": {
              "hostname": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "recordType": {
                "type": "string",
                "enum": [
                  "A",
                  "AAAA",
                  "CNAME",
                  "MX",
                  "TXT",
                  "NS"
                ]
              }
            },
            "required": [
              "hostname"
            ],
            "additionalProperties": false
          },
          "publicTls": {
            "type": "object",
            "properties": {
              "host": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              }
            },
            "required": [
              "host"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "latencyAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "packetLossWarnPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "network-intelligence__log-normalize": "0.03",
  "network-intelligence__latency-anomaly-detect": "0.03",
  "network-intelligence__packet-loss-pattern-analyze": "0.03",
  "network-intelligence__dns-resolution-diagnose": "0.03",
  "network-intelligence__bgp-route-change-analyze": "0.04",
  "network-intelligence__certificate-expiry-inventory": "0.03",
  "network-intelligence__configuration-diff": "0.03",
  "network-intelligence__ip-address-reputation-check": "0.03",
  "network-intelligence__incident-timeline-build": "0.03",
  "network-intelligence__infrastructure-health-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "network-intelligence__log-normalize": "network-intelligence/log-normalize",
  "network-intelligence__latency-anomaly-detect": "network-intelligence/latency-anomaly-detect",
  "network-intelligence__packet-loss-pattern-analyze": "network-intelligence/packet-loss-pattern-analyze",
  "network-intelligence__dns-resolution-diagnose": "network-intelligence/dns-resolution-diagnose",
  "network-intelligence__bgp-route-change-analyze": "network-intelligence/bgp-route-change-analyze",
  "network-intelligence__certificate-expiry-inventory": "network-intelligence/certificate-expiry-inventory",
  "network-intelligence__configuration-diff": "network-intelligence/configuration-diff",
  "network-intelligence__ip-address-reputation-check": "network-intelligence/ip-address-reputation-check",
  "network-intelligence__incident-timeline-build": "network-intelligence/incident-timeline-build",
  "network-intelligence__infrastructure-health-report": "network-intelligence/infrastructure-health-report"
}


class BrainiacNetworkIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — network-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the network-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "network-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize network logs"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the network-intelligence group. "
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
