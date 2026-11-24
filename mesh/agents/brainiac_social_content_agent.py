"""Auto-generated BRAINIAC Heurist Mesh agent for group `social-content` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "social-content__post-performance-analyze",
      "description": "Analyze post performance. Calculate engagement and an engagement rate from supplied impressions, likes, comments, shares, and saves. A missing count is left out, and no rate is calculated without impressions. Equal rates keep the caller's input order. Docs: https://www.brainiac.software/api/social-content/post-performance-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__calendar-generate",
      "description": "Draft a content calendar. Place supplied posts on a caller-supplied window. Dated posts stay on their date. Undated posts fill empty days in input order. No caption is written and nothing is scheduled. Docs: https://www.brainiac.software/api/social-content/calendar-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__repurpose",
      "description": "Repurpose content for a platform. Shorten supplied text to a documented character limit only when the caller names a target platform. No words are added and nothing is published. Docs: https://www.brainiac.software/api/social-content/repurpose",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__hashtag-analyze",
      "description": "Analyze supplied hashtags. Count hashtags in the supplied posts and copy post and impression figures from supplied hashtag rows. The counts stay separate. Current popularity and reach are not estimated. Docs: https://www.brainiac.software/api/social-content/hashtag-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__comment-classify",
      "description": "Classify supplied comments. Match a supplied type to question, praise, complaint, spam, or request. Without a type, a comment is labeled only when one documented keyword rule matches. No moderation action is taken. Docs: https://www.brainiac.software/api/social-content/comment-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__engagement-anomaly-detect",
      "description": "Detect engagement anomalies. Apply a Tukey 1.5 IQR fence to engagement rates when at least 8 posts have impressions and an engagement count. A point outside the fence is not a confirmed anomaly. Docs: https://www.brainiac.software/api/social-content/engagement-anomaly-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__duplicate-detect",
      "description": "Detect repeated content. Group posts whose text matches after trimming, and list pairs that share at least 90 percent of their tokens. No post is removed. Docs: https://www.brainiac.software/api/social-content/duplicate-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
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
      "name": "social-content__account-performance-report",
      "description": "Report account performance. Combine supplied totals, platform splits, calendar slots, drafts, hashtags, comments, rate fences, and repeated text. The report does not publish content or estimate reach. Docs: https://www.brainiac.software/api/social-content/account-performance-report",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "maxLength": 200000
          },
          "csv": {
            "type": "string",
            "maxLength": 200000
          },
          "file": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 180
              },
              "mediaType": {
                "type": "string",
                "enum": [
                  "text/plain",
                  "text/csv",
                  "application/json"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              }
            },
            "required": [
              "mediaType",
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "posts": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "platform": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 4000
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "likes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "comments": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "shares": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "saves": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "additionalProperties": false
            }
          },
          "comments": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postId": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                },
                "type": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "hashtags": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tag": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "posts": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "impressions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000000
                }
              },
              "required": [
                "tag"
              ],
              "additionalProperties": false
            }
          },
          "window": {
            "type": "object",
            "properties": {
              "start": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "days": {
                "type": "integer",
                "minimum": 1,
                "maximum": 31
              }
            },
            "required": [
              "start",
              "days"
            ],
            "additionalProperties": false
          },
          "platform": {
            "type": "string",
            "maxLength": 40
          },
          "account": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "maxLength": 80
              },
              "platform": {
                "type": "string",
                "maxLength": 40
              },
              "followers": {
                "type": "integer",
                "minimum": 0,
                "maximum": 1000000000
              }
            },
            "additionalProperties": false
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "social-content__post-performance-analyze": "0.04",
  "social-content__calendar-generate": "0.05",
  "social-content__repurpose": "0.05",
  "social-content__hashtag-analyze": "0.04",
  "social-content__comment-classify": "0.03",
  "social-content__engagement-anomaly-detect": "0.05",
  "social-content__duplicate-detect": "0.05",
  "social-content__account-performance-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "social-content__post-performance-analyze": "social-content/post-performance-analyze",
  "social-content__calendar-generate": "social-content/calendar-generate",
  "social-content__repurpose": "social-content/repurpose",
  "social-content__hashtag-analyze": "social-content/hashtag-analyze",
  "social-content__comment-classify": "social-content/comment-classify",
  "social-content__engagement-anomaly-detect": "social-content/engagement-anomaly-detect",
  "social-content__duplicate-detect": "social-content/duplicate-detect",
  "social-content__account-performance-report": "social-content/account-performance-report"
}


class BrainiacSocialContentAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — social-content",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the social-content catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "social-content", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze post performance"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the social-content group. "
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
