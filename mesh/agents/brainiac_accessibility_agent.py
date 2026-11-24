"""Auto-generated BRAINIAC Heurist Mesh agent for group `accessibility` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "accessibility__html-audit",
      "description": "Audit HTML accessibility. Run the static image, heading, form, link, language, keyboard, ARIA, and inline-contrast checks. The result is not a WCAG conformance claim. Docs: https://www.brainiac.software/api/accessibility/html-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__image-alt-text-audit",
      "description": "Audit image alt text. Flag images, image inputs, and areas with no alt attribute. An empty alt is reported as a manual check, not as a confirmed failure. Docs: https://www.brainiac.software/api/accessibility/image-alt-text-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__heading-structure-audit",
      "description": "Audit heading structure. Read heading elements in source order and flag empty headings and skipped levels. A missing h1 is a potential issue, not a confirmed failure. Docs: https://www.brainiac.software/api/accessibility/heading-structure-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__form-audit",
      "description": "Audit form accessibility. Check that controls have a label, an aria-label, or a matching label element. A placeholder or title is not treated as a sufficient name. Docs: https://www.brainiac.software/api/accessibility/form-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__link-audit",
      "description": "Audit link accessibility. Flag links with no accessible name. Generic text such as click here is a potential issue because the surrounding sentence was not judged. Docs: https://www.brainiac.software/api/accessibility/link-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__document-language-check",
      "description": "Check document language. Read the lang attribute on the html element. The page text is not compared with that value, and a fragment without html is not marked as a failure. Docs: https://www.brainiac.software/api/accessibility/document-language-check",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__keyboard-signals",
      "description": "Check keyboard signals. Flag a positive tabindex and an onclick on a non-control. Keys are not pressed, so keyboard operation stays a manual check. Docs: https://www.brainiac.software/api/accessibility/keyboard-signals",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__aria-attribute-audit",
      "description": "Audit ARIA attributes. Check roles, boolean ARIA values, and references to ids that exist in this HTML. Runtime ARIA state changes are not tested. Docs: https://www.brainiac.software/api/accessibility/aria-attribute-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__color-contrast-check",
      "description": "Check inline colour contrast. Calculate a contrast ratio only when both colours are opaque values on the same element. A single colour is not compared with an assumed background. Docs: https://www.brainiac.software/api/accessibility/color-contrast-check",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "accessibility__remediation-report",
      "description": "Report accessibility remediation. Combine the static checks and list confirmed issues before potential issues and manual checks. The report does not claim WCAG conformance. Docs: https://www.brainiac.software/api/accessibility/remediation-report",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "accessibility__html-audit": "0.05",
  "accessibility__image-alt-text-audit": "0.03",
  "accessibility__heading-structure-audit": "0.03",
  "accessibility__form-audit": "0.04",
  "accessibility__link-audit": "0.03",
  "accessibility__document-language-check": "0.02",
  "accessibility__keyboard-signals": "0.04",
  "accessibility__aria-attribute-audit": "0.04",
  "accessibility__color-contrast-check": "0.04",
  "accessibility__remediation-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "accessibility__html-audit": "accessibility/html-audit",
  "accessibility__image-alt-text-audit": "accessibility/image-alt-text-audit",
  "accessibility__heading-structure-audit": "accessibility/heading-structure-audit",
  "accessibility__form-audit": "accessibility/form-audit",
  "accessibility__link-audit": "accessibility/link-audit",
  "accessibility__document-language-check": "accessibility/document-language-check",
  "accessibility__keyboard-signals": "accessibility/keyboard-signals",
  "accessibility__aria-attribute-audit": "accessibility/aria-attribute-audit",
  "accessibility__color-contrast-check": "accessibility/color-contrast-check",
  "accessibility__remediation-report": "accessibility/remediation-report"
}


class BrainiacAccessibilityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — accessibility",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the accessibility catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "accessibility", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit HTML accessibility"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the accessibility group. "
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
