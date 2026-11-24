"""Auto-generated BRAINIAC Heurist Mesh agent for group `data-quality` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "data-quality__csv-schema-detect",
      "description": "Detect a CSV schema. Infer a column type from the supplied CSV or JSON values. A column with more than one non-numeric type stays mixed. No value is rewritten. Docs: https://www.brainiac.software/api/data-quality/csv-schema-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-profile",
      "description": "Profile CSV columns. Count present, missing, and distinct values for each column and report the minimum and maximum of the supplied values. Docs: https://www.brainiac.software/api/data-quality/csv-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-column-type-detect",
      "description": "Detect CSV column types. List the observed types in each column. A value that differs from the most common type is referenced by row and column and is not changed. A tie is not blamed on a row. Docs: https://www.brainiac.software/api/data-quality/csv-column-type-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-missing-value-audit",
      "description": "Audit missing CSV values. Find empty or whitespace-only cells and give each one a row and column reference. The row stays in the table. Docs: https://www.brainiac.software/api/data-quality/csv-missing-value-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-duplicate-row-detect",
      "description": "Detect duplicate CSV rows. Group records that match after trimming each compared cell. When key columns are supplied, only those columns are compared. No record is removed. Docs: https://www.brainiac.software/api/data-quality/csv-duplicate-row-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-outlier-detect",
      "description": "Detect statistical outliers. Flag numeric values outside a Tukey fence of 1.5 times the interquartile range when a column has at least eight numbers. Each flag is a possible outlier, not a confirmed error. Docs: https://www.brainiac.software/api/data-quality/csv-outlier-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-normalize",
      "description": "Propose CSV normalization. Propose trim, email lowercase, boolean tokens, and unambiguous thousands separators. Each change names its rule and keeps the original cell. Dates that are not already YYYY-MM-DD are not rewritten. Docs: https://www.brainiac.software/api/data-quality/csv-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
      "name": "data-quality__csv-report",
      "description": "Report CSV quality. Combine the schema, profile, missing cells, duplicate groups, possible outliers, and proposed normalization for one supplied table. No record is removed and no outlier is confirmed. Docs: https://www.brainiac.software/api/data-quality/csv-report",
      "parameters": {
        "type": "object",
        "properties": {
          "records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "additionalProperties": {
                "anyOf": [
                  {
                    "type": "string",
                    "maxLength": 4000
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            }
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
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
          "keyColumns": {
            "maxItems": 20,
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "data-quality__csv-schema-detect": "0.03",
  "data-quality__csv-profile": "0.04",
  "data-quality__csv-column-type-detect": "0.04",
  "data-quality__csv-missing-value-audit": "0.03",
  "data-quality__csv-duplicate-row-detect": "0.05",
  "data-quality__csv-outlier-detect": "0.05",
  "data-quality__csv-normalize": "0.04",
  "data-quality__csv-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "data-quality__csv-schema-detect": "data-quality/csv-schema-detect",
  "data-quality__csv-profile": "data-quality/csv-profile",
  "data-quality__csv-column-type-detect": "data-quality/csv-column-type-detect",
  "data-quality__csv-missing-value-audit": "data-quality/csv-missing-value-audit",
  "data-quality__csv-duplicate-row-detect": "data-quality/csv-duplicate-row-detect",
  "data-quality__csv-outlier-detect": "data-quality/csv-outlier-detect",
  "data-quality__csv-normalize": "data-quality/csv-normalize",
  "data-quality__csv-report": "data-quality/csv-report"
}


class BrainiacDataQualityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — data-quality",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the data-quality catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "data-quality", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect a CSV schema"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the data-quality group. "
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
