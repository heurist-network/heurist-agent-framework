"""Auto-generated BRAINIAC Heurist Mesh agent for group `devops` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "devops__config-hardening-grade",
      "description": "Grade infrastructure config hardening. Grade a caller-supplied Dockerfile, Kubernetes YAML document, or Terraform JSON file for root execution, exposed ports, missing resource limits, and insecure defaults. Parsing stays in memory. The file is not applied, fetched, or stored. Docs: https://www.brainiac.software/api/devops/config-hardening-grade",
      "parameters": {
        "type": "object",
        "properties": {
          "config": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": [
          "config"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "devops__deployment-blast-radius",
      "description": "Calculate deployment blast radius. Walk a caller-supplied service dependency graph from proposed changes and list upstream and downstream services that may be affected. No CI/CD system is contacted. Docs: https://www.brainiac.software/api/devops/deployment-blast-radius",
      "parameters": {
        "type": "object",
        "properties": {
          "services": {
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
                "tier": {
                  "type": "string",
                  "enum": [
                    "edge",
                    "app",
                    "data",
                    "platform",
                    "other"
                  ]
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "dependencies": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from_service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "runtime",
                    "build",
                    "data",
                    "config",
                    "other"
                  ]
                }
              },
              "required": [
                "from_service_id",
                "to_service_id"
              ],
              "additionalProperties": false
            }
          },
          "changes": {
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
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "change_kind": {
                  "type": "string",
                  "enum": [
                    "code",
                    "config",
                    "schema",
                    "infra",
                    "other"
                  ]
                },
                "breaking": {
                  "type": "boolean"
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "service_id",
                "change_kind"
              ],
              "additionalProperties": false
            }
          },
          "direction": {
            "type": "string",
            "enum": [
              "downstream",
              "upstream",
              "both"
            ]
          }
        },
        "required": [
          "services",
          "dependencies",
          "changes"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "devops__rollback-feasibility-check",
      "description": "Check rollback feasibility. Evaluate whether a proposed deployment can be rolled back using supplied versions, migration reversibility, compatibility constraints, and recovery procedures. No deployment platform is queried. Docs: https://www.brainiac.software/api/devops/rollback-feasibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "versions": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "current_version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "target_version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "previous_version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "service_id",
                "current_version",
                "target_version"
              ],
              "additionalProperties": false
            }
          },
          "migrations": {
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
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "expand",
                    "contract",
                    "rewrite",
                    "other"
                  ]
                },
                "reversible": {
                  "type": "boolean"
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "service_id",
                "direction",
                "reversible"
              ],
              "additionalProperties": false
            }
          },
          "compatibility": {
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
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "depends_on_service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "min_version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "max_version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "compatible_with_rollback": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "service_id",
                "depends_on_service_id",
                "compatible_with_rollback"
              ],
              "additionalProperties": false
            }
          },
          "recovery_procedures": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "procedure": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "automated": {
                  "type": "boolean"
                },
                "rto_minutes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 525600
                }
              },
              "required": [
                "service_id",
                "procedure"
              ],
              "additionalProperties": false
            }
          },
          "max_rto_minutes": {
            "type": "integer",
            "minimum": 0,
            "maximum": 525600
          }
        },
        "required": [
          "versions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "devops__release-readiness-audit",
      "description": "Audit release readiness. Check whether a release meets supplied operational requirements: prerequisites, monitoring coverage, rollback plans, and unresolved blockers. Returns concrete gaps rather than a generic risk score. Docs: https://www.brainiac.software/api/devops/release-readiness-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "release_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "services": {
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
                "tier": {
                  "type": "string",
                  "enum": [
                    "edge",
                    "app",
                    "data",
                    "platform",
                    "other"
                  ]
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "prerequisites": {
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
                "satisfied": {
                  "type": "boolean"
                },
                "evidence": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "text",
                "satisfied"
              ],
              "additionalProperties": false
            }
          },
          "monitoring": {
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
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "signal": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "covered": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "service_id",
                "signal",
                "covered"
              ],
              "additionalProperties": false
            }
          },
          "rollback_plans": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "service_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "procedure": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "automated": {
                  "type": "boolean"
                },
                "rto_minutes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 525600
                }
              },
              "required": [
                "service_id",
                "procedure"
              ],
              "additionalProperties": false
            }
          },
          "blockers": {
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
                "severity": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "resolved": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "text",
                "severity",
                "resolved"
              ],
              "additionalProperties": false
            }
          },
          "require_monitoring_per_service": {
            "type": "boolean"
          },
          "require_rollback_plan_per_service": {
            "type": "boolean"
          }
        },
        "required": [
          "release_id",
          "services"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "devops__config-hardening-grade": "0.04",
  "devops__deployment-blast-radius": "0.04",
  "devops__rollback-feasibility-check": "0.04",
  "devops__release-readiness-audit": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "devops__config-hardening-grade": "devops/config-hardening-grade",
  "devops__deployment-blast-radius": "devops/deployment-blast-radius",
  "devops__rollback-feasibility-check": "devops/rollback-feasibility-check",
  "devops__release-readiness-audit": "devops/release-readiness-audit"
}


class BrainiacDevopsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — devops",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the devops catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "devops", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Grade infrastructure config hardening"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the devops group. "
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
