"""Auto-generated BRAINIAC Heurist Mesh agent for group `privacy-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "privacy-operations__policy-structure-audit",
      "description": "Audit privacy policy structure. List headings and Section lines in a supplied policy and compare them with the sections the caller marks as required. Headings are still listed when a required section is absent. A missing section is a gap in the document, not a legal conclusion. Docs: https://www.brainiac.software/api/privacy-operations/policy-structure-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__personal-data-inventory-extract",
      "description": "Extract a personal data inventory. Copy categories, purposes, stated legal bases, and retention periods from Category fields. Prose is not mined for categories, and a stated basis is not assessed. Docs: https://www.brainiac.software/api/privacy-operations/personal-data-inventory-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__data-retention-policy-check",
      "description": "Check stated retention periods. Read retention periods stated by the caller. A period counts only as days, months, years, account lifetime, or until deletion. Months are not converted to days, and no statutory period is invented. Docs: https://www.brainiac.software/api/privacy-operations/data-retention-policy-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__notice-consistency-check",
      "description": "Compare a policy and a notice. Compare purpose, stated basis, and retention for the same category in a supplied policy and notice. A difference is reported and neither document is chosen. Docs: https://www.brainiac.software/api/privacy-operations/notice-consistency-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__cookie-consent-configuration-audit",
      "description": "Audit cookie consent configuration. Read cookie purpose, duration, and the consent state supplied by the caller. An optional cookie without an opt-in or opt-out state is reported. Consent is not enforced and the cookie is not classified by law. Docs: https://www.brainiac.software/api/privacy-operations/cookie-consent-configuration-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__data-subject-request-classify",
      "description": "Classify data subject requests. Match a supplied request type to access, deletion, correction, export, objection, or restriction. Any other wording is left unrecognized. No response deadline is calculated. Docs: https://www.brainiac.software/api/privacy-operations/data-subject-request-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__data-deletion-evidence-check",
      "description": "Check deletion evidence. Compare supplied deletion requests with supplied evidence lines. A line that says deleted is only a statement in the request. No external record is accessed or deleted. Docs: https://www.brainiac.software/api/privacy-operations/data-deletion-evidence-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
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
      "name": "privacy-operations__documentation-report",
      "description": "Report privacy documentation. Combine supplied sections, categories, retention periods, notice differences, cookie consent states, request types, and deletion evidence. The report does not determine GDPR compliance. Docs: https://www.brainiac.software/api/privacy-operations/documentation-report",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 200000
          },
          "policy": {
            "type": "string",
            "maxLength": 200000
          },
          "notice": {
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
          "sections": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 80
            }
          },
          "requirements": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "section",
                    "category",
                    "field"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "categories": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "basis": {
                  "type": "string",
                  "maxLength": 160
                },
                "retention": {
                  "type": "string",
                  "maxLength": 160
                },
                "document": {
                  "type": "string",
                  "enum": [
                    "policy",
                    "notice"
                  ]
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "cookies": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "purpose": {
                  "type": "string",
                  "maxLength": 160
                },
                "duration": {
                  "type": "string",
                  "maxLength": 80
                },
                "consent": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "consents": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "state": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "name",
                "state"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
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
                "type": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requestId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "action": {
                  "type": "string",
                  "maxLength": 40
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "requestId"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "privacy-operations__policy-structure-audit": "0.04",
  "privacy-operations__personal-data-inventory-extract": "0.04",
  "privacy-operations__data-retention-policy-check": "0.04",
  "privacy-operations__notice-consistency-check": "0.05",
  "privacy-operations__cookie-consent-configuration-audit": "0.04",
  "privacy-operations__data-subject-request-classify": "0.03",
  "privacy-operations__data-deletion-evidence-check": "0.04",
  "privacy-operations__documentation-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "privacy-operations__policy-structure-audit": "privacy-operations/policy-structure-audit",
  "privacy-operations__personal-data-inventory-extract": "privacy-operations/personal-data-inventory-extract",
  "privacy-operations__data-retention-policy-check": "privacy-operations/data-retention-policy-check",
  "privacy-operations__notice-consistency-check": "privacy-operations/notice-consistency-check",
  "privacy-operations__cookie-consent-configuration-audit": "privacy-operations/cookie-consent-configuration-audit",
  "privacy-operations__data-subject-request-classify": "privacy-operations/data-subject-request-classify",
  "privacy-operations__data-deletion-evidence-check": "privacy-operations/data-deletion-evidence-check",
  "privacy-operations__documentation-report": "privacy-operations/documentation-report"
}


class BrainiacPrivacyOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — privacy-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the privacy-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "privacy-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit privacy policy structure"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the privacy-operations group. "
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
