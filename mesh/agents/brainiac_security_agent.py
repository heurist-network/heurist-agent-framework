"""Auto-generated BRAINIAC Heurist Mesh agent for group `security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "security__payload-anomaly-score",
      "description": "Score payload anomaly and input safety. Score a caller-supplied JSON value or text string for nesting depth, mixed types, injection-shaped text, and size inflation. Matching is local and deterministic. The payload is not executed, fetched, or stored. Docs: https://www.brainiac.software/api/security/payload-anomaly-score",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200000
              },
              {
                "type": "number"
              },
              {
                "type": "boolean"
              },
              {
                "type": "null"
              },
              {
                "maxItems": 5000,
                "type": "array",
                "items": {}
              },
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              }
            ]
          }
        },
        "required": [
          "payload"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "security__trust-boundary-violation-detect",
      "description": "Detect trust-boundary violations. Find caller-supplied data flows that cross from a higher trust zone to a lower one without the required controls. Uses only supplied components, zones, flows, and controls. No infrastructure is scanned. Docs: https://www.brainiac.software/api/security/trust-boundary-violation-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "components": {
            "minItems": 1,
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
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "zone_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "service",
                    "datastore",
                    "gateway",
                    "client",
                    "queue",
                    "other"
                  ]
                }
              },
              "required": [
                "id",
                "zone_id"
              ],
              "additionalProperties": false
            }
          },
          "zones": {
            "minItems": 2,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "trust_level": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100
                }
              },
              "required": [
                "id",
                "trust_level"
              ],
              "additionalProperties": false
            }
          },
          "flows": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "from_component_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_component_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "data_classes": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "protocol": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "control_ids": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "from_component_id",
                "to_component_id",
                "data_classes"
              ],
              "additionalProperties": false
            }
          },
          "controls": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "encryption_in_transit",
                    "encryption_at_rest",
                    "authentication",
                    "authorization",
                    "network_policy",
                    "tokenization",
                    "logging",
                    "other"
                  ]
                },
                "component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "flow_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "zone_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "kind"
              ],
              "additionalProperties": false
            }
          },
          "required_controls_on_trust_drop": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "encryption_in_transit",
                "authentication",
                "authorization",
                "network_policy",
                "tokenization"
              ]
            }
          }
        },
        "required": [
          "components",
          "zones",
          "flows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "security__sensitive-data-flow-audit",
      "description": "Audit sensitive data flows. Check where caller-declared sensitive data classes travel through supplied components and whether handling rules for zones, components, and required controls are violated. No repository is scanned. Docs: https://www.brainiac.software/api/security/sensitive-data-flow-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "components": {
            "minItems": 1,
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
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "zone_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "service",
                    "datastore",
                    "gateway",
                    "client",
                    "queue",
                    "other"
                  ]
                }
              },
              "required": [
                "id",
                "zone_id"
              ],
              "additionalProperties": false
            }
          },
          "zones": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "trust_level": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100
                }
              },
              "required": [
                "id",
                "trust_level"
              ],
              "additionalProperties": false
            }
          },
          "flows": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "from_component_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_component_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "data_classes": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "protocol": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "control_ids": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "from_component_id",
                "to_component_id",
                "data_classes"
              ],
              "additionalProperties": false
            }
          },
          "controls": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "encryption_in_transit",
                    "encryption_at_rest",
                    "authentication",
                    "authorization",
                    "network_policy",
                    "tokenization",
                    "logging",
                    "other"
                  ]
                },
                "component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "flow_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "zone_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "kind"
              ],
              "additionalProperties": false
            }
          },
          "handling_rules": {
            "minItems": 1,
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
                "data_class": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "allowed_zone_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "allowed_component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "forbidden_component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "require_control_kinds": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "encryption_in_transit",
                      "encryption_at_rest",
                      "authentication",
                      "authorization",
                      "network_policy",
                      "tokenization",
                      "logging",
                      "other"
                    ]
                  }
                }
              },
              "required": [
                "id",
                "data_class"
              ],
              "additionalProperties": false
            }
          },
          "sensitive_data_classes": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          }
        },
        "required": [
          "components",
          "zones",
          "flows",
          "handling_rules",
          "sensitive_data_classes"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "security__security-control-coverage-gap",
      "description": "Find security control coverage gaps. Compare supplied security requirements with declared controls and evidence. Report requirements with no matching control or with matching controls that lack evidence. No cloud account is queried. Docs: https://www.brainiac.software/api/security/security-control-coverage-gap",
      "parameters": {
        "type": "object",
        "properties": {
          "requirements": {
            "minItems": 1,
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "required_control_kinds": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "encryption_in_transit",
                      "encryption_at_rest",
                      "authentication",
                      "authorization",
                      "network_policy",
                      "tokenization",
                      "logging",
                      "other"
                    ]
                  }
                },
                "component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "zone_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "evidence_required": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "text",
                "required_control_kinds"
              ],
              "additionalProperties": false
            }
          },
          "controls": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "encryption_in_transit",
                    "encryption_at_rest",
                    "authentication",
                    "authorization",
                    "network_policy",
                    "tokenization",
                    "logging",
                    "other"
                  ]
                },
                "component_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "flow_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "zone_ids": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "kind"
              ],
              "additionalProperties": false
            }
          },
          "components": {
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
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "zone_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "service",
                    "datastore",
                    "gateway",
                    "client",
                    "queue",
                    "other"
                  ]
                }
              },
              "required": [
                "id",
                "zone_id"
              ],
              "additionalProperties": false
            }
          },
          "zones": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "trust_level": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100
                }
              },
              "required": [
                "id",
                "trust_level"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "control_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "control_id",
                "detail"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "requirements",
          "controls"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "security__payload-anomaly-score": "0.04",
  "security__trust-boundary-violation-detect": "0.04",
  "security__sensitive-data-flow-audit": "0.04",
  "security__security-control-coverage-gap": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "security__payload-anomaly-score": "security/payload-anomaly-score",
  "security__trust-boundary-violation-detect": "security/trust-boundary-violation-detect",
  "security__sensitive-data-flow-audit": "security/sensitive-data-flow-audit",
  "security__security-control-coverage-gap": "security/security-control-coverage-gap"
}


class BrainiacSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Score payload anomaly and input safety"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the security group. "
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
