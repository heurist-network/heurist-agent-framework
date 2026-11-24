"""Auto-generated BRAINIAC Heurist Mesh agent for group `network-exposure` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "network-exposure__cidr-calculate",
      "description": "Calculate IPv4/IPv6 CIDR details, aggregates and relations. Describe, aggregate or relate CIDR blocks without network access. Docs: https://www.brainiac.software/api/network-exposure/cidr-calculate",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__ip-list-diff",
      "description": "Diff two host/service exposure snapshots. Report new, closed and changed services between before and after snapshots. Docs: https://www.brainiac.software/api/network-exposure/ip-list-diff",
      "parameters": {
        "type": "object",
        "properties": {
          "before": {
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ip": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "port": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 65535
                },
                "protocol": {
                  "default": "tcp",
                  "type": "string",
                  "enum": [
                    "tcp",
                    "udp",
                    "sctp"
                  ]
                },
                "service": {
                  "type": "string",
                  "maxLength": 4096
                },
                "banner": {
                  "type": "string",
                  "maxLength": 4096
                }
              },
              "required": [
                "ip",
                "port"
              ],
              "additionalProperties": false
            }
          },
          "after": {
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ip": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "port": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 65535
                },
                "protocol": {
                  "default": "tcp",
                  "type": "string",
                  "enum": [
                    "tcp",
                    "udp",
                    "sctp"
                  ]
                },
                "service": {
                  "type": "string",
                  "maxLength": 4096
                },
                "banner": {
                  "type": "string",
                  "maxLength": 4096
                }
              },
              "required": [
                "ip",
                "port"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "before",
          "after"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__service-banner-fingerprint",
      "description": "Fingerprint service banners with Recog. Match banners against vendored Rapid7 Recog fingerprints. Docs: https://www.brainiac.software/api/network-exposure/service-banner-fingerprint",
      "parameters": {
        "type": "object",
        "properties": {
          "items": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "value": {
                  "type": "string",
                  "maxLength": 4096
                }
              },
              "required": [
                "type",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "items"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__cpe-parse-match",
      "description": "Parse CPE strings and match criteria. Unbind CPE 2.2/2.3 names and test version-range criteria. Docs: https://www.brainiac.software/api/network-exposure/cpe-parse-match",
      "parameters": {
        "type": "object",
        "properties": {
          "cpe": {
            "type": "string",
            "minLength": 1,
            "maxLength": 1024
          },
          "criteria": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "criteria": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 1024
                },
                "versionStartIncluding": {
                  "type": "string",
                  "maxLength": 128
                },
                "versionStartExcluding": {
                  "type": "string",
                  "maxLength": 128
                },
                "versionEndIncluding": {
                  "type": "string",
                  "maxLength": 128
                },
                "versionEndExcluding": {
                  "type": "string",
                  "maxLength": 128
                }
              },
              "required": [
                "criteria"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "cpe"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__cvss-calculate",
      "description": "Calculate CVSS v3.1 and v4.0 scores. Validate a CVSS vector and compute base/temporal/environmental or v4 scores. Docs: https://www.brainiac.software/api/network-exposure/cvss-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "vector": {
            "type": "string",
            "minLength": 8,
            "maxLength": 512
          }
        },
        "required": [
          "vector"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__tls-fingerprint-compute",
      "description": "Compute JA3 and JA4 TLS fingerprints. Derive JA3/JA4 from ClientHello fields without capturing traffic. Docs: https://www.brainiac.software/api/network-exposure/tls-fingerprint-compute",
      "parameters": {
        "type": "object",
        "properties": {
          "transport": {
            "default": "tcp",
            "type": "string",
            "enum": [
              "tcp",
              "quic",
              "dtls"
            ]
          },
          "legacyVersion": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "supportedVersions": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": -9007199254740991,
              "maximum": 9007199254740991
            }
          },
          "ciphers": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[0-9a-fA-F]{4}$"
            }
          },
          "extensions": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[0-9a-fA-F]{4}$"
            }
          },
          "signatureAlgorithms": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[0-9a-fA-F]{4}$"
            }
          },
          "alpn": {
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 64
            }
          },
          "supportedGroups": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": -9007199254740991,
              "maximum": 9007199254740991
            }
          },
          "ecPointFormats": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": -9007199254740991,
              "maximum": 9007199254740991
            }
          },
          "clientHelloHex": {
            "type": "string",
            "maxLength": 32768
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__x509-decode",
      "description": "Decode X.509 certificates and flag weaknesses. Parse PEM/DER certificates and apply NIST/BR validity flags. Docs: https://www.brainiac.software/api/network-exposure/x509-decode",
      "parameters": {
        "type": "object",
        "properties": {
          "pem": {
            "type": "string",
            "maxLength": 1000000
          },
          "derBase64": {
            "type": "string",
            "maxLength": 1000000
          },
          "now": {
            "type": "string"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__csr-decode-validate",
      "description": "Decode and validate a PKCS#10 CSR. Verify CSR self-signature and check key/SAN policy. Docs: https://www.brainiac.software/api/network-exposure/csr-decode-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "csrPem": {
            "type": "string",
            "minLength": 20,
            "maxLength": 65536
          },
          "policy": {
            "default": {
              "minRsaBits": 2048,
              "allowedKeyTypes": [
                "RSA",
                "EC",
                "Ed25519"
              ],
              "allowedCurves": [
                "P-256",
                "P-384"
              ],
              "requireSan": true,
              "cnMustBeInSan": true
            },
            "type": "object",
            "properties": {
              "minRsaBits": {
                "default": 2048,
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "allowedKeyTypes": {
                "default": [
                  "RSA",
                  "EC",
                  "Ed25519"
                ],
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": [
                    "RSA",
                    "EC",
                    "Ed25519"
                  ]
                }
              },
              "allowedCurves": {
                "default": [
                  "P-256",
                  "P-384"
                ],
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "requireSan": {
                "default": true,
                "type": "boolean"
              },
              "cnMustBeInSan": {
                "default": true,
                "type": "boolean"
              },
              "allowedDomains": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "csrPem"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__certificate-chain-build",
      "description": "Build and verify a certificate chain offline. Chain certificates against the vendored Mozilla root store. Docs: https://www.brainiac.software/api/network-exposure/certificate-chain-build",
      "parameters": {
        "type": "object",
        "properties": {
          "certificates": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 20
            }
          },
          "leafIndex": {
            "type": "integer",
            "minimum": 0,
            "maximum": 19
          },
          "now": {
            "type": "string"
          }
        },
        "required": [
          "certificates"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__ssh-key-audit",
      "description": "Fingerprint and audit SSH public keys. Parse OpenSSH public keys, authorized_keys and certificates. Docs: https://www.brainiac.software/api/network-exposure/ssh-key-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "keys": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 16384
            }
          },
          "minRsaBits": {
            "default": 2048,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "keys"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__nmap-xml-summarize",
      "description": "Summarise Nmap XML or Masscan JSON. Turn scan output into host/service risk summaries. Docs: https://www.brainiac.software/api/network-exposure/nmap-xml-summarize",
      "parameters": {
        "type": "object",
        "properties": {
          "format": {
            "type": "string",
            "enum": [
              "nmap_xml",
              "masscan_json"
            ]
          },
          "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000000
          }
        },
        "required": [
          "format",
          "content"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__port-service-risk-classify",
      "description": "Classify port/service exposure risk. Name IANA services and assign documented risk tiers. Docs: https://www.brainiac.software/api/network-exposure/port-service-risk-classify",
      "parameters": {
        "type": "object",
        "properties": {
          "services": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "port": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 65535
                },
                "protocol": {
                  "type": "string",
                  "enum": [
                    "tcp",
                    "udp",
                    "sctp",
                    "dccp"
                  ]
                },
                "bannerHint": {
                  "type": "string",
                  "maxLength": 256
                }
              },
              "required": [
                "port",
                "protocol"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "services"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__firewall-rule-analyze",
      "description": "Analyse firewall rules for anomalies. Find shadowed, redundant and overly permissive iptables/nftables/AWS SG rules. Docs: https://www.brainiac.software/api/network-exposure/firewall-rule-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "format": {
            "type": "string",
            "enum": [
              "iptables",
              "nftables",
              "aws_sg"
            ]
          },
          "rules": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "array",
                "items": {}
              },
              {
                "type": "object",
                "propertyNames": {
                  "type": "string"
                },
                "additionalProperties": {}
              }
            ]
          },
          "sensitivePorts": {
            "anyOf": [
              {
                "type": "array",
                "items": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "format",
          "rules"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__dns-zone-audit",
      "description": "Audit a BIND zone file. Flag dangling CNAMEs, wildcards, missing CAA/SPF/DMARC and TTL anomalies. Docs: https://www.brainiac.software/api/network-exposure/dns-zone-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "zone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000000
          },
          "origin": {
            "type": "string",
            "maxLength": 255
          },
          "deprovisionedTargets": {
            "default": [],
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "maxLength": 255
            }
          },
          "minTtl": {
            "default": 300,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "maxTtl": {
            "default": 604800,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "zone"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "network-exposure__dnssec-validate-offline",
      "description": "Validate DNSSEC records offline. Check DNSKEY, DS and RRSIG material without network queries. Docs: https://www.brainiac.software/api/network-exposure/dnssec-validate-offline",
      "parameters": {
        "type": "object",
        "properties": {
          "dnskeys": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "ds": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "rrset": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "rrsigs": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "now": {
            "type": "string"
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "network-exposure__cidr-calculate": "0.02",
  "network-exposure__ip-list-diff": "0.03",
  "network-exposure__service-banner-fingerprint": "0.03",
  "network-exposure__cpe-parse-match": "0.02",
  "network-exposure__cvss-calculate": "0.02",
  "network-exposure__tls-fingerprint-compute": "0.03",
  "network-exposure__x509-decode": "0.03",
  "network-exposure__csr-decode-validate": "0.03",
  "network-exposure__certificate-chain-build": "0.04",
  "network-exposure__ssh-key-audit": "0.02",
  "network-exposure__nmap-xml-summarize": "0.03",
  "network-exposure__port-service-risk-classify": "0.02",
  "network-exposure__firewall-rule-analyze": "0.04",
  "network-exposure__dns-zone-audit": "0.03",
  "network-exposure__dnssec-validate-offline": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "network-exposure__cidr-calculate": "network-exposure/cidr-calculate",
  "network-exposure__ip-list-diff": "network-exposure/ip-list-diff",
  "network-exposure__service-banner-fingerprint": "network-exposure/service-banner-fingerprint",
  "network-exposure__cpe-parse-match": "network-exposure/cpe-parse-match",
  "network-exposure__cvss-calculate": "network-exposure/cvss-calculate",
  "network-exposure__tls-fingerprint-compute": "network-exposure/tls-fingerprint-compute",
  "network-exposure__x509-decode": "network-exposure/x509-decode",
  "network-exposure__csr-decode-validate": "network-exposure/csr-decode-validate",
  "network-exposure__certificate-chain-build": "network-exposure/certificate-chain-build",
  "network-exposure__ssh-key-audit": "network-exposure/ssh-key-audit",
  "network-exposure__nmap-xml-summarize": "network-exposure/nmap-xml-summarize",
  "network-exposure__port-service-risk-classify": "network-exposure/port-service-risk-classify",
  "network-exposure__firewall-rule-analyze": "network-exposure/firewall-rule-analyze",
  "network-exposure__dns-zone-audit": "network-exposure/dns-zone-audit",
  "network-exposure__dnssec-validate-offline": "network-exposure/dnssec-validate-offline"
}


class BrainiacNetworkExposureAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — network-exposure",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the network-exposure catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "network-exposure", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Calculate IPv4/IPv6 CIDR details, aggregates and relations"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the network-exposure group. "
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
