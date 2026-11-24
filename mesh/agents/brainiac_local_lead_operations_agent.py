"""Auto-generated BRAINIAC Heurist Mesh agent for group `local-lead-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "local-lead-operations__record-normalize",
      "description": "Normalize lead records. Copy supplied leads, calls, quotes, responses, and enquiries into a consistent inventory. Counts come from the request only. No CRM account is accessed. Docs: https://www.brainiac.software/api/local-lead-operations/record-normalize",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__missed-call-analyze",
      "description": "Analyze missed-call leads. Identify missed calls and whether a later response was recorded for the same lead. Delays use supplied timestamps only. Docs: https://www.brainiac.software/api/local-lead-operations/missed-call-analyze",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__response-delay-detect",
      "description": "Detect lead response delays. Calculate hours from enquiry received time to the first recorded response. Overdue uses the disclosed hour limit and does not claim conversion. Docs: https://www.brainiac.software/api/local-lead-operations/response-delay-detect",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__quote-followup-priority",
      "description": "Prioritize quote follow-ups. Rank leads with transparent rules for missed calls, response delays, and quotes without outcomes. Priority is not a prediction that a customer will convert. Docs: https://www.brainiac.software/api/local-lead-operations/quote-followup-priority",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__unconverted-quote-detect",
      "description": "Detect unconverted quotes. Find quotes with no recorded outcome and age them from the sent timestamp. A missing outcome is not treated as a final loss. Docs: https://www.brainiac.software/api/local-lead-operations/unconverted-quote-detect",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__source-performance-analyze",
      "description": "Analyze lead source performance. Calculate conversion rates from supplied source lead and converted counts. Ranking uses only sources that meet the disclosed sample minimum. Docs: https://www.brainiac.software/api/local-lead-operations/source-performance-analyze",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__customer-enquiry-classify",
      "description": "Classify customer enquiries. Classify enquiry text with transparent token rules such as emergency, quote, booking, or complaint. Classification is not a conversion prediction. Docs: https://www.brainiac.software/api/local-lead-operations/customer-enquiry-classify",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "local-lead-operations__conversion-opportunity-report",
      "description": "Report lead conversion opportunities. Combine unanswered missed calls, response delays, unconverted quotes, source rates, and enquiry classes from supplied records. No messages are sent and conversion is not claimed. Docs: https://www.brainiac.software/api/local-lead-operations/conversion-opportunity-report",
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
          "leads": {
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
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "email": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 120
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "calls": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "duration": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 86400
                },
                "missed": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sent": {
                  "type": "string",
                  "maxLength": 40
                },
                "outcome": {
                  "type": "string",
                  "maxLength": 80
                },
                "outcomeAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "responses": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "enquiries": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "sources": {
            "maxItems": 80,
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
                "leads": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "converted": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "responseLimitHours": {
            "type": "number",
            "minimum": 0,
            "maximum": 720
          },
          "quoteLimitDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "local-lead-operations__record-normalize": "0.04",
  "local-lead-operations__missed-call-analyze": "0.04",
  "local-lead-operations__response-delay-detect": "0.04",
  "local-lead-operations__quote-followup-priority": "0.05",
  "local-lead-operations__unconverted-quote-detect": "0.04",
  "local-lead-operations__source-performance-analyze": "0.05",
  "local-lead-operations__customer-enquiry-classify": "0.04",
  "local-lead-operations__conversion-opportunity-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "local-lead-operations__record-normalize": "local-lead-operations/record-normalize",
  "local-lead-operations__missed-call-analyze": "local-lead-operations/missed-call-analyze",
  "local-lead-operations__response-delay-detect": "local-lead-operations/response-delay-detect",
  "local-lead-operations__quote-followup-priority": "local-lead-operations/quote-followup-priority",
  "local-lead-operations__unconverted-quote-detect": "local-lead-operations/unconverted-quote-detect",
  "local-lead-operations__source-performance-analyze": "local-lead-operations/source-performance-analyze",
  "local-lead-operations__customer-enquiry-classify": "local-lead-operations/customer-enquiry-classify",
  "local-lead-operations__conversion-opportunity-report": "local-lead-operations/conversion-opportunity-report"
}


class BrainiacLocalLeadOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — local-lead-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the local-lead-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "local-lead-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize lead records"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the local-lead-operations group. "
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
