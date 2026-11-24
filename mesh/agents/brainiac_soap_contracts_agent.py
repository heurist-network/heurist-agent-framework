"""Auto-generated BRAINIAC Heurist Mesh agent for group `soap-contracts` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "soap-contracts__wsdl-xsd-dependency-audit",
      "description": "Audit WSDL and XSD dependencies. Compare a caller-supplied WSDL 1.1 document and its XSD documents, including an optional previous set. audit_status is valid, warnings, breaking_changes, invalid, or incomplete. Imports are not downloaded. A schema difference is syntactic and is not proof that a SOAP client fails at runtime. Docs: https://www.brainiac.software/api/soap-contracts/wsdl-xsd-dependency-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "wsdl": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
              },
              "content": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100000
              }
            },
            "required": [
              "name",
              "content"
            ],
            "additionalProperties": false
          },
          "schemas": {
            "maxItems": 16,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "content": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "name",
                "content"
              ],
              "additionalProperties": false
            }
          },
          "previous": {
            "type": "object",
            "properties": {
              "wsdl": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                  },
                  "content": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100000
                  }
                },
                "required": [
                  "name",
                  "content"
                ],
                "additionalProperties": false
              },
              "schemas": {
                "maxItems": 16,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                    },
                    "content": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 100000
                    }
                  },
                  "required": [
                    "name",
                    "content"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "wsdl",
              "schemas"
            ],
            "additionalProperties": false
          },
          "clients": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "operations": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                  }
                },
                "elements": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "namespace": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "name": {
                        "type": "string",
                        "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                      }
                    },
                    "required": [
                      "namespace",
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "types": {
                  "maxItems": 32,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "namespace": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "name": {
                        "type": "string",
                        "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                      }
                    },
                    "required": [
                      "namespace",
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "wsdl",
          "schemas"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "soap-contracts__schema-dependency-tree",
      "description": "Score schema dependency weight. Read import, include, and complexType names from the supplied XML. A document cycle, or a complex type that references itself, sets the circular flag. The score counts types, imports, and non-builtin references. schemaLocation values are not downloaded. Docs: https://www.brainiac.software/api/soap-contracts/schema-dependency-tree",
      "parameters": {
        "type": "object",
        "properties": {
          "documents": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "content": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "name",
                "content"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "documents"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "soap-contracts__wsdl-xsd-dependency-audit": "0.05",
  "soap-contracts__schema-dependency-tree": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "soap-contracts__wsdl-xsd-dependency-audit": "soap-contracts/wsdl-xsd-dependency-audit",
  "soap-contracts__schema-dependency-tree": "soap-contracts/schema-dependency-tree"
}


class BrainiacSoapContractsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — soap-contracts",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the soap-contracts catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "soap-contracts", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit WSDL and XSD dependencies"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the soap-contracts group. "
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
