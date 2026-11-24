"""Auto-generated BRAINIAC Heurist Mesh agent for group `news-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "news-intelligence__original-source-trace",
      "description": "Trace original news sources. Cluster similar articles and identify the earliest published item. Later reprints are not treated as independent confirmation. Docs: https://www.brainiac.software/api/news-intelligence/original-source-trace",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__syndication-cluster",
      "description": "Cluster syndicated news articles. Group near-duplicate titles and bodies into syndication clusters without counting repeats as confirmation. Docs: https://www.brainiac.software/api/news-intelligence/syndication-cluster",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__claim-extract",
      "description": "Extract news claims. Extract claim-like sentences and quotes from supplied article text using local heuristics. Docs: https://www.brainiac.software/api/news-intelligence/claim-extract",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__claim-source-match",
      "description": "Match claims to sources. Match supplied or extracted claims to articles by text overlap. Multiple outlets repeating a claim are not independent confirmation. Docs: https://www.brainiac.software/api/news-intelligence/claim-source-match",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__event-timeline-build",
      "description": "Build news event timeline. Order supplied events or dated articles into a timeline without inventing missing dates. Docs: https://www.brainiac.software/api/news-intelligence/event-timeline-build",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__correction-history-detect",
      "description": "Detect news correction history. Flag correction, update, and retraction wording or updatedAt changes in supplied articles. Docs: https://www.brainiac.software/api/news-intelligence/correction-history-detect",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__source-independence-analyze",
      "description": "Analyze news source independence. Count distinct outlets and mark syndicated/similar copies as non-independent. Repeats are never claimed as confirmation. Docs: https://www.brainiac.software/api/news-intelligence/source-independence-analyze",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__contradiction-detect",
      "description": "Detect news claim contradictions. Find affirming vs negating overlapping claims, and label near-duplicate repeats without treating them as confirmation. Docs: https://www.brainiac.software/api/news-intelligence/contradiction-detect",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__country-event-monitor",
      "description": "Monitor country news events. Filter supplied articles and events by country into a dated monitor list. Docs: https://www.brainiac.software/api/news-intelligence/country-event-monitor",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__verification-evidence-report",
      "description": "Build news verification evidence report. Aggregate source tracing, syndication, claims, contradictions, corrections, and independence findings. Repeats are never independent confirmation. Docs: https://www.brainiac.software/api/news-intelligence/verification-evidence-report",
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
                  "application/json",
                  "application/xml",
                  "text/xml"
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
          "articles": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 400
                },
                "url": {
                  "type": "string",
                  "maxLength": 500
                },
                "outlet": {
                  "type": "string",
                  "maxLength": 200
                },
                "publisher": {
                  "type": "string",
                  "maxLength": 200
                },
                "author": {
                  "type": "string",
                  "maxLength": 200
                },
                "publishedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "updatedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "language": {
                  "type": "string",
                  "maxLength": 40
                },
                "body": {
                  "type": "string",
                  "maxLength": 50000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 5000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "syndicatedFrom": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "claims": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "polarity": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "event": {
                  "type": "string",
                  "maxLength": 200
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "events": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "maxLength": 300
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "articleId": {
                  "type": "string",
                  "maxLength": 80
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "rss": {
            "type": "object",
            "properties": {
              "url": {
                "type": "string",
                "maxLength": 500,
                "format": "uri"
              },
              "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 40
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "country": {
            "type": "string",
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__headlines",
      "description": "News headlines. Dated headlines from the public GDELT DOC API and documented official RSS feeds. Provide query or section. Docs: https://www.brainiac.software/api/news-intelligence/headlines",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "section": {
            "type": "string",
            "enum": [
              "crypto",
              "general"
            ]
          },
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "news-intelligence__crypto-headlines",
      "description": "Crypto news headlines. Crypto-section dated headlines from GDELT and documented official RSS feeds. Docs: https://www.brainiac.software/api/news-intelligence/crypto-headlines",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "news-intelligence__original-source-trace": "0.05",
  "news-intelligence__syndication-cluster": "0.04",
  "news-intelligence__claim-extract": "0.04",
  "news-intelligence__claim-source-match": "0.05",
  "news-intelligence__event-timeline-build": "0.04",
  "news-intelligence__correction-history-detect": "0.03",
  "news-intelligence__source-independence-analyze": "0.04",
  "news-intelligence__contradiction-detect": "0.05",
  "news-intelligence__country-event-monitor": "0.04",
  "news-intelligence__verification-evidence-report": "0.08",
  "news-intelligence__headlines": "0.001",
  "news-intelligence__crypto-headlines": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "news-intelligence__original-source-trace": "news-intelligence/original-source-trace",
  "news-intelligence__syndication-cluster": "news-intelligence/syndication-cluster",
  "news-intelligence__claim-extract": "news-intelligence/claim-extract",
  "news-intelligence__claim-source-match": "news-intelligence/claim-source-match",
  "news-intelligence__event-timeline-build": "news-intelligence/event-timeline-build",
  "news-intelligence__correction-history-detect": "news-intelligence/correction-history-detect",
  "news-intelligence__source-independence-analyze": "news-intelligence/source-independence-analyze",
  "news-intelligence__contradiction-detect": "news-intelligence/contradiction-detect",
  "news-intelligence__country-event-monitor": "news-intelligence/country-event-monitor",
  "news-intelligence__verification-evidence-report": "news-intelligence/verification-evidence-report",
  "news-intelligence__headlines": "news-intelligence/headlines",
  "news-intelligence__crypto-headlines": "news-intelligence/crypto-headlines"
}


class BrainiacNewsIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — news-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the news-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "news-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Trace original news sources"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the news-intelligence group. "
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
