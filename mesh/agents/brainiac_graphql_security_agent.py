"""Auto-generated BRAINIAC Heurist Mesh agent for group `graphql-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "graphql-security__federation-authorization-audit",
      "description": "Audit federation authorization. Compare @authenticated, @requiresScopes, @policy, and caller-defined authorization directives across supplied subgraph SDL. @requires, @key, @external, @provides, and @shareable are inspected for schema-level differences. audit_status is clean, findings_detected, invalid, or incomplete. risk_level is low, medium, high, or critical. A difference is not a runtime authorization result. No gateway is contacted. Docs: https://www.brainiac.software/api/graphql-security/federation-authorization-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "subgraphs": {
            "minItems": 1,
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "sdl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60000
                },
                "federationVersion": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$"
                }
              },
              "required": [
                "name",
                "sdl"
              ],
              "additionalProperties": false
            }
          },
          "authorizationDirectives": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[_A-Za-z][_0-9A-Za-z]{0,79}$"
                },
                "semantics": {
                  "type": "string",
                  "enum": [
                    "authenticated",
                    "scopes",
                    "policy"
                  ]
                },
                "argument": {
                  "type": "string",
                  "pattern": "^[_A-Za-z][_0-9A-Za-z]{0,79}$"
                }
              },
              "required": [
                "name",
                "semantics"
              ],
              "additionalProperties": false
            }
          },
          "expected": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "pattern": "^[_A-Za-z][_0-9A-Za-z]{0,79}$"
                },
                "field": {
                  "type": "string",
                  "pattern": "^[_A-Za-z][_0-9A-Za-z]{0,79}$"
                },
                "subgraph": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "authenticated": {
                  "type": "boolean"
                },
                "scopes": {
                  "minItems": 1,
                  "maxItems": 8,
                  "type": "array",
                  "items": {
                    "minItems": 1,
                    "maxItems": 16,
                    "type": "array",
                    "items": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  }
                },
                "policies": {
                  "minItems": 1,
                  "maxItems": 8,
                  "type": "array",
                  "items": {
                    "minItems": 1,
                    "maxItems": 16,
                    "type": "array",
                    "items": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  }
                }
              },
              "required": [
                "type"
              ],
              "additionalProperties": false
            }
          },
          "supergraph": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80000
          }
        },
        "required": [
          "subgraphs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "graphql-security__field-authorization-coverage",
      "description": "Score field authorization coverage. Count object and interface fields in the supplied subgraph SDL and mark a field when its line, or its type line, contains one of the supplied directive names. Coverage is the share of marked fields. This is a text count. It does not compose a supergraph or decide whether a request would be allowed. Docs: https://www.brainiac.software/api/graphql-security/field-authorization-coverage",
      "parameters": {
        "type": "object",
        "properties": {
          "protected_directives": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^@[A-Za-z][A-Za-z0-9]*$"
            }
          },
          "subgraphs": {
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
                "sdl": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                }
              },
              "required": [
                "name",
                "sdl"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "protected_directives",
          "subgraphs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "graphql-security__federation-subgraph-exposure-audit",
      "description": "Audit federation subgraph exposure. Compare caller-supplied subgraph endpoints, router authentication, network rules, and service or ingress labels with the intended public subgraph list. audit_status is clean, findings_detected, incomplete, or invalid. risk_level is low, medium, high, or critical. A public label is not evidence that an endpoint is reachable. No URL is probed. Docs: https://www.brainiac.software/api/graphql-security/federation-subgraph-exposure-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "subgraphs": {
            "minItems": 1,
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "endpoint": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "authentication": {
                  "type": "string",
                  "enum": [
                    "required",
                    "disabled",
                    "unknown"
                  ]
                },
                "acceptsDirectClients": {
                  "type": "boolean"
                },
                "introspection": {
                  "type": "boolean"
                },
                "developmentMode": {
                  "type": "boolean"
                },
                "service": {
                  "type": "object",
                  "properties": {
                    "exposure": {
                      "type": "string",
                      "enum": [
                        "cluster_local",
                        "internal",
                        "public",
                        "unknown"
                      ]
                    }
                  },
                  "required": [
                    "exposure"
                  ],
                  "additionalProperties": false
                },
                "ingress": {
                  "type": "object",
                  "properties": {
                    "audience": {
                      "type": "string",
                      "enum": [
                        "public",
                        "internal",
                        "unknown"
                      ]
                    }
                  },
                  "required": [
                    "audience"
                  ],
                  "additionalProperties": false
                },
                "federationFields": {
                  "type": "object",
                  "properties": {
                    "service": {
                      "type": "string",
                      "enum": [
                        "router_only",
                        "exposed",
                        "unknown"
                      ]
                    },
                    "entities": {
                      "type": "string",
                      "enum": [
                        "router_only",
                        "exposed",
                        "unknown"
                      ]
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "router": {
            "type": "object",
            "properties": {
              "authenticationToSubgraphs": {
                "type": "string",
                "enum": [
                  "required",
                  "disabled",
                  "per_subgraph",
                  "unknown"
                ]
              },
              "introspection": {
                "type": "boolean"
              },
              "sandbox": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "networkRules": {
            "maxItems": 128,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "subgraph": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "source": {
                  "type": "string",
                  "enum": [
                    "router",
                    "public",
                    "cluster",
                    "any"
                  ]
                },
                "action": {
                  "type": "string",
                  "enum": [
                    "allow",
                    "deny"
                  ]
                }
              },
              "required": [
                "subgraph",
                "source",
                "action"
              ],
              "additionalProperties": false
            }
          },
          "publicEndpoints": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
            }
          }
        },
        "required": [
          "subgraphs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "graphql-security__subgraph-complexity",
      "description": "Score subgraph query depth. Walk object-type references in the supplied SDL, starting at Query when that type is present. Scalars are ignored and a repeated type is not walked again. The index is that depth. The risk score rises when the depth passes the supplied limit, and when introspection is enabled. No router is contacted. Docs: https://www.brainiac.software/api/graphql-security/subgraph-complexity",
      "parameters": {
        "type": "object",
        "properties": {
          "sdl": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "max_depth": {
            "type": "integer",
            "minimum": 1,
            "maximum": 20
          },
          "introspection": {
            "type": "string",
            "enum": [
              "enabled",
              "disabled"
            ]
          }
        },
        "required": [
          "sdl",
          "max_depth",
          "introspection"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "graphql-security__federation-authorization-audit": "0.05",
  "graphql-security__field-authorization-coverage": "0.04",
  "graphql-security__federation-subgraph-exposure-audit": "0.05",
  "graphql-security__subgraph-complexity": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "graphql-security__federation-authorization-audit": "graphql-security/federation-authorization-audit",
  "graphql-security__field-authorization-coverage": "graphql-security/field-authorization-coverage",
  "graphql-security__federation-subgraph-exposure-audit": "graphql-security/federation-subgraph-exposure-audit",
  "graphql-security__subgraph-complexity": "graphql-security/subgraph-complexity"
}


class BrainiacGraphqlSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — graphql-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the graphql-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "graphql-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit federation authorization"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the graphql-security group. "
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
