"""Auto-generated BRAINIAC Heurist Mesh agent for group `ecommerce-catalog` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "ecommerce-catalog__product-normalize",
      "description": "Normalize product records. Read a brainiac-catalog-v1 or Google Merchant subset feed and standardize sku, title, category, price, availability, and GTIN. A dollar sign is not treated as USD, and missing materials or dimensions are not filled in. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-catalog__product-attribute-extract",
      "description": "Extract product attributes. Read structured attribute pairs and lines labeled Attribute: name | value. Unlabeled description prose is not turned into a specification. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-attribute-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-catalog__product-variant-validate",
      "description": "Validate product variants. Group products by the supplied parent sku and flag repeated color and size pairs, price disagreements, and parents that are not in the request. Missing options are not invented. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-variant-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-catalog__product-description-quality-check",
      "description": "Check product description quality. Flag missing, placeholder, HTML, and very short descriptions. When minLength is omitted, descriptions shorter than 40 characters are flagged. No description text is generated. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-description-quality-check",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          "minLength": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5000
          },
          "maxTitleLength": {
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-catalog__product-category-classify",
      "description": "Classify product categories. Match a supplied category to the caller taxonomy, or mark one keyword match as inferred. Several matches are a conflict, and no category is chosen or invented. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-category-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          "taxonomy": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "terms": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "category"
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
      "name": "ecommerce-catalog__product-feed-validate",
      "description": "Validate a product feed. Check brainiac-catalog-v1 or the documented Google Merchant subset, plus any required fields and types in the caller schema. Unknown columns are ignored. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-feed-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          "schema": {
            "type": "object",
            "properties": {
              "format": {
                "type": "string",
                "enum": [
                  "brainiac-catalog-v1",
                  "google-merchant-subset"
                ]
              },
              "required": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "fields": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "url",
                        "gtin",
                        "currency",
                        "identifier"
                      ]
                    }
                  },
                  "required": [
                    "name",
                    "type"
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
      "name": "ecommerce-catalog__product-image-metadata-audit",
      "description": "Audit product image metadata. Check supplied image URLs, alt text, filename extensions, and supplied pixel sizes. Image files are not downloaded and alt text is not generated. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-image-metadata-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ecommerce-catalog__product-health-report",
      "description": "Report product catalog health. Combine the normalize, attribute, variant, description, category, feed, and image checks. The report does not approve the catalog for a sales channel. Docs: https://www.brainiac.software/api/ecommerce-catalog/product-health-report",
      "parameters": {
        "type": "object",
        "properties": {
          "products": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "googleProductCategory": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12
                },
                "availability": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "condition": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "gtin": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "mpn": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "parentSku": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "color": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "size": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "material": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "certification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "link": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "imageUrl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "additionalImageUrls": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000
                  }
                },
                "imageAlt": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "imageWidth": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "imageHeight": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 20000
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "weightUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "length": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "width": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "height": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dimensionUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "attributes": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 500
                      }
                    },
                    "required": [
                      "name",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                },
                "attributesText": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
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
                  "text/csv",
                  "application/json",
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
          "minLength": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5000
          },
          "maxTitleLength": {
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          },
          "taxonomy": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "terms": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "category"
              ],
              "additionalProperties": false
            }
          },
          "schema": {
            "type": "object",
            "properties": {
              "format": {
                "type": "string",
                "enum": [
                  "brainiac-catalog-v1",
                  "google-merchant-subset"
                ]
              },
              "required": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "fields": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "url",
                        "gtin",
                        "currency",
                        "identifier"
                      ]
                    }
                  },
                  "required": [
                    "name",
                    "type"
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "ecommerce-catalog__product-normalize": "0.04",
  "ecommerce-catalog__product-attribute-extract": "0.03",
  "ecommerce-catalog__product-variant-validate": "0.04",
  "ecommerce-catalog__product-description-quality-check": "0.03",
  "ecommerce-catalog__product-category-classify": "0.04",
  "ecommerce-catalog__product-feed-validate": "0.05",
  "ecommerce-catalog__product-image-metadata-audit": "0.03",
  "ecommerce-catalog__product-health-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "ecommerce-catalog__product-normalize": "ecommerce-catalog/product-normalize",
  "ecommerce-catalog__product-attribute-extract": "ecommerce-catalog/product-attribute-extract",
  "ecommerce-catalog__product-variant-validate": "ecommerce-catalog/product-variant-validate",
  "ecommerce-catalog__product-description-quality-check": "ecommerce-catalog/product-description-quality-check",
  "ecommerce-catalog__product-category-classify": "ecommerce-catalog/product-category-classify",
  "ecommerce-catalog__product-feed-validate": "ecommerce-catalog/product-feed-validate",
  "ecommerce-catalog__product-image-metadata-audit": "ecommerce-catalog/product-image-metadata-audit",
  "ecommerce-catalog__product-health-report": "ecommerce-catalog/product-health-report"
}


class BrainiacEcommerceCatalogAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — ecommerce-catalog",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the ecommerce-catalog catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "ecommerce-catalog", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize product records"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the ecommerce-catalog group. "
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
