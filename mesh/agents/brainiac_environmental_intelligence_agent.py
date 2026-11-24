"""Auto-generated BRAINIAC Heurist Mesh agent for group `environmental-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "environmental-intelligence__carbon-emission-factor-normalize",
      "description": "Normalize carbon emission factors. Normalize caller-supplied emission factors with source, version, and asOf provenance. Disclosed public-style DEFRA/eGRID references may be listed when no factors are supplied. No paid ESG database. Docs: https://www.brainiac.software/api/environmental-intelligence/carbon-emission-factor-normalize",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__scope-1-emissions-calculate",
      "description": "Calculate Scope 1 emissions. Calculate Scope 1 emissions from caller-supplied activity quantities and emission factors (or disclosed public-style factors when unmatched). Factor source, version, and asOf are echoed. Docs: https://www.brainiac.software/api/environmental-intelligence/scope-1-emissions-calculate",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__scope-2-emissions-calculate",
      "description": "Calculate Scope 2 emissions. Calculate Scope 2 emissions from electricity activities and caller factors, disclosed public-style grid factors, or optional key-free Carbon Intensity API intensity. Docs: https://www.brainiac.software/api/environmental-intelligence/scope-2-emissions-calculate",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__scope-3-supplier-data-validate",
      "description": "Validate Scope 3 supplier data. Validate caller-supplied Scope 3 supplier emission rows for identity, period, quantity, and factor provenance. Recalculates when activity quantity and a factor are available. Docs: https://www.brainiac.software/api/environmental-intelligence/scope-3-supplier-data-validate",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__carbon-report-consistency-check",
      "description": "Check carbon report consistency. Compare reported Scope 1–3 totals to summed scope values from caller-supplied reports and/or calculated activities. Flags inconsistent totals within tolerance. Docs: https://www.brainiac.software/api/environmental-intelligence/carbon-report-consistency-check",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__water-consumption-anomaly-detect",
      "description": "Detect water consumption anomalies. Detect anomalous water consumption using z-scores on caller-supplied facility water quantity series. Docs: https://www.brainiac.software/api/environmental-intelligence/water-consumption-anomaly-detect",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__water-intensity-calculate",
      "description": "Calculate water intensity. Calculate water intensity (m³ per denominator unit) from caller-supplied water quantities and production/occupancy denominators. Docs: https://www.brainiac.software/api/environmental-intelligence/water-intensity-calculate",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__permit-expiry-check",
      "description": "Check environmental permit expiry. Check caller-supplied environmental permit expiry dates against asOf and a warning window. Compliance determinations are not made. Docs: https://www.brainiac.software/api/environmental-intelligence/permit-expiry-check",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__waste-manifest-reconcile",
      "description": "Reconcile waste manifests. Reconcile shipper and receiver waste manifest rows by manifest number, waste code, unit, and quantity. Docs: https://www.brainiac.software/api/environmental-intelligence/waste-manifest-reconcile",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "environmental-intelligence__evidence-report",
      "description": "Build environmental evidence report. Aggregate emission-factor, Scope 1–3, carbon-report, water, permit, and waste sections from caller-supplied operational records (and optional Carbon Intensity fetch). Docs: https://www.brainiac.software/api/environmental-intelligence/evidence-report",
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
          "factors": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "kgCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "gCo2ePerUnit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "scopeHint": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3",
                    "any"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "activities": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "activityKey": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope": {
                  "type": "string",
                  "enum": [
                    "1",
                    "2",
                    "3"
                  ]
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
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
          "suppliers": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "spendAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "activityQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reportedKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "factorId": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorSource": {
                  "type": "string",
                  "maxLength": 200
                },
                "factorVersion": {
                  "type": "string",
                  "maxLength": 80
                },
                "factorAsOf": {
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
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "scope1KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope2KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "scope3KgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "totalKgCo2e": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "waterRecords": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantityM3": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominator": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "denominatorUnit": {
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
          "permits": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "permitType": {
                  "type": "string",
                  "maxLength": 120
                },
                "issuedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "authority": {
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
          "wasteManifests": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "manifestNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "wasteCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "maxLength": 200
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "shippedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "receivedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "facilityId": {
                  "type": "string",
                  "maxLength": 80
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "shipper",
                    "receiver",
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
          "carbonIntensity": {
            "type": "object",
            "properties": {
              "fetch": {
                "type": "boolean"
              },
              "regionId": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "expiryWarningDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 3650
          },
          "waterAnomalyZ": {
            "type": "number",
            "minimum": 1,
            "maximum": 10
          },
          "consistencyToleranceKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "environmental-intelligence__carbon-emission-factor-normalize": "0.03",
  "environmental-intelligence__scope-1-emissions-calculate": "0.04",
  "environmental-intelligence__scope-2-emissions-calculate": "0.04",
  "environmental-intelligence__scope-3-supplier-data-validate": "0.04",
  "environmental-intelligence__carbon-report-consistency-check": "0.04",
  "environmental-intelligence__water-consumption-anomaly-detect": "0.03",
  "environmental-intelligence__water-intensity-calculate": "0.03",
  "environmental-intelligence__permit-expiry-check": "0.03",
  "environmental-intelligence__waste-manifest-reconcile": "0.04",
  "environmental-intelligence__evidence-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "environmental-intelligence__carbon-emission-factor-normalize": "environmental-intelligence/carbon-emission-factor-normalize",
  "environmental-intelligence__scope-1-emissions-calculate": "environmental-intelligence/scope-1-emissions-calculate",
  "environmental-intelligence__scope-2-emissions-calculate": "environmental-intelligence/scope-2-emissions-calculate",
  "environmental-intelligence__scope-3-supplier-data-validate": "environmental-intelligence/scope-3-supplier-data-validate",
  "environmental-intelligence__carbon-report-consistency-check": "environmental-intelligence/carbon-report-consistency-check",
  "environmental-intelligence__water-consumption-anomaly-detect": "environmental-intelligence/water-consumption-anomaly-detect",
  "environmental-intelligence__water-intensity-calculate": "environmental-intelligence/water-intensity-calculate",
  "environmental-intelligence__permit-expiry-check": "environmental-intelligence/permit-expiry-check",
  "environmental-intelligence__waste-manifest-reconcile": "environmental-intelligence/waste-manifest-reconcile",
  "environmental-intelligence__evidence-report": "environmental-intelligence/evidence-report"
}


class BrainiacEnvironmentalIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — environmental-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the environmental-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "environmental-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize carbon emission factors"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the environmental-intelligence group. "
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
