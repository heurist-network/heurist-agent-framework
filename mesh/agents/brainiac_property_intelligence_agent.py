"""Auto-generated BRAINIAC Heurist Mesh agent for group `property-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "property-intelligence__overview",
      "description": "Property overview. Retrieve available planning and heritage information for a property using UPRN, coordinates, or postcode. Docs: https://www.brainiac.software/api/property-intelligence/overview",
      "parameters": {
        "type": "object",
        "properties": {
          "uprn": {
            "type": "string"
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "postcode": {
            "type": "string"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__constraints__check",
      "description": "Check planning constraints. Check specific planning constraints (conservation areas, listed buildings, flood risk, etc.) for a location. Docs: https://www.brainiac.software/api/property-intelligence/constraints-check",
      "parameters": {
        "type": "object",
        "properties": {
          "uprn": {
            "type": "string"
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "datasets": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "conservation-area",
                "listed-building",
                "green-belt",
                "flood-risk-zone",
                "article-4-direction-area",
                "tree-preservation-zone",
                "scheduled-monument",
                "site-of-special-scientific-interest",
                "ancient-woodland",
                "heritage-at-risk",
                "area-of-outstanding-natural-beauty"
              ]
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
      "name": "property-intelligence__planning__search",
      "description": "Search planning applications. Search planning applications by local planning authority, date range, or other filters. Docs: https://www.brainiac.software/api/property-intelligence/planning-search",
      "parameters": {
        "type": "object",
        "properties": {
          "localPlanningAuthority": {
            "type": "string"
          },
          "startDateYear": {
            "type": "integer",
            "minimum": 2000,
            "maximum": 2100
          },
          "startDateMonth": {
            "type": "integer",
            "minimum": 1,
            "maximum": 12
          },
          "startDateDay": {
            "type": "integer",
            "minimum": 1,
            "maximum": 31
          },
          "startDateMatch": {
            "type": "string",
            "enum": [
              "since",
              "on",
              "before"
            ]
          },
          "limit": {
            "default": 50,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "offset": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__site__report",
      "description": "Generate site report. Generate a comprehensive site report combining constraints, brownfield land, and planning applications. Docs: https://www.brainiac.software/api/property-intelligence/site-report",
      "parameters": {
        "type": "object",
        "properties": {
          "uprn": {
            "type": "string"
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "postcode": {
            "type": "string"
          },
          "includeBrownfield": {
            "default": true,
            "type": "boolean"
          },
          "includePlanningApplications": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__listing-extract",
      "description": "Extract a listing. Read price, rent, address, and room counts from caller-supplied listing text or one public listing page. Missing figures stay blank. Docs: https://www.brainiac.software/api/property-intelligence/listing-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "price": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "rent": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "rentPeriod": {
            "type": "string",
            "enum": [
              "month",
              "year"
            ]
          },
          "bedrooms": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "bathrooms": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "floorAreaSqm": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000
          },
          "propertyType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "annualCosts": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "deposit": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "mortgageRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__details-normalize",
      "description": "Normalize listing details. Return one listing record from supplied fields or printed text. A supplied value is kept when it conflicts with the printed value. Docs: https://www.brainiac.software/api/property-intelligence/details-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "price": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "rent": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "rentPeriod": {
            "type": "string",
            "enum": [
              "month",
              "year"
            ]
          },
          "bedrooms": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "bathrooms": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "floorAreaSqm": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000
          },
          "propertyType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "annualCosts": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "deposit": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "mortgageRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__description-analyze",
      "description": "Analyze a listing description. List bedrooms, area, amenities, and marketing phrases only where those words are printed. Marketing words are not a quality score. Docs: https://www.brainiac.software/api/property-intelligence/description-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
      "name": "property-intelligence__area-context",
      "description": "Read area context. Look up the OpenStreetMap place for a supplied address or coordinates. Planning, crime, ownership, and valuation stay unavailable. Docs: https://www.brainiac.software/api/property-intelligence/area-context",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__location-features",
      "description": "List nearby location features. List schools, hospitals, pharmacies, supermarkets, stations, and parks that OpenStreetMap places within 500 metres. A missing feature is not treated as absent. Docs: https://www.brainiac.software/api/property-intelligence/location-features",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__amenities-extract",
      "description": "Extract amenities. Keep amenities printed in the description separate from amenities copied from the request. Caller amenities are not checked against the property. Docs: https://www.brainiac.software/api/property-intelligence/amenities-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "amenities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
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
      "name": "property-intelligence__listing-duplicate-detect",
      "description": "Detect duplicate listings. Compare at least two supplied listings. The same address is a duplicate. The same price, currency, and bedroom count is only a possible match. Docs: https://www.brainiac.software/api/property-intelligence/listing-duplicate-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "listings": {
            "minItems": 2,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 2000,
                  "pattern": "^https?:\\/\\/\\S+$"
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "address": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "rent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "rentPeriod": {
                  "type": "string",
                  "enum": [
                    "month",
                    "year"
                  ]
                },
                "bedrooms": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100
                },
                "bathrooms": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "floorAreaSqm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 1000000
                },
                "propertyType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "annualCosts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "deposit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "mortgageRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "additionalProperties": false
            }
          }
        },
        "required": [
          "listings"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__rent-yield-calculate",
      "description": "Calculate rent yield. Divide the supplied annual rent by the supplied price. Monthly rent is multiplied by 12 only when the period is month. The result is not a valuation. Docs: https://www.brainiac.software/api/property-intelligence/rent-yield-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "price": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "rent": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "rentPeriod": {
            "type": "string",
            "enum": [
              "month",
              "year"
            ]
          },
          "bedrooms": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "bathrooms": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "floorAreaSqm": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000
          },
          "propertyType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "annualCosts": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "deposit": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "mortgageRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__investment-metrics",
      "description": "Calculate investment metrics. Calculate net yield, price per square metre, loan, and cash flow only from supplied price, rent, costs, deposit, and mortgage rate. No loan-to-value is assumed. Docs: https://www.brainiac.software/api/property-intelligence/investment-metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "price": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "rent": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "rentPeriod": {
            "type": "string",
            "enum": [
              "month",
              "year"
            ]
          },
          "bedrooms": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "bathrooms": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "floorAreaSqm": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000
          },
          "propertyType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "annualCosts": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "deposit": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "mortgageRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "property-intelligence__due-diligence-report",
      "description": "Prepare a due diligence report. Combine the observed listing, supplied assumptions, and any OpenStreetMap place or nearby features. Planning, crime, ownership, and valuation stay unavailable. Docs: https://www.brainiac.software/api/property-intelligence/due-diligence-report",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "description": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "address": {
            "type": "string",
            "minLength": 1,
            "maxLength": 300
          },
          "price": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "rent": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "rentPeriod": {
            "type": "string",
            "enum": [
              "month",
              "year"
            ]
          },
          "bedrooms": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          },
          "bathrooms": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "floorAreaSqm": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1000000
          },
          "propertyType": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
          },
          "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
          },
          "annualCosts": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "deposit": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "mortgageRate": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "comparables": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 8,
                  "maxLength": 2000,
                  "pattern": "^https?:\\/\\/\\S+$"
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "address": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 300
                },
                "price": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "rent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "rentPeriod": {
                  "type": "string",
                  "enum": [
                    "month",
                    "year"
                  ]
                },
                "bedrooms": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100
                },
                "bathrooms": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "floorAreaSqm": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 1000000
                },
                "propertyType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "annualCosts": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "deposit": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "mortgageRate": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
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
  "property-intelligence__overview": "0.05",
  "property-intelligence__constraints__check": "0.05",
  "property-intelligence__planning__search": "0.05",
  "property-intelligence__site__report": "0.10",
  "property-intelligence__listing-extract": "0.05",
  "property-intelligence__details-normalize": "0.03",
  "property-intelligence__description-analyze": "0.03",
  "property-intelligence__area-context": "0.04",
  "property-intelligence__location-features": "0.05",
  "property-intelligence__amenities-extract": "0.03",
  "property-intelligence__listing-duplicate-detect": "0.04",
  "property-intelligence__rent-yield-calculate": "0.03",
  "property-intelligence__investment-metrics": "0.04",
  "property-intelligence__due-diligence-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "property-intelligence__overview": "property-intelligence/overview",
  "property-intelligence__constraints__check": "property-intelligence/constraints/check",
  "property-intelligence__planning__search": "property-intelligence/planning/search",
  "property-intelligence__site__report": "property-intelligence/site/report",
  "property-intelligence__listing-extract": "property-intelligence/listing-extract",
  "property-intelligence__details-normalize": "property-intelligence/details-normalize",
  "property-intelligence__description-analyze": "property-intelligence/description-analyze",
  "property-intelligence__area-context": "property-intelligence/area-context",
  "property-intelligence__location-features": "property-intelligence/location-features",
  "property-intelligence__amenities-extract": "property-intelligence/amenities-extract",
  "property-intelligence__listing-duplicate-detect": "property-intelligence/listing-duplicate-detect",
  "property-intelligence__rent-yield-calculate": "property-intelligence/rent-yield-calculate",
  "property-intelligence__investment-metrics": "property-intelligence/investment-metrics",
  "property-intelligence__due-diligence-report": "property-intelligence/due-diligence-report"
}


class BrainiacPropertyIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — property-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the property-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "property-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Property overview"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the property-intelligence group. "
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
