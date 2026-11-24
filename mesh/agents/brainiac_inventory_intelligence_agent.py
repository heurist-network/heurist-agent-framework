"""Auto-generated BRAINIAC Heurist Mesh agent for group `inventory-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "inventory-intelligence__data-normalize",
      "description": "Normalize inventory data. Copy supplied products, sales, supplier lead times, and purchases into a consistent inventory packet. Missing lead times and prices are not invented. Docs: https://www.brainiac.software/api/inventory-intelligence/data-normalize",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__stockout-risk-calculate",
      "description": "Calculate stockout risk. Compare available stock with the calculated reorder point from supplied demand and lead times. Risk is not calculated when lead time or demand history is missing. Docs: https://www.brainiac.software/api/inventory-intelligence/stockout-risk-calculate",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__reorder-point-calculate",
      "description": "Calculate reorder points. Calculate reorderPoint = averageDailyDemand × (leadTimeDays + reviewDays) + safetyStock from supplied history and lead times. No purchase order is created. Docs: https://www.brainiac.software/api/inventory-intelligence/reorder-point-calculate",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__safety-stock-calculate",
      "description": "Calculate safety stock. Calculate safetyStock = serviceLevelZ × demandStdev × sqrt(leadTimeDays). Short history raises disclosed uncertainty. Seasonality is not invented. Docs: https://www.brainiac.software/api/inventory-intelligence/safety-stock-calculate",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__excess-detect",
      "description": "Detect excess inventory. Flag SKUs whose days of cover from supplied on-hand and average daily demand exceed the disclosed excessDaysCover threshold. Docs: https://www.brainiac.software/api/inventory-intelligence/excess-detect",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__slow-moving-stock-detect",
      "description": "Detect slow-moving stock. Flag SKUs whose supplied unit sales over the disclosed lookback are at or below the slowUnits threshold. Docs: https://www.brainiac.software/api/inventory-intelligence/slow-moving-stock-detect",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__demand-forecast",
      "description": "Forecast inventory demand. Forecast units as averageDailyDemand × forecastDays from available dated sales only. Seasonality is not modeled and uncertainty is disclosed. Docs: https://www.brainiac.software/api/inventory-intelligence/demand-forecast",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "inventory-intelligence__optimization-report",
      "description": "Report inventory optimization. Combine stockout risk, reorder points, safety stock, excess, slow-moving stock, and demand forecasts from supplied data. No purchase order is created. Docs: https://www.brainiac.software/api/inventory-intelligence/optimization-report",
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
          "products": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "onHand": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "onOrder": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitCost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "suppliers": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "leadTimeDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "moq": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "purchases": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "serviceLevelZ": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
          },
          "reviewDays": {
            "type": "number",
            "minimum": 0,
            "maximum": 365
          },
          "excessDaysCover": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "slowUnits": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "slowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 3650
          },
          "forecastDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 365
          },
          "historyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "inventory-intelligence__data-normalize": "0.04",
  "inventory-intelligence__stockout-risk-calculate": "0.05",
  "inventory-intelligence__reorder-point-calculate": "0.05",
  "inventory-intelligence__safety-stock-calculate": "0.05",
  "inventory-intelligence__excess-detect": "0.04",
  "inventory-intelligence__slow-moving-stock-detect": "0.04",
  "inventory-intelligence__demand-forecast": "0.05",
  "inventory-intelligence__optimization-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "inventory-intelligence__data-normalize": "inventory-intelligence/data-normalize",
  "inventory-intelligence__stockout-risk-calculate": "inventory-intelligence/stockout-risk-calculate",
  "inventory-intelligence__reorder-point-calculate": "inventory-intelligence/reorder-point-calculate",
  "inventory-intelligence__safety-stock-calculate": "inventory-intelligence/safety-stock-calculate",
  "inventory-intelligence__excess-detect": "inventory-intelligence/excess-detect",
  "inventory-intelligence__slow-moving-stock-detect": "inventory-intelligence/slow-moving-stock-detect",
  "inventory-intelligence__demand-forecast": "inventory-intelligence/demand-forecast",
  "inventory-intelligence__optimization-report": "inventory-intelligence/optimization-report"
}


class BrainiacInventoryIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — inventory-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the inventory-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "inventory-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize inventory data"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the inventory-intelligence group. "
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
