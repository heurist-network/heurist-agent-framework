"""Auto-generated BRAINIAC Heurist Mesh agent for group `domain-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "domain-security__domain-infrastructure-consistency-audit",
      "description": "Audit domain infrastructure consistency. Compare caller-supplied DNS answers, certificate names, addresses, prefixes, and RPKI results for one domain. audit_status is consistent, inconsistencies_detected, warnings, or incomplete. risk_level is low, medium, high, or critical. No DNS, TLS, WHOIS, or BGP lookup is performed. Docs: https://www.brainiac.software/api/domain-security/domain-infrastructure-consistency-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "checkedAt": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
          },
          "snapshot": {
            "type": "object",
            "properties": {
              "records": {
                "maxItems": 128,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "enum": [
                        "A",
                        "AAAA",
                        "CNAME",
                        "MX",
                        "NS",
                        "TXT"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 253
                    },
                    "value": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 1024
                    },
                    "preference": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 65535
                    }
                  },
                  "required": [
                    "type",
                    "name",
                    "value"
                  ],
                  "additionalProperties": false
                }
              },
              "certificates": {
                "maxItems": 8,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "sans": {
                      "maxItems": 64,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 253
                      }
                    },
                    "issuer": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "notBefore": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    },
                    "notAfter": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    },
                    "fingerprint": {
                      "type": "string",
                      "minLength": 32,
                      "maxLength": 95
                    }
                  },
                  "required": [
                    "sans"
                  ],
                  "additionalProperties": false
                }
              },
              "addresses": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "ip": {
                      "type": "string",
                      "minLength": 2,
                      "maxLength": 45
                    },
                    "source": {
                      "type": "string",
                      "enum": [
                        "dns",
                        "observed",
                        "origin"
                      ]
                    }
                  },
                  "required": [
                    "ip"
                  ],
                  "additionalProperties": false
                }
              },
              "prefixes": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "prefix": {
                      "type": "string",
                      "minLength": 3,
                      "maxLength": 49
                    },
                    "asn": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 4294967295
                    },
                    "rpki": {
                      "type": "string",
                      "enum": [
                        "valid",
                        "invalid",
                        "not_found"
                      ]
                    }
                  },
                  "required": [
                    "prefix"
                  ],
                  "additionalProperties": false
                }
              },
              "owners": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "ip": {
                      "type": "string",
                      "minLength": 2,
                      "maxLength": 45
                    },
                    "asn": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 4294967295
                    },
                    "provider": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    }
                  },
                  "required": [
                    "ip"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "records",
              "certificates",
              "addresses",
              "prefixes"
            ],
            "additionalProperties": false
          },
          "previous": {
            "type": "object",
            "properties": {
              "records": {
                "maxItems": 128,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "enum": [
                        "A",
                        "AAAA",
                        "CNAME",
                        "MX",
                        "NS",
                        "TXT"
                      ]
                    },
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 253
                    },
                    "value": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 1024
                    },
                    "preference": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 65535
                    }
                  },
                  "required": [
                    "type",
                    "name",
                    "value"
                  ],
                  "additionalProperties": false
                }
              },
              "certificates": {
                "maxItems": 8,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "sans": {
                      "maxItems": 64,
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 253
                      }
                    },
                    "issuer": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "notBefore": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    },
                    "notAfter": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    },
                    "fingerprint": {
                      "type": "string",
                      "minLength": 32,
                      "maxLength": 95
                    }
                  },
                  "required": [
                    "sans"
                  ],
                  "additionalProperties": false
                }
              },
              "addresses": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "ip": {
                      "type": "string",
                      "minLength": 2,
                      "maxLength": 45
                    },
                    "source": {
                      "type": "string",
                      "enum": [
                        "dns",
                        "observed",
                        "origin"
                      ]
                    }
                  },
                  "required": [
                    "ip"
                  ],
                  "additionalProperties": false
                }
              },
              "prefixes": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "prefix": {
                      "type": "string",
                      "minLength": 3,
                      "maxLength": 49
                    },
                    "asn": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 4294967295
                    },
                    "rpki": {
                      "type": "string",
                      "enum": [
                        "valid",
                        "invalid",
                        "not_found"
                      ]
                    }
                  },
                  "required": [
                    "prefix"
                  ],
                  "additionalProperties": false
                }
              },
              "owners": {
                "maxItems": 64,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "ip": {
                      "type": "string",
                      "minLength": 2,
                      "maxLength": 45
                    },
                    "asn": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 4294967295
                    },
                    "provider": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 80
                    }
                  },
                  "required": [
                    "ip"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "records",
              "certificates",
              "addresses",
              "prefixes"
            ],
            "additionalProperties": false
          },
          "expected": {
            "type": "object",
            "properties": {
              "providers": {
                "maxItems": 16,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "asns": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 4294967295
                }
              },
              "ranges": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 49
                }
              },
              "names": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              },
              "issuers": {
                "maxItems": 8,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "nameservers": {
                "maxItems": 16,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              },
              "mailHosts": {
                "maxItems": 16,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              }
            },
            "additionalProperties": false
          },
          "edge": {
            "type": "object",
            "properties": {
              "providers": {
                "maxItems": 16,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "asns": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 4294967295
                }
              },
              "ranges": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 3,
                  "maxLength": 49
                }
              },
              "hosts": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "domain",
          "snapshot"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "domain-security__infrastructure-health",
      "description": "Grade domain snapshot health. Look through the supplied DNS records, certificate names, expiry date, and cipher names. A CNAME whose target has no A or AAAA in the snapshot, a certificate that omits the domain, an expiry before the supplied date, a weak cipher name, or a missing NS record raises the exposure. The grade follows that percentage. No DNS or TLS lookup is performed. Docs: https://www.brainiac.software/api/domain-security/infrastructure-health",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "as_of": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "records": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "TXT",
                    "NS",
                    "MX"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 512
                }
              },
              "required": [
                "type",
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "certificate": {
            "type": "object",
            "properties": {
              "names": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              },
              "not_after": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
              },
              "ciphers": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              }
            },
            "required": [
              "names",
              "not_after",
              "ciphers"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "domain",
          "as_of",
          "records",
          "certificate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "domain-security__custom-domain-onboarding-audit",
      "description": "Audit custom domain onboarding. Compare a custom domain, tenant, ownership TXT records, DNS targets, and platform assignment status. A dangling name is a potential condition only when the supplied assignment is unassigned or deleted. The audit does not query DNS or claim the domain. Docs: https://www.brainiac.software/api/domain-security/custom-domain-onboarding-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "tenant": {
            "type": "string",
            "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$"
          },
          "verification": {
            "maxItems": 16,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "TXT",
                    "CNAME"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 1024
                }
              },
              "required": [
                "type",
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "records": {
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME",
                    "TXT"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 1024
                }
              },
              "required": [
                "type",
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "token": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "targets": {
            "minItems": 1,
            "maxItems": 16,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "kind": {
                  "type": "string",
                  "enum": [
                    "A",
                    "AAAA",
                    "CNAME"
                  ]
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                }
              },
              "required": [
                "kind",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "assignments": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "hostname": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "tenant": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$"
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "assigned",
                    "unassigned",
                    "deleted"
                  ]
                }
              },
              "required": [
                "hostname",
                "status"
              ],
              "additionalProperties": false
            }
          },
          "previous": {
            "type": "object",
            "properties": {
              "tenant": {
                "type": "string",
                "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$"
              },
              "domain": {
                "type": "string",
                "minLength": 1,
                "maxLength": 253
              },
              "status": {
                "type": "string",
                "enum": [
                  "pending",
                  "active",
                  "removed"
                ]
              }
            },
            "required": [
              "tenant",
              "domain",
              "status"
            ],
            "additionalProperties": false
          },
          "certificates": {
            "maxItems": 4,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sans": {
                  "maxItems": 64,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 253
                  }
                },
                "issuer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "notBefore": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "notAfter": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "fingerprint": {
                  "type": "string",
                  "minLength": 32,
                  "maxLength": 95
                }
              },
              "required": [
                "sans"
              ],
              "additionalProperties": false
            }
          },
          "checkedAt": {
            "type": "string",
            "format": "date-time",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
          },
          "status": {
            "type": "string",
            "enum": [
              "pending",
              "active",
              "removed"
            ]
          }
        },
        "required": [
          "domain",
          "tenant",
          "verification",
          "records",
          "token",
          "targets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "domain-security__onboarding-readiness",
      "description": "Score custom domain readiness. Compare the supplied TXT name and token, the CNAME target, and a certificate flag. Readiness drops when the token is missing from the expected name, the CNAME does not match the target, or the certificate flag is false. The hijacking index rises when a CNAME points elsewhere, the token sits on another name, or the certificate does not cover the domain. No DNS lookup is performed. Docs: https://www.brainiac.software/api/domain-security/onboarding-readiness",
      "parameters": {
        "type": "object",
        "properties": {
          "domain": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "token": {
            "type": "string",
            "minLength": 8,
            "maxLength": 200
          },
          "txt_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "cname_target": {
            "type": "string",
            "minLength": 1,
            "maxLength": 253
          },
          "certificate_covers_domain": {
            "type": "boolean"
          },
          "records": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "TXT",
                    "CNAME"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 253
                },
                "value": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 512
                }
              },
              "required": [
                "type",
                "name",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "domain",
          "token",
          "txt_name",
          "cname_target",
          "certificate_covers_domain",
          "records"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "domain-security__domain-infrastructure-consistency-audit": "0.05",
  "domain-security__infrastructure-health": "0.04",
  "domain-security__custom-domain-onboarding-audit": "0.05",
  "domain-security__onboarding-readiness": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "domain-security__domain-infrastructure-consistency-audit": "domain-security/domain-infrastructure-consistency-audit",
  "domain-security__infrastructure-health": "domain-security/infrastructure-health",
  "domain-security__custom-domain-onboarding-audit": "domain-security/custom-domain-onboarding-audit",
  "domain-security__onboarding-readiness": "domain-security/onboarding-readiness"
}


class BrainiacDomainSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — domain-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the domain-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "domain-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit domain infrastructure consistency"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the domain-security group. "
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
