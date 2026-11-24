"""Auto-generated BRAINIAC Heurist Mesh agent for group `restaurant-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "restaurant-operations__recipe-cost-calculate",
      "description": "Calculate recipe cost. Calculate recipe and per-portion cost from supplied ingredient quantities and prices after unit conversion. Missing prices are not invented. Docs: https://www.brainiac.software/api/restaurant-operations/recipe-cost-calculate",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__menu-item-margin-analyze",
      "description": "Analyze menu item margins. Calculate gross margin and food-cost percentage from supplied sell prices and calculated recipe costs. Nutritional values are not invented. Docs: https://www.brainiac.software/api/restaurant-operations/menu-item-margin-analyze",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__ingredient-price-variance",
      "description": "Detect ingredient price variance. Compare supplied supplier prices for the same ingredient after unit conversion and report spreads and dated changes. Prices are never invented. Docs: https://www.brainiac.software/api/restaurant-operations/ingredient-price-variance",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__food-waste-estimate",
      "description": "Estimate food waste cost. Estimate waste cost from supplied waste quantities and ingredient prices after unit conversion. Missing prices are not invented. Docs: https://www.brainiac.software/api/restaurant-operations/food-waste-estimate",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__recipe-yield-normalize",
      "description": "Normalize recipe yields. Normalize recipe line quantities into ingredient units and per-portion amounts using accurate mass and volume conversions. Docs: https://www.brainiac.software/api/restaurant-operations/recipe-yield-normalize",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__menu-profitability-rank",
      "description": "Rank menu profitability. Rank menu items by contribution using calculated portion profit and supplied sales units. Ties fall back to gross margin. Docs: https://www.brainiac.software/api/restaurant-operations/menu-profitability-rank",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__allergen-matrix-validate",
      "description": "Validate allergen matrix. Compare menu allergen claims with explicitly supplied ingredient allergen flags. Allergen status is never invented and food-safety compliance is not claimed. Docs: https://www.brainiac.software/api/restaurant-operations/allergen-matrix-validate",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
      "name": "restaurant-operations__food-cost-report",
      "description": "Report restaurant food cost. Combine recipe costs, margins, price variance, waste estimates, yield normalization, profitability ranking, and allergen validation from supplied data. Docs: https://www.brainiac.software/api/restaurant-operations/food-cost-report",
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
          "ingredients": {
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
                  "maxLength": 160
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
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
          "prices": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 80
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "unitPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packSize": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "packPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "asOf": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "recipes": {
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
                  "maxLength": 160
                },
                "yieldQty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "yieldUnit": {
                  "type": "string",
                  "maxLength": 40
                },
                "portions": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "sellPrice": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "recipeLines": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "sales": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "units": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "revenue": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "waste": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "unit": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "additionalProperties": false
            }
          },
          "allergens": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ingredientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "present": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "matrix": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "recipeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "allergen": {
                  "type": "string",
                  "maxLength": 80
                },
                "claimed": {
                  "type": "boolean"
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
  "restaurant-operations__recipe-cost-calculate": "0.04",
  "restaurant-operations__menu-item-margin-analyze": "0.05",
  "restaurant-operations__ingredient-price-variance": "0.04",
  "restaurant-operations__food-waste-estimate": "0.04",
  "restaurant-operations__recipe-yield-normalize": "0.04",
  "restaurant-operations__menu-profitability-rank": "0.05",
  "restaurant-operations__allergen-matrix-validate": "0.05",
  "restaurant-operations__food-cost-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "restaurant-operations__recipe-cost-calculate": "restaurant-operations/recipe-cost-calculate",
  "restaurant-operations__menu-item-margin-analyze": "restaurant-operations/menu-item-margin-analyze",
  "restaurant-operations__ingredient-price-variance": "restaurant-operations/ingredient-price-variance",
  "restaurant-operations__food-waste-estimate": "restaurant-operations/food-waste-estimate",
  "restaurant-operations__recipe-yield-normalize": "restaurant-operations/recipe-yield-normalize",
  "restaurant-operations__menu-profitability-rank": "restaurant-operations/menu-profitability-rank",
  "restaurant-operations__allergen-matrix-validate": "restaurant-operations/allergen-matrix-validate",
  "restaurant-operations__food-cost-report": "restaurant-operations/food-cost-report"
}


class BrainiacRestaurantOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — restaurant-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the restaurant-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "restaurant-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Calculate recipe cost"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the restaurant-operations group. "
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
