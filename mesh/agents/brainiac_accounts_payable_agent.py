"""Auto-generated BRAINIAC Heurist Mesh agent for group `accounts-payable` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "accounts-payable__invoice-data-extract",
      "description": "Extract invoice data. Extract supplier, invoice number, dates, currency, purchase-order number, terms, and amounts from a supplied invoice or a text-based PDF. Missing fields stay unavailable. No tax rule or payment term is invented. Docs: https://www.brainiac.software/api/accounts-payable/invoice-data-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__invoice-line-item-extract",
      "description": "Extract invoice line items. Extract invoice line descriptions, quantities, unit prices, and amounts from supplied lines or selectable document text. Lines that are not present are not created. Docs: https://www.brainiac.software/api/accounts-payable/invoice-line-item-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__invoice-total-validate",
      "description": "Validate invoice totals. Recompute the total from line amounts, subtotal, tax, discount, and shipping figures that are actually present. A missing figure is not treated as zero. Docs: https://www.brainiac.software/api/accounts-payable/invoice-total-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__invoice-duplicate-detect",
      "description": "Detect duplicate invoices. Compare one invoice with other invoices supplied in the same request using the supplier and invoice number, and a content fingerprint. This does not search an accounts payable ledger. Docs: https://www.brainiac.software/api/accounts-payable/invoice-duplicate-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          "candidates": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "supplierName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "invoiceNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "invoiceDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "dueDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "poNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "paymentTerms": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "subtotal": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "discount": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "shipping": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "tax": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "taxRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "total": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "lines": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "description": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 300
                      },
                      "sku": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "quantity": {
                        "type": "number",
                        "minimum": -1000000000,
                        "maximum": 1000000000
                      },
                      "unitPrice": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      },
                      "amount": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      },
                      "tax": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      }
                    },
                    "required": [
                      "description"
                    ],
                    "additionalProperties": false
                  }
                },
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__purchase-order-match",
      "description": "Match an invoice to a purchase order. Match the invoice to a purchase order supplied in the request. Purchase orders are not looked up or created. Lines match on SKU when both sides have one, otherwise on the same description. Docs: https://www.brainiac.software/api/accounts-payable/purchase-order-match",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          "purchaseOrder": {
            "type": "object",
            "properties": {
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "poNumber"
            ],
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
      "name": "accounts-payable__invoice-tax-validate",
      "description": "Validate invoice tax. Check a printed or supplied tax amount against a printed or supplied rate and subtotal. No statutory tax rate is applied. Docs: https://www.brainiac.software/api/accounts-payable/invoice-tax-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__payment-terms-extract",
      "description": "Extract payment terms. Read payment terms only when they are supplied or printed, including Net N, due on receipt, and a stated discount such as 2/10 Net 30. Docs: https://www.brainiac.software/api/accounts-payable/payment-terms-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__payment-due-date-calculate",
      "description": "Calculate a payment due date. Return a stated due date, or calculate one from an invoice date plus terms that were actually stated. Net 30 is not assumed, and no payment is scheduled. Docs: https://www.brainiac.software/api/accounts-payable/payment-due-date-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__invoice-anomaly-detect",
      "description": "Detect invoice anomalies. Flag amount mismatches, negative figures, date-order problems, and repeated lines that are present on the invoice. Unusual amounts are not guessed from a normal range. Docs: https://www.brainiac.software/api/accounts-payable/invoice-anomaly-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accounts-payable__review",
      "description": "Review an invoice for payment. Combine the invoice checks into one review. No payment is initiated, and a clear review is not an approval to pay. Docs: https://www.brainiac.software/api/accounts-payable/review",
      "parameters": {
        "type": "object",
        "properties": {
          "invoice": {
            "type": "object",
            "properties": {
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "invoiceNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "invoiceDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "dueDate": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "paymentTerms": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "subtotal": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "discount": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "shipping": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "tax": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "taxRate": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
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
                  "application/pdf",
                  "text/plain",
                  "text/csv"
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
          "purchaseOrder": {
            "type": "object",
            "properties": {
              "poNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "supplierName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "total": {
                "type": "number",
                "minimum": -1000000000000,
                "maximum": 1000000000000
              },
              "lines": {
                "maxItems": 200,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "sku": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "quantity": {
                      "type": "number",
                      "minimum": -1000000000,
                      "maximum": 1000000000
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    },
                    "tax": {
                      "type": "number",
                      "minimum": -1000000000000,
                      "maximum": 1000000000000
                    }
                  },
                  "required": [
                    "description"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "poNumber"
            ],
            "additionalProperties": false
          },
          "candidates": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "supplierName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "invoiceNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "invoiceDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "dueDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "poNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "paymentTerms": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "subtotal": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "discount": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "shipping": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "tax": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "taxRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "total": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "lines": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "description": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 300
                      },
                      "sku": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "quantity": {
                        "type": "number",
                        "minimum": -1000000000,
                        "maximum": 1000000000
                      },
                      "unitPrice": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      },
                      "amount": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      },
                      "tax": {
                        "type": "number",
                        "minimum": -1000000000000,
                        "maximum": 1000000000000
                      }
                    },
                    "required": [
                      "description"
                    ],
                    "additionalProperties": false
                  }
                },
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "accounts-payable__invoice-data-extract": "0.06",
  "accounts-payable__invoice-line-item-extract": "0.06",
  "accounts-payable__invoice-total-validate": "0.04",
  "accounts-payable__invoice-duplicate-detect": "0.05",
  "accounts-payable__purchase-order-match": "0.06",
  "accounts-payable__invoice-tax-validate": "0.04",
  "accounts-payable__payment-terms-extract": "0.03",
  "accounts-payable__payment-due-date-calculate": "0.03",
  "accounts-payable__invoice-anomaly-detect": "0.05",
  "accounts-payable__review": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "accounts-payable__invoice-data-extract": "accounts-payable/invoice-data-extract",
  "accounts-payable__invoice-line-item-extract": "accounts-payable/invoice-line-item-extract",
  "accounts-payable__invoice-total-validate": "accounts-payable/invoice-total-validate",
  "accounts-payable__invoice-duplicate-detect": "accounts-payable/invoice-duplicate-detect",
  "accounts-payable__purchase-order-match": "accounts-payable/purchase-order-match",
  "accounts-payable__invoice-tax-validate": "accounts-payable/invoice-tax-validate",
  "accounts-payable__payment-terms-extract": "accounts-payable/payment-terms-extract",
  "accounts-payable__payment-due-date-calculate": "accounts-payable/payment-due-date-calculate",
  "accounts-payable__invoice-anomaly-detect": "accounts-payable/invoice-anomaly-detect",
  "accounts-payable__review": "accounts-payable/review"
}


class BrainiacAccountsPayableAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — accounts-payable",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the accounts-payable catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "accounts-payable", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract invoice data"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the accounts-payable group. "
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
