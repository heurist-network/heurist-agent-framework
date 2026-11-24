"""Auto-generated BRAINIAC Heurist Mesh agent for group `code` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "code__maintainability-index",
      "description": "Index source maintainability. Build a structural AST from a caller-supplied JavaScript, TypeScript, Python, or Go snippet, or from a caller-supplied AST, and score cyclomatic complexity, cognitive load, nesting depth, and duplicated function structure. The snippet is not executed or stored. Docs: https://www.brainiac.software/api/code/maintainability-index",
      "parameters": {
        "type": "object",
        "properties": {
          "language": {
            "type": "string",
            "enum": [
              "javascript",
              "typescript",
              "python",
              "go"
            ]
          },
          "source": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100000
          },
          "ast": {}
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "code__change-coupling-analyze",
      "description": "Analyze change coupling. Identify files outside a proposed change set that are coupled through supplied module edges, import paths, or historical co-change sets. The source is not compiled or executed. Docs: https://www.brainiac.software/api/code/change-coupling-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "files": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 260
                },
                "language": {
                  "type": "string",
                  "enum": [
                    "javascript",
                    "typescript",
                    "python",
                    "go",
                    "other"
                  ]
                },
                "source": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "path",
                "source"
              ],
              "additionalProperties": false
            }
          },
          "module_edges": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from_path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 260
                },
                "to_path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 260
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "import",
                    "call",
                    "data",
                    "other"
                  ]
                }
              },
              "required": [
                "from_path",
                "to_path"
              ],
              "additionalProperties": false
            }
          },
          "change_sets": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "paths": {
                  "minItems": 1,
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 260
                  }
                }
              },
              "required": [
                "id",
                "paths"
              ],
              "additionalProperties": false
            }
          },
          "proposed_paths": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 260
            }
          }
        },
        "required": [
          "files",
          "proposed_paths"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "code__concurrency-hazard-detect",
      "description": "Detect concurrency hazards. Flag potential race and shared-state hazards in caller-supplied source using deterministic pattern matches for async/concurrency markers, shared globals, and TOCTOU-shaped spans. The code is not executed. Docs: https://www.brainiac.software/api/code/concurrency-hazard-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "files": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 260
                },
                "language": {
                  "type": "string",
                  "enum": [
                    "javascript",
                    "typescript",
                    "python",
                    "go",
                    "other"
                  ]
                },
                "source": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "path",
                "source"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "files"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "code__error-propagation-audit",
      "description": "Audit error propagation. Find empty catches, swallowed promise rejections, logged-without-rethrow spans, and throw sites without local handlers in caller-supplied source. Pattern matches only; the code is not compiled or run. Docs: https://www.brainiac.software/api/code/error-propagation-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "files": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 260
                },
                "language": {
                  "type": "string",
                  "enum": [
                    "javascript",
                    "typescript",
                    "python",
                    "go",
                    "other"
                  ]
                },
                "source": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "path",
                "source"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "files"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "code__maintainability-index": "0.04",
  "code__change-coupling-analyze": "0.04",
  "code__concurrency-hazard-detect": "0.04",
  "code__error-propagation-audit": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "code__maintainability-index": "code/maintainability-index",
  "code__change-coupling-analyze": "code/change-coupling-analyze",
  "code__concurrency-hazard-detect": "code/concurrency-hazard-detect",
  "code__error-propagation-audit": "code/error-propagation-audit"
}


class BrainiacCodeAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — code",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the code catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "code", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Index source maintainability"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the code group. "
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
