"""Auto-generated BRAINIAC Heurist Mesh agent for group `vendor-compliance` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "vendor-compliance__onboarding-precheck",
      "description": "Precheck vendor onboarding. Compare a supplied vendor record, document list, and attestations with the buyer requirements. Missing, expired, failed, and unverified items are reported separately. Docs: https://www.brainiac.software/api/vendor-compliance/onboarding-precheck",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "vendor": {
            "type": "object",
            "properties": {
              "legalName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "identifierPresent": {
                "type": "boolean"
              },
              "contactName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "contactEmail": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 300
              },
              "yearsInBusiness": {
                "type": "number",
                "minimum": 0,
                "maximum": 200
              },
              "bondingCapacity": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "safetyRecord": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              }
            },
            "required": [
              "legalName"
            ],
            "additionalProperties": false
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "attestations": {
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
                "statement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "accepted": {
                  "type": "boolean"
                },
                "acceptedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "statement",
                "accepted"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "vendor"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vendor-compliance__contractor-prequalification",
      "description": "Prequalify a contractor. Compare buyer qualification criteria with supplied vendor facts, documents, and evidence. The result does not award eligibility or query a registry. Docs: https://www.brainiac.software/api/vendor-compliance/contractor-prequalification",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "vendor": {
            "type": "object",
            "properties": {
              "legalName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "identifierPresent": {
                "type": "boolean"
              },
              "contactName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "contactEmail": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 300
              },
              "yearsInBusiness": {
                "type": "number",
                "minimum": 0,
                "maximum": 200
              },
              "bondingCapacity": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "safetyRecord": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              }
            },
            "required": [
              "legalName"
            ],
            "additionalProperties": false
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
          },
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
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
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "vendor",
          "requirements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vendor-compliance__subcontractor-payment-readiness",
      "description": "Check subcontractor payment readiness. List missing payment documents and caller-supplied open items. This check does not release a payment or rerun sanctions, wage, or certificate screens. Docs: https://www.brainiac.software/api/vendor-compliance/subcontractor-payment-readiness",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "vendor": {
            "type": "object",
            "properties": {
              "legalName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "identifierPresent": {
                "type": "boolean"
              },
              "contactName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "contactEmail": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 300
              },
              "yearsInBusiness": {
                "type": "number",
                "minimum": 0,
                "maximum": 200
              },
              "bondingCapacity": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "safetyRecord": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              }
            },
            "required": [
              "legalName"
            ],
            "additionalProperties": false
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
          },
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openItems": {
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
                "status": {
                  "type": "string",
                  "enum": [
                    "satisfied",
                    "missing_evidence",
                    "expired",
                    "failed",
                    "not_verified"
                  ]
                }
              },
              "required": [
                "id",
                "name",
                "status"
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
      "name": "vendor-compliance__document-completeness",
      "description": "Check vendor document completeness. Compare a supplied document inventory with a buyer requirements list. Files are not fetched, and a present document is not treated as verified content. Docs: https://www.brainiac.software/api/vendor-compliance/document-completeness",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
          },
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "documents",
          "requirements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "vendor-compliance__report",
      "description": "Build a vendor compliance report. Consolidate supplied vendor information, documents, attestations, evidence, and open items into one requirements report. External registries are not contacted. Docs: https://www.brainiac.software/api/vendor-compliance/report",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "vendor": {
            "type": "object",
            "properties": {
              "legalName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "identifierPresent": {
                "type": "boolean"
              },
              "contactName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "contactEmail": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 300
              },
              "yearsInBusiness": {
                "type": "number",
                "minimum": 0,
                "maximum": 200
              },
              "bondingCapacity": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "safetyRecord": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              }
            },
            "required": [
              "legalName"
            ],
            "additionalProperties": false
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "attestations": {
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
                "statement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "accepted": {
                  "type": "boolean"
                },
                "acceptedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "statement",
                "accepted"
              ],
              "additionalProperties": false
            }
          },
          "evidence": {
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
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "openItems": {
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
                "status": {
                  "type": "string",
                  "enum": [
                    "satisfied",
                    "missing_evidence",
                    "expired",
                    "failed",
                    "not_verified"
                  ]
                }
              },
              "required": [
                "id",
                "name",
                "status"
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
      "name": "vendor-compliance__contractor-closeout-check",
      "description": "Check contractor closeout. Compare buyer closeout requirements with supplied documents and attestations. A passing result does not certify that the project is complete. Docs: https://www.brainiac.software/api/vendor-compliance/contractor-closeout-check",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "vendor": {
            "type": "object",
            "properties": {
              "legalName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "reference": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "country": {
                "type": "string",
                "minLength": 2,
                "maxLength": 80
              },
              "identifierPresent": {
                "type": "boolean"
              },
              "contactName": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "contactEmail": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 300
              },
              "yearsInBusiness": {
                "type": "number",
                "minimum": 0,
                "maximum": 200
              },
              "bondingCapacity": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "safetyRecord": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              }
            },
            "required": [
              "legalName"
            ],
            "additionalProperties": false
          },
          "documents": {
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
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "issuedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expiresOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "completedCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "certificateFields": {
                  "maxItems": 40,
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
                        "maxLength": 200
                      },
                      "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "type"
              ],
              "additionalProperties": false
            }
          },
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
                "kind": {
                  "type": "string",
                  "enum": [
                    "field",
                    "document",
                    "insurance",
                    "licence",
                    "attestation",
                    "criterion"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "required": {
                  "type": "boolean"
                },
                "field": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "documentType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "documentId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "evidenceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "expiresAfter": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "jurisdiction": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "licenseType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "minCeHours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000
                },
                "minimum": {
                  "type": "number"
                },
                "expected": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "insurance": {
                  "type": "object",
                  "properties": {
                    "namedInsured": {
                      "type": "string",
                      "maxLength": 200
                    },
                    "effectiveOn": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "expiresAfter": {
                      "type": "string",
                      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                    },
                    "generalLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "workersCompensation": {
                      "type": "object",
                      "properties": {
                        "statutory": {
                          "type": "boolean"
                        },
                        "employerLiability": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "automobileLiability": {
                      "type": "object",
                      "properties": {
                        "combinedSingleLimit": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "umbrellaLiability": {
                      "type": "object",
                      "properties": {
                        "eachOccurrence": {
                          "type": "number",
                          "minimum": 0
                        },
                        "aggregate": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "additionalProperties": false
                    },
                    "additionalInsured": {
                      "type": "boolean"
                    },
                    "waiverOfSubrogation": {
                      "type": "boolean"
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "attestations": {
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
                "statement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "accepted": {
                  "type": "boolean"
                },
                "acceptedOn": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "statement",
                "accepted"
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "vendor-compliance__onboarding-precheck": "0.04",
  "vendor-compliance__contractor-prequalification": "0.05",
  "vendor-compliance__subcontractor-payment-readiness": "0.04",
  "vendor-compliance__document-completeness": "0.03",
  "vendor-compliance__report": "0.08",
  "vendor-compliance__contractor-closeout-check": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "vendor-compliance__onboarding-precheck": "vendor-compliance/onboarding-precheck",
  "vendor-compliance__contractor-prequalification": "vendor-compliance/contractor-prequalification",
  "vendor-compliance__subcontractor-payment-readiness": "vendor-compliance/subcontractor-payment-readiness",
  "vendor-compliance__document-completeness": "vendor-compliance/document-completeness",
  "vendor-compliance__report": "vendor-compliance/report",
  "vendor-compliance__contractor-closeout-check": "vendor-compliance/contractor-closeout-check"
}


class BrainiacVendorComplianceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — vendor-compliance",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the vendor-compliance catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "vendor-compliance", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Precheck vendor onboarding"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the vendor-compliance group. "
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
