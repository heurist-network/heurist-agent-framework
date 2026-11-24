"""Auto-generated BRAINIAC Heurist Mesh agent for group `seo-content` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "seo-content__tfidf-term-gap",
      "description": "TF-IDF term gap vs competitor pages. Find stemmed terms common among competitor pages but missing or under-used in a draft, ranked by TF-IDF gap. Docs: https://www.brainiac.software/api/seo-content/tfidf-term-gap",
      "parameters": {
        "type": "object",
        "properties": {
          "draft": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "competitors": {
            "minItems": 2,
            "maxItems": 50,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200000
                },
                {
                  "type": "object",
                  "properties": {
                    "url": {
                      "type": "string"
                    },
                    "html": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200000
                    },
                    "text": {
                      "type": "string",
                      "maxLength": 200000
                    }
                  },
                  "required": [
                    "html"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "language": {
            "default": "en",
            "type": "string"
          },
          "minDocFrequency": {
            "default": 2,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "limit": {
            "default": 50,
            "type": "integer",
            "minimum": 1,
            "maximum": 200
          }
        },
        "required": [
          "draft",
          "competitors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__brief-from-serp-texts",
      "description": "Content brief from SERP page texts. Build a content brief from caller-supplied top-ranking HTML: common headings, word-count target, questions and recommended TF-IDF terms. Docs: https://www.brainiac.software/api/seo-content/brief-from-serp-texts",
      "parameters": {
        "type": "object",
        "properties": {
          "pages": {
            "minItems": 2,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1
                },
                "html": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200000
                }
              },
              "required": [
                "url",
                "html"
              ],
              "additionalProperties": false
            }
          },
          "language": {
            "default": "en",
            "type": "string"
          },
          "minHeadingShare": {
            "default": 0.5,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "termLimit": {
            "default": 30,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
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
      "name": "seo-content__readability-score",
      "description": "English readability metrics. Compute Flesch Reading Ease, Flesch-Kincaid, Gunning Fog, SMOG and Coleman-Liau from caller text. Docs: https://www.brainiac.software/api/seo-content/readability-score",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "language": {
            "default": "en",
            "type": "string"
          }
        },
        "required": [
          "text"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__near-duplicate-detect",
      "description": "Near-duplicate page clustering. Cluster near-duplicate pages with Jaccard similarity on token shingles and connected-component clustering. Docs: https://www.brainiac.software/api/seo-content/near-duplicate-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "pages": {
            "minItems": 2,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "html": {
                  "type": "string",
                  "maxLength": 200000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "shingleSize": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 10
          },
          "threshold": {
            "default": 0.8,
            "type": "number",
            "minimum": 0,
            "maximum": 1
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
      "name": "seo-content__internal-link-suggest",
      "description": "Internal link suggestions. Suggest internal links by unigram TF-IDF cosine similarity and extract exact or partial anchor text from target keywords. Docs: https://www.brainiac.software/api/seo-content/internal-link-suggest",
      "parameters": {
        "type": "object",
        "properties": {
          "pages": {
            "minItems": 2,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "html": {
                  "type": "string",
                  "maxLength": 200000
                },
                "targetKeywords": {
                  "default": [],
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "existingLinks": {
            "default": [],
            "type": "array",
            "items": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "string"
                },
                {
                  "type": "string"
                }
              ],
              "items": false,
              "minItems": 2,
              "maxItems": 2
            }
          },
          "minSimilarity": {
            "default": 0.2,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "maxPerSource": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
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
      "name": "seo-content__keyword-intent-classify",
      "description": "Rule-based keyword intent labels. Label keywords as navigational, transactional, commercial or informational from bundled English modifier rules and caller brands. Docs: https://www.brainiac.software/api/seo-content/keyword-intent-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "keywords": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "brands": {
            "default": [],
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "language": {
            "default": "en",
            "type": "string"
          }
        },
        "required": [
          "keywords"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__keyword-group-lexical",
      "description": "Lexical keyword grouping. Group keywords that share the same Porter2 stem signature, optionally merging groups by SERP URL overlap. Docs: https://www.brainiac.software/api/seo-content/keyword-group-lexical",
      "parameters": {
        "type": "object",
        "properties": {
          "keywords": {
            "minItems": 1,
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 500
            }
          },
          "serps": {
            "anyOf": [
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {
                  "maxItems": 10,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                }
              },
              {
                "type": "null"
              }
            ]
          },
          "minSharedUrls": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 10
          },
          "maxGroupSize": {
            "default": 500,
            "type": "integer",
            "minimum": 1,
            "maximum": 5000
          }
        },
        "required": [
          "keywords"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__keyword-difficulty-estimate",
      "description": "Transparent keyword difficulty. Estimate keyword difficulty as 100 × mean of capped log referring-domain scores from the caller-supplied top results. Docs: https://www.brainiac.software/api/seo-content/keyword-difficulty-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "keyword": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
          },
          "results": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "position": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 10
                },
                "referringDomains": {
                  "anyOf": [
                    {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "position",
                "referringDomains"
              ],
              "additionalProperties": false
            }
          },
          "referenceCap": {
            "default": 1000,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "serpFeatures": {
            "default": [],
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "keyword",
          "results"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__heading-outline-compare",
      "description": "Heading outline gap analysis. Compare a target H1–H6 outline with competitors and list common sections the target lacks. Docs: https://www.brainiac.software/api/seo-content/heading-outline-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "minLength": 1
              },
              "html": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200000
              }
            },
            "required": [
              "url",
              "html"
            ],
            "additionalProperties": false
          },
          "competitors": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1
                },
                "html": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200000
                }
              },
              "required": [
                "url",
                "html"
              ],
              "additionalProperties": false
            }
          },
          "minShare": {
            "default": 0.5,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "target",
          "competitors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__serp-snippet-preview",
      "description": "SERP snippet pixel-width preview. Estimate title and meta description pixel widths with Liberation Sans advances and truncate at caller-chosen limits. Docs: https://www.brainiac.software/api/seo-content/serp-snippet-preview",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "maxLength": 1000
          },
          "description": {
            "type": "string",
            "maxLength": 5000
          },
          "titleFontPx": {
            "default": 20,
            "type": "number",
            "minimum": 8,
            "maximum": 40
          },
          "descriptionFontPx": {
            "default": 14,
            "type": "number",
            "minimum": 8,
            "maximum": 40
          },
          "titleMaxPx": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ]
          },
          "descriptionMaxPx": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "title",
          "description"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__content-decay-detect",
      "description": "Content decay Mann-Kendall test. Flag pages whose clicks or impressions show a statistically significant decline with Mann-Kendall, Sen slope and windowed percent change. Docs: https://www.brainiac.software/api/seo-content/content-decay-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "series": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1
                },
                "metric": {
                  "default": "clicks",
                  "type": "string",
                  "minLength": 1
                },
                "values": {
                  "minItems": 1,
                  "maxItems": 1000,
                  "type": "array",
                  "items": {
                    "type": "number",
                    "minimum": 0
                  }
                }
              },
              "required": [
                "url",
                "values"
              ],
              "additionalProperties": false
            }
          },
          "period": {
            "anyOf": [
              {
                "type": "integer",
                "minimum": 2,
                "maximum": 9007199254740991
              },
              {
                "type": "null"
              }
            ]
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 0.5
          },
          "minDropPct": {
            "default": 10,
            "type": "number",
            "minimum": 0
          },
          "comparisonWindow": {
            "default": 3,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "series"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__topic-coverage-score",
      "description": "Topic coverage score. Score a draft against required subtopics with synonym phrases, listing covered, partial and missing topics. Docs: https://www.brainiac.software/api/seo-content/topic-coverage-score",
      "parameters": {
        "type": "object",
        "properties": {
          "draft": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "topics": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1
                },
                "phrases": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 500
                  }
                }
              },
              "required": [
                "id",
                "phrases"
              ],
              "additionalProperties": false
            }
          },
          "partialThreshold": {
            "default": 0.5,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          }
        },
        "required": [
          "draft",
          "topics"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__share-of-voice-calc",
      "description": "Share of voice from ranks. Compute estimated clicks, visibility and share of voice per domain from rank snapshots, volumes and a caller-supplied CTR curve. Docs: https://www.brainiac.software/api/seo-content/share-of-voice-calc",
      "parameters": {
        "type": "object",
        "properties": {
          "ctrCurve": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 1
            }
          },
          "keywords": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "keyword": {
                  "type": "string",
                  "minLength": 1
                },
                "volume": {
                  "type": "number",
                  "minimum": 0
                },
                "ranks": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string"
                  },
                  "additionalProperties": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  }
                }
              },
              "required": [
                "keyword",
                "volume",
                "ranks"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "ctrCurve",
          "keywords"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__rank-change-summary",
      "description": "Rank change winners and losers. Summarise winners, losers, new/lost keywords, top-3/top-10 crossings and volatility between rank snapshots. Docs: https://www.brainiac.software/api/seo-content/rank-change-summary",
      "parameters": {
        "type": "object",
        "properties": {
          "snapshots": {
            "minItems": 2,
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "minLength": 1
                },
                "ranks": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "keyword": {
                        "type": "string",
                        "minLength": 1
                      },
                      "position": {
                        "anyOf": [
                          {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 9007199254740991
                          },
                          {
                            "type": "null"
                          }
                        ]
                      },
                      "device": {
                        "type": "string"
                      },
                      "location": {
                        "type": "string"
                      },
                      "tags": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        }
                      }
                    },
                    "required": [
                      "keyword",
                      "position"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "ranks"
              ],
              "additionalProperties": false
            }
          },
          "segmentBy": {
            "default": [],
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "device",
                "location"
              ]
            }
          }
        },
        "required": [
          "snapshots"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "seo-content__keyword-opportunity-score",
      "description": "Keyword opportunity score. Rank keywords by click upside to a target position, weighted by difficulty using a disclosed formula. Docs: https://www.brainiac.software/api/seo-content/keyword-opportunity-score",
      "parameters": {
        "type": "object",
        "properties": {
          "ctrCurve": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 1
            }
          },
          "keywords": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "keyword": {
                  "type": "string",
                  "minLength": 1
                },
                "volume": {
                  "type": "number",
                  "minimum": 0
                },
                "difficulty": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "position": {
                  "anyOf": [
                    {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "keyword",
                "volume",
                "difficulty",
                "position"
              ],
              "additionalProperties": false
            }
          },
          "targetPosition": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "difficultyWeight": {
            "default": 1,
            "type": "number",
            "minimum": 0
          }
        },
        "required": [
          "ctrCurve",
          "keywords"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "seo-content__tfidf-term-gap": "0.04",
  "seo-content__brief-from-serp-texts": "0.04",
  "seo-content__readability-score": "0.02",
  "seo-content__near-duplicate-detect": "0.03",
  "seo-content__internal-link-suggest": "0.04",
  "seo-content__keyword-intent-classify": "0.02",
  "seo-content__keyword-group-lexical": "0.03",
  "seo-content__keyword-difficulty-estimate": "0.02",
  "seo-content__heading-outline-compare": "0.03",
  "seo-content__serp-snippet-preview": "0.02",
  "seo-content__content-decay-detect": "0.03",
  "seo-content__topic-coverage-score": "0.03",
  "seo-content__share-of-voice-calc": "0.03",
  "seo-content__rank-change-summary": "0.03",
  "seo-content__keyword-opportunity-score": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "seo-content__tfidf-term-gap": "seo-content/tfidf-term-gap",
  "seo-content__brief-from-serp-texts": "seo-content/brief-from-serp-texts",
  "seo-content__readability-score": "seo-content/readability-score",
  "seo-content__near-duplicate-detect": "seo-content/near-duplicate-detect",
  "seo-content__internal-link-suggest": "seo-content/internal-link-suggest",
  "seo-content__keyword-intent-classify": "seo-content/keyword-intent-classify",
  "seo-content__keyword-group-lexical": "seo-content/keyword-group-lexical",
  "seo-content__keyword-difficulty-estimate": "seo-content/keyword-difficulty-estimate",
  "seo-content__heading-outline-compare": "seo-content/heading-outline-compare",
  "seo-content__serp-snippet-preview": "seo-content/serp-snippet-preview",
  "seo-content__content-decay-detect": "seo-content/content-decay-detect",
  "seo-content__topic-coverage-score": "seo-content/topic-coverage-score",
  "seo-content__share-of-voice-calc": "seo-content/share-of-voice-calc",
  "seo-content__rank-change-summary": "seo-content/rank-change-summary",
  "seo-content__keyword-opportunity-score": "seo-content/keyword-opportunity-score"
}


class BrainiacSeoContentAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — seo-content",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the seo-content catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "seo-content", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["TF-IDF term gap vs competitor pages"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the seo-content group. "
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
