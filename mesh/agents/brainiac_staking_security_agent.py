"""Auto-generated BRAINIAC Heurist Mesh agent for group `staking-security` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "staking-security__validator-slashing-protection-audit",
      "description": "Audit validator slashing protection. Check caller-supplied EIP-3076 version 5 slashing-protection interchanges before validator history is imported or reused. A double proposal is two different blocks at the same slot. A double vote is two different attestations with the same target epoch. A surround vote has an earlier source epoch and a later target epoch than the vote it surrounds. audit_status is safe, conflicts_detected, warnings, invalid, or incomplete. risk_level is low, medium, high, or critical. Identical records without signing_root are not a confirmed slash. The export is not a complete signing history and does not protect against a later signature. No private key is accepted and no beacon node is queried. Docs: https://www.brainiac.software/api/staking-security/validator-slashing-protection-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "interchange": {
            "type": "object",
            "properties": {
              "metadata": {
                "type": "object",
                "properties": {
                  "interchange_format_version": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 16
                  },
                  "genesis_validators_root": {
                    "type": "string",
                    "pattern": "^0x[0-9a-fA-F]{64}$"
                  }
                },
                "required": [
                  "interchange_format_version",
                  "genesis_validators_root"
                ],
                "additionalProperties": false
              },
              "data": {
                "maxItems": 128,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "pubkey": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{96}$"
                    },
                    "signed_blocks": {
                      "maxItems": 256,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "slot": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "signing_root": {
                            "type": "string",
                            "pattern": "^0x[0-9a-fA-F]{64}$"
                          }
                        },
                        "required": [
                          "slot"
                        ],
                        "additionalProperties": false
                      }
                    },
                    "signed_attestations": {
                      "maxItems": 256,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "source_epoch": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "target_epoch": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "signing_root": {
                            "type": "string",
                            "pattern": "^0x[0-9a-fA-F]{64}$"
                          }
                        },
                        "required": [
                          "source_epoch",
                          "target_epoch"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "pubkey",
                    "signed_blocks",
                    "signed_attestations"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "metadata",
              "data"
            ],
            "additionalProperties": false
          },
          "comparison": {
            "type": "object",
            "properties": {
              "metadata": {
                "type": "object",
                "properties": {
                  "interchange_format_version": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 16
                  },
                  "genesis_validators_root": {
                    "type": "string",
                    "pattern": "^0x[0-9a-fA-F]{64}$"
                  }
                },
                "required": [
                  "interchange_format_version",
                  "genesis_validators_root"
                ],
                "additionalProperties": false
              },
              "data": {
                "maxItems": 128,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "pubkey": {
                      "type": "string",
                      "pattern": "^0x[0-9a-fA-F]{96}$"
                    },
                    "signed_blocks": {
                      "maxItems": 256,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "slot": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "signing_root": {
                            "type": "string",
                            "pattern": "^0x[0-9a-fA-F]{64}$"
                          }
                        },
                        "required": [
                          "slot"
                        ],
                        "additionalProperties": false
                      }
                    },
                    "signed_attestations": {
                      "maxItems": 256,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "source_epoch": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "target_epoch": {
                            "type": "string",
                            "pattern": "^(0|[1-9][0-9]{0,19})$"
                          },
                          "signing_root": {
                            "type": "string",
                            "pattern": "^0x[0-9a-fA-F]{64}$"
                          }
                        },
                        "required": [
                          "source_epoch",
                          "target_epoch"
                        ],
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "pubkey",
                    "signed_blocks",
                    "signed_attestations"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "metadata",
              "data"
            ],
            "additionalProperties": false
          },
          "pubkeys": {
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^0x[0-9a-fA-F]{96}$"
            }
          },
          "network": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "genesisValidatorsRoot": {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{64}$"
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "interchange"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "staking-security__validator-key-deployment-conflict-audit",
      "description": "Audit validator deployment conflicts. Compare a caller-supplied validator deployment inventory for duplicate active public keys, simultaneous primary and backup activation, overlapping activation windows, and failover rules that disagree. Windows are absolute instants, including offsets. An inactive standby covered by an exclusive failover rule is not treated as concurrent. audit_status is clean, conflicts_detected, warnings, or incomplete. risk_level is low, medium, high, or critical. Activation status is an assertion. No host is contacted and no private key is read. Docs: https://www.brainiac.software/api/staking-security/validator-key-deployment-conflict-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "deployments": {
            "minItems": 1,
            "maxItems": 256,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "pubkey": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{96}$"
                },
                "environment": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "node": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "primary",
                    "standby",
                    "backup",
                    "recovery"
                  ]
                },
                "activation": {
                  "type": "string",
                  "enum": [
                    "active",
                    "inactive",
                    "scheduled"
                  ]
                },
                "owner": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "activationWindow": {
                  "type": "object",
                  "properties": {
                    "start": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    },
                    "end": {
                      "type": "string",
                      "format": "date-time",
                      "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                    }
                  },
                  "required": [
                    "start",
                    "end"
                  ],
                  "additionalProperties": false
                }
              },
              "required": [
                "pubkey",
                "environment",
                "role",
                "activation"
              ],
              "additionalProperties": false
            }
          },
          "maintenanceWindows": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "environment": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "start": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                },
                "end": {
                  "type": "string",
                  "format": "date-time",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d+)?(?:Z|([+-](?:[01]\\d|2[0-3]):[0-5]\\d)))$"
                }
              },
              "required": [
                "environment",
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          },
          "failoverRules": {
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "pubkey": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{96}$"
                },
                "environments": {
                  "minItems": 2,
                  "maxItems": 16,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                  }
                },
                "exclusive": {
                  "type": "boolean"
                }
              },
              "required": [
                "pubkey",
                "environments",
                "exclusive"
              ],
              "additionalProperties": false
            }
          },
          "expectedTopology": {
            "maxItems": 256,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "pubkey": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{96}$"
                },
                "environment": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "node": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "role": {
                  "type": "string",
                  "enum": [
                    "primary",
                    "standby",
                    "backup",
                    "recovery"
                  ]
                },
                "activation": {
                  "type": "string",
                  "enum": [
                    "active",
                    "inactive",
                    "scheduled"
                  ]
                }
              },
              "required": [
                "pubkey",
                "environment",
                "role"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "deployments"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "staking-security__validator-withdrawal-credential-audit",
      "description": "Audit validator withdrawal credentials. Compare caller-supplied Ethereum validator withdrawal credentials with expected types, withdrawal addresses, and ownership mappings. 0x00 is a BLS credential and the other 31 bytes are a hash fragment, not an address. 0x01 and 0x02 decode an execution address only when the next 11 bytes are zero. audit_status is valid, mismatched, warnings, invalid, or incomplete. risk_level is low, medium, high, or critical. A match is not proof of control and was not read from a beacon node. Docs: https://www.brainiac.software/api/staking-security/validator-withdrawal-credential-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "validators": {
            "minItems": 1,
            "maxItems": 128,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "pubkey": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{96}$"
                },
                "withdrawalCredentials": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{64}$"
                }
              },
              "required": [
                "pubkey",
                "withdrawalCredentials"
              ],
              "additionalProperties": false
            }
          },
          "expected": {
            "minItems": 1,
            "maxItems": 128,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "pubkey": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{96}$"
                },
                "credentialType": {
                  "type": "string",
                  "enum": [
                    "bls",
                    "execution",
                    "compounding"
                  ]
                },
                "address": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                }
              },
              "required": [
                "pubkey",
                "credentialType"
              ],
              "additionalProperties": false
            }
          },
          "ownership": {
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "address": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                },
                "operator": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                },
                "beneficiary": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                }
              },
              "required": [
                "address",
                "operator"
              ],
              "additionalProperties": false
            }
          },
          "network": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "policy": {
            "type": "object",
            "properties": {
              "duplicateDestinations": {
                "type": "string",
                "enum": [
                  "allow",
                  "prohibit"
                ]
              },
              "ownership": {
                "type": "string",
                "enum": [
                  "require_listed",
                  "informational"
                ]
              },
              "operators": {
                "maxItems": 32,
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]{0,79}$"
                }
              }
            },
            "additionalProperties": false
          }
        },
        "required": [
          "validators",
          "expected"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "staking-security__validator-slashing-protection-audit": "0.05",
  "staking-security__validator-key-deployment-conflict-audit": "0.05",
  "staking-security__validator-withdrawal-credential-audit": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "staking-security__validator-slashing-protection-audit": "staking-security/validator-slashing-protection-audit",
  "staking-security__validator-key-deployment-conflict-audit": "staking-security/validator-key-deployment-conflict-audit",
  "staking-security__validator-withdrawal-credential-audit": "staking-security/validator-withdrawal-credential-audit"
}


class BrainiacStakingSecurityAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — staking-security",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the staking-security catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "staking-security", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Audit validator slashing protection"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.05",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the staking-security group. "
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
