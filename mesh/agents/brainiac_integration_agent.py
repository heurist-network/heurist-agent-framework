"""Auto-generated BRAINIAC Heurist Mesh agent for group `integration` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "integration__json-schema-generate",
      "description": "Generate a JSON schema. Build a schema from supplied examples. Required properties are keys present on every example. Whole numbers are integer. Additional properties stay allowed. Docs: https://www.brainiac.software/api/integration/json-schema-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__json-schema-validate",
      "description": "Validate a payload. Check a payload against a supplied schema using the documented subset. Each failure has a JSON pointer. Unsupported keywords are reported and not applied. Docs: https://www.brainiac.software/api/integration/json-schema-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__response-normalize",
      "description": "Normalize an API response. Trim string edges and sort object keys. Types are not changed, fields are not removed, and each change is listed. Docs: https://www.brainiac.software/api/integration/response-normalize",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__payload-transform",
      "description": "Transform a payload. Apply rename, copy, pick, omit, cast, and default in order. A missing source is reported and not invented. A default is written only when the path is absent. Docs: https://www.brainiac.software/api/integration/payload-transform",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__field-map-generate",
      "description": "Generate a field map. Map a path that exists on both sides, or a field name that matches one leaf on each side after splitting camel case and snake case. No value is copied. Docs: https://www.brainiac.software/api/integration/field-map-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__contract-compare",
      "description": "Compare API contracts. List schema changes. A change is labeled breaking or non-breaking only when side is request or response. Title and description are ignored. Docs: https://www.brainiac.software/api/integration/contract-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__version-compatibility-check",
      "description": "Check version compatibility. Order dotted numeric versions and compare the supplied schemas. A version number alone is not treated as compatible. The payload is checked against the later schema. Docs: https://www.brainiac.software/api/integration/version-compatibility-check",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
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
      "name": "integration__diagnose",
      "description": "Diagnose an integration. Generate a schema from examples, validate the payload, map fields that exist, compare contracts, and apply documented transforms. No external API is called. Docs: https://www.brainiac.software/api/integration/diagnose",
      "parameters": {
        "type": "object",
        "properties": {
          "payload": {},
          "example": {},
          "examples": {
            "maxItems": 20,
            "type": "array",
            "items": {}
          },
          "schema": {},
          "source": {},
          "target": {},
          "before": {},
          "after": {},
          "json": {
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
          "operations": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "rename"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "copy"
                    },
                    "from": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "to": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    }
                  },
                  "required": [
                    "op",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "pick"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "omit"
                    },
                    "paths": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    }
                  },
                  "required": [
                    "op",
                    "paths"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "cast"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "string",
                        "number",
                        "integer",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "op",
                    "path",
                    "type"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "op": {
                      "type": "string",
                      "const": "default"
                    },
                    "path": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "value": {}
                  },
                  "required": [
                    "op",
                    "path",
                    "value"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "side": {
            "type": "string",
            "enum": [
              "request",
              "response"
            ]
          },
          "fromVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "toVersion": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "integration__json-schema-generate": "0.04",
  "integration__json-schema-validate": "0.04",
  "integration__response-normalize": "0.03",
  "integration__payload-transform": "0.05",
  "integration__field-map-generate": "0.05",
  "integration__contract-compare": "0.05",
  "integration__version-compatibility-check": "0.04",
  "integration__diagnose": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "integration__json-schema-generate": "integration/json-schema-generate",
  "integration__json-schema-validate": "integration/json-schema-validate",
  "integration__response-normalize": "integration/response-normalize",
  "integration__payload-transform": "integration/payload-transform",
  "integration__field-map-generate": "integration/field-map-generate",
  "integration__contract-compare": "integration/contract-compare",
  "integration__version-compatibility-check": "integration/version-compatibility-check",
  "integration__diagnose": "integration/diagnose"
}


class BrainiacIntegrationAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — integration",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the integration catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "integration", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Generate a JSON schema"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the integration group. "
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
