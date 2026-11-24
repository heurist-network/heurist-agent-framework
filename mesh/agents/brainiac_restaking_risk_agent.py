"""Auto-generated BRAINIAC Heurist Mesh agent for group `restaking-risk` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "restaking-risk__cross-network-slashing-exposure",
      "description": "Calculate cross-network slashing exposure. Calculate unique collateral, gross exposure, and overlap when caller-supplied vault collateral is reused across networks. Simultaneous scenarios slash the starting balance and cap the combined percent at 100%. Sequential scenarios reduce the remaining balance after each event. audit_status is calculated, warnings, incomplete, or invalid. Amounts are integers in the caller-supplied unit. Prices and conversion rates are used only when supplied. No balance or price is fetched. Docs: https://www.brainiac.software/api/restaking-risk/cross-network-slashing-exposure",
      "parameters": {
        "type": "object",
        "properties": {
          "vaults": {
            "minItems": 1,
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "collateral": {
                  "minItems": 1,
                  "maxItems": 16,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "asset": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "amount": {
                        "type": "string",
                        "pattern": "^(0|[1-9][0-9]{0,77})$"
                      }
                    },
                    "required": [
                      "asset",
                      "amount"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "collateral"
              ],
              "additionalProperties": false
            }
          },
          "allocations": {
            "minItems": 1,
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "vault": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "network": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "operator": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "string",
                  "pattern": "^(0|[1-9][0-9]{0,77})$"
                }
              },
              "required": [
                "id",
                "vault",
                "network",
                "operator",
                "asset",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "reuse": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "amount": {
                  "type": "string",
                  "pattern": "^(0|[1-9][0-9]{0,77})$"
                },
                "allocations": {
                  "minItems": 2,
                  "maxItems": 16,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 80
                  }
                }
              },
              "required": [
                "id",
                "asset",
                "amount",
                "allocations"
              ],
              "additionalProperties": false
            }
          },
          "slashing": {
            "maxItems": 64,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "network": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "operator": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "percent": {
                  "type": "string",
                  "pattern": "^(100(?:\\.0{1,4})?|(?:0|[1-9]\\d?)(?:\\.\\d{1,4})?)$"
                }
              },
              "required": [
                "network",
                "percent"
              ],
              "additionalProperties": false
            }
          },
          "scenarios": {
            "minItems": 1,
            "maxItems": 16,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "ordering": {
                  "type": "string",
                  "enum": [
                    "simultaneous",
                    "sequential"
                  ]
                },
                "events": {
                  "minItems": 1,
                  "maxItems": 16,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "network": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "operator": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "percent": {
                        "type": "string",
                        "pattern": "^(100(?:\\.0{1,4})?|(?:0|[1-9]\\d?)(?:\\.\\d{1,4})?)$"
                      }
                    },
                    "required": [
                      "network"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "ordering",
                "events"
              ],
              "additionalProperties": false
            }
          },
          "prices": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "asset": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "quote": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "price": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d{0,24})(?:\\.\\d{1,8})?$"
                }
              },
              "required": [
                "asset",
                "quote",
                "price"
              ],
              "additionalProperties": false
            }
          },
          "rates": {
            "maxItems": 32,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "base": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "quote": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "rate": {
                  "type": "string",
                  "pattern": "^(?:0|[1-9]\\d{0,24})(?:\\.\\d{1,8})?$"
                }
              },
              "required": [
                "base",
                "quote",
                "rate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "vaults",
          "allocations",
          "slashing",
          "scenarios"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "restaking-risk__slashing-correlation",
      "description": "Score cross-network slashing correlation. Cap each operator's network weights at 100 percent of its stake, then weight that exposure by stake. The correlation score is the share of stake that sits on more than one network. Weights are the caller's risk weights. No stake is fetched. Docs: https://www.brainiac.software/api/restaking-risk/slashing-correlation",
      "parameters": {
        "type": "object",
        "properties": {
          "operators": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "stake": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 9007199254740991
                },
                "networks": {
                  "minItems": 1,
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "weight": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 100
                      }
                    },
                    "required": [
                      "id",
                      "weight"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "stake",
                "networks"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "operators"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "restaking-risk__slashing-window-feasibility",
      "description": "Check slashing window feasibility. Compare caller-supplied slashing stages with an available window. Each duration is an integer in seconds, or in epochs when its unit is epochs. Epoch length is seconds. Stages run in detection, evidence, submission, veto, execution, and finality order. Consecutive stages listed in parallel start together and the timeline uses the longest. A missing stage is incomplete and is not treated as zero. feasibility_status is feasible, margin_exceeded, infeasible, incomplete, or invalid. A fit is arithmetic only. No protocol parameters are fetched. Docs: https://www.brainiac.software/api/restaking-risk/slashing-window-feasibility",
      "parameters": {
        "type": "object",
        "properties": {
          "epoch": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "window": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "detection": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "evidence": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "submission": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "veto": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "execution": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "finality": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "margin": {
            "type": "object",
            "properties": {
              "value": {
                "type": "string",
                "pattern": "^(0|[1-9][0-9]{0,12})$"
              },
              "unit": {
                "type": "string",
                "enum": [
                  "seconds",
                  "epochs"
                ]
              }
            },
            "required": [
              "value",
              "unit"
            ],
            "additionalProperties": false
          },
          "parallel": {
            "maxItems": 3,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "stages": {
                  "minItems": 2,
                  "maxItems": 6,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "enum": [
                      "detection",
                      "evidence",
                      "submission",
                      "veto",
                      "execution",
                      "finality"
                    ]
                  }
                }
              },
              "required": [
                "stages"
              ],
              "additionalProperties": false
            }
          },
          "alternatives": {
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "epoch": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "window": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "detection": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "evidence": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "submission": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "veto": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "execution": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "finality": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "margin": {
                  "type": "object",
                  "properties": {
                    "value": {
                      "type": "string",
                      "pattern": "^(0|[1-9][0-9]{0,12})$"
                    },
                    "unit": {
                      "type": "string",
                      "enum": [
                        "seconds",
                        "epochs"
                      ]
                    }
                  },
                  "required": [
                    "value",
                    "unit"
                  ],
                  "additionalProperties": false
                },
                "parallel": {
                  "maxItems": 3,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "stages": {
                        "minItems": 2,
                        "maxItems": 6,
                        "type": "array",
                        "items": {
                          "type": "string",
                          "enum": [
                            "detection",
                            "evidence",
                            "submission",
                            "veto",
                            "execution",
                            "finality"
                          ]
                        }
                      }
                    },
                    "required": [
                      "stages"
                    ],
                    "additionalProperties": false
                  }
                },
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                }
              },
              "required": [
                "epoch",
                "window",
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "epoch",
          "window"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "restaking-risk__exit-window",
      "description": "Score exit timing before a slash. Subtract the unbonding time and the withdrawal delay from the soonest caller-supplied slash horizon. The buffer is that remainder in hours. The feasibility score is the buffer divided by the soonest horizon, and it is zero when the buffer is negative. No queue is read from a network. Docs: https://www.brainiac.software/api/restaking-risk/exit-window",
      "parameters": {
        "type": "object",
        "properties": {
          "unbonding_hours": {
            "type": "integer",
            "minimum": 0,
            "maximum": 8760
          },
          "withdrawal_delay_hours": {
            "type": "integer",
            "minimum": 0,
            "maximum": 8760
          },
          "events": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "network": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "hours_until_slash": {
                  "type": "integer",
                  "exclusiveMinimum": 0,
                  "maximum": 8760
                }
              },
              "required": [
                "network",
                "hours_until_slash"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "unbonding_hours",
          "withdrawal_delay_hours",
          "events"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "restaking-risk__cross-network-slashing-exposure": "0.05",
  "restaking-risk__slashing-correlation": "0.04",
  "restaking-risk__slashing-window-feasibility": "0.05",
  "restaking-risk__exit-window": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "restaking-risk__cross-network-slashing-exposure": "restaking-risk/cross-network-slashing-exposure",
  "restaking-risk__slashing-correlation": "restaking-risk/slashing-correlation",
  "restaking-risk__slashing-window-feasibility": "restaking-risk/slashing-window-feasibility",
  "restaking-risk__exit-window": "restaking-risk/exit-window"
}


class BrainiacRestakingRiskAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — restaking-risk",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the restaking-risk catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "restaking-risk", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Calculate cross-network slashing exposure"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the restaking-risk group. "
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
