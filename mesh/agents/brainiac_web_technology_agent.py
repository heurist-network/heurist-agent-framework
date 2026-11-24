"""Auto-generated BRAINIAC Heurist Mesh agent for group `web-technology` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "web-technology__technology-detect",
      "description": "Detect web technologies. Detect CMS, frameworks, analytics, CDN and widgets from caller-supplied HTML, headers, cookies, scripts and meta with confidence and evidence. Docs: https://www.brainiac.software/api/web-technology/technology-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "maxLength": 2000
          },
          "html": {
            "type": "string",
            "maxLength": 2097152
          },
          "headers": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
            }
          },
          "cookies": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "domain": {
                  "type": "string"
                },
                "value": {
                  "type": "string"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "scriptUrls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "meta": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
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
      "name": "web-technology__js-library-vuln-detect",
      "description": "JS library vulnerability detect. Identify front-end JS libraries from script URLs or contents via Retire.js extractors and list known vulnerabilities. Docs: https://www.brainiac.software/api/web-technology/js-library-vuln-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "scripts": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "maxLength": 4000
                },
                "content": {
                  "type": "string",
                  "maxLength": 65536
                }
              },
              "additionalProperties": false
            }
          }
        },
        "required": [
          "scripts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__analytics-tag-inventory",
      "description": "Analytics tag inventory. Extract GA4, UA, GTM, Google Ads, Meta, LinkedIn, TikTok, Microsoft UET and Hotjar tag IDs from HTML. Docs: https://www.brainiac.software/api/web-technology/analytics-tag-inventory",
      "parameters": {
        "type": "object",
        "properties": {
          "html": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2097152
          }
        },
        "required": [
          "html"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__ecommerce-platform-detect",
      "description": "Ecommerce platform detect. Classify the ecommerce platform from technology detection results in the Ecommerce category. Docs: https://www.brainiac.software/api/web-technology/ecommerce-platform-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "maxLength": 2000
          },
          "html": {
            "type": "string",
            "maxLength": 2097152
          },
          "headers": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
            }
          },
          "cookies": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "domain": {
                  "type": "string"
                },
                "value": {
                  "type": "string"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "scriptUrls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "meta": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
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
      "name": "web-technology__payment-provider-detect",
      "description": "Payment provider detect. Detect payment processors and checkout widgets from the Payment processors technology category. Docs: https://www.brainiac.software/api/web-technology/payment-provider-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "maxLength": 2000
          },
          "html": {
            "type": "string",
            "maxLength": 2097152
          },
          "headers": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
            }
          },
          "cookies": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "domain": {
                  "type": "string"
                },
                "value": {
                  "type": "string"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "scriptUrls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "meta": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
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
      "name": "web-technology__tech-stack-diff",
      "description": "Technology stack diff. Diff two technology-detect results for added, removed and version-changed technologies. Docs: https://www.brainiac.software/api/web-technology/tech-stack-diff",
      "parameters": {
        "type": "object",
        "properties": {
          "before": {
            "type": "object",
            "properties": {
              "technologies": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "version": {
                      "type": [
                        "string",
                        "null"
                      ]
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "technologies"
            ],
            "additionalProperties": false
          },
          "after": {
            "type": "object",
            "properties": {
              "technologies": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "version": {
                      "type": [
                        "string",
                        "null"
                      ]
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "technologies"
            ],
            "additionalProperties": false
          },
          "beforeInput": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 2000
              },
              "html": {
                "type": "string",
                "maxLength": 2097152
              },
              "headers": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "string"
                }
              },
              "cookies": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "domain": {
                      "type": "string"
                    },
                    "value": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "scriptUrls": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "meta": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "string"
                }
              }
            },
            "additionalProperties": false
          },
          "afterInput": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 2000
              },
              "html": {
                "type": "string",
                "maxLength": 2097152
              },
              "headers": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "string"
                }
              },
              "cookies": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "domain": {
                      "type": "string"
                    },
                    "value": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "scriptUrls": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "meta": {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "type": "string"
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
      "name": "web-technology__tcf-consent-string-decode",
      "description": "Decode IAB TCF v2 TC string. Decode an IAB Europe TCF v2.x transparency and consent string into purposes, vendors and publisher restrictions. Docs: https://www.brainiac.software/api/web-technology/tcf-consent-string-decode",
      "parameters": {
        "type": "object",
        "properties": {
          "tcString": {
            "type": "string",
            "minLength": 1,
            "maxLength": 10000
          }
        },
        "required": [
          "tcString"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__ads-txt-validate",
      "description": "Validate ads.txt / app-ads.txt. Validate ads.txt records and variables, optionally cross-checking DIRECT seller IDs against sellers.json. Docs: https://www.brainiac.software/api/web-technology/ads-txt-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "adsTxt": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500000
          },
          "sellersJson": {
            "type": "object",
            "properties": {
              "sellers": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "seller_id": {
                      "type": "string"
                    },
                    "domain": {
                      "type": "string"
                    },
                    "seller_type": {
                      "type": "string"
                    },
                    "name": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "seller_id"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "sellers"
            ],
            "additionalProperties": false
          },
          "ownDomain": {
            "type": "string"
          }
        },
        "required": [
          "adsTxt"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__security-txt-validate",
      "description": "Validate security.txt (RFC 9116). Validate security.txt Contact/Expires and optional fields per RFC 9116, including expiry and Canonical checks. Docs: https://www.brainiac.software/api/web-technology/security-txt-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100000
          },
          "servedAt": {
            "type": "string",
            "format": "uri"
          },
          "now": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z))$"
          }
        },
        "required": [
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__web-manifest-audit",
      "description": "Web app manifest audit. Validate a web app manifest against W3C installability checks for start_url, scope, display and icons. Docs: https://www.brainiac.software/api/web-technology/web-manifest-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "manifest": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {}
          },
          "manifestUrl": {
            "type": "string",
            "format": "uri"
          },
          "documentUrl": {
            "type": "string",
            "format": "uri"
          }
        },
        "required": [
          "manifest",
          "manifestUrl",
          "documentUrl"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__favicon-hash",
      "description": "Favicon MurmurHash3 / SHA-256. Compute Shodan-style MurmurHash3 and SHA-256 of a favicon from raw base64 bytes. Docs: https://www.brainiac.software/api/web-technology/favicon-hash",
      "parameters": {
        "type": "object",
        "properties": {
          "faviconBase64": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1398202
          }
        },
        "required": [
          "faviconBase64"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__user-agent-parse",
      "description": "Parse User-Agent and Client Hints. Parse a User-Agent with uap-core patterns into browser, OS and device, optionally overriding with Client Hints. Docs: https://www.brainiac.software/api/web-technology/user-agent-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "userAgent": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2000
          },
          "clientHints": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "type": "string"
            }
          }
        },
        "required": [
          "userAgent"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__crawler-identify",
      "description": "Identify crawlers and Googlebot IPs. Match crawler-user-agents patterns and optionally verify Googlebot IPs against vendored Googlebot CIDR ranges. Docs: https://www.brainiac.software/api/web-technology/crawler-identify",
      "parameters": {
        "type": "object",
        "properties": {
          "userAgent": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2000
          },
          "ip": {
            "type": "string"
          }
        },
        "required": [
          "userAgent"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "web-technology__cookie-inventory-classify",
      "description": "Classify cookies via Open Cookie Database. Categorise cookies using exact and wildcard matches against the Open Cookie Database. Docs: https://www.brainiac.software/api/web-technology/cookie-inventory-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "cookies": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1
                },
                "domain": {
                  "type": "string"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "cookies"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "web-technology__technology-detect": "0.04",
  "web-technology__js-library-vuln-detect": "0.04",
  "web-technology__analytics-tag-inventory": "0.02",
  "web-technology__ecommerce-platform-detect": "0.03",
  "web-technology__payment-provider-detect": "0.03",
  "web-technology__tech-stack-diff": "0.02",
  "web-technology__tcf-consent-string-decode": "0.03",
  "web-technology__ads-txt-validate": "0.02",
  "web-technology__security-txt-validate": "0.02",
  "web-technology__web-manifest-audit": "0.02",
  "web-technology__favicon-hash": "0.01",
  "web-technology__user-agent-parse": "0.02",
  "web-technology__crawler-identify": "0.02",
  "web-technology__cookie-inventory-classify": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "web-technology__technology-detect": "web-technology/technology-detect",
  "web-technology__js-library-vuln-detect": "web-technology/js-library-vuln-detect",
  "web-technology__analytics-tag-inventory": "web-technology/analytics-tag-inventory",
  "web-technology__ecommerce-platform-detect": "web-technology/ecommerce-platform-detect",
  "web-technology__payment-provider-detect": "web-technology/payment-provider-detect",
  "web-technology__tech-stack-diff": "web-technology/tech-stack-diff",
  "web-technology__tcf-consent-string-decode": "web-technology/tcf-consent-string-decode",
  "web-technology__ads-txt-validate": "web-technology/ads-txt-validate",
  "web-technology__security-txt-validate": "web-technology/security-txt-validate",
  "web-technology__web-manifest-audit": "web-technology/web-manifest-audit",
  "web-technology__favicon-hash": "web-technology/favicon-hash",
  "web-technology__user-agent-parse": "web-technology/user-agent-parse",
  "web-technology__crawler-identify": "web-technology/crawler-identify",
  "web-technology__cookie-inventory-classify": "web-technology/cookie-inventory-classify"
}


class BrainiacWebTechnologyAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — web-technology",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the web-technology catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "web-technology", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect web technologies"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the web-technology group. "
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
