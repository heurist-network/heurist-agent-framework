"""Auto-generated BRAINIAC Heurist Mesh agent for group `cybersecurity-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "cybersecurity-intelligence__vulnerability",
      "description": "Get vulnerability details. Retrieve details for a CVE or vulnerability ID from OSV, CISA KEV, FIRST EPSS, and NVD. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/vulnerability",
      "parameters": {
        "type": "object",
        "properties": {
          "cveId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 30
          }
        },
        "required": [
          "cveId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__package__check",
      "description": "Check package vulnerabilities. Check one package and version for vulnerabilities using OSV, enriched with CISA KEV, EPSS, and NVD data. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/package-check",
      "parameters": {
        "type": "object",
        "properties": {
          "ecosystem": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
          },
          "package": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "version": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          }
        },
        "required": [
          "ecosystem",
          "package",
          "version"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__package__batch-check",
      "description": "Batch check package vulnerabilities. Check multiple packages and versions for vulnerabilities using OSV batch query, enriched with CISA KEV, EPSS, and NVD data. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/package-batch-check",
      "parameters": {
        "type": "object",
        "properties": {
          "packages": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50
                },
                "package": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                }
              },
              "required": [
                "ecosystem",
                "package",
                "version"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "packages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__risk__assess",
      "description": "Assess vulnerability risk. Produce a consolidated vulnerability risk assessment for multiple packages, combining OSV, CISA KEV, EPSS, and NVD data. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/risk-assess",
      "parameters": {
        "type": "object",
        "properties": {
          "packages": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50
                },
                "package": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                }
              },
              "required": [
                "ecosystem",
                "package",
                "version"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "packages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__dependency-tree",
      "description": "Get dependency tree. Return direct and transitive dependencies, dependency versions and available dependency metadata using Google deps.dev API. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/dependency-tree",
      "parameters": {
        "type": "object",
        "properties": {
          "ecosystem": {
            "type": "string",
            "enum": [
              "GO",
              "RUBYGEMS",
              "NPM",
              "CARGO",
              "MAVEN",
              "PYPI",
              "NUGET"
            ]
          },
          "packageName": {
            "type": "string"
          },
          "version": {
            "type": "string"
          }
        },
        "required": [
          "ecosystem",
          "packageName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__package__project-health",
      "description": "Get package project health. Return project activity indicators, repository associations, package metadata and available security information using Google deps.dev API. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/package-project-health",
      "parameters": {
        "type": "object",
        "properties": {
          "ecosystem": {
            "type": "string",
            "enum": [
              "GO",
              "RUBYGEMS",
              "NPM",
              "CARGO",
              "MAVEN",
              "PYPI",
              "NUGET"
            ]
          },
          "packageName": {
            "type": "string"
          }
        },
        "required": [
          "ecosystem",
          "packageName"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__repository__scorecard",
      "description": "Get repository Scorecard. Retrieve the official OpenSSF Scorecard result for a GitHub, GitLab or other supported repository. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/repository-scorecard",
      "parameters": {
        "type": "object",
        "properties": {
          "repository": {
            "type": "string",
            "format": "uri"
          }
        },
        "required": [
          "repository"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cybersecurity-intelligence__lockfile__audit",
      "description": "Audit lockfile. Parse supported package lockfiles, identify dependencies and versions, then combine deps.dev and existing OSV/CISA/EPSS/NVD findings. Docs: https://www.brainiac.software/api/cybersecurity-intelligence/lockfile-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "lockfileContent": {
            "type": "string"
          },
          "ecosystem": {
            "type": "string",
            "enum": [
              "NPM",
              "PYPI",
              "MAVEN",
              "RUBYGEMS",
              "CARGO",
              "NUGET",
              "GO"
            ]
          }
        },
        "required": [
          "lockfileContent"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "cybersecurity-intelligence__vulnerability": "0.001",
  "cybersecurity-intelligence__package__check": "0.001",
  "cybersecurity-intelligence__package__batch-check": "0.001",
  "cybersecurity-intelligence__risk__assess": "0.001",
  "cybersecurity-intelligence__dependency-tree": "0.001",
  "cybersecurity-intelligence__package__project-health": "0.001",
  "cybersecurity-intelligence__repository__scorecard": "0.001",
  "cybersecurity-intelligence__lockfile__audit": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "cybersecurity-intelligence__vulnerability": "cybersecurity-intelligence/vulnerability",
  "cybersecurity-intelligence__package__check": "cybersecurity-intelligence/package/check",
  "cybersecurity-intelligence__package__batch-check": "cybersecurity-intelligence/package/batch-check",
  "cybersecurity-intelligence__risk__assess": "cybersecurity-intelligence/risk/assess",
  "cybersecurity-intelligence__dependency-tree": "cybersecurity-intelligence/dependency-tree",
  "cybersecurity-intelligence__package__project-health": "cybersecurity-intelligence/package/project-health",
  "cybersecurity-intelligence__repository__scorecard": "cybersecurity-intelligence/repository/scorecard",
  "cybersecurity-intelligence__lockfile__audit": "cybersecurity-intelligence/lockfile/audit"
}


class BrainiacCybersecurityIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — cybersecurity-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the cybersecurity-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "cybersecurity-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Get vulnerability details"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the cybersecurity-intelligence group. "
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
