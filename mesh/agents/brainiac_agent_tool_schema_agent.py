"""Auto-generated BRAINIAC Heurist Mesh agent for group `agent-tool-schema` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "agent-tool-schema__tool-schema-lint",
      "description": "Lint agent tool schemas. Find malformed JSON Schema and OpenAPI tool definitions in caller-supplied tools: bad types, required names that are not properties, empty enums, and duplicate tool names. Nothing is fetched. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-lint",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-ambiguity-detect",
      "description": "Detect ambiguous tool schemas. Flag generic tool names, generic parameter names, and descriptions that repeat the name or are missing. Matching is against a fixed word list, not a language model. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-ambiguity-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-overlap-detect",
      "description": "Detect overlapping tool schemas. Compare caller-supplied tools for the same name, the same description text, or a very high overlap of longer words. Sharing a few keywords is not treated as a duplicate. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-overlap-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-example-validate",
      "description": "Validate tool request examples. Check caller-supplied request examples against their JSON Schema types, required fields, enums, and bounds. External schema URLs are not fetched. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-example-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-required-field-audit",
      "description": "Audit tool required fields. Find required names that are not properties, repeated required names, and required fields that also declare a default. The audit uses only the supplied schema. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-required-field-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-compatibility-check",
      "description": "Check tool schema dialect compatibility. Report JSON Schema keywords that the caller-selected dialect does not allow. Targets are draft-07, 2020-12, OpenAPI 3.0, and OpenAPI 3.1. The schema is not sent to a validator service. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-compatibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          },
          "target": {
            "type": "string",
            "enum": [
              "draft-07",
              "2020-12",
              "openapi-3.0",
              "openapi-3.1"
            ]
          }
        },
        "required": [
          "target"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-token-cost",
      "description": "Estimate tool schema token cost. Estimate tokens for caller-supplied tool names, descriptions, and schemas at four characters per token. The figure is an estimate, not a provider tokenizer count. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-token-cost",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-tool-schema__tool-schema-description-score",
      "description": "Score tool description clarity. Score whether a tool description states a purpose, inputs, outputs, and when to use it. The checks are phrase and length rules, not a language-model reading. Docs: https://www.brainiac.software/api/agent-tool-schema/tool-schema-description-score",
      "parameters": {
        "type": "object",
        "properties": {
          "tools": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "parameters": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "inputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "examples": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {}
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "schemas": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "schema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                }
              },
              "required": [
                "name",
                "schema"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "agent-tool-schema__tool-schema-lint": "0.03",
  "agent-tool-schema__tool-schema-ambiguity-detect": "0.03",
  "agent-tool-schema__tool-schema-overlap-detect": "0.04",
  "agent-tool-schema__tool-schema-example-validate": "0.04",
  "agent-tool-schema__tool-schema-required-field-audit": "0.03",
  "agent-tool-schema__tool-schema-compatibility-check": "0.04",
  "agent-tool-schema__tool-schema-token-cost": "0.03",
  "agent-tool-schema__tool-schema-description-score": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "agent-tool-schema__tool-schema-lint": "agent-tool-schema/tool-schema-lint",
  "agent-tool-schema__tool-schema-ambiguity-detect": "agent-tool-schema/tool-schema-ambiguity-detect",
  "agent-tool-schema__tool-schema-overlap-detect": "agent-tool-schema/tool-schema-overlap-detect",
  "agent-tool-schema__tool-schema-example-validate": "agent-tool-schema/tool-schema-example-validate",
  "agent-tool-schema__tool-schema-required-field-audit": "agent-tool-schema/tool-schema-required-field-audit",
  "agent-tool-schema__tool-schema-compatibility-check": "agent-tool-schema/tool-schema-compatibility-check",
  "agent-tool-schema__tool-schema-token-cost": "agent-tool-schema/tool-schema-token-cost",
  "agent-tool-schema__tool-schema-description-score": "agent-tool-schema/tool-schema-description-score"
}


class BrainiacAgentToolSchemaAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — agent-tool-schema",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the agent-tool-schema catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "agent-tool-schema", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Lint agent tool schemas"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the agent-tool-schema group. "
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
