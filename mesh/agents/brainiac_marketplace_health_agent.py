"""Auto-generated BRAINIAC Heurist Mesh agent for group `marketplace-health` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "marketplace-health__account-notice-extract",
      "description": "Extract marketplace notices. Copy the reason, deadline, and requested action from labeled Notice fields. Prose is not mined for a reason, and no response window is added when the deadline is blank. Docs: https://www.brainiac.software/api/marketplace-health/account-notice-extract",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__seller-performance-metric-analyze",
      "description": "Analyze seller performance metrics. Compare a supplied metric with a supplied target only when the caller also says whether higher or lower is better. No marketplace threshold is invented, and a miss is not a suspension. Docs: https://www.brainiac.software/api/marketplace-health/seller-performance-metric-analyze",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__payout-hold-diagnose",
      "description": "Diagnose a stated payout hold. Read the amount, currency, date, and reason stated on a hold. The hold is not removed and the record is not treated as a release. Docs: https://www.brainiac.software/api/marketplace-health/payout-hold-diagnose",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__account-restriction-evidence-check",
      "description": "Check restriction evidence. Compare supplied evidence with the evidence kinds the caller marks as required, and with the restrictions in the export. A missing document is not invented, and a restriction is not lifted. Docs: https://www.brainiac.software/api/marketplace-health/account-restriction-evidence-check",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__policy-issue-classify",
      "description": "Classify a notice against supplied policies. Match a notice reason to a policy only when the reason equals the supplied policy name or id. No marketplace policy page is fetched, and a partial overlap is not chosen. Docs: https://www.brainiac.software/api/marketplace-health/policy-issue-classify",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__seller-appeal-evidence-build",
      "description": "Build an appeal evidence checklist. List the evidence supplied for a notice and the caller-required kinds that are absent. The checklist does not predict that an appeal will succeed. Docs: https://www.brainiac.software/api/marketplace-health/seller-appeal-evidence-build",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__account-risk-report",
      "description": "Report account health records. Combine supplied notices, metrics, holds, policy matches, evidence gaps, and a factual draft. The report does not predict a suspension or say that a hold will be removed. Docs: https://www.brainiac.software/api/marketplace-health/account-risk-report",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
      "name": "marketplace-health__notice-response-draft",
      "description": "Draft a notice response. Write a response from the stated reason, deadline, requested action, and supplied evidence. The draft is not sent, and it does not promise an appeal result or a payout release. Docs: https://www.brainiac.software/api/marketplace-health/notice-response-draft",
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
          "notices": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "marketplace": {
                  "type": "string",
                  "maxLength": 80
                },
                "received": {
                  "type": "string",
                  "maxLength": 40
                },
                "deadline": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                },
                "action": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "metrics": {
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
                "value": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "target": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "above",
                    "below"
                  ]
                },
                "period": {
                  "type": "string",
                  "maxLength": 40
                },
                "unit": {
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
          "holds": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "reason": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "text": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "restrictions": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "since": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "evidence": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "noticeId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "date": {
                  "type": "string",
                  "maxLength": 40
                },
                "text": {
                  "type": "string",
                  "maxLength": 500
                }
              },
              "additionalProperties": false
            }
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "name"
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
  "marketplace-health__account-notice-extract": "0.04",
  "marketplace-health__seller-performance-metric-analyze": "0.04",
  "marketplace-health__payout-hold-diagnose": "0.04",
  "marketplace-health__account-restriction-evidence-check": "0.05",
  "marketplace-health__policy-issue-classify": "0.04",
  "marketplace-health__seller-appeal-evidence-build": "0.05",
  "marketplace-health__account-risk-report": "0.12",
  "marketplace-health__notice-response-draft": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "marketplace-health__account-notice-extract": "marketplace-health/account-notice-extract",
  "marketplace-health__seller-performance-metric-analyze": "marketplace-health/seller-performance-metric-analyze",
  "marketplace-health__payout-hold-diagnose": "marketplace-health/payout-hold-diagnose",
  "marketplace-health__account-restriction-evidence-check": "marketplace-health/account-restriction-evidence-check",
  "marketplace-health__policy-issue-classify": "marketplace-health/policy-issue-classify",
  "marketplace-health__seller-appeal-evidence-build": "marketplace-health/seller-appeal-evidence-build",
  "marketplace-health__account-risk-report": "marketplace-health/account-risk-report",
  "marketplace-health__notice-response-draft": "marketplace-health/notice-response-draft"
}


class BrainiacMarketplaceHealthAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — marketplace-health",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the marketplace-health catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "marketplace-health", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract marketplace notices"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the marketplace-health group. "
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
