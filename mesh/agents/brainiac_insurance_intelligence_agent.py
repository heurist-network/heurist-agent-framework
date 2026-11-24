"""Auto-generated BRAINIAC Heurist Mesh agent for group `insurance-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "insurance-intelligence__policy-normalize",
      "description": "Normalize insurance policies. Normalize caller-supplied or locally extracted policy identity, term, and premium fields. Preliminary document analysis only—not coverage confirmation. Docs: https://www.brainiac.software/api/insurance-intelligence/policy-normalize",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__policy-limit-compare",
      "description": "Compare policy limits. Compare caller-supplied left/right or prior/renewal coverage limits. Not a coverage determination. Docs: https://www.brainiac.software/api/insurance-intelligence/policy-limit-compare",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__policy-exclusion-compare",
      "description": "Compare policy exclusions. Compare caller-supplied exclusion schedules across prior/renewal or left/right sides. Preliminary text matching only. Docs: https://www.brainiac.software/api/insurance-intelligence/policy-exclusion-compare",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__deductible-structure-extract",
      "description": "Extract deductible structures. Extract deductible/SIR amounts and apply-per structure from caller-supplied rows or local PDF text. Docs: https://www.brainiac.software/api/insurance-intelligence/deductible-structure-extract",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__renewal-change-detect",
      "description": "Detect insurance renewal changes. Detect insurer, premium, limit, and exclusion deltas between prior and renewal sides. Not insurer confirmation. Docs: https://www.brainiac.software/api/insurance-intelligence/renewal-change-detect",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__premium-change-analyze",
      "description": "Analyze premium changes. Analyze prior versus renewal premium amounts from caller-supplied policy or premium rows. Docs: https://www.brainiac.software/api/insurance-intelligence/premium-change-analyze",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__coverage-gap-detect",
      "description": "Detect coverage gaps. Compare caller-supplied contract requirements to supplied limits, deductibles, and exclusions. Preliminary gap signals only—not coverage confirmation. Docs: https://www.brainiac.software/api/insurance-intelligence/coverage-gap-detect",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__loss-run-normalize",
      "description": "Normalize loss runs. Normalize caller-supplied loss-run claim rows into paid/reserved/incurred fields. Not a claim adjudication. Docs: https://www.brainiac.software/api/insurance-intelligence/loss-run-normalize",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__underwriting-evidence-completeness",
      "description": "Check underwriting evidence completeness. Check caller-supplied evidence items against a required checklist. Missing items are flagged; coverage is not confirmed. Docs: https://www.brainiac.software/api/insurance-intelligence/underwriting-evidence-completeness",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
      "name": "insurance-intelligence__program-comparison",
      "description": "Compare insurance programs. Aggregate policy, limit, exclusion, deductible, premium, coverage-gap, and renewal comparisons from caller-supplied program records only. Docs: https://www.brainiac.software/api/insurance-intelligence/program-comparison",
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
                  "application/pdf",
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
              },
              "side": {
                "type": "string",
                "enum": [
                  "left",
                  "right",
                  "a",
                  "b",
                  "prior",
                  "renewal",
                  "current",
                  "required"
                ]
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
                    "application/pdf",
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
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
                  ]
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "insurer": {
                  "type": "string",
                  "maxLength": 160
                },
                "insured": {
                  "type": "string",
                  "maxLength": 160
                },
                "lineOfBusiness": {
                  "type": "string",
                  "maxLength": 120
                },
                "effectiveAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "premium": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "limits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "limitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "aggregateAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "exclusions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "deductibles": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "appliesPer": {
                  "type": "string",
                  "maxLength": 80
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current",
                    "required"
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
          "premiums": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "left",
                    "right",
                    "a",
                    "b",
                    "prior",
                    "renewal",
                    "current"
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
          "requirements": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "coverage": {
                  "type": "string",
                  "maxLength": 160
                },
                "minLimitAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxDeductibleAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "requiredEndorsement": {
                  "type": "string",
                  "maxLength": 200
                },
                "forbiddenExclusion": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "lossRuns": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "policyNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lossDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "paidAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "reservedAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "incurredAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "cause": {
                  "type": "string",
                  "maxLength": 200
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "evidenceItems": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "requiredEvidence": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
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
  "insurance-intelligence__policy-normalize": "0.04",
  "insurance-intelligence__policy-limit-compare": "0.04",
  "insurance-intelligence__policy-exclusion-compare": "0.04",
  "insurance-intelligence__deductible-structure-extract": "0.03",
  "insurance-intelligence__renewal-change-detect": "0.05",
  "insurance-intelligence__premium-change-analyze": "0.03",
  "insurance-intelligence__coverage-gap-detect": "0.05",
  "insurance-intelligence__loss-run-normalize": "0.04",
  "insurance-intelligence__underwriting-evidence-completeness": "0.03",
  "insurance-intelligence__program-comparison": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "insurance-intelligence__policy-normalize": "insurance-intelligence/policy-normalize",
  "insurance-intelligence__policy-limit-compare": "insurance-intelligence/policy-limit-compare",
  "insurance-intelligence__policy-exclusion-compare": "insurance-intelligence/policy-exclusion-compare",
  "insurance-intelligence__deductible-structure-extract": "insurance-intelligence/deductible-structure-extract",
  "insurance-intelligence__renewal-change-detect": "insurance-intelligence/renewal-change-detect",
  "insurance-intelligence__premium-change-analyze": "insurance-intelligence/premium-change-analyze",
  "insurance-intelligence__coverage-gap-detect": "insurance-intelligence/coverage-gap-detect",
  "insurance-intelligence__loss-run-normalize": "insurance-intelligence/loss-run-normalize",
  "insurance-intelligence__underwriting-evidence-completeness": "insurance-intelligence/underwriting-evidence-completeness",
  "insurance-intelligence__program-comparison": "insurance-intelligence/program-comparison"
}


class BrainiacInsuranceIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — insurance-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the insurance-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "insurance-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize insurance policies"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the insurance-intelligence group. "
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
