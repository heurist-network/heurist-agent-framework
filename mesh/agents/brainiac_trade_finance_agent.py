"""Auto-generated BRAINIAC Heurist Mesh agent for group `trade-finance` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "trade-finance__document-match",
      "description": "Match trade finance documents. Match supplied invoices to contracts, letters of credit, and trade documents by id, amount, and parties without inventing missing links. Docs: https://www.brainiac.software/api/trade-finance/document-match",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__letter-of-credit-discrepancy-detect",
      "description": "Detect letter of credit discrepancies. Compare supplied LC terms with linked invoices and documents. Missing required document types are flagged only from the LC list. Docs: https://www.brainiac.software/api/trade-finance/letter-of-credit-discrepancy-detect",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__invoice-financing-readiness",
      "description": "Assess invoice financing readiness. Score supplied invoices for completeness of identifiers, amounts, parties, and dates. This is not a financing approval. Docs: https://www.brainiac.software/api/trade-finance/invoice-financing-readiness",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__receivable-aging-risk-analyze",
      "description": "Analyze receivable aging risk. Bucket supplied invoice outstanding amounts by days past due from the as-of date. Missing due dates stay unlabeled. Docs: https://www.brainiac.software/api/trade-finance/receivable-aging-risk-analyze",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__invoice-assignment-conflict-detect",
      "description": "Detect invoice assignment conflicts. Flag when the same invoice id or number is assigned to more than one assignee in the supplied set. Docs: https://www.brainiac.software/api/trade-finance/invoice-assignment-conflict-detect",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__document-party-consistency",
      "description": "Check trade document party consistency. Compare buyer, seller, applicant, beneficiary, shipper, and consignee fields across linked invoices, contracts, LCs, and documents. Docs: https://www.brainiac.software/api/trade-finance/document-party-consistency",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__export-payment-term-risk",
      "description": "Assess export payment term risk. Label supplied payment terms as lower, moderate, higher, or unclassified from wording only. Not a credit decision. Docs: https://www.brainiac.software/api/trade-finance/export-payment-term-risk",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__credit-exposure-calculate",
      "description": "Calculate trade credit exposure. Sum supplied outstanding or face amounts by buyer and currency. Missing amounts are not invented. Docs: https://www.brainiac.software/api/trade-finance/credit-exposure-calculate",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__invoice-discounting-calculate",
      "description": "Calculate invoice discounting. Calculate simple discount and proceeds from supplied face amounts, due dates, as-of date, and discount rate. Not a financing approval. Docs: https://www.brainiac.software/api/trade-finance/invoice-discounting-calculate",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "trade-finance__evidence-package",
      "description": "Build trade finance evidence package. Assemble document match, LC discrepancy, readiness, aging, assignment, party, term, exposure, and discounting summaries from the supplied set. Docs: https://www.brainiac.software/api/trade-finance/evidence-package",
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
          "parties": {
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
                  "maxLength": 200
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "dueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "outstanding": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "contracts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "buyer": {
                  "type": "string",
                  "maxLength": 200
                },
                "seller": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "paymentTerms": {
                  "type": "string",
                  "maxLength": 200
                },
                "incoterm": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "lettersOfCredit": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "issueDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiryDate": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "applicant": {
                  "type": "string",
                  "maxLength": 200
                },
                "beneficiary": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "latestShipment": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiredDocs": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 120
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "documents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "number": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "shipper": {
                  "type": "string",
                  "maxLength": 200
                },
                "consignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "goods": {
                  "type": "string",
                  "maxLength": 400
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "lcId": {
                  "type": "string",
                  "maxLength": 80
                },
                "contractId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 80
                },
                "assignee": {
                  "type": "string",
                  "maxLength": 200
                },
                "assignor": {
                  "type": "string",
                  "maxLength": 200
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
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
                "source": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "worldBank": {
            "type": "object",
            "properties": {
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 3
              },
              "indicator": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "perPage": {
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
          "discountRatePct": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "trade-finance__document-match": "0.05",
  "trade-finance__letter-of-credit-discrepancy-detect": "0.06",
  "trade-finance__invoice-financing-readiness": "0.04",
  "trade-finance__receivable-aging-risk-analyze": "0.04",
  "trade-finance__invoice-assignment-conflict-detect": "0.04",
  "trade-finance__document-party-consistency": "0.04",
  "trade-finance__export-payment-term-risk": "0.03",
  "trade-finance__credit-exposure-calculate": "0.04",
  "trade-finance__invoice-discounting-calculate": "0.04",
  "trade-finance__evidence-package": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "trade-finance__document-match": "trade-finance/document-match",
  "trade-finance__letter-of-credit-discrepancy-detect": "trade-finance/letter-of-credit-discrepancy-detect",
  "trade-finance__invoice-financing-readiness": "trade-finance/invoice-financing-readiness",
  "trade-finance__receivable-aging-risk-analyze": "trade-finance/receivable-aging-risk-analyze",
  "trade-finance__invoice-assignment-conflict-detect": "trade-finance/invoice-assignment-conflict-detect",
  "trade-finance__document-party-consistency": "trade-finance/document-party-consistency",
  "trade-finance__export-payment-term-risk": "trade-finance/export-payment-term-risk",
  "trade-finance__credit-exposure-calculate": "trade-finance/credit-exposure-calculate",
  "trade-finance__invoice-discounting-calculate": "trade-finance/invoice-discounting-calculate",
  "trade-finance__evidence-package": "trade-finance/evidence-package"
}


class BrainiacTradeFinanceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — trade-finance",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the trade-finance catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "trade-finance", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Match trade finance documents"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the trade-finance group. "
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
