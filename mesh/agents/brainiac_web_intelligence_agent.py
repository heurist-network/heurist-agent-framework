"""Auto-generated BRAINIAC Heurist Mesh agent for group `web-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "web-intelligence__url-to-markdown",
      "description": "Convert URL to Markdown. Fetch one public webpage and convert its readable HTML into Markdown, returning title, byline, excerpt, finalUrl, contentType, fetchedAt, and wordCount when present. Scripts are not run, and missing text is not filled in. Docs: https://www.brainiac.software/api/web-intelligence/url-to-markdown",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          }
        },
        "required": [
          "url"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-intelligence__structured-page-extract",
      "description": "Extract structured page data. Extract caller-defined fields from one public webpage. A field is returned only when a selector, JSON-LD property, or matching meta tag contains it. Otherwise the value is null. Docs: https://www.brainiac.software/api/web-intelligence/structured-page-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "schema": {
            "minItems": 1,
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "pattern": "^[A-Za-z][A-Za-z0-9_]{0,40}$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "string",
                    "number",
                    "boolean",
                    "url"
                  ]
                },
                "selector": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "attribute": {
                  "type": "string",
                  "pattern": "^[A-Za-z_:][A-Za-z0-9_:-]{0,40}$"
                }
              },
              "required": [
                "name",
                "type"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "url",
          "schema"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-intelligence__page-change-detect",
      "description": "Detect page changes. Fetch a public page and compare its Markdown with a caller-supplied previous snapshot. The snapshot is not stored. The result lists added and removed lines and does not rank their importance. Docs: https://www.brainiac.software/api/web-intelligence/page-change-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          },
          "previousMarkdown": {
            "type": "string",
            "maxLength": 200000
          },
          "previousRetrievedAt": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
          }
        },
        "required": [
          "url",
          "previousMarkdown"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-intelligence__website-metadata-extract",
      "description": "Extract website metadata. Read title, description, canonical URL, Open Graph tags, language, and robots directives from one public page. Absent tags are null. robots.txt is not fetched. Docs: https://www.brainiac.software/api/web-intelligence/website-metadata-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          }
        },
        "required": [
          "url"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-intelligence__website-contact-extract",
      "description": "Extract website contacts. Read publicly displayed emails, tel: links, address elements, and structured contact data from one public page. Linked pages are not crawled, and missing contacts are not guessed. Docs: https://www.brainiac.software/api/web-intelligence/website-contact-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          }
        },
        "required": [
          "url"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-intelligence__sitemap-content-index",
      "description": "Index sitemap content. Fetch one public sitemap or sitemap index and return the listed URLs with lastmod, changefreq, and priority when those fields are present. Page URLs are not fetched. Docs: https://www.brainiac.software/api/web-intelligence/sitemap-content-index",
      "parameters": {
        "type": "object",
        "properties": {
          "sitemapUrl": {
            "type": "string",
            "minLength": 8,
            "maxLength": 2000,
            "pattern": "^https?:\\/\\/\\S+$"
          }
        },
        "required": [
          "sitemapUrl"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "web-intelligence__url-to-markdown": "0.002",
  "web-intelligence__structured-page-extract": "0.003",
  "web-intelligence__page-change-detect": "0.05",
  "web-intelligence__website-metadata-extract": "0.002",
  "web-intelligence__website-contact-extract": "0.04",
  "web-intelligence__sitemap-content-index": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "web-intelligence__url-to-markdown": "web-intelligence/url-to-markdown",
  "web-intelligence__structured-page-extract": "web-intelligence/structured-page-extract",
  "web-intelligence__page-change-detect": "web-intelligence/page-change-detect",
  "web-intelligence__website-metadata-extract": "web-intelligence/website-metadata-extract",
  "web-intelligence__website-contact-extract": "web-intelligence/website-contact-extract",
  "web-intelligence__sitemap-content-index": "web-intelligence/sitemap-content-index"
}


class BrainiacWebIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — web-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the web-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "web-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Convert URL to Markdown"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.002",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the web-intelligence group. "
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
