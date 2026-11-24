"""Auto-generated BRAINIAC Heurist Mesh agent for group `freight-customs` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "freight-customs__shipping-document-extract",
      "description": "Extract a shipping document. Read parties, addresses, goods lines, weights, values, and references from supplied shipment text or a text-based PDF. Fields that are not printed are left empty. Docs: https://www.brainiac.software/api/freight-customs/shipping-document-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__commercial-invoice-validate",
      "description": "Validate a commercial invoice. Check that supplied invoice lines, quantities, and amounts agree, and that the seller, buyer, currency, and total are present. No duty is calculated. Docs: https://www.brainiac.software/api/freight-customs/commercial-invoice-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__packing-list-validate",
      "description": "Validate a packing list. Check package counts and net and gross weights on a supplied packing list. A missing weight is not treated as zero. Docs: https://www.brainiac.software/api/freight-customs/packing-list-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__bill-of-lading-extract",
      "description": "Extract a bill of lading. Read the bill of lading number, shipper, consignee, container, and weight from supplied text. No shipment is booked. Docs: https://www.brainiac.software/api/freight-customs/bill-of-lading-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__shipment-document-consistency",
      "description": "Cross-check shipment documents. Compare references, parties, quantities, and weights across at least two supplied documents. A field that appears on only one document is reported separately from a conflict. Docs: https://www.brainiac.software/api/freight-customs/shipment-document-consistency",
      "parameters": {
        "type": "object",
        "properties": {
          "commercialInvoice": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
              }
            },
            "additionalProperties": false
          },
          "packingList": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
              }
            },
            "additionalProperties": false
          },
          "billOfLading": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
      "name": "freight-customs__hs-code-candidate-suggest",
      "description": "Suggest HS code candidates. Search the public UK Trade Tariff for commodity candidates matching a goods description. The result is not a customs classification and does not state a duty. Docs: https://www.brainiac.software/api/freight-customs/hs-code-candidate-suggest",
      "parameters": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "minLength": 2,
            "maxLength": 300
          },
          "hsCode": {
            "type": "string",
            "minLength": 4,
            "maxLength": 14
          }
        },
        "required": [
          "description"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__data-completeness",
      "description": "Check customs data completeness. List shipment fields that are present or missing in the supplied documents. Duty, restrictions, sanctions, and country-specific requirements stay unverified. Docs: https://www.brainiac.software/api/freight-customs/data-completeness",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__shipment-weight-volume-calculate",
      "description": "Calculate shipment weight and volume. Sum supplied package weights and calculate volume from centimetre dimensions. Volumetric weight is calculated only when the request includes a divisor. Docs: https://www.brainiac.software/api/freight-customs/shipment-weight-volume-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "packages": {
            "minItems": 1,
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "count": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100000
                },
                "lengthCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "widthCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "heightCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "netWeightKg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "grossWeightKg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "count"
              ],
              "additionalProperties": false
            }
          },
          "statedNetWeightKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "statedGrossWeightKg": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "statedVolumeM3": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000
          },
          "volumetricDivisor": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 10000
          }
        },
        "required": [
          "packages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__incoterms-obligation-extract",
      "description": "Extract Incoterms obligations. Read a named Incoterms rule and its named place from the request. The obligation text is that named rule. No duty amount is calculated. Docs: https://www.brainiac.software/api/freight-customs/incoterms-obligation-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "incoterm": {
            "type": "string",
            "minLength": 3,
            "maxLength": 80
          },
          "namedPlace": {
            "type": "string",
            "minLength": 1,
            "maxLength": 160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "freight-customs__preparation-report",
      "description": "Prepare a customs evidence report. Combine document checks, weight evidence, the named Incoterm, and UK Trade Tariff candidates. No declaration is submitted and no shipment is booked. Docs: https://www.brainiac.software/api/freight-customs/preparation-report",
      "parameters": {
        "type": "object",
        "properties": {
          "commercialInvoice": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
              }
            },
            "additionalProperties": false
          },
          "packingList": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
              }
            },
            "additionalProperties": false
          },
          "billOfLading": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "shipment": {
                "type": "object",
                "properties": {
                  "reference": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
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
                  "billOfLadingNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  },
                  "containerNumber": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 20
                  },
                  "vessel": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "voyage": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "currency": {
                    "type": "string",
                    "pattern": "^[A-Za-z]{3}$"
                  },
                  "incoterm": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 80
                  },
                  "namedPlace": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 160
                  },
                  "originCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "destinationCountry": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 80
                  },
                  "portOfLoading": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "portOfDischarge": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  },
                  "totalAmount": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000000
                  },
                  "totalNetWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalGrossWeightKg": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000000
                  },
                  "totalVolumeM3": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "totalPackages": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000000
                  },
                  "parties": {
                    "maxItems": 12,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "role": {
                          "type": "string",
                          "enum": [
                            "seller",
                            "exporter",
                            "buyer",
                            "importer",
                            "consignee",
                            "shipper",
                            "notify"
                          ]
                        },
                        "name": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 200
                        },
                        "address": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 400
                        }
                      },
                      "required": [
                        "role",
                        "name"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "lines": {
                    "maxItems": 80,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "description": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 300
                        },
                        "quantity": {
                          "type": "number",
                          "exclusiveMinimum": 0,
                          "maximum": 1000000000
                        },
                        "unit": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 20
                        },
                        "unitPrice": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "amount": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000000
                        },
                        "netWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "grossWeightKg": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000000
                        },
                        "packages": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "volumeM3": {
                          "type": "number",
                          "minimum": 0,
                          "maximum": 1000000
                        },
                        "hsCode": {
                          "type": "string",
                          "minLength": 4,
                          "maxLength": 14
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
              }
            },
            "additionalProperties": false
          },
          "shipment": {
            "type": "object",
            "properties": {
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
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
              "billOfLadingNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "containerNumber": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20
              },
              "vessel": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "voyage": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "incoterm": {
                "type": "string",
                "minLength": 3,
                "maxLength": 80
              },
              "namedPlace": {
                "type": "string",
                "minLength": 1,
                "maxLength": 160
              },
              "originCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "destinationCountry": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "portOfLoading": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "portOfDischarge": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "totalAmount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "totalNetWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalGrossWeightKg": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000
              },
              "totalVolumeM3": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000
              },
              "totalPackages": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000
              },
              "parties": {
                "maxItems": 12,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "role": {
                      "type": "string",
                      "enum": [
                        "seller",
                        "exporter",
                        "buyer",
                        "importer",
                        "consignee",
                        "shipper",
                        "notify"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "address": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 400
                    }
                  },
                  "required": [
                    "role",
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "lines": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "description": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 300
                    },
                    "quantity": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1000000000
                    },
                    "unit": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "unitPrice": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "amount": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000000
                    },
                    "netWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "grossWeightKg": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000000
                    },
                    "packages": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "volumeM3": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "hsCode": {
                      "type": "string",
                      "minLength": 4,
                      "maxLength": 14
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
          "packages": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "count": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100000
                },
                "lengthCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "widthCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "heightCm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 100000
                },
                "netWeightKg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "grossWeightKg": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "count"
              ],
              "additionalProperties": false
            }
          },
          "volumetricDivisor": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 10000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "freight-customs__shipping-document-extract": "0.05",
  "freight-customs__commercial-invoice-validate": "0.05",
  "freight-customs__packing-list-validate": "0.04",
  "freight-customs__bill-of-lading-extract": "0.05",
  "freight-customs__shipment-document-consistency": "0.06",
  "freight-customs__hs-code-candidate-suggest": "0.06",
  "freight-customs__data-completeness": "0.04",
  "freight-customs__shipment-weight-volume-calculate": "0.03",
  "freight-customs__incoterms-obligation-extract": "0.04",
  "freight-customs__preparation-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "freight-customs__shipping-document-extract": "freight-customs/shipping-document-extract",
  "freight-customs__commercial-invoice-validate": "freight-customs/commercial-invoice-validate",
  "freight-customs__packing-list-validate": "freight-customs/packing-list-validate",
  "freight-customs__bill-of-lading-extract": "freight-customs/bill-of-lading-extract",
  "freight-customs__shipment-document-consistency": "freight-customs/shipment-document-consistency",
  "freight-customs__hs-code-candidate-suggest": "freight-customs/hs-code-candidate-suggest",
  "freight-customs__data-completeness": "freight-customs/data-completeness",
  "freight-customs__shipment-weight-volume-calculate": "freight-customs/shipment-weight-volume-calculate",
  "freight-customs__incoterms-obligation-extract": "freight-customs/incoterms-obligation-extract",
  "freight-customs__preparation-report": "freight-customs/preparation-report"
}


class BrainiacFreightCustomsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — freight-customs",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the freight-customs catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "freight-customs", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract a shipping document"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the freight-customs group. "
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
