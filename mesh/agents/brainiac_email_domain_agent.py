"""Auto-generated BRAINIAC Heurist Mesh agent for group `email-domain` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "email-domain__syntax-validate",
      "description": "Validate email syntax. Check that an address is a bare email with a public domain. The mailbox is not contacted, and a valid result does not mean the address exists. Docs: https://www.brainiac.software/api/email-domain/syntax-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "minLength": 3,
            "maxLength": 254
          }
        },
        "required": [
          "email"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__verify",
      "description": "Verify an email domain. Resolve a public domain and report whether nameserver, address, and MX records were found. MX presence does not mean a mailbox exists. Docs: https://www.brainiac.software/api/email-domain/verify",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "minLength": 3,
            "maxLength": 254
          },
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__mx-record-check",
      "description": "Check MX records. Look up MX hosts, including a null MX, and resolve each public host. Missing records, lookup failures, and non-public hosts are reported separately. No message is sent. Docs: https://www.brainiac.software/api/email-domain/mx-record-check",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__spf-record-analyze",
      "description": "Analyze an SPF record. Read the published SPF policy and expand redirect or include targets for one level, up to eight lookups. +all is reported as a misconfiguration. Docs: https://www.brainiac.software/api/email-domain/spf-record-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__dkim-record-check",
      "description": "Check DKIM records. Look up DKIM public keys for the supplied selectors. When no selector is supplied, only google, selector1, selector2, s1, s2, and k1 are queried. Docs: https://www.brainiac.software/api/email-domain/dkim-record-check",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "selectors": {
            "minItems": 1,
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
            }
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__dmarc-policy-analyze",
      "description": "Analyze a DMARC policy. Read the _dmarc TXT record and report p and pct. A missing record, a failed lookup, and p=none are separate results. No aggregate report is sent. Docs: https://www.brainiac.software/api/email-domain/dmarc-policy-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__reputation-signals",
      "description": "Report domain registration signals. Return the RDAP registration date and whether a DNSSEC DS record is published. The reputation verdict stays unavailable because no unauthenticated reputation feed is queried. Docs: https://www.brainiac.software/api/email-domain/reputation-signals",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__registration-lookup",
      "description": "Look up domain registration. Read public RDAP data for the domain, including registrar, registration and expiration events, status, and nameservers. A not-found response is not proof the domain is unregistered everywhere. Docs: https://www.brainiac.software/api/email-domain/registration-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__tls-inspect",
      "description": "Inspect domain TLS. Connect to port 443 of a public address for the domain and read the certificate. Certificate transparency names come from public crt.sh results. No other port is contacted. Docs: https://www.brainiac.software/api/email-domain/tls-inspect",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          }
        },
        "required": [
          "domain"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "email-domain__deliverability-report",
      "description": "Report email deliverability checks. Combine syntax, MX, SPF, DKIM, DMARC, RDAP, and TLS checks. No message is sent, the mailbox is not checked, and a clear report does not promise delivery. Docs: https://www.brainiac.software/api/email-domain/deliverability-report",
      "parameters": {
        "type": "object",
        "properties": {
          "email": {
            "type": "string",
            "minLength": 3,
            "maxLength": 254
          },
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "selectors": {
            "minItems": 1,
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "email-domain__syntax-validate": "0.01",
  "email-domain__verify": "0.03",
  "email-domain__mx-record-check": "0.03",
  "email-domain__spf-record-analyze": "0.04",
  "email-domain__dkim-record-check": "0.04",
  "email-domain__dmarc-policy-analyze": "0.03",
  "email-domain__reputation-signals": "0.04",
  "email-domain__registration-lookup": "0.005",
  "email-domain__tls-inspect": "0.05",
  "email-domain__deliverability-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "email-domain__syntax-validate": "email-domain/syntax-validate",
  "email-domain__verify": "email-domain/verify",
  "email-domain__mx-record-check": "email-domain/mx-record-check",
  "email-domain__spf-record-analyze": "email-domain/spf-record-analyze",
  "email-domain__dkim-record-check": "email-domain/dkim-record-check",
  "email-domain__dmarc-policy-analyze": "email-domain/dmarc-policy-analyze",
  "email-domain__reputation-signals": "email-domain/reputation-signals",
  "email-domain__registration-lookup": "email-domain/registration-lookup",
  "email-domain__tls-inspect": "email-domain/tls-inspect",
  "email-domain__deliverability-report": "email-domain/deliverability-report"
}


class BrainiacEmailDomainAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — email-domain",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the email-domain catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "email-domain", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate email syntax"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.005",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the email-domain group. "
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
