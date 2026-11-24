"""Auto-generated BRAINIAC Heurist Mesh agent for group `rental-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "rental-operations__tenant-move-in-readiness",
      "description": "Check move-in readiness. Compare supplied move-in items with the items the caller marks as required. A pending item is not counted as present, and a complete list does not mean the handover was done. Docs: https://www.brainiac.software/api/rental-operations/tenant-move-in-readiness",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__deposit-payment-evidence-check",
      "description": "Check deposit payment evidence. Compare deposit evidence with the expected amount, currency, and reference. A matching screenshot is still not treated as cleared funds. Docs: https://www.brainiac.software/api/rental-operations/deposit-payment-evidence-check",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__first-rent-payment-check",
      "description": "Check first-rent payment evidence. Compare first-rent evidence with the expected amount, currency, and reference. A payment instruction is not treated as cleared funds. Docs: https://www.brainiac.software/api/rental-operations/first-rent-payment-check",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__tenancy-document-completeness",
      "description": "Check tenancy document completeness. List the document kinds the caller marked as required and which of them were supplied. A jurisdiction name does not add a legal checklist. Docs: https://www.brainiac.software/api/rental-operations/tenancy-document-completeness",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__move-in-inventory-compare",
      "description": "Compare move-in inventory. Compare a baseline inventory with the move-in list by room, name, condition, and count. A difference is not a finding of liability. Docs: https://www.brainiac.software/api/rental-operations/move-in-inventory-compare",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__tenant-document-expiry-check",
      "description": "Check tenant document expiry. Compare supplied expiry dates with a supplied as-of date. No as-of date means expiry is not judged, and a document number is reduced to its last four characters. Docs: https://www.brainiac.software/api/rental-operations/tenant-document-expiry-check",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__tenancy-obligation-extract",
      "description": "Extract tenancy obligations. Copy labeled obligations, the stated party, and a real due date. The wording is not treated as legal advice or an eviction right. Docs: https://www.brainiac.software/api/rental-operations/tenancy-obligation-extract",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
      "name": "rental-operations__handover-report",
      "description": "Report a rental handover. Combine the supplied readiness items, payment evidence, inventory comparison, document dates, and obligations. The report does not clear funds, give legal advice, or complete a handover. Docs: https://www.brainiac.software/api/rental-operations/handover-report",
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
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "items": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "purpose": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 40
                },
                "form": {
                  "type": "string",
                  "maxLength": 40
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
                "reference": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "issued": {
                  "type": "string",
                  "maxLength": 40
                },
                "expires": {
                  "type": "string",
                  "maxLength": 40
                },
                "holder": {
                  "type": "string",
                  "maxLength": 160
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "inventory": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "list": {
                  "type": "string",
                  "maxLength": 40
                },
                "room": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 80
                },
                "condition": {
                  "type": "string",
                  "maxLength": 80
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "obligations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "party": {
                  "type": "string",
                  "maxLength": 40
                },
                "due": {
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
          "jurisdiction": {
            "type": "string",
            "maxLength": 40
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
  "rental-operations__tenant-move-in-readiness": "0.05",
  "rental-operations__deposit-payment-evidence-check": "0.04",
  "rental-operations__first-rent-payment-check": "0.04",
  "rental-operations__tenancy-document-completeness": "0.04",
  "rental-operations__move-in-inventory-compare": "0.05",
  "rental-operations__tenant-document-expiry-check": "0.04",
  "rental-operations__tenancy-obligation-extract": "0.04",
  "rental-operations__handover-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "rental-operations__tenant-move-in-readiness": "rental-operations/tenant-move-in-readiness",
  "rental-operations__deposit-payment-evidence-check": "rental-operations/deposit-payment-evidence-check",
  "rental-operations__first-rent-payment-check": "rental-operations/first-rent-payment-check",
  "rental-operations__tenancy-document-completeness": "rental-operations/tenancy-document-completeness",
  "rental-operations__move-in-inventory-compare": "rental-operations/move-in-inventory-compare",
  "rental-operations__tenant-document-expiry-check": "rental-operations/tenant-document-expiry-check",
  "rental-operations__tenancy-obligation-extract": "rental-operations/tenancy-obligation-extract",
  "rental-operations__handover-report": "rental-operations/handover-report"
}


class BrainiacRentalOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — rental-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the rental-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "rental-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Check move-in readiness"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the rental-operations group. "
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
