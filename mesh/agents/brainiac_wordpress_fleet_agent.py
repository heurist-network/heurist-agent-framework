"""Auto-generated BRAINIAC Heurist Mesh agent for group `wordpress-fleet` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "wordpress-fleet__site-inventory-normalize",
      "description": "Normalize a WordPress site inventory. Copy supplied sites, plugins, and themes into a consistent inventory. Counts come from the request only. No site is logged into. Docs: https://www.brainiac.software/api/wordpress-fleet/site-inventory-normalize",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__plugin-version-audit",
      "description": "Audit WordPress plugin versions. Compare installed plugin versions with caller-supplied or WordPress.org public releases. An older version is a version-age warning. A vulnerability is listed only when the caller supplied it. Docs: https://www.brainiac.software/api/wordpress-fleet/plugin-version-audit",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__theme-version-audit",
      "description": "Audit WordPress theme versions. Compare installed theme versions with caller-supplied or WordPress.org public releases. An older version is a version-age warning, not a confirmed vulnerability. Docs: https://www.brainiac.software/api/wordpress-fleet/theme-version-audit",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__update-compatibility-check",
      "description": "Check update compatibility metadata. Compare a site's stated WordPress and PHP versions with public requires and tested fields. A match is not treated as proof that an update is safe. Docs: https://www.brainiac.software/api/wordpress-fleet/update-compatibility-check",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__plugin-conflict-detect",
      "description": "Detect possible plugin conflicts. Flag duplicate active plugin slugs and caller-supplied conflict pairs. A match is not a confirmed runtime conflict. Docs: https://www.brainiac.software/api/wordpress-fleet/plugin-conflict-detect",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__site-maintenance-priority",
      "description": "Prioritize site maintenance. Rank supplied sites by outdated software, caller-supplied vulnerability matches, compatibility gaps, and conflict flags. The ranking does not approve an update. Docs: https://www.brainiac.software/api/wordpress-fleet/site-maintenance-priority",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__risk-analyze",
      "description": "Analyze WordPress fleet risk. Summarize version-age warnings and caller-supplied vulnerability matches across the inventory. Version age is not treated as a confirmed vulnerability. Docs: https://www.brainiac.software/api/wordpress-fleet/risk-analyze",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "wordpress-fleet__agency-report",
      "description": "Report a WordPress agency fleet. Combine the inventory, version audits, compatibility metadata, conflict flags, and maintenance priorities. The report does not log into sites or install updates. Docs: https://www.brainiac.software/api/wordpress-fleet/agency-report",
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
          "sites": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "wordpress": {
                  "type": "string",
                  "maxLength": 40
                },
                "php": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "additionalProperties": false
            }
          },
          "plugins": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "themes": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "siteId": {
                  "type": "string",
                  "maxLength": 80
                },
                "slug": {
                  "type": "string",
                  "maxLength": 120
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "active": {
                  "type": "boolean"
                }
              },
              "additionalProperties": false
            }
          },
          "publicCatalog": {
            "maxItems": 80,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 40
                },
                "requires": {
                  "type": "string",
                  "maxLength": 40
                },
                "tested": {
                  "type": "string",
                  "maxLength": 40
                },
                "requiresPhp": {
                  "type": "string",
                  "maxLength": 40
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "vulnerabilities": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "plugin",
                    "theme"
                  ]
                },
                "slug": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fixedIn": {
                  "type": "string",
                  "maxLength": 40
                },
                "cve": {
                  "type": "string",
                  "maxLength": 40
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "slug"
              ],
              "additionalProperties": false
            }
          },
          "conflicts": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "left": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "right": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "maxLength": 300
                }
              },
              "required": [
                "left",
                "right"
              ],
              "additionalProperties": false
            }
          },
          "fetchPublic": {
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "wordpress-fleet__site-inventory-normalize": "0.04",
  "wordpress-fleet__plugin-version-audit": "0.05",
  "wordpress-fleet__theme-version-audit": "0.05",
  "wordpress-fleet__update-compatibility-check": "0.05",
  "wordpress-fleet__plugin-conflict-detect": "0.04",
  "wordpress-fleet__site-maintenance-priority": "0.04",
  "wordpress-fleet__risk-analyze": "0.05",
  "wordpress-fleet__agency-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "wordpress-fleet__site-inventory-normalize": "wordpress-fleet/site-inventory-normalize",
  "wordpress-fleet__plugin-version-audit": "wordpress-fleet/plugin-version-audit",
  "wordpress-fleet__theme-version-audit": "wordpress-fleet/theme-version-audit",
  "wordpress-fleet__update-compatibility-check": "wordpress-fleet/update-compatibility-check",
  "wordpress-fleet__plugin-conflict-detect": "wordpress-fleet/plugin-conflict-detect",
  "wordpress-fleet__site-maintenance-priority": "wordpress-fleet/site-maintenance-priority",
  "wordpress-fleet__risk-analyze": "wordpress-fleet/risk-analyze",
  "wordpress-fleet__agency-report": "wordpress-fleet/agency-report"
}


class BrainiacWordpressFleetAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — wordpress-fleet",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the wordpress-fleet catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "wordpress-fleet", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize a WordPress site inventory"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the wordpress-fleet group. "
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
