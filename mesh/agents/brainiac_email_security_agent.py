"""Auto-generated BRAINIAC Heurist Mesh agent for group `email-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "email-security__header-forensics",
      "description": "Analyze email headers. Analyze caller-supplied email headers for routing hops and suspicious inconsistencies (From/Return-Path/Reply-To, auth results, dates). Indicators only—not confirmed malice. Docs: https://www.brainiac.software/api/email-security/header-forensics",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__spoofing-detect",
      "description": "Detect email spoofing indicators. Detect sender spoofing indicators from supplied SPF/DKIM/DMARC authentication results and optional public DNS TXT evidence. Not a confirmed spoof verdict without multi-signal evidence. Docs: https://www.brainiac.software/api/email-security/spoofing-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__phishing-signal-detect",
      "description": "Detect phishing signals. Identify phishing indicators in caller-supplied email content and URLs (urgency phrases, lookalike hosts, IP URLs, password forms). Indicators are not confirmed malicious activity. Docs: https://www.brainiac.software/api/email-security/phishing-signal-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__bec-pattern-detect",
      "description": "Detect BEC patterns. Detect Business Email Compromise patterns such as payment-change language, executive persona cues, external Reply-To, and lookalike sender domains from supplied mail. Docs: https://www.brainiac.software/api/email-security/bec-pattern-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__domain-impersonation-check",
      "description": "Check domain impersonation. Identify domains resembling supplied company or brand domains using edit distance, hyphen variants, homoglyph folding, and brand-token embedding. Resemblance is not proof of abuse. Docs: https://www.brainiac.software/api/email-security/domain-impersonation-check",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__url-chain-analyze",
      "description": "Analyze email URL redirect chains. Analyze caller-supplied redirect hops or optionally follow public URLs with strict SSRF protections. Never sends email content to external scanners. Docs: https://www.brainiac.software/api/email-security/url-chain-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__attachment-risk-analyze",
      "description": "Analyze email attachment risk. Inspect caller-supplied attachment filenames, metadata, and local magic-byte structures for suspicious patterns. No external sandbox or scanner is used. Docs: https://www.brainiac.software/api/email-security/attachment-risk-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
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
      "name": "email-security__conversation-tamper-detect",
      "description": "Detect conversation tampering. Identify inconsistencies between supplied email conversation copies (missing messages, body hash mismatches, header field divergence). Export artifacts are distinguished from confirmed tampering. Docs: https://www.brainiac.software/api/email-security/conversation-tamper-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "maxLength": 500000
          },
          "eml": {
            "type": "string",
            "maxLength": 500000
          },
          "headers": {
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
                  "message/rfc822",
                  "text/csv",
                  "application/json",
                  "application/octet-stream",
                  "application/pdf",
                  "application/zip"
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
                    "message/rfc822",
                    "text/csv",
                    "application/json",
                    "application/octet-stream",
                    "application/pdf",
                    "application/zip"
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
          "emails": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "raw": {
                  "type": "string",
                  "maxLength": 500000
                },
                "headers": {
                  "type": "string",
                  "maxLength": 200000
                },
                "from": {
                  "type": "string",
                  "maxLength": 500
                },
                "to": {
                  "type": "string",
                  "maxLength": 2000
                },
                "cc": {
                  "type": "string",
                  "maxLength": 2000
                },
                "replyTo": {
                  "type": "string",
                  "maxLength": 500
                },
                "returnPath": {
                  "type": "string",
                  "maxLength": 500
                },
                "subject": {
                  "type": "string",
                  "maxLength": 998
                },
                "date": {
                  "type": "string",
                  "maxLength": 80
                },
                "messageId": {
                  "type": "string",
                  "maxLength": 300
                },
                "inReplyTo": {
                  "type": "string",
                  "maxLength": 300
                },
                "references": {
                  "type": "string",
                  "maxLength": 4000
                },
                "bodyText": {
                  "type": "string",
                  "maxLength": 200000
                },
                "bodyHtml": {
                  "type": "string",
                  "maxLength": 200000
                },
                "urls": {
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 2000
                  }
                },
                "authenticationResults": {
                  "type": "object",
                  "properties": {
                    "spf": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "softfail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dkim": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "neutral",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "dmarc": {
                      "type": "string",
                      "enum": [
                        "pass",
                        "fail",
                        "none",
                        "temperror",
                        "permerror",
                        "unknown"
                      ]
                    },
                    "source": {
                      "type": "string",
                      "maxLength": 200
                    }
                  },
                  "additionalProperties": false
                },
                "attachments": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "filename": {
                        "type": "string",
                        "maxLength": 260
                      },
                      "mediaType": {
                        "type": "string",
                        "maxLength": 120
                      },
                      "sizeBytes": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100000000
                      },
                      "contentBase64": {
                        "type": "string",
                        "maxLength": 12000000
                      },
                      "sha256": {
                        "type": "string",
                        "maxLength": 128
                      },
                      "source": {
                        "type": "string",
                        "maxLength": 200
                      }
                    },
                    "additionalProperties": false
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
          "attachments": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "filename": {
                  "type": "string",
                  "maxLength": 260
                },
                "mediaType": {
                  "type": "string",
                  "maxLength": 120
                },
                "sizeBytes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000000
                },
                "contentBase64": {
                  "type": "string",
                  "maxLength": 12000000
                },
                "sha256": {
                  "type": "string",
                  "maxLength": 128
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "urls": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 2000
            }
          },
          "urlHops": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                },
                "status": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 999
                },
                "location": {
                  "type": "string",
                  "maxLength": 2000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "url"
              ],
              "additionalProperties": false
            }
          },
          "brandDomains": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 253
            }
          },
          "companyNames": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 200
            }
          },
          "conversations": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 120
                },
                "emails": {
                  "minItems": 1,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "raw": {
                        "type": "string",
                        "maxLength": 500000
                      },
                      "headers": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "from": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "to": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "cc": {
                        "type": "string",
                        "maxLength": 2000
                      },
                      "replyTo": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "returnPath": {
                        "type": "string",
                        "maxLength": 500
                      },
                      "subject": {
                        "type": "string",
                        "maxLength": 998
                      },
                      "date": {
                        "type": "string",
                        "maxLength": 80
                      },
                      "messageId": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "inReplyTo": {
                        "type": "string",
                        "maxLength": 300
                      },
                      "references": {
                        "type": "string",
                        "maxLength": 4000
                      },
                      "bodyText": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "bodyHtml": {
                        "type": "string",
                        "maxLength": 200000
                      },
                      "urls": {
                        "maxItems": 200,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "maxLength": 2000
                        }
                      },
                      "authenticationResults": {
                        "type": "object",
                        "properties": {
                          "spf": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "softfail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dkim": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "neutral",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "dmarc": {
                            "type": "string",
                            "enum": [
                              "pass",
                              "fail",
                              "none",
                              "temperror",
                              "permerror",
                              "unknown"
                            ]
                          },
                          "source": {
                            "type": "string",
                            "maxLength": 200
                          }
                        },
                        "additionalProperties": false
                      },
                      "attachments": {
                        "maxItems": 50,
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "string",
                              "maxLength": 80
                            },
                            "filename": {
                              "type": "string",
                              "maxLength": 260
                            },
                            "mediaType": {
                              "type": "string",
                              "maxLength": 120
                            },
                            "sizeBytes": {
                              "type": "number",
                              "minimum": 0,
                              "maximum": 100000000
                            },
                            "contentBase64": {
                              "type": "string",
                              "maxLength": 12000000
                            },
                            "sha256": {
                              "type": "string",
                              "maxLength": 128
                            },
                            "source": {
                              "type": "string",
                              "maxLength": 200
                            }
                          },
                          "additionalProperties": false
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
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "required": [
                "emails"
              ],
              "additionalProperties": false
            }
          },
          "authenticationResults": {
            "type": "object",
            "properties": {
              "spf": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "softfail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dkim": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "neutral",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "dmarc": {
                "type": "string",
                "enum": [
                  "pass",
                  "fail",
                  "none",
                  "temperror",
                  "permerror",
                  "unknown"
                ]
              },
              "source": {
                "type": "string",
                "maxLength": 200
              }
            },
            "additionalProperties": false
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "publicDns": {
            "type": "boolean"
          },
          "followPublicUrls": {
            "type": "boolean"
          },
          "dkimSelectors": {
            "maxItems": 6,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 63
            }
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "email-security__header-forensics": "0.04",
  "email-security__spoofing-detect": "0.05",
  "email-security__phishing-signal-detect": "0.04",
  "email-security__bec-pattern-detect": "0.05",
  "email-security__domain-impersonation-check": "0.03",
  "email-security__url-chain-analyze": "0.05",
  "email-security__attachment-risk-analyze": "0.04",
  "email-security__conversation-tamper-detect": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "email-security__header-forensics": "email-security/header-forensics",
  "email-security__spoofing-detect": "email-security/spoofing-detect",
  "email-security__phishing-signal-detect": "email-security/phishing-signal-detect",
  "email-security__bec-pattern-detect": "email-security/bec-pattern-detect",
  "email-security__domain-impersonation-check": "email-security/domain-impersonation-check",
  "email-security__url-chain-analyze": "email-security/url-chain-analyze",
  "email-security__attachment-risk-analyze": "email-security/attachment-risk-analyze",
  "email-security__conversation-tamper-detect": "email-security/conversation-tamper-detect"
}


class BrainiacEmailSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — email-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the email-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "email-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyze email headers"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the email-security group. "
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
