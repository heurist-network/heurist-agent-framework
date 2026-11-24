"""Auto-generated BRAINIAC Heurist Mesh agent for group `appsec-config` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "appsec-config__secrets-scan",
      "description": "Scan files for secrets with gitleaks rules. Find secrets in text or diffs using vendored gitleaks rules with redaction. Docs: https://www.brainiac.software/api/appsec-config/secrets-scan",
      "parameters": {
        "type": "object",
        "properties": {
          "files": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "path": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 1024
                },
                "content": {
                  "type": "string",
                  "maxLength": 2000000
                }
              },
              "required": [
                "path",
                "content"
              ],
              "additionalProperties": false
            }
          },
          "mode": {
            "default": "text",
            "type": "string",
            "enum": [
              "text",
              "diff"
            ]
          },
          "allowlistPaths": {
            "default": [],
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "includeLowEntropy": {
            "default": false,
            "type": "boolean"
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
      "name": "appsec-config__github-actions-audit",
      "description": "Audit GitHub Actions workflows. Find injection, pinning, permission and pull_request_target risks. Docs: https://www.brainiac.software/api/appsec-config/github-actions-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "files": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "path": {
                  "type": "string"
                },
                "content": {
                  "type": "string",
                  "maxLength": 2000000
                }
              },
              "required": [
                "path",
                "content"
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
      "name": "appsec-config__gitlab-ci-audit",
      "description": "Audit GitLab CI configuration. Flag unpinned images, remote includes, secrets and dind risks. Docs: https://www.brainiac.software/api/appsec-config/gitlab-ci-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 2000000
          },
          "requireDigest": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__cloudformation-audit",
      "description": "Audit CloudFormation templates. Flag public storage, open security groups, missing encryption and wildcard IAM. Docs: https://www.brainiac.software/api/appsec-config/cloudformation-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "template": {
            "type": "string",
            "maxLength": 5000000
          }
        },
        "required": [
          "template"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__aws-iam-policy-analyze",
      "description": "Analyse AWS IAM policy documents. Find wildcards, NotAction pitfalls, privilege-escalation actions and public principals. Docs: https://www.brainiac.software/api/appsec-config/aws-iam-policy-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "policy": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              }
            ]
          },
          "policyType": {
            "default": "identity",
            "type": "string",
            "enum": [
              "identity",
              "resource",
              "trust"
            ]
          }
        },
        "required": [
          "policy"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__gcp-iam-binding-analyze",
      "description": "Analyse GCP IAM policy bindings. Flag basic roles, public members and service-account impersonation. Docs: https://www.brainiac.software/api/appsec-config/gcp-iam-binding-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "policy": {
            "type": "object",
            "properties": {
              "bindings": {
                "type": "array",
                "items": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string"
                  },
                  "additionalProperties": {}
                }
              }
            },
            "required": [
              "bindings"
            ],
            "additionalProperties": false
          },
          "serviceAccountPolicies": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {}
          }
        },
        "required": [
          "policy"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__jwt-inspect",
      "description": "Inspect JWTs for weak crypto and claims. Decode JWTs, flag alg:none, weak HMAC secrets and lifetime issues. Docs: https://www.brainiac.software/api/appsec-config/jwt-inspect",
      "parameters": {
        "type": "object",
        "properties": {
          "token": {
            "type": "string",
            "minLength": 10,
            "maxLength": 16384
          },
          "now": {
            "type": "string"
          },
          "maxLifetimeSeconds": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "expectedAudience": {
            "type": [
              "string",
              "null"
            ]
          },
          "publicKeyPem": {
            "type": "string"
          }
        },
        "required": [
          "token"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__regex-redos-check",
      "description": "Detect ReDoS risk in a regular expression. Check a JavaScript regex for catastrophic backtracking with recheck. Docs: https://www.brainiac.software/api/appsec-config/regex-redos-check",
      "parameters": {
        "type": "object",
        "properties": {
          "pattern": {
            "type": "string",
            "maxLength": 2000
          },
          "flags": {
            "default": "",
            "type": "string",
            "maxLength": 16
          },
          "flavour": {
            "default": "javascript",
            "type": "string",
            "enum": [
              "javascript"
            ]
          }
        },
        "required": [
          "pattern"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__injection-sink-scan",
      "description": "Scan a file for injection sinks. Lightweight single-file taint scan for SQL, command and XSS sinks. Docs: https://www.brainiac.software/api/appsec-config/injection-sink-scan",
      "parameters": {
        "type": "object",
        "properties": {
          "language": {
            "type": "string",
            "enum": [
              "javascript",
              "typescript",
              "python"
            ]
          },
          "path": {
            "default": "input",
            "type": "string"
          },
          "content": {
            "type": "string",
            "maxLength": 500000
          }
        },
        "required": [
          "language",
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__openapi-security-audit",
      "description": "Audit OpenAPI 3.x security design. OWASP API Top 10 style checks on an OpenAPI document. Docs: https://www.brainiac.software/api/appsec-config/openapi-security-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "spec": {
            "type": "string",
            "maxLength": 5000000
          }
        },
        "required": [
          "spec"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__password-policy-evaluate",
      "description": "Evaluate a password policy vs NIST. Check policy fields and optional samples against NIST SP 800-63B-4. Docs: https://www.brainiac.software/api/appsec-config/password-policy-evaluate",
      "parameters": {
        "type": "object",
        "properties": {
          "policy": {
            "type": "object",
            "properties": {
              "minLength": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "maxLength": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "usedAsSingleFactor": {
                "type": "boolean"
              },
              "compositionRules": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "periodicExpiryDays": {
                "anyOf": [
                  {
                    "type": "integer",
                    "minimum": -9007199254740991,
                    "maximum": 9007199254740991
                  },
                  {
                    "type": "null"
                  }
                ]
              },
              "blocklistCheck": {
                "type": "boolean"
              },
              "allowsUnicode": {
                "type": "boolean"
              },
              "allowsSpace": {
                "type": "boolean"
              },
              "hintsAllowed": {
                "type": "boolean"
              },
              "securityQuestions": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "samples": {
            "default": [],
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 256
            }
          }
        },
        "required": [
          "policy"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__sbom-generate",
      "description": "Generate an SBOM from a lockfile. Build CycloneDX or SPDX SBOMs from npm/PyPI/Go/Cargo lockfiles. Docs: https://www.brainiac.software/api/appsec-config/sbom-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "lockfile": {
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "enum": [
                  "package-lock",
                  "pnpm-lock",
                  "yarn-lock",
                  "requirements",
                  "poetry-lock",
                  "go-mod",
                  "cargo-lock"
                ]
              },
              "content": {
                "type": "string",
                "maxLength": 10000000
              }
            },
            "required": [
              "type",
              "content"
            ],
            "additionalProperties": false
          },
          "format": {
            "default": "cyclonedx-1.6-json",
            "type": "string",
            "enum": [
              "cyclonedx-1.6-json",
              "spdx-2.3-json"
            ]
          }
        },
        "required": [
          "lockfile"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__nginx-config-audit",
      "description": "Audit nginx configuration. Find weak TLS, alias traversal, open proxy and missing headers. Docs: https://www.brainiac.software/api/appsec-config/nginx-config-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 2000000
          }
        },
        "required": [
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__apache-config-audit",
      "description": "Audit Apache httpd configuration. Find weak TLS, directory listing, TRACE and missing hardening. Docs: https://www.brainiac.software/api/appsec-config/apache-config-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "maxLength": 2000000
          },
          "kind": {
            "default": "httpd.conf",
            "type": "string",
            "enum": [
              "httpd.conf",
              "htaccess"
            ]
          }
        },
        "required": [
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appsec-config__oauth-client-audit",
      "description": "Audit OAuth/OIDC client registration. Check client settings against RFC 9700 security BCP. Docs: https://www.brainiac.software/api/appsec-config/oauth-client-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "client": {
            "type": "object",
            "properties": {
              "clientType": {
                "type": "string",
                "enum": [
                  "public",
                  "confidential"
                ]
              },
              "grantTypes": {
                "default": [],
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "responseTypes": {
                "default": [],
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "redirectUris": {
                "default": [],
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "pkceRequired": {
                "type": "boolean"
              },
              "pkceMethods": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "refreshTokenRotation": {
                "type": "boolean"
              },
              "senderConstrainedRefreshTokens": {
                "type": "boolean"
              },
              "accessTokenLifetimeSeconds": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "scopes": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            },
            "required": [
              "clientType"
            ],
            "additionalProperties": false
          },
          "maxAccessTokenLifetimeSeconds": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "broadScopes": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "client"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "appsec-config__secrets-scan": "0.04",
  "appsec-config__github-actions-audit": "0.03",
  "appsec-config__gitlab-ci-audit": "0.03",
  "appsec-config__cloudformation-audit": "0.04",
  "appsec-config__aws-iam-policy-analyze": "0.03",
  "appsec-config__gcp-iam-binding-analyze": "0.03",
  "appsec-config__jwt-inspect": "0.03",
  "appsec-config__regex-redos-check": "0.02",
  "appsec-config__injection-sink-scan": "0.03",
  "appsec-config__openapi-security-audit": "0.04",
  "appsec-config__password-policy-evaluate": "0.02",
  "appsec-config__sbom-generate": "0.03",
  "appsec-config__nginx-config-audit": "0.03",
  "appsec-config__apache-config-audit": "0.03",
  "appsec-config__oauth-client-audit": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "appsec-config__secrets-scan": "appsec-config/secrets-scan",
  "appsec-config__github-actions-audit": "appsec-config/github-actions-audit",
  "appsec-config__gitlab-ci-audit": "appsec-config/gitlab-ci-audit",
  "appsec-config__cloudformation-audit": "appsec-config/cloudformation-audit",
  "appsec-config__aws-iam-policy-analyze": "appsec-config/aws-iam-policy-analyze",
  "appsec-config__gcp-iam-binding-analyze": "appsec-config/gcp-iam-binding-analyze",
  "appsec-config__jwt-inspect": "appsec-config/jwt-inspect",
  "appsec-config__regex-redos-check": "appsec-config/regex-redos-check",
  "appsec-config__injection-sink-scan": "appsec-config/injection-sink-scan",
  "appsec-config__openapi-security-audit": "appsec-config/openapi-security-audit",
  "appsec-config__password-policy-evaluate": "appsec-config/password-policy-evaluate",
  "appsec-config__sbom-generate": "appsec-config/sbom-generate",
  "appsec-config__nginx-config-audit": "appsec-config/nginx-config-audit",
  "appsec-config__apache-config-audit": "appsec-config/apache-config-audit",
  "appsec-config__oauth-client-audit": "appsec-config/oauth-client-audit"
}


class BrainiacAppsecConfigAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — appsec-config",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the appsec-config catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "appsec-config", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Scan files for secrets with gitleaks rules"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the appsec-config group. "
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
