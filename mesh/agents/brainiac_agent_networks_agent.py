"""Auto-generated BRAINIAC Heurist Mesh agent for group `agent-networks` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "agent-networks__float-loss-attribution",
      "description": "Attribute agent float loss. Reconcile caller-supplied opening and closing cash with every cash-in, cash-out, commission, fee, reversal, and adjustment. The expected closing is the opening balance plus those signed amounts. unexplained_amount is the counted closing minus that expected closing. A supplied expected balance is compared with the same expected closing. A reversal uses the opposite sign of an earlier transaction and its own amount. Amounts are safe integers in one minor unit. No ledger is fetched or stored. Docs: https://www.brainiac.software/api/agent-networks/float-loss-attribution",
      "parameters": {
        "type": "object",
        "properties": {
          "agents": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "opening_balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "closing_balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "expected_balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "opening_balance",
                "closing_balance"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "category": {
                  "type": "string",
                  "enum": [
                    "cash_in",
                    "cash_out",
                    "commission",
                    "fee",
                    "reversal",
                    "adjustment"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "reverses": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "id",
                "agent_id",
                "category",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "agents",
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__cash-shortage-analysis",
      "description": "Analyze agent cash shortage. Project caller-supplied outlet cash over the requested days. Historical cash in and cash out are averaged by weekday, and a missing day is not treated as zero. Expected demand replaces historical cash out on the dates or weekdays it names. A closed weekday follows the supplied schedule. The minimum replenishment is the amount that must be added at the start so the balance stays at the outlet minimum. Assumptions name every open day that has neither demand nor history. No ledger is fetched or stored. Docs: https://www.brainiac.software/api/agent-networks/cash-shortage-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "start_date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "period_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 90
          },
          "outlets": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "cash_balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "minimum_balance": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "cash_balance"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "outlet_id",
                "date",
                "direction",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "demand": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "weekday": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 6
                },
                "cash_out": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "outlet_id",
                "cash_out"
              ],
              "additionalProperties": false
            }
          },
          "schedules": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "weekday": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 6
                }
              },
              "required": [
                "outlet_id",
                "weekday"
              ],
              "additionalProperties": false
            }
          },
          "replenishment": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "weekday": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 6
                },
                "every_days": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 90
                }
              },
              "required": [
                "outlet_id",
                "amount"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "start_date",
          "period_days",
          "outlets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__terminal-profitability",
      "description": "Score terminal profitability. Score caller-supplied payment terminals from transaction counts, values, fee rules, revenue shares, and operating costs. Fees may be fixed, a rate in basis points, or tiers by cumulative count. revenue_share_bps is the share of the fee the terminal keeps; omitted means 10000. Each terminal keeps its own currency code. No amount is converted. profit_margin_bps is net profit over revenue in basis points. break_even_count is the transaction count that covers the period costs at the average revenue per transaction from the supplied mix. Ranking is by net profit inside each currency. No ledger is fetched or stored. Docs: https://www.brainiac.software/api/agent-networks/terminal-profitability",
      "parameters": {
        "type": "object",
        "properties": {
          "terminals": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "costs": {
                  "type": "object",
                  "properties": {
                    "rent": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "equipment": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "connectivity": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "maintenance": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "other": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    }
                  },
                  "additionalProperties": false
                }
              },
              "required": [
                "id",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "transaction_types": {
            "minItems": 1,
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fee": {
                  "type": "object",
                  "properties": {
                    "kind": {
                      "type": "string",
                      "enum": [
                        "fixed",
                        "percent",
                        "tiered"
                      ]
                    },
                    "amount": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    },
                    "rate_bps": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 1000000
                    },
                    "tiers": {
                      "minItems": 1,
                      "maxItems": 40,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "up_to": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 9007199254740991
                          },
                          "amount": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 9007199254740991
                          },
                          "rate_bps": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 1000000
                          }
                        },
                        "additionalProperties": false
                      }
                    }
                  },
                  "required": [
                    "kind"
                  ],
                  "additionalProperties": false
                },
                "revenue_share_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "required": [
                "id",
                "fee"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "terminal_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "count": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "terminal_id",
                "type_id",
                "count",
                "value"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "terminals",
          "transaction_types",
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__commission-leakage",
      "description": "Find commission leakage. Compare caller-supplied transactions with dated agent agreements and commission payments. Expected commission follows the agreement in force on the transaction date: fixed, percent, tiered by cumulative count under that agreement, or capped. transaction_types limit a rule to named types; type-specific agreements beat general ones, then the latest effective_from wins. Payments that name a transaction apply there first. Remaining payments apply FIFO to unpaid expected amounts for that agent. unpaid is expected minus paid. overpaid is paid above expected, including leftover unallocated payments. exposure is unpaid plus overpaid inside each currency. No ledger is fetched or stored. Docs: https://www.brainiac.software/api/agent-networks/commission-leakage",
      "parameters": {
        "type": "object",
        "properties": {
          "agents": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                }
              },
              "required": [
                "id",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "rules": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "fixed",
                    "percent",
                    "tiered",
                    "capped"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "rate_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "tiers": {
                  "minItems": 1,
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "up_to": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9007199254740991
                      },
                      "amount": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9007199254740991
                      },
                      "rate_bps": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 1000000
                      }
                    },
                    "additionalProperties": false
                  }
                },
                "cap": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_types": {
                  "minItems": 1,
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "kind"
              ],
              "additionalProperties": false
            }
          },
          "agreements": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "rule_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "effective_from": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "effective_to": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "agent_id",
                "rule_id",
                "effective_from"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "type_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "id",
                "agent_id",
                "type_id",
                "amount",
                "date"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "transaction_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "id",
                "agent_id",
                "amount",
                "date"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "agents",
          "rules",
          "agreements",
          "transactions",
          "payments"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__float-rebalancing",
      "description": "Rebalance agent float. Propose the cheapest cash transfers that lift every agent to its minimum float after expected demand. projected_before is cash_balance minus expected_demand. Surplus is cash above the minimum; shortage is the shortfall below the minimum. Allowed corridors come only from transfer_costs. transfer_limits cap a corridor. maximum_float caps how much a receiver can take. budget caps total transfer cost. Currencies are never mixed. Allocation is successive shortest-path min-cost flow on the surplus-to-shortage network. The response is a proposal only; no transfer is initiated. feasibility explains when shortages remain. Docs: https://www.brainiac.software/api/agent-networks/float-rebalancing",
      "parameters": {
        "type": "object",
        "properties": {
          "agents": {
            "minItems": 2,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "cash_balance": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "minimum_float": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "maximum_float": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "expected_demand": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "currency",
                "cash_balance",
                "minimum_float"
              ],
              "additionalProperties": false
            }
          },
          "transfer_costs": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from_agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "cost_per_unit": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "from_agent_id",
                "to_agent_id",
                "cost_per_unit"
              ],
              "additionalProperties": false
            }
          },
          "transfer_limits": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from_agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "max_amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "from_agent_id",
                "to_agent_id",
                "max_amount"
              ],
              "additionalProperties": false
            }
          },
          "budget": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "agents",
          "transfer_costs"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__liquidity-cost-analysis",
      "description": "Analyze liquidity cost. Calculate the cost of holding cash and electronic float for the supplied period. Funding from funding_rate_bps or funding_costs, replenishment costs, collection costs, and transfer fees are actual expenses. Idle capital from idle_periods and cost_of_capital_bps is an opportunity cost. Rates annualize with annualization_days (default 365): floor(balance * rate_bps * days / (10000 * annualization_days)). Currencies are never mixed. lines and formulas show every intermediate. No ledger is fetched or stored. Docs: https://www.brainiac.software/api/agent-networks/liquidity-cost-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "period_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "annualization_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "cost_of_capital_bps": {
            "type": "integer",
            "minimum": 0,
            "maximum": 1000000
          },
          "agents": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "cash_float": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "electronic_float": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_count": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "funding_rate_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "cost_of_capital_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "required": [
                "id",
                "currency",
                "cash_float",
                "electronic_float",
                "transaction_count"
              ],
              "additionalProperties": false
            }
          },
          "funding_costs": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "agent_id",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "replenishments": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "cost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "agent_id",
                "amount",
                "cost"
              ],
              "additionalProperties": false
            }
          },
          "collections": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "cost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "agent_id",
                "amount",
                "cost"
              ],
              "additionalProperties": false
            }
          },
          "transfer_fees": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "agent_id",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "idle_periods": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "days": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3660
                }
              },
              "required": [
                "agent_id",
                "amount",
                "days"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "period_days",
          "agents"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__outlet-performance-benchmark",
      "description": "Benchmark outlet performance. Compare caller-supplied outlet productivity inside peer groups of category:currency. Metrics are transactions per active day, revenue per operating hour from commission, average transaction value, commission per transaction, operating cost per transaction, and cash utilization_bps when capacity is supplied. When active_days or operating_hours are present, ranking uses the normalized per-day and per-hour figures instead of raw totals. productivity_score is the sum of competition ranks across available metrics; lower is better. explanations and formulas document every metric. No industry benchmark or external market data is used. Docs: https://www.brainiac.software/api/agent-networks/outlet-performance-benchmark",
      "parameters": {
        "type": "object",
        "properties": {
          "outlets": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "category": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transaction_count": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "active_days": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 3660
                },
                "operating_hours": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 100000
                },
                "commission": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "operating_cost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "cash_available": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "cash_capacity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "currency",
                "transaction_count",
                "transaction_value",
                "commission",
                "operating_cost"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "outlets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__cash-denomination-optimization",
      "description": "Optimize cash denominations. Plan note and coin acquisitions so agents can fulfil caller-supplied cash-in and cash-out amounts. denominations define the only currency systems used; none are assumed. Cash-out and change use largest-first greedy composition against on-hand quantities, preferring notes above minimum_reserves before dipping into reserves. Cash-in adds a greedy composition of tender (defaulting to amount) then dispenses change of tender minus amount. Recommended acquisitions cover shortage compositions and reserve top-ups, capped by replenishment.max_quantity. minimum_cash_required is starting inventory value plus recommended acquisitions. No replenishment is initiated. Docs: https://www.brainiac.software/api/agent-networks/cash-denomination-optimization",
      "parameters": {
        "type": "object",
        "properties": {
          "denominations": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "value": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "currency",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "agents": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "inventory": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 9007199254740991
                      },
                      "quantity": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9007199254740991
                      }
                    },
                    "required": [
                      "value",
                      "quantity"
                    ],
                    "additionalProperties": false
                  }
                },
                "minimum_reserves": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "value": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 9007199254740991
                      },
                      "quantity": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 9007199254740991
                      }
                    },
                    "required": [
                      "value",
                      "quantity"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "currency",
                "inventory"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "direction": {
                  "type": "string",
                  "enum": [
                    "in",
                    "out"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "tender": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "agent_id",
                "direction",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "replenishment": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "value": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "max_quantity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "agent_id",
                "value",
                "max_quantity"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "denominations",
          "agents",
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__outlet-capacity-allocation",
      "description": "Allocate outlet capacity. Distribute caller-supplied demand across outlets that share the demand location, support the service type, and have operating hours in the interval. Interval capacity is capacity_per_hour times hours, and when staffing is supplied it is also limited by staff_count times staff_capacity_per_hour times hours. Demand is allocated in demand id order to the eligible outlet with the most remaining capacity, then by outlet id. utilization_bps is floor(allocated * 10000 / capacity). capacity_required is the extra allocated volume still needed to reach each supplied fulfil_bps target. No map, geocoder, or demand database is used. Docs: https://www.brainiac.software/api/agent-networks/outlet-capacity-allocation",
      "parameters": {
        "type": "object",
        "properties": {
          "outlets": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "location_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "service_types": {
                  "minItems": 1,
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                },
                "capacity_per_hour": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "staff_count": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "staff_capacity_per_hour": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "operating_hours": {
                  "minItems": 1,
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "interval_id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "hours": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 24
                      }
                    },
                    "required": [
                      "interval_id",
                      "hours"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "location_id",
                "service_types",
                "capacity_per_hour",
                "operating_hours"
              ],
              "additionalProperties": false
            }
          },
          "demand": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "location_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "interval_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "service_type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transactions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "location_id",
                "interval_id",
                "service_type",
                "transactions"
              ],
              "additionalProperties": false
            }
          },
          "service_level_targets": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "location_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "interval_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "service_type": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "fulfil_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "required": [
                "fulfil_bps"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "outlets",
          "demand"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__agent-concentration-risk",
      "description": "Measure agent concentration risk. Measure how concentrated caller-supplied agent, outlet, and operator activity is. For transaction_volume, transaction_value, and revenue, compute share_bps, top-n concentration ratios, HHI = floor(sum(share_bps^2) / 10000), and dependency rankings overall, per entity kind, and for each supplied segment dimension/label. Outage scenarios remove unavailable_ids, report affected volume/value/revenue, and compare affected volume with remaining entities' replacement_capacity. No industry HHI threshold is invented or applied. Docs: https://www.brainiac.software/api/agent-networks/agent-concentration-risk",
      "parameters": {
        "type": "object",
        "properties": {
          "entities": {
            "minItems": 1,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "agent",
                    "outlet",
                    "operator"
                  ]
                },
                "transaction_volume": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "revenue": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "segments": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "dimension": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "label": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      }
                    },
                    "required": [
                      "dimension",
                      "label"
                    ],
                    "additionalProperties": false
                  }
                },
                "replacement_capacity": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "kind",
                "transaction_volume",
                "transaction_value",
                "revenue"
              ],
              "additionalProperties": false
            }
          },
          "outages": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "unavailable_ids": {
                  "minItems": 1,
                  "maxItems": 200,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "id",
                "unavailable_ids"
              ],
              "additionalProperties": false
            }
          },
          "top_counts": {
            "minItems": 1,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100
            }
          }
        },
        "required": [
          "entities"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__dormant-outlet-detect",
      "description": "Detect dormant outlets. Classify caller-supplied outlets as active, declining, temporarily inactive, permanently inactive, seasonal, suspended, closed, never active, or not yet active. Open days follow the supplied weekday schedule (or every day when omitted) excluding dates covered by closure, suspension, or seasonal status records. Inactivity uses open days after the last transaction through as_of_date against inactive_days_threshold and permanent_days_threshold. Decline compares recent_days volume with the preceding baseline window. Every outlet row includes evidence strings. No external dormancy threshold is invented. Docs: https://www.brainiac.software/api/agent-networks/dormant-outlet-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "as_of_date": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "inactive_days_threshold": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "permanent_days_threshold": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "decline_bps_threshold": {
            "type": "integer",
            "minimum": 0,
            "maximum": 1000000
          },
          "baseline_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "recent_days": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "outlets": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "activation_date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "expected_transactions_per_active_day": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "count": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "outlet_id",
                "date"
              ],
              "additionalProperties": false
            }
          },
          "schedules": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "weekday": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 6
                }
              },
              "required": [
                "outlet_id",
                "weekday"
              ],
              "additionalProperties": false
            }
          },
          "status_records": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "outlet_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "closure",
                    "suspension",
                    "seasonal"
                  ]
                },
                "start_date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "end_date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                }
              },
              "required": [
                "outlet_id",
                "kind",
                "start_date"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "as_of_date",
          "outlets",
          "transactions"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__cash-replenishment-route-plan",
      "description": "Plan cash replenishment routes. Build capacitated cash replenishment routes for caller-supplied outlets, depots, and vehicles. Distances prefer directed distances[] entries and otherwise use rounded haversine meters from coordinates, labeled supplied versus straight_line. Routes use nearest-neighbor construction, intra-route 2-opt, and a cheapest-feasible insertion pass. Optional time windows use minutes_per_distance_unit for travel. No mapping, routing, or external optimization API is called. Docs: https://www.brainiac.software/api/agent-networks/cash-replenishment-route-plan",
      "parameters": {
        "type": "object",
        "properties": {
          "outlets": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "replenishment_amount": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "window_start_minute": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100800
                },
                "window_end_minute": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100800
                },
                "service_minutes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100800
                },
                "delivery_cost": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "id",
                "replenishment_amount"
              ],
              "additionalProperties": false
            }
          },
          "depots": {
            "minItems": 1,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "latitude": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "longitude": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "vehicles": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "depot_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "capacity": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "cost_per_distance_unit": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "max_route_distance": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 9007199254740991
                },
                "max_stops": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 500
                },
                "ready_minute": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100800
                },
                "due_minute": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 100800
                }
              },
              "required": [
                "id",
                "depot_id",
                "capacity"
              ],
              "additionalProperties": false
            }
          },
          "distances": {
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "distance": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "from_id",
                "to_id",
                "distance"
              ],
              "additionalProperties": false
            }
          },
          "minutes_per_distance_unit": {
            "type": "integer",
            "minimum": 0,
            "maximum": 60
          }
        },
        "required": [
          "outlets",
          "depots",
          "vehicles"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__settlement-reconciliation",
      "description": "Reconcile agent settlements. Reconcile caller-supplied agent transactions against provider settlement statement rows. Confirmed matches require a unique settlement.transaction_id, a unique settlement.reference equal to transaction.settlement_reference, or a unique currency+amount pair. Ambiguous candidates are listed separately and are never treated as confirmed. Amount and fee deltas, missing settlements, unmatched credits, and duplicate reference groups are returned with evidence. No FX conversion is applied. Docs: https://www.brainiac.software/api/agent-networks/settlement-reconciliation",
      "parameters": {
        "type": "object",
        "properties": {
          "transactions": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "occurred_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "fee": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "settlement_reference": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "id",
                "amount",
                "currency",
                "occurred_at"
              ],
              "additionalProperties": false
            }
          },
          "settlements": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "settled_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "fee": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "reference": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "settlement",
                    "credit",
                    "fee",
                    "adjustment"
                  ]
                }
              },
              "required": [
                "id",
                "amount",
                "currency",
                "settled_at"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "transactions",
          "settlements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__shift-handover-audit",
      "description": "Audit shift cash handovers. Audit consecutive agent shifts for cash and electronic-float handovers. Expected balances use opening amounts plus supplied transaction totals and adjustments. Actual balances prefer cash_count and electronic_float_balance when present. Missing handover records between consecutive same-agent shifts, inconsistent handed amounts, and unexplained deltas are reported. No external till balance is invented. Docs: https://www.brainiac.software/api/agent-networks/shift-handover-audit",
      "parameters": {
        "type": "object",
        "properties": {
          "shifts": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "started_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "ended_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "opening_cash": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "closing_cash": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "opening_float": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "closing_float": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "cash_count": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "electronic_float_balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "transaction_cash_in": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_cash_out": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_float_in": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_float_out": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "adjustments": {
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      },
                      "kind": {
                        "type": "string",
                        "enum": [
                          "cash",
                          "float"
                        ]
                      },
                      "amount": {
                        "type": "integer",
                        "minimum": -9007199254740991,
                        "maximum": 9007199254740991
                      },
                      "reason": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 240
                      }
                    },
                    "required": [
                      "id",
                      "kind",
                      "amount"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id",
                "agent_id",
                "started_at",
                "ended_at",
                "opening_cash",
                "closing_cash",
                "opening_float",
                "closing_float"
              ],
              "additionalProperties": false
            }
          },
          "handovers": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "from_shift_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "to_shift_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "cash_handed": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "float_handed": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "recorded_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                }
              },
              "required": [
                "id",
                "from_shift_id",
                "to_shift_id",
                "cash_handed",
                "float_handed"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "shifts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__failed-transaction-dispute",
      "description": "Assess failed transaction disputes. Investigate customer disputes where a charge is claimed against a failed, reversed, or pending agent transaction. Reconstruct a timeline only from supplied lifecycle events, receipts, reversals, and the dispute claim. Report conflicting evidence, missing lifecycle steps, possible duplicate receipts, and reversal inconsistencies. Successful payment is never inferred without a supplied settled fact. Docs: https://www.brainiac.software/api/agent-networks/failed-transaction-dispute",
      "parameters": {
        "type": "object",
        "properties": {
          "dispute": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "transaction_id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "customer_claimed_amount": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Z]{3}$"
              },
              "claimed_at": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
              },
              "customer_detail": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              }
            },
            "required": [
              "id",
              "transaction_id",
              "customer_claimed_amount",
              "currency",
              "claimed_at"
            ],
            "additionalProperties": false
          },
          "events": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transaction_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "initiated",
                    "authorized",
                    "provider_response",
                    "pending",
                    "failed",
                    "reversed",
                    "settled",
                    "receipt_issued",
                    "customer_claim",
                    "agent_note"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "provider_code": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                },
                "source": {
                  "type": "string",
                  "enum": [
                    "provider",
                    "agent",
                    "customer",
                    "system"
                  ]
                }
              },
              "required": [
                "id",
                "transaction_id",
                "at",
                "type"
              ],
              "additionalProperties": false
            }
          },
          "receipts": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transaction_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "issued_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "issued",
                    "void"
                  ]
                }
              },
              "required": [
                "id",
                "transaction_id",
                "amount",
                "issued_at"
              ],
              "additionalProperties": false
            }
          },
          "reversals": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transaction_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "reversed_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "posted",
                    "pending",
                    "failed"
                  ]
                }
              },
              "required": [
                "id",
                "transaction_id",
                "amount",
                "reversed_at"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "dispute",
          "events"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__terminal-downtime-impact",
      "description": "Measure terminal downtime impact. Quantify agent terminal outages using supplied availability intervals, historical day totals, and optional per-hour averages. measured_* values come only from history rows on the outage start date. estimated_lost_* values come only from supplied averages. Restoration priority ranks terminals by estimated lost commission, then value, then transactions, then downtime. No market demand model is invented. Docs: https://www.brainiac.software/api/agent-networks/terminal-downtime-impact",
      "parameters": {
        "type": "object",
        "properties": {
          "terminals": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "agent_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "location_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "outages": {
            "minItems": 1,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "terminal_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "started_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "ended_at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                }
              },
              "required": [
                "id",
                "terminal_id",
                "started_at",
                "ended_at"
              ],
              "additionalProperties": false
            }
          },
          "history": {
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "terminal_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "transaction_count": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "transaction_value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "commission": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "active_minutes": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 1440
                }
              },
              "required": [
                "terminal_id",
                "date",
                "transaction_count"
              ],
              "additionalProperties": false
            }
          },
          "averages": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "terminal_id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "transactions_per_hour": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "average_transaction_value": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "commission_bps": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1000000
                }
              },
              "required": [
                "terminal_id",
                "transactions_per_hour"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "terminals",
          "outages"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "agent-networks__agent-dispute-evidence",
      "description": "Build agent dispute evidence. Package caller-supplied agent and operator records into a chronological evidence timeline for financial disputes. Balance transitions are checked against intervening signed amounts. Conflicting references, unexplained balance changes, and missing records for declared dispute categories are labeled separately from verified supplied facts. No liability outcome is assigned and no compensating transactions are invented. Docs: https://www.brainiac.software/api/agent-networks/agent-dispute-evidence",
      "parameters": {
        "type": "object",
        "properties": {
          "dispute": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "agent_id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Z]{3}$"
              },
              "disputed_amount": {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 9007199254740991
              },
              "opened_at": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
              },
              "categories": {
                "minItems": 1,
                "maxItems": 10,
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": [
                    "balance",
                    "commission",
                    "reversal",
                    "cash_deposit",
                    "settlement_deduction",
                    "other"
                  ]
                }
              },
              "detail": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              }
            },
            "required": [
              "id",
              "agent_id",
              "currency",
              "disputed_amount",
              "opened_at",
              "categories"
            ],
            "additionalProperties": false
          },
          "records": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "at": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,3})?Z$"
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "transaction",
                    "balance_snapshot",
                    "commission",
                    "settlement",
                    "cash_deposit",
                    "reversal",
                    "adjustment",
                    "note"
                  ]
                },
                "amount": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Z]{3}$"
                },
                "balance": {
                  "type": "integer",
                  "minimum": -9007199254740991,
                  "maximum": 9007199254740991
                },
                "reference": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "detail": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 500
                }
              },
              "required": [
                "id",
                "at",
                "kind"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "dispute",
          "records"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "agent-networks__float-loss-attribution": "0.04",
  "agent-networks__cash-shortage-analysis": "0.04",
  "agent-networks__terminal-profitability": "0.04",
  "agent-networks__commission-leakage": "0.04",
  "agent-networks__float-rebalancing": "0.04",
  "agent-networks__liquidity-cost-analysis": "0.04",
  "agent-networks__outlet-performance-benchmark": "0.04",
  "agent-networks__cash-denomination-optimization": "0.04",
  "agent-networks__outlet-capacity-allocation": "0.04",
  "agent-networks__agent-concentration-risk": "0.04",
  "agent-networks__dormant-outlet-detect": "0.04",
  "agent-networks__cash-replenishment-route-plan": "0.04",
  "agent-networks__settlement-reconciliation": "0.04",
  "agent-networks__shift-handover-audit": "0.04",
  "agent-networks__failed-transaction-dispute": "0.04",
  "agent-networks__terminal-downtime-impact": "0.04",
  "agent-networks__agent-dispute-evidence": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "agent-networks__float-loss-attribution": "agent-networks/float-loss-attribution",
  "agent-networks__cash-shortage-analysis": "agent-networks/cash-shortage-analysis",
  "agent-networks__terminal-profitability": "agent-networks/terminal-profitability",
  "agent-networks__commission-leakage": "agent-networks/commission-leakage",
  "agent-networks__float-rebalancing": "agent-networks/float-rebalancing",
  "agent-networks__liquidity-cost-analysis": "agent-networks/liquidity-cost-analysis",
  "agent-networks__outlet-performance-benchmark": "agent-networks/outlet-performance-benchmark",
  "agent-networks__cash-denomination-optimization": "agent-networks/cash-denomination-optimization",
  "agent-networks__outlet-capacity-allocation": "agent-networks/outlet-capacity-allocation",
  "agent-networks__agent-concentration-risk": "agent-networks/agent-concentration-risk",
  "agent-networks__dormant-outlet-detect": "agent-networks/dormant-outlet-detect",
  "agent-networks__cash-replenishment-route-plan": "agent-networks/cash-replenishment-route-plan",
  "agent-networks__settlement-reconciliation": "agent-networks/settlement-reconciliation",
  "agent-networks__shift-handover-audit": "agent-networks/shift-handover-audit",
  "agent-networks__failed-transaction-dispute": "agent-networks/failed-transaction-dispute",
  "agent-networks__terminal-downtime-impact": "agent-networks/terminal-downtime-impact",
  "agent-networks__agent-dispute-evidence": "agent-networks/agent-dispute-evidence"
}


class BrainiacAgentNetworksAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — agent-networks",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the agent-networks catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "agent-networks", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Attribute agent float loss"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the agent-networks group. "
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
