"""Auto-generated BRAINIAC Heurist Mesh agent for group `grant-compliance` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "grant-compliance__requirements-extract",
      "description": "Extract grant requirements. Read Requirement lines and structured requirements. Other prose is not turned into a grant rule. Docs: https://www.brainiac.software/api/grant-compliance/requirements-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "guidelines": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "requirements": {
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
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
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__eligibility-check",
      "description": "Check supplied eligibility rules. Compare each supplied rule with the supplied fact of the same name. A match is not an approval, and missing facts are not filled in. Docs: https://www.brainiac.software/api/grant-compliance/eligibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "rules": {
            "minItems": 1,
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
                "fact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "operator": {
                  "type": "string",
                  "enum": [
                    "equals",
                    "includes",
                    "number_at_least",
                    "number_at_most",
                    "boolean_is"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "id",
                "fact",
                "operator",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "facts": {
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
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "rules"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__application-completeness",
      "description": "Check application completeness. Mark a requirement present only when an application section cites its id. The answer is not scored, and a complete set is not compliance. Docs: https://www.brainiac.software/api/grant-compliance/application-completeness",
      "parameters": {
        "type": "object",
        "properties": {
          "guidelines": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "requirements": {
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "applicationText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "sections": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "requirementId",
                "text"
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
      "name": "grant-compliance__budget-validate",
      "description": "Validate a grant budget. Sum the supplied lines, compare that sum with a supplied total, and check supplied category amount or percent caps. No cap is assumed. Docs: https://www.brainiac.software/api/grant-compliance/budget-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "lines": {
            "minItems": 1,
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                }
              },
              "required": [
                "category",
                "description",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "total": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "limits": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "maxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxPercent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                }
              },
              "required": [
                "category"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "lines"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__expense-eligibility-check",
      "description": "Check expenses against supplied rules. Apply only the supplied category decisions. A category with no rule stays not supplied, and an eligible rule is not a funder decision. Docs: https://www.brainiac.software/api/grant-compliance/expense-eligibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "expenses": {
            "minItems": 1,
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
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                }
              },
              "required": [
                "id",
                "description",
                "category",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "rules": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "decision": {
                  "type": "string",
                  "enum": [
                    "eligible",
                    "ineligible"
                  ]
                }
              },
              "required": [
                "category",
                "decision"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "expenses",
          "rules"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__evidence-match",
      "description": "Match evidence to requirements. Attach evidence that cites a requirement id. Evidence with no id is not matched, and the strength of the evidence is not judged. Docs: https://www.brainiac.software/api/grant-compliance/evidence-match",
      "parameters": {
        "type": "object",
        "properties": {
          "requirements": {
            "minItems": 1,
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "id",
                "text"
              ],
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
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
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
          "requirements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__deliverable-track",
      "description": "Track supplied deliverables. Repeat the status supplied for each deliverable and compare an update date with a supplied due date. accepted_by_caller is not an official acceptance. Docs: https://www.brainiac.software/api/grant-compliance/deliverable-track",
      "parameters": {
        "type": "object",
        "properties": {
          "deliverables": {
            "minItems": 1,
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
                  "minLength": 1,
                  "maxLength": 200
                },
                "dueDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                }
              },
              "required": [
                "id",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "updates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "deliverableId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "not_started",
                    "in_progress",
                    "submitted",
                    "accepted_by_caller"
                  ]
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "note": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "deliverableId",
                "status"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "deliverables"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__report-validate",
      "description": "Validate a grant report. Mark a reporting obligation present only when the report cites its id. A present section is not accepted by a funder. Docs: https://www.brainiac.software/api/grant-compliance/report-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "guidelines": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "obligations": {
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "reportText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "reportSections": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "obligationId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "obligationId",
                "text"
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
      "name": "grant-compliance__deadline-extract",
      "description": "Extract grant deadlines. Read Deadline lines that contain a YYYY-MM-DD date. Other dates in the guidelines are not turned into deadlines. Docs: https://www.brainiac.software/api/grant-compliance/deadline-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "guidelines": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          }
        },
        "required": [
          "guidelines"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "grant-compliance__report",
      "description": "Prepare a grant compliance report. Combine the supplied requirement, eligibility, budget, evidence, deliverable, and reporting checks. The report does not approve the application or determine compliance. Docs: https://www.brainiac.software/api/grant-compliance/report",
      "parameters": {
        "type": "object",
        "properties": {
          "guidelines": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "requirements": {
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "rules": {
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
                "fact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "operator": {
                  "type": "string",
                  "enum": [
                    "equals",
                    "includes",
                    "number_at_least",
                    "number_at_most",
                    "boolean_is"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "id",
                "fact",
                "operator",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "facts": {
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
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "applicationText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "sections": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "requirementId",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          },
          "lines": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                }
              },
              "required": [
                "category",
                "description",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "total": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000000
          },
          "limits": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "maxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "maxPercent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                }
              },
              "required": [
                "category"
              ],
              "additionalProperties": false
            }
          },
          "expenses": {
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
                "description": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                }
              },
              "required": [
                "id",
                "description",
                "category",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "expenseRules": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "decision": {
                  "type": "string",
                  "enum": [
                    "eligible",
                    "ineligible"
                  ]
                }
              },
              "required": [
                "category",
                "decision"
              ],
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
                "requirementId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "deliverables": {
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
                  "minLength": 1,
                  "maxLength": 200
                },
                "dueDate": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                }
              },
              "required": [
                "id",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "updates": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "deliverableId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "not_started",
                    "in_progress",
                    "submitted",
                    "accepted_by_caller"
                  ]
                },
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "note": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "deliverableId",
                "status"
              ],
              "additionalProperties": false
            }
          },
          "obligations": {
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
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "id",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "reportText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "reportSections": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "obligationId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "obligationId",
                "text"
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
  "grant-compliance__requirements-extract": "0.04",
  "grant-compliance__eligibility-check": "0.04",
  "grant-compliance__application-completeness": "0.04",
  "grant-compliance__budget-validate": "0.05",
  "grant-compliance__expense-eligibility-check": "0.04",
  "grant-compliance__evidence-match": "0.05",
  "grant-compliance__deliverable-track": "0.03",
  "grant-compliance__report-validate": "0.04",
  "grant-compliance__deadline-extract": "0.03",
  "grant-compliance__report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "grant-compliance__requirements-extract": "grant-compliance/requirements-extract",
  "grant-compliance__eligibility-check": "grant-compliance/eligibility-check",
  "grant-compliance__application-completeness": "grant-compliance/application-completeness",
  "grant-compliance__budget-validate": "grant-compliance/budget-validate",
  "grant-compliance__expense-eligibility-check": "grant-compliance/expense-eligibility-check",
  "grant-compliance__evidence-match": "grant-compliance/evidence-match",
  "grant-compliance__deliverable-track": "grant-compliance/deliverable-track",
  "grant-compliance__report-validate": "grant-compliance/report-validate",
  "grant-compliance__deadline-extract": "grant-compliance/deadline-extract",
  "grant-compliance__report": "grant-compliance/report"
}


class BrainiacGrantComplianceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — grant-compliance",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the grant-compliance catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "grant-compliance", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract grant requirements"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the grant-compliance group. "
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
