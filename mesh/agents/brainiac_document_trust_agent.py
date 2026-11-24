"""Auto-generated BRAINIAC Heurist Mesh agent for group `document-trust` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "document-trust__pdf-digital-signature-verify",
      "description": "Verify PDF digital signatures. Inspect PDF /Sig dictionaries and optional detached signatures locally. Technical verification is not legal enforceability. Docs: https://www.brainiac.software/api/document-trust/pdf-digital-signature-verify",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__signature-certificate-chain-validate",
      "description": "Validate signature certificate chains. Parse supplied X.509 certificates and check validity windows and issuer links locally. Not a legal trust determination. Docs: https://www.brainiac.software/api/document-trust/signature-certificate-chain-validate",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__signature-timestamp-validate",
      "description": "Validate signature timestamps. Check PDF /M timestamps and caller-supplied signer signedAt values against asOf and optional certificate windows. Docs: https://www.brainiac.software/api/document-trust/signature-timestamp-validate",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__signed-tamper-detect",
      "description": "Detect signed-document tampering. Compare current PDF hashes and ByteRange digests to caller-supplied expectations. Missing expectations are not invented. Docs: https://www.brainiac.software/api/document-trust/signed-tamper-detect",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__signature-coverage-check",
      "description": "Check document signature coverage. Measure ByteRange coverage over supplied PDF bytes for each signature field found locally. Docs: https://www.brainiac.software/api/document-trust/signature-coverage-check",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__signature-revocation-status-check",
      "description": "Check signature revocation status. Compare certificate serials to caller-supplied revocation entries only. Live commercial OCSP/CRL networks are not queried. Docs: https://www.brainiac.software/api/document-trust/signature-revocation-status-check",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__contract-signed-version-match",
      "description": "Match signed contract versions. Compare sha256 digests and version labels across supplied signed PDF copies. Differing hashes are reported, not invented. Docs: https://www.brainiac.software/api/document-trust/contract-signed-version-match",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__multi-signer-audit",
      "description": "Audit multi-signer documents. List PDF signature dictionaries and caller-supplied signers per document. Technical listing is not legal enforceability. Docs: https://www.brainiac.software/api/document-trust/multi-signer-audit",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__evidence-bundle-build",
      "description": "Build document evidence bundles. Bundle local signature, certificate, timestamp, tamper, coverage, and revocation checks with an explicit technical-vs-legal distinction. Docs: https://www.brainiac.software/api/document-trust/evidence-bundle-build",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
      "name": "document-trust__electronic-trust-report",
      "description": "Build electronic document trust report. Aggregate local signature, chain, timestamp, tamper, coverage, revocation, version, and multi-signer findings. Distinguishes technical verification from legal enforceability. Docs: https://www.brainiac.software/api/document-trust/electronic-trust-report",
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
          "files": {
            "maxItems": 20,
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
                    "application/pdf",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "versionLabel": {
                  "type": "string",
                  "maxLength": 80
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                },
                "expectedSha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "expectedByteRangeSha256": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "pem": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 50000
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "leaf",
                    "intermediate",
                    "root"
                  ]
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "pem"
              ],
              "additionalProperties": false
            }
          },
          "signers": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 200
                },
                "signedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "fieldName": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateId": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "revocations": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "serialNumber": {
                  "type": "string",
                  "maxLength": 128
                },
                "revokedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
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
          "detachedSignatures": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "documentId": {
                  "type": "string",
                  "maxLength": 80
                },
                "algorithm": {
                  "type": "string",
                  "enum": [
                    "RSA-SHA256",
                    "RSA-SHA1",
                    "RSA-SHA512"
                  ]
                },
                "signatureBase64": {
                  "type": "string",
                  "maxLength": 100000
                },
                "publicKeyPem": {
                  "type": "string",
                  "maxLength": 50000
                },
                "digestSha256": {
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
  "document-trust__pdf-digital-signature-verify": "0.05",
  "document-trust__signature-certificate-chain-validate": "0.04",
  "document-trust__signature-timestamp-validate": "0.03",
  "document-trust__signed-tamper-detect": "0.04",
  "document-trust__signature-coverage-check": "0.03",
  "document-trust__signature-revocation-status-check": "0.03",
  "document-trust__contract-signed-version-match": "0.04",
  "document-trust__multi-signer-audit": "0.04",
  "document-trust__evidence-bundle-build": "0.07",
  "document-trust__electronic-trust-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "document-trust__pdf-digital-signature-verify": "document-trust/pdf-digital-signature-verify",
  "document-trust__signature-certificate-chain-validate": "document-trust/signature-certificate-chain-validate",
  "document-trust__signature-timestamp-validate": "document-trust/signature-timestamp-validate",
  "document-trust__signed-tamper-detect": "document-trust/signed-tamper-detect",
  "document-trust__signature-coverage-check": "document-trust/signature-coverage-check",
  "document-trust__signature-revocation-status-check": "document-trust/signature-revocation-status-check",
  "document-trust__contract-signed-version-match": "document-trust/contract-signed-version-match",
  "document-trust__multi-signer-audit": "document-trust/multi-signer-audit",
  "document-trust__evidence-bundle-build": "document-trust/evidence-bundle-build",
  "document-trust__electronic-trust-report": "document-trust/electronic-trust-report"
}


class BrainiacDocumentTrustAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — document-trust",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the document-trust catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "document-trust", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Verify PDF digital signatures"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the document-trust group. "
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
