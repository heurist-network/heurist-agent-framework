"""Auto-generated BRAINIAC Heurist Mesh agent for group `construction-site-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "construction-site-operations__daily-report-parse",
      "description": "Parse construction daily reports. Copy supplied daily reports into structured rows with dates, locations, authors, workforce, and referenced activities. Delay wording is flagged as recorded narrative only. Docs: https://www.brainiac.software/api/construction-site-operations/daily-report-parse",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__progress-analyze",
      "description": "Analyze site progress. Compare supplied baseline and actual activity dates to identify schedule deviations. Inferred impact is labeled and is not an entitlement determination. Docs: https://www.brainiac.software/api/construction-site-operations/progress-analyze",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__delay-event-detect",
      "description": "Detect construction delay events. Collect recorded delay rows and daily-report delay wording, and separately label impacts inferred from baseline versus actual dates. Liability is not determined. Docs: https://www.brainiac.software/api/construction-site-operations/delay-event-detect",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__request-for-information-track",
      "description": "Track requests for information. Track RFI asked/due/answered dates and identify unresolved or overdue items from supplied statuses. Contractual entitlement is not decided. Docs: https://www.brainiac.software/api/construction-site-operations/request-for-information-track",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__instruction-extract",
      "description": "Extract site instructions. Extract dates, issuers, locations, referenced activities, and change flags from supplied site instructions. Docs: https://www.brainiac.software/api/construction-site-operations/instruction-extract",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__material-delivery-reconcile",
      "description": "Reconcile material deliveries. Reconcile expected and delivered material records, flagging missing deliveries and short quantities from supplied dates and counts. Docs: https://www.brainiac.software/api/construction-site-operations/material-delivery-reconcile",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__change-impact",
      "description": "Compare construction change impact. Compare change instructions with supplied scope and programme dates. Linked schedule impact is labeled inferred and is not a liability finding. Docs: https://www.brainiac.software/api/construction-site-operations/change-impact",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
      "name": "construction-site-operations__report",
      "description": "Report site operations. Combine daily reports, progress deviations, recorded and inferred delays, RFIs, instructions, deliveries, and change comparisons from supplied site records. Docs: https://www.brainiac.software/api/construction-site-operations/report",
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
          "reports": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 120
                },
                "weather": {
                  "type": "string",
                  "maxLength": 160
                },
                "workforce": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
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
                  "maxLength": 200
                },
                "baselineStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "baselineEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "actualEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "percentComplete": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "responsible": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "delays": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "recorded": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "rfis": {
            "maxItems": 200,
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
                  "maxLength": 300
                },
                "asked": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
                  "type": "string",
                  "maxLength": 40
                },
                "answered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "asker": {
                  "type": "string",
                  "maxLength": 120
                },
                "responder": {
                  "type": "string",
                  "maxLength": 120
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "instructions": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 120
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "change": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "deliveries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "maxLength": 200
                },
                "expected": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityExpected": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "quantityDelivered": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "location": {
                  "type": "string",
                  "maxLength": 200
                },
                "supplier": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "scope": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
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
  "construction-site-operations__daily-report-parse": "0.04",
  "construction-site-operations__progress-analyze": "0.05",
  "construction-site-operations__delay-event-detect": "0.04",
  "construction-site-operations__request-for-information-track": "0.04",
  "construction-site-operations__instruction-extract": "0.04",
  "construction-site-operations__material-delivery-reconcile": "0.04",
  "construction-site-operations__change-impact": "0.05",
  "construction-site-operations__report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "construction-site-operations__daily-report-parse": "construction-site-operations/daily-report-parse",
  "construction-site-operations__progress-analyze": "construction-site-operations/progress-analyze",
  "construction-site-operations__delay-event-detect": "construction-site-operations/delay-event-detect",
  "construction-site-operations__request-for-information-track": "construction-site-operations/request-for-information-track",
  "construction-site-operations__instruction-extract": "construction-site-operations/instruction-extract",
  "construction-site-operations__material-delivery-reconcile": "construction-site-operations/material-delivery-reconcile",
  "construction-site-operations__change-impact": "construction-site-operations/change-impact",
  "construction-site-operations__report": "construction-site-operations/report"
}


class BrainiacConstructionSiteOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — construction-site-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the construction-site-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "construction-site-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Parse construction daily reports"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the construction-site-operations group. "
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
