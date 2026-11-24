"""Auto-generated BRAINIAC Heurist Mesh agent for group `customer-support` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "customer-support__ticket-classify",
      "description": "Classify support tickets. Classify supplied tickets into billing, access, outage, defect, delivery, or account when one documented keyword list has the most matches. A caller-supplied category list replaces that set. A tie stays unclassified. Docs: https://www.brainiac.software/api/customer-support/ticket-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__ticket-prioritize",
      "description": "Prioritize support tickets. Set priority from a supplied severity and from documented urgency and business-impact phrases. A ticket with none of those signals stays unspecified. Docs: https://www.brainiac.software/api/customer-support/ticket-prioritize",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__ticket-deduplicate",
      "description": "Detect duplicate tickets. Find duplicate tickets for the same email address and repeated wording across customers. Each pair names the rule and a confidence level. Tickets are not merged. Docs: https://www.brainiac.software/api/customer-support/ticket-deduplicate",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__conversation-summarize",
      "description": "Summarize a support conversation. Restate up to three customer sentences and quote supplied agent replies. The summary does not decide that a ticket was resolved. Docs: https://www.brainiac.software/api/customer-support/conversation-summarize",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__sentiment-analyze",
      "description": "Analyze ticket sentiment. Label customer wording with a documented positive and negative word list. Text with no listed words stays unspecified. Docs: https://www.brainiac.software/api/customer-support/sentiment-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__resolution-suggest",
      "description": "Draft a support reply. Draft a reply that quotes the customer and a supplied policy only when that policy shares a word with the ticket. The draft does not resolve the ticket or state an unsupplied policy. Docs: https://www.brainiac.software/api/customer-support/resolution-suggest",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__escalation-detect",
      "description": "Detect escalation signals. Flag a ticket when the text contains a documented escalation phrase, the priority rules mark it critical, or the same email appears on three tickets in the request. No escalation is performed. Docs: https://www.brainiac.software/api/customer-support/escalation-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
      "name": "customer-support__quality-audit",
      "description": "Audit support reply quality. Check supplied replies for a resolution claim, a missing reply, or an email, amount, order, or policy that was not in the ticket. The audit does not confirm that any action happened. Docs: https://www.brainiac.software/api/customer-support/quality-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "tickets": {
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
                "subject": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "body": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "email": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 254
                },
                "customer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "severity": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "impact": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "reply": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "orderId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8000
                },
                "messages": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": {
                        "type": "string",
                        "enum": [
                          "customer",
                          "agent",
                          "system"
                        ]
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000
                      }
                    },
                    "required": [
                      "role",
                      "text"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "messages": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "role": {
                  "type": "string",
                  "enum": [
                    "customer",
                    "agent",
                    "system"
                  ]
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 4000
                }
              },
              "required": [
                "role",
                "text"
              ],
              "additionalProperties": false
            }
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
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
          "categories": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 60
                },
                "keywords": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  }
                }
              },
              "required": [
                "name",
                "keywords"
              ],
              "additionalProperties": false
            }
          },
          "policies": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
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
  }
]
TOOL_PRICES: Dict[str, str] = {
  "customer-support__ticket-classify": "0.03",
  "customer-support__ticket-prioritize": "0.04",
  "customer-support__ticket-deduplicate": "0.05",
  "customer-support__conversation-summarize": "0.04",
  "customer-support__sentiment-analyze": "0.03",
  "customer-support__resolution-suggest": "0.05",
  "customer-support__escalation-detect": "0.04",
  "customer-support__quality-audit": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "customer-support__ticket-classify": "customer-support/ticket-classify",
  "customer-support__ticket-prioritize": "customer-support/ticket-prioritize",
  "customer-support__ticket-deduplicate": "customer-support/ticket-deduplicate",
  "customer-support__conversation-summarize": "customer-support/conversation-summarize",
  "customer-support__sentiment-analyze": "customer-support/sentiment-analyze",
  "customer-support__resolution-suggest": "customer-support/resolution-suggest",
  "customer-support__escalation-detect": "customer-support/escalation-detect",
  "customer-support__quality-audit": "customer-support/quality-audit"
}


class BrainiacCustomerSupportAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — customer-support",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the customer-support catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "customer-support", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Classify support tickets"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the customer-support group. "
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
