"""Auto-generated BRAINIAC Heurist Mesh agent for group `property-maintenance` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "property-maintenance__request-classify",
      "description": "Classify a maintenance request. Classify a stated type only from an explicit token, and flag a documented safety keyword for a person to review. An unrecognized word is left unrecognized. Docs: https://www.brainiac.software/api/property-maintenance/request-classify",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__priority-assess",
      "description": "Assess maintenance priority. Apply a fixed order: a safety keyword, then a stated emergency, urgent, or routine urgency. A missing urgency is not treated as routine, and the result is not a safety verdict. Docs: https://www.brainiac.software/api/property-maintenance/priority-assess",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__work-order-generate",
      "description": "Draft a maintenance work order. Write a draft from the stated property, type, issue, and contractor name. The draft is not sent and no contractor is dispatched. Docs: https://www.brainiac.software/api/property-maintenance/work-order-generate",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__contractor-quote-compare",
      "description": "Compare contractor quotes. Compare supplied quotes by price, stated completion days, scope, and exclusions. The lowest price is not a recommendation, and different currencies are not converted. Docs: https://www.brainiac.software/api/property-maintenance/contractor-quote-compare",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__response-sla-check",
      "description": "Check a response service level. Compare a supplied response time with the service level for that stated urgency. No deadline is assumed when the caller does not supply one. Docs: https://www.brainiac.software/api/property-maintenance/response-sla-check",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__repair-history-analyze",
      "description": "Analyze repair history. Count supplied requests for the same property and type. A repeat is reported at three or more. The count is not a finding that the property is unsafe. Docs: https://www.brainiac.software/api/property-maintenance/repair-history-analyze",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__invoice-validate",
      "description": "Validate a maintenance invoice. Compare an invoice amount and scope with one linked quote. A difference is not an overcharge finding, and a stated paid status does not mean a payment was sent. Docs: https://www.brainiac.software/api/property-maintenance/invoice-validate",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-maintenance__report",
      "description": "Report property maintenance. Combine supplied request classes, safety keywords, quote comparisons, service levels, repeat repairs, and invoice differences. The report does not call a property safe or dispatch a contractor. Docs: https://www.brainiac.software/api/property-maintenance/report",
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
          "requests": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "property": {
                  "type": "string",
                  "maxLength": 160
                },
                "reported": {
                  "type": "string",
                  "maxLength": 40
                },
                "responded": {
                  "type": "string",
                  "maxLength": 40
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "quotes": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "days": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "exclusions": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "quoteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "scope": {
                  "type": "string",
                  "maxLength": 300
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "slas": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "urgency": {
                  "type": "string",
                  "maxLength": 40
                },
                "limit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "works": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractor": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "property-maintenance__request-classify": "0.04",
  "property-maintenance__priority-assess": "0.04",
  "property-maintenance__work-order-generate": "0.05",
  "property-maintenance__contractor-quote-compare": "0.05",
  "property-maintenance__response-sla-check": "0.04",
  "property-maintenance__repair-history-analyze": "0.04",
  "property-maintenance__invoice-validate": "0.04",
  "property-maintenance__report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "property-maintenance__request-classify": "property-maintenance/request-classify",
  "property-maintenance__priority-assess": "property-maintenance/priority-assess",
  "property-maintenance__work-order-generate": "property-maintenance/work-order-generate",
  "property-maintenance__contractor-quote-compare": "property-maintenance/contractor-quote-compare",
  "property-maintenance__response-sla-check": "property-maintenance/response-sla-check",
  "property-maintenance__repair-history-analyze": "property-maintenance/repair-history-analyze",
  "property-maintenance__invoice-validate": "property-maintenance/invoice-validate",
  "property-maintenance__report": "property-maintenance/report"
}


class BrainiacPropertyMaintenanceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — property-maintenance",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the property-maintenance catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "property-maintenance", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Classify a maintenance request"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the property-maintenance group. "
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
