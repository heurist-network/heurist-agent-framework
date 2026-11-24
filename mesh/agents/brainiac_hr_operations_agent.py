"""Auto-generated BRAINIAC Heurist Mesh agent for group `hr-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "hr-operations__employee-document-extract",
      "description": "Extract employee documents. Read employee records and labeled document lines supplied by the caller. Dates, roles, and document types are returned as supplied. Document numbers are masked. Docs: https://www.brainiac.software/api/hr-operations/employee-document-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__employee-record-validate",
      "description": "Validate employee records. Compare employee records with the required fields supplied by the caller, and report an end date that falls before the start date. No legal requirement is added. Docs: https://www.brainiac.software/api/hr-operations/employee-record-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__employee-policy-acknowledgement-check",
      "description": "Check policy acknowledgements. Match supplied acknowledgements to supplied policies by policy id. An acknowledgement dated before the policy date is stale. This is not a compliance determination. Docs: https://www.brainiac.software/api/hr-operations/employee-policy-acknowledgement-check",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__employee-onboarding-checklist",
      "description": "List onboarding tasks. Build an onboarding checklist only from supplied onboarding policies. A document or acknowledgement counts only when it matches that policy. No statutory form is added. Docs: https://www.brainiac.software/api/hr-operations/employee-onboarding-checklist",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__employee-offboarding-checklist",
      "description": "List offboarding tasks. Build an offboarding checklist only from supplied offboarding policies. A task is met only by a supplied completion record. Access is not changed. Docs: https://www.brainiac.software/api/hr-operations/employee-offboarding-checklist",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__job-role-description-compare",
      "description": "Compare a role description. Compare Duty lines in a role description with Duty lines supplied for an employee. Unlabeled prose is not a duty. The comparison is not an employment decision. Docs: https://www.brainiac.software/api/hr-operations/job-role-description-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__workforce-document-expiry-check",
      "description": "Check document expiry. Compare supplied expiry dates with a supplied as-of date. A document is due only inside the supplied day window. No date is invented when the as-of date is missing. Docs: https://www.brainiac.software/api/hr-operations/workforce-document-expiry-check",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
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
      "name": "hr-operations__record-completeness-report",
      "description": "Report personnel record completeness. Combine supplied records, document dates, policy acknowledgements, onboarding and offboarding items, and role duties. The report does not determine legal compliance or change access. Docs: https://www.brainiac.software/api/hr-operations/record-completeness-report",
      "parameters": {
        "type": "object",
        "properties": {
          "employees": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "role": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "startDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "endDate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "identifier": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "issuedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "expiresOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stage": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "match": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "effectiveOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "acknowledgements": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "policyId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "acknowledgedOn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "completions": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "employeeId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                }
              },
              "required": [
                "field"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "roleText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "employeeText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "asOf": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10
          },
          "withinDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "hr-operations__employee-document-extract": "0.04",
  "hr-operations__employee-record-validate": "0.04",
  "hr-operations__employee-policy-acknowledgement-check": "0.04",
  "hr-operations__employee-onboarding-checklist": "0.05",
  "hr-operations__employee-offboarding-checklist": "0.05",
  "hr-operations__job-role-description-compare": "0.04",
  "hr-operations__workforce-document-expiry-check": "0.04",
  "hr-operations__record-completeness-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "hr-operations__employee-document-extract": "hr-operations/employee-document-extract",
  "hr-operations__employee-record-validate": "hr-operations/employee-record-validate",
  "hr-operations__employee-policy-acknowledgement-check": "hr-operations/employee-policy-acknowledgement-check",
  "hr-operations__employee-onboarding-checklist": "hr-operations/employee-onboarding-checklist",
  "hr-operations__employee-offboarding-checklist": "hr-operations/employee-offboarding-checklist",
  "hr-operations__job-role-description-compare": "hr-operations/job-role-description-compare",
  "hr-operations__workforce-document-expiry-check": "hr-operations/workforce-document-expiry-check",
  "hr-operations__record-completeness-report": "hr-operations/record-completeness-report"
}


class BrainiacHrOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — hr-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the hr-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "hr-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract employee documents"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the hr-operations group. "
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
