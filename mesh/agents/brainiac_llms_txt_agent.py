"""Auto-generated BRAINIAC Heurist Mesh agent for group `llms-txt` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "llms-txt__structure-validate",
      "description": "Validate llms.txt structure. Check caller-supplied llms.txt text or structured JSON for one H1, a summary blockquote, H2 sections, and well-formed list links. URLs are not fetched. Docs: https://www.brainiac.software/api/llms-txt/structure-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
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
      "name": "llms-txt__link-quality-check",
      "description": "Check llms.txt link quality. Review link titles and descriptions in caller-supplied llms.txt content for generic labels and missing descriptions. Links are not opened. Docs: https://www.brainiac.software/api/llms-txt/link-quality-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
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
      "name": "llms-txt__context-budget-analyze",
      "description": "Analyze llms.txt context budget. Measure caller-supplied llms.txt size, repeated lines, and repeated link paths. The token figure is characters divided by four, not a model tokenizer. Docs: https://www.brainiac.software/api/llms-txt/context-budget-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
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
      "name": "llms-txt__coverage-analyze",
      "description": "Analyze llms.txt page coverage. Compare llms.txt link paths with a caller-supplied page list and report pages that have no matching link. Pages are not fetched, and an unmatched link is not treated as a missing site page. Docs: https://www.brainiac.software/api/llms-txt/coverage-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "pages": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "path": {
                  "type": "string",
                  "maxLength": 2000
                },
                "title": {
                  "type": "string",
                  "maxLength": 200
                }
              },
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
      "name": "llms-txt__navigation-analyze",
      "description": "Analyze llms.txt navigation. Find repeated link titles that point at different paths and generic section names in caller-supplied llms.txt content. No page is fetched. Docs: https://www.brainiac.software/api/llms-txt/navigation-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
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
      "name": "llms-txt__contradiction-detect",
      "description": "Detect llms.txt contradictions. Compare caller-supplied llms.txt text with caller-supplied documents for conflicting account, API key, price, and HTTP method statements. This is a phrase match, not a reading of intent. Docs: https://www.brainiac.software/api/llms-txt/contradiction-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "documents": {
            "minItems": 1,
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 100000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
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
      "name": "llms-txt__instruction-risk-scan",
      "description": "Scan llms.txt instruction risk. Look in caller-supplied llms.txt text for a fixed set of instruction-override phrases, script tags, hidden characters, and javascript links. Ordinary how-to steps are not flagged, and nothing is executed. Docs: https://www.brainiac.software/api/llms-txt/instruction-risk-scan",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "document": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string",
                "maxLength": 200
              },
              "summary": {
                "type": "string",
                "maxLength": 5000
              },
              "sections": {
                "maxItems": 50,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "links": {
                      "maxItems": 200,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "title": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "url": {
                            "type": "string",
                            "maxLength": 2000
                          },
                          "description": {
                            "type": "string",
                            "maxLength": 1000
                          }
                        },
                        "required": [
                          "title",
                          "url"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "name",
                    "links"
                  ],
                  "additionalProperties": false
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
      "name": "llms-txt__version-consistency",
      "description": "Check llms.txt version consistency. Compare caller-supplied llms.txt versions for /api/vN/ majors, summary semantic versions, updated dates, and link titles whose paths differ. Neither version is fetched. Docs: https://www.brainiac.software/api/llms-txt/version-consistency",
      "parameters": {
        "type": "object",
        "properties": {
          "versions": {
            "minItems": 2,
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "document": {
                  "type": "object",
                  "properties": {
                    "title": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "summary": {
                      "type": "string",
                      "maxLength": 5000
                    },
                    "sections": {
                      "maxItems": 50,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "maxLength": 200
                          },
                          "links": {
                            "maxItems": 200,
                            "type": "array",
                            "items": {
                              "type": "object",
                              "properties": {
                                "title": {
                                  "type": "string",
                                  "maxLength": 200
                                },
                                "url": {
                                  "type": "string",
                                  "maxLength": 2000
                                },
                                "description": {
                                  "type": "string",
                                  "maxLength": 1000
                                }
                              },
                              "required": [
                                "title",
                                "url"
                              ],
                              "additionalProperties": false
                            }
                          }
                        },
                        "required": [
                          "name",
                          "links"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "versions"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "llms-txt__structure-validate": "0.03",
  "llms-txt__link-quality-check": "0.03",
  "llms-txt__context-budget-analyze": "0.03",
  "llms-txt__coverage-analyze": "0.04",
  "llms-txt__navigation-analyze": "0.03",
  "llms-txt__contradiction-detect": "0.04",
  "llms-txt__instruction-risk-scan": "0.04",
  "llms-txt__version-consistency": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "llms-txt__structure-validate": "llms-txt/structure-validate",
  "llms-txt__link-quality-check": "llms-txt/link-quality-check",
  "llms-txt__context-budget-analyze": "llms-txt/context-budget-analyze",
  "llms-txt__coverage-analyze": "llms-txt/coverage-analyze",
  "llms-txt__navigation-analyze": "llms-txt/navigation-analyze",
  "llms-txt__contradiction-detect": "llms-txt/contradiction-detect",
  "llms-txt__instruction-risk-scan": "llms-txt/instruction-risk-scan",
  "llms-txt__version-consistency": "llms-txt/version-consistency"
}


class BrainiacLlmsTxtAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — llms-txt",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the llms-txt catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "llms-txt", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Validate llms.txt structure"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the llms-txt group. "
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
