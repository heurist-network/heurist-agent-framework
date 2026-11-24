"""Auto-generated BRAINIAC Heurist Mesh agent for group `evidence-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "evidence-intelligence__file-hash-manifest",
      "description": "Build evidence file hash manifest. Hash uploaded evidence bytes locally with md5, sha1, sha256, and sha512. Hash matches verify cryptographic integrity only, not factual authenticity. Docs: https://www.brainiac.software/api/evidence-intelligence/file-hash-manifest",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__metadata-extract",
      "description": "Extract evidence metadata. Extract container metadata from uploaded files locally. Missing EXIF or GPS fields are not invented. Docs: https://www.brainiac.software/api/evidence-intelligence/metadata-extract",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__c2pa-provenance-verify",
      "description": "Verify C2PA provenance markers. Look for local C2PA/JUMBF markers in uploaded bytes. Marker presence is not a factual authenticity determination. Docs: https://www.brainiac.software/api/evidence-intelligence/c2pa-provenance-verify",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__chain-of-custody-build",
      "description": "Build evidence chain of custody. Order supplied custody events per evidence id and compare optional hashAfter values to current sha256 digests. Docs: https://www.brainiac.software/api/evidence-intelligence/chain-of-custody-build",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__image-source-timeline-build",
      "description": "Build image source timeline. Combine caller-supplied capture times, local EXIF timestamps, and custody events into an image timeline. Docs: https://www.brainiac.software/api/evidence-intelligence/image-source-timeline-build",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__video-keyframe-extract",
      "description": "Extract video keyframe evidence. Inspect local video container metadata and hash caller-supplied keyframe image files. Frames are not decoded by external services. Docs: https://www.brainiac.software/api/evidence-intelligence/video-keyframe-extract",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__visual-location-clue-extract",
      "description": "Extract visual location clues. Extract embedded GPS or location text clues from local image metadata. Missing coordinates are not invented. Docs: https://www.brainiac.software/api/evidence-intelligence/visual-location-clue-extract",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__duplicate-cluster",
      "description": "Cluster duplicate evidence. Cluster uploaded evidence files that share the same sha256 digest. Duplicates are cryptographic only. Docs: https://www.brainiac.software/api/evidence-intelligence/duplicate-cluster",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__integrity-recheck",
      "description": "Recheck evidence integrity. Compare current local hashes to caller-supplied expected digests. A match verifies cryptographic integrity only. Docs: https://www.brainiac.software/api/evidence-intelligence/integrity-recheck",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "evidence-intelligence__forensic-report",
      "description": "Build forensic evidence report. Aggregate hash, metadata, C2PA, custody, timeline, keyframe, location, duplicate, and integrity results. Distinguishes cryptographic integrity from factual authenticity. Docs: https://www.brainiac.software/api/evidence-intelligence/forensic-report",
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
          "files": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 180
                },
                "mediaType": {
                  "type": "string",
                  "enum": [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                    "image/gif",
                    "video/mp4",
                    "video/quicktime",
                    "application/pdf",
                    "application/octet-stream",
                    "text/plain",
                    "application/json"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "parentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 200
                },
                "capturedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "custodyEvents": {
            "maxItems": 400,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "actor": {
                  "type": "string",
                  "maxLength": 200
                },
                "action": {
                  "type": "string",
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "note": {
                  "type": "string",
                  "maxLength": 500
                },
                "hashAfter": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "expectedHashes": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "evidenceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 180
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "md5",
                    "sha1",
                    "sha256",
                    "sha512"
                  ]
                },
                "digest": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "evidence-intelligence__file-hash-manifest": "0.04",
  "evidence-intelligence__metadata-extract": "0.04",
  "evidence-intelligence__c2pa-provenance-verify": "0.05",
  "evidence-intelligence__chain-of-custody-build": "0.04",
  "evidence-intelligence__image-source-timeline-build": "0.04",
  "evidence-intelligence__video-keyframe-extract": "0.05",
  "evidence-intelligence__visual-location-clue-extract": "0.04",
  "evidence-intelligence__duplicate-cluster": "0.03",
  "evidence-intelligence__integrity-recheck": "0.03",
  "evidence-intelligence__forensic-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "evidence-intelligence__file-hash-manifest": "evidence-intelligence/file-hash-manifest",
  "evidence-intelligence__metadata-extract": "evidence-intelligence/metadata-extract",
  "evidence-intelligence__c2pa-provenance-verify": "evidence-intelligence/c2pa-provenance-verify",
  "evidence-intelligence__chain-of-custody-build": "evidence-intelligence/chain-of-custody-build",
  "evidence-intelligence__image-source-timeline-build": "evidence-intelligence/image-source-timeline-build",
  "evidence-intelligence__video-keyframe-extract": "evidence-intelligence/video-keyframe-extract",
  "evidence-intelligence__visual-location-clue-extract": "evidence-intelligence/visual-location-clue-extract",
  "evidence-intelligence__duplicate-cluster": "evidence-intelligence/duplicate-cluster",
  "evidence-intelligence__integrity-recheck": "evidence-intelligence/integrity-recheck",
  "evidence-intelligence__forensic-report": "evidence-intelligence/forensic-report"
}


class BrainiacEvidenceIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — evidence-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the evidence-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "evidence-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Build evidence file hash manifest"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the evidence-intelligence group. "
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
