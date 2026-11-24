"""Auto-generated BRAINIAC Heurist Mesh agent for group `public-records` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "public-records__court-decision-search-normalize",
      "description": "Normalize court decision records. Normalize supplied court records and label allegation, investigation, charge, and judgment statuses separately. Guilt is never inferred. Docs: https://www.brainiac.software/api/public-records/court-decision-search-normalize",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__court-case-timeline-extract",
      "description": "Extract court case timelines. Group supplied court records by case number into dated timelines. Non-judgment steps are not treated as guilt. Docs: https://www.brainiac.software/api/public-records/court-case-timeline-extract",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__regulatory-enforcement-search",
      "description": "Search regulatory enforcement actions. List supplied regulatory enforcement actions with explicit status labels. Investigations are not treated as guilt. Docs: https://www.brainiac.software/api/public-records/regulatory-enforcement-search",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__crime-statistics-compare",
      "description": "Compare public crime statistics. Compare supplied official crime counts or rates across periods for the same offense and area. Missing values are not invented. Docs: https://www.brainiac.software/api/public-records/crime-statistics-compare",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__incident-cluster",
      "description": "Cluster public incidents. Cluster supplied public incidents by offense and area. Allegation or investigation labels are preserved and guilt is not inferred. Docs: https://www.brainiac.software/api/public-records/incident-cluster",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__police-notice-extract",
      "description": "Extract police public notices. Extract structured fields and wording signals from supplied police or public safety notices without inferring guilt. Docs: https://www.brainiac.software/api/public-records/police-notice-extract",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__business-litigation-history",
      "description": "List business litigation history. List supplied court records linked to a business name. Charges and allegations are not treated as convictions. Docs: https://www.brainiac.software/api/public-records/business-litigation-history",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__regulatory-penalty-history",
      "description": "List regulatory penalty history. List supplied penalty and fine actions with amounts when present. Missing amounts are not invented. Docs: https://www.brainiac.software/api/public-records/regulatory-penalty-history",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__investigation-cross-reference",
      "description": "Cross-reference public investigations. Cross-reference subjects across court, enforcement, and notice records while preserving non-judgment statuses and never inferring guilt. Docs: https://www.brainiac.software/api/public-records/investigation-cross-reference",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "public-records__evidence-report",
      "description": "Build public records evidence report. Aggregate court, enforcement, crime-stat, incident, notice, litigation, penalty, and cross-reference findings. Distinguishes allegations, charges, and judgments; never infers guilt. Docs: https://www.brainiac.software/api/public-records/evidence-report",
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
                  "application/xml",
                  "text/xml"
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
          "courtRecords": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "caseNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "court": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "parties": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "disposition": {
                  "type": "string",
                  "maxLength": 200
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "jurisdiction": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementActions": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "subject": {
                  "type": "string",
                  "maxLength": 200
                },
                "businessName": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "penaltyAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "crimeStats": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "count": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "rate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "incidents": {
            "maxItems": 1000,
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
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "offense": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "summary": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "notices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "agency": {
                  "type": "string",
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "area": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "body": {
                  "type": "string",
                  "maxLength": 20000
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "allegation",
                    "investigation",
                    "charge",
                    "judgment",
                    "penalty",
                    "notice",
                    "statistic",
                    "unknown"
                  ]
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "feed": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "businessName": {
            "type": "string",
            "maxLength": 200
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "public-records__court-decision-search-normalize": "0.05",
  "public-records__court-case-timeline-extract": "0.04",
  "public-records__regulatory-enforcement-search": "0.04",
  "public-records__crime-statistics-compare": "0.04",
  "public-records__incident-cluster": "0.04",
  "public-records__police-notice-extract": "0.03",
  "public-records__business-litigation-history": "0.05",
  "public-records__regulatory-penalty-history": "0.04",
  "public-records__investigation-cross-reference": "0.05",
  "public-records__evidence-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "public-records__court-decision-search-normalize": "public-records/court-decision-search-normalize",
  "public-records__court-case-timeline-extract": "public-records/court-case-timeline-extract",
  "public-records__regulatory-enforcement-search": "public-records/regulatory-enforcement-search",
  "public-records__crime-statistics-compare": "public-records/crime-statistics-compare",
  "public-records__incident-cluster": "public-records/incident-cluster",
  "public-records__police-notice-extract": "public-records/police-notice-extract",
  "public-records__business-litigation-history": "public-records/business-litigation-history",
  "public-records__regulatory-penalty-history": "public-records/regulatory-penalty-history",
  "public-records__investigation-cross-reference": "public-records/investigation-cross-reference",
  "public-records__evidence-report": "public-records/evidence-report"
}


class BrainiacPublicRecordsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — public-records",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the public-records catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "public-records", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize court decision records"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the public-records group. "
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
