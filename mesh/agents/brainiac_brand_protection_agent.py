"""Auto-generated BRAINIAC Heurist Mesh agent for group `brand-protection` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "brand-protection__product-listing-match",
      "description": "Match a listing to a supplied brand. Find a supplied brand name only when it is the listing brand field or a whole name in the title, description, or public page title. A partial overlap is not matched, and a name match is not a trademark determination. Docs: https://www.brainiac.software/api/brand-protection/product-listing-match",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__suspected-counterfeit-listing-detect",
      "description": "Detect listing signals against a reference. Compare a listing with one linked reference product and report brand, price, and stated-word differences. A signal is not a finding that the listing is counterfeit. Docs: https://www.brainiac.software/api/brand-protection/suspected-counterfeit-listing-detect",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__product-image-similarity-check",
      "description": "Compare product images. Decode the supplied reference and listing images and compare their pixels. Images that cannot be decoded are not compared, and a visual match is not proof of counterfeiting. Docs: https://www.brainiac.software/api/brand-protection/product-image-similarity-check",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__unauthorized-seller-evidence-extract",
      "description": "Extract seller evidence. Copy the seller, marketplace, source URL, and timestamp from the supplied listing or a public page. A name missing from the supplied list is not a finding that the sale is unauthorized. Docs: https://www.brainiac.software/api/brand-protection/unauthorized-seller-evidence-extract",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__name-usage-audit",
      "description": "Audit brand-name usage. Record each whole supplied brand name in a listing field or public page title. A partial overlap is not counted, and usage is not a trademark determination. Docs: https://www.brainiac.software/api/brand-protection/name-usage-audit",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__marketplace-listing-compare",
      "description": "Compare two listing records. Compare supplied titles, brands, sellers, prices, and decoded images field by field. Different currencies are not converted, and a difference is not a finding that either listing is counterfeit. Docs: https://www.brainiac.software/api/brand-protection/marketplace-listing-compare",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__intellectual-property-evidence-package",
      "description": "Package intellectual-property evidence. Collect the supplied listing, registration text, decoded image hash, source URL, and timestamp, and list the pieces that were not supplied. The package is not a legal conclusion. Docs: https://www.brainiac.software/api/brand-protection/intellectual-property-evidence-package",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
      "name": "brand-protection__investigation-report",
      "description": "Report a brand investigation. Combine the brand match, listing signals, image comparison, seller list, and evidence gaps from the supplied records. The report does not determine infringement or counterfeiting. Docs: https://www.brainiac.software/api/brand-protection/investigation-report",
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
          "brands": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "owner": {
                  "type": "string",
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "products": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "listings": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "seller": {
                  "type": "string",
                  "maxLength": 160
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "sku": {
                  "type": "string",
                  "maxLength": 80
                },
                "imageUrl": {
                  "type": "string",
                  "maxLength": 2000
                },
                "observed": {
                  "type": "string",
                  "maxLength": 40
                },
                "description": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "additionalProperties": false
            }
          },
          "images": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "reference",
                    "listing"
                  ]
                },
                "listingId": {
                  "type": "string",
                  "maxLength": 80
                },
                "productId": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "maxLength": 2200000
                }
              },
              "additionalProperties": false
            }
          },
          "authorizedSellers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "registrations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "office": {
                  "type": "string",
                  "maxLength": 120
                },
                "mark": {
                  "type": "string",
                  "maxLength": 160
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "rules": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "value": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "value"
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
  "brand-protection__product-listing-match": "0.04",
  "brand-protection__suspected-counterfeit-listing-detect": "0.05",
  "brand-protection__product-image-similarity-check": "0.05",
  "brand-protection__unauthorized-seller-evidence-extract": "0.04",
  "brand-protection__name-usage-audit": "0.04",
  "brand-protection__marketplace-listing-compare": "0.05",
  "brand-protection__intellectual-property-evidence-package": "0.05",
  "brand-protection__investigation-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "brand-protection__product-listing-match": "brand-protection/product-listing-match",
  "brand-protection__suspected-counterfeit-listing-detect": "brand-protection/suspected-counterfeit-listing-detect",
  "brand-protection__product-image-similarity-check": "brand-protection/product-image-similarity-check",
  "brand-protection__unauthorized-seller-evidence-extract": "brand-protection/unauthorized-seller-evidence-extract",
  "brand-protection__name-usage-audit": "brand-protection/name-usage-audit",
  "brand-protection__marketplace-listing-compare": "brand-protection/marketplace-listing-compare",
  "brand-protection__intellectual-property-evidence-package": "brand-protection/intellectual-property-evidence-package",
  "brand-protection__investigation-report": "brand-protection/investigation-report"
}


class BrainiacBrandProtectionAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — brand-protection",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the brand-protection catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "brand-protection", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Match a listing to a supplied brand"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the brand-protection group. "
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
