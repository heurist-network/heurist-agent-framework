"""Auto-generated BRAINIAC Heurist Mesh agent for group `security-configuration` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "security-configuration__header-audit",
      "description": "Audit security headers. Fetch a public URL (or use caller-supplied headers) and return per-header present/value/note rows for HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy, plus a documented mechanical grade. A grade is not proof the site is secure. Docs: https://www.brainiac.software/api/security-configuration/header-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__tls-audit",
      "description": "Audit TLS configuration. Read the certificate from one public HTTPS request, or from certificate fields supplied by the caller. An old protocol, an expired certificate, a name mismatch, or an untrusted certificate is confirmed. This does not show that the site is secure. Docs: https://www.brainiac.software/api/security-configuration/tls-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__cookie-audit",
      "description": "Audit cookie attributes. Check Secure, HttpOnly, and SameSite on Set-Cookie headers from one public response or from cookie lines supplied by the caller. Cookie values are not returned. Docs: https://www.brainiac.software/api/security-configuration/cookie-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__cors-policy-audit",
      "description": "Audit a CORS policy. Read CORS response headers. When an origin is supplied, it is sent once on the public GET. A wildcard, or a reflected origin with credentials, is confirmed. No other origins are tried. Docs: https://www.brainiac.software/api/security-configuration/cors-policy-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__csp-policy-analyze",
      "description": "Analyze a CSP policy. Read Content-Security-Policy from a public response or from policy text supplied by the caller. unsafe-inline, unsafe-eval, a script wildcard, and data: scripts are confirmed. This is not a full policy review. Docs: https://www.brainiac.software/api/security-configuration/csp-policy-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__exposed-file-check",
      "description": "Check listed public paths. Request only the paths the caller lists, on the same host as the supplied URL. A non-HTML HTTP 200 is a confirmed reachable path. No common-file list is guessed and the body is not copied. Docs: https://www.brainiac.software/api/security-configuration/exposed-file-check",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__public-endpoint-audit",
      "description": "Audit listed public endpoints. Send one GET to each listed public URL and record HTTPS, HSTS, and nosniff. Credential URLs and non-public addresses are not fetched. No login or credential test is attempted. Docs: https://www.brainiac.software/api/security-configuration/public-endpoint-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
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
      "name": "security-configuration__website-report",
      "description": "Report website security configuration. Combine header, TLS, cookie, CORS, and CSP observations for one public URL or supplied configuration. Extra paths and endpoints are requested only when listed. The report does not show that the site is secure. Docs: https://www.brainiac.software/api/security-configuration/website-report",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "origin": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "transport": {
            "type": "string",
            "enum": [
              "http",
              "https"
            ]
          },
          "headers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "value": {
                  "type": "string",
                  "maxLength": 4000
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "setCookies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "contentSecurityPolicy": {
            "type": "string",
            "maxLength": 8000
          },
          "contentSecurityPolicyReportOnly": {
            "type": "string",
            "maxLength": 8000
          },
          "tls": {
            "type": "object",
            "properties": {
              "protocol": {
                "type": "string",
                "maxLength": 40
              },
              "issuer": {
                "type": "string",
                "maxLength": 200
              },
              "subject": {
                "type": "string",
                "maxLength": 200
              },
              "validFrom": {
                "type": "string",
                "maxLength": 80
              },
              "validTo": {
                "type": "string",
                "maxLength": 80
              },
              "authorized": {
                "type": "boolean"
              },
              "hostnameMatches": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "paths": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "endpoints": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 8,
              "maxLength": 2000,
              "pattern": "^https?:\\/\\/\\S+$"
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "security-configuration__header-audit": "0.01",
  "security-configuration__tls-audit": "0.04",
  "security-configuration__cookie-audit": "0.03",
  "security-configuration__cors-policy-audit": "0.04",
  "security-configuration__csp-policy-analyze": "0.04",
  "security-configuration__exposed-file-check": "0.05",
  "security-configuration__public-endpoint-audit": "0.05",
  "security-configuration__website-report": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "security-configuration__header-audit": "security-configuration/header-audit",
  "security-configuration__tls-audit": "security-configuration/tls-audit",
  "security-configuration__cookie-audit": "security-configuration/cookie-audit",
  "security-configuration__cors-policy-audit": "security-configuration/cors-policy-audit",
  "security-configuration__csp-policy-analyze": "security-configuration/csp-policy-analyze",
  "security-configuration__exposed-file-check": "security-configuration/exposed-file-check",
  "security-configuration__public-endpoint-audit": "security-configuration/public-endpoint-audit",
  "security-configuration__website-report": "security-configuration/website-report"
}


class BrainiacSecurityConfigurationAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — security-configuration",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the security-configuration catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "security-configuration", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit security headers"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the security-configuration group. "
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
