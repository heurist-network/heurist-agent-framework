"""Auto-generated BRAINIAC Heurist Mesh agent for group `manufacturing-quality` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "manufacturing-quality__production-inspection-parse",
      "description": "Parse production inspections. Copy supplied inspections, measurements, batches, and standards into a consistent packet with pass/fail outcomes. Tolerances are not invented. Docs: https://www.brainiac.software/api/manufacturing-quality/production-inspection-parse",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__defect-classify",
      "description": "Classify manufacturing defects. Classify failed inspections with transparent token rules such as dimensional, surface, assembly, material, or functional. Classification is not a certification. Docs: https://www.brainiac.software/api/manufacturing-quality/defect-classify",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__defect-rate-calculate",
      "description": "Calculate defect rate. Calculate defect rate from decided pass/fail inspections and compare it with an explicitly supplied threshold. Small samples are disclosed. Docs: https://www.brainiac.software/api/manufacturing-quality/defect-rate-calculate",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__batch-compare",
      "description": "Compare batch quality. Compare batch defect rates only when each batch meets the disclosed sample minimum. Rate differences are not treated as regulatory findings. Docs: https://www.brainiac.software/api/manufacturing-quality/batch-compare",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__nonconformance-report-generate",
      "description": "Generate nonconformance reports. Assemble structured nonconformance rows from failed inspections with linked measurements and evidence ids. The report does not claim certification or compliance. Docs: https://www.brainiac.software/api/manufacturing-quality/nonconformance-report-generate",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__production-tolerance-check",
      "description": "Check production tolerances. Compare supplied measurements with caller-supplied lower and upper limits. SPC mean±3σ limits are computed only when the disclosed observation minimum is met. Docs: https://www.brainiac.software/api/manufacturing-quality/production-tolerance-check",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__root-cause-evidence-analyze",
      "description": "Analyze root-cause evidence. Link supplied evidence rows to failed inspections by id and summarize evidence kinds. Links are associations in the request, not proven root causes. Docs: https://www.brainiac.software/api/manufacturing-quality/root-cause-evidence-analyze",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
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
      "name": "manufacturing-quality__report",
      "description": "Report manufacturing quality. Combine inspection parsing, defect classes, defect rates, batch comparisons, tolerances, NCR rows, and evidence links from supplied records. No certification or compliance is claimed. Docs: https://www.brainiac.software/api/manufacturing-quality/report",
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
          "inspections": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "partId": {
                  "type": "string",
                  "maxLength": 80
                },
                "result": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectCode": {
                  "type": "string",
                  "maxLength": 80
                },
                "defectText": {
                  "type": "string",
                  "maxLength": 500
                },
                "inspectedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "inspector": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "measurements": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "characteristic": {
                  "type": "string",
                  "maxLength": 120
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
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "standards": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "characteristic": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "target": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "lower": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "upper": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "characteristic"
              ],
              "additionalProperties": false
            }
          },
          "batches": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 160
                },
                "produced": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "started": {
                  "type": "string",
                  "maxLength": 40
                },
                "ended": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "batchId": {
                  "type": "string",
                  "maxLength": 80
                },
                "inspectionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "thresholds": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "defectRateThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "spcMinSample": {
            "type": "integer",
            "minimum": 2,
            "maximum": 100000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "manufacturing-quality__production-inspection-parse": "0.04",
  "manufacturing-quality__defect-classify": "0.04",
  "manufacturing-quality__defect-rate-calculate": "0.04",
  "manufacturing-quality__batch-compare": "0.05",
  "manufacturing-quality__nonconformance-report-generate": "0.05",
  "manufacturing-quality__production-tolerance-check": "0.05",
  "manufacturing-quality__root-cause-evidence-analyze": "0.04",
  "manufacturing-quality__report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "manufacturing-quality__production-inspection-parse": "manufacturing-quality/production-inspection-parse",
  "manufacturing-quality__defect-classify": "manufacturing-quality/defect-classify",
  "manufacturing-quality__defect-rate-calculate": "manufacturing-quality/defect-rate-calculate",
  "manufacturing-quality__batch-compare": "manufacturing-quality/batch-compare",
  "manufacturing-quality__nonconformance-report-generate": "manufacturing-quality/nonconformance-report-generate",
  "manufacturing-quality__production-tolerance-check": "manufacturing-quality/production-tolerance-check",
  "manufacturing-quality__root-cause-evidence-analyze": "manufacturing-quality/root-cause-evidence-analyze",
  "manufacturing-quality__report": "manufacturing-quality/report"
}


class BrainiacManufacturingQualityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — manufacturing-quality",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the manufacturing-quality catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "manufacturing-quality", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Parse production inspections"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the manufacturing-quality group. "
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
