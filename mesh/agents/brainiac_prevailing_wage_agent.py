"""Auto-generated BRAINIAC Heurist Mesh agent for group `prevailing-wage` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "prevailing-wage__search",
      "description": "Search Davis-Bacon wage determinations. Search Davis-Bacon wage determinations by state, county, construction type, or award/bid date. Results include source details and an indicator when a record may be out of date. Docs: https://www.brainiac.software/api/prevailing-wage/search",
      "parameters": {
        "type": "object",
        "properties": {
          "state": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
          },
          "county": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "constructionType": {
            "type": "string",
            "enum": [
              "building",
              "residential",
              "highway",
              "heavy"
            ]
          },
          "awardBidDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "query": {
            "type": "string",
            "maxLength": 120
          },
          "limit": {
            "default": 50,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__resolve",
      "description": "Resolve a wage determination. Resolve an active determination by state, county, construction type, and award/bid date. Unmatched determinations are not inferred. Docs: https://www.brainiac.software/api/prevailing-wage/resolve",
      "parameters": {
        "type": "object",
        "properties": {
          "state": {
            "type": "string",
            "minLength": 2,
            "maxLength": 2
          },
          "county": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "constructionType": {
            "type": "string",
            "enum": [
              "building",
              "residential",
              "highway",
              "heavy"
            ]
          },
          "awardBidDate": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          }
        },
        "required": [
          "state",
          "county",
          "constructionType",
          "awardBidDate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__classification-rates",
      "description": "Read classification rates. Return sourced base/fringe rates, notes, zones, and excerpts for a wage determination. Docs: https://www.brainiac.software/api/prevailing-wage/classification-rates",
      "parameters": {
        "type": "object",
        "properties": {
          "wdId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "craft": {
            "type": "string",
            "maxLength": 120
          }
        },
        "required": [
          "wdId"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__classification-validate",
      "description": "Validate a labor classification. Use deterministic keyword matching against a selected wage determination. Ambiguous work is routed for human conformance review. Docs: https://www.brainiac.software/api/prevailing-wage/classification-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "wdId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "duties": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          },
          "trade": {
            "type": "string",
            "maxLength": 120
          }
        },
        "required": [
          "wdId",
          "duties"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__conformance-draft",
      "description": "Draft a classification conformance request. Prepare optional SF-1444 request language from caller-supplied facts. Human review and contracting-officer submission are required; this is not an approved classification or rate. Docs: https://www.brainiac.software/api/prevailing-wage/conformance-draft",
      "parameters": {
        "type": "object",
        "properties": {
          "projectName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          },
          "wdId": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "duties": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          },
          "proposedClassification": {
            "type": "string",
            "maxLength": 120
          },
          "proposedRate": {
            "type": "number",
            "minimum": 0
          },
          "rationale": {
            "type": "string",
            "maxLength": 4000
          }
        },
        "required": [
          "projectName",
          "wdId",
          "duties"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__payroll-precheck",
      "description": "Precheck certified payroll. Run deterministic DBRA checks against a wage determination. This is a compliance precheck, not a certified government filing. Docs: https://www.brainiac.software/api/prevailing-wage/payroll-precheck",
      "parameters": {
        "type": "object",
        "properties": {
          "wdId": {
            "type": "string",
            "minLength": 1
          },
          "weekEnding": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "cwhssaCovered": {
            "type": "boolean"
          },
          "project": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              },
              "contractNumber": {
                "type": "string",
                "maxLength": 120
              },
              "payrollNumber": {
                "type": "string",
                "maxLength": 120
              },
              "contractor": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              },
              "location": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              }
            },
            "required": [
              "name",
              "contractor",
              "address",
              "location"
            ],
            "additionalProperties": false
          },
          "workers": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "middleInitial": {
                  "type": "string",
                  "maxLength": 1
                },
                "identifyingNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8,
                  "description": "Use a worker-specific ID or last four digits only; never enter a full SSN."
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "J",
                    "RA"
                  ]
                },
                "apprenticeLevel": {
                  "type": "string",
                  "maxLength": 80
                },
                "classification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "hoursOtherWork": {
                  "type": "number",
                  "minimum": 0,
                  "description": "Hours this worker worked for the week on other work, in addition to the listed project. Enter 0 when none."
                },
                "days": {
                  "minItems": 7,
                  "maxItems": 7,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "date": {
                        "type": "string",
                        "format": "date",
                        "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                      },
                      "straight": {
                        "default": 0,
                        "type": "number",
                        "minimum": 0,
                        "maximum": 24
                      },
                      "overtime": {
                        "default": 0,
                        "type": "number",
                        "minimum": 0,
                        "maximum": 24
                      }
                    },
                    "required": [
                      "date"
                    ],
                    "additionalProperties": false
                  }
                },
                "straightRate": {
                  "type": "number",
                  "minimum": 0
                },
                "overtimeRate": {
                  "type": "number",
                  "minimum": 0
                },
                "fringeCreditHourly": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "cashInLieuHourly": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "grossProject": {
                  "type": "number",
                  "minimum": 0
                },
                "grossAllWork": {
                  "type": "number",
                  "minimum": 0
                },
                "taxWithheld": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "ficaWithheld": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "otherDeductions": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "netAllWork": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "lastName",
                "firstName",
                "identifyingNumber",
                "status",
                "classification",
                "hoursOtherWork",
                "days",
                "straightRate",
                "overtimeRate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "wdId",
          "weekEnding",
          "cwhssaCovered",
          "project",
          "workers"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__fringe-reconcile",
      "description": "Reconcile fringe credits. Compare annualized benefit contributions and cash-in-lieu with the supplied required hourly fringe. Inputs and findings are returned for review. Docs: https://www.brainiac.software/api/prevailing-wage/fringe-reconcile",
      "parameters": {
        "type": "object",
        "properties": {
          "planCostAnnual": {
            "type": "number",
            "minimum": 0
          },
          "annualHours": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "projectHours": {
            "type": "number",
            "minimum": 0
          },
          "reportedPlanContribution": {
            "type": "number",
            "minimum": 0
          },
          "reportedCashInLieu": {
            "type": "number",
            "minimum": 0
          },
          "requiredFringeHourly": {
            "type": "number",
            "minimum": 0
          }
        },
        "required": [
          "planCostAnnual",
          "annualHours",
          "projectHours",
          "reportedPlanContribution",
          "reportedCashInLieu",
          "requiredFringeHourly"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "prevailing-wage__payroll-report",
      "description": "Build payroll report files. Generate an editable XLSX and a minimal PDF summary after DBRA precheck. Output is not a prescribed government form. Docs: https://www.brainiac.software/api/prevailing-wage/payroll-report",
      "parameters": {
        "type": "object",
        "properties": {
          "wdId": {
            "type": "string",
            "minLength": 1
          },
          "weekEnding": {
            "type": "string",
            "format": "date",
            "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
          },
          "cwhssaCovered": {
            "type": "boolean"
          },
          "project": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              },
              "contractNumber": {
                "type": "string",
                "maxLength": 120
              },
              "payrollNumber": {
                "type": "string",
                "maxLength": 120
              },
              "contractor": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              },
              "address": {
                "type": "string",
                "minLength": 1,
                "maxLength": 500
              },
              "location": {
                "type": "string",
                "minLength": 1,
                "maxLength": 240
              }
            },
            "required": [
              "name",
              "contractor",
              "address",
              "location"
            ],
            "additionalProperties": false
          },
          "workers": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "lastName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "firstName": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "middleInitial": {
                  "type": "string",
                  "maxLength": 1
                },
                "identifyingNumber": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 8,
                  "description": "Use a worker-specific ID or last four digits only; never enter a full SSN."
                },
                "status": {
                  "type": "string",
                  "enum": [
                    "J",
                    "RA"
                  ]
                },
                "apprenticeLevel": {
                  "type": "string",
                  "maxLength": 80
                },
                "classification": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "hoursOtherWork": {
                  "type": "number",
                  "minimum": 0,
                  "description": "Hours this worker worked for the week on other work, in addition to the listed project. Enter 0 when none."
                },
                "days": {
                  "minItems": 7,
                  "maxItems": 7,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "date": {
                        "type": "string",
                        "format": "date",
                        "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                      },
                      "straight": {
                        "default": 0,
                        "type": "number",
                        "minimum": 0,
                        "maximum": 24
                      },
                      "overtime": {
                        "default": 0,
                        "type": "number",
                        "minimum": 0,
                        "maximum": 24
                      }
                    },
                    "required": [
                      "date"
                    ],
                    "additionalProperties": false
                  }
                },
                "straightRate": {
                  "type": "number",
                  "minimum": 0
                },
                "overtimeRate": {
                  "type": "number",
                  "minimum": 0
                },
                "fringeCreditHourly": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "cashInLieuHourly": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "grossProject": {
                  "type": "number",
                  "minimum": 0
                },
                "grossAllWork": {
                  "type": "number",
                  "minimum": 0
                },
                "taxWithheld": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "ficaWithheld": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "otherDeductions": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                },
                "netAllWork": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "lastName",
                "firstName",
                "identifyingNumber",
                "status",
                "classification",
                "hoursOtherWork",
                "days",
                "straightRate",
                "overtimeRate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "wdId",
          "weekEnding",
          "cwhssaCovered",
          "project",
          "workers"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "prevailing-wage__search": "0.01",
  "prevailing-wage__resolve": "0.01",
  "prevailing-wage__classification-rates": "0.01",
  "prevailing-wage__classification-validate": "0.02",
  "prevailing-wage__conformance-draft": "0.01",
  "prevailing-wage__payroll-precheck": "0.05",
  "prevailing-wage__fringe-reconcile": "0.02",
  "prevailing-wage__payroll-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "prevailing-wage__search": "prevailing-wage/search",
  "prevailing-wage__resolve": "prevailing-wage/resolve",
  "prevailing-wage__classification-rates": "prevailing-wage/classification-rates",
  "prevailing-wage__classification-validate": "prevailing-wage/classification-validate",
  "prevailing-wage__conformance-draft": "prevailing-wage/conformance-draft",
  "prevailing-wage__payroll-precheck": "prevailing-wage/payroll-precheck",
  "prevailing-wage__fringe-reconcile": "prevailing-wage/fringe-reconcile",
  "prevailing-wage__payroll-report": "prevailing-wage/payroll-report"
}


class BrainiacPrevailingWageAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — prevailing-wage",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the prevailing-wage catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "prevailing-wage", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Search Davis-Bacon wage determinations"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the prevailing-wage group. "
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
