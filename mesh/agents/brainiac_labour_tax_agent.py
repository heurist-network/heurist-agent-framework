"""Auto-generated BRAINIAC Heurist Mesh agent for group `labour-tax` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "labour-tax__uk-minimum-wage-lookup",
      "description": "Look up UK National Minimum Wage. Return the official GOV.UK National Minimum / Living Wage hourly rate for a date and age/apprentice category from vendored rate rows. Docs: https://www.brainiac.software/api/labour-tax/uk-minimum-wage-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "minLength": 8,
            "maxLength": 32
          },
          "category": {
            "type": "string",
            "enum": [
              "age_21_plus",
              "age_18_to_20",
              "under_18",
              "apprentice"
            ]
          }
        },
        "required": [
          "asOf",
          "category"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__us-minimum-wage-lookup",
      "description": "Look up US federal minimum wage. Return the federal FLSA minimum wage for a date. State and local rates are not included in this slice. Docs: https://www.brainiac.software/api/labour-tax/us-minimum-wage-lookup",
      "parameters": {
        "type": "object",
        "properties": {
          "asOf": {
            "type": "string",
            "minLength": 8,
            "maxLength": 32
          },
          "jurisdiction": {
            "default": "federal",
            "type": "string",
            "enum": [
              "federal"
            ]
          }
        },
        "required": [
          "asOf"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__uk-holiday-entitlement-calculate",
      "description": "Calculate UK statutory holiday entitlement. Estimate statutory holiday entitlement days from weeks worked in the leave year and days worked per week, using the GOV.UK 5.6-week baseline. Docs: https://www.brainiac.software/api/labour-tax/uk-holiday-entitlement-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "weeksWorkedInLeaveYear": {
            "type": "number",
            "minimum": 0,
            "maximum": 53
          },
          "daysWorkedPerWeek": {
            "type": "number",
            "minimum": 0,
            "maximum": 7
          },
          "statutoryWeeks": {
            "default": 5.6,
            "type": "number",
            "minimum": 0,
            "maximum": 8
          }
        },
        "required": [
          "weeksWorkedInLeaveYear",
          "daysWorkedPerWeek"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__iana-timezone-convert",
      "description": "Convert a timestamp between IANA time zones. Convert an instant between IANA time zones using the runtime Intl/tzdb revision. Coordinate-to-zone lookup is not included. Docs: https://www.brainiac.software/api/labour-tax/iana-timezone-convert",
      "parameters": {
        "type": "object",
        "properties": {
          "instant": {
            "type": "string",
            "minLength": 8,
            "maxLength": 64
          },
          "fromTimeZone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "toTimeZone": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          }
        },
        "required": [
          "instant",
          "fromTimeZone",
          "toTimeZone"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__business-day-calendar",
      "description": "Business day calendar (UK/US). Report whether a date is a business day on the England & Wales, Scotland, Northern Ireland or US federal holiday calendar, with the holiday name and previous/next business days. Docs: https://www.brainiac.software/api/labour-tax/business-day-calendar",
      "parameters": {
        "type": "object",
        "properties": {
          "date": {
            "type": "string",
            "minLength": 8,
            "maxLength": 32
          },
          "calendar": {
            "default": "england-wales",
            "type": "string",
            "enum": [
              "england-wales",
              "gb-eaw",
              "gb-sct",
              "gb-nir",
              "us-federal"
            ]
          }
        },
        "required": [
          "date"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__uk-statutory-pay-calculate",
      "description": "Calculate UK statutory pay (SSP, SMP, SAP, SPP, ShPP, SPBP, SNCP). Calculate Statutory Sick Pay and statutory maternity, adoption, paternity, shared parental, parental bereavement and neonatal care pay for tax year 2026-27 from caller-supplied average weekly earnings. Docs: https://www.brainiac.software/api/labour-tax/uk-statutory-pay-calculate",
      "parameters": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "SSP",
              "SMP",
              "SAP",
              "SPP",
              "ShPP",
              "SPBP",
              "SNCP"
            ]
          },
          "averageWeeklyEarnings": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000
          },
          "startDate": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "weeks": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 52
          },
          "ssp": {
            "type": "object",
            "properties": {
              "qualifyingDaysPerWeek": {
                "type": "integer",
                "minimum": 1,
                "maximum": 7
              },
              "daysToPay": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10000
              }
            },
            "required": [
              "qualifyingDaysPerWeek",
              "daysToPay"
            ],
            "additionalProperties": false
          },
          "smpEligibility": {
            "type": "object",
            "properties": {
              "continuousEmployment26Weeks": {
                "type": "boolean"
              },
              "noticeGiven": {
                "type": "boolean"
              }
            },
            "required": [
              "continuousEmployment26Weeks",
              "noticeGiven"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "type",
          "averageWeeklyEarnings",
          "startDate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__uk-paye-ni-estimate",
      "description": "Estimate UK PAYE income tax and National Insurance. Estimate income tax and Class 1 employee and employer National Insurance for one pay period at constant pay in tax year 2026-27 (rUK, Scotland and Wales bands). Not a payslip. Docs: https://www.brainiac.software/api/labour-tax/uk-paye-ni-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "grossPay": {
            "type": "number",
            "minimum": 0,
            "maximum": 100000000
          },
          "period": {
            "type": "string",
            "enum": [
              "weekly",
              "monthly",
              "annual"
            ]
          },
          "taxCode": {
            "type": "string",
            "minLength": 2,
            "maxLength": 16
          },
          "niCategory": {
            "default": "A",
            "type": "string",
            "enum": [
              "A",
              "B",
              "C",
              "D",
              "E",
              "F",
              "H",
              "I",
              "J",
              "K",
              "L",
              "M",
              "N",
              "S",
              "V",
              "Z"
            ]
          }
        },
        "required": [
          "grossPay",
          "period"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__us-federal-withholding-estimate",
      "description": "Estimate US federal income-tax withholding (Pub 15-T 2026). Compute federal income-tax withholding for one pay period using IRS Publication 15-T (2026) Worksheet 1A and the Annual Percentage Method tables. FICA is not included. Docs: https://www.brainiac.software/api/labour-tax/us-federal-withholding-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "taxYear": {
            "type": "number",
            "const": 2026
          },
          "wagesThisPeriod": {
            "type": "number",
            "minimum": 0,
            "maximum": 100000000
          },
          "payFrequency": {
            "type": "string",
            "enum": [
              "daily",
              "weekly",
              "biweekly",
              "semimonthly",
              "monthly",
              "quarterly",
              "semiannually"
            ]
          },
          "w4": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "formYear": {
                    "type": "string",
                    "const": "2020-or-later"
                  },
                  "filingStatus": {
                    "type": "string",
                    "enum": [
                      "single_or_mfs",
                      "mfj",
                      "hoh"
                    ]
                  },
                  "step2Checkbox": {
                    "type": "boolean"
                  },
                  "step3Credits": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100000000
                  },
                  "step4aOtherIncome": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100000000
                  },
                  "step4bDeductions": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100000000
                  },
                  "step4cExtra": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100000000
                  }
                },
                "required": [
                  "formYear",
                  "filingStatus",
                  "step2Checkbox"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "formYear": {
                    "type": "string",
                    "const": "2019-or-earlier"
                  },
                  "maritalStatus": {
                    "type": "string",
                    "enum": [
                      "single",
                      "married"
                    ]
                  },
                  "allowances": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 1000
                  },
                  "additional": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100000000
                  }
                },
                "required": [
                  "formYear",
                  "maritalStatus",
                  "allowances"
                ],
                "additionalProperties": false
              }
            ]
          },
          "nonresidentAlien": {
            "type": "boolean"
          }
        },
        "required": [
          "taxYear",
          "wagesThisPeriod",
          "payFrequency",
          "w4"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "labour-tax__uk-sponsor-register-search",
      "description": "Search the UK licensed sponsor register. Check whether an organisation appears on the vendored Home Office Register of licensed sponsors (Worker and Temporary Worker). Returns candidate matches for human review. Docs: https://www.brainiac.software/api/labour-tax/uk-sponsor-register-search",
      "parameters": {
        "type": "object",
        "properties": {
          "organisationName": {
            "type": "string",
            "minLength": 2,
            "maxLength": 200
          },
          "town": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "route": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
          },
          "limit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          }
        },
        "required": [
          "organisationName"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "labour-tax__uk-minimum-wage-lookup": "0.01",
  "labour-tax__us-minimum-wage-lookup": "0.02",
  "labour-tax__uk-holiday-entitlement-calculate": "0.02",
  "labour-tax__iana-timezone-convert": "0.01",
  "labour-tax__business-day-calendar": "0.02",
  "labour-tax__uk-statutory-pay-calculate": "0.03",
  "labour-tax__uk-paye-ni-estimate": "0.03",
  "labour-tax__us-federal-withholding-estimate": "0.03",
  "labour-tax__uk-sponsor-register-search": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "labour-tax__uk-minimum-wage-lookup": "labour-tax/uk-minimum-wage-lookup",
  "labour-tax__us-minimum-wage-lookup": "labour-tax/us-minimum-wage-lookup",
  "labour-tax__uk-holiday-entitlement-calculate": "labour-tax/uk-holiday-entitlement-calculate",
  "labour-tax__iana-timezone-convert": "labour-tax/iana-timezone-convert",
  "labour-tax__business-day-calendar": "labour-tax/business-day-calendar",
  "labour-tax__uk-statutory-pay-calculate": "labour-tax/uk-statutory-pay-calculate",
  "labour-tax__uk-paye-ni-estimate": "labour-tax/uk-paye-ni-estimate",
  "labour-tax__us-federal-withholding-estimate": "labour-tax/us-federal-withholding-estimate",
  "labour-tax__uk-sponsor-register-search": "labour-tax/uk-sponsor-register-search"
}


class BrainiacLabourTaxAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — labour-tax",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the labour-tax catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "labour-tax", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Look up UK National Minimum Wage"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the labour-tax group. "
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
