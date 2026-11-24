"""Auto-generated BRAINIAC Heurist Mesh agent for group `file-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "file-security__file-behavior-indicator-extract",
      "description": "Extract file behaviour indicators. Extract suspicious behaviour indicators from caller-supplied analysis reports/text using local static pattern matching. Files are never executed. Absence of matches is not a malware-free verdict. Docs: https://www.brainiac.software/api/file-security/file-behavior-indicator-extract",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__malware-artifact-cluster",
      "description": "Cluster malware artifacts. Group caller-supplied files/artifacts by identical hashes and structural similarity (magic/extension/size). Clustering is not family attribution or confirmed malware. Docs: https://www.brainiac.software/api/file-security/malware-artifact-cluster",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__executable-metadata-analyze",
      "description": "Analyze executable metadata. Analyze PE/ELF/Mach-O metadata and structural properties from caller-supplied bytes. Static only—files are never executed. Docs: https://www.brainiac.software/api/file-security/executable-metadata-analyze",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__macro-document-risk-detect",
      "description": "Detect macro document risk. Identify suspicious macro markers in caller-supplied Office/RTF documents via static strings/package entries. Macros are never executed. Docs: https://www.brainiac.software/api/file-security/macro-document-risk-detect",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__file-extension-mismatch-detect",
      "description": "Detect extension/format mismatches. Identify mismatches between caller-supplied filenames/extensions and local magic-byte formats, including double extensions. Docs: https://www.brainiac.software/api/file-security/file-extension-mismatch-detect",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__suspicious-script-pattern-detect",
      "description": "Detect suspicious script patterns. Analyze caller-supplied scripts for suspicious static patterns (encoded commands, download cradles, obfuscation). Scripts are never executed. Docs: https://www.brainiac.software/api/file-security/suspicious-script-pattern-detect",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__archive-payload-risk-detect",
      "description": "Detect archive payload risk. Inspect caller-supplied archives for nested members and risky file types with strict depth/size/decompression limits. Contents are never executed or uploaded to scanners. Docs: https://www.brainiac.software/api/file-security/archive-payload-risk-detect",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "file-security__malware-indicator-extract",
      "description": "Extract malware indicators. Extract IPs, domains, URLs, hashes, and emails from caller-supplied files/reports using local static parsing. Extracted strings are not live threat-intel verdicts. Docs: https://www.brainiac.software/api/file-security/malware-indicator-extract",
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
              "id": {
                "type": "string",
                "maxLength": 80
              },
              "filename": {
                "type": "string",
                "minLength": 1,
                "maxLength": 260
              },
              "mediaType": {
                "type": "string",
                "maxLength": 120
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "sha256": {
                "type": "string",
                "maxLength": 128
              },
              "md5": {
                "type": "string",
                "maxLength": 64
              },
              "sha1": {
                "type": "string",
                "maxLength": 80
              },
              "sizeBytes": {
                "type": "number",
                "minimum": 0,
                "maximum": 100000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "reports": {
            "maxItems": 40,
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
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "maxLength": 200000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "text"
              ],
              "additionalProperties": false
            }
          },
          "artifacts": {
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
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "md5": {
                  "type": "string",
                  "maxLength": 64
                },
                "sha1": {
                  "type": "string",
                  "maxLength": 80
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "role": {
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
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "maxArchiveDepth": {
            "type": "number",
            "minimum": 1,
            "maximum": 5
          },
          "maxInflateBytes": {
            "type": "number",
            "minimum": 1000,
            "maximum": 2000000
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "file-security__file-behavior-indicator-extract": "0.04",
  "file-security__malware-artifact-cluster": "0.04",
  "file-security__executable-metadata-analyze": "0.04",
  "file-security__macro-document-risk-detect": "0.04",
  "file-security__file-extension-mismatch-detect": "0.03",
  "file-security__suspicious-script-pattern-detect": "0.04",
  "file-security__archive-payload-risk-detect": "0.05",
  "file-security__malware-indicator-extract": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "file-security__file-behavior-indicator-extract": "file-security/file-behavior-indicator-extract",
  "file-security__malware-artifact-cluster": "file-security/malware-artifact-cluster",
  "file-security__executable-metadata-analyze": "file-security/executable-metadata-analyze",
  "file-security__macro-document-risk-detect": "file-security/macro-document-risk-detect",
  "file-security__file-extension-mismatch-detect": "file-security/file-extension-mismatch-detect",
  "file-security__suspicious-script-pattern-detect": "file-security/suspicious-script-pattern-detect",
  "file-security__archive-payload-risk-detect": "file-security/archive-payload-risk-detect",
  "file-security__malware-indicator-extract": "file-security/malware-indicator-extract"
}


class BrainiacFileSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — file-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the file-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "file-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract file behaviour indicators"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the file-security group. "
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
