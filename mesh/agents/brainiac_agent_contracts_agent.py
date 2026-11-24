"""Auto-generated BRAINIAC Heurist Mesh agent for group `agent-contracts` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "agent-contracts__expiry-contract-check",
      "description": "Check expiry contracts. Find presigned URLs and access tokens in caller-supplied operations that do not state a lifetime, and sentences that both expire and never expire. A missing lifetime is undocumented, not a live-server defect. Docs: https://www.brainiac.software/api/agent-contracts/expiry-contract-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__retry-safety-check",
      "description": "Check retry safety contracts. Read caller-supplied retry sentences and timeout statuses. A timeout with no retry sentence is missing documentation. The HTTP method is not treated as safe or unsafe to retry. Docs: https://www.brainiac.software/api/agent-contracts/retry-safety-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__idempotency-audit",
      "description": "Audit idempotency contracts. Find create or update sentences that do not name an idempotency key or a replay result. The check does not call an operation idempotent unless the supplied text says so, and POST alone is not proof of a write. Docs: https://www.brainiac.software/api/agent-contracts/idempotency-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__pagination-contract-check",
      "description": "Check pagination contracts. Find page or cursor operations in caller-supplied OpenAPI or tool definitions that omit the next-page field, the end condition, or which of cursor and offset to follow. Docs: https://www.brainiac.software/api/agent-contracts/pagination-contract-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__error-recovery-audit",
      "description": "Audit error recovery contracts. Check whether caller-supplied 4xx and 5xx responses name a code, message, or field an agent can correct. A missing error schema is undocumented, not proof the server never fails. Docs: https://www.brainiac.software/api/agent-contracts/error-recovery-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__output-contract-check",
      "description": "Check output contracts. Compare caller-supplied success examples with their output schemas for type, enum, required fields, and extra properties. A mismatch is a conflict between those documents, not a confirmed live response. Docs: https://www.brainiac.software/api/agent-contracts/output-contract-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__state-transition-check",
      "description": "Check state transition contracts. Find supplied workflow transitions that name an unknown state, two destinations for one trigger, or an operation that is not in the supplied list. Missing edges are undocumented, not proof a state is unreachable. Docs: https://www.brainiac.software/api/agent-contracts/state-transition-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-contracts__partial-failure-check",
      "description": "Check partial failure contracts. Find multi-step workflows that do not say whether a later failure leaves earlier steps in place, rolls them back, or can be retried. Atomic and partial success in the same text is a contract contradiction. Docs: https://www.brainiac.software/api/agent-contracts/partial-failure-check",
      "parameters": {
        "type": "object",
        "properties": {
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "method": {
                  "type": "string",
                  "maxLength": 16
                },
                "path": {
                  "type": "string",
                  "maxLength": 400
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "summary": {
                  "type": "string",
                  "maxLength": 1000
                },
                "parameters": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "in": {
                        "type": "string",
                        "enum": [
                          "query",
                          "header",
                          "path",
                          "cookie",
                          "body"
                        ]
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "required": {
                        "type": "boolean"
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "requestSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "outputSchema": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "maxLength": 80
                  },
                  "additionalProperties": {}
                },
                "responses": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "status": {
                        "type": "string",
                        "maxLength": 40
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "schema": {
                        "type": "object",
                        "propertyNames": {
                          "type": "string",
                          "maxLength": 80
                        },
                        "additionalProperties": {}
                      },
                      "example": {},
                      "examples": {
                        "maxItems": 8,
                        "type": "array",
                        "items": {}
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "examples": {
                  "maxItems": 8,
                  "type": "array",
                  "items": {}
                },
                "steps": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 200
                  }
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "workflows": {
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 160
                },
                "description": {
                  "type": "string",
                  "maxLength": 8000
                },
                "states": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                },
                "transitions": {
                  "maxItems": 80,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "from": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "to": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
                      },
                      "on": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "from",
                      "to"
                    ],
                    "additionalProperties": false
                  }
                },
                "steps": {
                  "maxItems": 30,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 160
                      },
                      "description": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "operation": {
                        "type": "string",
                        "maxLength": 160
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
                "name"
              ],
              "additionalProperties": false
            }
          },
          "openapi": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "maxLength": 80
            },
            "additionalProperties": {}
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "agent-contracts__expiry-contract-check": "0.03",
  "agent-contracts__retry-safety-check": "0.03",
  "agent-contracts__idempotency-audit": "0.04",
  "agent-contracts__pagination-contract-check": "0.03",
  "agent-contracts__error-recovery-audit": "0.04",
  "agent-contracts__output-contract-check": "0.04",
  "agent-contracts__state-transition-check": "0.04",
  "agent-contracts__partial-failure-check": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "agent-contracts__expiry-contract-check": "agent-contracts/expiry-contract-check",
  "agent-contracts__retry-safety-check": "agent-contracts/retry-safety-check",
  "agent-contracts__idempotency-audit": "agent-contracts/idempotency-audit",
  "agent-contracts__pagination-contract-check": "agent-contracts/pagination-contract-check",
  "agent-contracts__error-recovery-audit": "agent-contracts/error-recovery-audit",
  "agent-contracts__output-contract-check": "agent-contracts/output-contract-check",
  "agent-contracts__state-transition-check": "agent-contracts/state-transition-check",
  "agent-contracts__partial-failure-check": "agent-contracts/partial-failure-check"
}


class BrainiacAgentContractsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — agent-contracts",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the agent-contracts catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "agent-contracts", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Check expiry contracts"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the agent-contracts group. "
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
