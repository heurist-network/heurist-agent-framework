"""Auto-generated BRAINIAC Heurist Mesh agent for group `soap-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "soap-security__soap-security-policy-audit",
      "description": "Audit SOAP security policy. Compare WS-Policy and WS-SecurityPolicy assertions across caller-supplied WSDL 1.1 bindings and operations. audit_status is valid, warnings, policy_conflicts, invalid, or incomplete. risk_level is low, medium, high, or critical. A declared policy is not evidence that a server enforces it. Imports are not fetched. Docs: https://www.brainiac.software/api/soap-security/soap-security-policy-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "documents": {
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
                "role": {
                  "type": "string",
                  "enum": [
                    "wsdl",
                    "xsd",
                    "policy"
                  ]
                },
                "content": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 100000
                }
              },
              "required": [
                "name",
                "role",
                "content"
              ],
              "additionalProperties": false
            }
          },
          "expected": {
            "type": "object",
            "properties": {
              "token": {
                "type": "string",
                "enum": [
                  "username",
                  "x509",
                  "saml",
                  "issued",
                  "https",
                  "kerberos",
                  "secure_conversation",
                  "spnego"
                ]
              },
              "signBody": {
                "type": "boolean"
              },
              "encryptBody": {
                "type": "boolean"
              },
              "transport": {
                "type": "boolean"
              },
              "timestamp": {
                "type": "boolean"
              }
            },
            "additionalProperties": false
          },
          "selection": {
            "type": "object",
            "properties": {
              "service": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
              },
              "port": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
              },
              "binding": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
              },
              "operation": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "documents"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "soap-security__policy-strength",
      "description": "Score SOAP policy strength. Score a caller-supplied algorithm suite, body signature, body encryption, timestamp, and token kind. Basic256Sha256 contributes the most, TripleDes and None the least. A username token scores below an X.509 token. The grade follows that score. No certificate is validated and no policy file is fetched. Docs: https://www.brainiac.software/api/soap-security/policy-strength",
      "parameters": {
        "type": "object",
        "properties": {
          "algorithm_suite": {
            "type": "string",
            "enum": [
              "Basic256Sha256",
              "Basic256",
              "Basic128Sha256",
              "Basic128",
              "TripleDes",
              "None"
            ]
          },
          "body_signed": {
            "type": "boolean"
          },
          "body_encrypted": {
            "type": "boolean"
          },
          "timestamp": {
            "type": "boolean"
          },
          "token": {
            "type": "string",
            "enum": [
              "x509",
              "username",
              "none"
            ]
          }
        },
        "required": [
          "algorithm_suite",
          "body_signed",
          "body_encrypted",
          "timestamp",
          "token"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "soap-security__soap-security-policy-audit": "0.05",
  "soap-security__policy-strength": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "soap-security__soap-security-policy-audit": "soap-security/soap-security-policy-audit",
  "soap-security__policy-strength": "soap-security/policy-strength"
}


class BrainiacSoapSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — soap-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the soap-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "soap-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit SOAP security policy"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the soap-security group. "
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
