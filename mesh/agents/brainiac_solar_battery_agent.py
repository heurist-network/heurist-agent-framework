"""Auto-generated BRAINIAC Heurist Mesh agent for group `solar-battery` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "solar-battery__generation-deviation-detect",
      "description": "Detect solar generation deviations. Compare supplied solar generation kWh to expected kWh and flag deviations. Missing expected values are not invented. Docs: https://www.brainiac.software/api/solar-battery/generation-deviation-detect",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__panel-degradation-estimate",
      "description": "Estimate solar panel degradation. Estimate panel degradation from supplied nameplate/prior and measured capacity over time. Missing baselines are not invented. Docs: https://www.brainiac.software/api/solar-battery/panel-degradation-estimate",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__inverter-fault-classify",
      "description": "Classify solar inverter faults. Classify supplied inverter log events using a caller fault map or keyword signals in supplied messages. Cloud catalogs are not queried. Docs: https://www.brainiac.software/api/solar-battery/inverter-fault-classify",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__cycle-aging-analyze",
      "description": "Analyze battery cycle aging. Analyze supplied battery cycle counts, depth of discharge, and throughput. Rated cycle life is used only when supplied. Docs: https://www.brainiac.software/api/solar-battery/cycle-aging-analyze",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__state-of-health-estimate",
      "description": "Estimate battery state of health. Estimate battery SOH from supplied sohPct or measured versus nameplate energy. Missing capacities are not invented. Docs: https://www.brainiac.software/api/solar-battery/state-of-health-estimate",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__warranty-threshold-check",
      "description": "Check battery warranty thresholds. Compare supplied SOH, cycles, and calendar age to caller-supplied warranty thresholds. Legal warranty coverage is not determined. Docs: https://www.brainiac.software/api/solar-battery/warranty-threshold-check",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__round-trip-efficiency",
      "description": "Calculate battery round-trip efficiency. Calculate round-trip efficiency from supplied charge and discharge energy for each period. Docs: https://www.brainiac.software/api/solar-battery/round-trip-efficiency",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__storage-self-consumption",
      "description": "Calculate solar storage self-consumption. Calculate self-consumption and self-sufficiency from supplied generation, load, and optional import/export energy. Docs: https://www.brainiac.software/api/solar-battery/storage-self-consumption",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__asset-compare",
      "description": "Compare distributed energy assets. Compare supplied solar/storage assets on generation deviation, SOH, efficiency, and self-consumption metrics derived only from caller records. Docs: https://www.brainiac.software/api/solar-battery/asset-compare",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-battery__performance-report",
      "description": "Build solar battery performance report. Aggregate generation deviation, degradation, inverter faults, cycle aging, SOH, warranty, efficiency, self-consumption, and asset comparison from caller-supplied records only. Docs: https://www.brainiac.software/api/solar-battery/performance-report",
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
          "generation": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "kwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "expectedKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "irradiance": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "panels": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "nameplateKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "measuredAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "priorMeasuredKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "priorMeasuredAt": {
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
          "inverterEvents": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "message": {
                  "type": "string",
                  "maxLength": 500
                },
                "severity": {
                  "type": "string",
                  "maxLength": 40
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryCycles": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "depthOfDischargePct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "throughputKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "batteryHealth": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "nameplateKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "measuredKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "cycleCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "ratedCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "sohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "measuredAt": {
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
          "warranties": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "minSohPct": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "maxCycles": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "maxCalendarYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "installedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "asOf": {
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
          "efficiencyPeriods": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "periodStart": {
                  "type": "string",
                  "maxLength": 40
                },
                "periodEnd": {
                  "type": "string",
                  "maxLength": 40
                },
                "chargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "dischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "consumption": {
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "assetId": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "generationKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "loadKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridImportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "gridExportKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryChargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "batteryDischargeKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "assets": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "maxLength": 160
                },
                "kind": {
                  "type": "string",
                  "maxLength": 80
                },
                "capacityKw": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "capacityKwh": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "installedAt": {
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
          "faultMap": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "code": {
                  "type": "string",
                  "maxLength": 80
                },
                "label": {
                  "type": "string",
                  "maxLength": 160
                },
                "category": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "solar-battery__generation-deviation-detect": "0.04",
  "solar-battery__panel-degradation-estimate": "0.04",
  "solar-battery__inverter-fault-classify": "0.04",
  "solar-battery__cycle-aging-analyze": "0.04",
  "solar-battery__state-of-health-estimate": "0.04",
  "solar-battery__warranty-threshold-check": "0.03",
  "solar-battery__round-trip-efficiency": "0.03",
  "solar-battery__storage-self-consumption": "0.04",
  "solar-battery__asset-compare": "0.05",
  "solar-battery__performance-report": "0.08"
}
TOOL_ROUTES: Dict[str, str] = {
  "solar-battery__generation-deviation-detect": "solar-battery/generation-deviation-detect",
  "solar-battery__panel-degradation-estimate": "solar-battery/panel-degradation-estimate",
  "solar-battery__inverter-fault-classify": "solar-battery/inverter-fault-classify",
  "solar-battery__cycle-aging-analyze": "solar-battery/cycle-aging-analyze",
  "solar-battery__state-of-health-estimate": "solar-battery/state-of-health-estimate",
  "solar-battery__warranty-threshold-check": "solar-battery/warranty-threshold-check",
  "solar-battery__round-trip-efficiency": "solar-battery/round-trip-efficiency",
  "solar-battery__storage-self-consumption": "solar-battery/storage-self-consumption",
  "solar-battery__asset-compare": "solar-battery/asset-compare",
  "solar-battery__performance-report": "solar-battery/performance-report"
}


class BrainiacSolarBatteryAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — solar-battery",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the solar-battery catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "solar-battery", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect solar generation deviations"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the solar-battery group. "
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
