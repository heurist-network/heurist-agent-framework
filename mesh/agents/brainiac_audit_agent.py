"""Auto-generated BRAINIAC Heurist Mesh agent for group `audit` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "audit__receipt",
      "description": "Create a hash-based audit receipt. Create a stateless SHA-256 digest of supplied inputs, findings, and source revision. It is not a trusted signature or legal attestation. Docs: https://www.brainiac.software/api/audit/receipt",
      "parameters": {
        "type": "object",
        "properties": {
          "product": {
            "type": "string",
            "enum": [
              "prevailing_wage",
              "coi",
              "exclusion",
              "license",
              "claims"
            ]
          },
          "inputs": {},
          "findings": {},
          "sourceRevision": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          }
        },
        "required": [
          "product",
          "inputs",
          "findings",
          "sourceRevision"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "audit__integrity-receipt",
      "description": "Issue a deterministic integrity receipt. Hash a caller-supplied evaluation and payload, repeat the caller-supplied timestamp, and score whether the declared fields and optional payload checksum are present. The same input always produces the same hash. The receipt is not a signature. Docs: https://www.brainiac.software/api/audit/integrity-receipt",
      "parameters": {
        "type": "object",
        "properties": {
          "evaluated_at": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$"
          },
          "evaluation": {
            "type": "object",
            "properties": {
              "subject": {
                "type": "string",
                "minLength": 3,
                "maxLength": 160
              },
              "operation": {
                "type": "string",
                "pattern": "^[a-z0-9]+(?:\\.[a-z0-9-]+){1,4}$"
              },
              "result": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "review"
                ]
              },
              "declared_fields": {
                "minItems": 1,
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^[a-z][a-z0-9_]{0,40}$"
                }
              }
            },
            "required": [
              "subject",
              "operation",
              "result"
            ],
            "additionalProperties": false
          },
          "payload": {},
          "payload_sha256": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$"
          }
        },
        "required": [
          "evaluated_at",
          "evaluation",
          "payload"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "audit__receipt": "0.01",
  "audit__integrity-receipt": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "audit__receipt": "audit/receipt",
  "audit__integrity-receipt": "audit/integrity-receipt"
}


class BrainiacAuditAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — audit",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the audit catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "audit", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Create a hash-based audit receipt"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the audit group. "
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
