"""Auto-generated BRAINIAC Heurist Mesh agent for group `account-abstraction` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "account-abstraction__paymaster-sponsorship-audit",
      "description": "Audit paymaster sponsorship. Compare ERC-4337 UserOperations with a caller-supplied Paymaster sponsorship policy. EntryPoint versions are 0.6 and 0.7. An omitted paymasterDataFormat is envelope: the EntryPoint address and, on 0.7, the two 16-byte gas limits are read, and later bytes stay opaque. verifying_paymaster also reads validUntil and validAfter as two 6-byte integers; a validUntil of 0 means no upper bound, and the signature is not verified. Call targets and selectors are read only from declared values, raw calldata offsets, or execute(address,uint256,bytes). audit_status is allowed, denied, warnings, invalid, or indeterminate. risk_level is low, medium, high, or critical. Sponsored gas is the EntryPoint required-prefund sum, multiplied by maxFeePerGas for the amount in wei. No Paymaster deposit, balance, reputation, or other chain state is read, and the result does not say whether a bundler will accept the operation. Docs: https://www.brainiac.software/api/account-abstraction/paymaster-sponsorship-aud",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "account-abstraction__sponsorship-risk",
      "description": "Score paymaster sponsorship risk. Add the caller-supplied call gas and verification gas, multiply by the max fee, and compare that cost with the paymaster deposit. Gas above the stated ceilings, and init code when it is not allowed, raise the risk score. The safety index is how far each gas field sits inside its ceiling. No deposit is read from a chain. Docs: https://www.brainiac.software/api/account-abstraction/sponsorship-risk",
      "parameters": {
        "type": "object",
        "properties": {
          "deposit_wei": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "max_fee_per_gas": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "max_call_gas": {
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 30000000
          },
          "max_verification_gas": {
            "type": "integer",
            "minimum": 0,
            "maximum": 30000000
          },
          "allow_init_code": {
            "type": "boolean"
          },
          "user_operations": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "call_gas_limit": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 30000000
                },
                "verification_gas_limit": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 30000000
                },
                "init_code": {
                  "type": "string",
                  "maxLength": 20000,
                  "pattern": "^0x[0-9a-fA-F]*$"
                }
              },
              "required": [
                "call_gas_limit",
                "verification_gas_limit"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "deposit_wei",
          "max_fee_per_gas",
          "max_call_gas",
          "max_verification_gas",
          "allow_init_code",
          "user_operations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "account-abstraction__user-operation-audit",
      "description": "Audit user operation. Check the structure of one ERC-4337 UserOperation before it is submitted to a bundler. EntryPoint 0.6 uses initCode and paymasterAndData. EntryPoint 0.7 uses factory, factoryData, and separate Paymaster fields. On 0.7, callGasLimit, verificationGasLimit, the fee fields, and Paymaster gas limits must fit in uint128. Calldata is decoded only with the supplied ABI. Expected targets are compared only with decoded address parameters named dest, target, or to. validation_status is valid, invalid, warnings, or indeterminate. risk_level is low, medium, high, or critical. The signature is not recovered. No chain state is read, execution is not simulated, and the result does not say whether a bundler will accept the operation. Docs: https://www.brainiac.software/api/account-abstraction/user-operation-audit",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "account-abstraction__user-op-validity",
      "description": "Score UserOperation format. Check a caller-supplied nonce, signature length, init code, and calldata length. A signature of 64 or 65 bytes passes the length check and is not recovered. init code of at least 20 bytes is a factory deployment and is not simulated. The rejection index counts format problems. It does not say whether a bundler will accept the operation. Docs: https://www.brainiac.software/api/account-abstraction/user-op-validity",
      "parameters": {
        "type": "object",
        "properties": {
          "sender": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "nonce": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "expected_nonce": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "signature": {
            "type": "string",
            "maxLength": 1000,
            "pattern": "^0x[0-9a-fA-F]*$"
          },
          "init_code": {
            "type": "string",
            "maxLength": 20000,
            "pattern": "^0x[0-9a-fA-F]*$"
          },
          "call_data": {
            "type": "string",
            "maxLength": 20000,
            "pattern": "^0x[0-9a-fA-F]*$"
          }
        },
        "required": [
          "sender",
          "nonce",
          "signature",
          "init_code",
          "call_data"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "account-abstraction__paymaster-sponsorship-audit": "0.05",
  "account-abstraction__sponsorship-risk": "0.04",
  "account-abstraction__user-operation-audit": "0.05",
  "account-abstraction__user-op-validity": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "account-abstraction__paymaster-sponsorship-audit": "account-abstraction/paymaster-sponsorship-audit",
  "account-abstraction__sponsorship-risk": "account-abstraction/sponsorship-risk",
  "account-abstraction__user-operation-audit": "account-abstraction/user-operation-audit",
  "account-abstraction__user-op-validity": "account-abstraction/user-op-validity"
}


class BrainiacAccountAbstractionAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — account-abstraction",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the account-abstraction catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "account-abstraction", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit paymaster sponsorship"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the account-abstraction group. "
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
