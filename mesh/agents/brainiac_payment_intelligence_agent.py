"""Auto-generated BRAINIAC Heurist Mesh agent for group `payment-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "payment-intelligence__open-banking-transaction-classify",
      "description": "Classify open-banking transactions. Classify supplied transactions using description, merchant, category, and amount-sign hints. No bank connection is used. Docs: https://www.brainiac.software/api/payment-intelligence/open-banking-transaction-classify",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__recurring-detect",
      "description": "Detect recurring payments. Detect repeating merchant and amount patterns from supplied transaction dates. Cadence is labeled from spacing only. Docs: https://www.brainiac.software/api/payment-intelligence/recurring-detect",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__subscription-spend-identify",
      "description": "Identify subscription spend. Identify subscription candidates from recurring cadence and subscription wording in supplied merchants or descriptions. Docs: https://www.brainiac.software/api/payment-intelligence/subscription-spend-identify",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__merchant-identity-resolve",
      "description": "Resolve merchant identity. Match transaction merchants against a caller-supplied directory. Unmatched names keep the supplied transaction text. Docs: https://www.brainiac.software/api/payment-intelligence/merchant-identity-resolve",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__income-stability-analyze",
      "description": "Analyze income stability. Summarize labeled income credits by month and report variability from supplied amounts only. Income is never invented. Docs: https://www.brainiac.software/api/payment-intelligence/income-stability-analyze",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__affordability-data-calculate",
      "description": "Calculate affordability data. Calculate inflow, outflow, subscription estimates, and income ratios from supplied transactions. No affordability decision is returned. Docs: https://www.brainiac.software/api/payment-intelligence/affordability-data-calculate",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__failure-pattern-analyze",
      "description": "Analyze payment failure patterns. Find failed, declined, or returned payment wording and statuses in supplied transactions and group counts by merchant text. Docs: https://www.brainiac.software/api/payment-intelligence/failure-pattern-analyze",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__transaction-categorization-correct",
      "description": "Correct transaction categorization. Apply caller-supplied category corrections to matching transaction ids or merchants without inventing categories. Docs: https://www.brainiac.software/api/payment-intelligence/transaction-categorization-correct",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__account-cashflow-compare",
      "description": "Compare account cashflow. Consolidate inflow and outflow by account and compare pairs only when currencies match. Docs: https://www.brainiac.software/api/payment-intelligence/account-cashflow-compare",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "payment-intelligence__iban-validate",
      "description": "Validate an IBAN. Validate IBAN structure and mod-97 checksum using public IBAN Registry lengths, and parse domestic bank/account fields for GB, DE, FR, and NL. Bank legal names are not looked up from a live directory. Docs: https://www.brainiac.software/api/payment-intelligence/iban-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "iban": {
            "type": "string",
            "minLength": 5,
            "maxLength": 42
          }
        },
        "required": [
          "iban"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "payment-intelligence__routing-number-validate",
      "description": "Validate a US ABA routing number. Validate a 9-digit US ABA routing number checksum (weights 3-7-1). Bank directory names are not returned in this version. Docs: https://www.brainiac.software/api/payment-intelligence/routing-number-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "routingNumber": {
            "type": "string",
            "minLength": 8,
            "maxLength": 12
          }
        },
        "required": [
          "routingNumber"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "payment-intelligence__financial-data-quality-audit",
      "description": "Audit financial data quality. Combine classification, recurring spend, merchants, income, failures, corrections, cashflow, and missing-field checks from supplied records. Docs: https://www.brainiac.software/api/payment-intelligence/financial-data-quality-audit",
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
          "accounts": {
            "maxItems": 100,
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
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "type": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "amount": {
                  "type": "number",
                  "minimum": -1000000000,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "description": {
                  "type": "string",
                  "maxLength": 500
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "reference": {
                  "type": "string",
                  "maxLength": 160
                },
                "direction": {
                  "type": "string",
                  "maxLength": 40
                },
                "mcc": {
                  "type": "string",
                  "maxLength": 20
                }
              },
              "additionalProperties": false
            }
          },
          "merchants": {
            "maxItems": 400,
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
                "aliases": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                },
                "category": {
                  "type": "string",
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "corrections": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "transactionId": {
                  "type": "string",
                  "maxLength": 80
                },
                "from": {
                  "type": "string",
                  "maxLength": 120
                },
                "to": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchant": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
  "payment-intelligence__open-banking-transaction-classify": "0.04",
  "payment-intelligence__recurring-detect": "0.05",
  "payment-intelligence__subscription-spend-identify": "0.04",
  "payment-intelligence__merchant-identity-resolve": "0.04",
  "payment-intelligence__income-stability-analyze": "0.05",
  "payment-intelligence__affordability-data-calculate": "0.05",
  "payment-intelligence__failure-pattern-analyze": "0.04",
  "payment-intelligence__transaction-categorization-correct": "0.04",
  "payment-intelligence__account-cashflow-compare": "0.05",
  "payment-intelligence__iban-validate": "0.02",
  "payment-intelligence__routing-number-validate": "0.02",
  "payment-intelligence__financial-data-quality-audit": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "payment-intelligence__open-banking-transaction-classify": "payment-intelligence/open-banking-transaction-classify",
  "payment-intelligence__recurring-detect": "payment-intelligence/recurring-detect",
  "payment-intelligence__subscription-spend-identify": "payment-intelligence/subscription-spend-identify",
  "payment-intelligence__merchant-identity-resolve": "payment-intelligence/merchant-identity-resolve",
  "payment-intelligence__income-stability-analyze": "payment-intelligence/income-stability-analyze",
  "payment-intelligence__affordability-data-calculate": "payment-intelligence/affordability-data-calculate",
  "payment-intelligence__failure-pattern-analyze": "payment-intelligence/failure-pattern-analyze",
  "payment-intelligence__transaction-categorization-correct": "payment-intelligence/transaction-categorization-correct",
  "payment-intelligence__account-cashflow-compare": "payment-intelligence/account-cashflow-compare",
  "payment-intelligence__iban-validate": "payment-intelligence/iban-validate",
  "payment-intelligence__routing-number-validate": "payment-intelligence/routing-number-validate",
  "payment-intelligence__financial-data-quality-audit": "payment-intelligence/financial-data-quality-audit"
}


class BrainiacPaymentIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — payment-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the payment-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "payment-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Classify open-banking transactions"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the payment-intelligence group. "
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
