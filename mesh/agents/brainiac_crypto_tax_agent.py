"""Auto-generated BRAINIAC Heurist Mesh agent for group `crypto-tax` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crypto-tax__cost-basis-lots",
      "description": "Match disposals to acquisition lots. Match disposals to acquisition lots by FIFO, LIFO, HIFO or average cost and compute gains from a caller-supplied ledger and fiat values. No market prices are fetched. Docs: https://www.brainiac.software/api/crypto-tax/cost-basis-lots",
      "parameters": {
        "type": "object",
        "properties": {
          "fiatCurrency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "method": {
            "type": "string",
            "enum": [
              "FIFO",
              "LIFO",
              "HIFO",
              "AVERAGE"
            ]
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          },
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "fiatCurrency",
          "method",
          "ledger"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__specific-id-select",
      "description": "Apply specific-identification lot selections. Apply caller-chosen lot identifications to disposals, validate timing and quantities, and return matched basis or structured selection errors. Docs: https://www.brainiac.software/api/crypto-tax/specific-id-select",
      "parameters": {
        "type": "object",
        "properties": {
          "fiatCurrency": {
            "default": "USD",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          },
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "selections": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "disposalId": {
                  "type": "string",
                  "minLength": 1
                },
                "lots": {
                  "minItems": 1,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "lotId": {
                        "type": "string",
                        "minLength": 1
                      },
                      "qty": {
                        "type": "string",
                        "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                      }
                    },
                    "required": [
                      "lotId",
                      "qty"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "disposalId",
                "lots"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "ledger",
          "selections"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__us-form-8949-rows",
      "description": "Build IRS Form 8949 rows. Produce Form 8949 rows and Schedule D box totals from caller disposals using 2025 short/long-term and 1099-B / 1099-DA box rules. Docs: https://www.brainiac.software/api/crypto-tax/us-form-8949-rows",
      "parameters": {
        "type": "object",
        "properties": {
          "taxYear": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "roundToDollars": {
            "default": false,
            "type": "boolean"
          },
          "disposals": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 256
                },
                "acquired": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "sold": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "proceeds": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "basis": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "adjustmentCode": {
                  "anyOf": [
                    {
                      "type": "string",
                      "maxLength": 8
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "adjustment": {
                  "default": 0,
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "reportedOn": {
                  "type": "string",
                  "enum": [
                    "1099-DA",
                    "1099-B",
                    "none"
                  ]
                },
                "basisReported": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "description",
                "acquired",
                "sold",
                "proceeds",
                "basis",
                "reportedOn",
                "basisReported"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "taxYear",
          "disposals"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__uk-share-pooling",
      "description": "UK share pooling for cryptoassets. Apply same-day, 30-day and section 104 share-pooling rules to a GBP ledger and return allowable cost, gains, pool balances and AEA. Docs: https://www.brainiac.software/api/crypto-tax/uk-share-pooling",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "taxYear": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}$"
          },
          "fiatCurrency": {
            "default": "GBP",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          }
        },
        "required": [
          "ledger",
          "taxYear"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__canada-acb",
      "description": "Canadian adjusted cost base. Compute Canadian ACB and capital gains with superficial-loss detection for identical properties on a CAD ledger. Docs: https://www.brainiac.software/api/crypto-tax/canada-acb",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "treatment": {
            "default": "capital",
            "type": "string",
            "const": "capital"
          },
          "fiatCurrency": {
            "default": "CAD",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          }
        },
        "required": [
          "ledger"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__australia-cgt-discount",
      "description": "Australian CGT discount. Apply the Australian 12-month CGT discount by entity type after losses, from caller event proceeds and cost base. Docs: https://www.brainiac.software/api/crypto-tax/australia-cgt-discount",
      "parameters": {
        "type": "object",
        "properties": {
          "entity": {
            "type": "string",
            "enum": [
              "individual",
              "trust",
              "super_fund",
              "company"
            ]
          },
          "resident": {
            "type": "boolean"
          },
          "events": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "acquired": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "eventDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "capitalProceeds": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "costBase": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "acquired",
                "eventDate",
                "capitalProceeds",
                "costBase"
              ],
              "additionalProperties": false
            }
          },
          "carriedForwardLosses": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "entity",
          "resident",
          "events"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__germany-holding-period",
      "description": "German §23 holding-period screen. Classify crypto private sales under §23 EStG with FIFO (or caller method), one-year holding and the €1,000 Freigrenze. Docs: https://www.brainiac.software/api/crypto-tax/germany-holding-period",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "calendarYear": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "method": {
            "default": "FIFO",
            "type": "string",
            "enum": [
              "FIFO",
              "LIFO",
              "HIFO",
              "AVERAGE"
            ]
          },
          "fiatCurrency": {
            "default": "EUR",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          }
        },
        "required": [
          "ledger",
          "calendarYear"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__income-events-value",
      "description": "Value staking and income events. Value staking, mining, airdrop and interest receipts in fiat using caller-supplied prices within a max lag window. Docs: https://www.brainiac.software/api/crypto-tax/income-events-value",
      "parameters": {
        "type": "object",
        "properties": {
          "events": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "staking",
                    "mining",
                    "airdrop",
                    "interest",
                    "other"
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "asset",
                "qty",
                "kind"
              ],
              "additionalProperties": false
            }
          },
          "prices": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "price": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "asset",
                "ts",
                "price"
              ],
              "additionalProperties": false
            }
          },
          "maxPriceLagHours": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 8760
          },
          "fiatCurrency": {
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          }
        },
        "required": [
          "events",
          "prices",
          "maxPriceLagHours",
          "fiatCurrency"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__transfer-match",
      "description": "Match internal wallet transfers. Pair outgoing and incoming transfers between the caller's own wallets by txHash or amount/time so they are not treated as disposals. Docs: https://www.brainiac.software/api/crypto-tax/transfer-match",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "windowMinutes": {
            "default": 120,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 43200
          },
          "maxFeeRatio": {
            "default": 0.02,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "ledger"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__network-fee-allocate",
      "description": "Allocate network and gas fees. Assign network/gas fees to acquisition basis, disposal proceeds, expense or fee-asset disposal per caller policy. Docs: https://www.brainiac.software/api/crypto-tax/network-fee-allocate",
      "parameters": {
        "type": "object",
        "properties": {
          "fees": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "relatedId": {
                  "type": "string",
                  "minLength": 1
                },
                "context": {
                  "type": "string",
                  "enum": [
                    "disposal",
                    "acquisition",
                    "transfer",
                    "failed_tx"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "relatedId",
                "context",
                "asset",
                "qty",
                "fiatValue"
              ],
              "additionalProperties": false
            }
          },
          "policy": {
            "type": "object",
            "properties": {
              "acquisition": {
                "default": "add_to_basis",
                "type": "string",
                "enum": [
                  "add_to_basis"
                ]
              },
              "disposal": {
                "default": "deduct_from_proceeds",
                "type": "string",
                "enum": [
                  "deduct_from_proceeds"
                ]
              },
              "transfer": {
                "type": "string",
                "enum": [
                  "add_to_basis",
                  "disposal_of_fee_asset",
                  "expense"
                ]
              },
              "failed_tx": {
                "type": "string",
                "enum": [
                  "expense",
                  "ignore"
                ]
              }
            },
            "required": [
              "transfer",
              "failed_tx"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "fees",
          "policy"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__tax-loss-harvest",
      "description": "List tax-loss harvest candidates. List open lots with unrealised losses at caller prices and an estimated tax saving, with US/UK rule flags. Docs: https://www.brainiac.software/api/crypto-tax/tax-loss-harvest",
      "parameters": {
        "type": "object",
        "properties": {
          "openLots": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "lotId": {
                  "type": "string",
                  "minLength": 1
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "basis": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "acquired": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                }
              },
              "required": [
                "lotId",
                "asset",
                "qty",
                "basis",
                "acquired"
              ],
              "additionalProperties": false
            }
          },
          "prices": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "marginalRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "jurisdiction": {
            "type": "string",
            "enum": [
              "US",
              "UK",
              "other"
            ]
          },
          "asOf": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          }
        },
        "required": [
          "openLots",
          "prices",
          "marginalRate",
          "jurisdiction",
          "asOf"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__derivatives-pnl",
      "description": "Derivatives realised P/L. Compute realised P/L for linear perpetuals/futures and options including fees and funding from caller trade inputs. Docs: https://www.brainiac.software/api/crypto-tax/derivatives-pnl",
      "parameters": {
        "type": "object",
        "properties": {
          "trades": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "instrument": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "linear_future",
                    "option"
                  ]
                },
                "side": {
                  "type": "string",
                  "enum": [
                    "long",
                    "short"
                  ]
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "entryPrice": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "exitPrice": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "fees": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "fundingPayments": {
                  "default": [],
                  "maxItems": 10000,
                  "type": "array",
                  "items": {
                    "type": "integer",
                    "minimum": -9007199254740991,
                    "maximum": 9007199254740991
                  }
                },
                "premium": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "settlementValue": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "instrument",
                "kind",
                "side",
                "qty",
                "entryPrice",
                "exitPrice"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "trades"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__unrealized-snapshot",
      "description": "Unrealised holdings snapshot. Replay a ledger to a date with a cost-basis method and report holdings, basis, unrealised gain, dust and unpriced assets at caller prices. Docs: https://www.brainiac.software/api/crypto-tax/unrealized-snapshot",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
          },
          "prices": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "method": {
            "default": "FIFO",
            "type": "string",
            "enum": [
              "FIFO",
              "LIFO",
              "HIFO",
              "AVERAGE"
            ]
          },
          "feePolicy": {
            "default": "add_to_basis_and_deduct_from_proceeds",
            "type": "string",
            "enum": [
              "add_to_basis_and_deduct_from_proceeds",
              "ignore"
            ]
          },
          "dustThresholdFiat": {
            "default": 100,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "fiatCurrency": {
            "default": "USD",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          }
        },
        "required": [
          "ledger",
          "asOf",
          "prices"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__exchange-csv-normalize",
      "description": "Normalize exchange CSV to ledger. Convert a caller CSV export into the shared ledger schema using a caller column mapping, or return a mapping template from headers. Docs: https://www.brainiac.software/api/crypto-tax/exchange-csv-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "maxLength": 10485760
          },
          "mapping": {
            "type": "object",
            "properties": {
              "ts": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "type": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "asset": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "qty": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "fiatValue": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "feeFiat": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "wallet": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "txHash": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "counterAsset": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "counterQty": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              },
              "id": {
                "anyOf": [
                  {
                    "type": "string",
                    "minLength": 1
                  },
                  {
                    "type": "object",
                    "properties": {
                      "column": {
                        "type": "string",
                        "minLength": 1
                      },
                      "format": {
                        "type": "string",
                        "minLength": 1
                      },
                      "timezone": {
                        "type": "string",
                        "minLength": 1
                      },
                      "values": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string"
                        },
                        "additionalProperties": {
                          "type": "string"
                        }
                      },
                      "scale": {
                        "type": "number",
                        "exclusiveMinimum": 0
                      }
                    },
                    "required": [
                      "column"
                    ],
                    "additionalProperties": false
                  }
                ]
              }
            },
            "required": [
              "ts",
              "type",
              "asset",
              "qty",
              "fiatValue"
            ],
            "additionalProperties": false
          },
          "wallet": {
            "default": "exchange",
            "type": "string",
            "minLength": 1,
            "maxLength": 128
          },
          "fiatCurrency": {
            "default": "USD",
            "type": "string",
            "minLength": 3,
            "maxLength": 3
          }
        },
        "required": [
          "csv"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crypto-tax__missing-basis-detect",
      "description": "Detect missing basis problems. Replay balances to find disposal-without-acquisition, negative balance, unmatched transfer-in and unpriced events before gains are computed. Docs: https://www.brainiac.software/api/crypto-tax/missing-basis-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "ledger": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "ts": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "buy",
                    "sell",
                    "transfer_in",
                    "transfer_out",
                    "income",
                    "fee",
                    "trade"
                  ]
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 32
                },
                "qty": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                },
                "fiatValue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "feeFiat": {
                  "default": 0,
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "wallet": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "txHash": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 128
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterAsset": {
                  "anyOf": [
                    {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 32
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "counterQty": {
                  "anyOf": [
                    {
                      "type": "string",
                      "pattern": "^(?:0|[1-9]\\d*)(?:\\.\\d+)?$"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "id",
                "ts",
                "type",
                "asset",
                "qty",
                "fiatValue",
                "wallet"
              ],
              "additionalProperties": false
            }
          },
          "prices": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          }
        },
        "required": [
          "ledger"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "crypto-tax__cost-basis-lots": "0.05",
  "crypto-tax__specific-id-select": "0.05",
  "crypto-tax__us-form-8949-rows": "0.04",
  "crypto-tax__uk-share-pooling": "0.05",
  "crypto-tax__canada-acb": "0.04",
  "crypto-tax__australia-cgt-discount": "0.03",
  "crypto-tax__germany-holding-period": "0.04",
  "crypto-tax__income-events-value": "0.03",
  "crypto-tax__transfer-match": "0.04",
  "crypto-tax__network-fee-allocate": "0.02",
  "crypto-tax__tax-loss-harvest": "0.03",
  "crypto-tax__derivatives-pnl": "0.03",
  "crypto-tax__unrealized-snapshot": "0.04",
  "crypto-tax__exchange-csv-normalize": "0.03",
  "crypto-tax__missing-basis-detect": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "crypto-tax__cost-basis-lots": "crypto-tax/cost-basis-lots",
  "crypto-tax__specific-id-select": "crypto-tax/specific-id-select",
  "crypto-tax__us-form-8949-rows": "crypto-tax/us-form-8949-rows",
  "crypto-tax__uk-share-pooling": "crypto-tax/uk-share-pooling",
  "crypto-tax__canada-acb": "crypto-tax/canada-acb",
  "crypto-tax__australia-cgt-discount": "crypto-tax/australia-cgt-discount",
  "crypto-tax__germany-holding-period": "crypto-tax/germany-holding-period",
  "crypto-tax__income-events-value": "crypto-tax/income-events-value",
  "crypto-tax__transfer-match": "crypto-tax/transfer-match",
  "crypto-tax__network-fee-allocate": "crypto-tax/network-fee-allocate",
  "crypto-tax__tax-loss-harvest": "crypto-tax/tax-loss-harvest",
  "crypto-tax__derivatives-pnl": "crypto-tax/derivatives-pnl",
  "crypto-tax__unrealized-snapshot": "crypto-tax/unrealized-snapshot",
  "crypto-tax__exchange-csv-normalize": "crypto-tax/exchange-csv-normalize",
  "crypto-tax__missing-basis-detect": "crypto-tax/missing-basis-detect"
}


class BrainiacCryptoTaxAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crypto-tax",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crypto-tax catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crypto-tax", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Match disposals to acquisition lots"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crypto-tax group. "
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
