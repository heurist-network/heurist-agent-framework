"""Auto-generated BRAINIAC Heurist Mesh agent for group `conversion-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "conversion-intelligence__analytics-funnel-analyze",
      "description": "Analyze an analytics funnel. Calculate stage-to-stage conversion rates and drop-offs from supplied funnel counts. Missing counts are not filled in, and a drop-off is not treated as a proven cause. Docs: https://www.brainiac.software/api/conversion-intelligence/analytics-funnel-analyze",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__landing-page-dropoff-detect",
      "description": "Detect landing page drop-off. Rank supplied pages by measured exit rate from views and exits. Rates use only caller counts and do not claim why visitors left. Docs: https://www.brainiac.software/api/conversion-intelligence/landing-page-dropoff-detect",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__checkout-funnel-audit",
      "description": "Audit a checkout funnel. Audit supplied cart, checkout, payment, and purchase stage counts. The largest measured drop-off is reported without inventing missing steps. Docs: https://www.brainiac.software/api/conversion-intelligence/checkout-funnel-audit",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__event-coverage-check",
      "description": "Check conversion event coverage. Compare expected tracking events with supplied event counts. Missing or zero events are flagged. No analytics account is accessed. Docs: https://www.brainiac.software/api/conversion-intelligence/event-coverage-check",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__traffic-source-quality-analyze",
      "description": "Analyze traffic source quality. Calculate conversion rates by supplied traffic source. Ranking uses only sources that meet the disclosed sample minimum and does not claim causation. Docs: https://www.brainiac.software/api/conversion-intelligence/traffic-source-quality-analyze",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__form-abandonment-analyze",
      "description": "Analyze form abandonment. Measure form completion and field abandonment from supplied starts, completes, and field counts. Differences are associations in the numbers, not proven causes. Docs: https://www.brainiac.software/api/conversion-intelligence/form-abandonment-analyze",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__segment-compare",
      "description": "Compare conversion segments. Compare segment conversion rates only when both samples meet the disclosed minimum size. Rate differences are not treated as causation. Docs: https://www.brainiac.software/api/conversion-intelligence/segment-compare",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
      "name": "conversion-intelligence__diagnostics-report",
      "description": "Report conversion diagnostics. Combine funnel drop-offs, page exits, event coverage, source rates, form abandonment, and segment comparisons from supplied counts. No traffic or revenue is invented. Docs: https://www.brainiac.software/api/conversion-intelligence/diagnostics-report",
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
          "funnels": {
            "maxItems": 20,
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
                }
              },
              "additionalProperties": false
            }
          },
          "stages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "funnelId": {
                  "type": "string",
                  "maxLength": 80
                },
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "order": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 200
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "pages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "path": {
                  "type": "string",
                  "maxLength": 500
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "views": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "exits": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 120,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "page": {
                  "type": "string",
                  "maxLength": 500
                },
                "required": {
                  "type": "boolean"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "expectedEvents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "name"
              ],
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "forms": {
            "maxItems": 40,
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
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "completes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "fields": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "formId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "starts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "abandons": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "segments": {
            "maxItems": 40,
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
                "sessions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "conversions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
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
  "conversion-intelligence__analytics-funnel-analyze": "0.04",
  "conversion-intelligence__landing-page-dropoff-detect": "0.04",
  "conversion-intelligence__checkout-funnel-audit": "0.05",
  "conversion-intelligence__event-coverage-check": "0.04",
  "conversion-intelligence__traffic-source-quality-analyze": "0.05",
  "conversion-intelligence__form-abandonment-analyze": "0.04",
  "conversion-intelligence__segment-compare": "0.05",
  "conversion-intelligence__diagnostics-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "conversion-intelligence__analytics-funnel-analyze": "conversion-intelligence/analytics-funnel-analyze",
  "conversion-intelligence__landing-page-dropoff-detect": "conversion-intelligence/landing-page-dropoff-detect",
  "conversion-intelligence__checkout-funnel-audit": "conversion-intelligence/checkout-funnel-audit",
  "conversion-intelligence__event-coverage-check": "conversion-intelligence/event-coverage-check",
  "conversion-intelligence__traffic-source-quality-analyze": "conversion-intelligence/traffic-source-quality-analyze",
  "conversion-intelligence__form-abandonment-analyze": "conversion-intelligence/form-abandonment-analyze",
  "conversion-intelligence__segment-compare": "conversion-intelligence/segment-compare",
  "conversion-intelligence__diagnostics-report": "conversion-intelligence/diagnostics-report"
}


class BrainiacConversionIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — conversion-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the conversion-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "conversion-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze an analytics funnel"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the conversion-intelligence group. "
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
