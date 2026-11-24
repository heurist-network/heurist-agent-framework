"""Auto-generated BRAINIAC Heurist Mesh agent for group `threat-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "threat-intelligence__public-threat-feed-aggregate",
      "description": "Aggregate public threat feeds. Aggregate caller-supplied and verified key-free public threat feeds (CISA KEV, OpenPhish, capped PhishTank). URLhaus/ThreatFox require auth and are not queried. Feed hits are not confirmed malice. Docs: https://www.brainiac.software/api/threat-intelligence/public-threat-feed-aggregate",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__ioc-context-enrich",
      "description": "Enrich IoC context. Enrich supplied IPs, domains, URLs, and hashes using caller context plus optional public DNS/feeds. A single weak feed hit is never classified as malicious. Docs: https://www.brainiac.software/api/threat-intelligence/ioc-context-enrich",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__domain-threat-history",
      "description": "Analyze domain threat history. Analyze publicly accessible domain history and DNS/RDAP context from caller fields and optional key-free public lookups. History attributes alone are not malice. Docs: https://www.brainiac.software/api/threat-intelligence/domain-threat-history",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__certificate-threat-cluster",
      "description": "Cluster certificate relationships. Identify relationships between domains using caller-supplied certificates and optional public crt.sh data. Shared certificate attributes are linkage evidence, not confirmed abuse. Docs: https://www.brainiac.software/api/threat-intelligence/certificate-threat-cluster",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__typosquatting-domain-detect",
      "description": "Detect typosquat domains. Identify domains resembling supplied brand or company domains using local string/keyboard heuristics. Resemblance alone is not confirmed phishing. Docs: https://www.brainiac.software/api/threat-intelligence/typosquatting-domain-detect",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__phishing-infrastructure-cluster",
      "description": "Cluster phishing infrastructure. Group related phishing domains and infrastructure using caller evidence and optional public phishing feeds. Clusters are relationship hypotheses, not confirmed campaigns. Docs: https://www.brainiac.software/api/threat-intelligence/phishing-infrastructure-cluster",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__exposed-service-risk-analyze",
      "description": "Analyze exposed service risk. Analyze caller-supplied external service inventory and scan results for exposure risk. Never initiates intrusive network scanning. Docs: https://www.brainiac.software/api/threat-intelligence/exposed-service-risk-analyze",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "threat-intelligence__threat-indicator-confidence-score",
      "description": "Score threat-indicator confidence. Calculate explainable confidence scores for supplied threat indicators using multi-source corroboration. Single weak signals are capped and never claimed as confirmed malice. Docs: https://www.brainiac.software/api/threat-intelligence/threat-indicator-confidence-score",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "indicators": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "email",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "firstSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "lastSeen": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "confidenceHint": {
                  "type": "string",
                  "enum": [
                    "low",
                    "medium",
                    "high"
                  ]
                },
                "relatedIds": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "feeds": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "feed": {
                  "type": "string",
                  "maxLength": 80
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "cve",
                    "other"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "tags": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                },
                "url": {
                  "type": "string",
                  "maxLength": 2000
                }
              },
              "required": [
                "value"
              ],
              "additionalProperties": false
            }
          },
          "domains": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "brand": {
                  "type": "string",
                  "maxLength": 120
                },
                "registrar": {
                  "type": "string",
                  "maxLength": 200
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "expiresAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameservers": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "ips": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "asn": {
                  "type": "string",
                  "maxLength": 40
                },
                "hostingProvider": {
                  "type": "string",
                  "maxLength": 120
                },
                "certificateFingerprint": {
                  "type": "string",
                  "maxLength": 120
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "domain"
              ],
              "additionalProperties": false
            }
          },
          "certificates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "domain": {
                  "type": "string",
                  "maxLength": 253
                },
                "commonName": {
                  "type": "string",
                  "maxLength": 253
                },
                "issuer": {
                  "type": "string",
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "maxLength": 40
                },
                "notAfter": {
                  "type": "string",
                  "maxLength": 40
                },
                "fingerprintSha256": {
                  "type": "string",
                  "maxLength": 120
                },
                "serialNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "sans": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "services": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "host": {
                  "type": "string",
                  "maxLength": 253
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "port": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "maxLength": 40
                },
                "service": {
                  "type": "string",
                  "maxLength": 80
                },
                "product": {
                  "type": "string",
                  "maxLength": 120
                },
                "version": {
                  "type": "string",
                  "maxLength": 80
                },
                "banner": {
                  "type": "string",
                  "maxLength": 2000
                },
                "tls": {
                  "type": "boolean"
                },
                "exposure": {
                  "type": "string",
                  "enum": [
                    "public",
                    "internal",
                    "unknown"
                  ]
                },
                "cveIds": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 40
                  }
                },
                "observedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "brands": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "brand": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "domains": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "brand"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 253
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "fetchCisaKev": {
            "type": "boolean"
          },
          "fetchOpenPhish": {
            "type": "boolean"
          },
          "fetchPhishTank": {
            "type": "boolean"
          },
          "fetchCrtSh": {
            "type": "boolean"
          },
          "fetchRdap": {
            "type": "boolean"
          },
          "publicDns": {
            "type": "boolean"
          },
          "staleDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "crtShQuery": {
            "type": "string",
            "maxLength": 253
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "threat-intelligence__public-threat-feed-aggregate": "0.05",
  "threat-intelligence__ioc-context-enrich": "0.04",
  "threat-intelligence__domain-threat-history": "0.04",
  "threat-intelligence__certificate-threat-cluster": "0.04",
  "threat-intelligence__typosquatting-domain-detect": "0.03",
  "threat-intelligence__phishing-infrastructure-cluster": "0.04",
  "threat-intelligence__exposed-service-risk-analyze": "0.04",
  "threat-intelligence__threat-indicator-confidence-score": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "threat-intelligence__public-threat-feed-aggregate": "threat-intelligence/public-threat-feed-aggregate",
  "threat-intelligence__ioc-context-enrich": "threat-intelligence/ioc-context-enrich",
  "threat-intelligence__domain-threat-history": "threat-intelligence/domain-threat-history",
  "threat-intelligence__certificate-threat-cluster": "threat-intelligence/certificate-threat-cluster",
  "threat-intelligence__typosquatting-domain-detect": "threat-intelligence/typosquatting-domain-detect",
  "threat-intelligence__phishing-infrastructure-cluster": "threat-intelligence/phishing-infrastructure-cluster",
  "threat-intelligence__exposed-service-risk-analyze": "threat-intelligence/exposed-service-risk-analyze",
  "threat-intelligence__threat-indicator-confidence-score": "threat-intelligence/threat-indicator-confidence-score"
}


class BrainiacThreatIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — threat-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the threat-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "threat-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Aggregate public threat feeds"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the threat-intelligence group. "
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
