"""Auto-generated BRAINIAC Heurist Mesh agent for group `document-formats` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "document-formats__en16931-invoice-validate",
      "description": "Validate EN 16931 electronic invoices. Validate UBL or CII e-invoices against CEN EN 16931 artefacts 1.3.17 (and UBL 2.1 XSD). Docs: https://www.brainiac.software/api/document-formats/en16931-invoice-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "xml": {
            "type": "string",
            "maxLength": 5000000
          },
          "pdfBase64": {
            "type": "string",
            "maxLength": 13981077
          },
          "syntax": {
            "default": "auto",
            "type": "string",
            "enum": [
              "auto",
              "ubl",
              "cii"
            ]
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "document-formats__fhir-resource-validate",
      "description": "Validate FHIR JSON resources. Validate a FHIR resource against the official HL7 JSON Schema for R4 or R5. Docs: https://www.brainiac.software/api/document-formats/fhir-resource-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "resource": {
            "anyOf": [
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              },
              {
                "type": "string",
                "maxLength": 2000000
              }
            ]
          },
          "version": {
            "default": "R4",
            "type": "string",
            "enum": [
              "R4",
              "R5"
            ]
          }
        },
        "required": [
          "resource"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "document-formats__mrz-parse-checkdigits",
      "description": "Parse MRZ and verify check digits. Parse TD1/TD2/TD3 machine-readable zones and verify ICAO Doc 9303 check digits. Docs: https://www.brainiac.software/api/document-formats/mrz-parse-checkdigits",
      "parameters": {
        "type": "object",
        "properties": {
          "mrz": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 20,
                "maxLength": 200
              },
              {
                "minItems": 2,
                "maxItems": 3,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 20,
                  "maxLength": 50
                }
              }
            ]
          }
        },
        "required": [
          "mrz"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "document-formats__epc-swiss-qr-bill-parse",
      "description": "Parse EPC GiroCode and Swiss QR-bill payloads. Parse SEPA EPC069-12 or Swiss QR-bill SPC text into structured payment fields. Docs: https://www.brainiac.software/api/document-formats/epc-swiss-qr-bill-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {
            "type": "string",
            "minLength": 3,
            "maxLength": 1000
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
      "name": "document-formats__pdf-table-extract",
      "description": "Extract tables from a text PDF. Extract bordered or whitespace-aligned tables from a caller-supplied PDF (no OCR). Docs: https://www.brainiac.software/api/document-formats/pdf-table-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "pdfBase64": {
            "type": "string",
            "minLength": 16,
            "maxLength": 20971584
          },
          "pages": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "integer",
              "exclusiveMinimum": 0,
              "maximum": 9007199254740991
            }
          },
          "mode": {
            "default": "auto",
            "type": "string",
            "enum": [
              "auto",
              "lattice",
              "stream"
            ]
          }
        },
        "required": [
          "pdfBase64"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "document-formats__barcode-decode",
      "description": "Decode barcodes from an image. Decode 1D/2D barcodes (QR, Data Matrix, PDF417, Code 128, EAN, …) from a PNG/JPEG/WebP/GIF. Docs: https://www.brainiac.software/api/document-formats/barcode-decode",
      "parameters": {
        "type": "object",
        "properties": {
          "imageBase64": {
            "type": "string",
            "minLength": 16,
            "maxLength": 13981077
          },
          "formats": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "tryHarder": {
            "default": true,
            "type": "boolean"
          },
          "maxResults": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 20
          }
        },
        "required": [
          "imageBase64"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "document-formats__en16931-invoice-validate": "0.05",
  "document-formats__fhir-resource-validate": "0.02",
  "document-formats__mrz-parse-checkdigits": "0.01",
  "document-formats__epc-swiss-qr-bill-parse": "0.02",
  "document-formats__pdf-table-extract": "0.04",
  "document-formats__barcode-decode": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "document-formats__en16931-invoice-validate": "document-formats/en16931-invoice-validate",
  "document-formats__fhir-resource-validate": "document-formats/fhir-resource-validate",
  "document-formats__mrz-parse-checkdigits": "document-formats/mrz-parse-checkdigits",
  "document-formats__epc-swiss-qr-bill-parse": "document-formats/epc-swiss-qr-bill-parse",
  "document-formats__pdf-table-extract": "document-formats/pdf-table-extract",
  "document-formats__barcode-decode": "document-formats/barcode-decode"
}


class BrainiacDocumentFormatsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — document-formats",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the document-formats catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "document-formats", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate EN 16931 electronic invoices"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the document-formats group. "
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
