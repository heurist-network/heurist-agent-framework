"""Auto-generated BRAINIAC Heurist Mesh agent for group `contract-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "contract-operations__clause-extract",
      "description": "Extract contract clauses. Extract numbered clauses, parties, defined terms, and a governing-law sentence from supplied contract text or a text-based PDF. Each item keeps a source excerpt. Missing headings stay unavailable. Docs: https://www.brainiac.software/api/contract-operations/clause-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
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
      "name": "contract-operations__obligation-extract",
      "description": "Extract contract obligations. Extract sentences that use shall, must, agrees to, is required to, or undertakes to, and name the party stated before the verb. Sentences that only say may are not turned into obligations. Docs: https://www.brainiac.software/api/contract-operations/obligation-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
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
      "name": "contract-operations__deadline-extract",
      "description": "Extract contract deadlines. Extract stated periods, notice periods, and unambiguous calendar dates. Slash dates are not guessed, and a deadline is not created when the text gives no number or date. Docs: https://www.brainiac.software/api/contract-operations/deadline-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
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
      "name": "contract-operations__renewal-risk-check",
      "description": "Check renewal wording. Read renewal and expiration wording that is actually printed. A notice date is calculated only from a stated expiration date and a stated notice period. Renewal wording is flagged as a potential risk, not a legal conclusion. Docs: https://www.brainiac.software/api/contract-operations/renewal-risk-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "withinDays": {
            "type": "integer",
            "minimum": 0,
            "maximum": 3650
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "contract-operations__missing-clause-check",
      "description": "Check for missing provisions. Compare the contract with a checklist or with provisions supplied for a named standard. A standard name alone does not create required clauses, and similar wording is not inferred. Docs: https://www.brainiac.software/api/contract-operations/missing-clause-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "checklist": {
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
                "phrases": {
                  "minItems": 1,
                  "maxItems": 8,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "id",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "standard": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "provisions": {
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
                    "phrases": {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "id",
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "name"
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
      "name": "contract-operations__version-diff",
      "description": "Compare contract versions. Compare two supplied contract versions by clause number or heading. Whitespace and letter case alone are not reported. Clauses are not matched by meaning. Docs: https://www.brainiac.software/api/contract-operations/version-diff",
      "parameters": {
        "type": "object",
        "properties": {
          "base": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "clauses": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "number": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "heading": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20000
                    }
                  },
                  "required": [
                    "heading",
                    "text"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "revised": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "clauses": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "number": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "heading": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20000
                    }
                  },
                  "required": [
                    "heading",
                    "text"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "base",
          "revised"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "contract-operations__change-impact",
      "description": "Describe contract changes. Label meaningful version changes as a date, a stated period, an obligation verb, or an added or removed clause. The legal effect of a change is not decided. Docs: https://www.brainiac.software/api/contract-operations/change-impact",
      "parameters": {
        "type": "object",
        "properties": {
          "base": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "clauses": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "number": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "heading": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20000
                    }
                  },
                  "required": [
                    "heading",
                    "text"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "revised": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "clauses": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "number": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "heading": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20000
                    }
                  },
                  "required": [
                    "heading",
                    "text"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "base",
          "revised"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "contract-operations__party-obligations",
      "description": "Group obligations by party. Group extracted obligations under the party named before shall, must, or agrees to. An obligation that names no party stays unassigned. Docs: https://www.brainiac.software/api/contract-operations/party-obligations",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
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
      "name": "contract-operations__risk-summary",
      "description": "Summarize contract wording risks. Flag renewal, indemnity, unlimited-liability, and termination-for-convenience wording that is present in the text. These are potential risks, not a legal opinion or a risk score. Docs: https://www.brainiac.software/api/contract-operations/risk-summary",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
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
      "name": "contract-operations__compliance-review",
      "description": "Review a contract against supplied checks. Combine clause, obligation, deadline, renewal, checklist, party, and risk checks. checklist_satisfied means the supplied phrases were found. It is not a legal compliance determination. Docs: https://www.brainiac.software/api/contract-operations/compliance-review",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
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
                  "application/pdf",
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
          "clauses": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "number": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "heading": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                }
              },
              "required": [
                "heading",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "checklist": {
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
                "phrases": {
                  "minItems": 1,
                  "maxItems": 8,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "id",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "standard": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "provisions": {
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
                    "phrases": {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "id",
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "name"
            ],
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "withinDays": {
            "type": "integer",
            "minimum": 0,
            "maximum": 3650
          },
          "revised": {
            "type": "object",
            "properties": {
              "text": {
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
                      "application/pdf",
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
              "clauses": {
                "maxItems": 80,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "number": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "heading": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20000
                    }
                  },
                  "required": [
                    "heading",
                    "text"
                  ],
                  "additionalProperties": false
                }
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
  "contract-operations__clause-extract": "0.06",
  "contract-operations__obligation-extract": "0.06",
  "contract-operations__deadline-extract": "0.05",
  "contract-operations__renewal-risk-check": "0.04",
  "contract-operations__missing-clause-check": "0.05",
  "contract-operations__version-diff": "0.08",
  "contract-operations__change-impact": "0.06",
  "contract-operations__party-obligations": "0.05",
  "contract-operations__risk-summary": "0.06",
  "contract-operations__compliance-review": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "contract-operations__clause-extract": "contract-operations/clause-extract",
  "contract-operations__obligation-extract": "contract-operations/obligation-extract",
  "contract-operations__deadline-extract": "contract-operations/deadline-extract",
  "contract-operations__renewal-risk-check": "contract-operations/renewal-risk-check",
  "contract-operations__missing-clause-check": "contract-operations/missing-clause-check",
  "contract-operations__version-diff": "contract-operations/version-diff",
  "contract-operations__change-impact": "contract-operations/change-impact",
  "contract-operations__party-obligations": "contract-operations/party-obligations",
  "contract-operations__risk-summary": "contract-operations/risk-summary",
  "contract-operations__compliance-review": "contract-operations/compliance-review"
}


class BrainiacContractOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — contract-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the contract-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "contract-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Extract contract clauses"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the contract-operations group. "
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
