"""Auto-generated BRAINIAC Heurist Mesh agent for group `ecommerce-fraud` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "ecommerce-fraud__suspicious-order-detect",
      "description": "Detect suspicious order patterns. Compare supplied amounts with a Tukey fence when 8 orders share a currency, and with a customer's own median when that customer has at least four amounts. A new address counts only after earlier orders. One signal is an indicator, not confirmed fraud. Docs: https://www.brainiac.software/api/ecommerce-fraud/suspicious-order-detect",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__card-testing-pattern-detect",
      "description": "Detect card-testing patterns. Group supplied card fingerprints. Three or more declines on one fingerprint, or three or more cards for one customer, are indicators. A small-amount rule is used only when the caller supplies it. No payment is retried. Docs: https://www.brainiac.software/api/ecommerce-fraud/card-testing-pattern-detect",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__bulk-order-abuse-detect",
      "description": "Detect bulk-order patterns. Flag a shipping address only when it appears on at least three supplied orders. Combined quantity is compared with a caller rule across those orders. One large order is not a bulk pattern. Docs: https://www.brainiac.software/api/ecommerce-fraud/bulk-order-abuse-detect",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__refund-abuse-pattern-detect",
      "description": "Detect refund patterns. Count supplied orders whose status is refunded. A customer needs at least three refunds before a repeat pattern is reported. A single refund is not treated as abuse. Docs: https://www.brainiac.software/api/ecommerce-fraud/refund-abuse-pattern-detect",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__promotion-abuse-detect",
      "description": "Detect promotion patterns. Report a promotion code only when the same customer uses it on at least three supplied orders, or when the same code and address appear for at least two customers. One use is not abuse. Docs: https://www.brainiac.software/api/ecommerce-fraud/promotion-abuse-detect",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__shipping-address-risk-analyze",
      "description": "Analyze shipping-address patterns. Compare supplied shipping addresses across orders. A shared address needs at least three orders and two customers. Several addresses for one customer are a separate indicator. A missing address is not a fraud finding. Docs: https://www.brainiac.software/api/ecommerce-fraud/shipping-address-risk-analyze",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__order-velocity-analyze",
      "description": "Analyze order velocity. Count supplied orders for the same customer, IP, or card. With a minute window and timestamps, the orders must fall inside that window. Otherwise they are compared on the same calendar day. Fewer than three orders is not a pattern. Docs: https://www.brainiac.software/api/ecommerce-fraud/order-velocity-analyze",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-fraud__investigation-report",
      "description": "Report order-risk indicators. Combine supplied amount, card, address, promotion, refund, and velocity patterns. Review means two or more indicators. The report does not confirm fraud, process a payment, or block an order. Docs: https://www.brainiac.software/api/ecommerce-fraud/investigation-report",
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
          "orders": {
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
                "customer": {
                  "type": "string",
                  "maxLength": 160
                },
                "created": {
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
                "status": {
                  "type": "string",
                  "maxLength": 40
                },
                "card": {
                  "type": "string",
                  "maxLength": 40
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "promo": {
                  "type": "string",
                  "maxLength": 40
                },
                "quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "address": {
                  "type": "string",
                  "maxLength": 200
                },
                "country": {
                  "type": "string",
                  "maxLength": 40
                },
                "billCountry": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10080
          },
          "rules": {
            "type": "object",
            "properties": {
              "smallAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "quantity": {
                "type": "integer",
                "minimum": 1,
                "maximum": 1000000
              },
              "orders": {
                "type": "integer",
                "minimum": 3,
                "maximum": 50
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "ecommerce-fraud__suspicious-order-detect": "0.05",
  "ecommerce-fraud__card-testing-pattern-detect": "0.05",
  "ecommerce-fraud__bulk-order-abuse-detect": "0.04",
  "ecommerce-fraud__refund-abuse-pattern-detect": "0.04",
  "ecommerce-fraud__promotion-abuse-detect": "0.04",
  "ecommerce-fraud__shipping-address-risk-analyze": "0.04",
  "ecommerce-fraud__order-velocity-analyze": "0.05",
  "ecommerce-fraud__investigation-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "ecommerce-fraud__suspicious-order-detect": "ecommerce-fraud/suspicious-order-detect",
  "ecommerce-fraud__card-testing-pattern-detect": "ecommerce-fraud/card-testing-pattern-detect",
  "ecommerce-fraud__bulk-order-abuse-detect": "ecommerce-fraud/bulk-order-abuse-detect",
  "ecommerce-fraud__refund-abuse-pattern-detect": "ecommerce-fraud/refund-abuse-pattern-detect",
  "ecommerce-fraud__promotion-abuse-detect": "ecommerce-fraud/promotion-abuse-detect",
  "ecommerce-fraud__shipping-address-risk-analyze": "ecommerce-fraud/shipping-address-risk-analyze",
  "ecommerce-fraud__order-velocity-analyze": "ecommerce-fraud/order-velocity-analyze",
  "ecommerce-fraud__investigation-report": "ecommerce-fraud/investigation-report"
}


class BrainiacEcommerceFraudAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — ecommerce-fraud",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the ecommerce-fraud catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "ecommerce-fraud", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect suspicious order patterns"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the ecommerce-fraud group. "
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
