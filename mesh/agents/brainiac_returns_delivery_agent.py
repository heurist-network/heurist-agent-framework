"""Auto-generated BRAINIAC Heurist Mesh agent for group `returns-delivery` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "returns-delivery__exception-classify",
      "description": "Classify delivery exceptions. Classify a supplied carrier code or order status only when it matches a documented token. Any other code stays unrecognized, and no tracking scan is added. Docs: https://www.brainiac.software/api/returns-delivery/exception-classify",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__failed-pattern-detect",
      "description": "Detect failed-delivery patterns. Group supplied failed, undeliverable, refused, or returned orders by postcode, address, or carrier. A pattern needs at least three orders. One failure is not a carrier finding. Docs: https://www.brainiac.software/api/returns-delivery/failed-pattern-detect",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__shipping-address-validate",
      "description": "Validate shipping-address structure. Check that the supplied lines, city, postcode, and country are present, and compare a postcode with a published shape for nine country codes. The check does not confirm that a carrier can deliver. Docs: https://www.brainiac.software/api/returns-delivery/shipping-address-validate",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__return-shipping-cost-calculate",
      "description": "Calculate return shipping cost. Apply one matching caller-supplied rate to a return. A missing rate is not estimated, currencies are not converted, and the result is not a refund. Docs: https://www.brainiac.software/api/returns-delivery/return-shipping-cost-calculate",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__return-reason-analyze",
      "description": "Analyze return reasons. Count supplied return reasons exactly as written. A reason is a pattern only at three or more returns. The reason text is not rewritten and no refund is granted. Docs: https://www.brainiac.software/api/returns-delivery/return-reason-analyze",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__promise-variance",
      "description": "Calculate delivery-promise variance. Subtract the supplied promise timestamp from the supplied delivery timestamp. A missing timestamp is not filled in, and the comparison is not a carrier guarantee. Docs: https://www.brainiac.software/api/returns-delivery/promise-variance",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__return-window-calculate",
      "description": "Calculate a return window. Add the supplied day count to the supplied delivered or ordered date and compare a return request with that end date. No day count is assumed, and an inside date is not a refund entitlement. Docs: https://www.brainiac.software/api/returns-delivery/return-window-calculate",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
      "name": "returns-delivery__logistics-report",
      "description": "Report returns and delivery logistics. Combine supplied exceptions, failed-order groups, address structure, return rates, promise variance, and the return window. The report does not contact a carrier or grant a refund. Docs: https://www.brainiac.software/api/returns-delivery/logistics-report",
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
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "promised": {
                  "type": "string",
                  "maxLength": 40
                },
                "delivered": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "ordered": {
                  "type": "string",
                  "maxLength": 40
                },
                "windowDays": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 3650
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "addressId": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "addresses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "line1": {
                  "type": "string",
                  "maxLength": 160
                },
                "line2": {
                  "type": "string",
                  "maxLength": 160
                },
                "city": {
                  "type": "string",
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "maxLength": 80
                },
                "postcode": {
                  "type": "string",
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "returns": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "orderId": {
                  "type": "string",
                  "maxLength": 80
                },
                "reason": {
                  "type": "string",
                  "maxLength": 160
                },
                "requested": {
                  "type": "string",
                  "maxLength": 40
                },
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "cost": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "carrier": {
                  "type": "string",
                  "maxLength": 80
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
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
                "basis": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "days": {
                "type": "number",
                "minimum": 0,
                "maximum": 3650
              },
              "from": {
                "type": "string",
                "maxLength": 40
              }
            },
            "additionalProperties": false
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
  "returns-delivery__exception-classify": "0.04",
  "returns-delivery__failed-pattern-detect": "0.05",
  "returns-delivery__shipping-address-validate": "0.04",
  "returns-delivery__return-shipping-cost-calculate": "0.04",
  "returns-delivery__return-reason-analyze": "0.04",
  "returns-delivery__promise-variance": "0.04",
  "returns-delivery__return-window-calculate": "0.04",
  "returns-delivery__logistics-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "returns-delivery__exception-classify": "returns-delivery/exception-classify",
  "returns-delivery__failed-pattern-detect": "returns-delivery/failed-pattern-detect",
  "returns-delivery__shipping-address-validate": "returns-delivery/shipping-address-validate",
  "returns-delivery__return-shipping-cost-calculate": "returns-delivery/return-shipping-cost-calculate",
  "returns-delivery__return-reason-analyze": "returns-delivery/return-reason-analyze",
  "returns-delivery__promise-variance": "returns-delivery/promise-variance",
  "returns-delivery__return-window-calculate": "returns-delivery/return-window-calculate",
  "returns-delivery__logistics-report": "returns-delivery/logistics-report"
}


class BrainiacReturnsDeliveryAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — returns-delivery",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the returns-delivery catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "returns-delivery", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Classify delivery exceptions"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the returns-delivery group. "
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
