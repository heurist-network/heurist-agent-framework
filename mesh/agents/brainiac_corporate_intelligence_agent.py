"""Auto-generated BRAINIAC Heurist Mesh agent for group `corporate-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "corporate-intelligence__registry-record-normalize",
      "description": "Normalize corporate registry records. Normalize supplied company registry fields and legal-name tokens. Missing identifiers stay blank rather than invented. Docs: https://www.brainiac.software/api/corporate-intelligence/registry-record-normalize",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__company-identity-cross-check",
      "description": "Cross-check company identity. Compare supplied company records by registry number, LEI, and normalized names. Possible matches are never treated as confirmed. Docs: https://www.brainiac.software/api/corporate-intelligence/company-identity-cross-check",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__director-history",
      "description": "List corporate director history. Group supplied director appointments by company into a chronological history without inventing missing dates. Docs: https://www.brainiac.software/api/corporate-intelligence/director-history",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__company-ownership-chain-map",
      "description": "Map company ownership chains. Walk supplied parent-child ownership edges into chains. Missing ownership percents are labeled, not invented. Docs: https://www.brainiac.software/api/corporate-intelligence/company-ownership-chain-map",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__name-variant-resolve",
      "description": "Resolve corporate name variants. Group legal, trading, and alias names per company. Similar-only variants stay possible and are not confirmed identity matches. Docs: https://www.brainiac.software/api/corporate-intelligence/name-variant-resolve",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__sanctions-list-change-detect",
      "description": "Detect sanctions list changes. Diff current and previous supplied sanctions entries by normalized name. Optional OFAC fetch can populate the current list when requested. Docs: https://www.brainiac.software/api/corporate-intelligence/sanctions-list-change-detect",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__company-enforcement-history",
      "description": "List company enforcement history. Attach supplied enforcement actions to companies. Possible name matches are listed separately and never confirmed. Docs: https://www.brainiac.software/api/corporate-intelligence/company-enforcement-history",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__public-procurement-exclusion-check",
      "description": "Check public procurement exclusions. Compare companies to a supplied procurement exclusion list. Only exact name or registry matches are confirmed exclusions. Docs: https://www.brainiac.software/api/corporate-intelligence/public-procurement-exclusion-check",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__network-relationship-analyze",
      "description": "Analyze corporate network relationships. Build a relationship graph from supplied directors, ownership edges, and explicit relationships. Docs: https://www.brainiac.software/api/corporate-intelligence/network-relationship-analyze",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "corporate-intelligence__investigation-source-citation-package",
      "description": "Build investigation source citation package. Aggregate registry, ownership, sanctions, enforcement, exclusion, and network summaries with source citations. Uncertain matches stay unconfirmed. Docs: https://www.brainiac.software/api/corporate-intelligence/investigation-source-citation-package",
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
          "companies": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "legalName": {
                  "type": "string",
                  "maxLength": 300
                },
                "tradingName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registry": {
                  "type": "string",
                  "maxLength": 120
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "lei": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "address": {
                  "type": "string",
                  "maxLength": 400
                },
                "incorporatedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "directors": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 120
                },
                "appointedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "resignedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentName": {
                  "type": "string",
                  "maxLength": 300
                },
                "childId": {
                  "type": "string",
                  "maxLength": 80
                },
                "childName": {
                  "type": "string",
                  "maxLength": 300
                },
                "percent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "nameVariants": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
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
          "sanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "previousSanctionsEntries": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "list": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 300
                },
                "aliases": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 300
                  }
                },
                "program": {
                  "type": "string",
                  "maxLength": 160
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "listedOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "snapshot": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "enforcementRecords": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyId": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "authority": {
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
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "summary": {
                  "type": "string",
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "exclusions": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "companyName": {
                  "type": "string",
                  "maxLength": 300
                },
                "registryNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "authority": {
                  "type": "string",
                  "maxLength": 200
                },
                "reason": {
                  "type": "string",
                  "maxLength": 400
                },
                "effectiveOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresOn": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "relationships": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromId": {
                  "type": "string",
                  "maxLength": 80
                },
                "fromName": {
                  "type": "string",
                  "maxLength": 300
                },
                "toId": {
                  "type": "string",
                  "maxLength": 80
                },
                "toName": {
                  "type": "string",
                  "maxLength": 300
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "sourceUrl": {
                  "type": "string",
                  "maxLength": 400
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchOfac": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "corporate-intelligence__registry-record-normalize": "0.04",
  "corporate-intelligence__company-identity-cross-check": "0.05",
  "corporate-intelligence__director-history": "0.04",
  "corporate-intelligence__company-ownership-chain-map": "0.05",
  "corporate-intelligence__name-variant-resolve": "0.04",
  "corporate-intelligence__sanctions-list-change-detect": "0.05",
  "corporate-intelligence__company-enforcement-history": "0.05",
  "corporate-intelligence__public-procurement-exclusion-check": "0.04",
  "corporate-intelligence__network-relationship-analyze": "0.05",
  "corporate-intelligence__investigation-source-citation-package": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "corporate-intelligence__registry-record-normalize": "corporate-intelligence/registry-record-normalize",
  "corporate-intelligence__company-identity-cross-check": "corporate-intelligence/company-identity-cross-check",
  "corporate-intelligence__director-history": "corporate-intelligence/director-history",
  "corporate-intelligence__company-ownership-chain-map": "corporate-intelligence/company-ownership-chain-map",
  "corporate-intelligence__name-variant-resolve": "corporate-intelligence/name-variant-resolve",
  "corporate-intelligence__sanctions-list-change-detect": "corporate-intelligence/sanctions-list-change-detect",
  "corporate-intelligence__company-enforcement-history": "corporate-intelligence/company-enforcement-history",
  "corporate-intelligence__public-procurement-exclusion-check": "corporate-intelligence/public-procurement-exclusion-check",
  "corporate-intelligence__network-relationship-analyze": "corporate-intelligence/network-relationship-analyze",
  "corporate-intelligence__investigation-source-citation-package": "corporate-intelligence/investigation-source-citation-package"
}


class BrainiacCorporateIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — corporate-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the corporate-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "corporate-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize corporate registry records"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the corporate-intelligence group. "
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
