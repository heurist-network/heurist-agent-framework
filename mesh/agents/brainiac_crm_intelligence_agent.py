"""Auto-generated BRAINIAC Heurist Mesh agent for group `crm-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "crm-intelligence__contact-normalize",
      "description": "Normalize CRM contacts. Normalize names, emails, phone numbers, company names, and addresses from a CSV or JSON contact export. Original values stay beside the normalized values. Docs: https://www.brainiac.software/api/crm-intelligence/contact-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crm-intelligence__company-normalize",
      "description": "Normalize CRM companies. Normalize company names, domains, phone numbers, and addresses from a CSV or JSON company export. A trailing legal suffix stays in the name and is used only as a match key. Docs: https://www.brainiac.software/api/crm-intelligence/company-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "companies": {
            "maxItems": 500,
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
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crm-intelligence__duplicate-contact-detect",
      "description": "Detect duplicate contacts. Find duplicate contacts with explainable rules and confidence levels. Different email addresses are not treated as the same person. Safe merge suggestions copy only empty fields and do not change a CRM. Docs: https://www.brainiac.software/api/crm-intelligence/duplicate-contact-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crm-intelligence__duplicate-company-detect",
      "description": "Detect duplicate companies. Find duplicate companies by a normalized domain or company-name key, and flag fuzzy name matches with a confidence level. Different domains are not merged. Suggestions do not change a CRM. Docs: https://www.brainiac.software/api/crm-intelligence/duplicate-company-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "companies": {
            "maxItems": 500,
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
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crm-intelligence__record-enrichment-from-input",
      "description": "Enrich CRM records from input. Copy caller-supplied facts into empty contact fields. A fact never overwrites a value that is already present, and no contact detail is invented. Docs: https://www.brainiac.software/api/crm-intelligence/record-enrichment-from-input",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "facts": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "match": {
                  "type": "string",
                  "enum": [
                    "email",
                    "domain",
                    "company"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "match",
                "value"
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
      "name": "crm-intelligence__data-quality-audit",
      "description": "Audit CRM data quality. Report missing names, invalid emails, short phone numbers, missing companies, and duplicate records. A company is not inferred from an email domain. Docs: https://www.brainiac.software/api/crm-intelligence/data-quality-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "companies": {
            "maxItems": 500,
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
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
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
      "name": "crm-intelligence__contact-relationship-match",
      "description": "Match contacts to companies. Link each contact to a company that was supplied in the same request, by company-name key or email domain. A company that was not supplied is not created. Docs: https://www.brainiac.software/api/crm-intelligence/contact-relationship-match",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "companies": {
            "maxItems": 500,
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
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "crm-intelligence__database-cleanup-report",
      "description": "Report a CRM cleanup. Combine normalized records, duplicate pairs, safe merge suggestions, caller-fact enrichment, relationship matches, and quality issues. No external CRM is changed. Docs: https://www.brainiac.software/api/crm-intelligence/database-cleanup-report",
      "parameters": {
        "type": "object",
        "properties": {
          "contacts": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "fullName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "csv": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200000
          },
          "json": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "application/json",
                  "text/plain"
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
          "companies": {
            "maxItems": 500,
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
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "additionalProperties": false
            }
          },
          "facts": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "match": {
                  "type": "string",
                  "enum": [
                    "email",
                    "domain",
                    "company"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "company": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "industry": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "street": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "city": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "postalCode": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "country": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "match",
                "value"
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
  "crm-intelligence__contact-normalize": "0.03",
  "crm-intelligence__company-normalize": "0.03",
  "crm-intelligence__duplicate-contact-detect": "0.05",
  "crm-intelligence__duplicate-company-detect": "0.05",
  "crm-intelligence__record-enrichment-from-input": "0.04",
  "crm-intelligence__data-quality-audit": "0.04",
  "crm-intelligence__contact-relationship-match": "0.05",
  "crm-intelligence__database-cleanup-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "crm-intelligence__contact-normalize": "crm-intelligence/contact-normalize",
  "crm-intelligence__company-normalize": "crm-intelligence/company-normalize",
  "crm-intelligence__duplicate-contact-detect": "crm-intelligence/duplicate-contact-detect",
  "crm-intelligence__duplicate-company-detect": "crm-intelligence/duplicate-company-detect",
  "crm-intelligence__record-enrichment-from-input": "crm-intelligence/record-enrichment-from-input",
  "crm-intelligence__data-quality-audit": "crm-intelligence/data-quality-audit",
  "crm-intelligence__contact-relationship-match": "crm-intelligence/contact-relationship-match",
  "crm-intelligence__database-cleanup-report": "crm-intelligence/database-cleanup-report"
}


class BrainiacCrmIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — crm-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the crm-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "crm-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize CRM contacts"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the crm-intelligence group. "
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
