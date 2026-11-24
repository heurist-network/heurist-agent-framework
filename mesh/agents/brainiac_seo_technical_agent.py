"""Auto-generated BRAINIAC Heurist Mesh agent for group `seo-technical` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "seo-technical__robots-txt-test",
      "description": "Test URLs against robots.txt. Evaluate path access for a user-agent against a caller-supplied robots.txt using RFC 9309 longest-match rules. Docs: https://www.brainiac.software/api/seo-technical/robots-txt-test",
      "parameters": {
        "type": "object",
        "properties": {
          "robotsTxt": {
            "type": "string",
            "maxLength": 512000
          },
          "userAgent": {
            "type": "string",
            "minLength": 1,
            "maxLength": 256
          },
          "urls": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          }
        },
        "required": [
          "robotsTxt",
          "userAgent",
          "urls"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__xml-sitemap-validate",
      "description": "Validate a sitemap or sitemap index. Check sitemap URL counts, absolute locs, lastmod/changefreq/priority and size limits against the sitemaps.org protocol. Docs: https://www.brainiac.software/api/seo-technical/xml-sitemap-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "xml": {
            "type": "string",
            "maxLength": 55000000
          },
          "gzipBase64": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 55000000
              },
              {
                "type": "null"
              }
            ]
          },
          "sitemapUrl": {
            "type": "string",
            "format": "uri"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__hreflang-validate",
      "description": "Validate an hreflang cluster. Check BCP 47 codes against the IANA subtag registry and reciprocal return tags across caller-supplied page alternates. Docs: https://www.brainiac.software/api/seo-technical/hreflang-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "pages": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "canonical": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "alternates": {
                  "maxItems": 500,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "hreflang": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64
                      },
                      "href": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4096
                      }
                    },
                    "required": [
                      "hreflang",
                      "href"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "url",
                "alternates"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "pages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__canonical-audit",
      "description": "Audit canonical tags in a crawl export. Find missing, multiple, chained, redirecting and noindex canonical targets inside a caller-supplied crawl export. Docs: https://www.brainiac.software/api/seo-technical/canonical-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "pages": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "status": {
                  "type": "integer",
                  "minimum": 100,
                  "maximum": 599
                },
                "canonicals": {
                  "default": [],
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 4096
                  }
                },
                "noindex": {
                  "default": false,
                  "type": "boolean"
                },
                "redirectTo": {
                  "anyOf": [
                    {
                      "type": "string",
                      "maxLength": 4096
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "url",
                "status"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "pages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__redirect-chain-analyze",
      "description": "Analyse redirect chains and loops. Walk caller-supplied redirect hops for chains, loops, mixed permanent/temporary statuses and HTTPS-to-HTTP downgrades. Docs: https://www.brainiac.software/api/seo-technical/redirect-chain-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "hops": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "to": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "status": {
                  "type": "integer",
                  "minimum": 300,
                  "maximum": 399
                }
              },
              "required": [
                "from",
                "to",
                "status"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "hops"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__internal-link-graph",
      "description": "Internal PageRank and click depth. Compute PageRank, in/out degree and BFS click depth from caller-supplied internal link edges. Docs: https://www.brainiac.software/api/seo-technical/internal-link-graph",
      "parameters": {
        "type": "object",
        "properties": {
          "edges": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "to": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "nofollow": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "from",
                "to"
              ],
              "additionalProperties": false
            }
          },
          "start": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4096
          },
          "damping": {
            "default": 0.85,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "excludeNofollow": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "edges",
          "start"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__orphan-page-detect",
      "description": "Detect orphan and unsitemap pages. Compare normalised sitemap, crawl and analytics URL sets to find orphans, missing sitemap entries and no-traffic pages. Docs: https://www.brainiac.software/api/seo-technical/orphan-page-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "sitemapUrls": {
            "default": [],
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "crawledUrls": {
            "default": [],
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "analyticsUrls": {
            "default": [],
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "ignoreTrailingSlash": {
            "default": true,
            "type": "boolean"
          },
          "stripParams": {
            "default": [
              "utm_*",
              "gclid",
              "fbclid",
              "msclkid"
            ],
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
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
      "name": "seo-technical__schema-org-validate",
      "description": "Validate JSON-LD against schema.org. Check JSON-LD types and properties against a vendored schema.org Product/Offer vocabulary subset. Docs: https://www.brainiac.software/api/seo-technical/schema-org-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "jsonld": {
            "anyOf": [
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              },
              {
                "type": "array",
                "items": {}
              }
            ]
          }
        },
        "required": [
          "jsonld"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__log-file-bot-analyze",
      "description": "Analyse crawler hits in an access log. Classify bot user-agents in Combined or W3C logs and verify Googlebot hits against vendored IP ranges. Docs: https://www.brainiac.software/api/seo-technical/log-file-bot-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "log": {
            "type": "string",
            "maxLength": 52428800
          },
          "format": {
            "default": "combined",
            "type": "string",
            "enum": [
              "combined",
              "w3c"
            ]
          },
          "directoryDepth": {
            "default": 1,
            "type": "integer",
            "minimum": 0,
            "maximum": 20
          }
        },
        "required": [
          "log"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__crawl-depth-analyze",
      "description": "Click-depth distribution from link edges. Multi-source BFS depth distribution with too-deep important URLs and unreachable nodes from caller edges. Docs: https://www.brainiac.software/api/seo-technical/crawl-depth-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "edges": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "to": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                }
              },
              "required": [
                "from",
                "to"
              ],
              "additionalProperties": false
            }
          },
          "startUrls": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "important": {
            "default": [],
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "maxDepth": {
            "default": 3,
            "type": "integer",
            "minimum": 0,
            "maximum": 100
          }
        },
        "required": [
          "edges",
          "startUrls"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__url-parameter-audit",
      "description": "Audit URL parameter explosion. Find parameter usage, tracking params and duplicate-content URL groups from a caller-supplied URL list. Docs: https://www.brainiac.software/api/seo-technical/url-parameter-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "urls": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4096
            }
          },
          "trackingParams": {
            "default": [
              "utm_source",
              "utm_medium",
              "utm_campaign",
              "utm_term",
              "utm_content",
              "gclid",
              "fbclid",
              "msclkid"
            ],
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          }
        },
        "required": [
          "urls"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__backlink-anchor-profile",
      "description": "Backlink anchor and referring-domain profile. Classify anchors, rel shares and referring-domain concentration (HHI) from a caller backlink export. Docs: https://www.brainiac.software/api/seo-technical/backlink-anchor-profile",
      "parameters": {
        "type": "object",
        "properties": {
          "links": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "source": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "target": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "anchor": {
                  "default": "",
                  "type": "string",
                  "maxLength": 2048
                },
                "rel": {
                  "type": "string",
                  "maxLength": 256
                }
              },
              "required": [
                "source",
                "target"
              ],
              "additionalProperties": false
            }
          },
          "brandTerms": {
            "default": [],
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 128
            }
          },
          "moneyKeywords": {
            "default": [],
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            }
          }
        },
        "required": [
          "links"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__disavow-file-build",
      "description": "Build or validate a Google disavow file. Validate domain: and URL entries, dedupe, and emit a Google Search Console disavow .txt within documented limits. Docs: https://www.brainiac.software/api/seo-technical/disavow-file-build",
      "parameters": {
        "type": "object",
        "properties": {
          "entries": {
            "default": [],
            "maxItems": 100100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 2200
            }
          },
          "existingFile": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 2097152
              },
              {
                "type": "null"
              }
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
      "name": "seo-technical__core-web-vitals-assess",
      "description": "Rate p75 Core Web Vitals. Rate caller-supplied p75 LCP/INP/CLS/FCP/TTFB against web.dev thresholds and rank URL groups by failing CWV. Docs: https://www.brainiac.software/api/seo-technical/core-web-vitals-assess",
      "parameters": {
        "type": "object",
        "properties": {
          "groups": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 256
                },
                "device": {
                  "default": "mobile",
                  "type": "string",
                  "enum": [
                    "mobile",
                    "desktop"
                  ]
                },
                "p75": {
                  "type": "object",
                  "properties": {
                    "lcpMs": {
                      "type": "number"
                    },
                    "inpMs": {
                      "type": "number"
                    },
                    "cls": {
                      "type": "number"
                    },
                    "fcpMs": {
                      "type": "number"
                    },
                    "ttfbMs": {
                      "type": "number"
                    },
                    "fidMs": {
                      "type": "number"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "name",
                "p75"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "groups"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-technical__keyword-cannibalization-detect",
      "description": "Detect keyword cannibalization. Find Search Console queries where multiple pages compete on impressions and estimate lost clicks. Docs: https://www.brainiac.software/api/seo-technical/keyword-cannibalization-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "rows": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "query": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 512
                },
                "page": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4096
                },
                "clicks": {
                  "type": "number",
                  "minimum": 0
                },
                "impressions": {
                  "type": "number",
                  "minimum": 0
                },
                "position": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "query",
                "page",
                "clicks",
                "impressions",
                "position"
              ],
              "additionalProperties": false
            }
          },
          "minImpressions": {
            "default": 100,
            "type": "number",
            "minimum": 0
          },
          "brandTerms": {
            "default": [],
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 128
            }
          },
          "minShare": {
            "default": 0.1,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "rows"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "seo-technical__robots-txt-test": "0.02",
  "seo-technical__xml-sitemap-validate": "0.03",
  "seo-technical__hreflang-validate": "0.03",
  "seo-technical__canonical-audit": "0.03",
  "seo-technical__redirect-chain-analyze": "0.02",
  "seo-technical__internal-link-graph": "0.04",
  "seo-technical__orphan-page-detect": "0.02",
  "seo-technical__schema-org-validate": "0.03",
  "seo-technical__log-file-bot-analyze": "0.04",
  "seo-technical__crawl-depth-analyze": "0.03",
  "seo-technical__url-parameter-audit": "0.02",
  "seo-technical__backlink-anchor-profile": "0.03",
  "seo-technical__disavow-file-build": "0.02",
  "seo-technical__core-web-vitals-assess": "0.02",
  "seo-technical__keyword-cannibalization-detect": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "seo-technical__robots-txt-test": "seo-technical/robots-txt-test",
  "seo-technical__xml-sitemap-validate": "seo-technical/xml-sitemap-validate",
  "seo-technical__hreflang-validate": "seo-technical/hreflang-validate",
  "seo-technical__canonical-audit": "seo-technical/canonical-audit",
  "seo-technical__redirect-chain-analyze": "seo-technical/redirect-chain-analyze",
  "seo-technical__internal-link-graph": "seo-technical/internal-link-graph",
  "seo-technical__orphan-page-detect": "seo-technical/orphan-page-detect",
  "seo-technical__schema-org-validate": "seo-technical/schema-org-validate",
  "seo-technical__log-file-bot-analyze": "seo-technical/log-file-bot-analyze",
  "seo-technical__crawl-depth-analyze": "seo-technical/crawl-depth-analyze",
  "seo-technical__url-parameter-audit": "seo-technical/url-parameter-audit",
  "seo-technical__backlink-anchor-profile": "seo-technical/backlink-anchor-profile",
  "seo-technical__disavow-file-build": "seo-technical/disavow-file-build",
  "seo-technical__core-web-vitals-assess": "seo-technical/core-web-vitals-assess",
  "seo-technical__keyword-cannibalization-detect": "seo-technical/keyword-cannibalization-detect"
}


class BrainiacSeoTechnicalAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — seo-technical",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the seo-technical catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "seo-technical", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Test URLs against robots.txt"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the seo-technical group. "
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
