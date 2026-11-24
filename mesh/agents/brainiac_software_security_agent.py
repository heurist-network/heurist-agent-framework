"""Auto-generated BRAINIAC Heurist Mesh agent for group `software-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "software-security__sbom-vulnerability-match",
      "description": "Match SBOM vulnerabilities. Parse a CycloneDX or SPDX SBOM, or a component list, and classify each exact package version against OSV advisories as affected, unaffected, or unknown. A similar package name is not a match. Docs: https://www.brainiac.software/api/software-security/sbom-vulnerability-match",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "software-security__dependency-risk-report",
      "description": "Report dependency risk. Summarise affected, unaffected, and unknown OSV advisory counts for each exact dependency version. No risk score is calculated. Docs: https://www.brainiac.software/api/software-security/dependency-risk-report",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "software-security__kev-exposure-check",
      "description": "Check KEV exposure. Compare exact dependency versions with OSV advisories and the CISA Known Exploited Vulnerabilities catalog. A KEV entry is reported only when that CVE applies to the same package and version range. Docs: https://www.brainiac.software/api/software-security/kev-exposure-check",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "software-security__license-compatibility-check",
      "description": "Check licence compatibility. Read licence identifiers declared in the SBOM or published by npm, PyPI, crates.io, or RubyGems, then compare them with the caller allow and deny policy. Missing identifiers are not treated as compatible. Docs: https://www.brainiac.software/api/software-security/license-compatibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "policy": {
            "type": "object",
            "properties": {
              "allow": {
                "maxItems": 30,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "deny": {
                "maxItems": 30,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "software-security__malicious-dependency-check",
      "description": "Check malicious dependencies. Look for OSV malicious-package advisories and npm compromise heuristics (typosquat distance to popular names, very new packages, few versions, missing repository). Signals are not proof of malware; no advisory does not mean the package is safe. Docs: https://www.brainiac.software/api/software-security/malicious-dependency-check",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
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
      "name": "software-security__release-precheck",
      "description": "Precheck release security. Combine exact-version OSV matches, CISA KEV exposure, licence policy, and malicious-package advisories into one release report. The report never approves a release. Docs: https://www.brainiac.software/api/software-security/release-precheck",
      "parameters": {
        "type": "object",
        "properties": {
          "sbom": {
            "type": "string",
            "minLength": 2,
            "maxLength": 400000
          },
          "components": {
            "minItems": 1,
            "maxItems": 25,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ecosystem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "version": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100
                },
                "purl": {
                  "type": "string",
                  "minLength": 4,
                  "maxLength": 500
                },
                "license": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "policy": {
            "type": "object",
            "properties": {
              "allow": {
                "maxItems": 30,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "deny": {
                "maxItems": 30,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "software-security__sbom-vulnerability-match": "0.001",
  "software-security__dependency-risk-report": "0.001",
  "software-security__kev-exposure-check": "0.001",
  "software-security__license-compatibility-check": "0.001",
  "software-security__malicious-dependency-check": "0.001",
  "software-security__release-precheck": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "software-security__sbom-vulnerability-match": "software-security/sbom-vulnerability-match",
  "software-security__dependency-risk-report": "software-security/dependency-risk-report",
  "software-security__kev-exposure-check": "software-security/kev-exposure-check",
  "software-security__license-compatibility-check": "software-security/license-compatibility-check",
  "software-security__malicious-dependency-check": "software-security/malicious-dependency-check",
  "software-security__release-precheck": "software-security/release-precheck"
}


class BrainiacSoftwareSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — software-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the software-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "software-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Match SBOM vulnerabilities"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the software-security group. "
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
